# Docker dev container

This workspace runs inside a Docker dev container built from
`isaac_ros_common`'s scripts and layered Dockerfiles. Source code on the host
(this `src/` directory and its parent `isaac_ros-dev/`) is bind-mounted into
the container at `/workspaces/isaac_ros-dev`, so edits made outside the
container are immediately visible inside it (and vice versa) — you rebuild
the image only when dependencies (apt packages, cloned repos in
`Dockerfile.thornbots`) change, not for ordinary source edits.

## Quick start

```bash
cd isaac_ros_common/scripts
./run_dev.sh
```

- First run builds the image (can take a while), then launches a container
  named `isaac_ros_dev-<arch>-container` and drops you into a bash shell as
  the `admin` user, workdir `/workspaces/isaac_ros-dev`.
- Re-running `run_dev.sh` while the container is already running just attaches
  another shell to it instead of starting a second container.
- The container is started with `docker run -it --rm`, so it is **not** left
  running in the background — `Ctrl-D` / `exit` on the *first* shell (the one
  that ran `run_dev.sh` and launched the container, i.e. the one running
  `workspace-entrypoint.sh` as PID 1) stops the container and Docker
  auto-removes it. `docker exec`-attached second/third shells (see "Common
  tasks" below) can exit freely without affecting the container — only
  exiting the original launching shell tears it down. The next `run_dev.sh`
  invocation after that starts a fresh container (and rebuilds the image
  unless `-b`/`SKIP_DOCKER_BUILD` is used).

## Which image gets built

`run_dev.sh` builds an image for `IMAGE_KEY` (default `ros2_humble`) on
platform `$(uname -m)` (`x86_64` here). The key is dot-composite: e.g.
`x86_64.ros2_humble.realsense.thornbots` resolves, right-to-left, against
`docker/Dockerfile.<suffix>` files, each layer using the previous as its
`BASE_IMAGE`:

```
Dockerfile.x86_64  →  Dockerfile.ros2_humble  →  Dockerfile.realsense  →  Dockerfile.thornbots
```

This repo pins that key via
`isaac_ros_common/scripts/.isaac_ros_common-config`:

```bash
CONFIG_IMAGE_KEY=ros2_humble.realsense.thornbots
```

`Dockerfile.thornbots` is the custom top layer — it installs the Isaac ROS
apt packages this project needs (yolov8, dnn_image_encoder, tensor_rt,
realsense, ros-gz for sim), patches the RealSense config YAMLs, and
git-clones + colcon-builds this org's packages (`sllidar_ros2`,
`ros2_dji_serial_bridge`, `Realsense_ROI_Depth_Rectifier`, `sentry_pkg`,
`realsense-yolov8-nitros-bridge`) straight into the image at
`/workspaces/ros2_ws`. See the comment header in that file for the full layer
list and cache-busting `ARG RECLONE_*` args.

`sim`'s gz-sim/`ros_gz` deps are **not** installed by default (real hardware
never launches gz-sim) — its layer is commented out in `Dockerfile.thornbots`.
If you need to run `sim` in a container built from this image, run
`sudo isaac_ros_common/docker/scripts/install-sim.sh` once after attaching
(installs `ros-humble-ros-gz` + builds `sim`; it's already bind-mounted at
`isaac_ros-dev/src/sim`, no clone needed).

## Helper scripts for running commands in the container (recommended)

`isaac_ros_common/scripts/dexec.sh` and `kill_launch.sh` wrap the two
error-prone patterns documented later in this file (correct env sourcing,
and cleanly killing a backgrounded `ros2 launch` tree) so you don't have to
hand-roll them — several sessions/agents working on this project got these
subtly wrong before the scripts existed (missing `-u admin`, forgetting one
of the two workspace installs, `kill`ing a process group as raw `docker
exec` argv instead of via `bash -c` as the right user, which silently fails
to deliver the signal).

