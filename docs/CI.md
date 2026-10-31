# CI and robot images

`nightly` integrates package changes; `main` receives promoted releases.
Only `main` builds an image and runs the full CI: workspace and package CI run
on pushes to `main`, on PRs into `main` and on manual dispatch. `nightly` runs
no CI on pushes or PRs; authors run the
[local checks](#local-checks-for-prs-into-nightly) before merging, and the
[nightly tests](#nightly-tests) run on the Mac mini each night. All eleven `.gitmodules` entries track `nightly`
on this integration branch, with exact gitlink pins. Sim and MCB firmware are
initialized by normal submodule checkout; firmware can be skipped.

| Repositories | Automatic validation |
| --- | --- |
| Workspace and packages | Ruff, ShellCheck, targeted C++ lint, XML/YAML parsing, actionlint; [checker tests](../.github/quality/test_check.py) |
| Workspace and seven portable ROS packages | Ubuntu 24.04/Jazzy build and registered colcon tests; logs and install artifact |
| Workspace and isaac-ros-startup | Native CMake/CTest [log and CUDA-probe tests](../isaac-ros-startup/tests), with an error on empty discovery |
| Workspace and isaac_ros_common | [Subprocess](../isaac_ros_common/isaac_common_py/tests) and [robot-image helper](../isaac_ros_common/tests) tests |
| Workspace | Native arm64 robot-image build and package tests |
| Workspace, covering bumped package commits | [Repository policy](#repository-policy) and its [regression tests](../.github/quality/test_policy.py) |
| MCBV3 | ARM builds in all robot/sysid combinations and hosted control/UART tests on `main` pushes and PRs into `main` |

Portable packages are thornbots_pkg, sim, sentry_localization,
rf2o_laser_odometry, ros2_dji_serial_bridge, Realsense_ROI_Depth_Rectifier,
and sllidar_ros2. Package workflows pin reusable tooling to existing immutable
workspace commits retained by `ci-tooling-884bfe6` and `ci-ros-58b7bf0` tags.
Their `workspace-ref` independently pins the integrated dependency workspace.
Refresh this immutable dependency pin across all seven portable package
workflows when integrated interfaces change. Updating workspace nightly alone
does not move package CI's dependency checkout. Keep the reusable tooling pins
unchanged unless the tooling itself changes.
Startup pins the native host-test tooling introduced by the C++ CI repair.
When updating reusable tooling, move workflow references and their
`tooling-ref` inputs together; dependency pins must continue to describe
nightly. The workspace uses its own tested revision.
Host helper jobs use the workspace's exact package pins and archive their JUnit
reports. Package quality workflows use the same
[host test runner](../.github/scripts/test_host_packages.sh).

## Local checks for PRs into nightly

Before merging into `nightly`, in each changed repo (workspace included):

- Python 3.12 venv with `.github/quality/requirements.txt`: `python
  .github/quality/check.py` and `actionlint -shellcheck=""`; checker changes
  also need `python -m unittest discover -s .github/quality -v`.
- ROS packages: `colcon build` and `colcon test --packages-select <pkg>` in
  your own agent container (`isaac_ros_common/scripts/agent_container.sh`,
  see the [Docker skill](../.claude/skills/isaac-ros-docker/SKILL.md)).
- MCBV3 firmware: run the GCC 14 unit tests, hosted firmware build and hosted
  UART/control tests in its [Continuous integration](../firmware/MCBV3/README.md#continuous-integration)
  section. ARM builds run on `main` pushes/PRs or dispatch.
- Optional GitHub run on a pushed branch:
  `gh workflow run CI -R Thornbots/<repo> --ref <branch>`.

Push-time [policy hooks](#repository-policy) still check commits and gitlinks.

## Nightly tests

[nightly_tests.sh](../.github/scripts/nightly_tests.sh) runs on the Mac mini
(`blaises-mini`) at 02:17 local from a launchd LaunchAgent
(`~/Library/LaunchAgents/com.thornbots.nightly-ci.plist`, written and loaded by
`nightly_tests.sh install`). It lives here, not in a package, because it tests
the workspace's pins and drives `agent_container.sh`.

- It updates `~/ros2_ws/nightly-ci/src` to `origin/nightly` (public https, the
  portable packages, `isaac_ros_common` and MCBV3) and starts one
  [agent container](../.claude/skills/isaac-ros-docker/SKILL.md#your-own-container)
  for the run; its container is removed afterwards. Colima stops only when
  no containers are running.
- [Inside it](../.github/scripts/nightly_tests_inside.sh): the hosted sentry
  firmware build and `colcon build`/`colcon test` as in the `package-repo:
  workspace` job of [ros.yml](../.github/workflows/ros.yml), then the sim
  Gazebo E2E stages GitHub cannot run, `mcb_parked` and `mcb_drive` with
  `backend:=hosted`, headless, one at a time.
- It skips, logging why, when another container on the mini runs a sim stack.
- Results: `~/ros2_ws/nightly-ci/results/<date>/` holds per-stage logs,
  `colcon-test-result.txt`, E2E logs, `shas.txt` and `summary.txt` (first line
  PASS/FAIL/SKIP per stage plus workspace and package SHAs); the newest 14 are
  kept and `results/launchd.log` has the job's own output. The exit status is
  the local result including publication.
- A PASS requires a zero runner exit and exactly one ordered record for each
  of setup, firmware, build, test and the two E2E stages. Invalid outcomes,
  malformed durations, missing/extra/duplicate records and impossible SKIPs
  fail the run. Setup/build/firmware failures retain their dependency SKIPs;
  those completed failure reports still return FAIL.
- After a local PASS, [nightly_publish.sh](../.github/scripts/nightly_publish.sh)
  makes a temporary nested checkout to isolate the CLI configuration paths,
  initializes every image gitlink (including recursive children, excluding sim
  and firmware), pulls the registry's shared
  [base layers](#robot-registry), builds the JetPack image on the host with
  `build_robot_image.sh`, then runs the registry workflow's `colcon test` and
  `colcon test-result --verbose` gate in its own agent container. It pushes the
  immutable SHA tag before updating the nightly tag. Colima starts if needed;
  cleanup uses `agent_container.sh` and leaves other running containers alone.
- `summary.txt` records `publish=PASS|FAIL|SKIP`; publication stays outside the
  six-stage `status.tsv` contract. Build, image-test or push failure fails the
  run. `NIGHTLY_PUBLISH=0` disables publication (default on); `install` persists
  only a non-default value. For build/test validation without any registry
  writes, run the publish helper with `NIGHTLY_PUBLISH_PUSH=0`.
- Publishing relies on the mini's existing Docker login. Authentication failure
  adds a `docker login ghcr.io` hint requiring a `write:packages` token to
  `summary.txt` and `run.log`; the job never provisions credentials. After both
  pushes succeed it removes older local `sha-*-arm64-jetpack` registry tags,
  retaining the new tag and base images, then removes dangling images (local
  bases replaced by registry copies). Before and after publication it prunes
  unused build cache toward a 12 GB retention target.
- After the local run it dispatches GitHub `CI` on `nightly` in every repo with
  that workflow (and MCBV3's `firmware.yml`) using the mini's `gh`, appends the
  run URLs to `summary.txt` and does not wait for them.

Build an image from `nightly` on demand, for example before a robot session:
`gh workflow run "publish robot image" -R Thornbots/thornbots_workspace --ref nightly`.
Run the job by hand with `launchctl kickstart gui/$(id -u)/com.thornbots.nightly-ci`.

## Coordinated package integration

Push package feature branches first, then a workspace feature branch that
bumps their gitlinks. Open draft PRs into `nightly` for review. Merge package
PRs first, then update the workspace gitlinks to the resulting package commits
and merge the workspace PR. Workspace CI validates the pinned commits;
workspace merges do not push or merge package branches.

## Repository policy

[policy.py](../.github/quality/policy.py) checks every commit new to a range,
in the workspace and in package ranges its changed gitlinks newly cover:

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
files plus pushed ranges and their `.msg` files (merges and rebases skip
pre-commit). Commit signing is optional; neither hooks nor CI check it.

Limits: hooks are bypassable with `--no-verify` and absent while the
workspace checks out a branch without `.githooks`. Pushes to an unnamed URL
check everything outside reviewed history. Package CI does not run the
policy (pinned tooling); package commits are checked when the workspace bumps
them, after they are pushed to GitHub. The `policy` check is required only once [branch protection](#branch-protection)
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
Workspace ROS CI builds its pinned hosted sentry firmware with GCC 14 before
running sim's native UART and ROS-bridge tests, and fails if the build does not
produce an executable. Package-only ROS jobs omit the optional firmware and may
skip those firmware-dependent cases.
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

The Mac mini publishes `ghcr.io/thornbots/isaac-ros:nightly-arm64-jetpack`
plus `sha-<full workspace SHA>-arm64-jetpack` from `origin/nightly` after its
nightly tests pass; see [Nightly tests](#nightly-tests). It builds the existing
Isaac ROS CLI JetPack layer chain natively under Colima and tests the built
packages before pushing.

The GitHub `publish robot image` workflow remains available for release and
manual builds on GitHub's arm64 runner. Pushes to
`main` publish `ghcr.io/thornbots/isaac-ros:main-arm64-jetpack`
and `sha-<full workspace SHA>-arm64-jetpack`. PRs into `main` build and test
without publishing robot tags. Manual dispatch can publish its selected branch revision (for
example `nightly`), with slashes replaced by dashes; see [Nightly tests](#nightly-tests). Simulation images are not published.

Base layers are cached as `isaac-ros:base-<layer>_<hash>-arm64-jetpack`, with
the hash covering Dockerfiles and build arguments. Cached layers let a run
build only the thornbots layer. The mini and the workflow build on the same
cached bases, so a robot pulls only the layers above them; independently built
bases share no layers. Same-repository PRs can populate base caches;
fork PRs only pull. The workflow publishes missing bases before package tests;
the mini publishes them only after its tests pass, and never replaces one that
exists. On the mini's Docker containerd image store, the publish helper also
fetches each pulled base's digest with Colima's `ctr -n moby content fetch`.
This direct content-store operation fills compressed blobs that Docker may skip
when reusing snapshots; otherwise export can try the CLI's nvcr alias for blobs
that exist only on ghcr. It requires the shared bases to be publicly readable
from the VM and fails before building if that fetch fails.

Source changes reach the image through workspace gitlinks. Failed builds
retain the preceding branch tag. Registry packages initially need an
administrator to make them public or grant read access. Private pulls require
a Docker login with `read:packages`; GitHub workflow publication uses its
`GITHUB_TOKEN` with `packages: write`. The pull helper
selects its exact workspace SHA, verifies clean tracked image sources and
matching mandatory gitlinks, and retags the image for isaac-ros-cli. Usage:
[image README](../isaac_ros_common/docker/README.md).

## Branch protection

`configure_branch_protection.py` prints an opt-in policy requiring named CI
checks and an up-to-date branch, blocking force pushes/deletion, applying to
administrators, and requiring zero reviews. It leaves linear history optional
so coordinated merges remain possible. `--branch nightly` selects integration
protection, requiring checks that PRs into `nightly` no longer run, so do not
apply it there; the default is `main`. MCBV3 is skipped for nightly because its
policy targets only main.

Without `--apply` it changes no GitHub settings. `--apply` replaces the
policy and requires repo admin access; review the printed payload and existing
settings before using it. Repos where the account lacks admin access are
skipped.
