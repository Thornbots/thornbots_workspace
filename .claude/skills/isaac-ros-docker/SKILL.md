---
name: isaac-ros-docker
description: Use when the user wants to launch, attach to, rebuild, or troubleshoot the Isaac ROS dev Docker container for this workspace (isaac_ros-dev) — e.g. "start the container", "rebuild the image", "attach a shell", "docker won't build", "add a package to the image".
---

# Isaac ROS Docker dev container

Full reference: `../../../DOCKER.md` (repo-relative: `src/DOCKER.md`). Read it
if you need details beyond this summary.

## Key facts

- Entry point script: `isaac_ros_common/scripts/run_dev.sh`. Run it from
  `isaac_ros_common/scripts/`.
- Host `isaac_ros-dev/src` is bind-mounted to
  `/workspaces/isaac_ros-dev/src` in the container — source edits don't need
  a rebuild, only dependency/package changes do. **But only for packages
  that actually resolve to this workspace** — several are ALSO cloned into
  `/workspaces/ros2_ws` by `Dockerfile.thornbots`, and that copy wins. See
  "Two workspaces" below before trusting any edit you make under `src/`.
  **Not** directly at
  `/workspaces/isaac_ros-dev` — that path is the colcon workspace root
  (`build/`, `install/`, `log/`, plus `src/`), one level up from the bind
  mount. Easy to get wrong when building a path by hand (e.g.
  `/workspaces/isaac_ros-dev/isaac_ros_common/...` silently resolves to
  nothing useful instead of erroring, since `isaac_ros-dev/` itself exists —
  it just doesn't contain `isaac_ros_common/`) — confirmed by `ls
  /workspaces/isaac_ros-dev/src` inside the container if in doubt.
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

`dexec.sh` sources `ros2_ws` first, then `isaac_ros-dev` — but sourcing
second does **not** win here: `ros2_ws`'s entries come first in
`AMENT_PREFIX_PATH`, so for any package present in both, **the image-baked
GitHub clone is what launches**, not your edit.

This fails silently and looks like a real result, not a mistake. Editing
`src/sentry_localization/config/ekf.yaml` and relaunching produces a stack
running the *old* config with no warning of any kind. On 2026-07-25 this
invalidated an entire round of EKF measurements before it was noticed —
the tell was the filter output matching an input to 3 decimal places,
which is not something real fusion does.

**Always confirm which copy is live before measuring:**
```bash
dexec.sh -- bash -lc 'ros2 pkg prefix sentry_localization'
# /workspaces/ros2_ws/install/...      -> your src/ edit is NOT live
# /workspaces/isaac_ros-dev/install/... -> your src/ edit IS live

# and to see the actual file a node will load (follows symlink-install):
dexec.sh -- bash -lc 'readlink -f $(ros2 pkg prefix sentry_localization)/share/sentry_localization/config/ekf.yaml'
```

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

Start or attach (rebuilds first if no container is running; attaches if one
already is):
```bash
cd isaac_ros_common/scripts && ./run_dev.sh
```

Attach a second shell to an already-running container — just re-run
`run_dev.sh` again; it detects the running container and `docker exec`s a
shell into it instead of rebuilding/relaunching:
```bash
./run_dev.sh
```
Manual equivalent (only needed for docker exec flags `run_dev.sh` doesn't expose):
```bash
docker exec -it -u admin --workdir /workspaces/isaac_ros-dev isaac_ros_dev-x86_64-container bash
```

Launch without rebuilding the image:
```bash
./run_dev.sh -b
```

Stop the container (needed before `run_dev.sh` will rebuild):
```bash
docker stop isaac_ros_dev-x86_64-container
```

Rebuild after editing `docker/Dockerfile.thornbots` — just re-run
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

## Helper scripts (use these instead of hand-rolling docker exec)

`isaac_ros_common/scripts/dexec.sh` and `kill_launch.sh` already get the
two error-prone patterns below right (env sourcing, cleanly killing a
backgrounded launch tree) — multiple sessions/agents on this project got
them subtly wrong by hand before these existed. Prefer them:

```bash
# Correct env already sourced (both workspace installs + bash.bashrc/PS1):
isaac_ros_common/scripts/dexec.sh -- ros2 topic list
isaac_ros_common/scripts/dexec.sh -r -- apt-get install -y ros-humble-foo

# Backgrounded launch (setsid'd so kill_launch.sh can clean up the whole
# tree later, not just the launch process):
isaac_ros_common/scripts/dexec.sh -d -- ros2 launch sim sim.launch.py
# find its ros2-launch PID:
isaac_ros_common/scripts/dexec.sh -- ps aux | grep "ros2 launch" | grep -v grep
# clean shutdown of the whole tree:
isaac_ros_common/scripts/kill_launch.sh <ros2-launch-pid>
```

Set `ISAAC_ROS_CONTAINER` to override the container name if needed. The
sections below explain *why* these scripts are built the way they are —
read them if something doesn't match observed behavior, but don't
hand-roll the manual `docker exec` forms when the scripts already work.

## Testing a git worktree's changes in docker without merging first

A background session working under `bgIsolation: worktree` (the default —
see the repo's top-level `CLAUDE.md`) edits inside `.claude/worktrees/<name>/`
until the change is merged into the branch checked out at the bind-mounted
path. That doesn't mean docker can't see it in the meantime, though:
worktrees created by `EnterWorktree` live *inside* the package directory
(e.g. `sim/.claude/worktrees/<name>/`), which is itself inside the
bind-mounted `isaac_ros-dev/src` tree — so the worktree's files are already
readable inside the container at
`/workspaces/isaac_ros-dev/src/<pkg>/.claude/worktrees/<name>/...`, no merge
needed. Confirmed directly: `xacro`/`ign sdf -p` run against a worktree path
picks up its uncommitted edits immediately.

That covers one-off checks (syntax validation, `ign sdf -p` conversion
tests, reading a file to confirm a value). It does **not** cover a full
`ros2 launch`/`colcon build` run, because colcon's `--symlink-install` tree
resolves everything back to the *main checkout's* files:
`install/<pkg>/share/.../file` → `build/<pkg>/.../file` →
`src/<pkg>/.../file`. `ros2 launch`, `xacro` invoked via a package share
path, and anything `ros2 run` resolves all go through that chain, so they
see the main checkout, not the worktree, by default.

To run a full launch against a worktree's version of one file without
merging: repoint the middle (`build/`) symlink at the worktree's copy,
test, then put it back. Verified working end-to-end (confirmed both the
swap and the restore land on the right target):
```bash
# swap: point the build-stage symlink at the worktree's file
docker exec -u admin isaac_ros_dev-x86_64-container \
  ln -sfn /workspaces/isaac_ros-dev/src/sim/.claude/worktrees/<name>/urdf/sentry.urdf.xacro \
          /workspaces/isaac_ros-dev/build/sim/urdf/sentry.urdf.xacro
# ...launch/test as normal (install/sim/share/.../sentry.urdf.xacro now
# resolves through to the worktree's copy)...

# restore: point it back at the main checkout before merging or discarding
docker exec -u admin isaac_ros_dev-x86_64-container \
  ln -sfn /workspaces/isaac_ros-dev/src/sim/urdf/sentry.urdf.xacro \
          /workspaces/isaac_ros-dev/build/sim/urdf/sentry.urdf.xacro
```
Works for any `--symlink-install`ed file (urdf/xacro, world/sdf, rviz
config, `launch/*.py`), not just this one — swap whichever `build/<pkg>/...`
path corresponds to the file under test. Always restore the symlink
afterward regardless of whether the worktree change gets merged or
discarded, so the main checkout's normal install tree isn't left pointing
at a worktree that may get removed later. This doesn't help for compiled
(C++) packages or for `ros2 run`-launched Python nodes specifically (their
installed executable is a generated wrapper, not a plain symlinked file) —
for those, merge into the main branch locally first (no push needed) the
same way this session has been doing it, then test normally.

## ROS_DOMAIN_ID and general env parity — always source /etc/bash.bashrc, with PS1 set

The image sets `ROS_DOMAIN_ID=42`, `RMW_IMPLEMENTATION`, and
`FASTRTPS_DEFAULT_PROFILES_FILE` via `/etc/bash.bashrc` (see
`Dockerfile.thornbots`), and the user's own attached terminal (from
`run_dev.sh`, a true `docker run -it` login shell) picks all of it up
normally.

**`/etc/bash.bashrc` is interactive-shell-only**: it starts with `[ -z
"$PS1" ] && return`, so it silently does nothing in a non-interactive
`docker exec ... bash -lc "source /etc/bash.bashrc && ..."` unless `PS1` is
set first — sourcing it "does nothing" is easy to miss since there's no
error, just missing env vars.

**Don't just manually export `ROS_DOMAIN_ID` and call it done** — that gets
topic discovery working (misleadingly!) but silently diverges from the
user's real environment in other ways. This exact gap cost a very long
debugging session (2026-07-20): every `docker exec` test command used a
hand-rolled partial env that happened to avoid a real FastDDS bug (see
"FastDDS profile" below) that the user's actual shell always hit, making the
bug look unreproducible for a long time. **Always set `PS1` and explicitly
`source /etc/bash.bashrc`** in any `docker exec` command that touches ROS,
so the debugging session's environment always matches what the user's
terminal actually has:
```bash
docker exec -u admin --workdir /workspaces/isaac_ros-dev isaac_ros_dev-x86_64-container \
  bash -lc "export PS1='\$ ' && source /etc/bash.bashrc && ros2 topic list"
```

## FastDDS profile (`FASTRTPS_DEFAULT_PROFILES_FILE`)

`/etc/bash.bashrc` also sets `RMW_IMPLEMENTATION=rmw_fastrtps_cpp` and
`FASTRTPS_DEFAULT_PROFILES_FILE=/etc/fastdds/profile.xml` for every
interactive shell (see `Dockerfile.thornbots`'s "LAYER 8" env block; the
profile XML source is `isaac_ros_common/docker/fastdds_cable.xml`, `COPY`'d
into the image at that same path).

`<useBuiltinTransports>` **must stay `true`**. It was briefly `false` and
broke all local sim/RViz work: with builtin transports off, FastDDS's
default UDP multicast discovery and shared-memory transport are disabled
entirely, so a node using this profile can only reach explicitly-listed
peers. Symptom: `ros2 topic info <topic> --verbose` shows matching
publishers/subscribers (plain DDS discovery still partially works), but
zero messages actually flow (`ros2 topic hz`/`echo` hang forever).

**A second, sneakier bug in the same file** (found 2026-07-20, after the
above was already fixed): the profile used to also hardcode an explicit
`<initialPeersList>` unicast peer at the real robot's tethered-link IP
(`192.168.55.1`), on the theory that it was "purely additive" alongside
normal multicast discovery. It wasn't — an unreachable explicit peer
measurably broke/delayed local discovery in practice even with
`useBuiltinTransports=true`. Symptom was much broader than the first bug:
`ros2 topic list` itself would only show a couple of topics (e.g. just
`/parameter_events`/`/rosout`) instead of the full graph, `ros2 topic echo
<topic> --once` on a `TRANSIENT_LOCAL` topic like `/tf_static` would hang
or say "does not appear to be published yet", `tf2_echo` would error "frame
does not exist" and never recover, and rviz's Fixed Frame dropdown would
stay completely empty. Confirmed by testing with `initialPeersList` removed
from the profile: `ros2 topic list` went from ~2 topics to the full graph
immediately. **Fixed by removing `<initialPeersList>` entirely** — normal
multicast discovery already reaches the real robot over the tethered link
when it's actually connected, without needing to hardcode its IP as an
explicit peer.

**This bug hid for a long time because of the PS1/bash.bashrc-sourcing gap
above**: every debugging `docker exec` session that manually exported just
`ROS_DOMAIN_ID` (skipping `FASTRTPS_DEFAULT_PROFILES_FILE`) never actually
loaded the broken profile, so it always "worked" while the user's real
shell — which always sources the profile via `/etc/bash.bashrc` — always
hit the bug. If a topic/TF/rviz problem looks unreproducible from a
`docker exec` session, that's a red flag: make sure the session is actually
loading `FASTRTPS_DEFAULT_PROFILES_FILE`, not just `ROS_DOMAIN_ID`.

**Whenever this profile changes**: it needs an image rebuild
(`./run_dev.sh`, not `-b`) to reach `/etc/fastdds/profile.xml` inside the
image, *and* any already-running `ros2` daemon needs `ros2 daemon stop &&
ros2 daemon start` afterward — it caches its old (possibly broken)
participant otherwise and won't pick up the new profile on its own.

If this ever needs to be diagnosed again: compare
`FASTRTPS_DEFAULT_PROFILES_FILE`/`RMW_IMPLEMENTATION` between the suspect
process's environment (`cat /proc/<pid>/environ | tr '\0' '\n'` — reliable
for a freshly-spawned leaf process like `rviz2`, *not* reliable for a
long-running shell that `export`ed vars after starting) and a `docker exec`
session that works, and bisect the profile XML by testing with elements
removed (write a trimmed copy to `/tmp`, point `FASTRTPS_DEFAULT_PROFILES_FILE`
at it, retest `ros2 topic list --no-daemon`) rather than guessing.

## Launching GUI apps (gz sim, rviz2) via `docker exec` (not an interactive shell)

When starting a launch file that pops a GUI window (e.g. `ros2 launch sim
sim.launch.py`) from a non-interactive `docker exec` (like Claude's Bash
tool, backgrounded with `-d`), it **must** run as `-u admin`, not the
default root user:
```bash
docker exec -d -u admin --workdir /workspaces/isaac_ros-dev \
  isaac_ros_dev-x86_64-container bash -lc \
  "source /opt/ros/humble/setup.bash && source /workspaces/isaac_ros-dev/install/setup.bash && ros2 launch sim sim.launch.py > /tmp/sim.log 2>&1"
```
Root's `$HOME` is `/root`, which has no `.Xauthority` file, so any Qt/X11
app run as root fails with `Authorization required, but no authorization
protocol specified` / `could not connect to display`. The X11 auth cookie
`run_dev.sh` set up at container start lives at `/home/admin/.Xauthority`
— only reachable when `HOME=/home/admin`, i.e. running as `admin`.
`DISPLAY` itself (`:0`) is already set container-wide for any user, so this
is the only piece that needs the explicit `-u admin`.

This applies to
`sim/test/localization/run_localization_drift_tests.py` too —
GUI is its default (matches the standing "always launch `sim` with GUI,
not headless" rule in `SESSION_NOTES.md`; pass `--headless` to opt out for
a quick unattended run). Launch via `dexec.sh -d` (defaults to `-u admin`,
gets X11 right automatically) rather than a bare `docker exec -d` without
`-u admin` — the latter runs as root and the GUI window will fail to open
with an X11/Qt auth error (same failure mode as any other GUI app, see
below):
```bash
isaac_ros_common/scripts/dexec.sh -d -- \
  python3 src/sim/test/localization/run_localization_drift_tests.py
```

Before backgrounding a new launch, check for and clean up stale/duplicate
processes first (`ps aux | grep -E 'ros2|gz|ign|parameter_bridge'` in the
container) — a dead `gz sim` server can leave orphaned bridge processes
that still show up in `ros2 topic list` but never publish, and relaunching
on top of a still-running session produces duplicate/conflicting sim
instances. Use `kill_launch.sh <launch-pid>` (see "Helper scripts" above)
to clean up an old launch, not `pkill`/`killall` — and not a bare `kill
-SIGINT <pid>` either, since a backgrounded launch without a TTY doesn't
reliably forward that to its children from the launch PID alone; it needs
`SIGINT` sent to the whole process group, which is what the script does.

## Troubleshooting quick hits

- "not a member of docker group" → `sudo usermod -aG docker $USER && newgrp docker`
- LFS errors → install `git-lfs`, re-clone
- Build succeeds but "no built image found" → `CONFIG_IMAGE_KEY` doesn't
  resolve to real `Dockerfile.<suffix>` files under `isaac_ros_common/docker/`
- GUI app run via `docker exec` fails with X11/Qt/xcb errors → see "Launching
  GUI apps" above; almost always a missing `-u admin`.
- `ros2 topic list` shows almost nothing, `ros2 topic echo`/`hz` hang or say
  "does not appear to be published yet", `tf2_echo` says "frame does not
  exist" and never recovers, or rviz's Fixed Frame dropdown is empty → see
  "FastDDS profile" above (the `initialPeersList` bug) — fixed 2026-07-20,
  needs an image rebuild + `ros2 daemon stop && ros2 daemon start` to take
  effect. `RMW_FASTRTPS_PUBLICATION_MODE=ASYNCHRONOUS` was also removed from
  `Dockerfile.thornbots` around the same time (a real FastDDS
  `TRANSIENT_LOCAL`-delivery issue, worth keeping fixed) but turned out to
  be a red herring for these specific symptoms — don't assume it's the fix
  if this recurs; check the FastDDS profile first.

Don't guess at flags — run `./run_dev.sh --help` or read the script directly
if something here doesn't match observed behavior (it may have changed).
