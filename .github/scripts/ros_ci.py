#!/usr/bin/env python3
"""Content-addressed build/test selection for the portable ROS CI job.

A package key hashes its committed git tree, the keys of its workspace
dependencies and the CI environment, so a change re-runs that package and
everything that depends on it. Design: docs/CI.md#warm-portable-ros-ci.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

IGNORE_MARKERS = ('COLCON_IGNORE', 'AMENT_IGNORE', 'CATKIN_IGNORE')
FIRMWARE_MARKER = 'MCB_FIRMWARE_BINARY'
FIRMWARE_PATH = 'firmware/MCBV3'
# The fork's 750-test suite belongs to its own repository (docs/CI.md).
SKIP_TESTS = frozenset({'robot_localization'})
DEPS_PACKAGE = 'thornbots_ros_ci_deps'


def sha256(*parts):
    digest = hashlib.sha256()
    for part in parts:
        data = part if isinstance(part, bytes) else str(part).encode()
        digest.update(len(data).to_bytes(8, 'big') + data)
    return digest.hexdigest()


def git(path, *args):
    return subprocess.run(['git', '-C', str(path), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


def discover(src):
    """Mirror colcon's discovery; the build job cross-checks it with colcon."""
    found = {}
    for root, dirs, files in os.walk(src):
        dirs[:] = sorted(d for d in dirs if not d.startswith('.'))
        if any(marker in files for marker in IGNORE_MARKERS):
            dirs[:] = []
        elif 'package.xml' in files:
            dirs[:] = []
            manifest = ET.parse(Path(root, 'package.xml')).getroot()
            name = manifest.findtext('name').strip()
            if name in found:
                sys.exit(f'duplicate package {name}: {found[name]["path"]} and {root}')
            deps = sorted({(child.text.strip(), child.get('condition', ''))
                           for child in manifest
                           if child.tag.endswith('depend') and child.text})
            found[name] = {'path': os.path.relpath(root, src), 'deps': deps}
    return found


def tree_id(path):
    """Committed tree of a package directory; refuses uncommitted content."""
    if git(path, 'status', '--porcelain', '--untracked-files=all', '--', '.'):
        sys.exit(f'{path} has uncommitted changes; its key would not describe them')
    prefix = git(path, 'rev-parse', '--show-prefix')
    return git(path, 'rev-parse', f'HEAD:{prefix}' if prefix else 'HEAD^{tree}')


def uses_firmware(path):
    return subprocess.run(['git', '-C', str(path), 'grep', '-q', '-F', FIRMWARE_MARKER, '--', '.'],
                          check=False).returncode == 0


def deps_manifest(packages):
    external = sorted({dep for info in packages.values() for dep in info['deps']
                       if dep[0] not in packages})
    lines = ['<?xml version="1.0"?>', '<package format="3">', f'  <name>{DEPS_PACKAGE}</name>',
             '  <version>0.0.0</version>', '  <description>Portable ROS CI dependencies</description>',
             '  <maintainer email="ci@thornbots.invalid">CI</maintainer>', '  <license>none</license>']
    for name, condition in external:
        attribute = f' condition="{condition}"' if condition else ''
        lines.append(f'  <depend{attribute}>{name}</depend>')
    return '\n'.join(lines + ['</package>', ''])


def image_tag(dockerfile, manifest_text):
    return 'ros-ci-' + sha256(Path(dockerfile).read_bytes(), manifest_text)[:24] + '-amd64'


def plan(args):
    src = Path(args.src)
    packages = discover(src)
    manifest_text = deps_manifest(packages)
    image = image_tag(args.dockerfile, manifest_text)
    firmware = git(src, 'rev-parse', f'HEAD:{FIRMWARE_PATH}') if args.firmware else 'absent'
    env = sha256(image, *args.env,
                 *(sha256(Path(f).name, Path(f).read_bytes()) for f in args.env_file))
    names = {name: {dep for dep, _ in info['deps'] if dep in packages}
             for name, info in packages.items()}
    keys, visiting = {}, set()

    def key(name):
        if name in keys:
            return keys[name]
        if name in visiting:
            sys.exit(f'dependency cycle through {name}')
        visiting.add(name)
        path = src / packages[name]['path']
        inputs = [env, name, tree_id(path)]
        if args.firmware and uses_firmware(path):
            packages[name]['firmware'] = True
            inputs.append(firmware)
        inputs += [f'{dep}={key(dep)}' for dep in sorted(names[name])]
        keys[name] = sha256(*inputs)
        return keys[name]

    for name in sorted(packages):
        packages[name].update(hash=key(name), ws_deps=sorted(names[name]))
        packages[name].setdefault('firmware', False)
    if args.scope == 'workspace':
        scope = sorted(packages)
    else:
        scope = sorted(n for n, info in packages.items()
                       if Path(info['path']).parts[:1] == (args.scope,))
        if not scope:
            sys.exit(f'no packages under {args.scope}')
    state = sha256(*(f'{n}={packages[n]["hash"]}' for n in scope))[:40]
    result = {'image': image, 'firmware': firmware, 'scope': scope, 'state': state,
              'packages': {n: {k: v for k, v in info.items() if k != 'deps'}
                           for n, info in packages.items()}}
    Path(args.out).write_text(json.dumps(result, indent=1, sort_keys=True) + '\n')
    if args.context:
        context = Path(args.context)
        (context / 'deps').mkdir(parents=True, exist_ok=True)
        (context / 'deps/package.xml').write_text(manifest_text)
        (context / 'Dockerfile').write_bytes(Path(args.dockerfile).read_bytes())
    for name in sorted(packages):
        print(f'{name:28} {packages[name]["hash"][:16]}  {packages[name]["path"]}')
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as output:
            output.write(f'image={image}\nstate={state}\nfirmware={firmware}\n')


