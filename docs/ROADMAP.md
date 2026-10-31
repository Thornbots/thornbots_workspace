# Where the project is going

Prove the firmware-driven CV stack end to end in sim, improve estimation, then validate on robots. This file owns open
work; usage, design and measurements stay in linked docs.

## Where we actually are

| Area | Current evidence | Home |
| --- | --- | --- |
| Localization | Native suite passes recorded | [Drift](../sim/README.md#localization-drift-suite), [EKF](../sim/README.md#ekf-ground-truth-suite), [native validation](https://github.com/Thornbots/sim/commit/4e9445a6c1be7562e188d70a94435a47bad8043d) |
| Estimation | Bench baseline recorded | [Bench](../sim/README.md#run-the-tests), [baseline](../sim/docs/cv-bench-results-2026-09-28.md) |
| Firmware / CV | Raw aim is isolated from navigation; board stages pass diagnostic tier. Fresh Mac hosted repeats clear all spinning cells and improve every stage; three accepted board drive/match repeats improve hits over nightly | [Type C](../sim/README.md#type-c-board-execution-with-renode), [board verification](../sim/docs/mcb-auto-drive-2026-10-12.md), [accuracy repeats](../sim/docs/aim-accuracy-2026-10-12.md#spinning-correction-and-board-comparison) |
| Robots | All four Orins on JetPack 7.2.1/Jazzy; robot acceptance remains; each robot runs its own ROS domain ([T38](#later-needs-a-robot)) | [T38](#later-needs-a-robot) |

## Short todos

- **T40 — MCBV3 / sentry_localization / thornbots_pkg / sim — temporary, not good:** The team start is the
  unmeasured spooky scrim (∓3.53, -0.426) from a route drawing, copied to the Jetson and the UART contract.
  Measure it, or restore the ARCC (∓4.625, 0), before the next event. sim still spawns at the ARCC start
  ([sim #60](https://github.com/Thornbots/sim/pull/60) is a draft: the new spawn is inside the ARCC world's
  start-zone wall), so sim MCB/E2E suites disagree with firmware until then.
  [Firmware constants](../firmware/MCBV3/MCB-project/src/subsystems/odometry/OdometrySubsystemConstants.hpp),
  [wire contract](../ros2_dji_serial_bridge/UART_PROTOCOL.md#message-types).
- **T36 — repository admins — blocked on admin access:** Lock `humble` read-only in Realsense_ROI_Depth_Rectifier,
  isaac-ros-startup, realsense-yolov8-nitros-bridge and ros2_dji_serial_bridge using the workspace
  [ruleset](https://github.com/Thornbots/thornbots_workspace/rules/24850059).
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
  [mailbox loss](../ros2_dji_serial_bridge/UART_PROTOCOL.md#mcb-receive) under CV traffic. [Aim and navigation frames](../ros2_dji_serial_bridge/README.md#aim-and-navigation-frames).
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

- **T30 — sim / sentry_localization — ready for review:** Static backend construction removes the lifecycle
  response-discovery race; the suite's startup retry is removed. Drive non-regression is accepted.
  The clock bridge uses UDP-only DDS after a captured SHM publication stall.
  Final full drift confirmations pass 9/9 twice with 0/18 startup failures and unchanged scoring.
  Large uncommanded simulator yaw excursions also reproduce on nightly; earlier failures are retained.
  [Evidence and limitations](t30-localization-startup-2026-10-16.md#shared-sim-comparison-and-acceptance-2026-10-18).
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
- **T39 — rf2o / sentry_localization — open; opt-in sim measured, hardware pending:** Bound parked rf2o drift. Parked, rf2o
  integrated scan-to-scan match noise (about 0.55 mm/s, head still or slewing) and the EKF follows its x/y; wheels held
  still and AMCL never updates parked. rf2o's `reference_scans` is available but off by default; when enabled, it matches parked scans against earlier ones from the
  same head angle once `/odom` has held still for 2 s: sim `mcb_parked` p95 0.002-0.009 m in every cell (was up to 0.090 m), and a 4 cm shove with the
  wheels held still shows up (`parked_push`). These results used references enabled, not the default configuration. Next: confirm on the robot parked with
  the head idle and turning for idle looks, and a hand shove. `mcb_parked` keeps its 0.15 m p95 gate.
  [Investigation](investigations/t39-parked-drift-2026-10-25.md),
  [reference scans](../rf2o_laser_odometry/README.md), [parked gate](../sim/README.md#more-on-the-tests).

Acceptance: SLAM+EKF passes amcl drift and game scenarios within 0.05 m on the same metric; error does not grow across
carried-map games, and maps do not accumulate robots or duplicate walls.
[Drift metrics](../sim/README.md#localization-drift-suite).

### J. Lidar and camera

Camera checks need hardware; sim detection stand-ins cannot validate them.

- **T23 — sentry_localization / thornbots_pkg — stage 1 in review:** Jetson patrol replaced by rate-capped idle looks
  (last enemy, hit hold, enemy zone); lidar tracks are stages 2-4 of the
  [lidar-guided aiming design](lidar-guided-aiming-2026-10-25.md#stages). Next: robot rf2o steps with the head idle.
  [Moving lidar](../sentry_localization/README.md#contract-with-thornbots_pkg),
  [idle looks](../thornbots_pkg/README.md#point_to_cv_target).
- **T19 — thornbots_pkg — untested:** Determine whether depth is needed or colour-only ranging suffices.
  [Depth input](../thornbots_pkg/README.md#target_tracker).
- **SENTRY-drift — robot run — open:** Angle compensation ([thornbots_pkg #18](https://github.com/Thornbots/thornbots_pkg/pull/18))
  and the RF2O scan-size guard ([rf2o #10](https://github.com/Thornbots/rf2o_laser_odometry/pull/10)) are merged; measure
  stationary drift (was 1–2 m) and moving SLAM scan acceptance on the robot.
  [Drift](investigations/sentry-sim-to-real-2026-10-18.md#stationary-localization-drift).
- **SIM-returns — sim — open:** Sim lidar matches the real 720-bin grid ([sim #31](https://github.com/Thornbots/sim/pull/31))
  but has no no-return (`inf`) beams beyond the self-filter; real has about 40%. SLAM drift in sim rose from
  0.08–0.13 m to 0.15–0.22 m with the new grid (limit 0.40 m, 3 trials); cause unknown.
- **LIDAR-range — sentry_localization — open:** `slam.yaml` and `amcl.yaml` drop returns under 0.15 m and call it the
  hardware minimum; the A2M8 minimum is 0.05 m.
- **T37 — camera/CV packages — unmeasured:** Measure camera copy latency and CPU/GPU cost on Orin before choosing
  zero-copy. [Copy boundary](../realsense-yolov8-nitros-bridge/README.md#copy-boundary).

## Later: deferred

- **T35 — MCBV3 — deferred:** Leave branches as they are for now. Later, an admin makes `main` the default branch
  (it already contains all of `newMain`; nothing references `newMain`), then deletes `newMain`.
  [Repository](https://github.com/Thornbots/MCBV3), [branch policy](../AGENTS.md#branches).

## Later: needs a robot

- **Sentry match Wi-Fi acceptance:** eduroam (priority 20, ClearPass-registered)
  autoconnects on sentry, standard and dev; sentry rejoined after a reboot
  2026-10-30. Hero still needs it. Install the
  [opt-in](../isaac-ros-startup/README.md#match-wi-fi-disconnect-opt-in), reject
  isolated battle frames, confirm three consecutive battle messages disconnect
  every Wi-Fi device with no reconnect after match/container restart, and that
  the next reboot restores autoconnect. Check journal, SSH/Foxglove loss and no
  clock step.

- **T38 — robots — open:** All four Orins run JetPack 7.2.1/Jazzy; none has passed robot acceptance. On each: check
  `ttyTHS1` (stop `thornbots` and disconnect the MCB before a UART loopback), the RPLIDAR (`/dev/ttyUSB0`, container udev) and the RealSense at USB 3; rebuild `yolo11s_fp16.plan`
  (standard's built 2026-10-26); measure 60 fps camera, YOLO FPS and camera-to-`TargetState` latency in the
  [full pipeline](../realsense-yolov8-nitros-bridge/README.md#full-robot-pipeline); re-measure the Fast DDS invariants
  (Fast DDS 2.14). Standard's reflash launch hold was
  removed 2026-10-26; `thornbots` starts at boot there too.
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
- **T27 — startup — mitigation unvalidated:** Test an air-gapped sentry boot with Wi-Fi enabled mid-run.
  [Clock-step mitigation](../isaac-ros-startup/README.md#design-notes).
- **T34 — startup — unmeasured:** Measure power-on to useful CV/localization on sentry, hero and standard, including
  UEFI/GPU recovery; target under one minute. [Boot instrumentation](../isaac-ros-startup/README.md#boot-time).

## Issues found

Open findings from the [documentation audit](../docs/audits/docs-audit-2026-10-06.md):

- **DOC14b — rf2o — open:** Add human-facing fork usage (#14b).
  [rf2o README](../rf2o_laser_odometry/README.md).
- **DOC14f — sim — open:** Shorten current instructions and separate historical experiments (#14f).
  [Sim README](../sim/README.md).
- **DOC14g — workspace — audit open:** Finish source/page audit and extract exact zone geometry, the referee UART specification and round timing (#14g).
  [Unextracted sources](ARCC_2026_SENTRY_CONTEXT.md#not-yet-extracted--worth-pulling-in-later).
- **SIM-wall — sim — untested:** Establish wall-impact behavior before demonstrating avoidance.
  [Motion-model limits](../sim/README.md#sentry_v2urdfxacro-motion-model).
