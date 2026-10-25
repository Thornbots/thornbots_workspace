#!/usr/bin/env bash
# In-container half of nightly_tests.sh (run by dexec.sh in the per-run agent
# container). Mirrors the `package-repo: workspace` job of .github/workflows/
# ros.yml, then runs the sim E2E stages GitHub cannot. Writes /evidence/*.log
# and /evidence/status.tsv (name, PASS|FAIL|SKIP, seconds); always exits 0 so
# the host decides from status.tsv.
set -o pipefail  # no -u: ROS setup.bash reads unset variables

EV=/evidence
WS=/workspaces/isaac_ros-dev
PKGS=(thornbots_pkg sim sentry_localization rf2o_laser_odometry
      ros2_dji_serial_bridge Realsense_ROI_Depth_Rectifier sllidar_ros2)
ELF="$WS/src/firmware/MCBV3/MCB-project/build/sim/scons-release/MCB-project.elf"
TOOLS=/tmp/mcb-tools
SELF="$(cd "$(dirname "$0")" && pwd -P)/$(basename "$0")"
cd "$WS" || exit 0

# stage NAME TIMEOUT_S FUNCTION [ARG]: run the function in a fresh bash under
# timeout (so it can be killed), log to $EV/NAME.log, record the verdict.
stage() {
    local name="$1" limit="$2" t0 rc
    shift 2
    t0=$(date +%s)
    echo "== $name: $*" >"$EV/$name.log"
    timeout "$limit" bash "$SELF" --run "$@" >>"$EV/$name.log" 2>&1
    rc=$?
    printf '%s\t%s\t%s\n' "$name" "$([ $rc -eq 0 ] && echo PASS || echo FAIL)" \
        "$(($(date +%s) - t0))" >>"$EV/status.tsv"
    return $rc
}
skip() { printf '%s\tSKIP\t0\n' "$1" >>"$EV/status.tsv"; }
cleanup_stack() { pkill -9 -f 'gz sim|MCB-project.elf|ros2 launch' 2>/dev/null; sleep 2; true; }

paths=(); for p in "${PKGS[@]}"; do paths+=("src/$p"); done

setup() {
    set -e
    apt-get update
    apt-get install -y gcc-14 g++-14 python3-venv
    python3 -m venv "$TOOLS"
    "$TOOLS/bin/python" -m pip install scons==4.11.1 pyelftools==0.32 Jinja2==3.1.6
    source /opt/ros/jazzy/setup.bash
    rosdep update --rosdistro jazzy
    rosdep install --from-paths "${paths[@]}" --ignore-src --rosdistro jazzy -y
}
firmware() {
    cd "$WS/src/firmware/MCBV3/MCB-project" &&
    "$TOOLS/bin/scons" build-sim robot=sentry profile=release compiler-suffix=-14 -j"$(nproc)" &&
    test -x "$ELF"
}
build() {
    source /opt/ros/jazzy/setup.bash &&
    colcon build --base-paths "${paths[@]}" --event-handlers console_direct+ \
        --parallel-workers 2 --cmake-args -DBUILD_TESTING=ON -DCMAKE_BUILD_TYPE=Release
}
test_all() {
    source /opt/ros/jazzy/setup.bash && source install/setup.bash &&
    export MCB_FIRMWARE_BINARY="$ELF" ROS_LOCALHOST_ONLY=1
    local rc
    colcon test --base-paths "${paths[@]}" --event-handlers console_direct+ --return-code-on-test-failure
    rc=$?
    colcon test-result --verbose >"$EV/colcon-test-result.txt" 2>&1 || rc=1
    cat "$EV/colcon-test-result.txt"
    return $rc
}
e2e() { # stage
    source /opt/ros/jazzy/setup.bash && source install/setup.bash || return 1
    export MCB_FIRMWARE_BINARY="$ELF"
    src/sim/tools/run_suite.sh "$1" backend:=hosted headless:=true foxglove:=false \
        "log_dir:=$EV/e2e-$1"
    local rc=$?
    cp /tmp/sim_suite_"$1"_*.log "$EV/" 2>/dev/null
    return $rc
}

if [ "${1:-}" = --run ]; then shift; "$@"; exit $?; fi
: >"$EV/status.tsv"

if stage setup 1800 setup; then
    if stage firmware 3600 firmware; then fw=1; else fw=0; fi
    if stage build 5400 build; then
        stage test 3600 test_all
        cp -r log "$EV/colcon-log" 2>/dev/null
        if [ $fw -eq 1 ]; then
            for s in mcb_parked mcb_drive; do
                stage "e2e_$s" 3600 e2e "$s"
                cleanup_stack
            done
        else
            skip e2e_mcb_parked; skip e2e_mcb_drive
        fi
    else
        skip test; skip e2e_mcb_parked; skip e2e_mcb_drive
    fi
else
    for s in firmware build test e2e_mcb_parked e2e_mcb_drive; do skip "$s"; done
fi
exit 0
