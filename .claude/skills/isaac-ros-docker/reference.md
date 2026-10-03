# Docker dev container: full reference (Jazzy)

Tier-two detail behind `SKILL.md`. Read `SKILL.md` first; come here for the
`isaac-ros` flag catalogue, where the CLI reads its config, the manual
equivalents of the helper scripts, and the dated postmortems. Where the two
disagree, `SKILL.md` is newer and wins.

The container comes from `isaac-ros-cli` (release-4.6), which replaced the
fork's `run_dev.sh` and `build_image_layers.sh`. Host `$ISAAC_ROS_WS` is
bind-mounted at `/workspaces/isaac_ros-dev`, so edits outside the container
are visible inside it and vice versa. Rebuild the image only when
dependencies or the baked package sources change, never for ordinary source
edits: the bind mount already carries those.

Every command in the next three sections is **for the user to run**. An agent
never runs `isaac-ros activate` in any form (the rule at the top of
`SKILL.md`).

## Container lifecycle

```bash
export ISAAC_ROS_WS=~/workspaces/isaac_ros-jazzy   # the workspace holding src/
isaac-ros activate
```

- If the image is missing, `activate` tries `docker pull` and stops with
  `Use --build to build remotely or --build-local to build locally`. Ours is
  never on a registry, so the first run needs `--build-local`.
- It starts `docker run -it --rm --privileged --network host --ipc=host` with
  the name from `docker.run.container_name` (ours: `isaac_ros_jazzy_container`)
  and drops you into bash as `admin` in `/workspaces/isaac_ros-dev`.
- Re-running `activate` while the container runs attaches another shell.
- Exiting the *first* shell stops the container and Docker removes it.
  `docker exec` shells can come and go.
- `activate` exits 0 even when the build or run failed. Read its output.
- `-it` means it needs a real terminal. On the laptop the user may keep it
  in a detached tmux session (`tmux attach -t jazzy`); that shell is the
  container's PID 1 shell, so don't send it keys.

## Where the CLI reads its config

Read from the release-4.6 source; the docs and the plan got two of these
wrong. `isaac_ros_common/scripts/setup_workspace.sh` links ours into place.

| file | searched in (first hit wins) | ours |
|---|---|---|
| `config.yaml` | merged: `/usr/share/isaac-ros-cli/`, `/etc/isaac-ros-cli/`, `~/.config/isaac-ros-cli/`, `$ISAAC_ROS_WS/.isaac-ros-cli/` (last wins) | `isaac_ros_common/.isaac-ros-cli/config.yaml` |
| `.isaac_ros_common-config` | `$ISAAC_ROS_WS/../scripts/`, `$ISAAC_ROS_WS/scripts/`, `/etc/isaac-ros-cli/` | `isaac_ros_common/scripts/.isaac_ros_common-config` |
| `.build_image_layers.yaml` | `$ISAAC_ROS_WS/../scripts/`, `/etc/isaac-ros-cli/` | `isaac_ros_common/scripts/.build_image_layers.yaml` |
| `.isaac_ros_dev-dockerargs` | `$DOCKER_ARGS_FILE`, `~/.isaac_ros_dev-dockerargs`, then `$ISAAC_ROS_WS/scripts/` or else `/etc/isaac-ros-cli/` | none |
| mode (`docker`) | `/etc/isaac-ros-cli/environment.conf` | set by `sudo isaac-ros init docker` |

- `config.yaml` keys (unknown keys are rejected): `version: 2`;
  `docker.image.{base_image_keys, additional_image_keys, push}`;
  `docker.run.{container_name, entrypoint, workdir, platform,
  use_cached_build_image}`; `apt.{key_url, repository, distro, components}`.
  `entrypoint` and `workdir` are validated but `run_dev.py` hardcodes both.
- `.isaac_ros_common-config` is sourced by bash; only
  `CONFIG_DOCKER_SEARCH_DIRS` and `BASE_DOCKER_REGISTRY_NAMES` are read. The
  CLI stops at the first file, so ours lists the CLI's own `docker/` too.
- `.build_image_layers.yaml` holds `context_overrides` (`thornbots: ../..`
  makes `src/` the build context), `image_key_order` and the registries. It
  replaces the stock file wholesale. Its only per-workspace location is
  *outside* the workspace, so sibling workspaces share it: re-run
  `setup_workspace.sh` from the one you build.
