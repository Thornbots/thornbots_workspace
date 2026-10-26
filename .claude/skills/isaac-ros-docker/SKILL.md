---
name: isaac-ros-docker
description: Load to run, launch, attach to, drive, screenshot, rebuild, or troubleshoot the isaac_ros-dev Isaac ROS Docker container, and before running `docker exec`, `colcon build`, or `ros2 launch`/`run`/`topic` against it, even if the user never says "docker". Covers creating and removing your own per-agent container, `smoke.sh`, `dexec.sh`/`kill_launch.sh`, the two-workspace shadowing trap, and the DDS discovery profile.
---

# Isaac ROS Docker dev container (Jazzy)

Drive it with `smoke.sh` and `dexec.sh`. Paths here are relative to the
workspace's `src/`. `reference.md`, next to this file, has the long version
of every section below: the `isaac-ros` flag catalogue, where the CLI reads
its config, the manual equivalents of the helper scripts, and the dated
postmortems.

## Your own container

Every agent task makes its own container from the existing image and removes
it when done. Never build the image (`isaac-ros activate`, `docker build`,
`buildx bake`), and never stop, restart or `rm` a container you did not
create, above all the user's long-lived `isaac_ros_jazzy_container`.
[`agent_container.sh`](../../../isaac_ros_common/scripts/agent_container.sh)
enforces the rest:

```bash
ACM=isaac_ros_common/scripts/agent_container.sh           # from this checkout's src/
$ACM up my-task [-w SRC] [-e EVIDENCE_DIR] [-c CPUS] [-m MEM]   # prints the env
export ISAAC_ROS_CONTAINER=isaac-agent-my-task            # dexec.sh/smoke.sh/kill_launch.sh use it
.claude/skills/isaac-ros-docker/smoke.sh
$ACM down my-task                                         # docker rm -f, volumes too
$ACM run my-task -- bash my-script.sh                     # up + run + down, even on failure/SIGTERM
```

Use `run` for anything scripted: its trap removes the container on failure or
SIGTERM. With separate `up`/`down` calls, `down` is yours even after errors.
Stale ones: `$ACM ls`, and `$ACM clean -t 6 [-n]` removes only labelled
containers older than 6 hours whose processes are just init, `sleep` and a
ros2 daemon (`-n` previews).

What the script refuses or guarantees, so you do not have to:

- **Domain/partition:** a unique `ROS_DOMAIN_ID` (100-199, never the robots'
  0-1) and `GZ_PARTITION=agent-<task>-<domain>` per container; collisions with
  any other container are refused. `dexec.sh` re-asserts them after
  `/etc/bash.bashrc`, which hardcodes domain 1, so use it, not bare
  `docker exec`. sim's MCB PTY link derives from both
  (`/tmp/mcb_emulator_pty-<partition>-<domain>`) in the container's own `/tmp`.
