# Docker dev container — full reference

Tier-two detail behind `SKILL.md`. Read `SKILL.md` first; come here for the
flag catalogue, the manual equivalents of what the helper scripts do, and the
dated postmortems. Where the two disagree, `SKILL.md` is newer and wins.

The workspace runs inside a Docker dev container built from
`isaac_ros_common`'s scripts and layered Dockerfiles. Host source (`src/` and
its parent `isaac_ros-dev/`) is bind-mounted at `/workspaces/isaac_ros-dev`,
so edits outside the container are immediately visible inside it and vice
versa. Rebuild the image only when dependencies change (apt packages, cloned
repos in `Dockerfile.thornbots`), not for ordinary source edits.

## Container lifecycle

```bash
cd isaac_ros_common/scripts
./run_dev.sh
```

- First run builds the image (can take a while), then launches a container
  named `isaac_ros_dev-<arch>-container` and drops you into a bash shell as
  the `admin` user, workdir `/workspaces/isaac_ros-dev`.
- Re-running `run_dev.sh` while the container is already running just attaches
  another shell instead of starting a second container.
- The container is started with `docker run -it --rm`, so it is **not** left
  running in the background. `Ctrl-D`/`exit` on the *first* shell (the one
  that ran `run_dev.sh` and launched the container, i.e. the one running
  `workspace-entrypoint.sh` as PID 1) stops the container and Docker
  auto-removes it. `docker exec`-attached shells can exit freely without
  affecting the container; only exiting the original launching shell tears it
  down. The next `run_dev.sh` starts a fresh container (and rebuilds the image
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

Pinned via `isaac_ros_common/scripts/.isaac_ros_common-config`:

```bash
CONFIG_IMAGE_KEY=ros2_humble.realsense.thornbots
```

`Dockerfile.thornbots` is the custom top layer. It installs the Isaac ROS
apt packages this project needs (yolov8, dnn_image_encoder, tensor_rt,
realsense, ros-gz for sim), patches the RealSense config YAMLs, and
git-clones + colcon-builds this org's packages straight into the image at
`/workspaces/ros2_ws`. See the comment header in that file for the full layer
list and cache-busting `ARG RECLONE_*` args.

**Complete list of packages baked into `/workspaces/ros2_ws`**, the ground
truth behind the shadowing warnings in each package's `AGENTS.md`
(directory name → ROS package name → cache-bust arg):

| cloned repo | ROS package | `RECLONE_*` |
|---|---|---|
| `sllidar_ros2` | `sllidar_ros2` | `RECLONE_SLLIDAR` |
| `ros2_dji_serial_bridge` | `dji_serial_bridge` | `RECLONE_SERIAL` |
| `Realsense_ROI_Depth_Rectifier` | `roi_depth_query` | `RECLONE_DEPTH` |
| `rf2o_laser_odometry` | `rf2o_laser_odometry` | `RECLONE_RF2O` |
| `sentry_localization` | `sentry_localization` | `RECLONE_LOCALIZATION` |
| `sentry_pkg` | `sentry_pkg` | `RECLONE_SENTRY` |
| `realsense-yolov8-nitros-bridge` | `realsense_yolov8_nitros_bridge` | `RECLONE_BRIDGE` |

`sim` is **not** in that list. It is deliberately never cloned or built into
the image (real hardware never launches gz-sim), which is why it is the one
package with no shadow copy and why a fresh container needs `install-sim.sh`
before the first sim launch. See `SKILL.md`.

## `run_dev.sh` flags and common tasks

All of these are **for the user to run**. Anything that can rebuild the
image is theirs, not an agent's (see the standing rule at the top of
`SKILL.md`).

**Attach a second terminal to the already-running container** by re-running
the same script; it detects the running container by name and `docker exec`s
a new shell in (see `run_dev.sh` lines 190-197):

```bash
./run_dev.sh
# equivalent manual form, if you need docker exec flags run_dev.sh doesn't expose:
docker exec -it -u admin --workdir /workspaces/isaac_ros-dev isaac_ros_dev-x86_64-container bash
```

**Force a full image rebuild** (e.g. after editing `Dockerfile.thornbots`):
`./run_dev.sh` rebuilds by default unless a container is already running; if
one is, stop it first with `docker stop isaac_ros_dev-x86_64-container`.

