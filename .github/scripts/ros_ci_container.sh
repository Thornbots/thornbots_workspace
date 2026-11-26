#!/usr/bin/env bash
# Portable ROS CI inside the ros-ci image: build and test the packages that
# `ros_ci.py select` listed in .ros-ci, against the restored install tree, and
# record the result. Run from the colcon workspace root; ROS_CI_TOOLING holds
# .github/scripts. Design: docs/CI.md#warm-portable-ros-ci
set -eo pipefail  # ROS setup scripts are not nounset-safe

tool="python3 $ROS_CI_TOOLING/.github/scripts/ros_ci.py"
state=.ros-ci
source /opt/ros/jazzy/setup.bash
$tool verify src --plan "$state/plan.json"
mapfile -t build < "$state/build.txt"
mapfile -t need < "$state/need.txt"
mapfile -t test < "$state/test.txt"

if [[ "$(cat "$state/firmware.txt")" == yes && ! -x "$MCB_FIRMWARE_BINARY" ]]; then
    (cd src/firmware/MCBV3/MCB-project &&
        /opt/mcb-tools/bin/scons build-sim robot=sentry profile=release \
            compiler-suffix=-14 -j"$(nproc)")
    test -x "$MCB_FIRMWARE_BINARY"
fi

if ((${#build[@]})); then
    # Clean per-package trees so removed sources cannot survive; ccache keeps it fast.
    for package in "${build[@]}"; do rm -rf "build/$package" "install/$package"; done
    ccache -z
    colcon build --packages-select "${build[@]}" --event-handlers console_direct+ \
        --parallel-workers "$(nproc)" --cmake-args -DBUILD_TESTING=ON \
        -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER_LAUNCHER=ccache \
        -DCMAKE_CXX_COMPILER_LAUNCHER=ccache
    ccache -s
    $tool record --plan "$state/plan.json" --manifest "$state/manifest.json" --built "${build[@]}"
fi
echo built > "$state/result"

if ((${#test[@]})); then
    source install/setup.bash
    colcon test --packages-select "${test[@]}" --event-handlers console_direct+ \
        --return-code-on-test-failure
    colcon test-result --verbose
fi
if ((${#need[@]})); then
    $tool record --plan "$state/plan.json" --manifest "$state/manifest.json" \
        --tested "${need[@]}" --passed
fi
echo passed > "$state/result"
