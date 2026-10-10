# thornbots_workspace

The `src/` root of the Thornbots Sentry's Isaac ROS dev workspace.

`main` is on ROS 2 Jazzy and Isaac ROS 4.6. The `humble` branch here and in
every package holds the Humble tree, **frozen since 2026-09-27**: it takes no
more work, and stays only for robots not yet reflashed to JetPack 7.2.
A GitHub ruleset makes it read-only (no pushes or deletion, admins
included); the repos still unlocked are listed in
[ROADMAP T36](ROADMAP.md#short-todos).

`nightly` integrates changes across the workspace and all eleven package repos.
On this branch, `.gitmodules` tracks each package's `nightly` branch while
keeping exact commit pins. [CHANGELOG.md](CHANGELOG.md) records unreleased
changes to carry into `main`; update it when adding work to nightly.

[Nightly validation, 2026-10-06](docs/testing/nightly-2026-10-06.md) records
the tested revisions, results, coverage limits, and commands to reproduce them.
## Working with submodules

Each package is a submodule:

```sh
git clone --recurse-submodules https://github.com/Thornbots/thornbots_workspace.git src
```

That leaves every submodule on a detached HEAD. Put each back on its branch before committing:

```sh
git submodule foreach --recursive \
  'git checkout $(git config -f $toplevel/.gitmodules submodule.$name.branch)'
```

A package change takes two commits: one in the package, one here to bump the gitlink. `Dockerfile.thornbots` builds from this directory, so your image picks up the change without the bump. Skip it and everyone else builds the old code, and your next `git submodule update` rewinds the package.

[CI and validation](docs/CI.md) covers repository checks, lint debt, and
robot images. PRs into `nightly` or `main` run CI; pushes to either branch
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
| `firmware/MCBV3` | `nightly` | MCB firmware, opt-in: not cloned by default, see below |

Start with [ROADMAP.md](ROADMAP.md) for open work and links to its plans,
[JAZZY_FLASH.md](JAZZY_FLASH.md) for migration status, robot checks and reflashing.
[ARCC_2026_SENTRY_CONTEXT.md](ARCC_2026_SENTRY_CONTEXT.md) covers competition
rules and hardware context. The [documentation ownership map](AGENTS.md#documentation)
identifies where shared information belongs; link there instead of copying it.

### MCB firmware

`firmware/MCBV3` is the MCB team's repo, so a wire change and its firmware half can be checked together. It's `update = none` in `.gitmodules`: `clone --recurse-submodules` and `submodule update --init` skip it, so the robots never fetch it. `firmware/COLCON_IGNORE` and `.dockerignore` keep it out of colcon and the image. To get it, with its own taproot submodules:

```sh
git submodule update --init --checkout firmware/MCBV3
git -C firmware/MCBV3 submodule update --init --recursive
```
