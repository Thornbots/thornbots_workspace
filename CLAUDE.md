# isaac_ros-dev workspace

ROS2 Humble workspace (this dir is `isaac_ros-dev/src`, mounted into the
Isaac ROS Docker dev container) for the "Thornbots" sentry robot project.

## Read these before doing related work

- **`DOCKER.md`** — how to build/launch/attach to the dev container
  (`isaac_ros_common/scripts/run_dev.sh`), the layered `Dockerfile.thornbots`
  image, and troubleshooting. Read before any docker/build-related task.
- **`ARCC_2026_SENTRY_CONTEXT.md`** — distilled competition rules for the
  autonomous Sentry robot (arena geometry, HP/heat/power limits, firing
  constraints). Read before SLAM/nav or firing-logic work in `sentry_pkg`/`sim`.
- **`SESSION_NOTES.md`** — overall goals, what's done, and currently open
  issues/TODOs for `sim`/`sentry_pkg`/`sentry_localization` (SLAM) work.
  Read before continuing that work.

## Current priority

SLAM/navigation for the Sentry robot first; timing-based firing logic comes
after SLAM works. Don't front-run firing/targeting features while nav is
still in progress unless explicitly asked.

## Coding conventions

- **Keep in-code comments/docstrings under 10 lines.** Trim to just the
  interface facts a reader needs right now (topics, params, key
  invariants, current tuned value). Move anything longer — design
  rationale, tuning history, bug postmortems, long usage examples — into
  a `## Notes` section in that package's own `README.md`, under a
  subheading naming the file/topic. Leave a one-line pointer comment
  (e.g. `# see README.md for design rationale`) only when the trimmed
  comment would otherwise lose context a future reader needs to know
  exists (tuning war-stories, incident postmortems, reference tables);
  skip the pointer for plain interface docstrings with no historical
  baggage.

## Packages

- `isaac_ros_common/` — NVIDIA upstream repo, Docker scripts/Dockerfiles
- `sentry_pkg/` — SLAM/autonomy for the Sentry robot
- `sentry_localization/` — localization stack (amcl/rf2o tuning, drift/jerk
  test scenarios), split out of `sentry_pkg`
- `sim/` — gz-sim simulation (ARCC_Field_2026 world)
- `realsense-yolov8-nitros-bridge/`, `ros2_dji_serial_bridge/` — sensor/serial
  driver packages