- **Network:** default bridge, private IPC, no published ports, not
  privileged; the user's host-network container and other agents cannot see
  its DDS, gz or Foxglove sockets (Foxglove 8765 is the container's own).
- **Mounts:** only your worktree (`-w`, default the checkout holding the
  script) at `/workspaces/isaac_ros-dev/src`, an optional `/evidence`, and
  per-task `build`/`install`/`log` volumes. It refuses `$ISAAC_ROS_WS/src` and
  a worktree another agent container already mounts. Git runs on the host.
- **CPU/memory:** unlimited unless `-c`/`-m` (or `ISAAC_AGENT_CPUS`/
  `ISAAC_AGENT_MEM`); cap long benches so others keep their share.
- **Mac mini (`blaises-mini`, Colima):** run the script there from a checkout
  on the mini. `up` starts Colima if needed; `down`, `clean` and `run`'s exit
  stop it only when no container is left running, so nothing sits idle.

The image is the one the user's container runs, else the newest local
`*thornbots*amd64` (`-i` overrides); on the Mac, `thornbots-mac`. A fresh
container has no `sim` build and no gz-sim: see Key facts.

`docker ps --format '{{.Names}}\t{{.Status}}'` shows who is up. The user's
`isaac_ros_jazzy_container` (name from `docker.run.container_name` in
`isaac_ros_common/.isaac-ros-cli/config.yaml`) and the frozen Humble
`isaac_ros_dev-x86_64-container` are not yours; don't work there.
`ISAAC_ROS_CONTAINER=<name>` picks which container the scripts drive.

## Driving it: `smoke.sh`

```bash
.claude/skills/isaac-ros-docker/smoke.sh          # container? mount? env? pkg resolution? graph?
.claude/skills/isaac-ros-docker/smoke.sh --sim    # + headless sim launch, topic check, teardown
```

Run it before trusting any measurement in your container. It never creates
one. Step 4 prints the package-resolution table through both entry points,
the fastest way to see whether your edit is the code that will run; step 6
refuses to launch on top of a session someone else started; `--sim` tears
down with `kill_launch.sh`.

`--sim` passes `gui:=false`, which drops only the gz window. **rviz** has its
own `rviz:=` argument, on by default when a display is reachable, so a window
still opens on the user's display.

## Key facts

- The user's entry point is `isaac-ros activate` on the host. Yours is
  `dexec.sh` against your own `isaac-agent-<task>` container.
- The image is `isaac_ros` -> `realsense` (both shipped by `isaac-ros-cli`)
  -> `isaac_ros_common/docker/Dockerfile.thornbots`. Ubuntu 24.04, ROS 2
  Jazzy, Isaac ROS 4.6, Python 3.12.
- The user's container bind-mounts the **whole** host workspace root,
  `$ISAAC_ROS_WS` to `/workspaces/isaac_ros-dev`, so `build/`, `install/`,
  `log/` and `src/` are shared and outlive it. An agent container mounts only
  `src/` and keeps its own `build/`, `install/`, `log/` volumes, gone with it.
  Packages are at `/workspaces/isaac_ros-dev/src/<pkg>`; a path missing that
  `src/` resolves to nothing instead of erroring.
- `ROS_DOMAIN_ID` is 1 in this image until the robots move, so Humble nodes on
  domain 0 stay invisible. Cross-machine work needs both sides on 1.
- **On a Mac** the container is `Dockerfile.mac` (arm64, no NVIDIA, no
  Isaac ROS), started with the `docker run` in
  `isaac_ros_common/docker/README.md` under the same name; agents use
  `agent_container.sh` there too. It has gz baked
  in, no `ros2_ws` and no `admin` user, so the scripts run as root there
  (`scripts/container.sh`). It has no display: benches drop the gz and
  rviz windows and you watch in Foxglove, `ws://<Mac tailscale IP>:8765`.
  The host tmux session `keepalive` (`scripts/mac-keepalive.sh`) carries the
  Mac's docker.sock forward and that Foxglove forward. Killing it
  cuts `docker` off; re-run the script instead.
- **A fresh container has no gz-sim.** Before any `sim` launch, run once:
  `dexec.sh -r -- src/isaac_ros_common/docker/scripts/install-sim.sh`.
  Background it and budget minutes: it pulls a few hundred apt packages. A
  foreground call that times out gets SIGKILLed and leaves gz installed but
  `sim` unbuilt, which then fails in a way that looks unrelated. Re-running
  is safe.

## Two workspaces: `ros2_ws` silently shadows your `src/` edits

Read this before concluding an edit "had no effect", and before trusting a
measurement taken after one. Two overlapping colcon workspaces exist, and
which one wins depends on the entry point:

| entry point | sources | resolves to |
|---|---|---|
| the user's terminal | `/etc/bash.bashrc`, which ends by sourcing **only** `ros2_ws/install` | the image-baked snapshot of `src/` |
| `dexec.sh` | bashrc, then `ros2_ws`, then `isaac_ros-dev` (prepended, wins) | your `src/` edit, if built locally |

The per-package resolution measured on the Humble image (2026-09-06) is in
[reference.md](reference.md#two-workspaces-workspacesros2_ws-silently-shadows-your-src-edits);
`smoke.sh` step 4 reprints it for the live container.

So the same `ros2 launch` runs different code depending on where it's typed,
and a package built only into `isaac_ros-dev` is invisible from the user's
terminal. Nothing warns you. **Always check through the entry point you will
launch from:**

```bash
dexec.sh -- ros2 pkg prefix sentry_localization
# /workspaces/ros2_ws/install/...       -> your src/ edit is NOT live
# /workspaces/isaac_ros-dev/install/... -> your src/ edit IS live
```

Also: the running image can lag `Dockerfile.thornbots` and the submodules.
Its tag hashes only the Dockerfiles, so `isaac-ros activate` keeps starting
an image built before your package edits. `dexec.sh -- ls
/workspaces/ros2_ws/src` is the only ground truth for what's baked in.
reference.md has the EKF postmortem this cost and the recipe for testing an
edit against the shadowing copy.

## DDS discovery: the default profile

`/etc/fastdds/profile.xml` (source `isaac_ros_common/docker/fastdds_cable.xml`)
uses SIMPLE discovery, so nodes on one machine find each other with no env
changes, and lists the robots' tailscale IPs as unicast initial peers for
cross-machine work. Don't unset it. Its recorded invariants were measured on
Fast DDS 2.6 (Humble); Jazzy ships 2.14 and they are due a re-measure
([ROADMAP T38](../../../docs/ROADMAP.md#later-needs-a-robot)).

Two things in that file look removable and aren't: the `239.255.0.1` peer
(without it local discovery breaks, the 2026-07-20 postmortem) and
`maxInitialPeersRange` 32 (at the default 4, remote nodes past participant ID
3 are never found). A new robot needs its tailscale IP added there.

**Shared memory is on. On a robot, logind must not delete it.** The
2026-09-20 note that SHM hides nodes from a robot shell (1 of 15 in `ros2 node
list`) was most likely logind's `RemoveIPC=yes`; the mechanism and the fix are
in [isaac-ros-startup's README](../../../isaac-ros-startup/README.md#design-notes).
A process started by `docker exec` into the running stack still finds few or
none, which `isaac-ros-startup/AGENTS.md` lists as open (2026-10-03). If it
reappears, check `ls /dev/shm | grep -c fastrtps` against a node's
`grep -c fastrtps /proc/<pid>/maps`: mapped but missing means deleted.

`auto.launch.py` still pins the small high-level publishers
(`dji_serial_bridge`, `pose_translator`, `odom_tf_broadcaster`,
`robot_state_publisher`, `target_tracker`, `point_to_cv_target`) to
`thornbots_pkg/config/fastdds_udp_only.xml`, and
`dds_transport:=udp_only` puts every node that file launches on UDP (not
`sentry_localization`'s nodes or the camera launch). One-off CLI calls can borrow the profile:

```bash
export FASTRTPS_DEFAULT_PROFILES_FILE=$(ros2 pkg prefix thornbots_pkg)/share/thornbots_pkg/config/fastdds_udp_only.xml
```

`sentry_localization` keeps its own copy of the same profile for
`passthrough_odom_publisher`; the two have diverged (neither the peers list nor
the name match). Change one, check the other.

## Helper scripts, never hand-rolled `docker exec`

`dexec.sh` and `kill_launch.sh` get the error-prone parts right: full env
parity (both workspace installs, and `PS1` set *before* sourcing
`/etc/bash.bashrc`, which is interactive-only and silently no-ops without
it), `-u admin` so X11 apps work, and stopping only verified container-owned
ROS launch/run trees.

```bash
isaac_ros_common/scripts/dexec.sh -- ros2 topic list
isaac_ros_common/scripts/dexec.sh -r -- apt-get install -y ros-jazzy-foo
isaac_ros_common/scripts/dexec.sh -d -- ros2 launch sim sim.launch.py   # detached; prints log path
isaac_ros_common/scripts/kill_launch.sh -l                              # owned ROS roots only
isaac_ros_common/scripts/kill_launch.sh --match sim.launch.py            # stop matching owned trees
isaac_ros_common/scripts/kill_launch.sh <ros2-launch-pid>               # stop this container-owned tree
```

Never loop over raw process listings or use `-f` (removed). PID 1 and foreign
processes are refused even with `--pid=host`; see
[safety and requirements](../../../isaac_ros_common/README.md#safe-launch-stopping).

Two traps with their own reference.md sections: **never interpolate a file
list into `dexec.sh -- bash -c "…"`** (every path after the first executes as
a command; this once started a four-minute sim stack nobody launched), and
**run source-rewriting scripts inside the container** (host python 3.14 vs
container 3.12 can disagree on what parses). Host `/tmp` is not the
container's `/tmp`, and `TaskStop` kills only the host-side job.

## Before and after any test or sim launch

Check for a live session first, since a collision corrupts measurements
silently rather than erroring:

```bash
dexec.sh -- ps aux | grep -E 'gz sim|slam_toolbox|amcl|map_server|ekf_filter_node|pose_translator|pose_emulator|ros2 launch' | grep -v grep
```

If something is running, **ask before touching it**; it may be the user's own
work. Afterwards, tear down what you started (`kill_launch.sh <pid>`, or
a `sim::LaunchTree` that goes out of scope for ad hoc C++: its destructor SIGINTs, then SIGKILLs, the whole process group) and re-run the
check. reference.md covers the official suites and the `--headless` flag.

## Troubleshooting quick hits

- `ros2 topic list` nearly empty, `hz`/`echo` hang, `tf2_echo` says the frame
  doesn't exist, rviz Fixed Frame empty → the DDS profile, above, or a
  `ROS_DOMAIN_ID` mismatch (this image is on 1).
- Every drift scenario fails `stack NOT ready` → one possibility is a stale
  DDS profile; check `/etc/fastdds/profile.xml` against the DDS section.
- Nodes visible from another machine but not from a shell on the robot, or a
  lifecycle manager losing a heartbeat → Fast DDS SHM files deleted by
  logind (`RemoveIPC`). See the DDS section.
- An edit "had no effect" → two workspaces, above. `ros2 pkg prefix <pkg>`.
- `ros2 launch sim ...` can't find gz plugins, or `dexec.sh -- bash -c
  'command -v gz'` is empty → `install-sim.sh` hasn't run in this container.
  `gz` lives under `/opt/ros/jazzy/opt/gz_tools_vendor/bin` and is on `PATH`
  only after sourcing ROS, which `dexec.sh` does.
- No `nvidia-smi` or `libcuda.so.1` in the container, gz headless segfaults
  in `Ogre2RenderEngine::CreateRenderSystem`, or rviz/gz run on `llvmpipe`
  → the host's `/etc/cdi/nvidia.yaml` is stale, so `--gpus all` mounted no
  driver libraries. Ask the user to run `sudo nvidia-ctk cdi generate
  --output=/etc/cdi/nvidia.yaml` and restart the container. Results taken
  in that state rendered in software; re-run them.
- rviz shows `No tf data. Frame [map] does not exist` after a bare
  `ros2 launch sim sim.launch.py` → by design. `sim` no longer runs
  `robot_state_publisher`; `thornbots_pkg`'s `auto.launch.py` owns TF.
- Screenshotting a container GUI → prefer the host's window-scoped
  `~/.config/sway/screenshot-app.sh app <tag> RViz <out.png>`, and take it
  twice: GL windows come back solid black on the first capture.
- `dexec.sh` says the container is not running while `docker ps` shows one →
  it's under another name. Check `container_name` in
  `.isaac-ros-cli/config.yaml`, or set `ISAAC_ROS_CONTAINER`.
- `isaac-ros activate` started a stock image with no `ros2_ws` → the CLI found
  none of our config: `ISAAC_ROS_WS` pointed at another workspace, or
  `setup_workspace.sh` never ran. reference.md lists where it looks.
- GUI app fails with X11/Qt/xcb "could not connect to display" → it ran as
  root, whose `$HOME=/root` has no `.Xauthority`. Use `dexec.sh` (`-u admin`).
- rviz "no Qt platform plugin" and `echo $DISPLAY` empty in the container →
  it was activated from a shell with no `DISPLAY`. Prefix the command with
  `env DISPLAY=:2` (`ls /tmp/.X11-unix`), or re-activate from the desktop.
- A TF/topic problem unreproducible from `docker exec` but real in the user's
  terminal → that session never loaded `FASTRTPS_DEFAULT_PROFILES_FILE`. Use
  `dexec.sh`.
- Topics from another machine over tailscale never arrive → one side's
  `fastdds_cable.xml` must list the other's tailscale IP, and both need
  the same `ROS_DOMAIN_ID`.
- "not a member of docker group" → `sudo usermod -aG docker $USER && newgrp docker`

Profile changes need an image rebuild (the user's call, see reference.md)
plus `ros2 daemon stop && ros2 daemon start`; don't re-blame
`RMW_FASTRTPS_PUBLICATION_MODE`, a settled red herring (reference.md).

Don't guess at flags. Read the script, or the CLI source, if something here
doesn't match what you observe.
