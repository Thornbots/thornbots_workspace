# Where the project is going

Prove the firmware-driven CV stack end to end in sim, improve estimation, then validate on robots. This file owns open
work; usage, design and measurements stay in linked docs.

## Where we actually are

| Area | Current evidence | Home |
| --- | --- | --- |
| Localization | Native suite passes recorded | [Drift](../sim/README.md#localization-drift-suite), [EKF](../sim/README.md#ekf-ground-truth-suite), [native validation](https://github.com/Thornbots/sim/commit/4e9445a6c1be7562e188d70a94435a47bad8043d) |
| Estimation | Bench baseline recorded | [Bench](../sim/README.md#run-the-tests), [baseline](../sim/docs/cv-bench-results-2026-09-28.md) |
| Firmware / CV | Raw aim is isolated from navigation; board stages pass diagnostic tier. Fresh Mac hosted repeats clear all spinning cells and improve every stage; three accepted board drive/match repeats improve hits over nightly | [Type C](../sim/README.md#type-c-board-execution-with-renode), [board verification](../sim/docs/mcb-auto-drive-2026-10-12.md), [accuracy repeats](../sim/docs/aim-accuracy-2026-10-12.md#spinning-correction-and-board-comparison) |
| Robots | Standard still needs the Jazzy flash; acceptance remains ([T38](#short-todos)) | [Hardware status](JAZZY_FLASH.md#hardware-status) |

## Short todos

- **T36 — repository admins — blocked on admin access:** Lock `humble` read-only in Realsense_ROI_Depth_Rectifier,
  isaac-ros-startup, realsense-yolov8-nitros-bridge and ros2_dji_serial_bridge using the workspace
  [ruleset](https://github.com/Thornbots/thornbots_workspace/rules/24850059).
- **T38 — standard — open:** Only `ts-nano-standard` still needs Jazzy: flash it per
  [Jazzy flash](JAZZY_FLASH.md#hardware-status), then run the [hardware checklist](JAZZY_FLASH.md#hardware-checklist). T20/T25 can use emulator validation.
- **T20 — startup / bridge — open:** Improve logs: throttle per-frame bridge INFO, CRC and rf2o warnings; publish bridge
  DIAG on `/diagnostics`; test free-space pruning of per-run bags.
  [Diagnostics](../ros2_dji_serial_bridge/README.md#diagnostics), [run logging](../isaac-ros-startup/README.md#use).
- **T25 — bridge / MCBV3 — design open:** Expose arbitrary MCB state in a bagged ROS message; decide struct/tags, rate
  and UART bandwidth, then specify and implement both ends.
  [Wire contract](../ros2_dji_serial_bridge/UART_PROTOCOL.md#message-types).
- **T29 — startup / common — decision open:** Validate [image pulling](../docs/CI.md#robot-registry) versus local builds.
  If builds stay, assess compression/caches/overlays and USB versus reverse SSH.
  [Image workflow](../isaac_ros_common/docker/README.md#on-the-x86-laptop).

## Tracks, in order of work

Sim first; robot work waits (2026-10-08). Address A, G, then sim parts of B; D supports A. Administration is
independent. E, F, H and J are unscheduled, with robot checks under [later](#later-needs-a-robot). Navigation waits
until after the Midwest competition.

### A. The match test

- **T17 — sim / thornbots_pkg — open:** Finish remaining lockstep gates and repeat the board parked-cell sweep. Inspect
  lost tracks and stamped detection/odometry inputs before tracker tuning.
  [Lockstep order](E2E_LOCKSTEP_PLAN.md#order-and-done-when),
  [hosted baseline](../sim/docs/match-check-2026-10-11.md#parked-cells).
- **A-combat — sim / thornbots_pkg — open:** Add calibrated combat floors; drive rejects zero native hits, while
  match still uses diagnostic checks. Raw aim no longer follows EKF/RELOCALIZE. Spin alignment gating clears the
  hosted near-range spinning floors. Three accepted board drive/match repeats improve hits over nightly;
  calibrated combat floors and board parked-cell repeatability remain open. Retain navigation startup
  failures in the acceptance record.
  [Diagnostic design](../sim/README.md#driving-and-combat-diagnostics-mcb_drive).

### G. Estimation accuracy

- **G.1 — thornbots_pkg — open:** Finish radius/spin repair; tested radius-noise and initial-prior settings fail
  full-matrix acceptance. Diagnostics and trial controls are available; defaults and limits stay unchanged.
  [Trials and remaining gates](../sim/docs/cv-estimation-g1-2026-10-15.md), [tracker](../thornbots_pkg/README.md#target_tracker).
- **G.2 — thornbots_pkg — open:** Tune radial depth noise with ray covariance; repair staggered-panel handoff/parity
  after blackouts. [Tracker](../thornbots_pkg/README.md#target_tracker).
- **G.3 — thornbots_pkg — open:** Gate validity on settling; compare age/residual gates and aiming cost.
  [Tracker](../thornbots_pkg/README.md#target_tracker).
- **T15 — thornbots_pkg — open:** Fix yaw/radius loss on angled stationary targets, then add limits to default
  `stationary45` cells. [Bench limits](../sim/README.md#run-the-tests).
- **T7 — thornbots_pkg — open:** Sweep acceleration process noise against velocity error, including path ends.
  [Tracker](../thornbots_pkg/README.md#target_tracker).
- **T8 — sim — open:** Compare cells run alone and in sequence. [Estimation bench](../sim/README.md#run-the-tests).

Score each accuracy change over three runs in its own commit; tighten limits to new worst runs and require all cells to
pass. Preserve baseline radial/blackout error within 1.5x; fresh tracks become valid only after facing-panel error
settles below 5 cm. [Bench](../sim/README.md#run-the-tests).

### B. Hit while we move

- **B-hardware — thornbots_pkg / bridge / MCBV3 — pending:** Validate separate raw aim/navigation frames and RELOCALIZE
  mailbox loss under CV traffic. [Aim and navigation frames](../ros2_dji_serial_bridge/README.md#aim-and-navigation-frames).
- **B-timing — bridge / thornbots_pkg — unmeasured:** Measure residual UART/camera delays, verify YOLO stamp propagation
  and set latency parameters. [Stamp contract](../ros2_dji_serial_bridge/UART_PROTOCOL.md#mcb--jetson),
  [tracker timing](../thornbots_pkg/README.md#target_tracker).
- **B-settling — thornbots_pkg — sim measured, hardware pending:** Use spin alignment gating after chase/lead/filter
  ablations; measure real gimbal and indexing delays before hardware acceptance.
  [Aimer](../thornbots_pkg/README.md#point_to_cv_target).
- **B-moving — sim / thornbots_pkg — open:** Run radial/diagonal aiming paths and add missing floors; each moving match
  segment must finish within 10 percentage points of the same target cell with our robot parked.
  [Bench](../sim/README.md#run-the-tests).

### D. Faster suites

- **D-speed — sim — open:** Find the RTF bottleneck and render only scored inputs.
  [Speed acceptance](E2E_PLAN.md#speed), [lockstep gates](E2E_LOCKSTEP_PLAN.md#order-and-done-when).

### E. Benches that start and stop cleanly

- **T30 — sim / sentry_localization — review blocked:** Static backend construction removes the lifecycle
  response-discovery race; the suite's startup retry is removed. Follow-up pooled drive is 179/190 nightly
  versus 176/187 fixed; fixed full drift is 8/9 with an additional EKF clock-start stall. PRs remain draft.
  [Evidence and remaining gates](t30-localization-startup-2026-10-16.md#alternating-follow-up-2026-10-16).
- **E-teardown — sim — open:** Resolve DDS teardown races and SIGKILL-only shutdown; obtain a matching-library aarch64
  scan-bridge backtrace. [Shutdown findings](../sim/docs/mcb-hosted-check-2026-10-11.md#shutdown-findings),
  [later observations](../sim/docs/mcb-auto-drive-2026-10-12.md).
- **E-launch — sim — open:** Ensure one-command startup, gz checks, readiness and clean completion/Ctrl-C/shell-death
  cleanup, including children outside `kill_launch.sh`. [Build prerequisite](../sim/README.md#build).
- **T24 — sim — cleanup open:** Standardize `localization_drift`, `ekf`, `aim`, `tracking`; retain `mcb_*` stage names
  and retire E1–E4 / Part 1–2 references, including Docker skill. [Current names](../sim/README.md#more-on-the-tests).

### F. CV nodes into their own repo

- **F-split — thornbots_pkg / workspace — deferred:** Move CV nodes/cores/tests to `thornbots_cv`, retaining
  hardware/TF/relay here. Update callers/build integration and rerun both benches.
  [Ownership](../thornbots_pkg/README.md#nodes), [integration](../docs/CI.md#coordinated-package-integration).

### H. SLAM at amcl's level

- **H-ekf — sentry_localization — open:** Test suspected stacked lidar corrections and raw odometry as SLAM input; retune while
  retaining EKF. [Investigation](../sentry_localization/README.md#slam---use-rf2o-worse).
- **H-map — sentry_localization — open:** In mapping mode, save/load a quickly rasterizing pose graph at the configured
  spawn; expose the hard-coded spawn. Assess a pre-Battle mapping lap against the rules.
  [Map loading](../sentry_localization/README.md#launchlocalizationlaunchpy).
- **T3 — sentry_localization / sim — open:** Run five-minute Battle from blank map with moving/spinning lidar occluders,
  high ground and realistic acceleration; score truth error, inspect crossed cells for retained robots, repeat three
  games on one carried map. [Scenario harness](../sim/README.md#scenarios).
- **H-anomalies — sentry_localization / sim — unverified:** Recheck historical EKF/map anomalies on comparable
  truth-error metrics; bisect the field-frame change if reproduced. [Metrics](../sim/README.md#localization-drift-suite),
  [history](https://github.com/Thornbots/thornbots_workspace/blob/3b8163141f919e61b4bf5dafb857130b61d78869/ROADMAP.md#issues-found).

Acceptance: SLAM+EKF passes amcl drift and game scenarios within 0.05 m on the same metric; error does not grow across
carried-map games, and maps do not accumulate robots or duplicate walls.
[Drift metrics](../sim/README.md#localization-drift-suite).

### J. Lidar and camera

Camera checks need hardware; sim detection stand-ins cannot validate them.

- **T23 — sentry_localization / thornbots_pkg — open:** Compare patrol on/off in sim and hardware; assess lidar-driven
  search if localization degrades. [Moving lidar](../sentry_localization/README.md#contract-with-thornbots_pkg),
  [patrol](../thornbots_pkg/README.md#point_to_cv_target).
- **T19 — thornbots_pkg — untested:** Determine whether depth is needed or colour-only ranging suffices.
  [Depth input](../thornbots_pkg/README.md#target_tracker).
- **T37 — camera/CV packages — unmeasured:** Measure camera copy latency and CPU/GPU cost on Orin before choosing
  zero-copy. [Copy boundary](../realsense-yolov8-nitros-bridge/README.md#copy-boundary).

## Later: deferred

- **T35 — MCBV3 — deferred:** Leave branches as they are for now. Later, an admin makes `main` the default branch
  (it already contains all of `newMain`; nothing references `newMain`), then deletes `newMain`.
  [Repository](https://github.com/Thornbots/MCBV3), [branch policy](../AGENTS.md#branches).

## Later: needs a robot

- **T21 — localization / startup — pending:** Collect maps/logs/bags from five-minute real-floor runs, including T27
  clock-validation artifacts. [Run artifacts](../isaac-ros-startup/README.md#use),
  [map persistence](../sentry_localization/README.md#launchlocalizationlaunchpy).
- **T21 shots — bridge / MCBV3 — pending:** Deploy matching firmware/ROS using the current wire format, then:
  - Validate lit-panel depth, bridge `pose>0`, field-aligned raw POSE and held aim across RELOCALIZE. Send a navigation
    correction only when the offset changes; driving alone must not trigger repeated fixes every 0.3 s.
    [Firmware coordination](../ros2_dji_serial_bridge/README.md#where-the-firmware-stands).
  - Check no-target fire-clear/bit-0 behavior; measure transit/indexer timing and give latency compensation one owner.
    [Timing contract](../ros2_dji_serial_bridge/UART_PROTOCOL.md#cv_target-id1--aim-point-and-fire-decision).
  - Verify muzzle speed below 25 m/s on a stand, with eye protection and accessible e-stop.
    [Hardware checks](JAZZY_FLASH.md#hardware-checklist).
- **T27 — startup — mitigation unvalidated:** Test an air-gapped sentry boot with Wi-Fi enabled mid-run.
  [Clock-step mitigation](../isaac-ros-startup/README.md#design-notes).
- **T34 — startup — unmeasured:** Measure power-on to useful CV/localization on sentry, hero and standard, including
  UEFI/GPU recovery; target under one minute. [Boot instrumentation](../isaac-ros-startup/README.md#boot-time).

## Issues found

Open findings from the [documentation audit](../docs/audits/docs-audit-2026-10-06.md):

- **DOC14b/c — rf2o / common — open:** Add human-facing fork usage and onboarding (#14b/#14c).
  [rf2o README](../rf2o_laser_odometry/README.md), [common README](../isaac_ros_common/README.md).
- **DOC14d — MCBV3 — open:** Replace obsolete artifact guidance and dead build anchor (#14d).
  [Deployment README](../firmware/MCBV3/isolated-deploy/README.md).
- **DOC14f — sim — open:** Shorten current instructions and separate historical experiments (#14f).
  [Sim README](../sim/README.md).
- **DOC14g — workspace — audit open:** Finish source/page audit and extract missing base-building specifications (#14g).
  [Unextracted sources](ARCC_2026_SENTRY_CONTEXT.md#not-yet-extracted--worth-pulling-in-later).
- **SIM-wall — sim — untested:** Establish wall-impact behavior before demonstrating avoidance.
  [Motion-model limits](../sim/README.md#sentry_v2urdfxacro-motion-model).
