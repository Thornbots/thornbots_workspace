"""Ensure CI's native host runner rejects missing and failing tests."""

from pathlib import Path
import subprocess
import tempfile
import unittest


RUNNER = Path(__file__).resolve().parents[1] / 'scripts/test_host_packages.sh'


class HostRunnerTests(unittest.TestCase):
    def run_fixture(self, tests):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'CMakeLists.txt').write_text(
                'cmake_minimum_required(VERSION 3.16)\n'
                'project(host_fixture LANGUAGES NONE)\n'
                'include(CTest)\n' + tests)
            return subprocess.run(['bash', str(RUNNER), directory, 'startup'],
                                  capture_output=True, text=True, timeout=30)

    def test_empty_ctest_discovery_fails(self):
        result = self.run_fixture('')
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('No tests were found', result.stdout + result.stderr)

    def test_native_test_failure_propagates(self):
        result = self.run_fixture('add_test(NAME broken COMMAND ${CMAKE_COMMAND} -E false)\n')
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('broken', result.stdout)


if __name__ == '__main__':
    unittest.main()
