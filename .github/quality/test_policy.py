"""Exercise repository policy against temporary repositories and real hooks."""

import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
import install_policy_hooks  # noqa: E402
import policy  # noqa: E402


HOOKS = Path(__file__).resolve().parents[2] / '.githooks'
GOOD_MSG = 'msg/Good.msg'
GOOD = '# header.stamp = capture time\nstd_msgs/Header header\nfloat64 x\n'


class PolicyTestCase(unittest.TestCase):
    """Isolated git config: fixtures never see the user's identity, signing or hooks."""

    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.tmp = Path(directory.name)
        (self.tmp / 'gitconfig').write_text('')
        environment = {
            'HOME': str(self.tmp), 'GIT_CONFIG_GLOBAL': str(self.tmp / 'gitconfig'),
            'GIT_CONFIG_NOSYSTEM': '1', 'GIT_TERMINAL_PROMPT': '0',
            'PATH': f'{Path(sys.executable).parent}{os.pathsep}{os.environ["PATH"]}'}
        patcher = mock.patch.dict(os.environ, environment)
        patcher.start()
        self.addCleanup(patcher.stop)
        for name in ('GIT_DIR', 'GIT_INDEX_FILE', 'GIT_WORK_TREE'):
            os.environ.pop(name, None)
        self.git(self.tmp, 'config', '--global', 'protocol.file.allow', 'always')
        self.git(self.tmp, 'config', '--global', 'init.defaultBranch', 'nightly')

    def git(self, repo, *args, env=None):
        result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True,
                                env={**os.environ, **(env or {})})
        if result.returncode:
            raise AssertionError(f'git {args}: {result.stderr}')
        return result.stdout.strip()

    def repo(self, name, person='pat', bare_remote=True):
        path = self.tmp / name
        self.git(self.tmp, 'init', '-q', str(path))
        self.as_person(path, person)
        if bare_remote:
            remote = self.tmp / f'{name}.git'
            self.git(self.tmp, 'init', '-q', '--bare', str(remote))
            self.git(path, 'remote', 'add', 'origin', str(remote))
        return path

    def as_person(self, repo, person):
        self.git(repo, 'config', 'user.name', f'{person.title()} Contributor')
        self.git(repo, 'config', 'user.email', f'{person}@example.com')

    def commit(self, repo, message='change', files=None, author=None, env=None):
        files = files or {f'file{self.git(repo, "rev-list", "--all", "--count")}.txt': message}
        for path, text in files.items():
            (repo / path).parent.mkdir(parents=True, exist_ok=True)
            (repo / path).write_text(text)
            self.git(repo, 'add', '--', path)
        args = ['commit', '-q', '-m', message]
        self.git(repo, *args, *(['--author', author] if author else []), env=env)
        return self.git(repo, 'rev-parse', 'HEAD')

    def install(self, *args):
        with contextlib.redirect_stdout(io.StringIO()):
            install_policy_hooks.install(*args)

    def run_policy(self, repo, *args, stdin=''):
        return subprocess.run([sys.executable, str(Path(policy.__file__)), *args],
                              cwd=repo, input=stdin, capture_output=True, text=True)