```bash
# Run a one-off command with the correct env (both workspace installs +
# /etc/bash.bashrc, PS1 satisfied) already sourced:
isaac_ros_common/scripts/dexec.sh -- ros2 topic list

# Run as root (e.g. for apt-get):
isaac_ros_common/scripts/dexec.sh -r -- apt-get install -y ros-humble-foo

# Launch something and leave it running in the background (setsid'd so
# kill_launch.sh can clean up the whole tree later):
isaac_ros_common/scripts/dexec.sh -d -- ros2 launch sim sim.launch.py
# -> prints the log path and the follow-up commands

# List running launch trees with their PIDs. Use this rather than
# `ps aux | grep "ros2 launch"`, which also matches dexec.sh's own bash
# wrapper -- killing that PID's group leaves the real tree running:
isaac_ros_common/scripts/kill_launch.sh -l

# Cleanly stop that launch tree (all its child nodes too, not just the
# launch process itself):
isaac_ros_common/scripts/kill_launch.sh <ros2-launch-pid>
```

`dexec.sh` is the intended way to run anything in the container — it is the
only form that gets the FastDDS profile, `ROS_DOMAIN_ID`, both workspace
installs, `-u admin` (X11/GUI), stdin passthrough, and exit-code
propagation right at once. Prefer it over hand-rolled `docker exec`.
One caveat worth knowing: it resolves packages differently from the user's
terminal — see "Two workspaces" in the `isaac-ros-docker` skill.

Set `ISAAC_ROS_CONTAINER` to override the container name if it's not
`isaac_ros_dev-x86_64-container` (e.g. on aarch64). See each script's own
header comment for the full story on why they're built the way they are.

## Common tasks

**Attach a second terminal to the already-running container**
```bash
./run_dev.sh
```
Just re-run the same script — it detects the running container by name and
`docker exec`s a new shell into it instead of building/launching again (see
`run_dev.sh` lines 190-197). Equivalent manual form, if you need to tweak
flags docker exec supports that `run_dev.sh` doesn't expose:
```bash
docker exec -it -u admin --workdir /workspaces/isaac_ros-dev isaac_ros_dev-x86_64-container bash
```

**Force a full image rebuild** (e.g. after editing `Dockerfile.thornbots`)
```bash
./run_dev.sh   # rebuilds by default unless a container is already running
```
If a container is already running, stop it first: `docker stop isaac_ros_dev-x86_64-container`.

**Rebuild without touching the cache for earlier layers** — bump the
relevant `RECLONE_*` build arg so only that package (and later layers)
re-clone/rebuild:
```bash
docker build --build-arg RECLONE_BRIDGE=37 -f isaac_ros_common/docker/Dockerfile.thornbots -t <image> isaac_ros_common/docker
```
(Note: `run_dev.sh`/`build_image_layers.sh` don't expose a flag for this —
for iterating on one of the cloned packages, it's usually faster to just
`git pull`/rebuild inside the running container with `colcon build`.)

**Skip the image build and just launch** (use existing cached image)
```bash
./run_dev.sh -b
# or
SKIP_DOCKER_BUILD=1 ./run_dev.sh
```

**Point at a different workspace directory**
```bash
./run_dev.sh -d /path/to/isaac_ros-dev
```

**Pass extra `docker run` args** (repeatable)
```bash
./run_dev.sh -a "-v /extra/host/path:/extra/container/path"
```
Or drop them one-per-line in `~/.isaac_ros_dev-dockerargs` (env vars in each
line are expanded via `envsubst`).

## What's already wired up for you inside the container

- GPU passthrough (`--runtime nvidia`, `NVIDIA_VISIBLE_DEVICES=all`)
- X11 forwarding for GUI apps (rviz2, gz sim) — `DISPLAY` and `.Xauthority`
  are forwarded from the host
- SSH agent forwarding, if `SSH_AUTH_SOCK` is set on the host
- `--network host` and `--ipc=host`
- `ROS_DOMAIN_ID` inherited from the host env
- Container user is created/renamed on entry to match your host UID/GID
  (`workspace-entrypoint.sh`), and is added to `video`, `plugdev`, `sudo`,
  and `dialout` groups (the last one patched in by `Dockerfile.thornbots` for
  serial device access, e.g. the DJI bridge)
