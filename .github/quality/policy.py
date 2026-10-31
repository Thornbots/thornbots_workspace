"""Check gitlink moves and ROS message stamps.

Coverage and limits: docs/CI.md#repository-policy. Hooks give early feedback;
`ci` checks the same rules on the pushed or proposed range.
"""

import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


ZERO = '0' * 40
TOOLING = Path(__file__).resolve().parents[2]
REVIEWED = '.github/quality/reviewed_history'
VENDOR = {'sdk', 'taproot', 'taproot-scripts'}
PROTECTED = ('main', 'nightly')
# Variables git sets for hooks; they must not leak into nested repositories.
HOOK_ENV = ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_PREFIX',
            'GIT_OBJECT_DIRECTORY', 'GIT_ALTERNATE_OBJECT_DIRECTORIES', 'GIT_COMMON_DIR')

def run_git(repo, args, nested):
    env = {k: v for k, v in os.environ.items() if not (nested and k in HOOK_ENV)}
    return subprocess.run(['git', '-C', str(repo), '-c', 'log.showSignature=false', *args],
                          capture_output=True, text=True, check=False, env=env)


def git(repo, *args, allowed=(0,), nested=False):
    result = run_git(repo, args, nested)
    if result.returncode not in allowed:
        raise ValueError(f'git {" ".join(args[:2])} in {repo}: {result.stderr.strip()}')
    return result.stdout


def has_commit(repo, oid, nested=False):
    return bool(oid) and oid != ZERO and not run_git(
        repo, ['cat-file', '-e', f'{oid}^{{commit}}'], nested).returncode


def is_ancestor(repo, old, new, nested=False):
    return not run_git(repo, ['merge-base', '--is-ancestor', old, new], nested).returncode


def vendor(path):
    return any(p in VENDOR or re.fullmatch(r'isaac_ros_\w+_interfaces', p)
               for p in PurePosixPath(path).parts)


def entries(repo, rev, nested=False):
    """(mode, oid, path) for the index (rev None) or a commit's tree."""
    if rev is None:
        lines = git(repo, 'ls-files', '-s', '-z', nested=nested).split('\0')
        fields = (re.split(r'[ \t]', item, maxsplit=3) for item in lines if item)
        return [(m, o, p) for m, o, _, p in fields]
    lines = git(repo, 'ls-tree', '-r', '-z', '--full-tree', rev, nested=nested).split('\0')
    fields = (re.split(r'[ \t]', item, maxsplit=3) for item in lines if item)
    return [(m, o, p) for m, _, o, p in fields]


def gitlinks(repo, rev, nested=False):
    return {p: o for m, o, p in entries(repo, rev, nested) if m == '160000' and not vendor(p)}


def contract_errors(repo, rev=None, nested=False, label='.'):
    """Internal .msg files carry std_msgs/Header and document header.stamp."""
    texts = {p: git(repo, 'cat-file', 'blob', o, nested=nested)
             for m, o, p in entries(repo, rev, nested)
             if m in {'100644', '100755'} and p.endswith('.msg') and not vendor(p)}
    embedded = set()  # element types; only top-level messages need their own header
    for path, text in texts.items():
        for line in text.splitlines():
            field = line.split('#', 1)[0].split()
            if len(field) >= 2:
                kind = re.sub(r'[\[<].*', '', field[0]).rsplit('/', 1)[-1]
                embedded.add((str(PurePosixPath(path).parent), kind))
    errors = []
    for path, text in sorted(texts.items()):
        comments = ' '.join(line.split('#', 1)[1] for line in text.splitlines() if '#' in line)
        header = re.search(r'^\s*std_msgs/(?:msg/)?Header\s+header\b', text, re.M)
        if header and not re.search(r'\bstamp\b', comments, re.I):
            errors.append(f'{label}/{path}: document what header.stamp means in a comment')
        own_type = (str(PurePosixPath(path).parent), PurePosixPath(path).stem)
        if not header and own_type not in embedded:
            errors.append(f'{label}/{path}: top-level internal messages need '
                          'std_msgs/Header header')
    return errors


def child_has(child, oid):
    """Uninitialized submodule paths must not fall through to the superproject."""
    return (child / '.git').exists() and has_commit(child, oid, nested=True)


def recursive_contracts(repo, rev, label='.', nested=False, skipped=None):
    """Strict unless `skipped` collects pins that are not available locally."""
    errors = contract_errors(repo, rev, nested, label)
    for path, oid in gitlinks(repo, rev, nested).items():
        child, child_label = repo / path, path if label == '.' else f'{label}/{path}'
        if not child_has(child, oid):
            if skipped is None:
                raise ValueError(f'{child_label}: initialize/fetch pinned commit {oid[:12]}')
            skipped.add(child_label)
            continue
        errors += recursive_contracts(child, oid, child_label, True, skipped)
    return errors


def read_reviewed(repo, rev, nested=False):
    shown = run_git(repo, ['show', f'{rev}:{REVIEWED}'], nested)
    if shown.returncode:
        return None
    result = {}
    for line in shown.stdout.splitlines():
        fields = line.split('#', 1)[0].split()
        if len(fields) == 2:
            result.setdefault(fields[0], []).append(fields[1])
    return result


def reviewed_history(repo, bases, head, nested=False):
    """Reviewed history roots: from the first base that has them (the bootstrap uses head).

    Head may only add lines for gitlinks that no base already pins (new imports).
    """
    bases = [b for b in bases if has_commit(repo, b, nested)]
    found = (read_reviewed(repo, b, nested) for b in bases)
    trusted = next((r for r in found if r is not None), None)
    proposed = read_reviewed(repo, head, nested) or {}
    if trusted is None:
        return proposed
    existing = {'.'}.union(*(gitlinks(repo, b, nested) for b in bases))
    return {**{p: o for p, o in proposed.items() if p not in existing}, **trusted}