class ContractTests(PolicyTestCase):
    def test_index_content_is_checked_not_worktree(self):
        repo = self.repo('pkg')
        self.commit(repo, files={GOOD_MSG: GOOD})
        (repo / GOOD_MSG).write_text('float64 x\n')  # unstaged regression
        self.assertEqual([], policy.contract_errors(repo))
        self.git(repo, 'add', GOOD_MSG)
        (repo / GOOD_MSG).write_text(GOOD)  # staged regression, fixed only in worktree
        self.assertIn('need std_msgs/Header', '\n'.join(policy.contract_errors(repo)))

    def test_deletions_symlinks_elements_and_vendor_files(self):
        repo = self.repo('pkg')
        self.commit(repo, files={GOOD_MSG: GOOD, 'msg/Old.msg': 'float64 x\n'})
        self.git(repo, 'rm', '-q', '--cached', 'msg/Old.msg')  # staged; worktree keeps it
        (repo / 'msg/Link.msg').symlink_to('Missing.msg')
        self.git(repo, 'add', 'msg/Link.msg')
        (repo / 'msg/Array.msg').write_text(GOOD + 'Element[] items\n')
        (repo / 'msg/Element.msg').write_text('float64 y\n')
        (repo / 'sdk/msg').mkdir(parents=True)
        (repo / 'sdk/msg/Vendor.msg').write_text('float64 z\n')
        (repo / 'isaac_ros_x_interfaces/msg').mkdir(parents=True)
        (repo / 'isaac_ros_x_interfaces/msg/Nv.msg').write_text('std_msgs/Header header\n')
        self.git(repo, 'add', 'msg/Array.msg', 'msg/Element.msg', 'sdk', 'isaac_ros_x_interfaces')
        self.assertEqual([], policy.contract_errors(repo))

    def test_header_stamp_must_be_documented(self):
        repo = self.repo('pkg')
        self.git(repo, 'add', '--intent-to-add', '.')
        (repo / 'msg').mkdir()
        (repo / 'msg/Bare.msg').write_text('std_msgs/Header header  # frame_id = camera\n')
        self.git(repo, 'add', '.')
        self.assertIn('header.stamp means', '\n'.join(policy.contract_errors(repo)))

    def test_recursive_contracts_read_pinned_commits(self):
        child = self.repo('child')
        self.commit(child, files={'msg/Bad.msg': 'float64 x\n'})
        workspace = self.repo('ws')
        self.git(workspace, 'submodule', 'add', '-q', str(child), 'child')
        self.commit(workspace, 'add child')
        self.assertIn('child/msg/Bad.msg', '\n'.join(policy.recursive_contracts(workspace, 'HEAD')))


class CommitRangeTests(PolicyTestCase):
    def push(self, repo, ref='nightly'):
        local = self.git(repo, 'rev-parse', ref)
        remote = self.git(repo, 'ls-remote', 'origin', f'refs/heads/{ref}').split()
        line = f'refs/heads/{ref} {local} refs/heads/{ref} {remote[0] if remote else policy.ZERO}\n'
        result = self.run_policy(repo, 'pre-push', 'origin', 'url', stdin=line)
        if not result.returncode:
            self.git(repo, 'push', '-q', '--no-verify', 'origin', ref)
        return result

    def test_unsigned_commits_from_any_contributor_pass(self):
        repo = self.repo('pkg')
        self.commit(repo)
        self.assertEqual(0, self.push(repo).returncode)
        self.as_person(repo, 'sam')
        self.commit(repo, 'collaborator change')
        result = self.push(repo)
        self.assertEqual(0, result.returncode, result.stderr)

    def workspace_with_child(self):
        child = self.repo('child')
        old = self.commit(child, 'child base')
        self.git(child, 'push', '-q', 'origin', 'nightly')
        workspace = self.repo('ws')
        self.commit(workspace, 'root')
        self.git(workspace, 'submodule', 'add', '-q', str(self.tmp / 'child.git'), 'child')
        (workspace / policy.REVIEWED).parent.mkdir(parents=True)
        (workspace / policy.REVIEWED).write_text(f'child {old}  # imported history\n')
        self.git(workspace, 'add', policy.REVIEWED)
        self.commit(workspace, 'add child')
        self.assertEqual(0, self.push(workspace).returncode, self.push(workspace).stderr)
        nested = workspace / 'child'
        self.as_person(nested, 'pat')
        return workspace, nested, old

    def bump(self, workspace, nested, oid):
        self.git(nested, 'checkout', '-q', oid)
        self.git(workspace, 'add', 'child')
        return self.commit(workspace, f'bump child {oid[:7]}')

    def test_installed_hooks_reject_unpushed_package_pins(self):
        workspace, nested, _ = self.workspace_with_child()
        self.install(workspace, [workspace], HOOKS)
        self.git(nested, 'switch', '-q', '-c', 'work')
        self.bump(workspace, nested, self.commit(nested, 'unpushed'))
        with self.assertRaisesRegex(AssertionError, 'not be found on any remote'):
            self.git(workspace, 'push', '-q', 'origin', 'nightly')  # push.recurseSubmodules
        self.git(nested, 'push', '-q', 'origin', 'work')
        self.git(workspace, 'push', '-q', 'origin', 'nightly')

    def test_pre_push_skips_only_unchanged_uninitialized_submodules(self):
        self.workspace_with_child()
        clone = self.tmp / 'clone'
        self.git(self.tmp, 'clone', '-q', str(self.tmp / 'ws.git'), str(clone))  # child not init
        self.as_person(clone, 'pat')
        self.commit(clone, 'unrelated root change')
        result = self.push(clone)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn('child not initialized; skipped its .msg check', result.stderr)
        self.git(clone, 'update-index', '--cacheinfo', f'160000,{"1" * 40},child')
        self.commit(clone, 'bump unavailable child')
        self.assertIn(f'child: fetch/initialize gitlink target {"1" * 12}',
                      self.push(clone).stderr)
        with self.assertRaisesRegex(ValueError, 'child: initialize/fetch pinned commit'):
            policy.recursive_contracts(clone, 'HEAD')  # CI and explicit scans stay strict

    def test_gitlink_must_fast_forward(self):
        workspace, nested, old = self.workspace_with_child()
        self.git(nested, 'switch', '-q', '-c', 'work')
        newer = self.commit(nested, 'package change')
        self.bump(workspace, nested, newer)
        self.assertEqual(0, self.push(workspace).returncode)
        self.git(nested, 'switch', '-q', '-c', 'stale', old)
        sideways = self.commit(nested, 'stale branch')
        self.bump(workspace, nested, sideways)
        self.assertIn('not a fast-forward', self.push(workspace).stderr)

    def test_new_gitlink_requires_reviewed_history(self):
        workspace, _, _ = self.workspace_with_child()
        upstream = self.repo('upstream', bare_remote=False)
        self.commit(upstream, 'upstream', author='Up <up@example.org>')
        self.git(workspace, 'submodule', 'add', '-q', str(upstream), 'upstream')
        self.commit(workspace, 'import upstream')
        self.assertIn('upstream: new gitlink needs a reviewed', self.push(workspace).stderr)
        reviewed = workspace / policy.REVIEWED
        upstream_head = self.git(upstream, 'rev-parse', 'HEAD')
        reviewed.write_text(reviewed.read_text() + f'upstream {upstream_head}\n')
        self.git(workspace, 'add', policy.REVIEWED)
        self.commit(workspace, 'review upstream import')
        self.assertEqual(0, self.push(workspace).returncode, self.push(workspace).stderr)


