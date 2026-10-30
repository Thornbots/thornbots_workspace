#!/usr/bin/env bash
# Host-side nightly image build/test/push; see docs/CI.md#nightly-tests.
# NIGHTLY_PUBLISH_PUSH=0 exercises the build and tests without registry writes.
set -euo pipefail
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
SRC="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$SRC"
ACM="$SRC/isaac_ros_common/scripts/agent_container.sh"
# A unique task lets cleanup reuse ACM's locked, idle-only Colima shutdown.
task_dir="$(mktemp -d /tmp/nightly-publish.XXXXXXXX)"
task="publish-$(basename "$task_dir" | tr '[:upper:].' '[:lower:]-')"
rmdir "$task_dir"
build_root="$(mktemp -d "$SRC/../robot-publish.XXXXXXXX")"
cleanup() {
    local rc=$?
    "$ACM" down "$task" || rc=1
    rm -rf "$build_root"
    exit "$rc"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
trap 'exit 129' HUP
colima status >/dev/null 2>&1 || colima start
export DOCKER_HOST="unix://$HOME/.colima/default/docker.sock"

# setup_workspace.sh writes above the workspace; isolate that shared CLI path.
git clone --quiet --shared --no-checkout "$SRC" "$build_root/ws/src"
git -C "$build_root/ws/src" checkout --quiet --detach "$(git rev-parse HEAD)"
SRC="$build_root/ws/src"
cd "$SRC"
# Match all image gitlinks checked by pull_robot_image.sh, including children.
while read -r _ package; do
    case "$package" in sim|firmware|firmware/*) continue ;; esac
    git submodule update --init --recursive --checkout -- "$package"
done < <(git config --file .gitmodules --get-regexp '^submodule\..*\.path$')

# Only unused cache is eligible; retain 12 GB for rebuilds.
docker builder prune -f --keep-storage 12GB
bash isaac_ros_common/scripts/build_robot_image.sh
names="$(DRY_RUN=1 bash isaac_ros_common/scripts/build_robot_image.sh)"
source_tag="${names%%$'\n'*}"
docker image inspect "$source_tag" >/dev/null
revision="$(git rev-parse HEAD)"
registry_tag="ghcr.io/thornbots/isaac-ros:sha-${revision}-arm64-jetpack"
docker tag "$source_tag" "$registry_tag"
echo "Robot image: $registry_tag (CLI image: $source_tag)"
"$ACM" up "$task" -w "$SRC" -i "$registry_tag"
ISAAC_ROS_CONTAINER="isaac-agent-$task" bash isaac_ros_common/scripts/dexec.sh -r -- /bin/bash -c '
    set -eo pipefail
    source /opt/ros/jazzy/setup.bash
    source /workspaces/ros2_ws/install/setup.bash
    cd /workspaces/ros2_ws
    colcon test --return-code-on-test-failure --event-handlers console_direct+
    colcon test-result --verbose'
echo 'In-image colcon test: PASS'
[ "${NIGHTLY_PUBLISH_PUSH:-1}" != 0 ] || { echo 'Push disabled; build and test only'; exit 0; }

push_tag() {
    local tag="$1" output rc
    rc=0
    output="$(docker push "$tag" 2>&1)" || rc=$?
    printf '%s\n' "$output"
    if [ "$rc" -ne 0 ]; then
        if printf '%s\n' "$output" | grep -Ei 'unauthorized|denied|authentication|forbidden|no basic auth|401|403' >/dev/null; then
            echo 'Publish auth failed: docker login ghcr.io with a write:packages token.'
        fi
        return "$rc"
    fi
}
push_tag "$registry_tag"
branch_tag=ghcr.io/thornbots/isaac-ros:nightly-arm64-jetpack
docker tag "$registry_tag" "$branch_tag"
push_tag "$branch_tag"
# Both pushes succeeded: cleanup below is best effort and never fails publication.
# docker refuses to remove a tag a container uses; that tag is kept.
while read -r tag; do
    case "$tag" in
        ghcr.io/thornbots/isaac-ros:sha-*-arm64-jetpack)
            [ "$tag" = "$registry_tag" ] || docker image rm "$tag" || echo "Kept $tag"
            ;;
    esac
done < <(docker image ls --format '{{.Repository}}:{{.Tag}}')
docker builder prune -f --keep-storage 12GB || echo 'Build cache prune failed'
