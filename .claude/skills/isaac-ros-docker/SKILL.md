---
name: isaac-ros-docker
description: Load to launch, attach to, rebuild, or troubleshoot the isaac_ros-dev Isaac ROS Docker container, and before running `docker exec`, `colcon build`, or `ros2 launch`/`run`/`topic` against it, even if the user never says "docker".
---

# Isaac ROS Docker dev container

`reference.md`, next to this file, holds the full reference: `run_dev.sh`'s
flag catalogue, what's wired up inside the container, the manual equivalents
of `dexec.sh`/`kill_launch.sh`, the complete `/workspaces/ros2_ws` clone
list, and the dated postmortems. Read it for details beyond this summary.

> **Never build the image yourself.** No `docker build`, no
> `build_image_layers.sh`/`build_base_image.sh`, and no `run_dev.sh`
> invocation that would trigger a build. The user runs every rebuild.
> When a change needs one, make the edit, then hand them the command and
> stop. Running commands *inside* an already-running container (`dexec.sh`)
> is fine.

## Key facts

- Entry point script: `isaac_ros_common/scripts/run_dev.sh`. Run it from
  `isaac_ros_common/scripts/`.
- Host `isaac_ros-dev/src` is bind-mounted to
  `/workspaces/isaac_ros-dev/src`, so source edits don't need a rebuild,
  only dependency/package changes do. **But only for packages that actually
  resolve to this workspace**; see "Two workspaces" below before trusting
  any edit under `src/`.
- The bind mount is **not** at `/workspaces/isaac_ros-dev`: that's the
  colcon workspace root (`build/`, `install/`, `log/`, `src/`), one level
  up. A hand-built path like `/workspaces/isaac_ros-dev/isaac_ros_common/…`
  silently resolves to nothing instead of erroring; run `ls
  /workspaces/isaac_ros-dev/src` if in doubt.
- Container name: `isaac_ros_dev-<uname -m>-container` (e.g.
  `isaac_ros_dev-x86_64-container`).
- Image key is pinned in `isaac_ros_common/scripts/.isaac_ros_common-config`:
  `CONFIG_IMAGE_KEY=ros2_humble.realsense.thornbots`. This resolves to a
  layered build across `docker/Dockerfile.x86_64` →
  `docker/Dockerfile.ros2_humble` → `docker/Dockerfile.realsense` →
  `docker/Dockerfile.thornbots` (custom top layer with this org's apt
  packages and git-cloned/colcon-built packages).
- **On a fresh/recreated container, run `install-sim.sh` before any `sim`
  launch.** `Dockerfile.thornbots` deliberately skips installing
  `ros-humble-ros-gz` and building `sim`, since real hardware never needs
  gz-sim (see "Two workspaces" below). If skipped, `ros2 launch sim ...`
  fails to find gz-sim plugins/executables, or `sim`'s install dir is
  missing or stale. Fix by running
  `dexec.sh -r -- src/isaac_ros_common/docker/scripts/install-sim.sh` (needs
  root for the apt install; fast, ~5s once apt is done, so it's safe to run
  once per container before the first sim test regardless).

## Two workspaces: `/workspaces/ros2_ws` silently shadows your `src/` edits

**Read this before concluding that a config or source change "had no
effect", and before trusting any measurement taken after editing one.**

There are two colcon workspaces in the container, and they overlap:

| workspace | what's in it | origin |
|---|---|---|
| `/workspaces/ros2_ws` | `sentry_pkg`, `sentry_localization`, `sllidar_ros2`, `rf2o_laser_odometry`, `dji_serial_bridge`, … | **git-cloned from GitHub during the Docker build** (`Dockerfile.thornbots` layers 4–10) |
| `/workspaces/isaac_ros-dev` | `sim`, `sentry_pkg`, `sentry_localization`, … | the **bind-mounted host `src/`** you actually edit |

**Which copy wins depends on the entry point** (re-measured 2026-07-26;
earlier notes here blamed `AMENT_PREFIX_PATH` ordering, which was wrong):

| entry point | what it sources | resolves to |
|---|---|---|
| the user's terminal | `/etc/bash.bashrc`, which ends by sourcing **only** `/workspaces/ros2_ws/install` | the **image-baked GitHub clone** |
| `dexec.sh` | bashrc, then `ros2_ws`, then `isaac_ros-dev` (prepended, so it wins) | **your `src/` edit**, if that package is built locally |

Packages not built into `/workspaces/isaac_ros-dev/install` (e.g.
`sllidar_ros2`) fall through to `ros2_ws` under either entry point.

So the same `ros2 launch` can run *different code* depending on where it's
launched from, and a `dexec.sh` check followed by a launch in the user's
terminal gives a confidently wrong answer. **Always run `ros2 pkg prefix`
through the same entry point you'll launch from:**
```bash
dexec.sh -- ros2 pkg prefix sentry_localization
# /workspaces/ros2_ws/install/...      -> your src/ edit is NOT live
# /workspaces/isaac_ros-dev/install/... -> your src/ edit IS live

# the actual file a node will load (follows symlink-install):
dexec.sh -- bash -lc 'readlink -f $(ros2 pkg prefix sentry_localization)/share/sentry_localization/config/ekf.yaml'
```

