"""Exercise repository policy against temporary signed repositories and real hooks."""

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
import urllib.error

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
import install_policy_hooks  # noqa: E402
import policy  # noqa: E402


HOOKS = Path(__file__).resolve().parents[2] / '.githooks'
GOOD_MSG = 'msg/Good.msg'
GOOD = '# header.stamp = capture time\nstd_msgs/Header header\nfloat64 x\n'


class PolicyTestCase(unittest.TestCase):
    """Isolated git config: fixtures never see the user's identity, keys or hooks."""

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
        self.keys = {name: self.keygen(name) for name in ('pat', 'sam')}
        signers = self.tmp / 'allowed_signers'
        signers.write_text(''.join(f'{n}@example.com {k.with_suffix(".pub").read_text()}'
                                   for n, k in self.keys.items()))
        self.signers = signers

    def keygen(self, name):
        key = self.tmp / f'{name}_key'
        subprocess.run(['ssh-keygen', '-q', '-t', 'ed25519', '-N', '', '-C', name, '-f', str(key)],
                       check=True)
        return key

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
        self.git(path, 'config', 'gpg.ssh.allowedSignersFile', str(self.signers))
        if bare_remote:
            remote = self.tmp / f'{name}.git'
            self.git(self.tmp, 'init', '-q', '--bare', str(remote))
            self.git(path, 'remote', 'add', 'origin', str(remote))
        return path

    def as_person(self, repo, person):
        self.git(repo, 'config', 'user.name', f'{person.title()} Contributor')
        self.git(repo, 'config', 'user.email', f'{person}@example.com')
        self.git(repo, 'config', 'gpg.format', 'ssh')
        self.git(repo, 'config', 'user.signingkey', str(self.keys[person]))
        self.git(repo, 'config', 'commit.gpgsign', 'true')

    def commit(self, repo, message='change', files=None, sign=True, author=None, env=None):
        files = files or {f'file{self.git(repo, "rev-list", "--all", "--count")}.txt': message}
        for path, text in files.items():
            (repo / path).parent.mkdir(parents=True, exist_ok=True)
            (repo / path).write_text(text)
            self.git(repo, 'add', '--', path)
        args = ['commit', '-q', '-m', message, '-S' if sign else '--no-gpg-sign']
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

    def test_signed_collaborators_pass_and_unsigned_commits_fail(self):
        repo = self.repo('pkg')
        self.commit(repo)
        self.assertEqual(0, self.push(repo).returncode)
        self.as_person(repo, 'sam')  # another contributor's own identity and key
        self.commit(repo, 'collaborator change')
        self.assertEqual(0, self.push(repo).returncode, self.push(repo).stderr)
        self.commit(repo, 'unsigned', sign=False)
        self.assertIn('unsigned', self.push(repo).stderr)

    def test_new_branch_checks_side_commits_not_only_tip(self):
        repo = self.repo('pkg')
        self.commit(repo)
        self.push(repo)
        self.git(repo, 'switch', '-q', '-c', 'side')
        bad = self.commit(repo, 'unsigned side', sign=False)
        self.git(repo, 'switch', '-q', '-c', 'feature', 'nightly')
        self.commit(repo, 'signed')
        self.git(repo, 'merge', '-q', '-S', '--no-ff', '-m', 'merge side', 'side')
        result = self.push(repo, 'feature')
        self.assertIn(bad[:12], result.stderr)

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
        self.git(nested, 'config', 'gpg.ssh.allowedSignersFile', str(self.signers))
        return workspace, nested, old

    def bump(self, workspace, nested, oid):
        self.git(nested, 'checkout', '-q', oid)
        self.git(workspace, 'add', 'child')
        return self.commit(workspace, f'bump child {oid[:7]}')

    def test_gitlink_bump_checks_package_range(self):
        workspace, nested, _ = self.workspace_with_child()
        self.git(nested, 'switch', '-q', '-c', 'work')
        unsigned = self.commit(nested, 'package unsigned', sign=False)
        signed = self.commit(nested, 'package signed')
        self.bump(workspace, nested, signed)
        self.assertIn(f'child@{unsigned[:12]}: commit is unsigned', self.push(workspace).stderr)

    def test_head_cannot_exempt_existing_gitlinks_through_installed_hooks(self):
        workspace, nested, _ = self.workspace_with_child()
        self.install(workspace, [workspace], HOOKS)
        self.git(nested, 'switch', '-q', '-c', 'work')
        self.bump(workspace, nested, self.commit(nested, 'signed but unpushed'))
        with self.assertRaisesRegex(AssertionError, 'not be found on any remote'):
            self.git(workspace, 'push', '-q', 'origin', 'nightly')  # push.recurseSubmodules
        self.git(workspace, 'reset', '-q', '--hard', 'HEAD~1')
        unsigned = self.commit(nested, 'package unsigned', sign=False)
        self.git(nested, 'push', '-q', '--no-verify', 'origin', 'work')
        self.bump(workspace, nested, unsigned)
        reviewed = workspace / policy.REVIEWED
        reviewed.write_text(reviewed.read_text() + f'child {unsigned}\n')
        self.git(workspace, 'add', policy.REVIEWED)
        self.commit(workspace, 'exempt my own package commit')
        with self.assertRaisesRegex(AssertionError, f'child@{unsigned[:12]}: commit is unsigned'):
            self.git(workspace, 'push', '-q', 'origin', 'nightly')

    def test_pre_push_skips_only_unchanged_uninitialized_submodules(self):
        self.workspace_with_child()
        clone = self.tmp / 'clone'
        self.git(self.tmp, 'clone', '-q', str(self.tmp / 'ws.git'), str(clone))  # child not init
        self.as_person(clone, 'pat')
        self.git(clone, 'config', 'gpg.ssh.allowedSignersFile', str(self.signers))
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
        newer = self.commit(nested, 'package signed')
        self.bump(workspace, nested, newer)
        self.assertEqual(0, self.push(workspace).returncode)
        self.git(nested, 'switch', '-q', '-c', 'stale', old)
        sideways = self.commit(nested, 'stale branch')
        self.bump(workspace, nested, sideways)
        self.assertIn('not a fast-forward', self.push(workspace).stderr)

    def test_new_gitlink_requires_reviewed_history(self):
        workspace, _, _ = self.workspace_with_child()
        upstream = self.repo('upstream', bare_remote=False)
        self.commit(upstream, 'upstream unsigned', sign=False, author='Up <up@example.org>')
        self.git(workspace, 'submodule', 'add', '-q', str(upstream), 'upstream')
        self.commit(workspace, 'import upstream')
        self.assertIn('upstream: new gitlink needs a reviewed', self.push(workspace).stderr)
        reviewed = workspace / policy.REVIEWED
        upstream_head = self.git(upstream, 'rev-parse', 'HEAD')
        reviewed.write_text(reviewed.read_text() + f'upstream {upstream_head}\n')
        self.git(workspace, 'add', policy.REVIEWED)
        self.commit(workspace, 'review upstream import')
        self.assertEqual(0, self.push(workspace).returncode, self.push(workspace).stderr)


