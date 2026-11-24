"""Ensure portable ROS CI re-runs every changed package and its dependents."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import ros_ci  # noqa: E402

GIT = ['git', '-c', 'user.name=CI', '-c', 'user.email=ci@example.invalid',
       '-c', 'commit.gpgsign=false']


def manifest(name, deps=()):
    lines = ''.join(f'<depend>{dep}</depend>' for dep in deps)
    return f'<package format="3"><name>{name}</name>{lines}</package>\n'


class PlannerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.src = self.root / 'src'
        self.dockerfile = self.root / 'Dockerfile'
        self.dockerfile.write_text('FROM scratch\n')
        # base <- mid <- top; leaf is independent; ignored is skipped.
        self.write('base/package.xml', manifest('base', ['rclcpp']))
        self.write('mid/package.xml', manifest('mid', ['base', 'eigen']))
        self.write('top/package.xml', manifest('top', ['mid']))
        self.write('top/src/main.cpp', 'getenv("MCB_FIRMWARE_BINARY");\n')
        self.write('leaf/package.xml', manifest('leaf'))
        self.write('ignored/COLCON_IGNORE', '')
        self.write('ignored/package.xml', manifest('ignored'))
        self.git('init', '-q')
        self.write('firmware/MCBV3/README', 'firmware\n')
        self.commit()

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, relative, text):
        path = self.src / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def git(self, *args):
        subprocess.run(GIT + ['-C', str(self.src), *args], check=True, capture_output=True)

    def commit(self):
        self.git('add', '-A')
        self.git('commit', '-q', '-m', 'change')

    def plan(self, *extra):
        out = self.root / 'plan.json'
        ros_ci.main(['plan', str(self.src), '--dockerfile', str(self.dockerfile),
                     '--out', str(out), *extra])
        return json.loads(out.read_text())

    def keys(self, *extra):
        return {name: info['hash'] for name, info in self.plan(*extra)['packages'].items()}

    def test_change_rekeys_package_and_dependents_only(self):
        before = self.keys()
        self.assertEqual(set(before), {'base', 'mid', 'top', 'leaf'})
        self.write('base/src/lib.cpp', 'int x;\n')
        self.commit()
        after = self.keys()
        self.assertEqual({n for n in before if before[n] != after[n]}, {'base', 'mid', 'top'})

    def test_environment_rekeys_everything(self):
        before = self.keys()
        self.dockerfile.write_text('FROM scratch\nRUN true\n')
        after = self.keys()
        self.assertTrue(all(before[n] != after[n] for n in before))

    def test_firmware_feeds_only_its_consumers(self):
        before = self.keys('--firmware')
        self.write('firmware/MCBV3/README', 'firmware 2\n')
        self.commit()
        after = self.keys('--firmware')
        self.assertEqual({n for n in before if before[n] != after[n]}, {'top'})

    def test_uncommitted_content_is_refused(self):
        self.write('leaf/extra.py', 'print(1)\n')
        with self.assertRaises(SystemExit):
            self.plan()

    def select(self, recorded):
        plan = self.root / 'plan.json'
        state = self.root / 'manifest.json'
        state.write_text(json.dumps({'packages': recorded}))
        install = self.root / 'install'
        install.mkdir(exist_ok=True)
        ros_ci.main(['select', '--plan', str(plan), '--manifest', str(state),
                     '--install', str(install), '--out', str(self.root)])
        return [(self.root / f).read_text().split() for f in ('build.txt', 'test.txt')]

    def test_selects_stale_packages_and_reuses_passing_ones(self):
        keys = self.keys()
        passed = {n: {'hash': h, 'passed': True} for n, h in keys.items()}
        self.assertEqual(self.select(passed), [[], []])
        self.write('mid/src/node.cpp', 'int y;\n')
        self.commit()
        self.keys()
        self.assertEqual(self.select(passed), [['mid', 'top'], ['mid', 'top']])
        failed = dict(passed, leaf={'hash': keys['leaf'], 'passed': False})
        self.assertIn('leaf', self.select(failed)[1])
        self.assertEqual(self.select({}), [sorted(keys)] * 2)

    def test_select_discards_install_tree_with_removed_package(self):
        keys = self.keys()
        recorded = {n: {'hash': h, 'passed': True} for n, h in keys.items()}
        self.git('rm', 'leaf/package.xml')
        self.commit()
        packages = sorted(self.keys())
        self.assertEqual(self.select(recorded), [packages, packages])
        self.assertFalse((self.root / 'install').exists())
        self.assertFalse((self.root / 'manifest.json').exists())

    def test_record_requires_fresh_install(self):
        keys = self.keys()
        state = self.root / 'manifest.json'
        args = ['record', '--plan', str(self.root / 'plan.json'), '--manifest', str(state)]
        ros_ci.main(args + ['--built', 'base'])
        ros_ci.main(args + ['--tested', 'base', '--passed'])
        self.assertEqual(json.loads(state.read_text())['packages']['base'],
                         {'hash': keys['base'], 'passed': True})
        with self.assertRaises(SystemExit):
            ros_ci.main(args + ['--tested', 'mid', '--passed'])

    def test_image_context_lists_external_dependencies(self):
        context = self.root / 'context'
        self.plan('--context', str(context))
        text = (context / 'deps/package.xml').read_text()
        self.assertIn('<depend>rclcpp</depend>', text)
        self.assertIn('<depend>eigen</depend>', text)
        self.assertNotIn('<depend>base</depend>', text)


if __name__ == '__main__':
    unittest.main()
