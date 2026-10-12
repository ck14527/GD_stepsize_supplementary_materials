#!/usr/bin/env python3
"""Export the review supplement using an explicit allowlist and SHA-256 manifest.

Proof sources and historical evidence are never rewritten. Author metadata,
manuscript PDFs, internal notes, caches, and build products are excluded. This
mechanical check cannot guarantee contextual anonymity of mathematical content.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_ROOT = 'GD_stepsize_supplement'
ROOT_FILES = {
    'README.md', 'NUMERICAL_REPRODUCIBILITY.md', 'LEAN_FORMALIZATION.md',
    'REVIEWER_GUIDE.md', 'requirements.txt',
}
SCRIPT_FILES = {
    'build.sh', 'check_bundled_data.py', 'check_phase_certificate.py',
    'export_anonymous.py', 'obsf_exhaustive.cpp', 'prepare_phase_plots.py',
    'reference_checks.py', 'verify_project.py', 'test_export.py', 'check_plot_support.py',
}
CHECK_FILES = {
    'README.md', 'environment.json', 'interval_checks.json', 'interval_run.txt',
    'numerical_checks.json', 'obsf_19.csv.gz', 'obsf_exhaustive_run.txt',
    'obsf_full_checks.json', 'original_result_inventory.json',
    'package_checks.json', 'plot_run.txt', 'preflight.json', 'reference_run.txt',
    'source_baseline.json',
}
LEAN_FILES = {'GD.lean', 'README.md', 'CONTRIBUTING.md', 'lean-toolchain',
              'lakefile.toml', 'lake-manifest.json'}
LEAN_AUDIT_FILES = {
    'README.md', 'build_provenance.json', 'corner_rational_certificate.json',
    'coverage.json', 'dag_check.json', 'inventory.csv', 'inventory.json',
    'lean_declarations.json', 'lean_theorem_graph.json', 'proof_graph_render.json',
    'run_checks.json', 'structure_check.json', 'theorem_signatures.json',
}
FORBIDDEN_PARTS = {
    '.git', '.lake', '.venv', '__pycache__', 'node_modules', 'author_notes',
    'tmp', 'dist', 'build',
}
TEXT_SUFFIXES = {'.md', '.py', '.sh', '.cpp', '.lean', '.toml', '.json', '.csv',
                 '.txt', '.dat', '.tex', '.html', '.svg', '.dot'}


def allowed(name: str) -> bool:
    """Only reviewer inputs and explicitly selected historical outputs enter ZIPs."""
    path = PurePosixPath(name)
    parts = path.parts
    if (not parts or path.is_absolute() or '..' in parts or '\\' in name
            or ':' in name or set(parts) & FORBIDDEN_PARTS):
        return False
    if len(parts) == 1:
        return name in ROOT_FILES
    if len(parts) == 2:
        if parts[0] == 'scripts':
            return parts[1] in SCRIPT_FILES
        if parts[0] == 'checks':
            return parts[1] in CHECK_FILES
        if parts[0] == 'figures':
            return path.suffix in {'.dat', '.tex', '.pdf'}
        if parts[0] == 'lean':
            return parts[1] in LEAN_FILES
    if parts[:3] == ('checks', 'current', 'reviewer'):
        return len(parts) == 4 and path.suffix == '.json'
    if name == 'checks/current/plot_checks.json':
        return True
    if name == 'checks/revision/package_validation.json':
        return True
    if parts[0] == 'lean' and len(parts) >= 3:
        if parts[1] == 'GD':
            return path.suffix == '.lean'
        if parts[1] == 'docs':
            return path.suffix in {'.md', '.json', '.csv'}
        if parts[1] == 'graphs':
            return path.suffix in {'.svg', '.dot', '.html'}
        if parts[1] == 'tools':
            return len(parts) == 3 and parts[2] in {'check_snapshot.py', 'run_checks.py'}
        if parts[1] == 'audit':
            return len(parts) == 3 and parts[2] in LEAN_AUDIT_FILES
    return False


def identity_tokens(root: Path) -> list[str]:
    """Use private local metadata for screening; never distribute those tokens."""
    path = root / 'lean/repository.json'
    if not path.exists():
        return []
    meta = json.loads(path.read_text(encoding='utf-8'))
    tokens = [meta.get(k, '') for k in ('owner', 'url', 'paper_arxiv_id')]
    for author in meta.get('paper_authors', []):
        given, family = author.get('given-names', ''), author.get('family-names', '')
        if given and family:
            tokens.extend([f'{given} {family}', f'{family}, {given}'])
    return [token for token in tokens if len(token) > 3]


def privacy_issues(name: str, data: bytes, tokens: list[str]) -> list[str]:
    path = PurePosixPath(name)
    if path.suffix == '.pdf':
        try:
            import fitz
        except ImportError as exc:
            raise RuntimeError('PDF export screening requires PyMuPDF; install requirements.txt.') from exc
        with fitz.open(stream=data, filetype='pdf') as document:
            metadata = document.metadata
            issues = ['nonempty PDF author metadata'] if metadata.get('author', '').strip() else []
            text = '\n'.join(str(v) for v in metadata.values() if v)
            text += '\n' + document.get_xml_metadata()
            text += '\n' + '\n'.join(page.get_text() for page in document)
    elif path.suffix in TEXT_SUFFIXES or path.name == 'lean-toolchain':
        issues = []
        text = data.decode('utf-8')
    else:
        return []
    # Split literals so that this source file does not trigger its own scanner.
    personal_path = re.compile(r'(?i)(?:[a-z]:[\\/](?:Users|Documents and Settings)[\\/][^\s"<>]+|/'
                               r'(?:home|Users)/[^\s"<>]+|file:' + r'//[^\s"<>]+)')
    if personal_path.search(text):
        issues.append('absolute personal path or file URL')
    folded = text.casefold()
    if any(token.casefold() in folded for token in tokens):
        issues.append('identity token from private repository metadata')
    return issues


def collect_entries(root: Path) -> list[tuple[str, bytes]]:
    entries = []
    tokens = identity_tokens(root)
    candidates = []
    for folder, directories, files in os.walk(root, followlinks=False):
        directories[:] = sorted(d for d in directories if d not in FORBIDDEN_PARTS)
        candidates.extend(Path(folder)/name for name in files)
    for path in sorted(candidates):
        name = path.relative_to(root).as_posix()
        if not allowed(name) or not path.is_file():
            continue
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f'Refusing linked file: {name}')
        data = path.read_bytes()
        issues = privacy_issues(name, data, tokens)
        if issues:
            raise ValueError(f'Anonymity screen failed: {name}: {", ".join(issues)}')
        entries.append((name, data))
    required = {'README.md', 'NUMERICAL_REPRODUCIBILITY.md', 'LEAN_FORMALIZATION.md',
                'requirements.txt', 'checks/README.md', 'checks/obsf_19.csv.gz',
                'lean/GD.lean', 'lean/lean-toolchain', 'lean/lakefile.toml',
                'lean/lake-manifest.json', 'lean/audit/build_provenance.json',
                'lean/audit/lean_declarations.json', 'lean/tools/check_snapshot.py',
                'scripts/verify_project.py'}
    missing = required - {name for name, _ in entries}
    if missing:
        raise ValueError(f'Missing required supplement files: {sorted(missing)}')
    return entries


def export(root: Path, output: Path) -> dict:
    entries = collect_entries(root)
    manifest = ''.join(f'{hashlib.sha256(data).hexdigest()}  {name}\n'
                       for name, data in entries).encode('utf-8')
    output.parent.mkdir(parents=True, exist_ok=True)
    # A fixed timestamp makes identical inputs produce an identical archive.
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name, data in [*entries, ('SHA256SUMS', manifest)]:
            info = zipfile.ZipInfo(f'{ARCHIVE_ROOT}/{name}', date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data, compresslevel=6)
    return {'archive_name': output.name, 'entries': len(entries) + 1,
            'bytes': output.stat().st_size,
            'sha256': hashlib.sha256(output.read_bytes()).hexdigest(),
            'privacy_screen_passed': True,
            'contextual_anonymity_guaranteed': False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', nargs='?', type=Path,
                        default=ROOT/'dist/GD_stepsize_supplement.zip')
    args = parser.parse_args()
    output = args.output.resolve()
    if output.suffix.lower() != '.zip':
        parser.error('output must have a .zip extension')
    print(json.dumps(export(ROOT, output), indent=2))


if __name__ == '__main__':
    main()
