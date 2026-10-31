# thornbots_workspace

The `src/` root of the Thornbots Sentry's Isaac ROS dev workspace.

`main` is on ROS 2 Jazzy and Isaac ROS 4.6. The `humble` branch here and in
every package holds the Humble tree, **frozen since 2026-09-27**: it takes no
more work; every robot now runs JetPack 7.2.1, so it is history only.
A GitHub ruleset makes it read-only (no pushes or deletion, admins
included); the repos still unlocked are listed in
[ROADMAP T36](docs/ROADMAP.md#short-todos).

`nightly` integrates changes across the workspace and all eleven package repos.
On this branch, `.gitmodules` tracks each package's `nightly` branch while
keeping exact commit pins. [CHANGELOG.md](CHANGELOG.md) records unreleased
changes to carry into `main`; update it when adding work to nightly.

## Working with submodules

Each package is a submodule:

```sh
git clone --recurse-submodules https://github.com/Thornbots/thornbots_workspace.git src
```

That checks out the exact commits this repo pins, each on a detached HEAD.
Build from that state to reproduce the workspace. To change a package, start a
branch where it stands, then rebase onto the package's `nightly` only when you
mean to take newer work:

```sh
cd thornbots_pkg
git switch -c my-change
git fetch origin && git rebase origin/nightly   # optional: move to the branch tip
```

Do not run `git checkout nightly` in every submodule: it jumps each package to
its branch tip, which can differ from the pinned commit, and nested
submodules have no configured branch.

A package change takes two commits: one in the package, one here to bump the gitlink. `Dockerfile.thornbots` builds from this directory, so your image picks up the change without the bump. Skip it and everyone else builds the old code, and your next `git submodule update` rewinds the package.

[CI and validation](docs/CI.md) covers repository checks, lint debt, and
robot images. Only `main` runs CI and builds images (`nightly` is covered by
[local checks](docs/CI.md#local-checks-for-prs-into-nightly) and the
[nightly tests](docs/CI.md#nightly-tests)); pushes to `main`
publish tested images to `ghcr.io/thornbots/isaac-ros`, using exact gitlinks.

One logical change, one bump: a bump may move several gitlinks when they belong
to the same change, and a one-line package commit still earns its own. Push the
package before you push here — a gitlink pointing at an unpushed commit fails
everyone else's `git submodule update --init`.

A change across packages can live on a branch of the same name in each, with
this repo's branch bumping the gitlinks. Follow the
[coordinated package integration procedure](docs/CI.md#coordinated-package-integration).

| Path | Branch | Role |
| --- | --- | --- |
| `thornbots_pkg` | `nightly` | Hardware interface, URDF, CV target selection, `auto.launch.py` |
| `sentry_localization` | `nightly` | SLAM / AMCL / EKF backends |
| `sim` | `nightly` | gz-sim worlds and the localization test suite |
| `realsense-yolov8-nitros-bridge` | `nightly` | YOLOv8 detection on the RealSense stream |
| `Realsense_ROI_Depth_Rectifier` | `nightly` | Depth rectification for detection ROIs |
| `ros2_dji_serial_bridge` | `nightly` | Serial link to the DJI Type-C board |
| `sllidar_ros2` | `nightly` | RPLIDAR driver (fork) |
| `rf2o_laser_odometry` | `nightly` | Scan-matched odometry (fork) |
| `isaac_ros_common` | `nightly` | Isaac ROS base, our Dockerfiles and container scripts |
| `isaac-ros-startup` | `nightly` | systemd service that starts the robot stack at boot |
| `firmware/MCBV3` | `nightly` | MCB firmware, cloned by default but optional, see below |

Start with [ROADMAP.md](docs/ROADMAP.md) for open work, robot checks and links to its plans.
[ARCC_2026_SENTRY_CONTEXT.md](docs/ARCC_2026_SENTRY_CONTEXT.md) covers competition
rules and hardware context. The [documentation ownership map](AGENTS.md#documentation)
identifies where shared information belongs; link there instead of copying it.

### MCB firmware

`firmware/MCBV3` is the MCB team's repo, so a wire change and its firmware half can be checked together. `clone --recurse-submodules` and `submodule update --init --recursive` fetch it with its taproot submodules like any other package. Nothing on the ROS side needs it: `firmware/COLCON_IGNORE` and `.dockerignore` keep it out of colcon and the image, and sim's firmware-dependent tests skip without it. To skip it, clone without `--recurse-submodules`, then:

```sh
git config submodule.firmware/MCBV3.update none
git submodule update --init --recursive
```

On an existing clone, set that config and run `git submodule deinit firmware/MCBV3`.
