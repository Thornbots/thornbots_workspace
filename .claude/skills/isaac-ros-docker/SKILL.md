---
name: isaac-ros-docker
description: Load to run, launch, attach to, drive, screenshot, rebuild, or troubleshoot the isaac_ros-dev Isaac ROS Docker container, and before running `docker exec`, `colcon build`, or `ros2 launch`/`run`/`topic` against it, even if the user never says "docker". Covers the attach-only rule, `smoke.sh`, `dexec.sh`/`kill_launch.sh`, the two-workspace shadowing trap, and the DDS discovery profile.
---

# Isaac ROS Docker dev container

Drive it with `smoke.sh` and `dexec.sh`. Paths here are relative to
`isaac_ros-dev/src/`. `reference.md`, next to this file, has the long
version of every section below: `run_dev.sh`'s flag catalogue, the manual
equivalents of the helper scripts, and the dated postmortems.

> **Never create a container, and never build the image. Attach only.**
> Run commands *inside* a container the user already started (`smoke.sh`,
> `dexec.sh`, `kill_launch.sh`), and nothing else.
>
> Forbidden, though each looks harmless: `docker build`,
> `build_image_layers.sh`, `build_base_image.sh`, a hand-rolled `docker run`,
> and `run_dev.sh` in **any** form. That includes `-b`/`SKIP_DOCKER_BUILD=1`
> (skips the build, still does the `docker run`) and wrapping it in
> `tmux`/`script` to get past its TTY requirement.
>
> **If no container is running, stop and ask the user to start one.** Not
> even "just to check something": a container you create runs with `--rm`,
> dies with your shell, and makes the user's next `run_dev.sh` silently
> attach to yours instead of starting the fresh one they wanted. When a
> rebuild is needed, make the edit, hand them the command, stop.

## Is a container running?

```bash
docker ps --format '{{.Names}}\t{{.Status}}'
# isaac_ros_dev-x86_64-container    Up 13 seconds
```

Nothing listed means you stop and ask the user to run
`cd src/isaac_ros_common/scripts && ./run_dev.sh` (`-b` skips the image
rebuild). `smoke.sh` and `dexec.sh` both preflight this.

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

`--sim` passes `gui:=false`, which still starts **rviz** (`sim.launch.py`
starts rviz regardless), so a window opens on the user's display. Verified
2026-09-06: 31 fps, sim time advancing, depth panel live.

## Key facts

- The user's entry point is `isaac_ros_common/scripts/run_dev.sh`. Yours is
  `dexec.sh` against the container they started.
- Container name: `isaac_ros_dev-<uname -m>-container`. Override with
  `ISAAC_ROS_CONTAINER`.
- The **whole** host workspace root is bind-mounted, not just `src/`:
  `~/workspaces/isaac_ros-dev` to `/workspaces/isaac_ros-dev`, so `build/`,
  `install/`, `log/` and `src/` are shared and colcon artifacts outlive the
  container. Packages are at `/workspaces/isaac_ros-dev/src/<pkg>`; a path
  missing that `src/` resolves to nothing instead of erroring.
- Image key is pinned in `scripts/.isaac_ros_common-config`:
  `CONFIG_IMAGE_KEY=ros2_humble.realsense.thornbots`, layered across
  `docker/Dockerfile.{x86_64,ros2_humble,realsense,thornbots}`.
- **A fresh container has no gz-sim.** Before any `sim` launch, run once:
  `dexec.sh -r -- src/isaac_ros_common/docker/scripts/install-sim.sh`.
  Background it and budget minutes: 2026-09-06 it pulled 225 apt packages
  (the `colcon build` of `sim` at the end is 3.7s). A foreground call that
  times out gets SIGKILLed and leaves `ign` installed but `sim` unbuilt,
  which then fails in a way that looks unrelated. Re-running is safe.

## Two workspaces: `ros2_ws` silently shadows your `src/` edits

