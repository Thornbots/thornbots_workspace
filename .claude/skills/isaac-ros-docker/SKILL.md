---
name: isaac-ros-docker
description: Load to run, launch, attach to, drive, screenshot, rebuild, or troubleshoot the isaac_ros-dev Isaac ROS Docker container, and before running `docker exec`, `colcon build`, or `ros2 launch`/`run`/`topic` against it, even if the user never says "docker". Covers the attach-only rule, `smoke.sh`, `dexec.sh`/`kill_launch.sh`, the two-workspace shadowing trap, and the DDS discovery profile.
---

# Isaac ROS Docker dev container (Jazzy)

Drive it with `smoke.sh` and `dexec.sh`. Paths here are relative to the
workspace's `src/`. `reference.md`, next to this file, has the long version
of every section below: the `isaac-ros` flag catalogue, where the CLI reads
its config, the manual equivalents of the helper scripts, and the dated
postmortems.

> **On this laptop, never create a container, and never build the image.
> Attach only.** Remote boxes (`ts-nano-*`) are exempt when the user asks:
> there, start, stop, build and remove as asked (`../../../CLAUDE.md`
> § Containers). The rest of this block is about the laptop.
>
> Run commands *inside* a container the user already started (`smoke.sh`,
> `dexec.sh`, `kill_launch.sh`), and nothing else.
>
> Forbidden, though each looks harmless: `isaac-ros activate` in **any**
> form (`--build-local`, `--build`, `--build-only`, `--start-only`,
> `--use-cached-build-image`, `-c ...`), `isaac-ros init`, the CLI's
> `run_dev.py` and `build_image_layers.py` called directly, `docker build`,
> `docker buildx bake`, and a hand-rolled `docker run`. That includes
> wrapping any of them in `tmux`/`script` to get past the TTY requirement.
> `--build-only` still builds; `--start-only` still does the `docker run`.
>
> **If no container is running, stop and ask the user to start one.** Not
> even "just to check something": the container runs with `--rm`, dies with
> the shell that started it, and a later `isaac-ros activate` silently
> attaches to yours instead of starting the one the user wanted. When a
> rebuild is needed, make the edit, hand them the command, stop.

## Is a container running?

```bash
docker ps --format '{{.Names}}\t{{.Status}}'
# isaac_ros_jazzy_container    Up 13 seconds
```

The name comes from `docker.run.container_name` in
`isaac_ros_common/.isaac-ros-cli/config.yaml`. Nothing listed means you stop
and ask the user to run, on the host:

```bash
export ISAAC_ROS_WS=~/workspaces/isaac_ros-jazzy   # the workspace holding this src/
isaac-ros activate
```

`smoke.sh` and `dexec.sh` both preflight this. The frozen Humble container,
`isaac_ros_dev-x86_64-container`, may run beside it; don't work there. The
scripts on this branch never pick it; `ISAAC_ROS_CONTAINER=<name>` overrides.

## Driving it: `smoke.sh`

```bash
.claude/skills/isaac-ros-docker/smoke.sh          # container? mount? env? pkg resolution? graph?
.claude/skills/isaac-ros-docker/smoke.sh --sim    # + headless sim launch, topic check, teardown
```

Run it before trusting any measurement in this container. It never creates
one. Step 4 prints the package-resolution table through both entry points,
the fastest way to see whether your edit is the code that will run; step 6
refuses to launch on top of a session someone else started; `--sim` tears
down with `kill_launch.sh`.

`--sim` passes `gui:=false`, which drops only the gz window. **rviz** has its
own `rviz:=` argument, on by default when a display is reachable, so a window
still opens on the user's display.

## Key facts

- The user's entry point is `isaac-ros activate` on the host. Yours is
  `dexec.sh` against the container they started.
- The image is `isaac_ros` -> `realsense` (both shipped by `isaac-ros-cli`)
  -> `isaac_ros_common/docker/Dockerfile.thornbots`. Ubuntu 24.04, ROS 2
  Jazzy, Isaac ROS 4.6, Python 3.12.
- The **whole** host workspace root is bind-mounted, not just `src/`:
  `$ISAAC_ROS_WS` to `/workspaces/isaac_ros-dev`, so `build/`, `install/`,
  `log/` and `src/` are shared and colcon artifacts outlive the container.
  Packages are at `/workspaces/isaac_ros-dev/src/<pkg>`; a path missing that
  `src/` resolves to nothing instead of erroring.
- `ROS_DOMAIN_ID` is 1 in this image until the robots move, so Humble nodes on
  domain 0 stay invisible. Cross-machine work needs both sides on 1.
- **On a Mac** the container is `Dockerfile.mac` (arm64, no NVIDIA, no
  Isaac ROS), started with the `docker run` in
  `isaac_ros_common/docker/README.md` under the same name. It has gz baked
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

Measured on the Humble image 2026-09-06 (`smoke.sh` step 4 reprints this for
the live container):

| package | `dexec.sh` | user's terminal |
|---|---|---|
| `sim` | `isaac_ros-dev` | **Package not found** |
| `thornbots_pkg` | `isaac_ros-dev` | **Package not found** |
| `sentry_localization` | `isaac_ros-dev` | `ros2_ws` (shadowed) |
| `sllidar_ros2` | `ros2_ws` | `ros2_ws` |

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
(JAZZY_FLASH.md#hardware-checklist).

Two things in that file look removable and aren't: the `239.255.0.1` peer
(without it local discovery breaks, the 2026-07-20 postmortem) and
`maxInitialPeersRange` 32 (at the default 4, remote nodes past participant ID
3 are never found). A new robot needs its tailscale IP added there.

**Shared memory is on. On a robot, logind must not delete it.** The 2026-09-20
note that SHM hides nodes from a robot shell (1 of 15 in `ros2 node list`) was
most likely logind's `RemoveIPC=yes`: 10 s after the last ssh session of
UID 1000 ends, logind deletes that UID's `/dev/shm` files, Fast DDS's
segments included, and same-host nodes stop hearing each other, the
localization lifecycle too. With `RemoveIPC=no` (`isaac-ros-startup`
`install.sh`, 2026-10-01) a robot shell saw all 15 nodes; a process started by
`docker exec` into the running stack still finds few or none, which
`isaac-ros-startup/AGENTS.md` lists as open (2026-10-03). If it reappears,
check `ls /dev/shm | grep -c fastrtps` against a node's
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
it), `-u admin` so X11 apps work, and killing a launch's whole process group.

```bash
isaac_ros_common/scripts/dexec.sh -- ros2 topic list
isaac_ros_common/scripts/dexec.sh -r -- apt-get install -y ros-jazzy-foo
isaac_ros_common/scripts/dexec.sh -d -- ros2 launch sim sim.launch.py   # detached; prints log path
isaac_ros_common/scripts/kill_launch.sh -l                              # running launch trees
isaac_ros_common/scripts/kill_launch.sh <ros2-launch-pid>               # clean shutdown, not pkill
```

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
`teardown_stack()` in a `finally` block for ad hoc scripts) and re-run the
check. reference.md covers the official suites and the `--headless` flag.

## Troubleshooting quick hits

- `ros2 topic list` nearly empty, `hz`/`echo` hang, `tf2_echo` says the frame
  doesn't exist, rviz Fixed Frame empty → the DDS profile, above, or a
  `ROS_DOMAIN_ID` mismatch (this image is on 1).
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
