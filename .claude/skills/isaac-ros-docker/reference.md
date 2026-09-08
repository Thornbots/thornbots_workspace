# Docker dev container: full reference

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

**Packages `Dockerfile.thornbots` clones into `/workspaces/ros2_ws`**, the
list behind the shadowing warnings in each package's `AGENTS.md` (directory
name → ROS package name → cache-bust arg). This is what the *Dockerfile*
says; a running container built before the last edit can hold something else
(on 2026-09-06 a 4-day-old image still had the repo under its old name
`sentry_pkg`). `dexec.sh -- ls /workspaces/ros2_ws/src` is the ground truth:

| cloned repo | ROS package | `RECLONE_*` |
|---|---|---|
| `sllidar_ros2` | `sllidar_ros2` | `RECLONE_SLLIDAR` |
| `ros2_dji_serial_bridge` | `dji_serial_bridge` | `RECLONE_SERIAL` |
| `Realsense_ROI_Depth_Rectifier` | `roi_depth_query` | `RECLONE_DEPTH` |
| `rf2o_laser_odometry` | `rf2o_laser_odometry` | `RECLONE_RF2O` |
| `sentry_localization` | `sentry_localization` | `RECLONE_LOCALIZATION` |
| `thornbots_pkg` | `thornbots_pkg` | `RECLONE_THORNBOTS` |
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

### Cross-machine ROS 2 over Tailscale (2026-09-02)

tailscale0 carries no usable multicast, so SIMPLE discovery never finds a peer
on another machine, however healthy the link is (plain UDP to the peer's 100.x
address works fine; that is not the problem). Cross-machine topics go through a
Fast DDS **discovery server**, started by hand on the publisher:

```bash
isaac_ros_common/scripts/dds_server.sh    # on the robot; -l to check, -s to stop
```

Clients need no env vars: `docker/fastdds_cable.xml` (installed at
`/etc/fastdds/profile.xml`) points at the robots' tailscale addresses. Four
things that each look like something else when they are wrong:

1. **`profile_name` must be `participant_profile`.** rmw_fastrtps looks the
   participant profile up by that exact name; `is_default_profile="true"` is not
   enough. Until 2026-09-02 this file was named `unicast_robot_link`, so the
   whole profile had never applied to anything.
2. **The server needs the same `ROS_DOMAIN_ID` as its clients.** A server in
   domain 0 is invisible to clients in domain 42, and vice versa.
3. **Tools need the whole graph.** A plain `CLIENT` only learns the endpoints it
   matches, so `ros2 topic list`/`hz` and rviz show nothing and it reads exactly
   like broken discovery. The profile uses `SUPER_CLIENT`; a shell overriding it
   with `ROS_DISCOVERY_SERVER` also wants `ROS_SUPER_CLIENT=TRUE`.
4. **Do not add `<useBuiltinTransports>false</useBuiltinTransports>` or an
   `<interfaceWhiteList>`.** Measured 2026-09-02: with those, a participant
   stops registering with the server entirely. The realsense node came up clean,
   opened its stream, and never appeared in the graph even on the server's own
   machine. Same `useBuiltinTransports` trap as the postmortem below, in a
   discovery-server disguise.

If the server is not running, nothing discovers anything, including two nodes on
the same machine. That is the trade for making the remote case work by default;
`dds_server.sh -l` says so in one line.

