---
name: isaac-ros-docker
description: Use when the user wants to launch, attach to, rebuild, or troubleshoot the Isaac ROS dev Docker container for this workspace (isaac_ros-dev) — e.g. "start the container", "rebuild the image", "attach a shell", "docker won't build", "add a package to the image".
---

# Isaac ROS Docker dev container

Full reference: `../../../DOCKER.md` (repo-relative: `src/DOCKER.md`). Read it
if you need details beyond this summary.

> **Never build the image yourself.** No `docker build`, no
> `build_image_layers.sh`/`build_base_image.sh`, and no `run_dev.sh`
> invocation that would trigger a build — the user runs every rebuild.
> When a change needs one, make the edit, then hand them the command and
> stop. Running commands *inside* an already-running container (`dexec.sh`)
> is fine.

## Key facts

- Entry point script: `isaac_ros_common/scripts/run_dev.sh`. Run it from
  `isaac_ros_common/scripts/`.
- Host `isaac_ros-dev/src` is bind-mounted to
  `/workspaces/isaac_ros-dev/src` — source edits don't need a rebuild, only
  dependency/package changes do. **But only for packages that actually
  resolve to this workspace**; see "Two workspaces" below before trusting
  any edit under `src/`.
- The bind mount is **not** at `/workspaces/isaac_ros-dev` — that's the
  colcon workspace root (`build/`, `install/`, `log/`, `src/`), one level
  up. A hand-built path like `/workspaces/isaac_ros-dev/isaac_ros_common/…`
  silently resolves to nothing instead of erroring; `ls
  /workspaces/isaac_ros-dev/src` if in doubt.
- Container name: `isaac_ros_dev-<uname -m>-container` (e.g.
  `isaac_ros_dev-x86_64-container`).
- Image key is pinned in `isaac_ros_common/scripts/.isaac_ros_common-config`:
  `CONFIG_IMAGE_KEY=ros2_humble.realsense.thornbots`. This resolves to a
  layered build across `docker/Dockerfile.x86_64` →
  `docker/Dockerfile.ros2_humble` → `docker/Dockerfile.realsense` →
  `docker/Dockerfile.thornbots` (custom top layer with this org's apt
  packages and git-cloned/colcon-built packages).

## Two workspaces: `/workspaces/ros2_ws` silently shadows your `src/` edits

**Read this before concluding that a config or source change "had no
effect", and before trusting any measurement taken after editing one.**

There are two colcon workspaces in the container, and they overlap:

| workspace | what's in it | origin |
|---|---|---|
| `/workspaces/ros2_ws` | `sentry_pkg`, `sentry_localization`, `sllidar_ros2`, `rf2o_laser_odometry`, `dji_serial_bridge`, … | **git-cloned from GitHub during the Docker build** (`Dockerfile.thornbots` layers 4–10) |
| `/workspaces/isaac_ros-dev` | `sim`, `sentry_pkg`, `sentry_localization`, … | the **bind-mounted host `src/`** you actually edit |

**Which copy wins depends on the entry point** (re-measured 2026-07-26 —
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
measurements before it was noticed — the tell was the filter output
matching an input to 3 decimal places, which is not something real fusion
does.

**To test an edit against the shadowing copy**, push it into `ros2_ws`'s
source tree (root-owned, hence `-r`). Layers build with
`--symlink-install`, so for config/launch/xacro files this takes effect
immediately with no rebuild:
```bash
dexec.sh -r -- bash -lc 'cp /workspaces/isaac_ros-dev/src/sentry_localization/config/ekf.yaml \
    /workspaces/ros2_ws/src/sentry_localization/config/ekf.yaml'
```
This is a **test-only** shim — it lives inside the container and dies with
it. The edit still has to be committed and pushed to the package's own
GitHub repo to survive, since that's where the build clones from.

Packages that exist *only* in `isaac_ros-dev` (notably `sim`, which
`Dockerfile.thornbots` deliberately does not clone — see LAYER 2b and
`install-sim.sh`) have no shadow copy, so `src/` edits to them are live
immediately. That asymmetry is itself confusing: `sim/urdf/*.xacro` edits
apply instantly while `sentry_localization/config/*.yaml` edits appear to
do nothing.

## Common commands

These are commands **for the user to run** — anything that can rebuild is
theirs, not yours:
```bash
cd isaac_ros_common/scripts
./run_dev.sh        # start (rebuilds if needed), or attach another shell
                    # to the already-running container
./run_dev.sh -b     # launch without rebuilding the image
docker stop isaac_ros_dev-x86_64-container   # needed before it will rebuild
```

Rebuild after editing `docker/Dockerfile.thornbots` — the user re-runs
`run_dev.sh` (after stopping any running container). To bust the cache for
one cloned package only, bump its `ARG RECLONE_*` (see the file's header
comment for the full list, e.g. `RECLONE_BRIDGE` for
`realsense-yolov8-nitros-bridge`).

## When editing `Dockerfile.thornbots`

- Preserve the layer ordering documented in its header comment (slowest/most
  stable first, most volatile last) — that's what keeps rebuilds fast.
- New apt packages this project depends on go in LAYER 2 (Isaac ROS apt
  packages) unless they're sim-specific (LAYER 2b) or belong to one of the
  per-package clone/build layers.
- New cloned-and-built org packages get their own `ARG RECLONE_<NAME>` +
  `git clone` + `colcon build --packages-select <pkg>` block, placed after
  any packages they depend on (each layer sources the workspace install
  before building).

## Helper scripts — use these, never hand-rolled `docker exec`

`isaac_ros_common/scripts/dexec.sh` and `kill_launch.sh` already get the
error-prone parts right: full env parity (both workspace installs, plus
`PS1` set *before* sourcing `/etc/bash.bashrc`, which is
interactive-shell-only and silently no-ops without it — that gap hid a real
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

Before backgrounding a new launch, check for and clean up stale processes
(`dexec.sh -- ps aux | grep -E 'ros2|gz|ign|parameter_bridge'`) — a dead
`gz sim` server leaves orphaned bridges that appear in `ros2 topic list`
but never publish, and relaunching on top of a live session gives duplicate
sim instances.

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
tree — so their files are already readable in the container at
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
wrapper) — for those, merge into the main branch locally first (no push
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
  breaks local multicast discovery even so). Full writeup in DOCKER.md's
  Troubleshooting section; don't re-blame
  `RMW_FASTRTPS_PUBLICATION_MODE=ASYNCHRONOUS`, which was a red herring.
  Any profile change needs a full rebuild (`./run_dev.sh`, not `-b`) **and**
  `ros2 daemon stop && ros2 daemon start`.
- A topic/TF/rviz problem that looks **unreproducible from a `docker exec`
  session** but always happens in the user's terminal → the session isn't
  loading `FASTRTPS_DEFAULT_PROFILES_FILE` (only `ROS_DOMAIN_ID`), so it
  never picks up the profile the real shell uses. Use `dexec.sh`, which
  sources the full env.

Don't guess at flags — run `./run_dev.sh --help` or read the script directly
if something here doesn't match observed behavior (it may have changed).
