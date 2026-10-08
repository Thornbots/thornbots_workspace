"""Lint tracked first-party files; keep existing debt from growing."""

import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

import yaml


def run(args, allowed=(0,)):
    result = subprocess.run(args, text=True, capture_output=True, check=False)
    if result.returncode not in allowed:
        raise RuntimeError(f'{args[0]} failed: {result.stdout}{result.stderr}')
    return result


def tracked_files(root):
    paths = run(['git', '-C', str(root), 'ls-files', '-z']).stdout.split('\0')
    excluded = {'taproot', 'taproot-scripts', 'sdk', 'build', 'install', 'log'}
    return [p for p in paths if p and not excluded.intersection(Path(p).parts)
            and (root / p).is_file() and not (root / p).is_symlink()]


def diagnostics(root):
    files = tracked_files(root)
    findings = []
    python_files = [p for p in files if p.endswith('.py')]
    if python_files:
        result = run([sys.executable, '-m', 'ruff', 'check', '--isolated',
                      '--select', 'E9,F', '--ignore', 'F403,F405',
                      '--output-format', 'json', *python_files], (0, 1))
        for item in json.loads(result.stdout):
            path = str(Path(item['filename']).relative_to(root))
            findings.append((path, item['code'], item['message']))
    shell_files = [p for p in files if p.endswith('.sh')]
    if shell_files:
        result = run(['shellcheck', '--severity=error', '--format=json',
                      *shell_files], (0, 1))
        for item in json.loads(result.stdout):
            findings.append((item['file'], f"SC{item['code']}", item['message']))
    cpp_files = [p for p in files if Path(p).suffix in {'.c', '.cc', '.cpp', '.h', '.hpp'}]
    if cpp_files:
        result = run([sys.executable, '-m', 'cpplint', '--quiet',
                      '--filter=-,+runtime/int,+runtime/printf,+runtime/memset,'
                      '+runtime/explicit,+runtime/string,+readability/casting',
                      *cpp_files], (0, 1))
        for line in result.stderr.splitlines():
            match = re.match(r'^(.*):\d+:\s+(.*?)\s+\[([^]]+)\]\s+\[\d\]$', line)
            if match:
                findings.append((match[1], match[3], match[2]))
    for path in files:
        try:
            if path.endswith(('.xml', '.xacro')):
                ET.parse(root / path)
            elif path.endswith(('.yaml', '.yml')):
                contents = (root / path).read_text()
                if not contents.startswith('%YAML:1.0'):
                    list(yaml.safe_load_all(contents))
        except (ET.ParseError, yaml.YAMLError) as error:
            findings.append((path, 'parse', str(error)))
    return Counter(json.dumps(item) for item in findings)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', action='store_true', help='record reviewed existing debt')
    args = parser.parse_args()
    root = Path.cwd().resolve()
    baseline_path = root / '.github/quality-baseline.json'
    current = diagnostics(root)
    if args.baseline:
        baseline_path.parent.mkdir(parents=True, exist_ok=True)
        baseline_path.write_text(json.dumps(dict(sorted(current.items())), indent=2) + '\n')
        print(f'Recorded {sum(current.values())} existing diagnostics.')
        return 0
    baseline = Counter(json.loads(baseline_path.read_text())) if baseline_path.exists() else Counter()
    added = current - baseline
    for finding, count in sorted(added.items()):
        path, rule, message = json.loads(finding)
        print(f'{path}: {rule}: {message} ({count})')
    print(f'{len(tracked_files(root))} files checked; {sum(current.values())} existing '
          f'diagnostics; {sum(added.values())} new.')
    if any(json.loads(f)[1] in {'parse', 'invalid-syntax'}
           or json.loads(f)[1].startswith(('E9', 'SC1')) for f in current):
        print('Syntax errors must be fixed; they cannot be baselined.')
        return 1
    return int(bool(added))


if __name__ == '__main__':
    sys.exit(main())
