#!/usr/bin/env bash
# nightly_tests.sh -- the nightly tests on the Mac mini (docs/CI.md#nightly-tests).
#
#   nightly_tests.sh run       # one night: update, test in a per-run container, report
#   nightly_tests.sh install   # (re)write and load the launchd LaunchAgent
#
# `run` updates a dedicated checkout to origin/$NIGHTLY_REF over public https,
# runs nightly_tests_inside.sh in a container made by agent_container.sh (which
# starts Colima and removes both afterwards), writes results/<date>/ with logs
# and a summary.txt, keeps the last 14, then dispatches GitHub CI on nightly
# without waiting. Exit status follows the local result only.
# Env: NIGHTLY_CI_ROOT (~/ros2_ws/nightly-ci), NIGHTLY_REF (nightly),
# NIGHTLY_URL, NIGHTLY_DISPATCH_REF (nightly; empty skips the dispatch).
# Needs bash 3.2 (macOS /bin/bash).
set -uo pipefail
export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

ROOT="${NIGHTLY_CI_ROOT:-$HOME/ros2_ws/nightly-ci}"
REF="${NIGHTLY_REF:-nightly}"
URL="${NIGHTLY_URL:-https://github.com/Thornbots/thornbots_workspace.git}"
DISPATCH_REF="${NIGHTLY_DISPATCH_REF-nightly}"
GH=/opt/homebrew/bin/gh
KEEP=14
TASK=nightly-ci
LABEL=com.thornbots.nightly-ci
SRC="$ROOT/src"
PORTABLE="thornbots_pkg sim sentry_localization rf2o_laser_odometry ros2_dji_serial_bridge Realsense_ROI_Depth_Rectifier sllidar_ros2"
# Repos with a `CI` workflow; MCBV3 also has firmware.yml.
CI_REPOS="thornbots_workspace $PORTABLE realsense-yolov8-nitros-bridge isaac_ros_common isaac-ros-startup MCBV3"

log() { echo "[$(date '+%F %T')] $*"; }

# True if some container on the (already running) Colima VM runs a sim stack.
other_stack() {
    local c
    colima status >/dev/null 2>&1 || return 1
    [ -S "$HOME/.colima/default/docker.sock" ] && export DOCKER_HOST="unix://$HOME/.colima/default/docker.sock"
    for c in $(docker ps -q 2>/dev/null); do
        if docker top "$c" -eo args 2>/dev/null | grep -Eq 'gz sim|ros2 launch|MCB-project|e2e_suite'; then
            echo "$(docker inspect -f '{{.Name}}' "$c")"; return 0
        fi
    done
    return 1
}

update_checkout() {
    if [ ! -d "$SRC/.git" ]; then
        git clone -q --no-checkout "$URL" "$SRC" || return 1
    fi
    cd "$SRC" || return 1
    git remote set-url origin "$URL"
    git fetch -q origin "$REF" || return 1
    git checkout -q --force --detach FETCH_HEAD || return 1
    git submodule foreach --recursive --quiet 'git reset -q --hard; git clean -ffdxq' >/dev/null 2>&1
    git clean -ffdxq
    git submodule sync -q --recursive
    git -c submodule.firmware/MCBV3.update=checkout submodule update -q --init --checkout --force --depth 1 -- \
        $PORTABLE isaac_ros_common firmware/MCBV3 || return 1
    git -C firmware/MCBV3 submodule update -q --init --checkout --force --depth 1 taproot-scripts || return 1
}

shas() { # "name sha" lines: the workspace, then each initialized submodule
    echo "workspace $(git -C "$SRC" rev-parse --short=9 HEAD)"
    git -C "$SRC" submodule status | sed 's/^[-+U ]//' | awk '{print $2, substr($1, 1, 9)}'
}

# Dispatch GitHub CI on nightly; record URLs; never fails the run.
dispatch_ci() { # outfile
    local out="$1" repo wf url
    [ -x "$GH" ] || { echo "ci dispatch skipped: no gh" >>"$out"; return; }
    for repo in $CI_REPOS; do
        for wf in CI $([ "$repo" = MCBV3 ] && echo firmware.yml); do
            if "$GH" workflow run "$wf" -R "Thornbots/$repo" --ref "$DISPATCH_REF" >/dev/null 2>&1; then
                sleep 4
                url="$("$GH" run list -R "Thornbots/$repo" -w "$wf" --branch "$DISPATCH_REF" -e workflow_dispatch \
                    -L 1 --json url -q '.[0].url' 2>/dev/null)"
                echo "ci $repo $wf ${url:-dispatched}" >>"$out"
            else
                echo "ci $repo $wf DISPATCH-FAILED" >>"$out"
            fi
        done
    done
}

