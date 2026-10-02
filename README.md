# thornbots_workspace

The `src/` root of the Thornbots Sentry's Isaac ROS dev workspace.

`main` is on ROS 2 Jazzy and Isaac ROS 4.6. The `humble` branch here and in
every package holds the Humble tree, **frozen since 2026-09-27**: it takes no
more work, and stays only for robots not yet reflashed to JetPack 7.2.

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

One logical change, one bump: a bump may move several gitlinks when they belong
to the same change, and a one-line package commit still earns its own. Push the
package before you push here — a gitlink pointing at an unpushed commit fails
everyone else's `git submodule update --init`.

| Path | Branch | Role |
| --- | --- | --- |
| `thornbots_pkg` | `main` | Hardware interface, URDF, CV target selection, `auto.launch.py` |
| `sentry_localization` | `main` | SLAM / AMCL / EKF backends |
| `sim` | `main` | gz-sim worlds and the localization test suite |
| `realsense-yolov8-nitros-bridge` | `main` | YOLOv8 detection on the RealSense stream |
| `Realsense_ROI_Depth_Rectifier` | `main` | Depth rectification for detection ROIs |
| `ros2_dji_serial_bridge` | `main` | Serial link to the DJI Type-C board |
| `sllidar_ros2` | `main` | RPLIDAR driver (fork) |
| `rf2o_laser_odometry` | `ros2` | Scan-matched odometry (fork) |
| `isaac_ros_common` | `main` | Isaac ROS base, our Dockerfiles and container scripts |
| `isaac-ros-startup` | `main` | systemd service that starts the robot stack at boot |
| `firmware/MCBV3` | `newMain` | MCB firmware, opt-in: not cloned by default, see below |

Root files: `ARCC_2026_SENTRY_CONTEXT.md` (competition rules), `ROADMAP.md` (where the project is going), `CV_SPLIT_PLAN.md`, `E2E_PLAN.md` and `JAZZY_PLAN.md` (the plans behind ROADMAP.md's tracks: world-frame aim, match test and speed, Jazzy on the robots), `JAZZY_FLASH.md` (the Orin reflash runbook, JAZZY_PLAN.md step 1), `CLAUDE.md` and `.claude/` (agent config), `.dockerignore` (build context for `Dockerfile.thornbots`).

### MCB firmware

`firmware/MCBV3` is the MCB team's repo, so a wire change and its firmware half can be checked together. It's `update = none` in `.gitmodules`: `clone --recurse-submodules` and `submodule update --init` skip it, so the robots never fetch it. `firmware/COLCON_IGNORE` and `.dockerignore` keep it out of colcon and the image. To get it, with its own taproot submodules:

```sh
git submodule update --init --checkout firmware/MCBV3
git -C firmware/MCBV3 submodule update --init --recursive
```
