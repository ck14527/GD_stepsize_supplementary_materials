#!/usr/bin/env python3
"""Prepare compact PGFPlots panels for Figure 1.

The symmetric panel displays the exact leading objective-coefficient phase
1/(2 Phi(t)), sampled on a dyadic block via N^p/(2 U_N). The asymmetric panel
shows the finite-scale interpolant Psi_18(t) together with the structural
barrier c_*. No finite-scale plot is labeled as the exact limiting OBS-F
profile.
"""
from __future__ import annotations
import argparse, json, math, platform, subprocess
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RHO = 1.0 + math.sqrt(2.0)
P = math.log2(RHO)
def sharp_support_constant() -> float:
    """Evaluate c_* = B_sup^(-p) from Lemma E.5, equations (72)-(74).

    The desired root is the interior root of x^(2q-1)*(2-x)=1.
    Bisection is restricted to the increasing branch to avoid the root x=1.
    This floating-point value is for plotting, not an interval certificate.
    """
    q = 1.0 / P
    exponent = 2.0 * q - 1.0
    lo, hi = 0.0, 2.0 * exponent / (exponent + 1.0)
    for _ in range(80):
        mid = (lo + hi) / 2.0
        if mid ** exponent * (2.0 - mid) < 1.0:
            lo = mid
        else:
            hi = mid
    xi = (lo + hi) / 2.0
    support = 2.0 ** q * (1.0 - xi ** (2.0 * q)) / (1.0 - xi) ** q
    return support ** (-P)


C_STAR = sharp_support_constant()


def kernel(x, y):
    return (x + y + np.sqrt(x * x + 6.0 * x * y + y * y)) / 2.0