This fails silently and looks like a real result, not a mistake. Editing
`src/sentry_localization/config/ekf.yaml` and relaunching from a shell that
resolves to `ros2_ws` produces a stack running the *old* config with no
warning of any kind. On 2026-07-25 this invalidated an entire round of EKF
measurements before anyone noticed: the tell was the filter output matching
an input to 3 decimal places, which real fusion doesn't do.

**To test an edit against the shadowing copy**, push it into `ros2_ws`'s
source tree (root-owned, hence `-r`). This matters when the launch will
come from the user's terminal, which resolves to `ros2_ws`; `dexec.sh`
launches already pick up your `src/` edit and don't need it. Layers build with
`--symlink-install`, so for config/launch/xacro files this takes effect
immediately with no rebuild:
```bash
dexec.sh -r -- bash -lc 'cp /workspaces/isaac_ros-dev/src/sentry_localization/config/ekf.yaml \
    /workspaces/ros2_ws/src/sentry_localization/config/ekf.yaml'
```
This is a **test-only** shim: it lives inside the container and dies with
it. The edit still has to be committed and pushed to the package's own
GitHub repo to survive, since that's where the build clones from.

Packages that exist *only* in `isaac_ros-dev` (notably `sim`, which
`Dockerfile.thornbots` deliberately does not clone; see LAYER 2b and
`install-sim.sh`) have no shadow copy, so `src/` edits to them are live
immediately. That asymmetry is itself confusing: `sim/urdf/*.xacro` edits
apply instantly while `sentry_localization/config/*.yaml` edits appear to
do nothing.

## Common commands

These are commands **for the user to run**: anything that can rebuild is
theirs, not yours.
```bash
cd isaac_ros_common/scripts
./run_dev.sh        # start (rebuilds if needed), or attach another shell
                    # to the already-running container
./run_dev.sh -b     # launch without rebuilding the image
docker stop isaac_ros_dev-x86_64-container   # needed before it will rebuild
```

After editing `docker/Dockerfile.thornbots`, the user re-runs `run_dev.sh`
(after stopping any running container) to rebuild. To bust the cache for
one cloned package only, bump its `ARG RECLONE_*` (see the file's header
comment for the full list, e.g. `RECLONE_BRIDGE` for
`realsense-yolov8-nitros-bridge`).

## When editing `Dockerfile.thornbots`

- Preserve the layer ordering documented in its header comment (slowest/most
  stable first, most volatile last): that's what keeps rebuilds fast.
- New apt packages this project depends on go in LAYER 2 (Isaac ROS apt
  packages) unless they're sim-specific (LAYER 2b) or belong to one of the
  per-package clone/build layers.
- New cloned-and-built org packages get their own `ARG RECLONE_<NAME>` +
  `git clone` + `colcon build --packages-select <pkg>` block, placed after
  any packages they depend on (each layer sources the workspace install
  before building).

## Helper scripts: use these, never hand-rolled `docker exec`

`isaac_ros_common/scripts/dexec.sh` and `kill_launch.sh` already get the
error-prone parts right: full env parity (both workspace installs, plus
`PS1` set *before* sourcing `/etc/bash.bashrc`, which is
interactive-shell-only and silently no-ops without it: that gap hid a real
FastDDS bug for a whole session), `-u admin` so X11/GUI apps work, and
killing a backgrounded launch's whole process group rather than just the
launch PID.

```bash
# One-off command with correct env:
isaac_ros_common/scripts/dexec.sh -- ros2 topic list
isaac_ros_common/scripts/dexec.sh -r -- apt-get install -y ros-humble-foo

# Backgrounded launch (setsid'd, runs as admin so GUIs open; prints the
# log path and the follow-up commands):
isaac_ros_common/scripts/dexec.sh -d -- ros2 launch sim sim.launch.py
# list running launch trees and their PIDs:
isaac_ros_common/scripts/kill_launch.sh -l
# clean shutdown of the whole tree (not pkill/killall, not bare kill -SIGINT):
isaac_ros_common/scripts/kill_launch.sh <ros2-launch-pid>
```

Set `ISAAC_ROS_CONTAINER` to override the container name if needed.

## Before/after running any test or one-off sim launch

