# isaac_ros-dev workspace

ROS2 Humble workspace (this dir is `isaac_ros-dev/src`, mounted into the
Isaac ROS Docker dev container) for the "Thornbots" sentry robot project.

## Read these before doing related work

- The `isaac-ros-docker` skill (`.claude/skills/isaac-ros-docker/`) covers the
  dev container (`isaac_ros_common/scripts/run_dev.sh`), the layered
  `Dockerfile.thornbots` image, and troubleshooting. Load it before any docker
  or build task, and before running anything inside the container. Its
  `reference.md` holds the detail that used to live in `DOCKER.md`.
- `ARCC_2026_SENTRY_CONTEXT.md`: distilled competition rules for the
  autonomous Sentry robot (arena geometry, HP/heat/power limits, firing
  constraints). Read before SLAM/nav or firing-logic work in
  `sentry_pkg`/`sim`.
- Each package's `AGENTS.md` carries its own `## Open` section — the live
  TODO list for that package. Read it before continuing work there.

## Current priority

CV (computer-vision target detection/tracking) first; localization is good
enough for now. Timing-based firing logic comes after CV works. Don't
front-run firing logic while CV is still in progress unless explicitly asked.

## Coding conventions

Keep in-code comments and docstrings under 10 lines, trimmed to the interface
facts a reader needs now: topics, params, key invariants, current tuned value.
Anything longer (design rationale, tuning history, bug postmortems, usage
examples) goes in a `## Notes` section in that package's own `README.md`,
under a subheading naming the file or topic. Leave a one-line pointer like
`# see README.md for design rationale` only when the trimmed comment would
otherwise hide context a future reader needs to know exists: a tuning
war-story, an incident postmortem, a reference table.

## Packages

Every package dir below is its own git repo under the `Thornbots` GitHub org;
`src/` itself only tracks the top-level docs and `.claude/`. Commit and push
inside the package dir, not from `src/`.

Per-package agent notes live in that package's own `AGENTS.md`: build, test
and launch invocation, whether it's shadowed by `/workspaces/ros2_ws`, and its
scope boundaries. Read it before working in a package. Its `README.md` stays
the reference doc for topics, nodes and design rationale. Conventions here are
inherited, not restated there.

- `isaac_ros_common/`: NVIDIA upstream repo, Docker scripts/Dockerfiles
- `sentry_pkg/`: SLAM/autonomy for the Sentry robot
- `sentry_localization/`: localization stack (amcl/rf2o tuning, drift/jerk
  test scenarios), split out of `sentry_pkg`
- `sim/`: gz-sim simulation (ARCC_Field_2026 world)
- `realsense-yolov8-nitros-bridge/`, `ros2_dji_serial_bridge/`: sensor and
  serial driver packages
