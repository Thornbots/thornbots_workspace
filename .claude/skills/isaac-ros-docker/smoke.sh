#!/bin/bash
# smoke.sh -- prove the running Isaac ROS container is usable, without
# creating one. Read-only by default.
#
# This script NEVER starts a container or builds an image (see SKILL.md's
# attach-only rule). If nothing is running it says so and exits 1, and the
# fix is for the USER to run `isaac-ros activate`.
#
# Usage:
#   .claude/skills/isaac-ros-docker/smoke.sh            # checks only
#   .claude/skills/isaac-ros-docker/smoke.sh --sim      # + headless sim launch,
#                                                       # topic check, teardown
#
# Container name: isaac_ros_common/scripts/container.sh (same rule as dexec.sh).
set -uo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS="$(cd "$SKILL_DIR/../../../isaac_ros_common/scripts" && pwd)"
DEXEC="$SCRIPTS/dexec.sh"
KILL_LAUNCH="$SCRIPTS/kill_launch.sh"
source "$SCRIPTS/container.sh"
RUN_SIM=0
[ "${1:-}" = "--sim" ] && RUN_SIM=1

fail() { echo "FAIL: $*" >&2; exit 1; }
ok()   { echo "  ok: $*"; }

echo "== 1. container running?"
if [ "$(docker inspect -f '{{.State.Running}}' "$CONTAINER" 2>/dev/null)" != "true" ]; then
    echo "No container named '$CONTAINER' is running." >&2
    echo "Do NOT start one yourself. Ask the user to run:" >&2
    echo "  ISAAC_ROS_WS=<workspace> isaac-ros activate" >&2
    exit 1
fi
ok "$CONTAINER up"
# Dockerfile.mac (docker/README.md) has no NVIDIA by design.
MAC=0
[ "$(docker inspect -f '{{.Config.Image}}' "$CONTAINER")" = thornbots-mac ] && MAC=1
if [ "$MAC" -eq 1 ]; then
    ok "Mac image: no NVIDIA, gz and rviz on llvmpipe (VNC at vnc://localhost:5901)"
else
# --gpus all through a stale /etc/cdi/nvidia.yaml mounts no driver libs.
docker exec "$CONTAINER" sh -c 'ldconfig -p | grep -q "libcuda.so.1 " || ls /usr/lib/*/tegra/libcuda.so.1' >/dev/null 2>&1 \
    || fail "no libcuda.so.1 in the container: the host's CDI spec is stale (SKILL.md: Troubleshooting)"
ok "NVIDIA driver libraries mounted"
fi

echo "== 2. bind mount is the workspace ROOT (build/ install/ log/ src/)"
docker inspect -f '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{"\n"}}{{end}}' "$CONTAINER" | grep isaac_ros-dev
"$DEXEC" -- ls /workspaces/isaac_ros-dev | tr '\n' ' '; echo
"$DEXEC" -- test -d /workspaces/isaac_ros-dev/src || fail "no src/ in the mount (ISAAC_ROS_WS wrong when isaac-ros activate ran?)"
ok "src/ present"
WS_ROOT="$(cd "$SKILL_DIR/../../../.." && pwd)"
MOUNT_SRC=$(docker inspect -f '{{range .Mounts}}{{if eq .Destination "/workspaces/isaac_ros-dev"}}{{.Source}}{{end}}{{end}}' "$CONTAINER")
if [ "$MOUNT_SRC" = "$WS_ROOT" ]; then
    ok "mount is this checkout's workspace ($WS_ROOT)"
else
    echo "  WARN: mount is $MOUNT_SRC, not this checkout's $WS_ROOT; edits here won't run there" >&2
fi

echo "== 3. env parity through dexec.sh (bare 'docker exec' gets none of this)"
"$DEXEC" -- bash -c 'echo "  user=$(whoami) ROS_DOMAIN_ID=$ROS_DOMAIN_ID RMW=$RMW_IMPLEMENTATION"
echo "  FASTRTPS_DEFAULT_PROFILES_FILE=$FASTRTPS_DEFAULT_PROFILES_FILE DISPLAY=$DISPLAY"' \
    || fail "dexec.sh env probe failed"