class CiTests(PolicyTestCase):
    def event(self, payload, ref='refs/heads/nightly'):
        path = self.tmp / 'event.json'
        path.write_text(json.dumps(payload))
        return mock.patch.dict(os.environ, {'GITHUB_EVENT_PATH': str(path), 'GITHUB_REF': ref})

    def test_pull_request_checks_head_contracts(self):
        workspace = self.repo('ws')
        base = self.commit(workspace, 'base', files={GOOD_MSG: GOOD})
        head = self.commit(workspace, 'unsigned change')
        pr = {'pull_request': {'base': {'sha': base}, 'head': {'sha': head}}}
        with self.event(pr):
            self.assertEqual([], policy.ci_errors(workspace))
        bad = self.commit(workspace, 'bad message', files={'msg/Bad.msg': 'float64 x\n'})
        pr['pull_request']['head']['sha'] = bad
        with self.event(pr):
            self.assertIn('msg/Bad.msg', '\n'.join(policy.ci_errors(workspace)))

    def test_push_without_before_falls_back_to_protected_branches(self):
        workspace = self.repo('ws')
        self.commit(workspace, 'base', files={GOOD_MSG: GOOD})
        self.git(workspace, 'push', '-q', 'origin', 'nightly')
        self.git(workspace, 'fetch', '-q', 'origin')
        self.git(workspace, 'switch', '-q', '-c', 'feature')
        new = self.commit(workspace, 'feature')
        seen = []
        moves = mock.Mock(side_effect=lambda repo, commits, nested: seen.extend(commits) or [])
        with self.event({'before': policy.ZERO, 'after': new}, 'refs/heads/feature'), \
                mock.patch.object(policy.Checker, 'moves', moves):
            policy.ci_errors(workspace)
        self.assertEqual([new], seen)


