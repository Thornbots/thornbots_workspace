# Physical robot validation

This is the maintained home for unfinished physical-robot acceptance. Software/sim work stays in
[ROADMAP](ROADMAP.md); passing sim does not establish robot acceptance. Preserve IDs, numerical gates and
linked owner contracts when recording results. Follow [robot-run authorization](../AGENTS.md#containers-and-runs)
and the linked package procedures before running hardware.

## Field starts

- **T40 — sentry_localization / thornbots_pkg — unmeasured:** Survey the independent red/blue team starts
  before the next event. `AUTO_LAUNCH_ARGS` in `/etc/thornbots/launch.env` is empty by default, so robots use
  `auto.launch.py`'s unmeasured ARCC Season 2 start centres (red -5.25, -3.0; blue 5.25, -3.0 m).
  Routes live on the Jetson in `thornbots_nav`'s `waypoint_nav` (`nav_route`, default `pipes`); firmware only tracks
  the NAV_GOAL point and waits for the first RELOCALIZE.
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
  ablations; measure real gimbal and indexing delays before hardware acceptance. The planner (spin gating,
  chase/lead) is firmware `aim::AimPlanner`: [MCBV3 aiming planner](../firmware/MCBV3/README.md#mcbv3-aiming-planner),
  [TARGET_STATE](../ros2_dji_serial_bridge/UART_PROTOCOL.md#target_state-id7--tracked-enemy-armor-model).

- **B-manager-ticks — thornbots_pkg — pending:** With the real camera, cover and uncover a tracked plate. The
  TARGET_STATE clear should follow track loss within about one 5 ms decision tick of the confidence crossing,
  and no clear should come while detections keep arriving. [target_manager](../thornbots_pkg/README.md#target_manager).

B-timing depends on the [software stamp audit](ROADMAP.md#b-hit-while-we-move); measure residual
UART/camera delay on the robot before selecting physical latency compensation.

## Parked localization

- **T39 — rf2o / sentry_localization — open; references enabled by default, robot run confirms:** Bound parked rf2o drift. Parked, rf2o
  integrated scan-to-scan match noise (about 0.55 mm/s, head still or slewing) and the EKF follows its x/y; wheels held
  still. `reference_scans` is now on by default in `sentry_localization`'s `rf2o.yaml` (enabled before this robot run by user
  decision 2026-11-15, validated in sim; [sentry_localization #18](https://github.com/Thornbots/sentry_localization/pull/18)).
  Once `/odom` has held still for 2 s, rf2o keeps one anchor scan per park (7.5 s lifetime) and prewarps the stamped head
  offset, not "the same head angle" (`CLaserOdometry2DNode.cpp` `findReference`). Sim `mcb_parked` p95 was 0.002-0.009 m in every cell
  in earlier Renode runs (was up to 0.090 m) and 0.005-0.025 m on 2026-11-16 hosted runs, and a 4 cm shove with the
  wheels held still shows up (`parked_push`). AMCL can still update while parked:
  `map_pose_publisher` sends no-motion update requests when the backend pose is older than 0.5 s. Next: the robot run confirms
  this parked with the head idle and turning for idle looks, and a hand shove; follow the
  [parked acceptance procedure](../sentry_localization/README.md#robot-parked-acceptance). `mcb_parked` keeps its 0.15 m p95 gate.
  [Investigation](investigations/t39-parked-drift-2026-10-25.md),
  [reference scans](../rf2o_laser_odometry/README.md), [parked gate](../sim/README.md#more-on-the-tests).
- **T41 — thornbots_pkg / firmware — unmeasured:** Confirm absolute RELOCALIZE on the robot: after boot
  and after driving, the MCB's navigation position should match the AMCL field pose within the sim result
  (0.087 m RMS), with no rejected-jump lockout. [Gates and measurements](investigations/absolute-relocalize-2026-11-11.md).

## Lidar and camera

- **T23 — sentry_localization / thornbots_pkg — hardware pending:** After merged stage 1 idle looks,
  measure robot rf2o steps with the head idle. Software stages 2–4 remain in
  [ROADMAP](ROADMAP.md#j-lidar-and-camera).
  [Moving lidar](../sentry_localization/README.md#contract-with-thornbots_pkg),
  [idle looks](../thornbots_pkg/README.md#point_to_cv_target).
- **SENTRY-drift — robot run — open:** Angle compensation ([thornbots_pkg #18](https://github.com/Thornbots/thornbots_pkg/pull/18))
  and the RF2O scan-size guard ([rf2o #10](https://github.com/Thornbots/rf2o_laser_odometry/pull/10)) are merged; measure
  stationary drift (was 1–2 m) and moving scan acceptance under AMCL on the robot.
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
  `ttyTHS1` (stop `thornbots` and disconnect the MCB before a UART loopback), the RPLIDAR (`/host-dev/rplidar`, the udev symlink) and the RealSense at USB 3; rebuild `yolo11s_fp16.plan`
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
  - Check that idle looks never fire and that the MCB's TARGET_STATE ages, replan period and indexer latency hold on
    hardware; measure UART/USB transit, which the ages leave uncorrected.
    [TARGET_STATE contract](../ros2_dji_serial_bridge/UART_PROTOCOL.md#target_state-id7--tracked-enemy-armor-model).
  - Verify muzzle speed below 25 m/s on a stand, with eye protection and accessible e-stop.
- **T27 — startup — mitigation unvalidated:** Test an air-gapped sentry boot with Wi-Fi enabled mid-run.
  [Clock-step mitigation](../isaac-ros-startup/README.md#design-notes).
- **T34 — startup — unmeasured:** Measure power-on to useful CV/localization on sentry, hero and standard, including
  UEFI/GPU recovery; target under one minute. [Boot instrumentation](../isaac-ros-startup/README.md#boot-time).

## Consolidated hardware checks

- **Base tilt — firmware / aim:** With gimbal motors off, tip the sentry chassis a few degrees toward the barrel and
  back. POSE `head_pitch` must change by about the barrel's world tilt (down positive) and return to the encoder
  value within a few seconds; tipping sideways must not change it. Otherwise `IMU_BARREL_FORWARD`/`PITCH_UP_SIGN`
  do not match the board mount. Then compare drive-phase hits. [Base tilt](../firmware/MCBV3/README.md#base-tilt).
- **LIDAR-mount — bringup / localization:** Revalidate the restored upright mount translation and yaw with a head-turn fit, nose-up/down self-filter
  sectors and floor-to-scan height; update the map slice only from the measurement. Inspect `/scan_raw` between
  0.05–0.15 m before lowering the retained 0.15 m filtering margin. Validate fixed-heading rf2o against real chassis
  yaw drift, head still/slewing and moving scans. Depends on T38 and surveyed field registration.
  [Upright-mount evidence](investigations/lidar-mount-2026-10-26.md),
  [range rationale](../sentry_localization/README.md#configslamyaml).
- **T23 (continued):** Observe a real referee-triggered hit turn and verify head-idle rf2o steps near the measured
  0.7 mm still-head baseline. Measure detection range and time-to-first-detection; do not enable stage 4 from sim
  alone. Depends on S2-foundation and software stages 2–4. [Design](lidar-guided-aiming-2026-10-25.md#design).
- **MMM-field — bringup / localization / startup:** Run through `operator_workflow`, which relaunches with
  `localization_mode:=mapping`. On a normal amcl boot, check that a controller-started MMM is refused and the MCB
  ends in Done ([consequence](../thornbots_pkg/README.md#mcb-mapping-machine); intended, kept behavior).
  Validate physical map contract, controller hold/interlocks,
  away-and-back AMCL convergence, live wall/scan agreement, real referee match boot/reboot, release image identity,
  persistence/reload and physical field coverage. Exercise both team starts after survey; verify raw-x displacement
  loss/slip on measured distances. Verify MCB shared-power timing, storage durability, systemd activation and actual
  Jetson power-off. Depends on T38/T40/T27.
  [Operator contract](../thornbots_pkg/README.md#field-day-and-room-workflow),
  [MMM evidence boundary](investigations/mmm-node-validation-2026-10-29.md#corrections-and-limits),
  [mapping evidence](investigations/mapping-procedure-2026-10-26.md#repository-checks-and-open-acceptance).
- **T38 (continued):** Isolate source/pipeline loss from subscriber loss at 60 fps; verify calibrated depth, camera-to-
  odom TF at capture stamps and lit-panel depth. Measure real PING RTT and capture-to-CV latency; inspect interrupted
  MCAP integrity/replay after power loss. Rebuild per-Orin TensorRT assets before performance acceptance.
  [Unresolved capture](investigations/sentry-nightly-jetson-2026-10-18.md#remaining-acceptance).
- **T34 / T27 (continued):** Exercise actual GPU failure/recovery, real disk-pressure bag pruning (it runs only at service
  start, never mid-run) and mid-run Wi-Fi without a clock step/restart. Host pruning tests (T20 merged) do not establish hardware acceptance.
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
