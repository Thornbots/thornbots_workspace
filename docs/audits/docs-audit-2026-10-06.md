# Documentation audit of main

Dated record (2026-10-06). Open items are tracked from [ROADMAP](../ROADMAP.md#issues-found).

Reviewed 2026-10-06 against workspace `main` at `59e5b2d`, with every package at that commit's gitlink. Findings concern main; unmerged branches, external rulebooks and upstream release claims were out of scope. No containers, robot services, simulation suites, or flashing commands were run.

The main problem was maintenance: useful explanations were copied into several documents, then one copy got updated while the others kept incompatible instructions.

## Resolved

Rechecked against package `nightly` branches on 2026-10-15; git history keeps the original findings.

- #1 Disk backup verification: backup procedures removed; standard's reflash is a clean install.
- #2 Production launch recipe: [YOLO README](../../realsense-yolov8-nitros-bridge/README.md#full-robot-pipeline).
- #3 Obsolete inference diagram: replaced by a link to the [node diagram](../../thornbots_pkg/README.md#nodes).
- #4 Firmware quickstart default robot: [MCBV3 #87](https://github.com/Thornbots/MCBV3/pull/87).
- #5 Bridge exclusivity: the [node table](../../thornbots_pkg/README.md#nodes) and bridge AGENTS now limit exclusivity to outgoing aim/relocalization.
- #6 Chassis versus `root` rationale: [sentry_localization #5](https://github.com/Thornbots/sentry_localization/pull/5).
- #7 Old bridge stamp in latency docs, #9 firmware payload growth: [thornbots_pkg #11](https://github.com/Thornbots/thornbots_pkg/pull/11).
- #8 No-target behavior: the [aimer README](../../thornbots_pkg/README.md#point_to_cv_target) separates target-aim failure from patrol output.
- #10 Branch attachment after clone: workspace README and JAZZY_FLASH step 8.
- #11 Firmware branch in README: matches `.gitmodules`.
- #12 Conflicting hardware status: one table in JAZZY_FLASH (removed 2026-10-25; see git history).
- #13 Humble internals in the YOLO README: [realsense-yolov8-nitros-bridge #4](https://github.com/Thornbots/realsense-yolov8-nitros-bridge/pull/4) and [#5](https://github.com/Thornbots/realsense-yolov8-nitros-bridge/pull/5).
- #14c Common README: fork section links the container and Mac setup ([isaac_ros_common #8](https://github.com/Thornbots/isaac_ros_common/pull/8)).
- #14d Firmware deployment docs: GitHub CI artifacts and a working build link ([MCBV3 #95](https://github.com/Thornbots/MCBV3/pull/95)).
- #14e Dockerfile 'LAYER 5' references: none remain.

## Open: supporting docs are hard to follow from a fresh checkout (#14)

This dated finding list is superseded by [ROADMAP documentation work](../ROADMAP.md#issues-found).

#### 14a — Lidar README

Live shell-example repair: [DOC14a](../ROADMAP.md#issues-found); directory typo fixed by sllidar #5.

#### 14b — rf2o README

Completed by [rf2o #23](https://github.com/Thornbots/rf2o_laser_odometry/pull/23), integrated in workspace #157.

#### 14f — Simulation docs

Live history/current-instruction separation: [DOC14f](../ROADMAP.md#issues-found).

#### 14g — Rules context

Live extraction and unpublished-source dependencies: [DOC14g](../ROADMAP.md#issues-found).
Season 2 authority/timing was integrated in workspace #153/#157; these do not complete remaining geometry extraction.