**Rebuild without busting earlier layers' cache** by bumping the relevant
`RECLONE_*` build arg, so only that package and later layers re-clone. There's
no `run_dev.sh`/`build_image_layers.sh` flag for this; when iterating on one
cloned package it's usually faster to `git pull` + `colcon build` inside the
running container instead.

**Other flags:**

```bash
./run_dev.sh -b                      # skip the build, use the cached image
SKIP_DOCKER_BUILD=1 ./run_dev.sh     # same thing
./run_dev.sh -d /path/to/isaac_ros-dev        # point at a different workspace
./run_dev.sh -a "-v /host/path:/container/path"   # extra docker run args (repeatable)
```

Extra `docker run` args can also go one-per-line in
`~/.isaac_ros_dev-dockerargs` (env vars in each line are expanded via
`envsubst`).

## What's already wired up inside the container

- GPU passthrough (`--runtime nvidia`, `NVIDIA_VISIBLE_DEVICES=all`)
- X11 forwarding for GUI apps (rviz2, gz sim): `DISPLAY` and `.Xauthority`
  forwarded from the host
- SSH agent forwarding, if `SSH_AUTH_SOCK` is set on the host
- `--network host` and `--ipc=host`
- `ROS_DOMAIN_ID` inherited from the host env
- Container user is created/renamed on entry to match your host UID/GID
  (`workspace-entrypoint.sh`), and added to `video`, `plugdev`, `sudo`, and
  **`dialout`**, the last one patched in by `Dockerfile.thornbots` for serial
  device access (the DJI bridge's UART link)
- FastDDS profile (`FASTRTPS_DEFAULT_PROFILES_FILE=/etc/fastdds/profile.xml`,
  source `isaac_ros_common/docker/fastdds_cable.xml`) set as every interactive
  shell's default RTPS participant profile. As of 2026-07-20 it no longer
  hardcodes an explicit unicast peer at the real robot's tethered-link IP.
  See the Troubleshooting postmortem below.

## Manual equivalents of what `dexec.sh` does

Use `dexec.sh`. These are here so the pattern is inspectable, and because
each line encodes a bug that cost real debugging time.

**The `PS1` interactive guard.** `/etc/bash.bashrc` sets `ROS_DOMAIN_ID`,
`RMW_IMPLEMENTATION`, `FASTRTPS_DEFAULT_PROFILES_FILE` and sources both
`/opt/ros/humble` and `/workspaces/ros2_ws/install`, but it starts with
`[ -z "$PS1" ] && return`. It is an **interactive-shell-only** file, so
`docker exec ... bash -lc "source /etc/bash.bashrc && ..."` silently does
nothing unless `PS1` is set first. A `docker exec` session that skips this
(or exports only `ROS_DOMAIN_ID` by hand) can look completely healthy while
differing from the user's real terminal in ways that matter. That is what
delayed diagnosing the FastDDS `initialPeersList` bug below for a long time:
every debugging session using a hand-rolled env accidentally avoided the bug
the user's real shell always hit.

Note the `>/dev/null` on the sourcing: Ubuntu's `/etc/bash.bashrc` prints a
two-line `sudo` hint on **stdout** every time the interactive guard passes,
which otherwise gets glued onto the front of captured output, so `X=$(docker
exec …)` comes back with banner text in it.

```bash
docker exec -i -u admin --workdir /workspaces/isaac_ros-dev isaac_ros_dev-x86_64-container \
  bash -lc "{ export PS1='\$ ' && source /etc/bash.bashrc ; } >/dev/null && ros2 topic list"
```

**Both workspace installs.** `/etc/bash.bashrc` only sources
`/workspaces/ros2_ws/install` (the image's baked-in packages), not
`/workspaces/isaac_ros-dev/install` (packages built from this repo). Without
the second, `ros2 launch sim sim.launch.py` fails with "package 'sim' not
found" even though it's built:

```bash
docker exec -u admin --workdir /workspaces/isaac_ros-dev isaac_ros_dev-x86_64-container \
  bash -lc "export PS1='\$ ' && source /etc/bash.bashrc && source /workspaces/isaac_ros-dev/install/setup.bash && ros2 launch sim sim.launch.py"
```

## Killing a backgrounded launch tree

Sending `SIGINT` to just the launch process's PID doesn't reliably propagate
to child nodes when it was started without a controlling TTY (e.g. via
`docker exec -d`); you have to signal the whole process group. Running
`kill` as raw `docker exec` argv (no `-u admin`, no shell) was found to
silently fail to deliver the signal at all, even though it looks like it ran;
it has to go through `bash -c` as the user that owns the process.

Use `kill_launch.sh <launch-pid>`, never `pkill`/`killall`: a partial kill
that leaves orphaned children running alongside a fresh relaunch causes
duplicate-node TF jitter.

**Get the PID from `kill_launch.sh -l`, not `ps aux | grep "ros2 launch"`.**
That grep also matches `dexec.sh`'s own bash wrapper; killing *that* PID's
group leaves the real tree running. (The `ps aux` grep is still the right
tool for the different job of *detecting* whether a session is live before
you start one.)

## Robot deployment image

`isaac_ros_common/scripts/docker_deploy.sh` builds a separate, slimmer image
for flashing/running on the robot itself, not the interactive dev container.
It layers in extra debs/tarballs, does a `rosdep install` + `colcon build` of
a given ROS workspace, and sets a default `ros2 launch <package>
<launch_file>` command. See that script's header comment for a usage example.
Day-to-day development doesn't need it.

## Troubleshooting

- **"not a member of the docker group"**: `sudo usermod -aG docker $USER &&
  newgrp docker`, then re-run.
- **"Unable to run docker commands"**: check `docker ps` works standalone;
  you may need to log out/in after being added to the `docker` group.
- **"git-lfs is not installed" / LFS files missing**: install `git-lfs`,
  then re-clone the repos in this workspace (`run_dev.sh` checks LFS file
  integrity in `$ISAAC_ROS_DEV_DIR` before launching).
- **Build succeeds but no image found**: `build_image_layers.sh` couldn't
  resolve one of the composite `Dockerfile.<suffix>` names; check
  `CONFIG_IMAGE_KEY` in `.isaac_ros_common-config` matches actual files under
  `isaac_ros_common/docker/`.

### FastDDS discovery — the 2026-07-20 postmortem

Symptoms: topics show matched publishers/subscribers (`ros2 topic info
--verbose`) but `ros2 topic hz`/`echo` never receive anything; OR `ros2 topic
list` shows only a couple of topics (e.g. just `/parameter_events` and
`/rosout`) though far more are running; OR rviz's Fixed Frame dropdown is
empty and typing a frame name gives "Frame [X] does not exist".

This is FastDDS discovery broken or badly delayed by
`/etc/fastdds/profile.xml`. Two distinct causes were found and fixed, listed
in the order the investigation actually went. The first wasn't the real fix;
the second was:

1. `<useBuiltinTransports>` must be `true` (the FastDDS default). `false`
   disables default local multicast/SHM discovery entirely, restricting nodes
   to only the explicit `initialPeersList` peer. Already fixed previously; if
   it regresses, `ros2 topic hz`/`echo` hang with zero data despite `ros2
   topic info --verbose` showing a match.
2. **The bigger, sneakier one**: even with `useBuiltinTransports=true`, an
   explicit `<initialPeersList>` unicast peer that's unreachable (the real
   robot's tethered IP `192.168.55.1`, unreachable during any sim/dev session
   without the robot attached) measurably breaks/delays local multicast
   discovery in practice, despite the profile's own comment claiming it's
   "purely additive." Confirmed by removing the peers list and watching `ros2
   topic list` go from ~2 topics to the full graph. Fixed by removing
   `<initialPeersList>` from `fastdds_cable.xml` entirely; normal multicast
   discovery already reaches the real robot over the tethered link when it's
   actually connected.

A red herring chased along the way: `RMW_FASTRTPS_PUBLICATION_MODE=ASYNCHRONOUS`
(previously set in `/etc/bash.bashrc` via `Dockerfile.thornbots`) was removed
too, since FastDDS's async publication mode has real known issues delivering
`TRANSIENT_LOCAL` historical data (like `/tf_static`) to late-joining
subscribers. That's a legitimate fix to keep, but **not** what caused the
symptoms above. Don't re-blame it.

Both changes need a full image rebuild (`./run_dev.sh`, not `-b`) to take
effect, and any already-running daemon needs `ros2 daemon stop && ros2 daemon
start` afterward, since it caches its old, broken participant otherwise. Full
blow-by-blow in `SESSION_NOTES.md`.
