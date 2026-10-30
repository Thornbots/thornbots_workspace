"""Run the actual nightly host boundary with inert checkout/runner/VM/CI stubs."""
import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[2] / '.github/scripts/nightly_tests.sh'
SOURCE = SCRIPT.read_text().split('case "${1:-run}"')[0]
STAGES = ['setup', 'firmware', 'build', 'test', 'e2e_mcb_parked', 'e2e_mcb_drive']


def records(outcomes):
    return ''.join(f'{name}\t{res}\t1\n' for name, res in zip(STAGES, outcomes))


class NightlyVerdictTest(unittest.TestCase):
    def exercise(self, status, runner_rc=0, publish_rc=0, publish=True):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / 'src/isaac_ros_common/scripts'
            source.mkdir(parents=True)
            fixture = root / 'fixture.tsv'
            fixture.write_text(status)
            runner = source / 'agent_container.sh'
            runner.write_text(
                '#!/bin/bash\n'
                '[ "$1" != down ] || exit 0\n'
                'while [ "$#" -gt 0 ]; do\n'
                '  if [ "$1" = -e ]; then shift; cp "$FIXTURE" "$1/status.tsv"; break; fi\n'
                '  shift\n'
                'done\n'
                'exit "$RUNNER_RC"\n')
            runner.chmod(0o755)
            publisher = root / 'src/.github/scripts/nightly_publish.sh'
            publisher.parent.mkdir(parents=True)
            publisher.write_text('#!/bin/bash\necho publish-fixture\nexit "$PUBLISH_RC"\n')
            mocks = '''
other_stack() { return 1; }
update_checkout() { return 0; }
shas() { echo 'workspace fixture'; }
dispatch_ci() { echo 'dispatch must not run' >&2; exit 99; }
colima() { echo 'VM must not run' >&2; exit 99; }
docker() { echo 'Docker must not run' >&2; exit 99; }
cmd_run
'''
            result = subprocess.run(
                ['/bin/bash', '-c', SOURCE + mocks],
                env=dict(os.environ, NIGHTLY_CI_ROOT=tmp, NIGHTLY_DISPATCH_REF='',
                         FIXTURE=str(fixture), RUNNER_RC=str(runner_rc),
                         PUBLISH_RC=str(publish_rc), NIGHTLY_PUBLISH=str(int(publish))),
                capture_output=True, text=True, timeout=10)
            summaries = list((root / 'results').glob('*/summary.txt'))
            self.assertEqual(len(summaries), 1, result.stderr)
            return result.returncode, summaries[0].read_text()

    def test_complete_success_passes(self):
        rc, summary = self.exercise(records(['PASS'] * 6))
        self.assertEqual(rc, 0)
        self.assertTrue(summary.startswith('PASS '), summary)

    def test_publication_controls_final_verdict(self):
        status = records(['PASS'] * 6)
        for enabled, code, outcome in [(True, 0, 'PASS'), (True, 1, 'FAIL'),
                                       (False, 1, 'SKIP')]:
            with self.subTest(enabled=enabled, code=code):
                rc, summary = self.exercise(status, publish_rc=code, publish=enabled)
                self.assertEqual(rc, int(outcome == 'FAIL'), summary)
                self.assertIn('publish=' + outcome, summary)
        rc, summary = self.exercise(records(['PASS', 'PASS', 'PASS', 'FAIL',
                                            'PASS', 'PASS']), publish_rc=1)
        self.assertEqual(rc, 1)
        self.assertIn('publish=SKIP', summary)

    def test_runner_failure_overrides_even_complete_passes(self):
        for status in [records(['PASS'] * 6), 'setup\tPASS\t1\n', '']:
            with self.subTest(status=status):
                rc, summary = self.exercise(status, 143)
                self.assertNotEqual(rc, 0)
                self.assertIn('runner=FAIL(143)', summary)

    def test_every_incomplete_prefix_fails(self):
        for length in range(6):
            with self.subTest(length=length):
                rc, summary = self.exercise(records(['PASS'] * length))
                self.assertNotEqual(rc, 0)
                self.assertIn('invalid-status', summary)

    def test_dependency_skips_remain_valid_failed_runs(self):
        for outcomes in [
            ['FAIL', 'SKIP', 'SKIP', 'SKIP', 'SKIP', 'SKIP'],
            ['PASS', 'FAIL', 'PASS', 'PASS', 'SKIP', 'SKIP'],
            ['PASS', 'PASS', 'FAIL', 'SKIP', 'SKIP', 'SKIP'],
            ['PASS', 'FAIL', 'FAIL', 'SKIP', 'SKIP', 'SKIP'],
            ['PASS', 'PASS', 'PASS', 'FAIL', 'PASS', 'PASS'],
        ]:
            with self.subTest(outcomes=outcomes):
                rc, summary = self.exercise(records(outcomes))
                self.assertNotEqual(rc, 0)
                self.assertTrue(summary.startswith('FAIL '), summary)
                self.assertNotIn('invalid-status', summary)
                for stage, outcome in zip(STAGES, outcomes):
                    self.assertIn(f'{stage}={outcome}', summary)

    def test_malformed_duplicate_unexpected_and_impossible_records_fail(self):
        valid = records(['PASS'] * 6)
        for invalid in [
            valid + 'setup\tPASS\t1\n',
            valid.replace('firmware', 'surprise'),
            valid.replace('firmware', 'setup'),
            valid.replace('setup\tPASS', 'setup\tSKIP'),
            valid.replace('build\tPASS', 'build\tSKIP'),
            valid.replace('test\tPASS', 'test\tSKIP'),
            valid.replace('setup\tPASS', 'setup\tFAIL'),
            valid.replace('setup\tPASS', 'setup\tMAYBE'),
            valid.replace('setup\tPASS\t1', 'setup PASS 1'),
            valid.replace('setup\tPASS\t1', 'setup\tPASS\t-1'),
            valid.replace('setup\tPASS\t1', 'setup\tPASS\tnan'),
            valid.replace('setup\tPASS\t1', 'setup\tPASS\t1\textra'),
            valid.replace('setup\tPASS\t1', 'setup\tPASS'),
            valid + '\n',
        ]:
            with self.subTest(invalid=invalid):
                rc, summary = self.exercise(invalid)
                self.assertNotEqual(rc, 0)
                self.assertIn('invalid-status', summary)

    def test_actual_inner_failure_branches_emit_the_expected_stage_set(self):
        inner = SCRIPT.with_name('nightly_tests_inside.sh').read_text()
        orchestration = inner[inner.index(': >"$EV/status.tsv"'):]
        for failure in ['', 'setup', 'firmware', 'build', 'test']:
            with self.subTest(failure=failure), tempfile.TemporaryDirectory() as tmp:
                mocks = '''
EV=''' + shlex.quote(tmp) + '''
fw=0
skip() { printf '%s\\tSKIP\\t0\\n' "$1" >> "$EV/status.tsv"; }
stage() {
    local res=PASS; [ "$1" != "$FAILURE" ] || res=FAIL
    printf '%s\\t%s\\t1\\n' "$1" "$res" >> "$EV/status.tsv"
    [ "$res" = PASS ]
}
cleanup_stack() { :; }
cp() { :; }
'''
                subprocess.run(['/bin/bash', '-c', mocks + orchestration],
                               env=dict(os.environ, FAILURE=failure), check=True, timeout=10)
                rc, summary = self.exercise((Path(tmp) / 'status.tsv').read_text())
                self.assertEqual(rc, int(bool(failure)), summary)
                self.assertNotIn('invalid-status', summary)


if __name__ == '__main__':
    unittest.main()
