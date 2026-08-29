# sentry_workspace

Workspace-level docs and config for the Thornbots Sentry robot's `isaac_ros-dev/src` directory (mounted into the Isaac ROS Docker dev container).

This repo tracks only the files that live at the `src/` root and don't belong to any individual package. Each package under `src/` (`sentry_pkg`, `sentry_localization`, `sim`, `isaac_ros_common`, `realsense-yolov8-nitros-bridge`, `ros2_dji_serial_bridge`, ...) is its own separate git repo and is gitignored here. Clone those independently alongside this one.

## Contents

- **`CLAUDE.md`**: workspace overview and pointers for AI-assisted work
- **`ARCC_2026_SENTRY_CONTEXT.md`**: distilled ARCC 2026 competition rules
- **`.claude/`**: Claude Code settings and skills for this workspace
