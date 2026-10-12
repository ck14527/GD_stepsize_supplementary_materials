#!/usr/bin/env python3
"""Check the actual supplementary package; optionally run small numerical checks.

This is not a manuscript compilation, PDF layout check, or Lean kernel rebuild.
Historical audit logs are evidence from earlier runs, never new test results.
The default structural and hash checks use only Python's standard library.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    'README.md', 'NUMERICAL_REPRODUCIBILITY.md', 'LEAN_FORMALIZATION.md',
    'requirements.txt', 'checks/README.md', 'checks/obsf_19.csv.gz',
    'scripts/reference_checks.py', 'scripts/check_bundled_data.py',
    'scripts/check_phase_certificate.py', 'scripts/obsf_exhaustive.cpp',
    'lean/README.md', 'lean/GD.lean', 'lean/lean-toolchain', 'lean/lakefile.toml',
    'lean/lake-manifest.json', 'lean/GD/Targets.lean', 'lean/GD/Paper/Symmetric.lean',
    'lean/GD/Paper/Asymmetric.lean', 'lean/docs/THEOREMS.md',
    'lean/audit/build_provenance.json', 'lean/audit/lean_declarations.json',
    'lean/tools/check_snapshot.py',
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest_check(root: Path) -> dict:
    manifest = root / 'SHA256SUMS'
    if not manifest.exists():
        return {'present': False, 'passed': None, 'note': 'Manifest is added by anonymous export.'}
    issues, names = [], set()
    for line in manifest.read_text(encoding='utf-8').splitlines():
        try:
            expected, name = line.split('  ', 1)
        except ValueError:
            issues.append('malformed manifest line')
            continue
        path = PurePosixPath(name)
        if path.is_absolute() or '..' in path.parts or '\\' in name or ':' in name:
            issues.append('unsafe manifest path')
            continue
        if name in names:
            issues.append(f'duplicate manifest entry: {name}')
        names.add(name)
        target = root / name
        if not target.is_file() or sha256(target) != expected:
            issues.append(f'missing or changed: {name}')
    missing = REQUIRED - names
    issues.extend(f'required file not covered by manifest: {name}' for name in sorted(missing))
    return {'present': True, 'entries': len(names), 'issues': issues, 'passed': not issues}


def run_check(command: list[str], root: Path) -> dict:
    result = subprocess.run(command, cwd=root, text=True, capture_output=True)
    report = {'command': ['python' if part == sys.executable else part for part in command],
              'exit_code': result.returncode}
    if result.returncode:
        print(result.stdout, file=sys.stderr)
        print(result.stderr, file=sys.stderr)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--numerical', action='store_true',
                        help='also run OBS-F through N=2048 and bundled-data consistency checks')
    parser.add_argument('--output', type=Path, default=ROOT/'checks/rerun/package_validation.json')
    args = parser.parse_args()
    missing = sorted(name for name in REQUIRED if not (ROOT/name).is_file())
    manifest = manifest_check(ROOT)
    provenance = ROOT/'lean/audit/build_provenance.json'
    changed, checked = [], 0
    if provenance.exists():
        old = json.loads(provenance.read_text(encoding='utf-8'))
        for name, expected in old.get('files', {}).items():
            path = PurePosixPath(name)
            if path.is_absolute() or '..' in path.parts or '\\' in name or ':' in name:
                changed.append('unsafe historical hash path')
                continue
            target = ROOT/'lean'/name
            checked += 1
            if not target.is_file() or sha256(target) != expected:
                changed.append(name)
        exported = ROOT/'lean/audit/lean_declarations.json'
        if not exported.is_file() or sha256(exported) != old.get('elaborated_export_sha256'):
            changed.append('audit/lean_declarations.json')
    commands = []
    if not missing:
        commands.append(run_check([sys.executable, 'lean/tools/check_snapshot.py'], ROOT))
    if args.numerical and not missing:
        result_dir = args.output.resolve().parent/'numerical'
        commands.append(run_check([sys.executable, 'scripts/reference_checks.py',
                                   '--obsf-level', '10', '--phi-level', '12',
                                   '--output', str(result_dir/'reference/report.json')], ROOT))
        commands.append(run_check([sys.executable, 'scripts/check_bundled_data.py',
                                   '--output', str(result_dir/'bundled_data.json')], ROOT))
    for command in commands:
        command['command'] = [str(Path(x).relative_to(ROOT)).replace('\\', '/')
                              if Path(x).is_absolute() and Path(x).is_relative_to(ROOT) else x
                              for x in command['command']]
    report = {
        'classification': 'Current supplementary-package validation',
        'python': platform.python_version(),
        'missing_required_files': missing,
        'sha256_manifest': manifest,
        'historical_proof_input_hashes_checked': checked,
        'historical_proof_or_export_hash_mismatches': changed,
        'checks_executed': commands,
        'lean_kernel_rebuild_performed': False,
        'manuscript_compilation_or_layout_check_performed': False,
        'full_OBSF_run_performed_by_this_command': False,
        'level17_interval_run_performed_by_this_command': False,
        'historical_logs_overwritten': False,
    }
    report['passed'] = (not missing and not changed and manifest.get('passed') is not False
                        and all(c['exit_code'] == 0 for c in commands))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(report, indent=2))
    if not report['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
