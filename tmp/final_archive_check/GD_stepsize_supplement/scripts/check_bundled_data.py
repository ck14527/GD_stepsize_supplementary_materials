#!/usr/bin/env python3
"""Check the bundled OBS-F table without rerunning its large Bellman search.

These are floating-point consistency checks, not interval certification or a
proof that every stored Bellman value is globally maximizing. Optionally compare
a freshly generated small C++ table with the independent Python reference.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
import time
import numpy as np
from reference_checks import balanced_table, exhaustive_obsf

ROOT = Path(__file__).resolve().parents[1]

def load_table(path: Path) -> np.ndarray:
    table = np.loadtxt(path, delimiter=',', skiprows=1)
    if table.ndim != 2 or table.shape[1] != 4:
        raise ValueError(f'{path}: expected columns N,U_N,W_N,C_N')
    if not np.all(np.isfinite(table)):
        raise ValueError(f'{path}: table contains nonfinite values')
    n = np.arange(1, len(table)+1, dtype=np.int64)
    if not np.array_equal(table[:, 0], n):
        raise ValueError(f'{path}: leaf counts are not contiguous from 1')
    if not np.all(table[:, 1:] > 0):
        raise ValueError(f'{path}: scalar values must be positive')
    return table

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--data', type=Path, default=ROOT/'checks/obsf_19.csv.gz')
    ap.add_argument('--cpp-check', type=Path,
                    help='optional fresh C++ output through at most N=8192')
    ap.add_argument('--output', type=Path, default=ROOT/'checks/current/bundled_data.json')
    args = ap.parse_args()
    start = time.perf_counter()
    a = load_table(args.data)
    n = a[:, 0].astype(np.int64)
    if len(n) != 2**19:
        raise ValueError('The Figure 1 data check expects all N through 2^19.')
    rho = 1 + math.sqrt(2)
    p = math.log2(rho)
    expected_u = balanced_table(len(n))[1:]
    e_u = float(np.max(np.abs(a[:, 1]/expected_u-1)))
    e_c = float(np.max(np.abs(a[:, 3]/(n.astype(float)**p/a[:, 2])-1)))
    passed_u = e_u <= 2e-13
    passed_c = e_c <= 2e-13
    sandwich = bool(np.all(a[:, 2] >= (2*a[:, 1]-1)*(1-2e-13)) and
                    np.all(a[:, 2] <= rho*a[:, 1]*(1+2e-13)))
    take = n >= 2**18
    t = np.log2(n[take]/2**18)
    values = a[take, 3]
    prev = (n >= 2**17) & (n <= 2**18)
    tp = np.log2(n[prev]/2**17)
    diff = float(np.max(np.abs(values-np.interp(t, tp, a[prev, 3]))))
    i, j = int(np.argmin(values)), int(np.argmax(values))
    extrema_match = (round(float(values[i]), 8) == 0.42139019 and
                     round(float(values[j]), 8) == 0.42311312 and
                     round(diff/1e-7, 2) == 9.82)
    report = {
        'classification': 'Floating-point data consistency, not a new exhaustive large-scale run',
        'python': platform.python_version(), 'numpy': np.__version__,
        'data_sha256': hashlib.sha256(args.data.read_bytes()).hexdigest(),
        'rows': len(n), 'maximum_N': int(n[-1]),
        'symmetric_table_max_relative_error': e_u,
        'normalized_coefficient_max_relative_error': e_c,
        'symmetric_recurrence_consistent': passed_u,
        'normalized_coefficient_consistent': passed_c,
        'reciprocal_sandwich_passed': sandwich,
        'sampled_minimum': float(values[i]),
        'sampled_minimum_phase': float(t[i]),
        'sampled_maximum': float(values[j]),
        'sampled_maximum_phase': float(t[j]),
        'successive_scale_difference': diff,
        'rounded_annotations_match': extrema_match,
        'large_scale_bellman_search_rerun': False,
        'interval_certification_performed': False,
        'limiting_profile_error_bound_claimed': False,
    }
    passed_cpp = True
    if args.cpp_check:
        cpp = load_table(args.cpp_check)
        if len(cpp) > 8192:
            raise ValueError('Use a small C++ table (N<=8192) for the Python cross-check.')
        pu = balanced_table(len(cpp))
        pw, _ = exhaustive_obsf(len(cpp), pu)
        err = float(np.max(np.abs(cpp[:, 2]/pw[1:]-1)))
        passed_cpp = err <= 1e-12
        report['fresh_cpp_python_comparison'] = {
            'maximum_N': len(cpp), 'max_relative_W_error': err,
            'passed': passed_cpp,
        }
    report['seconds'] = time.perf_counter()-start
    report['passed'] = bool(passed_u and passed_c and sandwich and extrema_match and passed_cpp)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))
    if not report['passed']:
        raise SystemExit('A numerical package consistency check failed.')

if __name__ == '__main__':
    main()