### FastDDS discovery: the 2026-07-20 postmortem

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
start` afterward, since it caches its old, broken participant otherwise.

---

# Detail moved out of SKILL.md (2026-09-06)

`SKILL.md` keeps the rules and the short form of each of these. Everything
below is the long version: the postmortems, the exact recipes, and the
reasoning. `SKILL.md` links here by section title.

## Two workspaces: `/workspaces/ros2_ws` silently shadows your `src/` edits

**Read this before concluding that a config or source change "had no
effect", and before trusting any measurement taken after editing one.**

There are two colcon workspaces in the container, and they overlap:

| workspace | what's in it | origin |
|---|---|---|
| `/workspaces/ros2_ws` | `sentry_localization`, `sllidar_ros2`, `rf2o_laser_odometry`, `dji_serial_bridge`, … | **git-cloned from GitHub during the Docker build** (`Dockerfile.thornbots` layers 4–10) |
| `/workspaces/isaac_ros-dev` | `sim`, `thornbots_pkg`, `sentry_localization`, … | the **bind-mounted host `src/`** you actually edit |

**Which copy wins depends on the entry point** (re-measured 2026-07-26;
earlier notes here blamed `AMENT_PREFIX_PATH` ordering, which was wrong):

| entry point | what it sources | resolves to |
|---|---|---|
| the user's terminal | `/etc/bash.bashrc`, which ends by sourcing **only** `/workspaces/ros2_ws/install` | the **image-baked GitHub clone** |
| `dexec.sh` | bashrc, then `ros2_ws`, then `isaac_ros-dev` (prepended, so it wins) | **your `src/` edit**, if that package is built locally |

Packages not built into `/workspaces/isaac_ros-dev/install` (e.g.
`sllidar_ros2`) fall through to `ros2_ws` under either entry point.

Don't take the clone list in `reference.md` (or `Dockerfile.thornbots`) as
the container's contents. **The running image can lag the Dockerfile.**
Measured 2026-09-06 against an image built 4 days earlier: the Dockerfile's
LAYER 9 clones `thornbots_pkg`, but that image's `ros2_ws/src` still held the
repo under its old name `sentry_pkg`, so `thornbots_pkg` had *no* shadow copy
at all while a stale `sentry_pkg` did. `ls /workspaces/ros2_ws/src` through
`dexec.sh` is the only ground truth.

Measured through `dexec.sh` on that image, for calibration:

| package | `dexec.sh` resolves to | bashrc-only (user's terminal) |
|---|---|---|
| `sim` | `isaac_ros-dev` | **Package not found** |
| `thornbots_pkg` | `isaac_ros-dev` | **Package not found** |
| `sentry_localization` | `isaac_ros-dev` | `ros2_ws` (shadowed) |
| `rf2o_laser_odometry` | `isaac_ros-dev` | (cloned in both) |
| `sllidar_ros2` | `ros2_ws` | `ros2_ws` |

Shadowing has a second failure mode. A package built *only* into
`isaac_ros-dev` is **invisible** from the user's terminal, so `ros2 launch
sim …` there fails with "package not found" while the same command through
`dexec.sh` works.

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


### Never interpolate a file list into `dexec.sh -- bash -c "…"`

zsh does not word-split inside double quotes, so a newline-separated `find`
result arrives at `bash -c` as one string, and bash reads those newlines as
command separators. Only the first line runs as the command you intended;
**every remaining path is executed as its own command**. On 2026-09-02 this
started a full sim stack that ran for four minutes with nobody typing a launch,
because `sim`'s test wrappers are mode 755 with shebangs, so the stray paths
launched `sim.launch.py` per scenario and collided with another session's
measurements:

```zsh
# WRONG: every path after the first one gets executed
FILES=$(find … | sort)
dexec.sh -- bash -c "cd /workspaces/isaac_ros-dev/src && python3 script.py $FILES"

# use a NUL-delimited pipeline instead
find … -print0 | xargs -0 dexec.sh -- python3 script.py
```

Two things compound it:

- **Host `/tmp` is not the container's `/tmp`.** A script written to the host's
  `/tmp` is simply absent inside the container, so the `python3` call fails
  instantly and bash moves straight on to executing the rest of the list. Put
  helper scripts somewhere under the mounted workspace, never host `/tmp`.
- **`TaskStop` kills the host-side job only.** Container descendants survive it
  and have to be killed from inside the container, via `kill_launch.sh`.

### Run source-rewriting scripts inside the container

Host python is 3.14, container python is 3.10. PEP 701 changed f-string
tokenization between them, so `tokenize`/`ast` tooling run on the host silently
emits output that is invalid under 3.10. Anything that rewrites source goes
through `dexec.sh`.


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

`sim` launches with GUI by default (standing rule in `sim/AGENTS.md`);
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

