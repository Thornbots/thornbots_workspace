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

#### 14a — Lidar README

**Status (2026-10-11):** partly resolved by [sllidar_ros2 #5](https://github.com/Thornbots/sllidar_ros2/pull/5), which fixed the `rpldiar_ros` directory typo. The `$echo`/`$source` lines in the shell setup example remain open.

sllidar README's udev recipe uses nonexistent `src/rpldiar_ros/`; its shell setup examples include `$echo` and `$source`, which are not executable commands as written.

#### 14b — rf2o README

**Status (2026-10-15):** open.

rf2o README describes the algorithm but sends all fork-specific setup, parameters and tests into AGENTS. Add a short human-facing fork usage section.

#### 14f — Simulation docs

**Status (2026-10-15):** open for the README, now about 1,700 lines; sim AGENTS is down to 59 lines.

The simulation README was over 1,100 lines and its AGENTS over 300. Current commands, interface rationale, July tuning history and September postmortems are interleaved. Split historical experiments out, and keep the running instructions and current limitations short.

#### 14g — Rules context

The rules context mixes ARCC 2026, 2024 mounting specifications, 2018 hardware dimensions, user observations and RMUC rules while acknowledging the actual 2026 base building specification has not been extracted. Label each claim's authority and exact source/page; do not present older inferred rules as verified current requirements. This is a provenance finding, not a verdict that any individual rule is false.
