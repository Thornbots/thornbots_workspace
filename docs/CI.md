# CI and robot images

Every package repo and this workspace run GitHub quality checks on pushes
and PRs outside frozen Humble branches. Package workflows pin shared tooling
to an immutable workspace commit. Update the reusable workflow reference and
its input refs together when changing the tooling.

| Repositories | Automatic validation |
| --- | --- |
| All twelve | Ruff, ShellCheck, targeted C++ lint, XML/YAML parse, actionlint; seven checker regression tests |
| Workspace and seven portable ROS repos | Ubuntu 24.04/Jazzy build and registered colcon tests; logs and install artifact |
| MCBV3 | ARM builds for infantry/hero/sentry; 29 C++ unit tests and 11 compiled UART/control tests; firmware artifacts |
| isaac-ros-startup | Three log handling tests |
| isaac_ros_common | Four subprocess tests and seven robot-image pull tests |
| Workspace | Native arm64 robot-image build and package tests |

The portable ROS repos are thornbots_pkg, sim, sentry_localization,
rf2o_laser_odometry, ros2_dji_serial_bridge, Realsense_ROI_Depth_Rectifier,
and sllidar_ros2. CI explicitly initializes opt-in sim. The MCB fixture is
pinned to a compatible sim revision; missing firmware or skipped UART tests
fail its job. No CI job flashes firmware or deploys to a robot.

## Lint debt

The lint gate checks tracked first-party files. Vendored Taproot/modm/SDK,
build/install/log artifacts, symlinks, and nested gitlinks are excluded.
Ruff checks correctness (`E9,F`, except star-import diagnostics), ShellCheck
checks errors, and cpplint checks integer/printf/memset/constructor/string/cast
pitfalls. Registered ament lint runs in the Jazzy tier too.

`.github/quality-baseline.json` records current debt by file, rule, message,
and count. Existing findings pass; new findings or increased counts fail.
Syntax and document parse errors always fail, including when baselined.
Review changes to the baseline as code; do not regenerate it to hide failures.

The remaining debt includes C-style casts and implicit constructors in MCB,
upstream driver conventions in rf2o/sllidar, and unused imports in sim. This
change fixed invalid XML comments, uninitialized MCB history buffers,
obsolete firmware tests, and an EOF logging race instead of accepting them
as baseline debt.

## Validation boundaries

The isolated existing Jazzy container passed 69 thornbots Python cases,
22 tracker C++ cases, nine localization cases, 57 sim Python cases and eight
sim C++ cases, four rf2o cases, and three ROI cases. MCB additionally passed
all 29 C++ and 11 hosted UART tests, plus all three ARM release builds with
the supported GCC 10 toolchain. Common and startup unit tests passed on
GitHub as well. Integration simulation suites were excluded.

These checks do not validate physical motor dynamics, STM32 timing, camera
capture, or GPU inference. Legacy oldinfantry builds are excluded because
their calibration constants are absent. GPIO/CUDA-dependent Isaac upstream
builds and the YOLO bridge have a manual workspace `ROS Jazzy` workflow,
using a provisioned `isaac-ros-jazzy` self-hosted runner and the
`isaac-ros-ci` environment. Set `ISAAC_ROS_CI_UNDERLAY` there to an Isaac ROS
4.6 install directory containing `setup.bash`.

## Robot registry

`publish robot image` builds the existing Isaac ROS CLI layer chain natively
on GitHub's arm64 runner and tests packages before publishing. Pushes to
main/nightly publish `ghcr.io/thornbots/isaac-ros:<branch>-arm64-jetpack` and
`sha-<full workspace SHA>-arm64-jetpack`. PR/feature builds test without
publishing. A manual dispatch can publish its selected revision. Simulation
images are not published.

Package source changes reach the image after updating their workspace
gitlinks. A failed build keeps the preceding branch tag. The first image
becomes available only after a successful publishing run. The package starts
private; a package administrator can make it public for anonymous pulls or
grant read access. The source label links package permissions to this repo.
See [GitHub package access documentation](https://docs.github.com/en/packages/learn-github-packages/configuring-a-packages-access-control-and-visibility).

The robot's pull helper selects its exact workspace SHA, verifies clean
tracked image sources and matching mandatory gitlinks, and retags the image
for isaac-ros-cli. It does not build or start a container. Usage is in
[the image README](../isaac_ros_common/docker/README.md).

## Branch protection

The policy requires passing named CI checks and an up-to-date branch, blocks
force pushes/deletion, applies to administrators, and requires zero reviews.
It permits tested fast-forward pushes so the existing coordinated submodule
promotion workflow still works. It does not enforce linear history.

Applied and verified: workspace/main, thornbots_pkg/main, sim/main,
sentry_localization/main, rf2o_laser_odometry/main. The latter now uses main
as its default branch instead of ros2.
This account has write-only access to the other seven repos; protection
updates returned HTTP 404. Their protections are intentionally left unchanged
as requested. The script skips repositories without admin access.
For MCBV3 it targets **only main**, never newMain, nightly, or another branch.

The initial policy has no pre-existing settings to preserve. If adapting it
after other settings are added, review the generated payload before applying.