class LocalSignatureTests(PolicyTestCase):
    """Hooks accept only a good signature Git maps to the committer's email."""

    def verify(self, repo, oid, github=None):
        with mock.patch.object(policy, 'github_signature', github or self.fail_github):
            return policy.local_signature(repo, oid, False)

    def fail_github(self, *_):
        self.fail('only published commits may ask GitHub')

    def forge(self, repo, signature, committer='Pat Contributor <pat@example.com>'):
        tree = self.git(repo, 'write-tree')
        lines = [f'tree {tree}', f'author {committer} 1700000000 +0000',
                 f'committer {committer} 1700000000 +0000']
        body = '\n'.join(lines + ['gpgsig ' + signature.replace('\n', '\n ')]) + '\n\nforged\n'
        return subprocess.run(['git', '-C', str(repo), 'hash-object', '-t', 'commit', '-w',
                               '--stdin'], input=body, capture_output=True, text=True,
                              check=True).stdout.strip()

    def test_good_signature_must_match_committer_principal(self):
        repo = self.repo('pkg')
        self.assertIsNone(self.verify(repo, self.commit(repo)))
        self.git(repo, 'config', 'user.signingkey', str(self.keys['sam']))  # listed for sam only
        self.assertIn('signer sam@example.com', self.verify(repo, self.commit(repo, 'mismatch')))
        self.git(repo, 'config', 'user.signingkey', str(self.keygen('eve')))  # unlisted key
        self.assertIn('not verified for committer', self.verify(repo, self.commit(repo, 'eve')))
        self.git(repo, 'config', '--unset', 'gpg.ssh.allowedSignersFile')  # cannot verify at all
        self.assertIn('allowedSignersFile', self.verify(repo, self.commit(repo, 'no list')))
        unsigned = self.commit(repo, 'x', sign=False)
        self.assertEqual('commit is unsigned', self.verify(repo, unsigned))

    def test_malformed_signature_is_rejected(self):
        repo = self.repo('pkg')
        self.commit(repo)
        signed = self.git(repo, 'cat-file', 'commit', 'HEAD')
        armored = signed.split('gpgsig ', 1)[1].split('\n\n', 1)[0].replace('\n ', '\n')
        corrupt = armored.replace(armored.splitlines()[2], 'A' * len(armored.splitlines()[2]))
        for signature in [corrupt, 'not a signature']:
            with self.subTest(signature=signature[:20]):
                self.assertIn('not verified', self.verify(repo, self.forge(repo, signature)))

    def test_published_github_merge_falls_back_to_exact_github_verification(self):
        repo = self.repo('pkg')
        self.commit(repo)
        self.git(repo, 'config', 'gpg.program', str(self.tmp / 'missing-gpg'))
        pgp = '-----BEGIN PGP SIGNATURE-----\n\nwsBcBAABCAAQ\n=abcd\n-----END PGP SIGNATURE-----'
        merge = self.forge(repo, pgp, 'GitHub <noreply@github.com>')
        self.assertIn('not verified', self.verify(repo, merge))  # unpublished: no fallback
        self.git(repo, 'update-ref', 'refs/remotes/origin/nightly', merge)
        calls = []
        self.assertIsNone(self.verify(repo, merge, lambda *a: calls.append(a[1])))
        self.assertEqual([merge], calls)
        unverified = self.verify(repo, merge, lambda *_: 'GitHub does not verify (unsigned)')
        self.assertIn('GitHub does not verify', unverified)
        offline = mock.Mock(side_effect=ValueError('GitHub API unavailable'))
        self.assertIn('cannot verify signature locally', self.verify(repo, merge, offline))


