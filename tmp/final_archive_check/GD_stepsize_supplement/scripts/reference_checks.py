#!/usr/bin/env python3
"""Numerical regression tests for the paper's scalar recurrences.

These floating-point tests are not proofs and do not certify the limiting OBS-F
profile. The exhaustive reference implementation checks every ordered split.
"""
from __future__ import annotations
import argparse, json, math, platform, time
from pathlib import Path
import numpy as np

RHO = 1.0 + math.sqrt(2.0)
P = math.log2(RHO)

def kernel(x, y):
    return (x + y + np.sqrt(x*x + 6*x*y + y*y)) / 2.0

def join_f(u, w):
    return (4*u + w + np.sqrt(w*w + 8*u*w)) / 2.0

def balanced_table(n: int) -> np.ndarray:
    if n < 1:
        raise ValueError('n must be positive')
    u = np.zeros(n+1, dtype=np.float64); u[1] = 1.0
    start = 1
    while start < n:
        idx = np.arange(start+1, min(2*start, n)+1, dtype=np.int64)
        u[idx] = kernel(u[idx//2], u[(idx+1)//2])
        start *= 2
    return u

def evaluate_u(n: int) -> float:
    if n < 1:
        raise ValueError('n must be positive')
    a, b = 0.0, 1.0
    for bit in bin(n)[2:]:
        c = float(kernel(a, b))
        a, b = (RHO*a, c) if bit == '0' else (c, RHO*b)
    return a

def maximizing_splits(n: int) -> list[int]:
    if n < 2:
        return []
    power = n & -n; odd = n // power
    if odd == 1:
        return [n//2]
    if power == 1:
        return [(n-1)//2, (n+1)//2]
    return [(odd-1)*power//2, odd*power//2, (odd+1)*power//2]

def exhaustive_obsf(n: int, u: np.ndarray | None = None):
    if n < 1:
        raise ValueError('n must be positive')
    if u is None:
        u = balanced_table(n)
    w = np.zeros(n+1); w[1] = 1.0
    pivot = np.zeros(n+1, dtype=np.int64)
    for N in range(2, n+1):
        values = join_f(u[1:N], w[N-1:0:-1])
        idx = int(np.argmax(values)); pivot[N] = idx+1; w[N] = values[idx]
    return w, pivot

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--obsf-level', type=int, default=12)
    ap.add_argument('--phi-level', type=int, default=22)
    ap.add_argument('--output', type=Path, default=Path('checks/numerical_checks.json'))
    args=ap.parse_args()
    if not 1 <= args.obsf_level <= 18 or not 1 <= args.phi_level <= 22:
        ap.error('supported OBS-F levels: 1..18; symmetric levels: 1..22')
    begin=time.perf_counter()
    n=2**(args.phi_level+1)
    # Low-resolution CLI runs still need enough values for all regression tests.
    u=balanced_table(max(n,4096,2**(args.obsf_level+1)))
    table_time=time.perf_counter()-begin
    errors=[abs(evaluate_u(N)/u[N]-1) for N in range(1,4097)]
    bad=[]
    for N in range(2,257):
        values=kernel(u[1:N],u[N-1:0:-1]); mx=values.max()
        got=(np.flatnonzero(np.abs(values-mx) <= 5e-13*mx)+1).tolist()
        if got != maximizing_splits(N): bad.append(N)
    idx=np.arange(2**args.phi_level,n+1,dtype=np.int64)
    vals=u[idx]/np.power(idx.astype(float),P); j=int(np.argmin(vals)); Nmin=int(idx[j])
    phi={'level':args.phi_level,'sampled_minimum':float(vals[j]),'minimizing_N':Nmin,
         'sampled_minimum_phase':math.log2(Nmin)-args.phi_level,
         'nonconstancy_witness':evaluate_u(3)/3**P}
    # Main panel: floating-point balanced recurrence, sampled for display only.
    chosen=np.unique(np.r_[np.linspace(0,len(idx)-1,4097,dtype=int),j])
    figdir=args.output.parent.parent/'figures'; figdir.mkdir(parents=True,exist_ok=True)
    np.savetxt(figdir/'phi_compact_curve.dat',np.c_[np.log2(idx[chosen]/2**args.phi_level),vals[chosen]],
               header='t value',comments='',fmt='%.12g')
    Nf=2**(args.obsf_level+1); t=time.perf_counter(); w,piv=exhaustive_obsf(Nf,u)
    runtime=time.perf_counter()-t
    idxf=np.arange(2**args.obsf_level,Nf+1); cf=idxf.astype(float)**P/w[idxf]
    prev=np.arange(2**(args.obsf_level-1),2**args.obsf_level+1)
    tprev=np.log2(prev/2**(args.obsf_level-1)); vprev=prev.astype(float)**P/w[prev]
    tf=np.log2(idxf/2**args.obsf_level)
    diff=float(np.max(np.abs(cf-np.interp(tf,tprev,vprev))))
    sandwich=bool(np.all(w[1:] >= (2*u[1:Nf+1]-1)*(1-2e-13)) and
                  np.all(w[1:] <= RHO*u[1:Nf+1]*(1+2e-13)))
    report={'python':platform.python_version(),'numpy':np.__version__,
            'classification':'floating-point numerical regression; not a proof',
            'binary_evaluator_test_N_max':4096,'max_relative_binary_error':max(errors),
            'symmetric_all_splits_test_N_max':256,'split_mismatch_N':bad,
            'symmetric_table_seconds':table_time,'symmetric_phase':phi,
            'obsf':{'level':args.obsf_level,'maximum_N':Nf,'ordered_candidates':Nf*(Nf-1)//2,
                    'seconds':runtime,'sampled_minimum':float(cf.min()),'sampled_maximum':float(cf.max()),
                    'successive_scale_difference':diff,'sandwich_test_passed':sandwich},
            'total_seconds':time.perf_counter()-begin}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
    if bad or max(errors)>1e-12 or not sandwich:
        raise SystemExit('Regression check failed')

if __name__=='__main__': main()