echo "== 4. which workspace each package resolves to (see SKILL.md: Two workspaces)"
printf '  %-22s %-42s %s\n' PACKAGE 'dexec.sh (your src/ edits win)' 'user terminal (bashrc only)'
for p in sim thornbots_pkg sentry_localization sllidar_ros2; do
    a=$("$DEXEC" -- ros2 pkg prefix "$p" 2>&1 | tail -1)
    b=$(docker exec -u "$CONTAINER_USER" "$CONTAINER" bash -c \
        "export PS1='\$ '; source /etc/bash.bashrc >/dev/null; ros2 pkg prefix $p" 2>&1 | tail -1)
    printf '  %-22s %-42s %s\n' "$p" "$a" "$b"
done

echo "== 5. ROS graph reachable"
"$DEXEC" -- ros2 topic list || fail "ros2 topic list failed"

echo "== 6. nothing already running (do not kill what you did not start)"
LIVE=$("$DEXEC" -- ps aux | grep -E 'gz sim|slam_toolbox|amcl|map_server|ekf_filter_node|pose_translator|pose_emulator|ros2 launch' | grep -v grep)
if [ -n "$LIVE" ]; then
    echo "$LIVE"
    echo "  ^ a session is already live. ASK the user before touching it." >&2
    [ "$RUN_SIM" -eq 1 ] && fail "refusing to launch sim on top of a live session"
else
    ok "clean"
fi

[ "$RUN_SIM" -eq 0 ] && { echo "== done (pass --sim to also launch the sim stack)"; exit 0; }

echo "== 7. gz-sim installed? (fresh containers need install-sim.sh)"
# dexec.sh sources ROS first: Jazzy's gz is on PATH only after that.
if ! "$DEXEC" -- bash -c 'command -v gz' >/dev/null 2>&1; then
    echo "  gz missing. Run this ONCE per container, backgrounded -- it pulls" >&2
    echo "  a few hundred apt packages and takes minutes, and a foreground timeout that" >&2
    echo "  kills it leaves apt done but sim unbuilt:" >&2
    echo "    $DEXEC -r -- src/isaac_ros_common/docker/scripts/install-sim.sh" >&2
    exit 1
fi
ok "gz-sim present"

echo "== 8. launch sim headless, detached"
# Runs under the baked DDS profile on purpose: local discovery must work with
# it.
NOPROFILE=''
"$DEXEC" -- bash -c "$NOPROFILE ros2 daemon stop" >/dev/null 2>&1
"$DEXEC" -d -- bash -c "$NOPROFILE exec ros2 launch sim sim.launch.py gui:=false"
echo "   waiting for the graph to come up (rviz opens on the user's display)..."
for i in $(seq 1 30); do
    sleep 2
    n=$("$DEXEC" -- bash -c "$NOPROFILE ros2 topic list" 2>/dev/null | wc -l)
    [ "$n" -gt 5 ] && break
done
"$DEXEC" -- bash -c "$NOPROFILE ros2 topic list"
n=$("$DEXEC" -- bash -c "$NOPROFILE ros2 topic list" 2>/dev/null | wc -l)
[ "$n" -gt 5 ] && ok "$n topics" || echo "  only $n topics: discovery, not the launch. Read the log above." >&2

echo "== 9. teardown (kill_launch.sh, never pkill)"
PID=$("$KILL_LAUNCH" -l | awk '/ros2 launch/ {print $1; exit}')
if [ -n "$PID" ]; then
    "$KILL_LAUNCH" "$PID"
else
    echo "  no ros2 launch pid found -- check '$KILL_LAUNCH -l' by hand" >&2
fi
sleep 3
"$KILL_LAUNCH" -l
echo "== done"
