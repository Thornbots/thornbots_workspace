"""Point this checkout's repositories at the shared policy hooks (local config only).

Refuses to replace another hooks path or unmanaged hooks; rerunning is a no-op.
Also sets push.recurseSubmodules=check so the workspace cannot push gitlinks to
unpushed package commits. See docs/CI.md#repository-policy.
"""

import argparse
from pathlib import Path
import subprocess
import sys


WORKSPACE = Path(__file__).resolve().parents[1]


def git(repo, *args, allowed=(0,)):
    result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True,
                            check=False)
    if result.returncode not in allowed:
        raise ValueError(f'{repo}: git {args[0]}: {result.stderr.strip()}')
    return result.stdout.strip()


def submodules(workspace):
    """Initialized first-level submodules; vendored nested repositories keep their hooks."""
    paths = git(workspace, 'submodule', '--quiet', 'foreach', 'echo "$sm_path"').splitlines()
    return [workspace / p for p in paths if p]


def plan(repo, hooks):
    """Local config changes needed for one repository, or ValueError if unsafe."""
    current = git(repo, 'config', '--path', '--get', 'core.hooksPath', allowed=(0, 1))
    if current:
        resolved = Path(current) if Path(current).is_absolute() else repo / current
        if resolved.resolve() != hooks.resolve():
            raise ValueError(f'{repo}: core.hooksPath is {current}; refusing to replace it')
        return []
    directory = Path(git(repo, 'rev-parse', '--path-format=absolute', '--git-path', 'hooks'))
    existing = sorted(p.name for p in directory.glob('*')
                      if p.is_file() and not p.name.endswith('.sample'))
    if existing:
        raise ValueError(f'{repo}: unmanaged hooks {", ".join(existing)} in {directory}; '
                         'move them before installing')
    return [('core.hooksPath', str(hooks))]


def install(workspace, repos, hooks, dry_run=False):
    changes = {repo: plan(repo, hooks) for repo in repos}  # validate all before changing any
    recurse = git(workspace, 'config', '--get', 'push.recurseSubmodules', allowed=(0, 1))
    if not recurse:
        changes[workspace] = changes.get(workspace, []) + [('push.recurseSubmodules', 'check')]
    elif recurse not in {'check', 'on-demand'}:
        print(f'{workspace}: push.recurseSubmodules={recurse} left unchanged', file=sys.stderr)
    for repo, settings in changes.items():
        for key, value in settings:
            print(f'{repo}: {"would set" if dry_run else "set"} {key}={value}')
            if not dry_run:
                git(repo, 'config', '--local', key, value)
        if not settings:
            print(f'{repo}: already installed')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--recursive', action='store_true', help='include package submodules')
    parser.add_argument('--dry-run', action='store_true', help='print changes only')
    args = parser.parse_args()
    repos = [WORKSPACE] + (submodules(WORKSPACE) if args.recursive else [])
    try:
        install(WORKSPACE, repos, WORKSPACE / '.githooks', args.dry_run)
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
