# Where the project is going

A localization suite we can believe, CV split at `TargetState` with a bench
for each half, then the CV stack from detections to gimbal tested end to
end in sim. Updated 2026-10-09. Aiming is done; the estimation bench has
limits on 72 keyed cells, but its two default `stationary45` cells still
lack accuracy limits. Every match-test stage runs the compiled MCB
firmware, and `main` has been Jazzy since 2026-09-27. Humble is frozen on
the `humble` branches.

This file lists only work still to do. Delete an item when it's finished,
then commit and push; don't mark it done. Git history and the package docs
keep the record.

## Where we actually are

| Thing | State |
|---|---|
| Localization drift suite | Native suite passes on ARM64; startup races remain T30. [Suite design](sim/README.md#localization-drift-suite), [latest validation](https://github.com/Thornbots/sim/commit/4e9445a) |
| EKF fusion | Native ground-truth suite passes on ARM64. [Suite design](sim/README.md#ekf-ground-truth-suite), [latest validation](https://github.com/Thornbots/sim/commit/4e9445a) |
| Estimation bench | [Commands and behavior](sim/README.md#run-the-tests), [dated results](sim/docs/cv-bench-results-2026-09-28.md), and [remaining accuracy work](#g-estimation-accuracy) |
| CV end to end in sim | Native aiming, tracking and driving suites pass on ARM64/x86_64; match passes on ARM64 but an x86_64 run caught allied intersections. Parked moving-target cells and repeatability remain open (T17); passing drive/match diagnostics do not establish combat accuracy. [Latest validation](https://github.com/Thornbots/sim/commit/4e9445a) |
| Jazzy | Laptop validation is recorded in [JAZZY_FLASH.md](JAZZY_FLASH.md#laptop-validation-2026-09-30); current machine and hardware-check status is in [Hardware status](JAZZY_FLASH.md#hardware-status) |

## Short todos

Pointers lead to the detail, and numbers stay put when items are deleted
or move to a track (T3 to H; T7, T8 and T15 to G; T17 to A; T20, T25
and T29 to C; T24 and T30 to E; T19, T22 and T23 to J).

CV:

- T31: Tell the Type C when not to turn toward a hit (the user,
  2026-10-04). `turn_to_hit` (`CVTarget` bit 2) reaches the MCB with every
  frame, but `point_to_cv_target` sends its `turn_to_hit` parameter
  unchanged (default true). Decide it per frame instead. First rule: clear
  it while we hold a valid `TargetState`, so a hit can't pull the gun off
  a target we're shooting. The same rule should gate our own patrol's
  hit turn (`hit_turn_s`). The firmware already honours the bit
  (MCBV3 `AutoAimAndFireCommand.cpp`, 2026-10-08): clear, it ignores hits
  and ends a turn in progress; set, a hit overrides a live CV target for
  `HIT_TURN_DURATION` (500 ms), which is the problem. Also repair the hit
  input: `HitTracker::addHit` converts already-radian IMU yaw by `PI/180`,
  and its one-cycle `isHit` value can be missed by the 10 Hz REF_SYS sample.
  Establish the angle's units/reference and latch hits until reported;
  test with nonzero head/chassis yaw before trusting `hit_angle_sign`.
  Current behavior is in [firmware coordination](ros2_dji_serial_bridge/README.md#where-the-firmware-stands).
- T32: Choose the right panel on a robot that isn't spinning (the user,
  2026-10-04). Below `spin_exit_rad_s`, `plan_shot`
  (`point_to_cv_target_core.cpp`) leads the panel whose yaw is nearest the
  bearing to us, rounded per tick. Near 45 deg two panels face us about
  equally and the pick can flip tick to tick, swinging the gun a panel's
  width; it also leans on the tracker's yaw, weakest there (T15,
  `stationary45`). Want: the most face-on panel, held with hysteresis
  until another is clearly better. Measure on the aiming bench at 45 deg.
- T33: A patrol flag on `CVTarget` (the user, 2026-10-04). Our patrol
  points go out as aim points with `fire` clear, so the MCB can't tell a
  sweep from a target we're holding fire on. Add a bit (bit 3, reserved
  today) set on every patrol point: `CVTarget.msg`, the bridge's packing,
  `UART_PROTOCOL.md`, `point_to_cv_target`, sim's wire helper
  (`sim/src/mcb_protocol.cpp`) and MCBV3's `JetsonSubsystem.hpp`,
  which the emulator compiles. Ask the MCB team to adopt it with the
  [bridge firmware asks](ros2_dji_serial_bridge/README.md#asked-of-the-firmware).

## Tracks, in order of work

Sim work first; robot work waits for [later](#later-needs-a-robot) (the
user, 2026-10-08). Finish the short todos, then A, then G, then the sim
parts of B and C. D runs alongside A, and E, F, H and J are
unscheduled. Navigation comes after the Midwest competition;
until then the match test drives our robot from sim.

### A. The match test

[`E2E_PLAN.md`](E2E_PLAN.md), stages `mcb_parked`, `mcb_drive` and
`mcb_match` (`sim/README.md`). Sim plays the MCB with the compiled firmware
over a pty, `detector_standin` in place of YOLO and `roi_depth_node`, and
lidar. Our robot shoots, parked or driving, against other `sentry_v2`
copies with the real code in between; in `mcb_match` they shoot back.

- T17: Runs with the same inputs should score nearly the same (the user,
  2026-09-28). The aiming bench does (cells within 0.5 points over three
  runs, 2026-10-01). The estimation bench's moving cells can vary with the
  same seed (flat-speed4 facing p95 0.10 and 0.20 m, sim `80ddaa1`).
  `mcb_parked` doesn't: two runs 2026-10-08 (Mac, workspace `a65e025`)
  scored 8/12 and 7/12, failing different cells (speed1-radial 0% then
  30%, speed2-lateral 20% then 5%); sim `e834ba2` had 9/12 with
  stationary-lateral at 13%. Still targets hit 72-100%; moving ones
  0-30%. The worst cells are lost tracks, not aim: a third to under half
  the states, velocity error 2.2-2.5 m/s and spin rate off by up to
  6 rad/s, though the stand-in feeds truth. The aiming bench hits
  98-99% at every speed, so look at the tracker's input in gz (detection
  timing and stamps against `/clock`, the parked robot's odom walk in
  `odom_disagreement_m`) before the tracker. Lockstep gz is
  [`E2E_LOCKSTEP_PLAN.md`](E2E_LOCKSTEP_PLAN.md) (unfinished).
- `mcb_drive` passes with no hits: 2026-10-08, every segment 0% with
  "median aim error exceeds 0.10 m" and localization p95 0.46-0.91 m
  against truth. Make it fail on that, then find why localization is that
  far off while driving (the drift suite's 0.24 m is `map->odom` change,
  not truth error).

### I. MCB emulator

Every `e2e.launch.py` stage and `mcb.launch.py` run the checked-out MCBV3
code as a host build with fake hardware (`sim/README.md` "MCB emulator").
Its motor feedback and MCU timing are models. `mcb_drive` and `mcb_match`
drive our robot with `match_driver`, not the firmware's auto-drive, which
runs only in `mcb.launch.py` and the native tests.

- Wire physical CAN motor feedback and dynamics to gz instead of applying
  firmware setpoints through gz's existing controllers.
- A real Type C emulator (the user, 2026-10-03): emulate the board's
  STM32F407 and run the same `.elf` we flash, not a host build. It's the
  only way to catch what the host build hides: the real UART and DMA
  drivers, interrupt timing, the 1 kHz loop's overruns, `-O` and float
  behaviour. Candidates to check first: Renode (STM32F4 platforms, UART to
  pty) and QEMU's STM32F405 board. Peripherals to model: the Jetson UART on a
  pty, the referee UART, the remote's DBUS, the BMI088 IMU on SPI, and the
  DJI motors on CAN, bridged to gz.
- Drive `mcb_drive` and `mcb_match` with the firmware's auto-drive.

### B. Hit while we move

Later, needs a robot (the user, 2026-10-08), except the moving-shooter
aiming-bench runs, which are sim.

After track A's `mcb_drive` scores, agree the remaining wire and firmware
work with the MCB team. The [CV interface](thornbots_pkg/README.md#cv-interface) is
implemented; hardware validation remains unverified.

- Validate the [shared field frame](ros2_dji_serial_bridge/README.md#shared-aim-frame)
  on hardware with matching firmware and ROS revisions, including RELOCALIZE
  mailbox loss. The [POSE chassis-yaw proposal](ros2_dji_serial_bridge/UART_PROTOCOL.md#proposed-pose-chassis-yaw)
  remains unapplied; current heading-fixed aiming does not require it.
- Measure USB/read buffering and MCB sample-to-send delay before testing
  aiming while moving. A future MCB clock on the wire would need mapping to
  ROS time; it is a proposal, not the current stamp contract.
- Verify camera stamps survive YOLO, measure stamp-to-capture latency using
  metadata or a blinking LED, and set `camera_latency_s`.
- Measure the gimbal's roughly 7-degree chase jump settling, then set
  `chase_settle_s`.
- Run radial and diagonal aiming-bench paths with a moving shooter and add
  their missing floors.

Done when each moving match-test segment comes within 10 percentage points
of the same target cell with our robot parked. Record hardware results in
[hardware status](JAZZY_FLASH.md#hardware-status).

### C. Jazzy on the robots

Later, needs a robot (the user, 2026-10-08): the reflash, hardware
checks, boot time and T29. T20's bridge logging and T25's message can
land first, tested in sim against the MCB emulator.

Current migration state and unverified hardware checks live in
[JAZZY_FLASH.md](JAZZY_FLASH.md#hardware-status), alongside the flashing
instructions. Finish the remaining reflash and hardware checks. A Humble
performance comparison needs a recorded baseline; none is recorded in the
migration document.

Boot time: power-on to a running ROS stack under 1 min on each robot (the
user, 2026-09-30). The Jetsons used to run a minimized Ubuntu for this; the
7.2.1 installs are full `ubuntu-desktop` and boot to `graphical.target`
(sentry 15.0 s, dev 17.2 s, `systemd-analyze`).
`isaac_ros_common`'s `jetson_trim.sh` makes a robot headless. The sentry,
trimmed and running the Jazzy boot service, measured 2026-10-01: 13.6 s to
`multi-user.target`, both launches at 17.6 s, engine loaded about 21 s
(kernel start, not power-on). 2026-10-04:
`quiet` kernel, no RealSense reset on the first start: camera up at a
median 19.6 s (was 29 s). Open: 1 of 12 `quiet` boots lost the GPU
(`isaac-ros-startup` reboots on it), and the firmware time before the
kernel. Standard is the one robot left to flash (`JAZZY_FLASH.md` step 3
has the UEFI Shell workaround hero needed).

- T20: A better log format on the robots (the user, 2026-10-01). Today
  each boot-service run is one text file of console output
  (`isaac-ros-startup` `log-stamp`: uptime and wall-time prefix, run
  counter for a name). About 75% of its lines are `dji_serial_bridge`'s
  per-frame `ref_sys RX` (10 Hz) and `relocalize TX` INFO lines
  (`debug_log` defaults true). The per-run MCAP bag
  (`isaac-ros-startup` README.md "Per-run bag") records on the sentry;
  pruning old runs by free disk is untested. Left: the bridge's per-frame logs at DEBUG or throttled, throttled
  CRC and rf2o per-scan WARNs, its DIAG stats on `/diagnostics`.
- T25: Log any data from the MCB through a new message (the user,
  2026-10-03). Today the Jetson sees only what `POSE` and `REF_SYS`
  carry (plus `PING`, id 5, which the MCB echoes back), so the MCB's own state (mode, setpoints, what it did with a
  `CV_TARGET`, fire events, faults) is invisible after a run. Add a UART
  message the firmware can fill with any data, and have
  `dji_serial_bridge` publish it on a topic that the per-run bag records
  (T20). Open: a fixed struct or tagged key/value fields, its rate, and
  the bandwidth left on the 115200-baud link. Spec it in
  `UART_PROTOCOL.md` and land it on both sides (bridge, MCBV3).
- T29: Each robot builds its own image, faster (the user, 2026-10-03).
  Building on the Mac mini is a stopgap, not the way forward. Since
  2026-10-08 CI builds arm64 robot images natively and publishes them to
  GHCR per branch and workspace SHA ([docs/CI.md](docs/CI.md#robot-registry)),
  not yet pulled onto a robot. Decide whether pulling replaces building on
  the robot, then trim this item. `ts-nano-dev`'s local
  `build_robot_image.sh` took 29 min with `isaac_ros` and `realsense`
  cached: apt layer 502 s (5.46 GB re-downloaded because one package
  joined the `apt-get install` line), rosdep 84 s, colcon 172 s, and
  888 s exporting, which is the containerd image store gzipping each new
  layer on the CPU. To try: zstd or no compression on the local export;
  new apt packages in a small layer of their own, plus an apt cache
  mount; ccache in a cache mount for colcon; for code-only changes,
  `USE_WS_OVERLAY=true` and an incremental `colcon build`, no image.
  A robot with no BuildKit cache (image pulled, not built) rebuilds
  librealsense once. The `archlinux` laptop builds under QEMU on base
  layers copied once from the Mac mini (`SEED_FROM`), about 22 min for
  the thornbots layer (2026-10-03); shipping from it over `ssh -R` is
  untested (`isaac_ros_common/docker/README.md` "On the x86 laptop").
  The sentry built `8880173c` itself on 2026-10-04: 5.46 GB of apt
  again at ~2.3 MB/s over its Wi-Fi (~35 min), colcon 4 min 57 s, export
  ~10 min. Each robot is a USB device, so robots can't link to each
  other; the laptop's USB link to the sentry ran ~200 MB/s idle (the
  user), so carrying one robot's image to another via the laptop takes
  minutes where a build takes most of an hour.

### G. Estimation accuracy

Tuning waits until the stack works end to end (the user, 2026-09-29);
the match test runs on today's tracker. [Dated bench observations](sim/docs/cv-bench-results-2026-09-28.md)
record the errors behind these tasks.

| Step | Problem | Where to start |
| --- | --- | --- |
| G.1 | Radius and spin-rate outliers on some 4 m/s runs | Lower `process_noise_radius` and try an armor-radius prior; log innovations around spin misreads |
| G.2 | Radial depth error and staggered-panel handoff after blackouts | Tune `meas_noise_base_m` / `meas_noise_range_coeff` with `ray_covariance`; check `dz` pair parity across gaps |
| G.3 | Fresh tracks become `valid` before the estimate settles | Gate on track age or facing-panel predicted-versus-measured residual, rather than update count; check the aiming cost |

Each accuracy step is its own commit, scored over three estimation-bench
runs. Done when every cell passes limits tightened to the new worst runs,
radial and blackout error is within 1.5x of default, and no fresh track is
`valid` before facing-panel error settles under 5 cm. Include before/after
numbers in the commit message and update this track in the workspace bump.

- T15: A still target seen at an angle loses yaw and radius. The bench
  has `stationary45`, still at 45 deg with two panels in view (sim
  f47c84a). Four runs (2026-09-28), p95: staggered centre 0.064-0.071 m
  and `z_offset` 0.052-0.060 m (0.002 at yaw 0), yaw 0.12 rad on both
  layouts. Fix the tracker, then give the default `chassis_spin:=0`
  `stationary45` cells their `LIMITS`; only their `chassis_spin:=9` variants
  have limits today.
- T7: Sweep `process_noise_accel` against the velocity-error trace, path
  ends included.
- T8: Check the bench scores the same with a cell run alone as in sequence.

### D. Faster suites

[`E2E_PLAN.md`](E2E_PLAN.md) "Speed" and [`E2E_LOCKSTEP_PLAN.md`](E2E_LOCKSTEP_PLAN.md)
(unfinished). Every suite prints its wall-time split (`src/suite_timing.cpp`).
Find why the full gz stack caps at RTF ~1.55 and render only what gets
scored. Suites run one at a time; we are compute-limited. No suite runs the
gz camera (`camera:=false`); a subscribed RGB-D camera alone caps a bare
server near RTF 2.2.

### E. Benches that start and stop cleanly

Today a fresh container has no gz until `install-sim.sh` runs;
`tools/run_suite.sh` checks for it, a plain `ros2 launch` doesn't. Nodes cold-start into live topics (TF has run
0.6 s behind), and a lost lifecycle reply can leave `amcl` or `map_server`
unconfigured; the drift harness restarts such a stack once, the robot's
boot doesn't. The native port repairs shutdown races; verify interruption
and shell-death cleanup across the launch paths, including children that
`kill_launch.sh -l` cannot see.

**Done when:** each bench starts with one command, says if gz is missing,
waits for the stack before scoring, and on Ctrl-C or the end of the tests
stops every node it started, with no tracebacks and no orphans.

- T30: The robot stack's bring-up race fails drift scenarios (2026-10-03
  run, archlinux). 3 of 9 starts had no `map->root` after 30 s:
  `rf2o` can't look up `root -> lidar`, `amcl` comes up active but drops
  every scan as older than its TF. The harness's one restart
  (`_wait_for_root_chain`) saved drift_correction_obstacle and odom_stuck,
  not drift_correction. The robot can hit it at boot too. Find why the
  `root` chain is missing at start, rather than restart around it.
  2026-10-08: the drift suite's nine starts all came up first time, but
  `mcb_match` died in bring-up: `lifecycle_manager_localization` sent
  `map_server` its configure and heard nothing for 30 s (an `amcl`
  configure stall in sim `413502d`'s runs the same day).
- T24: One name per test, for what it tests, used by its launch file,
  test file and the docs alike (the user, 2026-10-03).
  Each has several names today ("aiming bench" is `shot_hit.launch.py` and
  `shot_hit_suite`). New names:
  - `localization_drift` (was `localization_tests.launch.py`, the drift suite)
  - `ekf` (now `suite:=ekf` in `localization_suite`)
  - `aim` (was `shot_hit`, the aiming bench)
  - `tracking` (was `estimation`, the estimation bench)

  The match-test stages are already `mcb_parked`, `mcb_drive` and
  `mcb_match`; stray E1-E4 and "Part 1/Part 2" names go too. About 160
  references to the old names across 41 files (2026-10-08), plus the
  isaac-ros-docker skill's `reference.md`.

### F. CV nodes into their own repo

Later (the user, 2026-10-02). Move most of the CV
aiming code, `target_selector`, `target_tracker` and `point_to_cv_target`
with its patrol, their C++ cores and tests, from `thornbots_pkg` to a new
`thornbots_cv` package in its own repo.
`thornbots_pkg` keeps the hardware interface, URDF, TF and `mcb_relay`. A
new submodule means a new `Thornbots/` repo, a `.gitmodules` entry and a
`Dockerfile.thornbots` build line. Everything naming
`package='thornbots_pkg'` for those nodes follows: `auto.launch.py` (with
its UDP-only DDS pinning, which `e2e.launch.py` includes) and `sim`'s
`shot_hit.launch.py` and `estimation.launch.py`; `sim`'s
`test/cpp/test_cv_bench.cpp` resolves `thornbots_pkg` assets. Do it between bench runs, and re-run both
benches after to show nothing moved.

### H. SLAM at amcl's level

Keep SLAM a real fallback to amcl. amcl with the EKF currently passes all
nine drift scenarios; the map-based ones read 0.23-0.24 m in the 2026-10-08
sweep ([current status](#where-we-actually-are)). That is `map->odom` change,
not truth error: compare both backends on the same metric.

The drift launch unconditionally rejects `backend:=slam`; it has no saved-map
override and no pose graph ships. Outside that suite, `auto.launch.py` can
localize against a pose graph supplied with `map_file`. The drift suite's
`--backend mapping` instead starts blank and scores against truth; it needs
no saved pose graph. Its dated results and backend behavior are in
[sim's drift suite](sim/README.md#localization-drift-suite).

SLAM here means `mapping` mode: slam_toolbox builds the map and localizes on
it, with the EKF allowed. It gets a mapping window before each game, and
carries one map from game to game: load it at boot, extend it during the
game, save it after. Earlier `slam --use-rf2o` read worse than plain `slam`,
likely because slam_toolbox's correction stacked on the EKF's rf2o
correction (`sentry_localization/README.md`); fix that, don't drop the EKF.

1. Fix the EKF stacking, for example by pointing slam_toolbox's
   `odom_frame` at raw odometry, then retune `slam.yaml`.
2. Carry the map across games. After each game, serialize the pose graph
   (slam_toolbox's `serialize_map`) and load it at the next boot with
   `load_map:=true` in `mapping` mode, starting from our known spawn pose
   (`map_start_pose`). Expose that pose from the configured field spawn:
   `localization.launch.py` currently hard-codes `[0, 0, 0]` for saved maps.
   Before the Battle, give it a mapping window: a short
   scripted lap, if the rules allow moving then (check the Setup Period
   rules). Moving robots from past games must not pile up in the map.
3. A game-like scenario: a full 5-minute Battle on the field with other
   `sentry_v2` copies driving, spinning and blocking the lidar (track A's
   opponents), our robot driving a match-like route with finite
   acceleration (`real_accel`'s 1.2 m/s^2), including the high ground. Score pose error against
   truth throughout, and check the built map doesn't keep robots as walls
   (T3: sample the grid cells the actors crossed, the `TODO` in
   `_run_cornering_loop_scenario`). Implement it first in `mapping` mode
   from a blank map; no pose graph blocks that check. Review the unmerged
   `sim` branch `t3-actor-map-check` before reusing it. Carried-map tests
   separately need a saved pose graph that rasterises in seconds.

**Done when:** SLAM with the EKF passes the drift scenarios amcl passes,
each within 0.05 m of amcl's error, and stays within 0.05 m of amcl on the
game-like scenario too (run both there). Run that scenario as three games
in a row on one carried-over map: the error must not grow from game to
game, and the map must not collect robots or duplicate walls.

### J. Lidar and camera

T22 and T23's robot half are later, needing a robot (the user,
2026-10-08).

What the sensors give, and whether we need them as they are.

- T22: Can the RPLIDAR's points per scan and scan rate change, and would
  it help (the user, 2026-10-02)? Questions, not answered yet:
  - Which scan modes and rates does our model support, and does
    `sllidar_node` (`auto.launch.py` sets only port, baud and frame) expose
    them?
  - What runs today: mode, points per scan, Hz?
  - Would more points or a faster scan help rf2o, the EKF, amcl or the
    map, and which matters more?
  - What does it cost: range, noise, CPU on the Orin, USB bandwidth?
  - Does a faster scan cut the skew while the head turns (T23)?
- T23: Does the patrol hurt the lidar (the user, 2026-10-02)? The lidar
  is on the head, so `point_to_cv_target`'s patrol (`thornbots_pkg`
  README, 2026-10-02) turns it at 2 rad/s, about 0.2 rad per scan at
  10 Hz, where a held head keeps it still in the world. Check rf2o, the EKF and
  the map with the patrol on against off, in sim and on the robot. If it
  hurts, use the lidar to find robots and only turn the gun toward them
  instead of patrolling all the time.
- T19: See if the depth camera is actually needed (the user, 2026-10-01).
  On the robot `roi_depth_node` ranges each detection off the D435's
  depth; no sim test uses depth since 2026-10-05 (`detector_standin`
  feeds 3D truth). Without it, range would have to come from
  the colour image.

## Later: needs a robot

Robot work waits; sim work goes first (the user, 2026-10-08). Tracks B,
C and J mark their robot parts the same way.

Current deployment and validation status: [JAZZY_FLASH.md](JAZZY_FLASH.md#hardware-status).
The dated boot/run observations below do not establish hardware acceptance.

- T21: The sentry's real-floor runs. Sunday 2026-10-04's practice field
  went well, but no localization runs happened (the user, 2026-10-08), so
  the map layer is still unjudged. Our side: `auto.launch.py` defaults to
  `mapping` from a blank map at boot, `mcb_relay` keeps relocalizing from
  rf2o + EKF (`/localization/odom`), and `map_autosaver` saves the map every 30 s to
  `maps/<boot time>/` on the workspace. Bring back the maps and logs to judge the map layer:
  `map->odom` averaged over 10 s matched the EKF in sim but never beat it,
  since sim's EKF barely drifts; real floors over 5-minute runs decide.
  The sentry boots `main`'s image (`8880173c`, built on it from
  `c87c97f`) with its own packages (`USE_WS_OVERLAY=false`) and
  `LOCALIZATION_MODE=mapping`, 2026-10-04 (run00051): stack up in 19.5 s,
  no `/pose` clash, bag filling. Left: one boot air-gapped with Wi-Fi
  turned on mid-run: no `[clock]` line, no restart, no `negative time
  point` abort, `systemd-timesyncd` inactive until the service stops.
  Bring back `~/logs/thornbots-run<N>/` with each `.log`: its bag holds
  `/tf`, `/scan`, `/scan_odom`, `/localization/odom` and
  `/localization/map_odom`, so the map layer can be judged offline. A run
  ended by a battery pull needs `ros2 bag reindex <dir>/bag -s mcap`.

  Shots (the user, 2026-10-02). The firmware the team runs is MCBV3
  `position-based-cv` (`0885a69`, contains `newMain`): it takes our
  15-byte `CV_TARGET` as `UART_PROTOCOL.md` has it, aims at x/y/z less its
  own odometry and fires `delay_ms` after receipt. New format only: the
  bridge doesn't fall back to the old one (the user, 2026-10-02).
  - Flash the matching firmware: MCBV3 `nightly` (pinned here) has
    both fixes asked in Thornbots/MCBV3#77 (closed), pitch for `z` above
    the pivot and rep-105's one field frame (x toward blue's base, (0, 0)
    at the field centre), the frame the ROS stack, maps and sim use since
    2026-10-04. Not on the robot, not flashed; deploy firmware and ROS
    stack together.
  - YOLO runs at about 58 fps (the user, 2026-10-02).
  - Patrol: `point_to_cv_target` sweeps the gun with no target, fire
    clear; the firmware fires on bit 0 alone (the user, 2026-10-04). Sweep
    direction checked on the robot 2026-10-04. The firmware's turn toward
    a hit works; T31 decides when to allow it.
  - Robot acceptance checks: depth on a lit panel, bridge diagnostics `pose>0`, muzzle under 25 m/s. The
    `odom` point rides on our TF, so check `POSE`'s x/y axes are the
    field frame's (`head_yaw` is fixed): a panel straight ahead should
    land straight ahead of `root`, and driving 1 m shouldn't fire a
    RELOCALIZE every 0.3 s.
    First shots on a stand, eye protection on, e-stop in reach.
  - First detections on the sentry on Jazzy (run00051, 2026-10-04):
    none for 3 min, then 48 frames of class 1 (scores 0.65-0.82) over
    9 s, tracked (`tracking robot 1`), 6 fire frames sent with
    `delay_ms` 0, then ~60/s at 13:05:30. Whether it shot is the
    MCB's side. Capture to tracker update 59 ms mean.
  - Timing (the user, 2026-10-04): `delay_ms` runs from
    MCB receipt but is computed at decision, transit not taken off
    (`mcb_relay` takes off its RELOCALIZE latency); our
    `firmware_latency_s` 0.05 and the firmware's 80 ms
    `FIRING_LATENCY_TIME` both cover the indexer, so spinning-target
    shots go ~50 ms early. Measure the indexer, then one side owns it.
- T27: The camera container dies when NTP steps the clock (2026-10-03,
  sentry). The RTC (`nvvrs-pseq-rtc`) resets the clock to 1970 at 10 s,
  after timesyncd restored it; with Wi-Fi, NTP steps it 56 years forward
  at ~49 s, RealSense stamps go wild and `component_container_mt` aborts
  (`cannot store a negative time point in rclcpp::Time`). Air-gapped,
  no jump. `Realsense_ROI_Depth_Rectifier` `d6caa99` no longer throws on
  such stamps; `isaac-ros-startup` now restores timesyncd's saved time after
  the RTC's hctosys, stops timesyncd for each run so Wi-Fi mid-match
  can't step the clock (it syncs between runs), and restarts the stack on
  any step over 1 s anyway (README.md "Clock steps restart the stack").
  Passes on `ts-nano-dev`'s host with `docker` stubbed (2026-10-03; dev
  has no camera). Left: a sentry boot with Wi-Fi, T21.
- T34: Look into boot time more (the user, 2026-10-04). Track C has the
  sentry's kernel-start numbers (2026-10-01, and camera up at 19.6 s with
  a `quiet` kernel on 2026-10-04). Missing: power-on to kernel (UEFI, not in
  `systemd-analyze`), time to the stack being useful (first detection,
  first `CVTarget`, first `map->odom`), hero and standard, and the
  rebuilt Jazzy image. Time it with a stopwatch from power-on alongside
  the `[boot]` lines (`isaac-ros-startup` README.md "Boot time"), then
  cut the longest stage. Target stays under 1 min.

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

From the 2026-10-08 test sweep (Mac, workspace `a65e025`: unit tests,
both CV benches, the three `mcb_*` stages, drift and EKF suites). Move each
to a track or todo once someone owns it.

- The EKF lost accuracy since 2026-09-28: fused error 0.023 and 0.050 m in
  two runs (RMS within 0.002 m of the mean, so a per-run offset rather
  than drift), against 0.007-0.020 m. The field-frame move (2026-10-04)
  landed between; bisect from there.
- The map-based drift scenarios read 0.23-0.24 m (drift_correction, with
  obstacle, moving obstacles), against 0.15-0.19 m on 2026-09-28. Still
  under the 0.40 m limit; investigate the regression against the dated baseline.
- `mcb_drive` passes on 0 hits (track A).
