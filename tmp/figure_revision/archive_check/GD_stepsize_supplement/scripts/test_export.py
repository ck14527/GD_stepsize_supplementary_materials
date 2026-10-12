#!/usr/bin/env python3
"""Regression tests for supplement allowlisting, anonymity screening and hashes."""
from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
import zipfile

from export_anonymous import ARCHIVE_ROOT, allowed, export, privacy_issues
from verify_project import REQUIRED, manifest_check


class PackagingTests(unittest.TestCase):
    def test_review_inputs_are_allowed(self):
        for name in ['README.md', 'lean/GD/Paper/Symmetric.lean', 'lean/GD.lean',
                     'lean/lake-manifest.json', 'lean/tools/check_snapshot.py',
                     'lean/audit/build_provenance.json', 'checks/obsf_19.csv.gz',
                     'checks/current/reviewer/reference.json']:
            self.assertTrue(allowed(name), name)

    def test_private_and_generated_files_are_excluded(self):
        for name in ['GD_stepsize_schedule.pdf', 'author_notes/MANUSCRIPT_EDITS.md',
                     'SUBMISSION_REVIEW_zh.md', 'lean/CITATION.cff',
                     'lean/repository.json', 'lean/.git/config',
                     'lean/.lake/build/lib/GD.olean', 'scripts/private.txt',
                     'figures/psi_phase_compact.log', 'build/obsf_exhaustive.exe',
                     'other.zip', '../README.md', '/README.md', '']:
            self.assertFalse(allowed(name), name)

    def test_personal_path_and_identity_screen(self):
        personal = '/'.join(['C:', 'Users', 'ExamplePerson', 'file.txt'])
        self.assertTrue(privacy_issues('README.md', personal.encode(), []))
        self.assertTrue(privacy_issues('README.md', b'Example Author', ['Example Author']))
        self.assertEqual(privacy_issues('README.md', b'Anonymous supplement', []), [])

    def test_manifest_detects_tampering(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            lines = []
            for name in sorted(REQUIRED):
                path = root/name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b'fixture')
                lines.append(f'{hashlib.sha256(b"fixture").hexdigest()}  {name}\n')
            (root/'SHA256SUMS').write_text(''.join(lines), encoding='utf-8')
            self.assertTrue(manifest_check(root)['passed'])
            (root/'README.md').write_bytes(b'changed')
            self.assertFalse(manifest_check(root)['passed'])

    def test_archive_manifest_and_reproducibility(self):
        entries = [('README.md', b'review input'), ('lean/GD.lean', b'import GD.Targets\n')]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with patch('export_anonymous.collect_entries', return_value=entries):
                first = export(root, root/'one.zip')
                second = export(root, root/'two.zip')
            self.assertEqual(first['sha256'], second['sha256'])
            with zipfile.ZipFile(root/'one.zip') as archive:
                self.assertEqual(len(archive.namelist()), len(entries)+1)
                self.assertIsNone(archive.testzip())
                manifest = archive.read(f'{ARCHIVE_ROOT}/SHA256SUMS').decode()
                for name, data in entries:
                    self.assertEqual(archive.read(f'{ARCHIVE_ROOT}/{name}'), data)
                    self.assertIn(f'{hashlib.sha256(data).hexdigest()}  {name}\n', manifest)


if __name__ == '__main__':
    unittest.main()
