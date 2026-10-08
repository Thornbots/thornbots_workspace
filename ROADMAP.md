# Where the project is going

A localization suite we can believe, CV split at `TargetState` with a bench
for each half, then the CV stack from detections to gimbal tested end to
end in sim. Updated 2026-10-03. Aiming is done, the estimation bench has
limits on all 60 cells, the match test's E1 scores, and `main` has been
Jazzy since 2026-09-27. Humble is frozen on the `humble` branches.

This file lists only work still to do. Delete an item when it's finished,
then commit and push; don't mark it done. Git history and the package docs
keep the record.

## Where we actually are

| Thing | State |
|---|---|
| Localization drift suite (9 scenarios) | **8 of 9 pass** at `--backend amcl --use-rf2o`, unthrottled, GUI on, 378 s, RTF 1.25 (archlinux, 2026-10-03): with obstacle 0.16 m, moving obstacles 0.16 m, real_accel 0.12 m, against 0.40 m; noise_correction growth 1.15, scan_degraded 0.45 m during. drift_correction failed bring-up, not drift: no `map->odom` in 45 s after the harness's one restart (T30). Last full pass 9 of 9, ~285 s, 2026-09-28 (drift_correction 0.16-0.18 m). One gz session per run, `sentry_v2` with collision and sprung wheels |
| EKF fusion | **90-95% better than raw `/odom`** (0.007-0.020 m vs 0.15-0.25 m mean, `suite:=ekf`, five runs 2026-09-28) |
| Estimation bench | [Commands and behavior](sim/README.md#run-the-tests), [dated results](sim/docs/cv-bench-results-2026-09-28.md), and [remaining accuracy work](#g-estimation-accuracy) |
| CV end to end in sim | **E1 scores** (`ros2 launch sim e2e.launch.py`, 2026-09-29): stationary ~100% hits, 2 m/s 0-11%. The gimbal follows the aim within ~1 deg and `roi_depth_node` sits 2.7 cm from truth; `target_tracker`'s velocity is 0.86 m/s off at 2 m/s (`sim/AGENTS.md`). E2 runs `position-based-cv` `f835be1` over the wire with the three fixes asked of it: 28/40 hits on a clean still track, a few % when E1's tracking goes bad (T17) |
| Jazzy | Laptop validation is recorded in [JAZZY_FLASH.md](JAZZY_FLASH.md#laptop-validation-2026-09-30); current machine and hardware-check status is in [Hardware status](JAZZY_FLASH.md#hardware-status) |

## Short todos

For Sunday 2026-10-04 (T21). Pointers lead to the detail, and numbers
stay put when items are deleted or move to a track (T3 to H; T7, T8 and
T15 to G; T17 to A; T20, T25 and T29 to C; T24 and T30 to E; T19, T22
and T23 to J).

Robot ops:

Current deployment and validation status: [JAZZY_FLASH.md](JAZZY_FLASH.md#hardware-status).
The dated boot/run observations below do not establish hardware acceptance.

- T21: Sunday 2026-10-04, the sentry on an unknown practice field (the
  user, 2026-10-02). The MCB team updates the auto-drive route for the
  field. Our side: `auto.launch.py` defaults to `mapping` from a blank map
  at boot, `mcb_relay` keeps relocalizing from rf2o + EKF
  (`/localization/odom`), and `map_autosaver` saves the map every 30 s to
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

  Shots on Sunday (the user, 2026-10-02). The firmware the team runs is
  MCBV3 `position-based-cv` (`0885a69`, contains `newMain`): it takes our
  15-byte `CV_TARGET` as `UART_PROTOCOL.md` has it, aims at x/y/z less its
  own odometry and fires `delay_ms` after receipt. New format only: the
  bridge doesn't fall back to the old one (the user, 2026-10-02).
  - Done: with no team colour, `target_selector` shoots at all targets.
    `robot_id` 0 (no referee) used to read as red (`thornbots_pkg` `ba37481`).
  - Firmware, MCB team (Thornbots/MCBV3#77): the two fixes in the
    bridge README "Asked of the firmware", redone against `0885a69`
    (2026-10-04; they build what we ask, the user 2026-10-03). The aim
    in one frame, REP-105 (its yaw already is, its odometry isn't), and
    pitch for `z` above the pivot (else every shot is 0.39 m high). The
    pitch fix is in `position-based-cv` `023802c`. rep-105 (2026-10-04,
    every repo) does the first and more: one field frame, (0, 0) at the
    field centre, x toward blue's base, in the firmware, on the wire, in
    `odom`, `map`, the maps and the sim world; `mcb_x_right` is gone. The
    emulator ports rep-105 at `cf42375`, before the rebase onto `023802c`
    (track I). Not on the robot, not flashed.
  - YOLO runs at about 58 fps (the user, 2026-10-02).
  - Patrol: `point_to_cv_target` sweeps the gun with no target, fire
    clear; the firmware fires on bit 0 alone (the user, 2026-10-04). On
    the robot, check the sweep direction. Turning toward a hit is
    firmware-only and works.
  - Robot acceptance checks: depth on a lit panel, bridge diagnostics `pose>0`, muzzle under 25 m/s. The
    `odom` point rides on our TF, so check `POSE`'s x/y axes under
    `mcb_x_right` (`head_yaw` is fixed): a panel straight ahead should
    land straight ahead of `root`, and driving 1 m shouldn't fire a
    RELOCALIZE every 0.3 s.
    First shots on a stand, eye protection on, e-stop in reach.
  - First detections on the sentry on Jazzy (run00051, 2026-10-04):
    none for 3 min, then 48 frames of class 1 (scores 0.65-0.82) over
    9 s, tracked (`tracking robot 1`), 6 fire frames sent with
    `delay_ms` 0, then ~60/s at 13:05:30. Whether it shot is the
    MCB's side. Capture to tracker update 59 ms mean.
  - Timing, after Sunday (the user, 2026-10-04): `delay_ms` runs from
    MCB receipt but is computed at decision, transit not taken off
    (`mcb_relay` takes off its RELOCALIZE latency); our
    `firmware_latency_s` 0.05 and the firmware's 80 ms
    `FIRING_LATENCY_TIME` both cover the indexer, so spinning-target
    shots go ~50 ms early. Measure the indexer, then one side owns it.
  - The MCB reports `robot_id` 3, red, with `hp` 100 and stage 0
    (run00051), so the selector shoots blue only. Check that's the
    field's referee and not a stale MCB value; robot_id 0 passes all.
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
- T34: Look into boot time more (the user, 2026-10-04). Track C's one
  measurement is the sentry on 2026-10-01: engine loaded about 21 s from
  kernel start. Missing: power-on to kernel (UEFI, not in
  `systemd-analyze`), time to the stack being useful (first detection,
  first `CVTarget`, first `map->odom`), hero and standard, and the
  rebuilt Jazzy image. Time it with a stopwatch from power-on alongside
  the `[boot]` lines (`isaac-ros-startup` README.md "Boot time"), then
  cut the longest stage. Target stays under 1 min.

CV:

- T31: Tell the Type C when not to turn toward a hit (the user,
  2026-10-04). `turn_to_hit` (`CVTarget` bit 2) reaches the MCB with every
  frame, but `point_to_cv_target` sends its `turn_to_hit` parameter
  unchanged (default true). Decide it per frame instead. First rule: clear
  it while we hold a valid `TargetState`, so a hit can't pull the gun off
  a target we're shooting. The same rule should gate our own patrol's
  hit turn (`hit_turn_s`). Check the firmware ignores hits when the bit
  is clear before relying on it.
- T32: Choose the right panel on a robot that isn't spinning (the user,
  2026-10-04). Below `spin_exit_rad_s`, `plan_shot`
  (`point_to_cv_target_core.py`) leads the panel whose yaw is nearest the
  bearing to us, rounded per tick. Near 45 deg two panels face us about
  equally and the pick can flip tick to tick, swinging the gun a panel's
  width; it also leans on the tracker's yaw, weakest there (T15,
  `stationary45`). Want: the most face-on panel, held with hysteresis
  until another is clearly better. Measure on the aiming bench at 45 deg.
- T33: A patrol flag on `CVTarget` (the user, 2026-10-04). Our patrol
  points go out as aim points with `fire` clear, so the MCB can't tell a
  sweep from a target we're holding fire on. Add a bit (bit 3, reserved
  today) set on every patrol point: `CVTarget.msg`, the bridge's packing,
  `UART_PROTOCOL.md`, `point_to_cv_target` and the MCB emulator. Ask the
  MCB team to adopt it with the bridge README's "Asked of the firmware".

## Tracks, in order of work

Finish the short todos first, then A-C in order, with I before A's E2,
then G. D runs alongside A, and E, F, H and J are unscheduled. Navigation comes after the Midwest competition;
until then the match test drives our robot from sim.

### A. The match test

[`E2E_PLAN.md`](E2E_PLAN.md), stages `mcb_parked`, `mcb_drive` and `mcb_match` (were E1-E4). Sim plays only the MCB over a
pty, a detector stand-in for YOLO, lidar and depth. Our robot drives and
shoots against other `sentry_v2` copies with the real code in between.
Stages: the stand-in to the gimbal with our robot parked, then the serial
link against an MCB emulator, then driving while shooting, then opponents
that shoot back.

- T17: Runs with the same inputs should score nearly the same (the user,
  2026-09-28). The estimation bench runs in lockstep now and every cell's
  p95s repeat to 1.03x (five Mac runs, 2026-10-01), close enough that one
  run is a benchmark; exact repeats aren't the goal. The aiming bench
  already is: three Mac runs 2026-10-01, cells within 0.5 points, worst
  `staggered-speed4` 0.968-0.981. E1 isn't, and looks broken since
  2026-09-29: three runs failed 11, 10 and 8 of 12 cases, most firing no
  shots at all (both still radial and diagonal cells in every run), only
  stationary-lateral hitting 95-100%. 2026-10-03: every radial and
  diagonal cell gets no valid `TargetState`, even run alone from a fresh
  stack (a still target at (3.5, 0) gets 5 detections in 15 s, one at
  (3.0, 0) hits 100%). So it's E1's sim, not the CV nodes: look at
  `detector_standin`'s 0.1 m depth check against where the gz opponent
  really is. Find why before measuring its spread. Left: drift and EKF runs, not yet measured.

### I. MCB emulator

The emulator now compiles the checked-out MCBV3 C++ code and supplies fake
hardware interfaces (the user, 2026-10-06). The Python control port is removed.
`MCB-project/src/hosted/` supplies lockstep time, sensor readings, CAN feedback
and UART-to-pty plumbing; the actual SentryControl, scheduler, parsers,
aim/fire and drive commands run. `sim mcb.launch.py` runs it against gz and
the real ROS bridge; every `e2e.launch.py` stage uses the same executable.
`sim/README.md` documents the build, tests and hardware-model limits.

Native control and real-bridge tests cover pose/referee output, ping,
aim/fire, relocalize, malformed frames, stage gating and both drive modes.
`mcb_parked` scores on field-safe paths, with no blanket skips or xfail. The
Odometry twist uses the child frame throughout sim; consumers rotate it
into their parent frame. `mcb_drive`/`mcb_match` run spawn-to-center routes and record
localization, head-TF and tracking failures alongside combat scores.
Moving accuracy, repeated-run floors and `mcb_match` segment equivalence remain open.
Motor feedback and
MCU timing remain models; next steps:
- Wire physical CAN motor feedback and dynamics to gz instead of applying
  firmware setpoints through gz's existing controllers.
- A real Type C emulator (the user, 2026-10-03): emulate the board's
  STM32F407 and run the same `.elf` we flash, not a host build. It's the
  only way to catch what the host build hides: the real UART and DMA
  drivers, interrupt timing, the 1 kHz loop's overruns, `-O` and float
  behaviour. Candidates to check first: Renode (STM32F4 platforms, UART to
  pty) and QEMU's STM32F405 board. Peripherals to model: the Jetson UART on a
  pty, the referee UART, the remote's DBUS, the BMI088 IMU on SPI, and the
  DJI motors on CAN, bridged to gz. The hosted build is now in place.

**Done when** the emulator runs the firmware's Jetson, aim-and-fire and
auto-drive logic against `dji_serial_bridge` on a pty, and every
`e2e.launch.py` stage scores through it.

### B. Hit while we move

After track A's E3, agree the remaining wire and firmware work with the
MCB team. The [CV interface](thornbots_pkg/README.md#cv-interface) is
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
(kernel start, not power-on; `isaac-ros-startup` `AGENTS.md`). 2026-10-04:
`quiet` kernel, no RealSense reset on the first start: camera up at a
median 19.6 s (was 29 s). Open: 1 of 12 `quiet` boots lost the GPU
(`isaac-ros-startup` reboots on it), and the firmware time before the
kernel. `robot_setup.sh`,
the keyboard-free USB installer (`isaac_ros_common`) and the Jazzy boot
service (`isaac-ros-startup`) moved to `main` on 2026-10-01, untested,
because hero's stick (`make_installer_usb.sh --robot hero`) clones `main` on
first boot. Hero's stick bounced back to the boot menu; started from the
UEFI Shell instead, the install ran 2026-10-01 (`JAZZY_FLASH.md` step 3 has
the workaround for standard). Check `journalctl -u robot-firstboot` on
`ts-nano-hero`.

- T20: A better log format on the robots (the user, 2026-10-01). Today
  each boot-service run is one text file of console output
  (`isaac-ros-startup` `log-stamp.py`: uptime and wall-time prefix, run
  counter for a name). About 75% of its lines are `dji_serial_bridge`'s
  per-frame `ref_sys RX` (10 Hz) and `relocalize TX` INFO lines
  (`debug_log` defaults true). Done 2026-10-02: each run also records
  an MCAP bag of `/rosout` plus the localization, lidar, referee and CV
  topics, keeps the ROS node logs, and prunes old runs by free disk
  (`isaac-ros-startup` README.md "Per-run bag"), untested on a robot.
  Left: the bridge's per-frame logs at DEBUG or throttled, throttled
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
  Building on the Mac mini is a stopgap, not the way forward. `ts-nano-dev`'s local
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
  layouts. Fix the tracker, then give `stationary45` its `LIMITS`.
- T7: Sweep `process_noise_accel` against the velocity-error trace, path
  ends included.
- T8: Check the bench scores the same with a cell run alone as in sequence.

### D. Faster suites

[`E2E_PLAN.md`](E2E_PLAN.md) "Speed". Log each suite's wall-time split,
find why the full gz stack caps at RTF ~1.55, render only what gets scored.
Suites run one at a time; we are compute-limited.

Keep the gz camera off (`camera:=false`, the default) in every suite but
the match test, which runs it depth-only (`e2e.launch.py`). A subscribed
RGB-D camera alone caps a bare server near RTF 2.2. Only E1 and E2 use
it, through `depth_camera_emulator` into the real `roi_depth_node`; the CV
benches make 3D detections directly and the drift and EKF suites run
camera-off. If T19 finds depth isn't needed, the match test can drop the
camera too.

### E. Benches that start and stop cleanly

Today a fresh container has no gz until `install-sim.sh` runs, and nothing
says so until a launch fails. Nodes cold-start into live topics (TF has run
0.6 s behind), and a lost lifecycle reply can leave `amcl` or `map_server`
unconfigured; the drift harness restarts such a stack once, the robot's
boot doesn't. Ctrl-C prints a traceback from every Python node (bare
`rclpy.spin`). A launch whose shell dies leaves orphans that
`kill_launch.sh -l` can't see.

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
- T24: One name per test, for what it tests, used by its launch file,
  test file and the docs alike (the user, 2026-10-03). After Sunday.
  Each has three names today ("aiming bench" is `shot_hit.launch.py` and
  `test_shot_hit.py`). New names:
  - `localization_drift` (was `localization_tests.launch.py`, the drift suite)
  - `ekf` (was `suite:=ekf`, `test_ekf_ground_truth.py`)
  - `aim` (was `shot_hit`, the aiming bench)
  - `tracking` (was `estimation`, the estimation bench)
  - `mcb_parked`, `mcb_drive`, `mcb_match` (were E1/E2, E3, E4; done
    2026-10-08: every stage runs the MCB emulator, E1's stand-in is gone)

  The CV plan names go too. About 200 doc
  references across 20 files, plus the isaac-ros-docker skill.

### F. CV nodes into their own repo

Later, not before Sunday (the user, 2026-10-02). Move most of the CV
aiming code, `target_selector`, `target_tracker` and `point_to_cv_target`
with its patrol, their `*_core.py` and tests, from `thornbots_pkg` to a new
`thornbots_cv` package in its own repo.
`thornbots_pkg` keeps the hardware interface, URDF, TF and `mcb_relay`. A
new submodule means a new `Thornbots/` repo, a `.gitmodules` entry and a
`Dockerfile.thornbots` build line. Everything naming
`package='thornbots_pkg'` for those nodes follows: `auto.launch.py` (with
its UDP-only DDS pinning) and `sim`'s `sim.launch.py`, `shot_hit.launch.py`,
`estimation.launch.py` and `e2e.launch.py`. Do it between bench runs, and re-run both
benches after to show nothing moved.

### H. SLAM at amcl's level

Keep SLAM a real fallback to amcl. amcl with the EKF passes all nine drift
scenarios, the map-based ones at 0.15-0.19 m (2026-09-28). `slam` was last tuned 2026-07
on the old stack, at 0.31-0.33 m, localizing against the saved field map.
The drift suite scores `--backend mapping` against truth since 2026-10-02:
with `--use-rf2o` it passes all nine, the cornering loops at 0.02-0.09 m;
without, it fails five (`sim/README.md`). amcl's 0.15-0.19 m is its
`map->odom` change, not truth error, so compare on the same metric.

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
   (`map_start_pose`). Before the Battle, give it a mapping window: a short
   scripted lap, if the rules allow moving then (check the Setup Period
   rules). Moving robots from past games must not pile up in the map.
3. A game-like scenario: a full 5-minute Battle on the field with other
   `sentry_v2` copies driving, spinning and blocking the lidar (track A's
   opponents), our robot driving a match-like route with finite
   acceleration (`real_accel`'s 1.2 m/s^2), including the high ground. Score pose error against
   truth throughout, and check the built map doesn't keep robots as walls
   (T3: sample the grid cells the actors crossed, the `TODO` in
   `_run_cornering_loop_scenario`; the check is on `sim` branch
   `t3-actor-map-check`. Blocked: with the ARCC26 pose graph loaded,
   slam_toolbox never publishes `/map`, `getOccupancyGrid` ran 600 s at
   100% of a core on 2026-09-28. Needs a map that rasterises in seconds).

**Done when:** SLAM with the EKF passes the drift scenarios amcl passes,
each within 0.05 m of amcl's error, and stays within 0.05 m of amcl on the
game-like scenario too (run both there). Run that scenario as three games
in a row on one carried-over map: the error must not grow from game to
game, and the map must not collect robots or duplicate walls.

### J. Lidar and camera

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
  Today `roi_depth_node` ranges each detection off the D435's depth, and
  the match test runs a gz depth camera for it (track D: an RGB-D camera
  alone caps gz near RTF 2.2). Without it, range would have to come from
  the colour image.

## Caveats

- Sim detection noise is 0.005 m against a D435's centimetres, and no sim
  test runs YOLO, so every CV rate here runs optimistic. The benches rank
  changes; they don't predict the field.
- `odom_stuck` loses the robot at 4 m/s with `/odom` frozen, accepted as a
  limit (2026-09-25).
- Neither CV bench runs gz; the drift suite does. SAPIEN is out for good.
- Nobody has checked what `sentry_v2` does when driven into a wall. That
  matters once obstacle avoidance has to be demonstrated.