**Before** launching anything (a background launch, `run_localization_drift_tests.py`,
`ekf_ground_truth_diag.py`, or an ad hoc probe script), check for a live
session first:
```bash
dexec.sh -- ps aux | grep -E 'ign gazebo|gz sim|slam_toolbox|amcl|map_server|ekf_filter_node|pose_translator|pose_emulator|ros2 launch' | grep -v grep
```
A dead `gz sim` server leaves orphaned bridges that appear in `ros2 topic
list` but never publish; a *live* session (the user's own manual sim/CV
work, or a previous test that didn't clean up) collides on the same
topics/services (duplicate `/pose_emulator`, `/scan`, etc. publishers) and
silently corrupts whatever you're about to measure. No error, just wrong
numbers or empty samples. `run_localization_drift_tests.py`'s own
`check_no_orphans()` does this exact check and only *warns*, it doesn't
block, so don't skip it just because the script ran.

If something is already running, **don't kill it yourself**: it may be
the user's own in-progress work (e.g. a manual CV/rviz session). Ask before
stopping anything you didn't start.

**After** your own test/probe finishes (including when it errors out or
you interrupt it), clean up what *you* started rather than leaving it for
the next run to collide with:
- The official suites (`run_localization_drift_tests.py`,
  `ekf_ground_truth_diag.py`) already do this via `teardown_stack()` in a
  `finally` block, which is why they're safe to Ctrl-C.
- Any ad hoc script you write that calls `run_stack()`/launches its own
  processes must do the same: wrap the body in `try`/`finally` and call
  `teardown_stack(sim_tree, sentry_tree, helper)` (or `kill_launch.sh
  <pid>` for anything launched outside that helper) unconditionally, and
  re-run the `ps aux` check above afterward to confirm nothing's left.

`sim` launches with GUI by default (standing rule in `SESSION_NOTES.md`);
that includes `run_localization_drift_tests.py`, which takes `--headless`
to opt out:
```bash
isaac_ros_common/scripts/dexec.sh -d -- \
  python3 src/sim/test/localization/run_localization_drift_tests.py
```

## Testing a git worktree's changes in docker without merging first

Worktrees created by `EnterWorktree` live *inside* the package directory
(e.g. `sim/.claude/worktrees/<name>/`), which is inside the bind-mounted
tree, so their files are already readable in the container at
`/workspaces/isaac_ros-dev/src/<pkg>/.claude/worktrees/<name>/...` with no
merge. That covers one-off checks (`xacro`, `ign sdf -p`, reading a value).

It does **not** cover `ros2 launch`/`colcon build`, because
`--symlink-install` resolves back to the *main checkout*:
`install/<pkg>/share/.../file` → `build/<pkg>/.../file` →
`src/<pkg>/.../file`.

To launch-test a worktree's version of one file, repoint the middle
(`build/`) symlink, test, then put it back:
```bash
# swap
dexec.sh -- ln -sfn \
  /workspaces/isaac_ros-dev/src/sim/.claude/worktrees/<name>/urdf/sentry.urdf.xacro \
  /workspaces/isaac_ros-dev/build/sim/urdf/sentry.urdf.xacro
# ...launch/test as normal...
# restore (always, merged or not — the worktree may be removed later)
dexec.sh -- ln -sfn \
  /workspaces/isaac_ros-dev/src/sim/urdf/sentry.urdf.xacro \
  /workspaces/isaac_ros-dev/build/sim/urdf/sentry.urdf.xacro
```
Works for any `--symlink-install`ed file (urdf/xacro, world/sdf, rviz
config, `launch/*.py`). It does **not** work for compiled (C++) packages or
`ros2 run`-launched Python nodes (their installed executable is a generated
wrapper). For those, merge into the main branch locally first (no push
needed), then test normally.

## Troubleshooting quick hits

- "not a member of docker group" → `sudo usermod -aG docker $USER && newgrp docker`
- LFS errors → install `git-lfs`, re-clone
- Build succeeds but "no built image found" → `CONFIG_IMAGE_KEY` doesn't
  resolve to real `Dockerfile.<suffix>` files under `isaac_ros_common/docker/`
- GUI app fails with X11/Qt/xcb "could not connect to display" → it ran as
  root, whose `$HOME=/root` has no `.Xauthority`; the cookie is at
  `/home/admin/.Xauthority`. Use `dexec.sh` (already `-u admin`).
- An edit to a config/source file "had no effect" → see "Two workspaces"
  above; check `ros2 pkg prefix <pkg>`.
- `ros2 topic list` shows almost nothing, `echo`/`hz` hang or say "does not
  appear to be published yet", `tf2_echo` says "frame does not exist", or
  rviz's Fixed Frame dropdown is empty → FastDDS discovery via
  `/etc/fastdds/profile.xml` (source: `isaac_ros_common/docker/fastdds_cable.xml`).
  Two causes were found and fixed 2026-07-20: `<useBuiltinTransports>` must
  stay `true`, and no `<initialPeersList>` (an unreachable explicit peer
  breaks local multicast discovery even so). Full writeup in `reference.md`'s
  Troubleshooting section; don't re-blame
  `RMW_FASTRTPS_PUBLICATION_MODE=ASYNCHRONOUS`, which was a red herring.
  Any profile change needs a full rebuild (`./run_dev.sh`, not `-b`) **and**
  `ros2 daemon stop && ros2 daemon start`.
- A topic/TF/rviz problem that looks **unreproducible from a `docker exec`
  session** but always happens in the user's terminal → the session isn't
  loading `FASTRTPS_DEFAULT_PROFILES_FILE` (only `ROS_DOMAIN_ID`), so it
  never picks up the profile the real shell uses. Use `dexec.sh`, which
  sources the full env.

Don't guess at flags. Run `./run_dev.sh --help` or read the script directly
if something here doesn't match observed behavior (it may have changed).