- FastDDS profile (`FASTRTPS_DEFAULT_PROFILES_FILE=/etc/fastdds/profile.xml`,
  source `isaac_ros_common/docker/fastdds_cable.xml`) set as every
  interactive shell's default RTPS participant profile. As of 2026-07-20 it
  no longer hardcodes an explicit unicast peer at the real robot's
  tethered-link IP — that entry measurably broke/delayed local multicast
  discovery whenever the robot isn't actually attached (i.e. essentially all
  sim/dev sessions), even with `useBuiltinTransports=true`. See "FastDDS
  profile" in the isaac-ros-docker skill and the Troubleshooting section
  below for the full story if discovery ever looks broken again (`ros2
  topic list` showing almost nothing, `ros2 topic hz`/`echo` hanging or
  saying "does not appear to be published yet", rviz's Fixed Frame dropdown
  empty).
- **Any `docker exec` running ROS commands should replicate a real
  interactive shell's environment, not hand-roll a partial one.**
  `/etc/bash.bashrc` (which sets `ROS_DOMAIN_ID`, `RMW_IMPLEMENTATION`,
  `FASTRTPS_DEFAULT_PROFILES_FILE`, and sources both `/opt/ros/humble` and
  `/workspaces/ros2_ws/install`) starts with `[ -z "$PS1" ] && return` — it
  is an **interactive-shell-only** file, so `docker exec ... bash -lc
  "source /etc/bash.bashrc && ..."` silently does nothing (the guard returns
  immediately) unless `PS1` is set first. A `docker exec` session that skips
  this (or manually exports only `ROS_DOMAIN_ID`) can look completely
  healthy while missing real config differences from the user's actual
  terminal — this delayed diagnosing the FastDDS `initialPeersList` bug
  above for a long time, since every debugging session using a hand-rolled
  env accidentally avoided the bug the user's real shell always hit.
  **Use `isaac_ros_common/scripts/dexec.sh`** (see "Helper scripts" above)
  instead of hand-rolling this — it already gets the pattern right:
  ```bash
  isaac_ros_common/scripts/dexec.sh -- ros2 topic list
  ```
  Manual equivalent, if you need to see/tweak the exact pattern — note the
  `>/dev/null` on the sourcing: Ubuntu's `/etc/bash.bashrc` prints a
  two-line `sudo` hint on **stdout** every time the interactive guard
  passes, which otherwise gets glued onto the front of any captured output
  (`X=$(docker exec …)` comes back with banner text in it):
  ```bash
  docker exec -i -u admin --workdir /workspaces/isaac_ros-dev isaac_ros_dev-x86_64-container \
    bash -lc "{ export PS1='\$ ' && source /etc/bash.bashrc ; } >/dev/null && ros2 topic list"
  ```
  **Also source the main workspace install** when running anything from
  `sim` or `sentry_pkg` — `/etc/bash.bashrc` only sources
  `/workspaces/ros2_ws/install` (the image's baked-in packages like
  `sllidar_ros2`), not `/workspaces/isaac_ros-dev/install` (the packages
  built from this repo). Without it, `ros2 launch sim sim.launch.py` fails
  with "package 'sim' not found" even though the package is built.
  `dexec.sh` already sources both; the manual equivalent:
  ```bash
  docker exec -u admin --workdir /workspaces/isaac_ros-dev isaac_ros_dev-x86_64-container \
    bash -lc "export PS1='\$ ' && source /etc/bash.bashrc && source /workspaces/isaac_ros-dev/install/setup.bash && ros2 launch sim sim.launch.py"
  ```
- **Killing a backgrounded `ros2 launch` tree**: sending `SIGINT` to just
  the launch process's PID doesn't reliably propagate to its child nodes
  when it was started without a controlling TTY (e.g. via `docker exec -d`)
  — you have to signal its whole process group. Also, running `kill` as raw
  `docker exec` argv (no `-u admin`, no shell) was found to silently fail to
  deliver the signal at all, even though it looks like it ran; it has to go
  through `bash -c` as the user that owns the process. Use
  `isaac_ros_common/scripts/kill_launch.sh <launch-pid>` instead of hand-
  rolling this, and never use `pkill`/`killall` — a partial kill that leaves
  orphaned children running alongside a fresh relaunch causes duplicate-node
  TF jitter.

