# Where the project is going

A localization suite we can believe, CV split at `TargetState` with a bench
for each half, then the CV stack from detections to gimbal tested end to
end in sim. Updated 2026-10-01. Aiming is done, the estimation bench has
limits on all 60 cells, the match test's E1 scores, and `main` has been
Jazzy since 2026-09-27. Humble is frozen on the `humble` branches.

This file lists only work still to do. Delete an item when it's finished,
then commit and push; don't mark it done. Git history and the package docs
keep the record.

## Where we actually are

| Thing | State |
|---|---|
| Localization drift suite (9 scenarios) | **9 of 9 pass** at `--backend amcl --use-rf2o`, unthrottled, legs ramped at 20 m/s^2, ~285 s (2026-09-28, three runs): drift_correction 0.16-0.18 m, with obstacle 0.15-0.18 m, moving obstacles 0.17-0.19 m, real_accel (1.2 m/s^2) 0.09-0.11 m, against 0.40 m. One gz session per run, `sentry_v2` with collision and sprung wheels |
| EKF fusion | **90-95% better than raw `/odom`** (0.007-0.020 m vs 0.15-0.25 m mean, `suite:=ekf`, five runs 2026-09-28) |
| Estimation bench (60 cells, no gz) | **Limits on every cell** (2026-09-27). Stationary under 2 cm facing-panel p95, moving 0.08-0.19 m. About a quarter of runs trip one limit on a spin-rate or radius outlier. `CV_SPLIT_PLAN.md` has the detail |
| CV end to end in sim | **E1 scores** (`ros2 launch sim e2e.launch.py`, 2026-09-29): stationary ~100% hits, 2 m/s 0-11%. The gimbal follows the aim within ~1 deg and `roi_depth_node` sits 2.7 cm from truth; `target_tracker`'s velocity is 0.86 m/s off at 2 m/s (`sim/AGENTS.md`). E2 runs over the wire against the MCB emulator but fires nothing: the firmware refuses our `CV_MSG` (track I) |
| Jazzy | Laptop matches Humble on every suite and bench. `ts-nano-dev` and `ts-nano-sentry` on JetPack 7.2.1; hardware checks, the sentry's image and hero and standard left (track C) |

## Short todos

Nearly finished work. Pointers lead to
the detail, and numbers stay put when items are deleted or move to a
track (T3 to H, T7, T8 and T15 to G).

Repeatability:

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

CV:

- T19: See if the depth camera is actually needed (the user, 2026-10-01).
  Today `roi_depth_node` ranges each detection off the D435's depth, and
  the match test runs a gz depth camera for it (track D: an RGB-D camera
  alone caps gz near RTF 2.2). Without it, range would have to come from
  the colour image.
- T23: Does the patrol hurt the lidar (the user, 2026-10-02)? The lidar
  is on the head, so `point_to_cv_target`'s patrol (`thornbots_pkg`
  README, 2026-10-02) turns it at 2 rad/s, about 0.2 rad per scan at
  10 Hz, where a held head keeps it still in the world. Check rf2o, the EKF and
  the map with the patrol on against off, in sim and on the robot. If it
  hurts, use the lidar to find robots and only turn the gun toward them
  instead of patrolling all the time.

Lidar:

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

Robot ops:

- T21: Sunday 2026-10-04, the sentry on an unknown practice field (the
  user, 2026-10-02). The MCB team updates the auto-drive route for the
  field. Our side: `auto.launch.py` defaults to `mapping` from a blank map
  at boot, `mcb_relay` keeps relocalizing from rf2o + EKF
  (`/localization/odom`), and `map_autosaver` saves the map every 30 s to
  `maps/<boot time>/` on the workspace. The robot runs its image's
  packages (`USE_WS_OVERLAY=false`), so it needs a rebuilt image or the
  overlay. Bring back the maps and logs to judge the map layer:
  `map->odom` averaged over 10 s matched the EKF in sim but never beat it,
  since sim's EKF barely drifts; real floors over 5-minute runs decide.
  Before Sunday, on the sentry: pull `isaac-ros-startup`, `sudo bash
  install.sh`, restart the service, and check `~/logs/latest/bag/` fills
  with `.mcap` files (the per-run bag, T20; unproven on the robot image).
  Bring back `~/logs/thornbots-run<N>/` with each `.log`: its bag holds
  `/tf`, `/scan`, `/scan_odom`, `/localization/odom` and
  `/localization/map_odom`, so the map layer can be judged offline. A run
  ended by a battery pull needs `ros2 bag reindex <dir>/bag -s mcap`.

  Shots on Sunday (the user, 2026-10-02). CV can't reach the gun: the
  firmware (MCBV3 `708b8d6`, `newMain` untouched since 2026-09-27) drops
  our 19-byte `CV_TARGET` (the firmware's `CV_MSG`) on its size check; it
  still expects the 40-byte `CVData` that `dji_serial_bridge` `1962841`
  (2026-07-28) dropped. New format only: the bridge doesn't fall back to
  the old one (the user, 2026-10-02), so the firmware has to take
  `CV_TARGET` as `UART_PROTOCOL.md` has it.
  - Done: with no team colour, `target_selector` shoots at all targets.
    `robot_id` 0 (no referee) used to read as red (`thornbots_pkg` `ba37481`).
  - Firmware: Thornbots/MCBV3#74 (open, 2026-10-02) takes our message
    names and the 19- and 8-byte layouts, so `CV_TARGET` and `RELOCALIZE`
    frames get through; it compiles (gcc 10, all three robots) but doesn't
    aim or fire on CV yet. Thornbots/MCBV3#73 (open) lets the firmware
    build on Linux. Left, MCB team: aiming and firing on `CV_TARGET`,
    Thornbots/MCBV3#77 (bridge README "Where the firmware stands" items 2-4). Take the 19-byte payload; aim at `x/y/z`
    as an `odom` point, not a camera-frame one; fire on the `fire` bit after
    `delay_ms`, not on its 60 deg rule; don't lead when `FLAG_LEAD_APPLIED` is
    set. Which `odom` the MCB holds is open (`CV_SPLIT_PLAN.md` W.3 issue 1);
    for Sunday, aiming at the latest point every frame skips holding it.
  - Our side: port the change into `sim`'s MCB emulator, then
    `e2e.launch.py stage:=e2` and `test_e2.py` (xfail today) should score.
    That checks the firmware change before it reaches the robot.
  - YOLO runs at about 58 fps (the user, 2026-10-02).
  - Patrol: `point_to_cv_target` sweeps the gun with no target and faces
    hits off `ref_sys`, never firing (2026-10-02). Firmware that fires on
    every frame would fire all through it: run `patrol_enabled:=false`
    unless the firmware fires on the bit alone. On the robot, check the
    sweep direction and that a hit turns the gun toward it.
  - On the sentry, the rest of CV hasn't run on Jazzy yet: depth on
    a lit panel, bridge diagnostics `pose>0`, muzzle under 25 m/s. The
    `odom` point rides on our TF, so check `head_yaw`'s sign and
    `POSE`'s x/y axes (bridge README items 7-8): a panel straight
    ahead should land straight ahead of `root`.
    First shots on a stand, eye protection on, e-stop in reach.
  - The rebuilt image carries both halves: on the Mac,
    `isaac_ros_common/scripts/build_robot_image.sh ts-nano-sentry`, then
    restart the service. With no referee, the selector logs `Team colour
    unknown (robot_id 0)`; `Team colour set to RED` means old code.
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

## Tracks, in order of work

Finish the short todos first, then A-C in order, with I before A's E2,
then G. D runs alongside A, and E, F and H are unscheduled. Navigation comes after the Midwest competition;
until then the match test drives our robot from sim.

### A. The match test

[`E2E_PLAN.md`](E2E_PLAN.md), stages E1-E4. Sim plays only the MCB over a
pty, a detector stand-in for YOLO, lidar and depth. Our robot drives and
shoots against other `sentry_v2` copies with the real code in between.
Stages: the stand-in to the gimbal with our robot parked, then the serial
link against an MCB emulator, then driving while shooting, then opponents
that shoot back.

### I. MCB emulator

The MCB on the far end of track A's pty, copied from the real firmware,
`Thornbots/MCBV3` (`MCB-project/src/subsystems/jetson/`, `robots/sentry/`),
not from `UART_PROTOCOL.md` alone (the user, 2026-09-28). Built
(2026-10-01): `sim/mcb_emulator/` ports MCBV3 `708b8d6`, and
`e2e.launch.py stage:=e2` runs it on a pty against `dji_serial_bridge`
and `mcb_relay` (`sim/README.md` "MCB emulator"). E2 scores nothing yet:
the firmware refuses our 19-byte `CV_TARGET` (its `CVData` is 40 bytes),
so it only patrols, and `test_e2.py` is xfail. MCBV3#74 takes the frame
but doesn't aim yet. The thirteen gaps from
`UART_PROTOCOL.md` are in `ros2_dji_serial_bridge/README.md` "Where the
firmware stands"; each goes to the firmware side. Yaw holds within 2 deg
over a match (the user).

**Done when** the emulator runs the firmware's Jetson, aim-and-fire and
auto-drive logic against `dji_serial_bridge` on a pty, and E2 scores
through it.

### B. Hit while we move

[`CV_SPLIT_PLAN.md`](CV_SPLIT_PLAN.md) "Hitting while we move", steps
W.1-W.5, after track A's E3. Our side is done (2026-09-29): target, aim
solve and `CVTarget`'s aim point in `odom`, `RobotPose` with chassis yaw and
a send-start stamp, TF looked up at the state's stamp, and the estimation
bench spinning our chassis. Left: W.1's wire half and W.3, a world-frame aim
the MCB holds. Both change the wire protocol and firmware, so agree them
with the firmware side first.

### C. Jazzy on the robots

[`JAZZY_PLAN.md`](JAZZY_PLAN.md) steps 1, 5 and 6 (runbook
[`JAZZY_FLASH.md`](JAZZY_FLASH.md)). `ts-nano-dev` and `ts-nano-sentry`
are on JetPack 7.2.1; hero and standard still run frozen Humble. Done when
YOLO fps and detection latency on the Orin are no worse than on Humble.

Boot time: power-on to a running ROS stack under 1 min on each robot (the
user, 2026-09-30). The Jetsons used to run a minimized Ubuntu for this; the
7.2.1 installs are full `ubuntu-desktop` and boot to `graphical.target`
(sentry 15.0 s, dev 17.2 s, `systemd-analyze`).
`isaac_ros_common`'s `jetson_trim.sh` makes a robot headless. The sentry,
trimmed and running the Jazzy boot service, measured 2026-10-01: 13.6 s to
`multi-user.target`, both launches at 17.6 s, engine loaded about 21 s
(kernel start, not power-on; `isaac-ros-startup` `AGENTS.md`). `robot_setup.sh`,
the keyboard-free USB installer (`isaac_ros_common`) and the Jazzy boot
service (`isaac-ros-startup`) moved to `main` on 2026-10-01, untested,
because hero's stick (`make_installer_usb.sh --robot hero`) clones `main` on
first boot. Hero's stick bounced back to the boot menu; started from the
UEFI Shell instead, the install ran 2026-10-01 (`JAZZY_FLASH.md` step 3 has
the workaround for standard). Check `journalctl -u robot-firstboot` on
`ts-nano-hero`.

### G. Estimation accuracy

[`CV_SPLIT_PLAN.md`](CV_SPLIT_PLAN.md) "Estimation accuracy", steps
G.1-G.3. The tracker's radius drifts on some 4 m/s runs, radial motion and
detection blackouts cost 2-3x the usual error, and a fresh track is `valid`
(so it can fire) up to 3 s before its estimate settles. Tuning waits until
the stack works end to end (the user, 2026-09-29); the match test runs on
today's tracker. Also from `CV_SPLIT_PLAN.md` "Todos":

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

## Caveats

- Sim detection noise is 0.005 m against a D435's centimetres, and no sim
  test runs YOLO, so every CV rate here runs optimistic. The benches rank
  changes; they don't predict the field.
- `odom_stuck` loses the robot at 4 m/s with `/odom` frozen, accepted as a
  limit (2026-09-25).
- Neither CV bench runs gz; the drift suite does. SAPIEN is out for good.
- Nobody has checked what `sentry_v2` does when driven into a wall. That
  matters once obstacle avoidance has to be demonstrated.