Read this before concluding an edit "had no effect", and before trusting a
measurement taken after one. Two overlapping colcon workspaces exist, and
which one wins depends on the entry point:

| entry point | sources | resolves to |
|---|---|---|
| the user's terminal | `/etc/bash.bashrc`, which ends by sourcing **only** `ros2_ws/install` | the image-baked snapshot of `src/` |
| `dexec.sh` | bashrc, then `ros2_ws`, then `isaac_ros-dev` (prepended, wins) | your `src/` edit, if built locally |

Measured 2026-09-06 (`smoke.sh` step 4 reprints this for the live container):

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

Also: the running image can lag `Dockerfile.thornbots`, so
`dexec.sh -- ls /workspaces/ros2_ws/src` is the only ground truth for what's
baked in. reference.md has the EKF postmortem this cost, the recipe for
testing an edit against the shadowing copy, and why `sim` has no shadow.

## DDS discovery: the default profile

`/etc/fastdds/profile.xml` (source `isaac_ros_common/docker/fastdds_cable.xml`)
uses SIMPLE discovery, so nodes on one machine find each other with no env
changes, and lists the robots' tailscale IPs as unicast initial peers for
cross-machine work. Don't unset it. Measured 2026-09-14: with it, the
`odom_stuck` drift scenario passed and a peer with participant ID 12 was
discovered over unicast only.

Two things in that file look removable and aren't: the `239.255.0.1` peer
(without it local discovery breaks, the 2026-07-20 postmortem) and
`maxInitialPeersRange` 32 (at the default 4, remote nodes past participant ID
3 are never found). A new robot needs its tailscale IP added there.

**UDP only, no shared memory, since 2026-09-20.** With the SHM transport in
the profile, a `ros2 node list` run in a robot shell saw 1 of 15 running
nodes while another machine saw all 15 over tailscale; same profile minus the
`shm` descriptor, 13. So a robot terminal that sees almost nothing while your
laptop sees everything is an image baked before that date. Intra-host traffic
now goes over UDP loopback, so if image topics start dropping, raise the
socket buffers in the profile *and* `net.core.rmem_max`/`wmem_max` -- the
kernel clamps silently otherwise.

`thornbots_pkg`'s `config/fastdds_no_shm.xml`, applied to three nodes via
`additional_env` in `auto.launch.py`, predates this and is now redundant:
it does the same thing for those nodes, minus the tailscale peers. Harmless,
but remove it only once every machine has rebuilt.

Containers built before 2026-09-14 bake the old discovery-server profile, where
nothing is visible until a server runs. If `ros2 topic list` shows ~2 topics,
check `grep discoveryProtocol /etc/fastdds/profile.xml`; `SUPER_CLIENT` means
the image predates the change and needs a full rebuild.

## Helper scripts, never hand-rolled `docker exec`

`dexec.sh` and `kill_launch.sh` get the error-prone parts right: full env
parity (both workspace installs, and `PS1` set *before* sourcing
`/etc/bash.bashrc`, which is interactive-only and silently no-ops without
it), `-u admin` so X11 apps work, and killing a launch's whole process group.

```bash
isaac_ros_common/scripts/dexec.sh -- ros2 topic list
isaac_ros_common/scripts/dexec.sh -r -- apt-get install -y ros-humble-foo
isaac_ros_common/scripts/dexec.sh -d -- ros2 launch sim sim.launch.py   # detached; prints log path
isaac_ros_common/scripts/kill_launch.sh -l                              # running launch trees
isaac_ros_common/scripts/kill_launch.sh <ros2-launch-pid>               # clean shutdown, not pkill
```

Two traps with their own reference.md sections: **never interpolate a file
list into `dexec.sh -- bash -c "…"`** (every path after the first executes as
a command; this once started a four-minute sim stack nobody launched), and
**run source-rewriting scripts inside the container** (host python 3.14 vs
container 3.10 tokenize f-strings differently). Host `/tmp` is not the
container's `/tmp`, and `TaskStop` kills only the host-side job.

