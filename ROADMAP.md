# Where the project is going

Prove the firmware-driven CV stack end to end in sim, then improve estimation
accuracy and validate the same stack on the robots. This file owns open work;
usage, design and measurements stay in the linked package docs and investigations.

## Where we actually are

| Area | Status | Maintained home / evidence |
| --- | --- | --- |
| Localization | Recorded native passes; startup race open (T30) | [Drift](sim/README.md#localization-drift-suite), [EKF](sim/README.md#ekf-ground-truth-suite), [native validation](https://github.com/Thornbots/sim/commit/4e9445a6c1be7562e188d70a94435a47bad8043d) |
| Estimation | Accuracy work open (G) | [Bench](sim/README.md#run-the-tests), [dated baseline](sim/docs/cv-bench-results-2026-09-28.md) |
| Firmware / CV | Board stages verified at diagnostic tier; accuracy open (A) | [Type C execution](sim/README.md#type-c-board-execution-with-renode), [board verification](sim/docs/mcb-auto-drive-2026-10-12.md) |
| Robots | Flashing and acceptance remain (C) | [Hardware status](JAZZY_FLASH.md#hardware-status) |

## Short todos

T-numbers and track letters are stable identifiers. Repository administration
can proceed independently of the sim work.

- **T31 — bridge / MCBV3, open:** decide hit-turn permission per frame (the
  user, 2026-10-04). Clear it while holding a valid `TargetState`, including
  the Jetson patrol's hit turn. Establish hit-angle units/reference and latch
  hits until REF_SYS reports them; test nonzero head and chassis yaw before
  trusting the sign. [Firmware coordination](ros2_dji_serial_bridge/README.md#where-the-firmware-stands).
- **T35 — MCBV3, not ready:** move the default branch from `newMain` to
  `main`, then retire `newMain` (the user, 2026-10-10).
  [Repository](https://github.com/Thornbots/MCBV3), [branch policy](AGENTS.md#branches).
- **T36 — repository admins, blocked on admin access:** lock `humble`
  read-only in Realsense_ROI_Depth_Rectifier, isaac-ros-startup,
  realsense-yolov8-nitros-bridge and ros2_dji_serial_bridge. Apply the workspace's
  “Archive humble (read-only)” [ruleset](https://github.com/Thornbots/thornbots_workspace/rules/24850059).

## Tracks, in order of work

Sim first; robot work waits (the user, 2026-10-08). Address T31, then A,
then G, then the sim parts of B and C. D supports A in parallel. E, F, H
and J are unscheduled; their robot checks join [later](#later-needs-a-robot).
Navigation waits until after the Midwest competition.

### A. The match test

Owner: sim and thornbots_pkg. Open: calibrated combat accuracy and repeatability.
Stage definitions and scoring live in [E2E_PLAN](E2E_PLAN.md); current board
acceptance is in the [dated verification](sim/docs/mcb-auto-drive-2026-10-12.md).

- **T17 — open:** identical inputs should produce nearly identical scores
  (the user, 2026-09-28). Finish the consumption-chain, UART-in-sim-time and
  deterministic bring-up work in [E2E_LOCKSTEP_PLAN](E2E_LOCKSTEP_PLAN.md#order-and-done-when).
  Check detection timing/stamps, lost tracks and `odom_disagreement_m` before
  tuning the tracker. Repeat the full parked-cell sweep on the board backend;
  the [hosted baseline](sim/docs/match-check-2026-10-11.md#parked-cells) is not
  current board acceptance.
- **Combat floors — open:** `mcb_drive` and `mcb_match` can pass diagnostic
  completion with zero hits when a miss diagnosis is present. Add calibrated
  hit-rate gates and resolve aim/frame and driving localization errors.
  [Diagnostic design](sim/README.md#driving-and-combat-diagnostics-mcb_drive).

### G. Estimation accuracy

Owner: thornbots_pkg and sim. Open; tuning follows end-to-end functionality
(the user, 2026-09-29). [Tracker design](thornbots_pkg/README.md#target_tracker)
and [dated observations](sim/docs/cv-bench-results-2026-09-28.md) own the rationale.

- **G.1 — open:** reduce radius/spin-rate outliers; test lower radius process
  noise and an armor-radius prior, with innovation logs around spin misreads.
- **G.2 — open:** tune radial depth noise with ray covariance and repair
  staggered-panel handoff/parity after blackouts.
- **G.3 — open:** gate fresh-track validity on settling, rather than update
  count; compare track age and facing-panel residual gates and their aiming cost.
- **T15 — open:** fix yaw/radius loss for angled stationary targets, then add
  limits to the default `stationary45` cells. [Bench limits](sim/README.md#run-the-tests).
- **T7 — open:** sweep acceleration process noise against velocity error,
  including path ends. [Tracker](thornbots_pkg/README.md#target_tracker).
- **T8 — open:** compare cells run alone with cells run in sequence.
  [Estimation bench](sim/README.md#run-the-tests).

Score each accuracy change over three runs in its own commit. Tighten limits
against the new worst runs and require every cell to pass; radial/blackout
error must stay within 1.5x of baseline, and fresh tracks must not become valid before facing-panel error
settles below 5 cm. Keep before/after measurements in commits.

### B. Hit while we move

Owner: thornbots_pkg, bridge and MCBV3. Open; hardware checks wait (the user,
2026-10-08), while moving-shooter bench runs can proceed in sim. After A scores,
coordinate remaining firmware work using the [shared aim frame](ros2_dji_serial_bridge/README.md#shared-aim-frame)
and [CV interface](thornbots_pkg/README.md#cv-interface).

- **Hardware validation — pending:** deploy matching ROS/firmware revisions;
  verify the shared frame and RELOCALIZE mailbox loss under CV traffic.
- **Timing — unmeasured:** measure USB/read buffering, MCB sample-to-send
  delay and camera stamp-to-capture latency; verify stamps survive YOLO and
  set the residual latency parameters. [Stamp contract](ros2_dji_serial_bridge/UART_PROTOCOL.md#mcb--jetson),
  [tracker timing](thornbots_pkg/README.md#target_tracker).
- **Chase settling — unmeasured:** measure the gimbal's chase jump and set
  settling time. [Aimer](thornbots_pkg/README.md#point_to_cv_target).
- **Moving shooter — open:** run radial/diagonal aiming-bench paths and add
  missing floors. Each moving match segment must finish within 10 percentage
  points of the same target cell with our robot parked. [Bench](sim/README.md#run-the-tests).

### C. Jazzy on the robots

Owner: startup, common package, bridge and MCBV3. Open; flashing and hardware
acceptance wait (the user, 2026-10-08). The [hardware checklist](JAZZY_FLASH.md#hardware-checklist)
owns deployment checks and the unavailable Humble comparison. T20/T25 can
land first with emulator validation; boot measurement is [T34](#later-needs-a-robot).

- **T20 — open:** improve robot logs (the user, 2026-10-01). Move/throttle
  per-frame bridge INFO logs, CRC and rf2o scan warnings; publish bridge DIAG
  statistics on `/diagnostics`, and test free-space-based pruning of per-run
  bags. [Bridge diagnostics](ros2_dji_serial_bridge/README.md#diagnostics),
  [run logging](isaac-ros-startup/README.md#use).
- **T25 — design open:** expose arbitrary MCB state in a bagged ROS message
  (the user, 2026-10-03). Decide fixed struct versus tagged fields, rate and
  UART bandwidth; specify and implement it in firmware and bridge.
  [Wire contract](ros2_dji_serial_bridge/UART_PROTOCOL.md#message-types).
- **T29 — decision open:** make robot image updates faster (the user,
  2026-10-03). Decide whether [published images](docs/CI.md#robot-registry)
  replace on-robot builds; robot pulling remains unverified. If local builds
  stay, evaluate export compression, apt layers/cache, colcon ccache and
  incremental overlays. Compare USB delivery with the untested reverse-SSH
  path. [Image workflow](isaac_ros_common/docker/README.md#on-the-x86-laptop).

### D. Faster suites

Owner: sim. Open: identify the full-stack RTF bottleneck and render only
scored inputs. Speed work and acceptance live in [E2E_PLAN](E2E_PLAN.md#speed);
remaining lockstep gates live in [E2E_LOCKSTEP_PLAN](E2E_LOCKSTEP_PLAN.md#order-and-done-when).

### E. Benches that start and stop cleanly

Owner: sim, localization and startup. Open: every bench must start with one
command, diagnose missing gz, wait for readiness, and stop all owned nodes
on completion, Ctrl-C or shell death without tracebacks or orphans.
[Suite lifecycle](sim/README.md#more-on-the-tests).

- **T30 — open:** fix missing `root` TF and localization lifecycle stalls
  at bring-up; do not rely on the suite's single retry to hide them.
  [Localization launch](sentry_localization/README.md#launchlocalizationlaunchpy).
- **Teardown — open:** resolve Fast DDS reader/participant races, obtain a
  matching-library aarch64 scan-bridge backtrace, and handle nodes/gz that
  need SIGKILL. [Shutdown findings](sim/docs/mcb-hosted-check-2026-10-11.md#shutdown-findings),
  [later board/hosted observations](sim/docs/mcb-auto-drive-2026-10-12.md).
- **Launch paths — open:** make direct launches diagnose missing gz and
  verify interruption cleanup, including children outside `kill_launch.sh`'s
  view. [Build prerequisite](sim/README.md#build).
- **T24 — cleanup open:** use one name across each launch, test and doc
  (the user, 2026-10-03): `localization_drift`, `ekf`, `aim`, `tracking`.
  Keep the `mcb_*` stage names; retire E1–E4 and Part 1/Part 2 references,
  including the Docker skill's reference. [Current names](sim/README.md#more-on-the-tests).

### F. CV nodes into their own repo

Owner: thornbots_pkg and workspace. Deferred (the user, 2026-10-02): move
selector, tracker, aimer/patrol, their cores and tests into `thornbots_cv`.
Keep hardware, URDF/TF and relay in thornbots_pkg. Update launch/test callers,
submodule and image build together; rerun both CV benches between bench runs.
[Node ownership](thornbots_pkg/README.md#nodes), [integration](docs/CI.md#coordinated-package-integration).

### H. SLAM at amcl's level

Owner: sentry_localization and sim. Open: retain SLAM with EKF as an amcl
fallback, using mapping mode and one map carried across games.
[Backend design](sentry_localization/README.md#launchlocalizationlaunchpy),
[drift metrics](sim/README.md#localization-drift-suite).

- **EKF interaction — open:** test the suspected stacked lidar corrections,
  including raw odometry as slam_toolbox's odom frame; retune SLAM without
  removing EKF. [Investigation](sentry_localization/README.md#slam---use-rf2o-worse).
- **Carried map — open:** serialize after games, load at the configured field
  spawn, and expose that spawn instead of hard-coded `[0, 0, 0]`. Provide a
  quickly rasterizing pose graph; assess a pre-Battle mapping lap against the
  rules. [Map loading](sentry_localization/README.md#launchlocalizationlaunchpy).
- **T3 / game scenario — open:** run a five-minute Battle from a blank map
  with moving/spinning lidar occluders, high ground and realistic acceleration.
  Score truth error and check crossed map cells for retained robots; repeat
  three games on one carried map. [Scenario harness](sim/README.md#scenarios).
- **Localization anomalies — unverified:** rerun comparable EKF and map-based
  scenarios to establish whether the historical error increase is a regression;
  bisect the field-frame change if it reproduces. Distinguish truth error from
  `map->odom` change. [Metric definitions](sim/README.md#localization-drift-suite),
  [historical note](https://github.com/Thornbots/thornbots_workspace/blob/3b8163141f919e61b4bf5dafb857130b61d78869/ROADMAP.md#issues-found).

SLAM+EKF must pass amcl's drift scenarios and the game scenario within 0.05 m
of amcl on the same error metric. Error must not grow across carried-map games,
and maps must not accumulate robots or duplicate walls.

### J. Lidar and camera

Owner: localization and camera/CV packages. Open; robot checks wait (the user,
2026-10-08). Sim stand-ins do not establish camera or field performance.

- **T23 — open:** compare head patrol on/off for rf2o, EKF and mapping in
  sim and on the robot (the user, 2026-10-02). If it harms localization,
  evaluate lidar-driven robot search instead of continuous patrol.
  [Moving lidar](sentry_localization/README.md#contract-with-thornbots_pkg),
  [patrol](thornbots_pkg/README.md#point_to_cv_target).
- **T19 — untested:** determine whether depth is needed or colour-only
  ranging suffices (the user, 2026-10-01). [Depth input](thornbots_pkg/README.md#target_tracker).
- **T37 — unmeasured:** measure camera copy latency and CPU/GPU cost on Orin
  before choosing a zero-copy path (the user, 2026-10-11).
  [Copy boundary and options](realsense-yolov8-nitros-bridge/README.md#copy-boundary).

## Later: needs a robot

Record validation at [hardware status](JAZZY_FLASH.md#hardware-status).

- **T21 — localization / startup, pending:** collect real-floor maps and
  per-run logs/bags to judge localization over five-minute runs (the user,
  2026-10-08: practice produced no localization runs). Include an air-gapped
  boot with Wi-Fi enabled mid-run for T27. [Run artifacts](isaac-ros-startup/README.md#use),
  [map persistence](sentry_localization/README.md#launchlocalizationlaunchpy).
- **T21 shots — bridge / MCBV3, pending:** deploy matching firmware and ROS,
  then validate lit-panel depth, bridge `pose>0`, field-aligned POSE, muzzle
  speed below 25 m/s and stand firing. Driving 1 m must not trigger repeated
  RELOCALIZE every 0.3 s (the user, 2026-10-02). Use only the current wire format (the user,
  2026-10-02). Check no-target patrol with fire clear and firmware's bit-0
  firing gate (the user, 2026-10-04); T31 owns hit-turn permission.
  Measure decision-to-receipt and indexer timing, then assign latency
  compensation to one side (the user, 2026-10-04).
  [Firmware coordination](ros2_dji_serial_bridge/README.md#where-the-firmware-stands),
  [timing contract](ros2_dji_serial_bridge/UART_PROTOCOL.md#cv_target-id1--aim-point-and-fire-decision).
  First shots need eye protection and an accessible e-stop.
- **T27 — startup, mitigation unvalidated:** test a sentry boot/run with
  Wi-Fi clock synchronization. [Clock-step mitigation](isaac-ros-startup/README.md#design-notes).
- **T34 — startup, unmeasured:** time power-on through useful detections,
  CVTarget and localization on sentry, hero and standard with the rebuilt
  Jazzy image (the user, 2026-10-04). Include UEFI and GPU-loss recovery;
  cut the longest stage to meet the under-one-minute target (the user,
  2026-09-30). [Boot instrumentation](isaac-ros-startup/README.md#boot-time).

## Issues found

Owner: the named documentation packages. Open audit follow-ups:
[2026-10-06 audit](docs/audits/docs-audit-2026-10-06.md). Resolved findings
are historical evidence there, not roadmap work.

- **rf2o / common docs — open:** add human-facing fork usage and onboarding
  (#14b/#14c). [rf2o README](rf2o_laser_odometry/README.md),
  [common README](isaac_ros_common/README.md).
- **MCBV3 deployment docs — open:** replace obsolete artifact guidance and
  the dead build anchor (#14d). [Deployment README](firmware/MCBV3/isolated-deploy/README.md).
- **Sim docs — open:** shorten current instructions and separate historical
  experiments (#14f). [Sim README](sim/README.md).
- **Rules provenance — audit open:** finish the source/page audit and
  extract the missing base building specifications (#14g).
  [Unextracted sources](ARCC_2026_SENTRY_CONTEXT.md#not-yet-extracted--worth-pulling-in-later).
- **Obstacle avoidance — untested:** establish wall-impact behavior before
  demonstrating avoidance. [Motion-model limits](sim/README.md#sentry_v2urdfxacro-motion-model).
