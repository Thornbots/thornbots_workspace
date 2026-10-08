# CI and robot images

`nightly` integrates package changes; `main` receives promoted releases.
Workspace and package CI run on PRs targeting either branch and on pushes to
either branch. Feature branches are validated through their PRs; manual
dispatch remains available. All eleven `.gitmodules` entries track `nightly`
on this integration branch, with exact gitlink pins. Sim is initialized by
normal submodule checkout; only MCB firmware remains opt-in.

| Repositories | Automatic validation |
| --- | --- |
| Workspace and packages | Ruff, ShellCheck, targeted C++ lint, XML/YAML parsing, actionlint; seven checker regression tests |
| Workspace and seven portable ROS packages | Ubuntu 24.04/Jazzy build and registered colcon tests; logs and install artifact |
| isaac-ros-startup | Three log handling tests |
| isaac_ros_common | Four subprocess tests and eight robot-image helper tests |
| Workspace | Native arm64 robot-image build and package tests |
| MCBV3 (existing nightly CI) | ARM builds and hosted control/UART tests; unchanged by this port |

Portable packages are thornbots_pkg, sim, sentry_localization,
rf2o_laser_odometry, ros2_dji_serial_bridge, Realsense_ROI_Depth_Rectifier,
and sllidar_ros2. Package workflows pin reusable tooling to existing immutable
workspace commits retained by `ci-tooling-884bfe6` and `ci-ros-58b7bf0` tags.
Their `workspace-ref` independently pins the integrated dependency workspace.
Update workflow references and their tooling inputs together; dependency pins
must continue to describe nightly. The workspace uses its own tested revision.

## Coordinated package integration

Push package feature branches first, then a workspace feature branch that
bumps their gitlinks. Open draft PRs into `nightly` for review. The workspace's
`advance` job checks each gitlink against its `.gitmodules` branch. A gitlink
equal to or behind that branch is accepted; one ahead must be a fast-forward;
a divergent gitlink fails and needs rebasing onto the latest package nightly.

After a workspace merge into `nightly` or `main`, `advance-submodules.yml`
pushes those fast-forwards to the configured package branches. It does not
merge package PRs or rewrite history. Its manual dispatch does the same push.
`SUBMODULES_TOKEN` needs contents read/write on every affected package repo;
the workflow's ordinary `GITHUB_TOKEN` cannot write across repositories.
PR checks do not use that secret. A missing or unauthorized token prevents
post-merge advancement even if the ancestry check passes. The push loop can
advance earlier packages before a later push fails; fix access and rerun.
Gitlinks behind a moved branch are accepted and never rewind it.

## Lint debt

The quality gate checks tracked first-party files, excluding vendored
Taproot/modm/SDK, build/install/log artifacts, symlinks and nested gitlinks.
Ruff checks correctness (`E9,F`, except star-import diagnostics), ShellCheck
checks errors, and cpplint checks selected integer/printf/memset/constructor/
string/cast pitfalls. Registered ament lint runs in the Jazzy tier too.

`.github/quality-baseline.json` records reviewed debt by file, rule, message
and count. Existing findings pass; new or increased findings fail. Syntax and
document parse errors always fail, even if baselined. Do not grow the baseline
to hide regressions. Existing driver debt includes C-style casts and `sprintf`;
these are departures from standard C++ practice, not endorsed conventions.

## Validation boundaries

ROS CI runs registered unit tests; sim's integration suites remain excluded.
The fixture uses the current Taproot UART bit layout only, with no legacy
schema switch. Missing firmware cannot establish native firmware coverage.
No job flashes firmware or deploys to a robot. These checks do not validate
physical motor dynamics, STM32 timing, camera capture or GPU inference.

GPU/CUDA-dependent upstream Isaac packages and the YOLO bridge use the manual
workspace `ROS Jazzy` workflow with a provisioned `isaac-ros-jazzy` runner and
`isaac-ros-ci` environment. Set `ISAAC_ROS_CI_UNDERLAY` there to an Isaac ROS
4.6 install directory containing `setup.bash`. Local results and exact test
counts belong in commit messages; old PR results do not validate new pins.

## Robot registry

`publish robot image` builds the existing Isaac ROS CLI layer chain natively
on GitHub's arm64 runner and tests packages before publishing. Pushes to
`nightly` and `main` publish `ghcr.io/thornbots/isaac-ros:<branch>-arm64-jetpack`
and `sha-<full workspace SHA>-arm64-jetpack`. PR builds test without publishing
robot tags. Manual dispatch can publish its selected branch revision, with
slashes replaced by dashes. Simulation images are not published.

Base layers are cached as `isaac-ros:base-<layer>_<hash>-arm64-jetpack`, with
the hash covering Dockerfiles and build arguments. Cached layers let a run
build only the thornbots layer. Same-repository PRs can populate base caches;
fork PRs only pull. Robot-image publication waits for package tests; cache
publication occurs after building base layers and before package tests.

Source changes reach the image through workspace gitlinks. Failed builds
retain the preceding branch tag. Registry packages initially need an
administrator to make them public or grant read access. The pull helper
selects its exact workspace SHA, verifies clean tracked image sources and
matching mandatory gitlinks, and retags the image for isaac-ros-cli. Usage:
[image README](../isaac_ros_common/docker/README.md).

## Branch protection

`configure_branch_protection.py` prints an opt-in policy requiring named CI
checks and an up-to-date branch, blocking force pushes/deletion, applying to
administrators, and requiring zero reviews. Workspace policy includes
`advance`. It leaves linear history optional so coordinated merges remain
possible. `--branch nightly` selects integration protection; the default is
`main`. MCBV3 is skipped for nightly because its policy targets only main.

This port does not apply or change GitHub protection settings. `--apply`
replaces the policy and requires repo admin access; review the printed payload
and existing settings before using it. Accounts without admin access are
skipped. Package protection must permit the configured token to perform
tested fast-forwards; whether existing required checks allow that remains an
administrative verification, separate from PR ancestry checks.