## Before and after any test or sim launch

Check for a live session first, since a collision corrupts measurements
silently rather than erroring:

```bash
dexec.sh -- ps aux | grep -E 'ign gazebo|gz sim|slam_toolbox|amcl|map_server|ekf_filter_node|pose_translator|pose_emulator|ros2 launch' | grep -v grep
```

If something is running, **ask before touching it**; it may be the user's own
work. Afterwards, tear down what you started (`kill_launch.sh <pid>`, or
`teardown_stack()` in a `finally` block for ad hoc scripts) and re-run the
check. reference.md covers the official suites and the `--headless` flag.

## Troubleshooting quick hits

- `ros2 topic list` nearly empty, `hz`/`echo` hang, `tf2_echo` says the frame
  doesn't exist, rviz Fixed Frame empty → the DDS profile, above. Check for
  an old `SUPER_CLIENT` image first.
- Topics/nodes visible from another machine but not from a shell on the robot
  → an image baked with the SHM transport still in the profile. Confirm with
  `grep -c shm /etc/fastdds/profile.xml` (0 on a current image); until it is
  rebuilt, prefix CLI calls with
  `FASTRTPS_DEFAULT_PROFILES_FILE=$(ros2 pkg prefix thornbots_pkg)/share/thornbots_pkg/config/fastdds_no_shm.xml`.
- An edit "had no effect" → two workspaces, above. `ros2 pkg prefix <pkg>`.
- `ros2 launch sim ...` can't find gz plugins, or `command -v ign` is empty →
  `install-sim.sh` hasn't run in this container.
- rviz shows `No tf data. Frame [map] does not exist` after a bare
  `ros2 launch sim sim.launch.py` → by design. `sim` no longer runs
  `robot_state_publisher`; `thornbots_pkg`'s `auto.launch.py` owns TF.
- Screenshotting a container GUI → the container has no `import`, `scrot`,
  `convert`, or `Xvfb`, only `/usr/bin/ffmpeg`:
  `dexec.sh -- ffmpeg -y -f x11grab -video_size 1920x1080 -i $DISPLAY -frames:v 1 /workspaces/isaac_ros-dev/shot.png`
  grabs the whole desktop, so ask first. Prefer the host's window-scoped
  `~/.config/sway/screenshot-app.sh app <tag> RViz <out.png>`, and take it
  twice: GL windows come back solid black on the first capture.
- Container came up with no `src/` in `/workspaces/isaac_ros-dev` →
  `run_dev.sh` ran without `ISAAC_ROS_WS`, which lives in `~/.zshrc` and so is
  absent from non-interactive shells. It then mounts `src/` itself at the
  workspace root.
- GUI app fails with X11/Qt/xcb "could not connect to display" → it ran as
  root, whose `$HOME=/root` has no `.Xauthority`. Use `dexec.sh` (`-u admin`).
- A TF/topic problem unreproducible from `docker exec` but real in the user's
  terminal → that session never loaded `FASTRTPS_DEFAULT_PROFILES_FILE`. Use
  `dexec.sh`.
- Topics from another machine over tailscale never arrive → one side's
  `fastdds_cable.xml` must list the other's tailscale IP, and both need
  the same `ROS_DOMAIN_ID`.
- "not a member of docker group" → `sudo usermod -aG docker $USER && newgrp docker`
- LFS errors → install `git-lfs`, re-clone.
- "no built image found" → `CONFIG_IMAGE_KEY` doesn't resolve to real
  `Dockerfile.<suffix>` files under `isaac_ros_common/docker/`.

Profile changes need a full rebuild (`run_dev.sh`, not `-b`) plus
`ros2 daemon stop && ros2 daemon start`; don't re-blame
`RMW_FASTRTPS_PUBLICATION_MODE`, a settled red herring (reference.md).

Don't guess at flags. Read the script if something here doesn't match what
you observe.