def balanced_table(n: int) -> np.ndarray:
    u = np.zeros(n + 1, dtype=np.float64)
    u[1] = 1.0
    start = 1
    while start < n:
        idx = np.arange(start + 1, min(2 * start, n) + 1, dtype=np.int64)
        u[idx] = kernel(u[idx // 2], u[(idx + 1) // 2])
        start *= 2
    return u


def write_symmetric_panel() -> dict:
    level = 22
    nmax = 2 ** (level + 1)
    u = balanced_table(nmax)
    idx = np.arange(2 ** level, nmax + 1, dtype=np.int64)
    t = np.log2(idx / 2 ** level)
    y = np.power(idx.astype(float), P) / (2.0 * u[idx])
    imax = int(np.argmax(y))
    chosen = np.unique(np.r_[np.linspace(0, len(idx) - 1, 4097, dtype=int), imax])
    np.savetxt(
        ROOT / 'figures' / 'phi_leading_compact_curve.dat',
        np.c_[t[chosen], y[chosen]],
        header='t value', comments='', fmt='%.12g')
    return {
        'symmetric_phase_level': level,
        'symmetric_leading_sampled_minimum': float(np.min(y)),
        'symmetric_leading_sampled_maximum': float(y[imax]),
        'symmetric_leading_maximizing_N': int(idx[imax]),
        'symmetric_leading_maximizing_phase': float(t[imax]),
        'symmetric_leading_endpoint_value': 0.5,
    }


def write_asymmetric_panel() -> dict:
    data_file = ROOT / 'checks' / 'obsf_19.csv'
    if not data_file.exists():
        data_file = ROOT / 'checks' / 'obsf_19.csv.gz'
    a = np.loadtxt(data_file, delimiter=',', skiprows=1)
    n = a[:, 0].astype(np.int64)
    c = a[:, 3]
    take = n >= 2 ** 18
    nn = n[take]
    cc = c[take]
    t = np.log2(nn / 2 ** 18)
    prev = (n >= 2 ** 17) & (n <= 2 ** 18)
    tp = np.log2(n[prev] / 2 ** 17)
    diff = float(np.max(np.abs(cc - np.interp(t, tp, c[prev]))))
    imin, imax = int(np.argmin(cc)), int(np.argmax(cc))
    chosen = np.unique(np.r_[np.linspace(0, len(t) - 1, 4097, dtype=int), imin, imax])
    np.savetxt(
        ROOT / 'figures' / 'psi_compact_curve.dat',
        np.c_[t[chosen], cc[chosen]],
        header='t value', comments='', fmt='%.12g')
    report = {
        'classification': 'float64 postprocessing of a supplied Bellman table; not a fresh exhaustive search',
        'large_bellman_search_rerun': False,
        'support_barrier_c_star': C_STAR,
        'support_barrier_definition': 'Lemma E.5, equations (72)-(74); floating-point evaluation',
        'max_N': int(n[-1]),
        'phase_level': 18,
        'ordered_candidates': int(n[-1]) * (int(n[-1]) - 1) // 2,
        'sampled_minimum': float(cc[imin]),
        'sampled_minimum_N': int(nn[imin]),
        'sampled_minimum_phase': float(t[imin]),
        'sampled_maximum': float(cc[imax]),
        'sampled_maximum_N': int(nn[imax]),
        'sampled_maximum_phase': float(t[imax]),
        'successive_scale_difference': diff,
        'reported_rounded_minimum_matches': round(float(cc[imin]), 8) == 0.42139019,
        'reported_rounded_maximum_matches': round(float(cc[imax]), 8) == 0.42311312,
        'reported_rounded_scale_difference_matches': round(diff / 1e-7, 2) == 9.82,
        'postprocessing_system': platform.platform(),
        'inherited_bellman_environment_file': 'checks/environment.json',
        'inherited_bellman_run_log': (ROOT / 'checks' / 'obsf_exhaustive_run.txt').read_text().strip(),
    }
    return report


def write_tex_files(panel: str = 'both') -> None:
    pre = r'''\documentclass[border=2pt]{standalone}
\usepackage{times,amsmath,pgfplots}
\pgfplotsset{compat=1.18}
\begin{document}
\begin{tikzpicture}
\begin{axis}[
 width=6.65cm,height=5.0cm,scale only axis=false,
 axis lines=left,xmin=0,xmax=1,xtick={0,.25,.5,.75,1},
 xticklabels={$0$,$0.25$,$0.5$,$0.75$,$1$},
 xlabel={Dyadic phase $t$},
 tick label style={font=\footnotesize},label style={font=\footnotesize},
 title style={font=\small},
 scaled ticks=false,yticklabel style={/pgf/number format/fixed,/pgf/number format/precision=3},
 tick align=outside,major tick length=2pt,
'''
    phi = pre + r'''title={(a) Symmetric: exact leading phase},
 ylabel={$\frac{1}{2\Phi(t)}$},ymin=.4998,ymax=.5039,
 ytick={.500,.502,.504},yticklabels={$0.500$,$0.502$,$0.504$}]
\addplot[thick,no marks] table[x=t,y=value] {phi_leading_compact_curve.dat};
\end{axis}
\end{tikzpicture}
\end{document}
'''
    psi = pre + rf'''title={{(b) Asymmetric: finite-scale interpolant}},
 ylabel={{$\Psi_{{18}}(t)$}},ymin=.4200,ymax=.4234,
 ytick={{.420,.421,.422,.423}},yticklabels={{$0.420$,$0.421$,$0.422$,$0.423$}}]
\addplot[semithick,densely dashed] coordinates {{(0,{C_STAR:.15f}) (1,{C_STAR:.15f})}};
\addplot[thick,no marks] table[x=t,y=value] {{psi_compact_curve.dat}};
\node[font=\scriptsize,anchor=south] at (axis cs:.86,{C_STAR + 0.00006:.6f}) {{$c_*$}};
\end{{axis}}
\end{{tikzpicture}}
\end{{document}}
'''
    for name, content in [('phi', phi), ('psi', psi)]:
        if panel != 'both' and panel != name:
            continue
        path = ROOT / 'figures' / f'{name}_phase_compact.tex'
        path.write_text(content)
        subprocess.run(
            ['pdflatex', '-interaction=nonstopmode', '-halt-on-error', path.name],
            cwd=path.parent, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=True,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--panel', choices=['both', 'phi', 'psi'], default='both',
                        help='Regenerate only the selected panel, or both (default).')
    args = parser.parse_args()
    symm = write_symmetric_panel() if args.panel in ('both', 'phi') else {}
    asymm = write_asymmetric_panel() if args.panel in ('both', 'psi') else {}
    report = asymm | symm
    report_path = ROOT / 'checks' / 'current' / 'plot_checks.json'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    write_tex_files(args.panel)
    if asymm and not all(report[k] for k in [
        'reported_rounded_minimum_matches',
        'reported_rounded_maximum_matches',
        'reported_rounded_scale_difference_matches',
    ]):
        raise SystemExit('Reported asymmetric values differ: inspect JSON before using plots')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
