#!/usr/bin/env python3
"""Check the reported finite phase-minimum and dyadic-corner enclosures.

U_N is enclosed using exact integer arithmetic and integer square roots on a
fixed decimal grid. Noninteger powers and finite corner products use mpmath's
outward interval arithmetic at 60 decimal digits. This is a numerical interval
certificate, not a Lean formalization; the analytic implications are in the paper.
"""
from __future__ import annotations
import argparse, json, math, platform, time
from pathlib import Path
import mpmath
from mpmath import iv


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).resolve().parents[1]/'checks/current/reviewer/interval_checks.json',
                        help='Write a fresh report without overwriting inherited interval evidence.')
    args = parser.parse_args()
    iv.dps=60
    start=time.perf_counter(); level=17; maximum=2**(level+1)
    scale=10**45
    lo=[0]*(maximum+1); hi=[0]*(maximum+1); lo[1]=hi[1]=scale
    for n in range(2, maximum+1):
        a,b=lo[n//2],lo[(n+1)//2]
        lo[n]=(a+b+math.isqrt(a*a+6*a*b+b*b))//2
        a,b=hi[n//2],hi[(n+1)//2]
        rad=a*a+6*a*b+b*b; root=math.isqrt(rad)
        ceilroot=root if root*root==rad else root+1
        hi[n]=(a+b+ceilroot+1)//2
    rho=1+iv.sqrt(2); p=iv.log(rho)/iv.log(2)
    def u(n): return iv.mpf([lo[n],hi[n]])/scale
    lower_min_interval=iv.mpf(['0.9928123698','0.9928123700'])
    upper_min_interval=iv.mpf(['0.9928193322','0.9928193324'])
    denom=iv.power(2**level,p)
    lowwitness=upwitness=None
    low_witness_interval=up_witness_interval=None
    other_low=other_up=iv.mpf("+inf")
    for j in range(2**level,maximum):
        next_denom=iv.power(j+1,p)
        lower_candidate=u(j)/next_denom
        upper_candidate=u(j)/denom
        assert bool(lower_candidate > lower_min_interval.a), f'lower bound fails at {j}'
        assert bool(upper_candidate > upper_min_interval.a), f'upper-grid bound fails at {j}'
        if j==181314:
            assert bool(lower_candidate < lower_min_interval.b)
            lowwitness=str(lower_candidate)
            low_witness_interval=lower_candidate
        elif bool(lower_candidate.a < other_low):
            other_low=lower_candidate.a
        if j==181324:
            assert bool(upper_candidate < upper_min_interval.b)
            upwitness=str(upper_candidate)
            up_witness_interval=upper_candidate
        elif bool(upper_candidate.a < other_up):
            other_up=upper_candidate.a
        denom=next_denom
    end_candidate=u(maximum)/denom
    assert bool(end_candidate > upper_min_interval.a)
    if bool(end_candidate.a < other_up): other_up=end_candidate.a
    assert low_witness_interval is not None and up_witness_interval is not None
    assert bool(low_witness_interval.b < other_low)
    assert bool(up_witness_interval.b < other_up)
    # Validate the looser finite-product enclosures recorded in the source.
    def T0(r): return (1+r+iv.sqrt(r*r+6*r+1))/(2*rho)
    def T1(r): return rho*(iv.sqrt(r*r+6*r+1)-r-1)/2
    def w0(r): return 2*(T0(r)-1)/(r-1)
    def w1(r): return 2*(r-T0(r))/(r-1)
    x,y=T0(rho),T1(rho)
    pm,pp=(rho-1)*w0(rho),(rho-1)*w1(rho)
    for _ in range(6):
        pm=pm*w1(x); pp=pp*w0(y); x=T1(x); y=T0(y)
    bounds=[(x,'1.006713216536','1.006713216564'),
            (y,'1.006668059132','1.006668059134'),
            (pm,'1.419687938587','1.419687949396'),
            (pp,'1.419604771595','1.419604772437')]
    for value,a,b in bounds:
        assert bool(value > iv.mpf(a)) and bool(value < iv.mpf(b))
    assert bool(pm>pp)
    result={'classification':'exact integer enclosures plus 60-digit interval arithmetic',
            'python':platform.python_version(), 'mpmath':mpmath.__version__,
            'lean_kernel_verification':False,
            'level':level,'maximum_N':maximum,'fixed_point_decimal_places':45,
            'interval_decimal_digits':60,'all_grid_lower_bounds_passed':True,
            'lower_minimum_witness_N':181314,'lower_minimum_witness_interval':lowwitness,
            'upper_minimum_witness_N':181324,'upper_minimum_witness_interval':upwitness,
            'certified_phi_enclosure':['0.99281236','0.99281934'],
            'finite_grid_minimizing_indices_verified':True,
            'finite_grid_minimizers_unique_at_level_17':True,
            'limiting_profile_extremizer_uniqueness_claimed':False,
            'corner_finite_products_separated':True,'P_minus_6':str(pm),'P_plus_6':str(pp),
            'seconds':time.perf_counter()-start}
    dest=args.output
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(result,indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