class GitHubVerificationTests(PolicyTestCase):
    def event(self, payload, ref='refs/heads/nightly'):
        path = self.tmp / 'event.json'
        path.write_text(json.dumps(payload))
        return mock.patch.dict(os.environ, {'GITHUB_EVENT_PATH': str(path), 'GITHUB_REF': ref})

    def test_ci_trusts_github_not_local_signature_or_repository_keys(self):
        workspace = self.repo('ws')
        base = self.commit(workspace, 'base', files={GOOD_MSG: GOOD})
        # A PR adds its own allowed-signers entry; locally that signature is "good".
        head = self.commit(workspace, 'add my key',
                           files={'allowed_signers': 'x@example.com key\n'})
        self.assertEqual('G', self.git(workspace, 'log', '-1', '--format=%G?'))
        seen = []

        def github(repo, oid, nested):
            seen.append((Path(repo), oid))
            return 'GitHub does not verify its signature (unknown_key)'

        pr = {'pull_request': {'base': {'sha': base}, 'head': {'sha': head}}}
        with self.event(pr):
            errors = policy.ci_errors(workspace, github)
        self.assertEqual([(workspace, head)], seen)
        self.assertIn('unknown_key', '\n'.join(errors))
        with self.event(pr):
            self.assertEqual([], policy.ci_errors(workspace, lambda *_: None))

    def test_push_without_before_falls_back_to_protected_branches(self):
        workspace = self.repo('ws')
        self.commit(workspace, 'base', files={GOOD_MSG: GOOD})
        self.git(workspace, 'push', '-q', 'origin', 'nightly')
        self.git(workspace, 'fetch', '-q', 'origin')
        self.git(workspace, 'switch', '-q', '-c', 'feature')
        new = self.commit(workspace, 'feature')
        seen = []
        with self.event({'before': policy.ZERO, 'after': new}, 'refs/heads/feature'):
            policy.ci_errors(workspace, lambda repo, oid, nested: seen.append(oid))
        self.assertEqual([new], seen)

    def response(self, payload):
        stream = io.BytesIO(json.dumps(payload).encode())
        stream.__enter__ = lambda *_: stream
        stream.__exit__ = lambda *_: None
        return stream

    def test_github_api_requires_exact_sha_and_verified_signature(self):
        repo = self.repo('pkg')
        self.git(repo, 'remote', 'set-url', 'origin', 'https://github.com/Org/pkg.git')
        oid = 'a' * 40
        cases = [({'sha': oid, 'commit': {'verification': {'verified': True}}}, None),
                 ({'sha': oid, 'commit': {'verification': {'verified': False,
                                                            'reason': 'unsigned'}}}, 'unsigned'),
                 ({'sha': 'b' * 40, 'commit': {'verification': {'verified': True}}}, 'does not')]
        for payload, expected in cases:
            with mock.patch.dict(os.environ, {'GITHUB_TOKEN': 'token'}), mock.patch(
                    'urllib.request.urlopen', return_value=self.response(payload)) as urlopen:
                result = policy.github_signature(repo, oid, False)
            request = urlopen.call_args[0][0]
            self.assertEqual(f'https://api.github.com/repos/Org/pkg/commits/{oid}',
                             request.full_url)
            self.assertEqual('Bearer token', request.get_header('Authorization'))
            self.assertTrue(expected in result if expected else result is None, result)
        missing = urllib.error.HTTPError('url', 422, 'missing', {}, None)
        with mock.patch('urllib.request.urlopen', side_effect=missing):
            self.assertIn('push it there first', policy.github_signature(repo, oid, False))
        limited = urllib.error.HTTPError('url', 403, 'rate limited', {}, None)
        with mock.patch('urllib.request.urlopen', side_effect=limited), \
                self.assertRaises(ValueError):
            policy.github_signature(repo, oid, False)


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
        self.git(nested, 'config', 'gpg.ssh.allowedSignersFile', str(self.signers))
        self.assertEqual([nested], install_policy_hooks.submodules(workspace))
        self.install(workspace, [workspace, *install_policy_hooks.submodules(workspace)], HOOKS)
        (nested / 'msg/Bad.msg').write_text('float64 x\n')
        self.git(nested, 'add', 'msg/Bad.msg')
        with self.assertRaisesRegex(AssertionError, 'std_msgs/Header'):
            self.commit(nested, 'package pre-commit')
        self.git(nested, 'rm', '-q', '--cached', 'msg/Bad.msg')
        unsigned = self.commit(nested, 'package unsigned', sign=False)
        with self.assertRaisesRegex(AssertionError, 'commit is unsigned'):
            self.git(nested, 'push', '-q', 'origin', 'HEAD:nightly')  # package pre-push
        self.git(nested, 'push', '-q', '--no-verify', 'origin', 'HEAD:work')
        self.git(workspace, 'add', 'child')
        self.commit(workspace, 'bump child')
        leaked = {'GIT_DIR': str(workspace / '.git'), 'GIT_WORK_TREE': str(workspace)}
        with self.assertRaisesRegex(AssertionError, f'child@{unsigned[:12]}: commit is unsigned'):
            self.git(workspace, 'push', '-q', 'origin', 'nightly', env=leaked)

    def test_pre_push_checks_contracts_that_skipped_pre_commit(self):
        repo = self.repo('pkg')
        self.commit(repo, files={GOOD_MSG: GOOD})
        self.install(repo, [repo], HOOKS)
        self.git(repo, 'switch', '-q', '-c', 'side')
        (repo / 'msg/Bad.msg').write_text('float64 x\n')
        self.git(repo, 'add', 'msg/Bad.msg')
        self.git(repo, 'commit', '-q', '--no-verify', '-S', '-m', 'bad message')
        self.git(repo, 'switch', '-q', 'nightly')
        self.git(repo, 'merge', '-q', '-S', '--no-edit', 'side')  # fast-forward skips hooks
        with self.assertRaisesRegex(AssertionError, 'msg/Bad.msg: top-level'):
            self.git(repo, 'push', '-q', 'origin', 'nightly')

    def test_installed_hooks_reject_staged_contracts_and_unsigned_config(self):
        repo = self.repo('pkg')
        self.install(repo, [repo], HOOKS)
        self.commit(repo, files={GOOD_MSG: GOOD})
        (repo / 'msg/Bad.msg').write_text('float64 x\n')
        self.git(repo, 'add', 'msg/Bad.msg')
        with self.assertRaisesRegex(AssertionError, 'std_msgs/Header'):
            self.commit(repo, 'bad message')
        self.git(repo, 'rm', '-q', '--cached', 'msg/Bad.msg')
        self.git(repo, 'config', 'commit.gpgsign', 'false')
        with self.assertRaisesRegex(AssertionError, 'commit.gpgsign'):
            self.commit(repo, 'unsigned config', sign=False)
        self.git(repo, 'config', 'commit.gpgsign', 'true')
        self.commit(repo, 'unsigned anyway', sign=False)
        with self.assertRaisesRegex(AssertionError, 'unsigned'):
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