- The stock `/etc/isaac-ros-cli/.isaac_ros_dev-dockerargs` mounts `~/.ssh`,
  `~/.aws`, `~/.cache`, `~/.config` (read-write), `~/.gitconfig` and
  `~/.bash_history`. The CLI also mounts the host `~/.bashrc`, `~/.profile`
  and `~/.bash_profile` read-only into `/home/admin`.

## Which image gets built

`base_image_keys` + `additional_image_keys` = `isaac_ros`, `realsense`,
`thornbots`, each resolved to a `Dockerfile.<key>` in the search dirs:

```
Dockerfile.isaac_ros (CLI)  →  Dockerfile.realsense (CLI)  →  isaac_ros_common/docker/Dockerfile.thornbots
```

`isaac_ros_common/docker/README.md` is the reference for
`Dockerfile.thornbots`: layers, context, rosdep. The short version:

- Sources come from the **checked-out submodules in `src/`**, uncommitted
  edits included.
- The final tag is `nvcr.io/nvidia/isaac/ros:isaac_ros-realsense-thornbots_<hash>-amd64`
  (`-arm64-jetpack` on a Jetson). The hash covers the Dockerfiles and apt
  build args only, not package sources, so `activate` keeps starting an image
  that predates your package edits until that tag is removed.
- The `isaac_ros` layer is on NGC, but the CLI checks for it under a
  different name when building, so `--build-local` builds it locally too
  (cached after the first time). `realsense` compiles librealsense.

**Packages `Dockerfile.thornbots` bakes into `/workspaces/ros2_ws`**, the
list behind the shadowing warnings in each package's `AGENTS.md` (directory
name → ROS package name). `dexec.sh -- ls /workspaces/ros2_ws/src` is the
ground truth for a running container:

| source dir in `src/` | ROS package |
|---|---|
| `sllidar_ros2` | `sllidar_ros2` |
| `ros2_dji_serial_bridge` | `dji_serial_bridge` |
| `Realsense_ROI_Depth_Rectifier` | `roi_depth_query` |
| `rf2o_laser_odometry` | `rf2o_laser_odometry` |
| `sentry_localization` | `sentry_localization` |
| `thornbots_pkg` | `thornbots_pkg` |
| `realsense-yolov8-nitros-bridge` | `realsense_yolov8_nitros_bridge` |

`sim` is **not** in that list. Real hardware never launches gz-sim, so it is
the one package with no shadow copy, and a fresh container needs
`install-sim.sh` before the first sim launch. See `SKILL.md`.

## `isaac-ros` flags and common tasks

```bash
isaac-ros activate                      # attach, or start from an existing/pullable image
isaac-ros activate --build-local        # build locally if the image is missing, then start
isaac-ros activate --build              # same, on the configured remote builder (we have none)
isaac-ros activate --build-only         # build/pull, don't start (no TTY needed)
isaac-ros activate --start-only         # start or attach; fail if the image is missing
isaac-ros activate --no-cache           # rebuild every layer, isaac_ros and realsense included
isaac-ros activate --use-cached-build-image   # run the last image activate used (cached_isaac_run_dev_image_local)
isaac-ros activate --push / --no-push   # push built layers to the registry (we don't)
isaac-ros activate --verbose            # print the resolved Dockerfiles, bake file and docker run
isaac-ros activate -c docker.run.container_name=foo   # override a config.yaml key once (repeatable)
isaac-ros status                        # mode and whether this shell is activated
sudo isaac-ros init docker              # one-time: set the mode
```

**Attach a second terminal**: run `isaac-ros activate` again, or

```bash
docker exec -it -u admin --workdir /workspaces/isaac_ros-dev isaac_ros_jazzy_container bash
```

**Rebuild after package or Dockerfile edits**: exit the container, remove the
final tag, build again. BuildKit's cache reruns only changed layers.

```bash
docker rmi nvcr.io/nvidia/isaac/ros:isaac_ros-realsense-thornbots_<hash>-amd64
isaac-ros activate --build-local
```

A `Dockerfile.thornbots` edit changes the hash, so there the old tag can stay.

**Rebuilding one package** for day-to-day work needs no image rebuild at all:
`colcon build` inside the running container.