class Checker:
    """Check commits new to a range, then the package ranges their gitlinks move over."""

    def __init__(self):
        self.errors = []

    def check(self, repo, head, exclude, label='.', reviewed=None, nested=False):
        reviewed = reviewed if reviewed is not None else {}
        exclude = [o for o in exclude + reviewed.get(label, [])
                   if o.startswith('--') or has_commit(repo, o, nested)]
        commits = git(repo, 'rev-list', head, '--not', *exclude, '--', nested=nested).split()
        for path, old, new in self.moves(repo, commits, nested):
            child_label = path if label == '.' else f'{label}/{path}'
            child = repo / path
            if not child_has(child, new):
                self.errors.append(f'{child_label}: fetch/initialize gitlink target {new[:12]}')
            elif old is None and child_label not in reviewed:
                self.errors.append(f'{child_label}: new gitlink needs a reviewed history line in '
                                   f'{REVIEWED}')
            elif old is not None and not child_has(child, old):
                self.errors.append(f'{child_label}: fetch previous gitlink {old[:12]}')
            else:
                if old is not None and not is_ancestor(child, old, new, nested=True):
                    self.errors.append(f'{child_label}: gitlink {old[:12]} -> {new[:12]} is not '
                                       'a fast-forward; stale pins revert other work')
                self.check(child, new, [old] if old else [], child_label, reviewed, True)

    @staticmethod
    def moves(repo, commits, nested):
        """(path, old or None, new) for each gitlink a commit changes from any parent."""
        moves = []
        for oid in commits:
            parents = git(repo, 'rev-list', '--parents', '-n', '1', oid, nested=nested).split()[1:]
            after = gitlinks(repo, oid, nested)
            for before in [gitlinks(repo, p, nested) for p in parents] or [{}]:
                moves += [(p, before.get(p), new) for p, new in after.items()
                          if before.get(p) != new and (p, before.get(p), new) not in moves]
        return moves


def workspace_label(root):
    try:
        relative = root.resolve().relative_to(TOOLING)
    except ValueError:
        return '.'
    return relative.as_posix() if relative.parts else '.'


def pre_push(root, remote, lines):
    checker = Checker()
    label = workspace_label(root)
    contracts, skipped = [], set()
    for line in lines:
        _, local_oid, _, remote_oid = line.split()
        if local_oid == ZERO:
            continue
        bases = [remote_oid] + [f'refs/remotes/{remote}/{b}' for b in PROTECTED]
        reviewed = reviewed_history(root, bases, local_oid) if label == '.' else \
            reviewed_history(TOOLING, ['HEAD'], 'HEAD', nested=True)
        exclude = [remote_oid] if has_commit(root, remote_oid) else []
        exclude.append(f'--remotes={remote}')
        checker.check(root, local_oid, exclude, label, reviewed)
        # Merges, rebases and cherry-picks skip pre-commit; check what is pushed.
        contracts += (recursive_contracts(root, local_oid, skipped=skipped) if label == '.'
                      else contract_errors(root, local_oid, label=label))
    for path in sorted(skipped):  # e.g. skipped firmware; changed gitlinks were checked above
        print(f'Repository policy: {path} not initialized; skipped its .msg check',
              file=sys.stderr)
    return checker.errors + sorted(set(contracts))


def ci_errors(root):
    """Range from the GitHub event; review covers the code."""
    event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
    if event.get('pull_request'):
        head, bases = event['pull_request']['head']['sha'], [event['pull_request']['base']['sha']]
    else:
        head = event.get('after') or git(root, 'rev-parse', 'HEAD').strip()
        before = event.get('before')
        bases = [before] if before and has_commit(root, before) else [
            f'refs/remotes/origin/{b}' for b in PROTECTED
            if os.environ.get('GITHUB_REF') != f'refs/heads/{b}'
            and has_commit(root, f'refs/remotes/origin/{b}')]
    reviewed = reviewed_history(root, bases, head)
    checker = Checker()
    checker.check(root, head, bases, reviewed=reviewed)
    return checker.errors + recursive_contracts(root, head)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['pre-commit', 'pre-push', 'contracts',
                                         'commits', 'ci'])
    parser.add_argument('args', nargs='*', help='hook arguments')
    parser.add_argument('--repo', type=Path, default=Path.cwd())
    parser.add_argument('--rev', default='HEAD', help='contracts: revision to check')
    parser.add_argument('--head', default='HEAD', help='commits: last commit to check')
    parser.add_argument('--base', action='append', default=[], help='commits: exclude history')
    parser.add_argument('--recursive', action='store_true', help='contracts: include gitlinks')
    options = parser.parse_args()
    root = options.repo.resolve()
    try:
        if options.mode == 'pre-commit':
            errors = contract_errors(root)
        elif options.mode == 'pre-push':
            errors = pre_push(root, options.args[0], sys.stdin.read().splitlines())
        elif options.mode == 'contracts':
            errors = (recursive_contracts(root, options.rev) if options.recursive
                      else contract_errors(root, options.rev))
        elif options.mode == 'commits':
            checker = Checker()
            checker.check(root, options.head, options.base or ['--remotes=origin'],
                          workspace_label(root),
                          reviewed_history(root, options.base, options.head))
            errors = checker.errors
        else:
            errors = ci_errors(root)
    except (ValueError, OSError, KeyError, IndexError, AttributeError) as error:
        print(f'Repository policy: {error}', file=sys.stderr)
        return 1
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print('Repository policy failed: docs/CI.md#repository-policy', file=sys.stderr)
    else:
        print('Repository policy passed.')
    return int(bool(errors))


if __name__ == '__main__':
    sys.exit(main())