## Robot deployment image

`isaac_ros_common/scripts/docker_deploy.sh` builds a separate, slimmer image
intended for flashing/running on the robot itself (not the interactive dev
container) — it layers in extra debs/tarballs, does a `rosdep install` +
`colcon build` of a given ROS workspace, and sets a default
`ros2 launch <package> <launch_file>` command. See that script's header
comment for a usage example. This is a different workflow from `run_dev.sh`
and most day-to-day development doesn't need it.

## Troubleshooting

- **"not a member of the docker group"** — `sudo usermod -aG docker $USER &&
  newgrp docker`, then re-run.
- **"Unable to run docker commands"** — check `docker ps` works standalone;
  you may need to log out/in after being added to the `docker` group.
- **"git-lfs is not installed" / LFS files missing** — install `git-lfs`,
  then re-clone the repos in this workspace (`run_dev.sh` checks LFS file
  integrity in `$ISAAC_ROS_DEV_DIR` before launching).
- **Build succeeds but no image found** — `build_image_layers.sh` couldn't
  resolve one of the composite `Dockerfile.<suffix>` names; check
  `CONFIG_IMAGE_KEY` in `.isaac_ros_common-config` matches actual files under
  `isaac_ros_common/docker/`.
- **Topics show matched publishers/subscribers (`ros2 topic info --verbose`)
  but `ros2 topic hz`/`echo` never receive anything, OR `ros2 topic list`
  itself only shows a couple topics (e.g. just `/parameter_events`/`/rosout`)
  even though far more are actually running, OR rviz's Fixed Frame dropdown
  is completely empty / typing a frame name gives "Frame [X] does not
  exist"** — this is FastDDS discovery being broken or badly delayed by
  `/etc/fastdds/profile.xml`. Two distinct causes were found and fixed here
  (2026-07-20), in order of how the investigation actually went — the first
  wasn't the real fix, the second was:
  1. `<useBuiltinTransports>` must be `true` (FastDDS default) — `false`
     disables default local multicast/SHM discovery entirely, restricting
     nodes to only the explicit `initialPeersList` peer. Already fixed
     previously; if this regresses, `ros2 topic hz`/`echo` hang with zero
     data despite `ros2 topic info --verbose` showing a match.
  2. **The bigger, sneakier one**: even with `useBuiltinTransports=true`, an
     explicit `<initialPeersList>` unicast peer that's unreachable (the real
     robot's tethered IP, `192.168.55.1` — unreachable during any sim/dev
     session without the robot attached) measurably breaks/delays local
     multicast discovery in practice, despite the profile's own comment
     claiming it's "purely additive." Confirmed by removing the peers list
     and watching `ros2 topic list` go from ~2 topics to the full graph.
     Fixed by removing `<initialPeersList>` from `fastdds_cable.xml`
     entirely — normal multicast discovery already reaches the real robot
     over the tethered link when it's actually connected, without needing to
     hardcode its IP.
  A red herring chased along the way: `RMW_FASTRTPS_PUBLICATION_MODE=ASYNCHRONOUS`
  (previously set in `/etc/bash.bashrc` via `Dockerfile.thornbots`) was
  removed too, since FastDDS's async publication mode has real known issues
  delivering `TRANSIENT_LOCAL` historical data (like `/tf_static`) to
  late-joining subscribers — a legitimate fix to keep, but it turned out
  **not** to be what was causing the symptoms above; the `initialPeersList`
  issue was. Both changes need an image rebuild (`./run_dev.sh`, not `-b`)
  to take effect, and any already-running `ros2` daemon needs `ros2 daemon
  stop && ros2 daemon start` afterward (it caches its old, broken
  participant otherwise). See `SESSION_NOTES.md` for the full
  blow-by-blow.
