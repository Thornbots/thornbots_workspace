"""Apply CI-only protection to each Thornbots repo's main branch."""

import argparse
import json
import subprocess
import sys

PORTABLE = {
    'thornbots_pkg', 'sim', 'sentry_localization', 'rf2o_laser_odometry',
    'ros2_dji_serial_bridge', 'Realsense_ROI_Depth_Rectifier', 'sllidar_ros2',
}
REPOS = ['thornbots_workspace', *sorted(PORTABLE), 'isaac_ros_common',
         'isaac-ros-startup', 'realsense-yolov8-nitros-bridge', 'MCBV3']


def api(path, payload=None):
    command = ['gh', 'api', path]
    if payload is not None:
        command += ['--method', 'PUT', '--input', '-']
    result = subprocess.run(command, input=json.dumps(payload) if payload else None,
                            text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.strip())
    return json.loads(result.stdout)


def policy(repo):
    contexts = ['quality / lint']
    if repo in PORTABLE or repo == 'thornbots_workspace':
        contexts.append('ros / portable')
    if repo == 'thornbots_workspace':
        contexts.append('Robot image build and tests')
    if repo == 'MCBV3':
        contexts += ['ARM / infantry', 'ARM / hero', 'ARM / sentry',
                     'Hosted control and UART tests']
    return {
        'required_status_checks': {'strict': True, 'contexts': contexts},
        'enforce_admins': True,
        'required_pull_request_reviews': None,
        'restrictions': None,
        'required_linear_history': False,
        'allow_force_pushes': False,
        'allow_deletions': False,
        'block_creations': False,
        'required_conversation_resolution': True,
        'lock_branch': False,
        'allow_fork_syncing': False,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--repo', choices=REPOS, action='append')
    args = parser.parse_args()
    failed = False
    for repo in args.repo or REPOS:
        branch = 'main'
        endpoint = f'repos/Thornbots/{repo}/branches/{branch}/protection'
        if not args.apply:
            print(json.dumps({'endpoint': endpoint, 'policy': policy(repo)}))
            continue
        try:
            metadata = api(f'repos/Thornbots/{repo}')
            if not metadata.get('permissions', {}).get('admin'):
                print(f'{repo}/{branch}: skipped; no admin access')
                continue
            api(endpoint, policy(repo))
            actual = api(endpoint)
            assert actual['required_status_checks']['contexts'] == policy(repo)['required_status_checks']['contexts']
            assert actual['enforce_admins']['enabled']
            assert not actual['allow_force_pushes']['enabled']
            assert not actual['allow_deletions']['enabled']
            print(f'{repo}/{branch}: protected, verified; zero required reviews')
        except (RuntimeError, AssertionError) as error:
            failed = True
            print(f'{repo}/{branch}: {error}', file=sys.stderr)
    return int(failed)


if __name__ == '__main__':
    sys.exit(main())