Extra `docker run` args go one per line in `~/.isaac_ros_dev-dockerargs`
(env vars in each line are expanded).

**Installing the CLI.** On Ubuntu: add the Isaac ROS apt repo (`release-4`,
`noble`), `sudo apt-get install isaac-ros-cli`, `sudo isaac-ros init docker`.
On the Arch laptop: `isaac_ros_common/scripts/install_isaac_ros_cli.sh`, a
no-root install into `~/.local` (its header says how).

## What's already wired up inside the container

- GPU passthrough (`--gpus all`, `NVIDIA_VISIBLE_DEVICES=all`)
- X11 forwarding for GUI apps (rviz2, gz sim): `DISPLAY` and `.Xauthority`
  forwarded from the host
- `--network host`, `--ipc=host`, `--privileged`
- `ROS_DOMAIN_ID` from the host env, overridden to 1 by `/etc/bash.bashrc`
  until the robots move to Jazzy
- Container user is created/renamed on entry to match your host UID/GID
  (`workspace-entrypoint.sh`), and added to `video`, `plugdev`, `sudo`, and
  **`dialout`**, the last one from `Dockerfile.thornbots`'s entrypoint
  addition for serial device access (the DJI bridge's UART link)
- FastDDS profile (`FASTRTPS_DEFAULT_PROFILES_FILE=/etc/fastdds/profile.xml`,
  source `isaac_ros_common/docker/fastdds_cable.xml`) set as every interactive
  shell's default RTPS participant profile. SIMPLE discovery plus the robots' tailscale IPs
  as unicast peers; see "Cross-machine ROS 2 over Tailscale" below.

## Manual equivalents of what `dexec.sh` does

Use `dexec.sh`. These are here so the pattern is inspectable, and because
each line encodes a bug that cost real debugging time.

**The `PS1` interactive guard.** `/etc/bash.bashrc` sets `ROS_DOMAIN_ID`,
`RMW_IMPLEMENTATION`, `FASTRTPS_DEFAULT_PROFILES_FILE` and sources both
`/opt/ros/jazzy` and `/workspaces/ros2_ws/install`, but it starts with
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
docker exec -i -u admin --workdir /workspaces/isaac_ros-dev isaac_ros_jazzy_container \
  bash -lc "{ export PS1='\$ ' && source /etc/bash.bashrc ; } >/dev/null && ros2 topic list"
```

**Both workspace installs.** `/etc/bash.bashrc` only sources
`/workspaces/ros2_ws/install` (the image's baked-in packages), not
`/workspaces/isaac_ros-dev/install` (packages built from this repo). Without
the second, `ros2 launch sim sim.launch.py` fails with "package 'sim' not
found" even though it's built:

```bash
docker exec -u admin --workdir /workspaces/isaac_ros-dev isaac_ros_jazzy_container \
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

## Troubleshooting

- **"not a member of the docker group"**: `sudo usermod -aG docker $USER &&
  newgrp docker`, then re-run.
- **"Unable to run docker commands"**: check `docker ps` works standalone;
  you may need to log out/in after being added to the `docker` group.
- **"git-lfs is not installed" / LFS files missing**: install `git-lfs`,
  then re-clone the repos in this workspace (the CLI checks LFS files in
  `$ISAAC_ROS_WS` before launching).
- **`Error: Could not resolve all Dockerfiles`**: a key in
  `docker.image.*_image_keys` has no `Dockerfile.<key>` in the search dirs.
  The error prints the dirs and the config file it used; a wrong
  `ISAAC_ROS_WS` or a missing `setup_workspace.sh` run are the usual causes.
- **`/home/admin/.profile: ... .cargo/env: No such file or directory`** on
  every `dexec.sh` call: the CLI mounts the host's `~/.profile` and
  `~/.bashrc` into the container. Harmless noise on stderr.
- **`ISAAC_ROS_WS or ISAAC_DIR environment variable is not set`**: export
  `ISAAC_ROS_WS` in the shell running `activate`.
- **Build fails at `COPY --parents`/`--exclude`**: the `# syntax=` line at the
  top of `Dockerfile.thornbots` was lost; those flags need `1.7-labs`.

### Cross-machine ROS 2 over Tailscale

tailscale0 carries no usable multicast, so SIMPLE discovery alone never finds a
peer on another machine, though plain UDP to its 100.x address works.

**2026-09-14 (current):** `docker/fastdds_cable.xml` keeps SIMPLE discovery and
adds the robots' tailscale IPs to `<initialPeersList>`. A participant announces
to every listed peer and the peer answers, so only one side needs the other's
address; the laptop lists the robots and needs no entry of its own. Measured in
the dev container:

- A "remote" group of 12 filler participants plus a talker, sending no
  multicast, was discovered by a listener whose only peer was `127.0.0.1` at
  `maxInitialPeersRange` 32, and not at the default 4. The range is per
  transport, which is why the profile redeclares SHM + UDPv4 as user transports
  with `useBuiltinTransports` false.
- With the full profile (multicast + three unreachable robot IPs), the
  `odom_stuck` drift scenario passed in 46s, the same as with no profile.
- Not yet verified between two real machines over tailscale.

Keep `239.255.0.1` in the list: an explicit `<initialPeersList>` replaces the
default multicast peer, the likely cause of the 2026-07-20 postmortem below.

**2026-09-02 to 2026-09-14 (replaced):** the profile made every node a
`SUPER_CLIENT` of Fast DDS discovery servers on the robots, started by hand with
`scripts/dds_server.sh` (now deleted). Nothing discovered anything, even on one
machine, until a server was reachable, so local sim runs needed
`unset FASTRTPS_DEFAULT_PROFILES_FILE`. Lessons that still apply: `profile_name`
must be `participant_profile` (until 2026-09-02 it was `unicast_robot_link` and
never applied), and every machine needs the same `ROS_DOMAIN_ID`. A robot still
running the old `dds-server` container can drop it with `docker rm -f dds-server`.

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
   (Since 2026-09-14 the profile sets `false` on purpose, redeclaring SHM +
   UDPv4 as user transports for `maxInitialPeersRange`; it works because
   `239.255.0.1` stays in the peers list.)
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
   (Superseded 2026-09-14: the list is back with `239.255.0.1` and the
   robots' tailscale IPs; see "Cross-machine ROS 2 over Tailscale".)

A red herring chased along the way: `RMW_FASTRTPS_PUBLICATION_MODE=ASYNCHRONOUS`
(previously set in `/etc/bash.bashrc` via `Dockerfile.thornbots`) was removed
too, since FastDDS's async publication mode has real known issues delivering
`TRANSIENT_LOCAL` historical data (like `/tf_static`) to late-joining
subscribers. That's a legitimate fix to keep, but **not** what caused the
symptoms above. Don't re-blame it.

Both changes need an image rebuild (see "Rebuild after package or Dockerfile edits") to take
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
| `/workspaces/ros2_ws` | `sentry_localization`, `sllidar_ros2`, `rf2o_laser_odometry`, `dji_serial_bridge`, … | **copied from `src/` and built during the Docker build** (`Dockerfile.thornbots` layer 3) -- a snapshot, frozen at build time |
| `/workspaces/isaac_ros-dev` | `sim`, `thornbots_pkg`, `sentry_localization`, … | the **bind-mounted host `src/`** you actually edit |

**Which copy wins depends on the entry point** (re-measured 2026-07-26;
earlier notes here blamed `AMENT_PREFIX_PATH` ordering, which was wrong):

| entry point | what it sources | resolves to |
|---|---|---|
| the user's terminal | `/etc/bash.bashrc`, which ends by sourcing **only** `/workspaces/ros2_ws/install` | the **image-baked snapshot** |
| `dexec.sh` | bashrc, then `ros2_ws`, then `isaac_ros-dev` (prepended, so it wins) | **your `src/` edit**, if that package is built locally |

Packages not built into `/workspaces/isaac_ros-dev/install` (e.g.
`sllidar_ros2`) fall through to `ros2_ws` under either entry point.

Don't take the package list in `reference.md` (or `Dockerfile.thornbots`) as
the container's contents. **The running image can lag the Dockerfile.**
Measured 2026-09-06 against an image built 4 days earlier: the Dockerfile
baked `thornbots_pkg`, but that image's `ros2_ws/src` still held the
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
GitHub repo to survive: teammates' images are built from the committed
submodules.

Packages that exist *only* in `isaac_ros-dev` (notably `sim`, which
`Dockerfile.thornbots` deliberately leaves out; see `install-sim.sh`) have no shadow copy, so `src/` edits to them are live
immediately. That asymmetry is itself confusing: `sim/urdf/*.xacro` edits
apply instantly while `sentry_localization/config/*.yaml` edits appear to
do nothing.


## When editing `Dockerfile.thornbots`

- Keep the layer order (slowest and most stable first): that's what keeps
  rebuilds fast. `isaac_ros_common/docker/README.md` has the table.
- A package's apt dependency goes in its `package.xml`, where the rosdep
  layer picks it up, not in the Dockerfile. Sim-only deps stay out of the
  image (`install-sim.sh`).
- A new first-party package needs only its directory name in the
  `--packages-select` list; the `COPY`s pick it up. Fold any new file into
  the existing config `RUN` rather than adding a layer.


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

Host python is 3.14, container python is 3.12 (3.10 on Humble). PEP 701 changed f-string
tokenization at 3.12 and host tooling keeps moving, so `tokenize`/`ast` tooling run on the host silently
can emit output the container's python rejects. Anything that rewrites source goes
through `dexec.sh`.


## Before/after running any test or one-off sim launch

**Before** launching anything (a background launch, either test launch
file, or an ad hoc probe script), check for a live session first:
```bash
dexec.sh -- ps aux | grep -E 'gz sim|slam_toolbox|amcl|map_server|ekf_filter_node|pose_translator|pose_emulator|ros2 launch' | grep -v grep
```
A dead `gz sim` server leaves orphaned bridges that appear in `ros2 topic
list` but never publish; a *live* session (the user's own manual sim/CV
work, or a previous test that didn't clean up) collides on the same
topics/services (duplicate `/pose_emulator`, `/scan`, etc. publishers) and
silently corrupts whatever you're about to measure. No error, just wrong
numbers or empty samples. The drift suite's own
`check_no_orphans()` does this exact check and only *warns*, it doesn't
block, so don't skip it just because the script ran.

If something is already running, **don't kill it yourself**: it may be
the user's own in-progress work (e.g. a manual CV/rviz session). Ask before
stopping anything you didn't start.

**After** your own test/probe finishes (including when it errors out or
you interrupt it), clean up what *you* started rather than leaving it for
the next run to collide with:
- The official suites (`localization_tests.launch.py`,
  `shot_hit.launch.py`) already do this, and are safe to `kill_launch.sh`:
  `teardown_stack()` runs in a `finally` block, and a per-scenario stack
  also gets SIGINT if pytest dies.
- Any ad hoc script you write that calls `run_stack()`/launches its own
  processes must do the same: wrap the body in `try`/`finally` and call
  `teardown_stack(stack, helper)` (or `kill_launch.sh
  <pid>` for anything launched outside that helper) unconditionally, and
  re-run the `ps aux` check above afterward to confirm nothing's left.

`sim` launches with GUI by default (standing rule in `sim/AGENTS.md`);
that includes both test launches, which take `headless:=true` to opt out:
```bash
isaac_ros_common/scripts/dexec.sh -d -- ros2 launch sim localization_tests.launch.py
```


## Testing a git worktree's changes in docker without merging first

Worktrees created by `EnterWorktree` live *inside* the package directory
(e.g. `sim/.claude/worktrees/<name>/`), which is inside the bind-mounted
tree, so their files are already readable in the container at
`/workspaces/isaac_ros-dev/src/<pkg>/.claude/worktrees/<name>/...` with no
merge. That covers one-off checks (`xacro`, `gz sdf -p`, reading a value).

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
# restore (always, merged or not; the worktree may be removed later)
dexec.sh -- ln -sfn \
  /workspaces/isaac_ros-dev/src/sim/urdf/sentry.urdf.xacro \
  /workspaces/isaac_ros-dev/build/sim/urdf/sentry.urdf.xacro
```
Works for any `--symlink-install`ed file (urdf/xacro, world/sdf, rviz
config, `launch/*.py`). It does **not** work for compiled (C++) packages or
`ros2 run`-launched Python nodes (their installed executable is a generated
wrapper). For those, merge into the main branch locally first (no push
needed), then test normally.

