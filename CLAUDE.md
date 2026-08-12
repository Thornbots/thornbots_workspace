# isaac_ros-dev workspace

ROS2 Humble workspace (this dir is `isaac_ros-dev/src`, mounted into the
Isaac ROS Docker dev container) for the "Thornbots" sentry robot project.

## Read these before doing related work

- **the `isaac-ros-docker` skill** (`.claude/skills/isaac-ros-docker/`) — how
  to build/launch/attach to the dev container
  (`isaac_ros_common/scripts/run_dev.sh`), the layered `Dockerfile.thornbots`
  image, and troubleshooting. Load it before any docker/build-related task,
  and before running anything inside the container. Its `reference.md` holds
  the long-form detail that used to live in `DOCKER.md`.
- **`ARCC_2026_SENTRY_CONTEXT.md`** — distilled competition rules for the
  autonomous Sentry robot (arena geometry, HP/heat/power limits, firing
  constraints). Read before SLAM/nav or firing-logic work in `sentry_pkg`/`sim`.
- **`SESSION_NOTES.md`** — overall goals, what's done, and currently open
  issues/TODOs for `sim`/`sentry_pkg`/`sentry_localization` (SLAM) work.
  Read before continuing that work.

## Current priority

CV (computer-vision target detection/tracking) first; localization is
considered good enough for now. Timing-based firing logic still comes after
CV works. Don't front-run firing logic while CV is still in progress unless
explicitly asked.

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

**Every package dir below is its own git repo** (all under the `Thornbots`
GitHub org) — `src/` itself only tracks the top-level docs and `.claude/`.
Commit and push inside the package dir, not from `src/`.

**Per-package agent notes live in that package's own `AGENTS.md`** — build/
test/launch invocation for that package, whether it's shadowed by
`/workspaces/ros2_ws`, and its scope boundaries. Read it before working in a
package; its `README.md` remains the reference doc (topics, nodes, design
rationale). Conventions here are inherited, not restated there.

- `isaac_ros_common/` — NVIDIA upstream repo, Docker scripts/Dockerfiles
- `sentry_pkg/` — SLAM/autonomy for the Sentry robot
- `sentry_localization/` — localization stack (amcl/rf2o tuning, drift/jerk
  test scenarios), split out of `sentry_pkg`
- `sim/` — gz-sim simulation (ARCC_Field_2026 world)
- `realsense-yolov8-nitros-bridge/`, `ros2_dji_serial_bridge/` — sensor/serial
  driver packages
