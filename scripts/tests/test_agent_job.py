"""Exit-code contract of scripts/agent_job.sh, with short real jobs."""

import os
import pathlib
import signal
import subprocess
import tempfile
import time
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / 'agent_job.sh'


class AgentJobTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)
        self.env = dict(os.environ, AGENT_JOB_ROOT=str(self.root))

    def tearDown(self):
        for pid_file in self.root.glob('*/pid'):
            try:
                os.killpg(int(pid_file.read_text()), signal.SIGKILL)
            except (ProcessLookupError, PermissionError, ValueError):
                pass
        self.tmp.cleanup()

    def job(self, *args, timeout=30):
        return subprocess.run(['bash', str(SCRIPT), *args], env=self.env, text=True,
                              capture_output=True, timeout=timeout, check=False)

    def test_wait_returns_job_exit_code_and_log_tail(self):
        self.assertEqual(self.job('start', 'a', '--', 'sh', '-c', 'echo out; exit 3').returncode, 0)
        result = self.job('wait', 'a')
        self.assertEqual(result.returncode, 3)
        self.assertIn('rc=3', result.stdout)
        self.assertIn('out', result.stdout)

    def test_start_runs_in_given_directory(self):
        work = self.root / 'work'
        work.mkdir()
        self.job('start', 'b', '-C', str(work), '--', 'sh', '-c', 'pwd -P')
        self.assertEqual(self.job('wait', 'b').returncode, 0)
        self.assertEqual((self.root / 'b' / 'log').read_text().strip(), str(work.resolve()))

    def test_timeout_is_124_and_rewait_completes(self):
        self.job('start', 'c', '--', 'sh', '-c', 'sleep 3; echo late')
        self.assertEqual(self.job('wait', 'c', '-t', '1').returncode, 124)
        result = self.job('wait', 'c', '-t', '20')
        self.assertEqual(result.returncode, 0)
        self.assertIn('late', result.stdout)

    def test_pattern_returns_before_exit_and_fails_if_job_ends_first(self):
        self.job('start', 'd', '--', 'sh', '-c', 'echo ready; echo ready; sleep 20')
        began = time.monotonic()
        self.assertEqual(self.job('wait', 'd', '-m', '^ready$', '-c', '2').returncode, 0)
        self.assertLess(time.monotonic() - began, 10)
        self.job('start', 'e', '--', 'true')
        self.assertEqual(self.job('wait', 'e', '-m', 'never').returncode, 1)

    def test_file_wait_counts_matches(self):
        log = self.root / 'other.log'
        log.write_text('accepted 1\naccepted 2\n')
        self.assertEqual(self.job('wait', '-f', str(log), '-m', 'accepted [0-9]', '-c', '3',
                                  '-t', '1').returncode, 124)
        log.write_text('accepted 1\naccepted 2\naccepted 3\n')
        self.assertEqual(self.job('wait', '-f', str(log), '-m', 'accepted [0-9]',
                                  '-c', '3').returncode, 0)

    def test_stop_records_sigterm_and_sigkill_is_reported(self):
        self.job('start', 'f', '--', 'sleep', '30')
        self.assertEqual(self.job('stop', 'f').returncode, 0)
        self.assertEqual(self.job('wait', 'f', '-t', '10').returncode, 143)
        self.job('start', 'g', '--', 'sleep', '30')
        os.kill(int((self.root / 'g' / 'pid').read_text()), signal.SIGKILL)
        self.assertEqual(self.job('wait', 'g', '-t', '10').returncode, 125)

    def test_names_are_never_reused(self):
        self.job('start', 'h', '--', 'true')
        self.job('wait', 'h')
        result = self.job('start', 'h', '--', 'true')
        self.assertEqual(result.returncode, 2)
        self.assertIn('already ran', result.stderr)
        self.assertEqual(self.job('start', '../x', '--', 'true').returncode, 2)


if __name__ == '__main__':
    unittest.main()
