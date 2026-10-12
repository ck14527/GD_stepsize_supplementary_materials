#!/usr/bin/env python3
"""Regression check for the asymmetric support barrier; not a formal proof.

Independently solve Lemma E.5 at high precision and check both the plotting
implementation and the exported line. This catches the former unrelated
closed-form constant and a correct value accidentally clipped by the axis.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import mpmath as mp
from prepare_phase_plots import C_STAR


def main() -> None:
    mp.mp.dps = 60
    p = mp.log(1 + mp.sqrt(2)) / mp.log(2)
    q = 1 / p
    xi = mp.findroot(lambda x: x ** (2*q-1) * (2-x) - 1,
                     (mp.mpf('0.4'), mp.mpf('0.6')))
    support = 2**q * (1-xi**(2*q)) / (1-xi)**q
    expected = support**(-p)
    root = Path(__file__).resolve().parents[1]
    tex = (root/'figures/psi_phase_compact.tex').read_text(encoding='utf-8')
    match = re.search(r'coordinates\s*\{\(0,([0-9.]+)\)\s*\(1,([0-9.]+)\)\}', tex)
    axes = re.search(r'ymin=([0-9.]+),ymax=([0-9.]+)', tex)
    if match is None or axes is None:
        raise ValueError('Missing support line or vertical range in compact panel')
    plotted = [float(x) for x in match.groups()]
    ymin, ymax = map(float, axes.groups())
    checks = {
        'interior_root': 0 < xi < 1,
        'script_matches_independent_support_value': abs(C_STAR-float(expected)) < 2e-14,
        'exported_line_matches_support_value': all(abs(x-float(expected)) < 2e-14 for x in plotted),
        'support_line_inside_vertical_range': all(ymin < x < ymax for x in plotted),
    }
    report = {
        'classification': 'Independent high-precision numerical regression; not interval or Lean certification',
        'xi_star': str(xi), 'B_sup': str(support), 'c_star': str(expected),
        'checks': checks, 'passed': all(checks.values()),
    }
    output = root/'checks/current/reviewer/plot_support.json'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    if not report['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
