# Where the project is going

A localization suite we can believe, CV split at `TargetState` with a bench
for each half, then the CV stack from detections to gimbal tested end to
end in sim. Updated 2026-10-11. `main` has been Jazzy since 2026-09-27;
Humble is frozen on the `humble` branches.

This file lists only work still to do. Delete an item when it's finished,
then commit and push; don't mark it done. Measurements and run histories
belong in commits and dated investigation docs.

## Where we actually are

| Thing | State |
|---|---|
| Drift suite, EKF | Native suites pass; startup races remain T30. [Drift design](sim/README.md#localization-drift-suite), [EKF design](sim/README.md#ekf-ground-truth-suite), [validation](https://github.com/Thornbots/sim/commit/4e9445a) |
| Estimation bench | [Commands](sim/README.md#run-the-tests), [dated results](sim/docs/cv-bench-results-2026-09-28.md), [remaining work](#g-estimation-accuracy) |
| CV end to end in sim | Aiming, tracking, driving and match suites pass, but an x86_64 match run caught allied intersections; moving-target cells and repeatability are open (T17). Passing drive/match diagnostics do not establish combat accuracy. |
| Jazzy | [Laptop validation](JAZZY_FLASH.md#laptop-validation-2026-09-30); [hardware status](JAZZY_FLASH.md#hardware-status) |

## Short todos

Numbers stay put when items are deleted or move to a track (T3 to H; T7, T8
and T15 to G; T17 to A; T20, T25 and T29 to C; T24 and T30 to E; T19, T22
and T23 to J).

CV:

- T31: Tell the Type C when not to turn toward a hit (the user,
  2026-10-04). `point_to_cv_target` sends `turn_to_hit` (`CVTarget` bit 2)
  unchanged (default true), so a hit overrides a live CV target for 500 ms.
  Decide it per frame: clear it while we hold a valid `TargetState`, and
  gate our own patrol's hit turn (`hit_turn_s`) the same way. Also repair
  the hit input: `HitTracker::addHit` converts already-radian IMU yaw by
  `PI/180`, and its one-cycle `isHit` can be missed by the 10 Hz REF_SYS
  sample. Establish the angle's units/reference, latch hits until
  reported, and test with nonzero head/chassis yaw before trusting
  `hit_angle_sign`. See [firmware coordination](ros2_dji_serial_bridge/README.md#where-the-firmware-stands).
- T32: Choose the right panel on a robot that isn't spinning (the user,
  2026-10-04). Below `spin_exit_rad_s`, `plan_shot`
  (`point_to_cv_target_core.cpp`) leads the panel whose yaw is nearest the
  bearing to us, rounded per tick. Near 45 deg two panels face us about
  equally and the pick can flip tick to tick, swinging the gun a panel's
  width; it also leans on the tracker's yaw, weakest there (T15). Want:
  the most face-on panel, held with hysteresis until another is clearly
  better. Measure on the aiming bench at 45 deg.
- T33: A patrol flag on `CVTarget` (the user, 2026-10-04). Patrol points go
  out as aim points with `fire` clear, so the MCB can't tell a sweep from a
  target we're holding fire on. Add a bit (bit 3, reserved today) set on
  every patrol point: `CVTarget.msg`, the bridge's packing,
  `UART_PROTOCOL.md`, `point_to_cv_target`, sim's wire helper
  (`sim/src/mcb_protocol.cpp`) and MCBV3's `JetsonSubsystem.hpp`. Ask the
  MCB team to adopt it with the
  [bridge firmware asks](ros2_dji_serial_bridge/README.md#asked-of-the-firmware).

Repos:

- T35: Move MCBV3 to `main` (the user, 2026-10-10; not ready yet). Its
  GitHub default is still `newMain`, far behind `nightly`. Make `main` the
  default like the other packages, then retire `newMain`.
- T36: Lock `humble` read-only in Realsense_ROI_Depth_Rectifier,
  isaac-ros-startup, realsense-yolov8-nitros-bridge and
  ros2_dji_serial_bridge. Needs a repo admin; copy the
  "Archive humble (read-only)" ruleset from thornbots_workspace.

## Tracks, in order of work

Sim work first; robot work waits for [later](#later-needs-a-robot) (the
user, 2026-10-08). Finish the short todos, then A, then G, then the sim
parts of B and C. D runs alongside A; E, F, H, I and J are unscheduled.
Navigation comes after the Midwest competition; until then the match test
drives our robot from sim.

### A. The match test

[`E2E_PLAN.md`](E2E_PLAN.md): stages `mcb_parked`, `mcb_drive` and
`mcb_match` ([sim README](sim/README.md)).

- T17: Runs with the same inputs should score nearly the same (the user,
  2026-09-28). The aiming bench does; the estimation bench's moving cells
  and `mcb_parked` do not. The worst cells are lost tracks, not aim, though
  the stand-in feeds truth, so look at the tracker's input in gz (detection
  timing and stamps against `/clock`, the parked robot's odom walk in
  `odom_disagreement_m`) before the tracker. The
  [MCB-batch gate](sim/README.md#mcb-emulator) is implemented; full
  hit-path lockstep and identical shot sequences remain in
  [`E2E_LOCKSTEP_PLAN.md`](E2E_LOCKSTEP_PLAN.md).
- `mcb_drive` passes with no hits (2026-10-08: every segment 0%, median aim
  error over 0.10 m, localization p95 0.46-0.91 m against truth). Make it
  fail on that, then find why localization is that far off while driving
  (the drift suite's 0.24 m is `map->odom` change, not truth error).

### I. MCB emulator

Stages run the checked-out MCBV3 code as a host build with fake hardware
([sim README](sim/README.md#mcb-emulator)); motor feedback and MCU timing
are models, and `mcb_drive`/`mcb_match` use `match_driver`, not the
firmware's auto-drive.

- Wire physical CAN motor feedback and dynamics to gz instead of applying
  firmware setpoints through gz's existing controllers.
- A real Type C emulator (the user, 2026-10-03): emulate the STM32F407 and
  run the same `.elf` we flash, to catch what the host build hides (UART/DMA
  drivers, interrupt timing, 1 kHz overruns, `-O` and float behaviour).
  Check Renode and QEMU's STM32F405 board first. Model the Jetson and
  referee UARTs, remote DBUS, BMI088 on SPI, and DJI motors on CAN bridged
  to gz.
- Drive `mcb_drive` and `mcb_match` with the firmware's auto-drive.

### B. Hit while we move

Later, needs a robot (the user, 2026-10-08), except the moving-shooter
aiming-bench runs, which are sim. After `mcb_drive` scores, agree the
remaining wire and firmware work with the MCB team. The
[CV interface](thornbots_pkg/README.md#cv-interface) is implemented;
hardware validation is not.

- Validate the [shared field frame](ros2_dji_serial_bridge/README.md#shared-aim-frame)
  on hardware with matching firmware and ROS revisions, including RELOCALIZE
  mailbox loss. The [POSE chassis-yaw proposal](ros2_dji_serial_bridge/UART_PROTOCOL.md#proposed-pose-chassis-yaw)
  stays unapplied; heading-fixed aiming does not need it.
- Measure USB/read buffering and MCB sample-to-send delay. An MCB clock on
  the wire is a proposal, not the current stamp contract.
- Verify camera stamps survive YOLO, measure stamp-to-capture latency
  (metadata or a blinking LED), and set `camera_latency_s`.
- Measure the gimbal's roughly 7-degree chase jump settling; set
  `chase_settle_s`.
- Run radial and diagonal aiming-bench paths with a moving shooter and add
  their missing floors.

Done when each moving match-test segment comes within 10 percentage points
of the same target cell with our robot parked. Record hardware results in
[hardware status](JAZZY_FLASH.md#hardware-status).

### C. Jazzy on the robots

Later, needs a robot (the user, 2026-10-08): the reflash, hardware checks,
boot time and T29. T20's bridge logging and T25's message can land first,
tested in sim against the MCB emulator. Migration state, unverified checks
and flashing steps: [JAZZY_FLASH.md](JAZZY_FLASH.md#hardware-status). A
Humble performance comparison needs a recorded baseline; none exists.

Boot time: power-on to a running ROS stack under 1 min on each robot (the
user, 2026-09-30). The trimmed sentry is at about 20 s from kernel start
([Boot time](isaac-ros-startup/README.md#boot-time), T34). Open: 1 of 12
`quiet` boots lost the GPU (`isaac-ros-startup` reboots on it), the firmware
time before the kernel, and Standard, the one robot left to flash.

- T20: A better log format on the robots (the user, 2026-10-01). About 75%
  of each boot-service log is `dji_serial_bridge`'s per-frame `ref_sys RX`
  and `relocalize TX` INFO lines (`debug_log` defaults true). Left: move
  those to DEBUG or throttle them, throttle CRC and rf2o per-scan WARNs,
  put the bridge's DIAG stats on `/diagnostics`, and test pruning old
  per-run bags by free disk.
- T25: Log any data from the MCB through a new message (the user,
  2026-10-03). The Jetson sees only `POSE`, `REF_SYS` and `PING`, so the
  MCB's own state (mode, setpoints, what it did with a `CV_TARGET`, fire
  events, faults) is invisible after a run. Add a UART message the
  firmware can fill with any data, published by `dji_serial_bridge` on a
  topic the per-run bag records (T20). Open: fixed struct or tagged
  key/value fields, its rate, and the bandwidth left on the 115200-baud
  link. Spec it in `UART_PROTOCOL.md`; land it in the bridge and MCBV3.
- T29: Each robot builds its own image, faster (the user, 2026-10-03).
  Building on the Mac mini is a stopgap. CI now publishes arm64 robot
  images to GHCR ([registry](docs/CI.md#robot-registry)), not yet pulled
  onto a robot. Decide whether pulling replaces building on the robot, then
  trim this item. If building stays, try zstd or no compression on the
  export, new apt packages in their own layer plus an apt cache mount,
  ccache for colcon, and `USE_WS_OVERLAY=true` with an incremental
  `colcon build` for code-only changes. Carrying an image from the laptop
  to the sentry over USB (~200 MB/s, the user) takes minutes; shipping over
  `ssh -R` is untested ([x86 laptop](isaac_ros_common/docker/README.md#on-the-x86-laptop)).

### G. Estimation accuracy

Tuning waits until the stack works end to end (the user, 2026-09-29); the
match test runs on today's tracker. [Dated bench observations](sim/docs/cv-bench-results-2026-09-28.md)
record the errors behind these tasks.

| Step | Problem | Where to start |
| --- | --- | --- |
| G.1 | Radius and spin-rate outliers on some 4 m/s runs | Lower `process_noise_radius` and try an armor-radius prior; log innovations around spin misreads |
| G.2 | Radial depth error and staggered-panel handoff after blackouts | Tune `meas_noise_base_m` / `meas_noise_range_coeff` with `ray_covariance`; check `dz` pair parity across gaps |
| G.3 | Fresh tracks become `valid` before the estimate settles | Gate on track age or facing-panel predicted-versus-measured residual, rather than update count; check the aiming cost |

Each accuracy step is its own commit, scored over three estimation-bench
runs. Done when every cell passes limits tightened to the new worst runs,
radial and blackout error is within 1.5x of default, and no fresh track is
`valid` before facing-panel error settles under 5 cm. Put before/after
numbers in the commit message and update this track in the workspace bump.

- T15: A still target seen at an angle loses yaw and radius (`stationary45`
  bench cells; p95 yaw 0.12 rad). Fix the tracker, then give the default
  `chassis_spin:=0` `stationary45` cells their `LIMITS`; only the
  `chassis_spin:=9` variants have limits today.
- T7: Sweep `process_noise_accel` against the velocity-error trace, path
  ends included.
- T8: Check the bench scores the same with a cell run alone as in sequence.

### D. Faster suites

[`E2E_PLAN.md`](E2E_PLAN.md) "Speed" and [`E2E_LOCKSTEP_PLAN.md`](E2E_LOCKSTEP_PLAN.md)
(unfinished). Find why the full gz stack caps at RTF ~1.55 and render only
what gets scored. Suites run one at a time; we are compute-limited. No
suite runs the gz camera (`camera:=false`); a subscribed RGB-D camera alone
caps a bare server near RTF 2.2.

### E. Benches that start and stop cleanly

A fresh container has no gz until `install-sim.sh` runs; `tools/run_suite.sh`
checks, a plain `ros2 launch` doesn't. A lost lifecycle reply can leave
`amcl` or `map_server` unconfigured; the drift harness restarts such a
stack once, the robot's boot doesn't. Verify interruption and shell-death
cleanup across the launch paths, including children that
`kill_launch.sh -l` cannot see.

**Done when:** each bench starts with one command, says if gz is missing,
waits for the stack before scoring, and on Ctrl-C or the end of the tests
stops every node it started, with no tracebacks and no orphans.

- T30: The robot stack's bring-up race fails drift scenarios (2026-10-03:
  3 of 9 starts). `rf2o` can't look up `root -> lidar` and `amcl` drops
  every scan as older than its TF, so there is no `map->root`; the
  harness's one restart (`_wait_for_root_chain`) hides some of it, and the
  robot can hit it at boot too. Find why the `root` chain is missing at
  start rather than restart around it. 2026-10-08: `mcb_match` died in
  bring-up when `lifecycle_manager_localization` heard nothing from
  `map_server` for 30 s (an `amcl` configure stall in sim `413502d`'s runs).
- T24: One name per test, for what it tests, used by its launch file, test
  file and the docs alike (the user, 2026-10-03). New names:
  `localization_drift` (was `localization_tests.launch.py`), `ekf` (now
  `suite:=ekf` in `localization_suite`), `aim` (was `shot_hit`) and
  `tracking` (was `estimation`). Stages stay `mcb_parked`, `mcb_drive`,
  `mcb_match`; stray E1-E4 and "Part 1/Part 2" names go. About 160
  references across 41 files, plus the isaac-ros-docker skill's
  `reference.md`.

### F. CV nodes into their own repo

Later (the user, 2026-10-02). Move `target_selector`, `target_tracker` and
`point_to_cv_target` with its patrol, their C++ cores and tests, from
`thornbots_pkg` to a new `thornbots_cv` package in its own repo.
`thornbots_pkg` keeps the hardware interface, URDF, TF and `mcb_relay`. A
new submodule needs a `Thornbots/` repo, a `.gitmodules` entry and a
`Dockerfile.thornbots` build line. Everything naming
`package='thornbots_pkg'` for those nodes follows: `auto.launch.py`, sim's
`shot_hit.launch.py` and `estimation.launch.py`, and
`test/cpp/test_cv_bench.cpp`. Do it between bench runs, and re-run both
benches after to show nothing moved.

### H. SLAM at amcl's level

Keep SLAM a real fallback to amcl. amcl with the EKF passes all nine drift
scenarios; the map-based ones read 0.23-0.24 m, which is `map->odom`
change, not truth error: compare both backends on the same metric
([drift suite](sim/README.md#localization-drift-suite)). The drift launch
rejects `backend:=slam` and no pose graph ships; `auto.launch.py` can
localize against one given as `map_file`.

SLAM here means `mapping` mode: slam_toolbox builds the map and localizes on
it, with the EKF allowed, one map carried from game to game (load at boot,
extend during the game, save after). Earlier `slam --use-rf2o` read worse
than plain `slam`, likely because slam_toolbox's correction stacked on the
EKF's rf2o correction ([sentry_localization](sentry_localization/README.md));
fix that, don't drop the EKF.

1. Fix the EKF stacking, for example by pointing slam_toolbox's `odom_frame`
   at raw odometry, then retune `slam.yaml`.
2. Carry the map across games: `serialize_map` after each game, load at the
   next boot with `load_map:=true` from the known spawn pose
   (`map_start_pose`). `localization.launch.py` hard-codes `[0, 0, 0]` for
   saved maps; expose the configured field spawn instead. Before the
   Battle, give it a mapping window (a short scripted lap, if the Setup
   Period rules allow moving). Robots from past games must not pile up in
   the map.
3. A game-like scenario: a full 5-minute Battle with other `sentry_v2`
   copies driving, spinning and blocking the lidar (track A's opponents),
   our robot on a match-like route with `real_accel`'s 1.2 m/s^2, including
   the high ground. Score pose error against truth and check the map
   doesn't keep robots as walls (T3: sample the grid cells the actors
   crossed, the `TODO` in `_run_cornering_loop_scenario`). Implement it
   first in `mapping` mode from a blank map; review the unmerged `sim`
   branch `t3-actor-map-check` before reusing it. Carried-map tests need a
   saved pose graph that rasterises in seconds.

**Done when:** SLAM with the EKF passes the drift scenarios amcl passes,
each within 0.05 m of amcl's error, and stays within 0.05 m of amcl on the
game-like scenario too. Run that scenario as three games in a row on one
carried-over map: the error must not grow from game to game, and the map
must not collect robots or duplicate walls.

### J. Lidar and camera

T22 and T23's robot half are later, needing a robot (the user, 2026-10-08).

- T22: Can the RPLIDAR's points per scan and scan rate change, and would it
  help (the user, 2026-10-02)? Open: which modes and rates our model
  supports and whether `sllidar_node` exposes them (`auto.launch.py` sets
  only port, baud and frame); what runs today; whether more points or a
  faster scan help rf2o, the EKF, amcl or the map; the cost in range,
  noise, Orin CPU and USB bandwidth; and whether a faster scan cuts the
  skew while the head turns (T23).
- T23: Does the patrol hurt the lidar (the user, 2026-10-02)? The lidar is
  on the head, so `point_to_cv_target`'s patrol turns it at 2 rad/s (about
  0.2 rad per scan at 10 Hz), where a held head keeps it still in the
  world. Check rf2o, the EKF and the map with the patrol on against off, in
  sim and on the robot. If it hurts, use the lidar to find robots and only
  turn the gun toward them instead of patrolling all the time.
- T19: See if the depth camera is actually needed (the user, 2026-10-01).
  On the robot `roi_depth_node` ranges each detection off the D435's depth;
  no sim test uses depth (`detector_standin` feeds 3D truth). Without it,
  range would have to come from the colour image.

## Later: needs a robot

Robot work waits; sim work goes first (the user, 2026-10-08). Tracks B, C
and J mark their robot parts the same way. Deployment and validation
status: [hardware status](JAZZY_FLASH.md#hardware-status).

- T21: The sentry's real-floor runs. The 2026-10-04 practice field went
  well, but no localization runs happened (the user, 2026-10-08), so the map
  layer is still unjudged. `auto.launch.py` defaults to `mapping` from a
  blank map and `map_autosaver` saves the map every 30 s to
  `maps/<boot time>/`. Bring back maps and `~/logs/thornbots-run<N>/` (each
  `.log` and its bag: `/tf`, `/scan`, `/scan_odom`, `/localization/odom`,
  `/localization/map_odom`) to judge it offline: `map->odom` matched the
  EKF in sim but never beat it, since sim's EKF barely drifts; real floors
  over 5-minute runs decide. A run ended by a battery pull needs
  `ros2 bag reindex <dir>/bag -s mcap`. Left: one boot air-gapped with
  Wi-Fi turned on mid-run (T27).

  Shots (the user, 2026-10-02). The team's firmware is MCBV3
  `position-based-cv`: it takes our 15-byte `CV_TARGET`
  ([UART_PROTOCOL](ros2_dji_serial_bridge/UART_PROTOCOL.md)), aims at x/y/z
  less its own odometry and fires `delay_ms` after receipt. New format only;
  the bridge doesn't fall back to the old one (the user, 2026-10-02).
  - Flash the matching firmware: MCBV3 `nightly` (pinned here) has pitch
    for `z` above the pivot and rep-105's one field frame (Thornbots/MCBV3#77,
    closed). Not flashed; deploy firmware and ROS stack together.
  - Patrol sweeps the gun with no target, fire clear; the firmware fires on
    bit 0 alone (the user, 2026-10-04). T31 decides when to allow its turn
    toward a hit.
  - Acceptance checks: depth on a lit panel, bridge diagnostics `pose>0`,
    muzzle under 25 m/s, `POSE`'s x/y in the field frame (a panel straight
    ahead lands straight ahead of `root`; driving 1 m fires no RELOCALIZE
    every 0.3 s). First shots on a stand, eye protection on, e-stop in
    reach.
  - Timing (the user, 2026-10-04): `delay_ms` runs from MCB receipt but is
    computed at decision, transit not taken off (`mcb_relay` takes off its
    RELOCALIZE latency); our `firmware_latency_s` 0.05 and the firmware's
    80 ms `FIRING_LATENCY_TIME` both cover the indexer, so spinning-target
    shots go ~50 ms early. Measure the indexer, then one side owns it.
- T27: The camera container dies when NTP steps the clock (2026-10-03,
  sentry): the RTC resets to 1970, Wi-Fi NTP steps it forward, RealSense
  stamps go wild and `component_container_mt` aborts. Mitigated in
  `Realsense_ROI_Depth_Rectifier` and `isaac-ros-startup` ("Clock steps
  restart the stack" in its README). Left: a sentry boot with Wi-Fi (T21).
- T34: Look into boot time more (the user, 2026-10-04). Missing: power-on to
  kernel (UEFI, not in `systemd-analyze`), time to the stack being useful
  (first detection, first `CVTarget`, first `map->odom`), hero and
  standard, and the rebuilt Jazzy image. Time it with a stopwatch from
  power-on alongside the `[boot]` lines, then cut the longest stage. Target
  stays under 1 min.

## Caveats

- Sim detection noise is 0.005 m against a D435's centimetres, and no sim
  test runs YOLO, so every CV rate here runs optimistic. The benches rank
  changes; they don't predict the field.
- `odom_stuck` loses the robot at 4 m/s with `/odom` frozen, accepted as a
  limit (2026-09-25).
- Neither CV bench runs gz; the drift suite does. SAPIEN is out for good.
- Nobody has checked what `sentry_v2` does when driven into a wall. That
  matters once obstacle avoidance has to be demonstrated.

## Issues found

From the 2026-10-08 test sweep (Mac, workspace `a65e025`). Move each to a
track or todo once someone owns it.

- The EKF lost accuracy since 2026-09-28: fused error 0.023 and 0.050 m in
  two runs against 0.007-0.020 m, a per-run offset rather than drift. The
  field-frame move (2026-10-04) landed between; bisect from there.
- The map-based drift scenarios read 0.23-0.24 m against 0.15-0.19 m on
  2026-09-28. Still under the 0.40 m limit; investigate the regression.
- `mcb_drive` passes on 0 hits (track A).
