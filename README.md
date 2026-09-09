# thornbots_workspace

Workspace-level docs and config for the Thornbots Sentry robot's `isaac_ros-dev/src` directory (mounted into the Isaac ROS Docker dev container).

This repo tracks the files that live at the `src/` root and don't belong to any individual package. Each package under `src/` is a git submodule pointing at its own repo, so a full checkout is:

```sh
git clone --recurse-submodules https://github.com/Thornbots/thornbots_workspace.git src
```

Most packages track `main`; `rf2o_laser_odometry` tracks `ros2` and `isaac_ros_common` tracks `release-3.2`. `.gitmodules` records the branch for each. A plain `git submodule update --init` checks out a detached HEAD, so before committing inside a package:

```sh
git submodule foreach --recursive \
  'git checkout $(git config -f $toplevel/.gitmodules submodule.$name.branch)'
```

Changing a package takes two commits: one in the package repo, one here to bump the gitlink. `Dockerfile.thornbots` builds from the `src/` directory rather than cloning from GitHub, so the image bakes whatever the submodules are checked out at. Your own builds pick the change up either way; a stale gitlink means everyone else's clone builds the old code, and a `git submodule update` on your box rewinds the package to the stale commit.

## Submodules

| Path | Branch | Role |
| --- | --- | --- |
| `thornbots_pkg` | `main` | Hardware interface, URDF, CV target selection, `auto.launch.py` |
| `sentry_localization` | `main` | SLAM / AMCL / EKF backends |
| `sim` | `main` | gz-sim worlds and the localization test suite |
| `realsense-yolov8-nitros-bridge` | `main` | YOLOv8 detection over the RealSense stream |
| `Realsense_ROI_Depth_Rectifier` | `main` | Depth rectification for detection ROIs |
| `ros2_dji_serial_bridge` | `main` | Serial link to the DJI Type-C main control board |
| `sllidar_ros2` | `main` | Slamtec RPLIDAR driver (vendored fork) |
| `rf2o_laser_odometry` | `ros2` | Scan-matched odometry (vendored fork) |
| `isaac_ros_common` | `release-3.2` | NVIDIA Isaac ROS base, plus our Dockerfiles and container scripts |

## Contents

- **`CLAUDE.md`**: workspace overview and pointers for AI-assisted work
- **`ARCC_2026_SENTRY_CONTEXT.md`**: distilled ARCC 2026 competition rules
- **`.dockerignore`**: build context for `isaac_ros_common/docker/Dockerfile.thornbots`, which is rooted here
- **`.claude/`**: Claude Code settings and skills for this workspace