LOCK="$ROOT/.lock"
cmd_run() {
    local day out n pid
    mkdir -p "$ROOT/results"
    while ! mkdir "$LOCK" 2>/dev/null; do
        pid="$(cat "$LOCK/pid" 2>/dev/null)"
        if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then log "another nightly run (pid $pid) is active"; exit 0; fi
        rm -rf "$LOCK"
    done
    echo $$ >"$LOCK/pid"
    trap 'rm -rf "$LOCK"' EXIT

    day="$(date +%F)"; out="$ROOT/results/$day"
    [ ! -e "$out" ] || out="$ROOT/results/$day-$(date +%H%M)"
    mkdir -p "$out"
    exec > >(tee -a "$out/run.log") 2>&1
    local t0; t0=$(date +%s)
    log "nightly tests for $URL $REF -> $out"

    if n="$(other_stack)"; then
        log "SKIP: sim stack running in container $n"
        echo "SKIP $day: sim stack running in $n" >"$out/summary.txt"
        exit 0
    fi

    local verdict=PASS
    if ! update_checkout; then
        log "checkout update failed"
        echo "FAIL $day: checkout update failed (see run.log)" >"$out/summary.txt"
        exit 1
    fi
    shas >"$out/shas.txt"
    local acm="$SRC/isaac_ros_common/scripts/agent_container.sh"
    if [ ! -x "$acm" ]; then
        echo "FAIL $day: $REF has no isaac_ros_common/scripts/agent_container.sh" >"$out/summary.txt"
        exit 1
    fi
    # A leftover from a crashed night has our task name and label.
    "$acm" down "$TASK" >/dev/null 2>&1
    : >"$out/status.tsv"
    "$acm" run "$TASK" -w "$SRC" -e "$out" -- bash src/.github/scripts/nightly_tests_inside.sh
    log "container run exit $?; container and Colima cleanup done by agent_container.sh"

    local parts="" name res
    while IFS="$(printf '\t')" read -r name res _; do
        parts="$parts $name=$res"
        [ "$res" = FAIL ] && verdict=FAIL
    done <"$out/status.tsv"
    [ -n "$parts" ] || { parts=" no-results"; verdict=FAIL; }
    echo "$verdict $day$parts | $(awk '{printf "%s@%s ", $1, $2}' "$out/shas.txt")| $(( ($(date +%s) - t0) / 60 )) min" >"$out/summary.txt"
    # Sorted to oldest-first; drop all but the newest $KEEP.
    ls -1d "$ROOT"/results/2* 2>/dev/null | sort | awk -v k="$KEEP" '{a[NR]=$0} END{for(i=1;i<=NR-k;i++) print a[i]}' \
        | while read -r d; do rm -rf "$d"; done

    [ -z "$DISPATCH_REF" ] || dispatch_ci "$out/summary.txt"
    log "$(head -1 "$out/summary.txt")"
    [ "$verdict" = PASS ]
}

cmd_install() {
    local plist="$HOME/Library/LaunchAgents/$LABEL.plist" script
    script="$SRC/.github/scripts/nightly_tests.sh"
    mkdir -p "$ROOT/results" "$(dirname "$plist")"
    {
        cat <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Label</key><string>$LABEL</string>
	<key>ProgramArguments</key>
	<array><string>/bin/bash</string><string>$script</string><string>run</string></array>
	<key>EnvironmentVariables</key>
	<dict>
		<key>PATH</key><string>$PATH</string>
		<key>NIGHTLY_CI_ROOT</key><string>$ROOT</string>
EOF
        [ "$REF" = nightly ] || echo "		<key>NIGHTLY_REF</key><string>$REF</string>"
        [ "$DISPATCH_REF" = nightly ] || echo "		<key>NIGHTLY_DISPATCH_REF</key><string>$DISPATCH_REF</string>"
        cat <<EOF
	</dict>
	<key>StartCalendarInterval</key>
	<dict><key>Hour</key><integer>2</integer><key>Minute</key><integer>17</integer></dict>
	<key>ProcessType</key><string>Background</string>
	<key>StandardOutPath</key><string>$ROOT/results/launchd.log</string>
	<key>StandardErrorPath</key><string>$ROOT/results/launchd.log</string>
</dict>
</plist>
EOF
    } >"$plist"
    plutil -lint "$plist" || return 1
    launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null
    launchctl bootstrap "gui/$(id -u)" "$plist" && echo "loaded $plist"
}

# The whole file is parsed before this line runs, and nothing after it is
# read, so the checkout step may rewrite this script mid-run.
case "${1:-run}" in run) cmd_run ;; install) cmd_install ;; *) echo "usage: $0 run|install" >&2; exit 2 ;; esac; exit $?