def closure(packages, names):
    seen, stack = set(), list(names)
    while stack:
        name = stack.pop()
        if name not in seen:
            seen.add(name)
            stack += packages[name]['ws_deps']
    return seen


def select(args):
    """Write build/need/test lists: stale or unpassed scope packages and stale deps."""
    current = json.loads(Path(args.plan).read_text())
    packages = current['packages']
    path = Path(args.manifest)
    recorded = json.loads(path.read_text())['packages'] if path.exists() else {}

    def fresh(name):
        return recorded.get(name, {}).get('hash') == packages[name]['hash']

    test = sorted(n for n in current['scope']
                  if not (fresh(n) and recorded[n].get('passed')))
    build = sorted(set(test) | {n for n in closure(packages, test) if not fresh(n)})
    out = Path(args.out)
    (out / 'build.txt').write_text(''.join(f'{n}\n' for n in build))
    (out / 'need.txt').write_text(''.join(f'{n}\n' for n in test))
    (out / 'test.txt').write_text(''.join(f'{n}\n' for n in test if n not in SKIP_TESTS))
    firmware = any(packages[n]['firmware'] for n in test)
    (out / 'firmware.txt').write_text('yes\n' if firmware else 'no\n')
    print(f'build: {" ".join(build) or "(none)"}\ntest: {" ".join(test) or "(none)"}')


def verify(args):
    """Fail when colcon disagrees with the planner's packages or dependency edges."""
    packages = json.loads(Path(args.plan).read_text())['packages']
    listed = set(subprocess.run(['colcon', 'list', '--names-only', '--base-paths', args.src],
                                check=True, capture_output=True, text=True).stdout.split())
    if listed != set(packages):
        sys.exit(f'colcon packages {sorted(listed)} != planned {sorted(packages)}')
    dot = subprocess.run(['colcon', 'graph', '--dot', '--base-paths', args.src],
                         check=True, capture_output=True, text=True).stdout
    edges = re.findall(r'"([^"]+)"\s*->\s*"([^"]+)"', dot)
    if not edges and any(info['ws_deps'] for info in packages.values()):
        sys.exit('colcon graph reported no edges')
    # Edges point from a package to a direct or (dashed) indirect dependency.
    missing = [(a, b) for a, b in edges if b not in closure(packages, [a]) - {a}]
    if missing:
        sys.exit(f'colcon dependency edges missing from the plan: {missing}')
    print(f'colcon agrees: {len(listed)} packages, {len(edges)} edges')


def record(args):
    """Record built keys, and passes only for a fully successful test run."""
    packages = json.loads(Path(args.plan).read_text())['packages']
    path = Path(args.manifest)
    state = json.loads(path.read_text()) if path.exists() else {'packages': {}}
    for name in args.built:
        state['packages'][name] = {'hash': packages[name]['hash'], 'passed': False}
    if args.passed:
        for name in args.tested:
            entry = state['packages'].get(name, {})
            if entry.get('hash') != packages[name]['hash']:
                sys.exit(f'{name} passed tests but its install tree is stale')
            entry['passed'] = True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=1, sort_keys=True) + '\n')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    p = sub.add_parser('plan')
    p.add_argument('src')
    p.add_argument('--dockerfile', required=True)
    p.add_argument('--scope', default='workspace')
    p.add_argument('--firmware', action='store_true', help='firmware gitlink feeds the keys')
    p.add_argument('--env', action='append', default=[], help='extra key input')
    p.add_argument('--env-file', action='append', default=[], help='file whose content keys all')
    p.add_argument('--context', help='write the image build context here')
    p.add_argument('--out', required=True)
    p.set_defaults(func=plan)
    s = sub.add_parser('select')
    s.add_argument('--plan', required=True)
    s.add_argument('--manifest', required=True)
    s.add_argument('--out', required=True)
    s.set_defaults(func=select)
    v = sub.add_parser('verify')
    v.add_argument('src')
    v.add_argument('--plan', required=True)
    v.set_defaults(func=verify)
    r = sub.add_parser('record')
    r.add_argument('--plan', required=True)
    r.add_argument('--manifest', required=True)
    r.add_argument('--built', nargs='*', default=[])
    r.add_argument('--tested', nargs='*', default=[])
    r.add_argument('--passed', action='store_true')
    r.set_defaults(func=record)
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == '__main__':
    main()
