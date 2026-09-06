#!/bin/bash
# smoke.sh -- prove the running Isaac ROS container is usable, without
# creating one. Read-only by default.
#
# This script NEVER starts a container or builds an image (see SKILL.md's
# attach-only rule). If nothing is running it says so and exits 1, and the
# fix is for the USER to run run_dev.sh.
#
# Usage:
#   .claude/skills/isaac-ros-docker/smoke.sh            # checks only
#   .claude/skills/isaac-ros-docker/smoke.sh --sim      # + headless sim launch,
#                                                       # topic check, teardown
#
# Env: ISAAC_ROS_CONTAINER to override the container name.
set -uo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS="$(cd "$SKILL_DIR/../../../isaac_ros_common/scripts" && pwd)"
DEXEC="$SCRIPTS/dexec.sh"
KILL_LAUNCH="$SCRIPTS/kill_launch.sh"
CONTAINER="${ISAAC_ROS_CONTAINER:-isaac_ros_dev-x86_64-container}"
RUN_SIM=0
[ "${1:-}" = "--sim" ] && RUN_SIM=1

fail() { echo "FAIL: $*" >&2; exit 1; }
ok()   { echo "  ok: $*"; }

echo "== 1. container running?"
if [ "$(docker inspect -f '{{.State.Running}}' "$CONTAINER" 2>/dev/null)" != "true" ]; then
    echo "No container named '$CONTAINER' is running." >&2
    echo "Do NOT start one yourself. Ask the user to run:" >&2
    echo "  cd src/isaac_ros_common/scripts && ./run_dev.sh -b" >&2
    exit 1
fi
ok "$CONTAINER up"

echo "== 2. bind mount is the workspace ROOT (build/ install/ log/ src/)"
docker inspect -f '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{"\n"}}{{end}}' "$CONTAINER" | grep isaac_ros-dev
"$DEXEC" -- ls /workspaces/isaac_ros-dev | tr '\n' ' '; echo
"$DEXEC" -- test -d /workspaces/isaac_ros-dev/src || fail "no src/ in the mount (ISAAC_ROS_WS unset when run_dev.sh ran?)"
ok "src/ present"

echo "== 3. env parity through dexec.sh (bare 'docker exec' gets none of this)"
"$DEXEC" -- bash -c 'echo "  user=$(whoami) ROS_DOMAIN_ID=$ROS_DOMAIN_ID RMW=$RMW_IMPLEMENTATION"
echo "  FASTRTPS_DEFAULT_PROFILES_FILE=$FASTRTPS_DEFAULT_PROFILES_FILE DISPLAY=$DISPLAY"' \
    || fail "dexec.sh env probe failed"

echo "== 4. which workspace each package resolves to (see SKILL.md: Two workspaces)"
printf '  %-22s %-42s %s\n' PACKAGE 'dexec.sh (your src/ edits win)' 'user terminal (bashrc only)'
for p in sim thornbots_pkg sentry_localization sllidar_ros2; do
    a=$("$DEXEC" -- ros2 pkg prefix "$p" 2>&1 | tail -1)
    b=$(docker exec -u admin "$CONTAINER" bash -c \
        "export PS1='\$ '; source /etc/bash.bashrc >/dev/null; ros2 pkg prefix $p" 2>&1 | tail -1)
    printf '  %-22s %-42s %s\n' "$p" "$a" "$b"
done

echo "== 5. ROS graph reachable"
"$DEXEC" -- ros2 topic list || fail "ros2 topic list failed"

echo "== 6. nothing already running (do not kill what you did not start)"
LIVE=$("$DEXEC" -- ps aux | grep -E 'ign gazebo|gz sim|slam_toolbox|amcl|map_server|ekf_filter_node|pose_translator|pose_emulator|ros2 launch' | grep -v grep)
if [ -n "$LIVE" ]; then
    echo "$LIVE"
    echo "  ^ a session is already live. ASK the user before touching it." >&2
    [ "$RUN_SIM" -eq 1 ] && fail "refusing to launch sim on top of a live session"
else
    ok "clean"
fi

[ "$RUN_SIM" -eq 0 ] && { echo "== done (pass --sim to also launch the sim stack)"; exit 0; }

echo "== 7. gz-sim installed? (fresh containers need install-sim.sh)"
if ! "$DEXEC" -- bash -c 'command -v ign || command -v gz' >/dev/null 2>&1; then
    echo "  gz/ign missing. Run this ONCE per container, backgrounded -- it pulls" >&2
    echo "  ~225 apt packages and takes minutes, and a foreground timeout that" >&2
    echo "  kills it leaves apt done but sim unbuilt:" >&2
    echo "    $DEXEC -r -- src/isaac_ros_common/docker/scripts/install-sim.sh" >&2
    exit 1
fi
ok "gz-sim present"

echo "== 8. launch sim headless, detached"
# FASTRTPS_DEFAULT_PROFILES_FILE is unset on BOTH the launch and every probe
# below. The baked profile makes each node a SUPER_CLIENT of three remote
# discovery servers on the robots' tailscale IPs; with none reachable, the
# whole stack runs but `ros2 topic list` returns 2 topics and rviz is empty.
# Unset on one side only is worse than not unsetting at all: the two halves
# then cannot see each other, with no error. See SKILL.md.
NOPROFILE='unset FASTRTPS_DEFAULT_PROFILES_FILE;'
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
