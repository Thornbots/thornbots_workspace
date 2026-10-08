"""Exercise lint gates against temporary repositories and real tool output."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CHECKER = Path(__file__).with_name('check.py')


class QualityGateTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.git('init', '--quiet')

    def git(self, *args):
        return subprocess.run(['git', '-C', str(self.root), *args], check=True,
                              capture_output=True, text=True)

    def write(self, path, contents):
        destination = self.root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(contents)
        self.git('add', '--', path)

    def check(self, *args):
        return subprocess.run([sys.executable, str(CHECKER), *args], cwd=self.root,
                              capture_output=True, text=True, check=False)

    def expect_status(self, expected, *args):
        result = self.check(*args)
        self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
        return result

    def test_clean_files_pass(self):
        self.write('node.py', 'VALUE = 1\n')
        self.write('package.xml', '<package><name>example</name></package>\n')
        self.write('config.yaml', 'threshold: 1\n')
        self.expect_status(0)

    def test_new_python_violation_fails(self):
        self.write('node.py', 'print(missing_value)\n')
        result = self.expect_status(1)
        self.assertIn('F821', result.stdout)

    def test_reviewed_debt_passes_until_its_count_grows(self):
        self.write('node.py', 'print(missing_value)\n')
        self.expect_status(0, '--baseline')
        baseline = json.loads((self.root / '.github/quality-baseline.json').read_text())
        self.assertEqual(1, sum(baseline.values()))
        self.expect_status(0)
        self.write('node.py', 'print(missing_value)\nprint(missing_value)\n')
        self.expect_status(1)

    def test_python_syntax_cannot_be_suppressed_by_baseline(self):
        self.write('node.py', 'def broken(:\n')
        self.expect_status(0, '--baseline')
        result = self.expect_status(1)
        self.assertIn('Syntax errors must be fixed', result.stdout)

    def test_invalid_documents_cannot_be_suppressed_by_baseline(self):
        for path, contents in [('package.xml', '<package>'), ('config.yaml', 'x: [')]:
            with self.subTest(path=path):
                self.write(path, contents)
                self.assertIn('parse:', self.expect_status(1).stdout)
                self.expect_status(0, '--baseline')
                result = self.expect_status(1)
                self.assertIn('Syntax errors must be fixed', result.stdout)

    def test_vendor_untracked_symlink_and_gitlink_files_are_excluded(self):
        self.write('sdk/vendor.py', 'def broken(:\n')
        (self.root / 'untracked.py').write_text('def broken(:\n')
        os.symlink('untracked.py', self.root / 'link.py')
        self.git('add', 'link.py')
        self.git('update-index', '--add', '--cacheinfo',
                 '160000,0123456789012345678901234567890123456789,child')
        (self.root / 'child').mkdir()
        (self.root / 'child/node.py').write_text('def broken(:\n')
        self.expect_status(0)

    def test_shell_parse_errors_fail(self):
        self.write('run.sh', '#!/bin/bash\nif true; then\n')
        result = self.expect_status(1)
        self.assertIn('SC', result.stdout)
        self.expect_status(0, '--baseline')
        self.expect_status(1)


if __name__ == '__main__':
    unittest.main()
