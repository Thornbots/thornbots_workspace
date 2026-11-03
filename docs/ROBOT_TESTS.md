# Physical robot validation

This is the maintained home for unfinished physical-robot acceptance. Software/sim work stays in
[ROADMAP](ROADMAP.md); passing sim does not establish robot acceptance. Preserve IDs, numerical gates and
linked owner contracts when recording results. Follow [robot-run authorization](../AGENTS.md#containers-and-runs)
and the linked package procedures before running hardware.

## Field starts

- **T40 — sentry_localization / thornbots_pkg — unmeasured:** Survey the independent red/blue team starts
  before the next event; defaults in `/etc/thornbots/launch.env` remain unmeasured spooky scrim values.
  Firmware receives starts through RELOCALIZE and uses absolute field routes.
  [Configuration](../thornbots_pkg/README.md#point_to_cv_target),
  [wire contract](../ros2_dji_serial_bridge/UART_PROTOCOL.md#message-types).
  The failed ARCC-world ingress remains software work under [T40](ROADMAP.md#short-todos).

## Robot image workflow

- **T29 — startup / common — hardware acceptance:** Registry bases plus offline source overlays are the supported
  [workflow](../isaac_ros_common/docker/README.md#building-the-robots-image); local image builds/shipping remain emergency fallback.
  [Orin measurements and acceptance boundary](investigations/robot-overlay-2026-11-01.md).
  Remaining: restart a fully equipped robot on the overlay and confirm a working `thornbots` stack; the dev board
  lacks camera/lidar/model assets and the equipped robots were unreachable. Existing images also need a manual
  pull after upstream CLI/base configuration changes; their offline contract covers Thornbots Docker inputs/manifests.

## Moving aim

- **B-hardware — thornbots_pkg / bridge / MCBV3 — pending:** Validate separate raw aim/navigation frames and RELOCALIZE
  [mailbox loss](../ros2_dji_serial_bridge/UART_PROTOCOL.md#mcb-receive) under CV traffic. [Aim and navigation frames](../ros2_dji_serial_bridge/README.md#aim-and-navigation-frames).
- **B-timing — bridge / thornbots_pkg — unmeasured:** Measure residual UART/camera delays, verify YOLO stamp propagation
  and set latency parameters. [Stamp contract](../ros2_dji_serial_bridge/UART_PROTOCOL.md#mcb--jetson),
  [tracker timing](../thornbots_pkg/README.md#target_tracker).
- **B-settling — thornbots_pkg — sim measured, hardware pending:** Use spin alignment gating after chase/lead/filter
  ablations; measure real gimbal and indexing delays before hardware acceptance.
  [Aimer](../thornbots_pkg/README.md#point_to_cv_target).

B-timing depends on the [software stamp audit](ROADMAP.md#b-hit-while-we-move); measure residual
UART/camera delay on the robot before selecting physical latency compensation.

## Parked localization

- **T39 — rf2o / sentry_localization — open; opt-in sim measured, hardware pending:** Bound parked rf2o drift. Parked, rf2o
  integrated scan-to-scan match noise (about 0.55 mm/s, head still or slewing) and the EKF follows its x/y; wheels held
  still and AMCL never updates parked. rf2o's `reference_scans` is available but off by default; when enabled, it matches parked scans against earlier ones from the
  same head angle once `/odom` has held still for 2 s: sim `mcb_parked` p95 0.002-0.009 m in every cell (was up to 0.090 m), and a 4 cm shove with the
  wheels held still shows up (`parked_push`). These results used references enabled, not the default configuration. Next: confirm on the robot parked with
  the head idle and turning for idle looks, and a hand shove. `mcb_parked` keeps its 0.15 m p95 gate.
  [Investigation](investigations/t39-parked-drift-2026-10-25.md),
  [reference scans](../rf2o_laser_odometry/README.md), [parked gate](../sim/README.md#more-on-the-tests).

## Lidar and camera

- **T23 — sentry_localization / thornbots_pkg — hardware pending:** After merged stage 1 idle looks,
  measure robot rf2o steps with the head idle. Software stages 2–4 remain in
  [ROADMAP](ROADMAP.md#j-lidar-and-camera).
  [Moving lidar](../sentry_localization/README.md#contract-with-thornbots_pkg),
  [idle looks](../thornbots_pkg/README.md#point_to_cv_target).
- **T19 — thornbots_pkg — untested:** Determine whether depth is needed or colour-only ranging suffices.
  [Depth input](../thornbots_pkg/README.md#target_tracker).
- **SENTRY-drift — robot run — open:** Angle compensation ([thornbots_pkg #18](https://github.com/Thornbots/thornbots_pkg/pull/18))
  and the RF2O scan-size guard ([rf2o #10](https://github.com/Thornbots/rf2o_laser_odometry/pull/10)) are merged; measure
  stationary drift (was 1–2 m) and moving SLAM scan acceptance on the robot.
  [Drift](investigations/sentry-sim-to-real-2026-10-18.md#stationary-localization-drift).
- **T37 — camera/CV packages — unmeasured:** Measure camera copy latency and CPU/GPU cost on Orin before choosing
  zero-copy. [Copy boundary](../realsense-yolov8-nitros-bridge/README.md#copy-boundary).

## Robot acceptance

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

## Consolidated hardware checks

- **LIDAR-mount — bringup / localization:** Measure flipped-mount yaw with a head-turn fit, nose-up/down self-filter
  sectors and floor-to-scan height; update the map slice only from the measurement. Inspect `/scan_raw` between
  0.05–0.15 m before lowering the retained 0.15 m filtering margin. Validate fixed-heading rf2o against real chassis
  yaw drift, head still/slewing and moving scans. Depends on T38 and surveyed field registration.
  [Flipped-mount evidence](investigations/lidar-flip-2026-10-31.md#robot-measurement),
  [range rationale](../sentry_localization/README.md#configslamyaml).
- **T23 (continued):** Observe a real referee-triggered hit turn and verify head-idle rf2o steps near the measured
  0.7 mm still-head baseline. Measure detection range and time-to-first-detection; do not enable stage 4 from sim
  alone. Depends on S2-foundation and software stages 2–4. [Design](lidar-guided-aiming-2026-10-25.md#design).
- **MMM-field — bringup / localization / startup:** Validate physical map contract, controller hold/interlocks,
  away-and-back AMCL convergence, live wall/scan agreement, real referee match boot/reboot, release image identity,
  persistence/reload and physical field coverage. Exercise both team starts after survey; verify raw-x displacement
  loss/slip on measured distances. Verify MCB shared-power timing, storage durability, systemd activation and actual
  Jetson power-off. Depends on H-map/H-graph-roundtrip, T38/T40/T27.
  [Operator contract](../thornbots_pkg/README.md#field-day-and-room-workflow),
  [MMM evidence boundary](investigations/mmm-node-validation-2026-10-29.md#corrections-and-limits),
  [mapping evidence](investigations/mapping-procedure-2026-10-26.md#repository-checks-and-open-acceptance).
- **T38 (continued):** Isolate source/pipeline loss from subscriber loss at 60 fps; verify calibrated depth, camera-to-
  odom TF at capture stamps and lit-panel depth. Measure real PING RTT and capture-to-CV latency; inspect interrupted
  MCAP integrity/replay after power loss. Rebuild per-Orin TensorRT assets before performance acceptance.
  [Unresolved capture](investigations/sentry-nightly-jetson-2026-10-18.md#remaining-acceptance).
- **T34 / T27 (continued):** Exercise actual GPU failure/recovery, real disk-pressure bag pruning and mid-run Wi-Fi
  without a clock step/restart. Host pruning tests (T20 merged) do not establish hardware acceptance.
  [Startup design](../isaac-ros-startup/README.md#design-notes).
- **E-discovery — startup / common:** After the Mini investigation, confirm attached-shell graph/topic discovery on
  the real stack with the supported DDS profile and bag comparison. Preserve Fast DDS invariants; missing CLI nodes
  alone are not proof of missing runtime nodes. [Mini work](ROADMAP.md#d-and-e-acceptance-details).
- **T21 shots (continued):** Verify firing receipt/indexer timing and HP/heat/power gates with matching ROS/firmware
  and the current referee spec before firing. Record disconnect/reconnect controller interlocks and measured muzzle
  speed under the existing <25 m/s stand/e-stop/eye-protection requirement. [Wire](../ros2_dji_serial_bridge/UART_PROTOCOL.md).
- **MCB-engineer — firmware — calibration pending:** Calibrate engineer homing offset and power-limiter torque scaling
  before admitting engineer to CI; do not enable it from hosted fake-hardware tests.
  [Owner](../firmware/MCBV3/AGENTS.md).
- **SIM-plant-calibration — sim / firmware:** Measure tire/braking/suspension and board gimbal/indexer response before
  treating simulated gains, feed geometry or timing as physical calibration. Subsequent model implementation and Mini
  regressions remain [SIM-plant-model](ROADMAP.md#additional-mini-work); keep current limits while unmeasured. [Plant limits](../sim/README.md#mcb-emulator).