class HookTests(PolicyTestCase):
    def test_recursive_install_checks_packages_and_ignores_leaked_git_dir(self):
        child = self.repo('child')
        self.commit(child, files={GOOD_MSG: GOOD})
        self.git(child, 'push', '-q', 'origin', 'nightly')
        workspace = self.repo('ws')
        self.git(workspace, 'submodule', 'add', '-q', str(self.tmp / 'child.git'), 'child')
        self.commit(workspace, 'add child')
        nested = workspace / 'child'
        self.as_person(nested, 'pat')
        self.assertEqual([nested], install_policy_hooks.submodules(workspace))
        self.install(workspace, [workspace, *install_policy_hooks.submodules(workspace)], HOOKS)
        (nested / 'msg/Bad.msg').write_text('float64 x\n')
        self.git(nested, 'add', 'msg/Bad.msg')
        with self.assertRaisesRegex(AssertionError, 'std_msgs/Header'):
            self.commit(nested, 'package pre-commit')
        self.git(nested, 'rm', '-q', '--cached', 'msg/Bad.msg')
        self.commit(nested, 'package change')
        self.git(nested, 'push', '-q', 'origin', 'HEAD:work')  # package pre-push
        self.git(workspace, 'add', 'child')
        self.commit(workspace, 'bump child')
        self.git(nested, 'switch', '-q', '-c', 'stale', 'HEAD~1')
        self.commit(nested, 'sideways')
        self.git(nested, 'push', '-q', 'origin', 'HEAD:stale')
        self.git(workspace, 'add', 'child')
        self.commit(workspace, 'bump child sideways')
        # A leaked GIT_DIR would resolve the child pin in the workspace and miss this.
        leaked = {'GIT_DIR': str(workspace / '.git'), 'GIT_WORK_TREE': str(workspace)}
        with self.assertRaisesRegex(AssertionError, 'not a fast-forward'):
            self.git(workspace, 'push', '-q', 'origin', 'nightly', env=leaked)

    def test_pre_push_checks_contracts_that_skipped_pre_commit(self):
        repo = self.repo('pkg')
        self.commit(repo, files={GOOD_MSG: GOOD})
        self.install(repo, [repo], HOOKS)
        self.git(repo, 'switch', '-q', '-c', 'side')
        (repo / 'msg/Bad.msg').write_text('float64 x\n')
        self.git(repo, 'add', 'msg/Bad.msg')
        self.git(repo, 'commit', '-q', '--no-verify', '-m', 'bad message')
        self.git(repo, 'switch', '-q', 'nightly')
        self.git(repo, 'merge', '-q', '--no-edit', 'side')  # fast-forward skips hooks
        with self.assertRaisesRegex(AssertionError, 'msg/Bad.msg: top-level'):
            self.git(repo, 'push', '-q', 'origin', 'nightly')

    def test_installed_hooks_reject_staged_contracts_not_unsigned_commits(self):
        repo = self.repo('pkg')
        self.install(repo, [repo], HOOKS)
        self.commit(repo, files={GOOD_MSG: GOOD})
        (repo / 'msg/Bad.msg').write_text('float64 x\n')
        self.git(repo, 'add', 'msg/Bad.msg')
        with self.assertRaisesRegex(AssertionError, 'std_msgs/Header'):
            self.commit(repo, 'bad message')
        self.git(repo, 'rm', '-q', '--cached', 'msg/Bad.msg')
        self.git(repo, 'config', 'commit.gpgsign', 'false')
        self.commit(repo, 'unsigned')
        self.git(repo, 'push', '-q', 'origin', 'nightly')

    def test_installer_is_idempotent_and_refuses_unmanaged_hooks(self):
        workspace = self.repo('ws')
        other = self.repo('other')
        (other / '.git/hooks/pre-commit').write_text('#!/bin/sh\n')
        global_config = (self.tmp / 'gitconfig').read_text()
        with self.assertRaisesRegex(ValueError, 'unmanaged hooks pre-commit'):
            self.install(workspace, [workspace, other], HOOKS)
        self.assertNotIn('hookspath', self.git(workspace, 'config', '--local', '--list').lower())
        self.install(workspace, [workspace], HOOKS)
        self.install(workspace, [workspace], HOOKS)
        self.assertEqual(str(HOOKS), self.git(workspace, 'config', '--local', 'core.hooksPath'))
        self.assertEqual('check', self.git(workspace, 'config', 'push.recurseSubmodules'))
        self.git(other, 'config', 'core.hooksPath', '/elsewhere')
        with self.assertRaisesRegex(ValueError, 'refusing to replace'):
            self.install(workspace, [other], HOOKS)
        self.assertEqual(global_config, (self.tmp / 'gitconfig').read_text())


if __name__ == '__main__':
    unittest.main()
