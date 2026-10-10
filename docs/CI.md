# CI and robot images

`nightly` integrates package changes; `main` receives promoted releases.
Workspace and package CI run on PRs targeting either branch and on pushes to
either branch. Feature branches are validated through their PRs; manual
dispatch remains available. All eleven `.gitmodules` entries track `nightly`
on this integration branch, with exact gitlink pins. Sim is initialized by
normal submodule checkout; only MCB firmware remains opt-in.

| Repositories | Automatic validation |
| --- | --- |
| Workspace and packages | Ruff, ShellCheck, targeted C++ lint, XML/YAML parsing, actionlint; [checker tests](../.github/quality/test_check.py) |
| Workspace and seven portable ROS packages | Ubuntu 24.04/Jazzy build and registered colcon tests; logs and install artifact |
| isaac-ros-startup | [Log handling tests](../isaac-ros-startup/tests) |
| isaac_ros_common | [Subprocess](../isaac_ros_common/isaac_common_py/tests) and [robot-image helper](../isaac_ros_common/tests) tests |
| Workspace | Native arm64 robot-image build and package tests |
| Workspace, covering bumped package commits | [Repository policy](#repository-policy) and its [regression tests](../.github/quality/test_policy.py) |
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
bumps their gitlinks. Open draft PRs into `nightly` for review. Merge package
PRs first, then update the workspace gitlinks to the resulting package commits
and merge the workspace PR. Workspace CI validates the pinned commits;
workspace merges do not push or merge package branches.

## Repository policy

[policy.py](../.github/quality/policy.py) checks every commit new to a range,
in the workspace and in package ranges its changed gitlinks newly cover:

- Signed by its committer, using each contributor's existing Git identity and
  GitHub-registered key; nothing compares against a fixed name, email or
  repository key. Workspace CI asks GitHub's commits API about the exact
  repository and SHA and requires `verified` (key on the committer's account,
  verified account email). GitHub-signed web merges pass; unsigned commits
  claiming GitHub as committer do not. Hooks require a good local signature
  whose SSH principal or GPG UID email is the committer email. Commits Git
  cannot verify locally pass only if already on a remote and verified by GitHub.
- Gitlinks fast-forward from every parent's pin, so stale checkouts cannot
  rewind another change's bump. A new gitlink needs a reviewed history line.
- First-party top-level `.msg` files declare `std_msgs/Header header`, and a
  comment mentions `stamp`. Vendored and NVIDIA `isaac_ros_*_interfaces` are
  excluded. This is structural; runtime tests prove which stamp is carried.

Ranges are PR base to head and push `before` to `after`; new branches,
manual runs and unreachable `before` check everything not on `origin/main`
or `origin/nightly`. Pre-push checks commits absent from that remote.
History reachable from [reviewed_history](../.github/quality/reviewed_history)
is skipped. Lines are read from the base; a change may only add lines for
gitlinks the base does not pin. To import new upstream history into an
existing package, first land a policy-only change adding its reviewed line,
then the bump.

CI runs `policy.py` from the base revision (PR base, push `before`, else the
target protected branch) against the revision under test, so a change cannot
weaken the checker that judges it; workflow edits still need review. The
bootstrap change has no base checker or `reviewed_history`: it runs its own
checker, logs a warning, and trusts its initial roots. Those roots were
checked to equal the `origin/main` and `origin/nightly` tips and nightly's
package pins at introduction.

`python3 scripts/install_policy_hooks.py --recursive`
([installer](../scripts/install_policy_hooks.py)) sets local `core.hooksPath`
in the workspace and package checkouts, plus workspace
`push.recurseSubmodules=check`. It refuses to replace other hooks paths or
unmanaged hooks and leaves global config alone. Hooks check staged `.msg`
files, `commit.gpgsign`, and pushed ranges and their `.msg` files (merges and
rebases skip pre-commit).

Limits: hooks are bypassable with `--no-verify` and absent while the
workspace checks out a branch without `.githooks`. Pushes to an unnamed URL
check everything outside reviewed history. Package CI does not run the
policy (pinned tooling); package commits are checked when the workspace bumps
them, after they are pushed to GitHub. Unsigned contributions need re-signing
or a signed squash; GitHub rebase-merge results must pass the same check. The
`policy` check is required only once [branch protection](#branch-protection)
is applied.

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
administrators, and requiring zero reviews. It leaves linear history optional
so coordinated merges remain possible. `--branch nightly` selects integration
protection; the default is `main`. MCBV3 is skipped for nightly because its
policy targets only main.

This port does not apply or change GitHub protection settings. `--apply`
replaces the policy and requires repo admin access; review the printed payload
and existing settings before using it. Accounts without admin access are
skipped.
