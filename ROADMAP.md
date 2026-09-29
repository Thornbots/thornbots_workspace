# Where the project is going

A localization suite we can believe, CV split at `TargetState` with a bench
for each half, then the CV stack from detections to gimbal tested end to
end in sim. Updated 2026-09-28. Aiming is done, the estimation bench has
limits on all 60 cells, and `main` has been Jazzy since 2026-09-27. Humble
is frozen on the `humble` branches.

This file lists only work still to do. Delete an item when it's finished,
then commit and push; don't mark it done. Git history and the package docs
keep the record.

## Where we actually are

| Thing | State |
|---|---|
| Localization drift suite (9 scenarios) | **9 of 9 pass** at `--backend amcl --use-rf2o`, unthrottled, legs ramped at 20 m/s^2, ~285 s (2026-09-28, three runs): drift_correction 0.16-0.18 m, with obstacle 0.15-0.18 m, moving obstacles 0.17-0.19 m, real_accel (1.2 m/s^2) 0.09-0.11 m, against 0.40 m. One gz session per run, `sentry_v2` with collision and sprung wheels |
| EKF fusion | **90-95% better than raw `/odom`** (0.007-0.020 m vs 0.15-0.25 m mean, `suite:=ekf`, five runs 2026-09-28) |
| Estimation bench (60 cells, no gz) | **Limits on every cell** (2026-09-27). Stationary under 2 cm facing-panel p95, moving 0.08-0.19 m. About a quarter of runs trip one limit on a spin-rate or radius outlier. `CV_SPLIT_PLAN.md` has the detail |
| CV end to end in sim | Nothing runs `roi_depth_node` or the serial link yet (track A) |
| Jazzy | Laptop matches Humble on every suite and bench. Orin reflash and robots left (track C) |

## Short todos

Nearly finished work, plus a few later items at the end. Pointers lead to
the detail, and numbers stay put when items are deleted.

Localization (`sim/README.md` has the scenarios):

- T3: Moving obstacles under `slam`: sample the grid cells the actors
  crossed and check none stayed walls (the `TODO` in `_run_cornering_loop_scenario`).
  The check is on `sim` branch `t3-actor-map-check`. Blocked: with the
  ARCC26 pose graph loaded, slam_toolbox never publishes `/map`; its
  `getOccupancyGrid` ran 600 s at 100% of a core (2026-09-28). Needs a
  map that rasterises in seconds (track H rebuilds it).

Estimation (`CV_SPLIT_PLAN.md` "Todos"):

- T15: A still target seen at an angle loses yaw and radius (0.35 rad,
  0.07 m), and the bench only tests one at an angle by accident
  (`CV_SPLIT_PLAN.md` "Todos"). Reset the target's yaw per case, add a
  still cell with two panels in view, then fix the tracker.
- T7: Sweep `process_noise_accel` against the velocity-error trace, path ends
  included.
- T8: Check the bench scores the same with a cell run alone as in sequence.

Repeatability:

- T17: Runs with the same inputs should score nearly the same, and today
  they don't (the user, 2026-09-28). Estimation bench runs stray up to 2x
  from each other, and about a quarter trip one limit on an outlier.
  Drift runs spread less (0.16-0.18 m). Find where the spread comes from
  (`bench_world`'s `seed` defaults to random, and pacing and DDS timing
  vary) and cut it, so one run is enough to judge a change.

Aiming:

- T18: Score hits on the canted panel, not a circle. Armor panels are
  canted 15 degrees (S122), but a hit is the ray passing within 0.0625 m
  (half the panel's 0.125 m height) of the panel centre, inside a 145-degree
  cone, not the ray crossing the canted 0.135 x 0.125 m face
  (`shot_hit_harness.py`). Intersect the ray with that face, then regenerate
  `FLOORS` over three runs. Track A's shot model can reuse it.

Tracker cost:

- T10: Measure what `target_tracker` costs before deciding on a C++ core:
  time per update and CPU on the Orin and the laptop, its share of
  detection-to-`TargetState` latency, and how much it caps the estimation
  bench's speed. On the laptop at ~8x, `ArmorTracker.step`'s numpy is 46% of
  its main thread and its TF listener 27%, so check how much of that the TF
  listener alone accounts for. Then the user decides.

Later:

- T11: Sim on a Mac. The Mac mini (M6, 12 cores, 32 GB) beats the laptop
  on every suite, inside `Dockerfile.mac` under Colima with gz and rviz on
  llvmpipe and the GUI on: drift 179 s at RTF 1.69 against 242 s at 1.29
  (laptop headless on its GPU), estimation 30 s against 54 s, aiming 31 s
  against 42 s (2026-09-28). Only YOLO and Isaac ROS need NVIDIA.
  Open: the GUI shows over VNC, not on the Mac's screen. Native macOS
  through RoboStack would put windows on the screen and gz on Metal. The
  stack builds there (2026-09-28): `~/robostack_ws/pixi.toml` on the Mac
  has every dep from `robostack-jazzy` (setuptools < 80, pytest < 8),
  `colcon build --base-paths ~/ros2_ws/src` into its own build and install
  dirs (the container shares `ros2_ws/build`), `sllidar_ros2` ignored
  (Linux-only, and sim never starts it). Next: the harnesses and
  `head_slider_relay.py` call Linux's `prctl(PR_SET_PDEATHSIG)`, so no sim
  test even collects; port that, then run each suite natively. `sim.launch.py`
  already runs gz's server and GUI as two processes, as macOS needs.

## Open for the user

- A C++ core for `target_tracker`, once T10 has measured its cost.
- The match test's open questions (`E2E_PLAN.md`).

## Tracks, in order of work

Finish the short todos first, then G, then A-C in order. D runs alongside
A, and E, F and H are unscheduled. Navigation comes after the Midwest competition;
until then the match test drives our robot from sim.

### G. Estimation accuracy

[`CV_SPLIT_PLAN.md`](CV_SPLIT_PLAN.md) "Estimation accuracy", steps
G.1-G.3. The tracker's radius drifts on some 4 m/s runs, radial motion and
detection blackouts cost 2-3x the usual error, and a fresh track is `valid`
(so it can fire) up to 3 s before its estimate settles. It runs first
because the match test would inherit all three.

### A. The match test

[`E2E_PLAN.md`](E2E_PLAN.md), stages E1-E4. Sim plays only the MCB over a
pty, a detector stand-in for YOLO, lidar and depth. Our robot drives and
shoots against other `sentry_v2` copies with the real code in between.
Stages: the stand-in to the gimbal with our robot parked, then the serial
link against an MCB emulator, then driving while shooting, then opponents
that shoot back.

### B. Hit while we move

[`CV_SPLIT_PLAN.md`](CV_SPLIT_PLAN.md) "Hitting while we move", steps
W.1-W.5, after track A's E3. The target, the aim solve and `CVTarget`'s aim
point are already in `odom`. `RobotPose` still lacks chassis yaw and a
capture stamp, and the MCB has to hold a world-frame aim. W.1 and W.3 change
the wire protocol and firmware, so agree them with the firmware side first.

### C. Jazzy on the robots

[`JAZZY_PLAN.md`](JAZZY_PLAN.md) steps 1, 5 and 6: reflash `ts-nano-dev`
(runbook [`JAZZY_FLASH.md`](JAZZY_FLASH.md)), run the hardware checks on it,
then each robot. Until then the robots run frozen Humble. Done when YOLO fps
and detection latency on the Orin are no worse than on Humble.

### D. Faster suites

[`E2E_PLAN.md`](E2E_PLAN.md) "Speed". Log each suite's wall-time split,
find why the full gz stack caps at RTF ~1.55, render only what gets scored.
Suites run one at a time; we are compute-limited.

Keep the gz camera off (`camera:=false`, the default) in every suite.
Nothing consumes its images yet, and a subscribed RGB-D camera alone caps a
bare server near RTF 2.2. Turn it on only when a suite scores it: track A
needs depth alone.

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

### F. CV nodes into their own package

Move `target_selector`, `target_tracker` and `point_to_cv_target`, their
`*_core.py` and tests from `thornbots_pkg` to a new `thornbots_cv`.
`thornbots_pkg` keeps the hardware interface, URDF, TF and `mcb_relay`. A
new submodule means a new `Thornbots/` repo, a `.gitmodules` entry and a
`Dockerfile.thornbots` build line. Everything naming
`package='thornbots_pkg'` for those nodes follows: `auto.launch.py` (with
its UDP-only DDS pinning) and `sim`'s `sim.launch.py`, `shot_hit.launch.py`
and `estimation.launch.py`. Do it between bench runs, and re-run both
benches after to show nothing moved.

### H. SLAM at amcl's level

Keep SLAM a real fallback to amcl. amcl with the EKF passes all nine drift
scenarios, the map-based ones at 0.15-0.19 m (2026-09-28). `slam` was last tuned 2026-07
on the old stack, at 0.31-0.33 m, localizing against the saved field map.

SLAM here means `mapping` mode: slam_toolbox builds the map and localizes on
it, with the EKF allowed. It gets a mapping window before each game, and
carries one map from game to game: load it at boot, extend it during the
game, save it after. Earlier `slam --use-rf2o` read worse than plain `slam`,
likely because slam_toolbox's correction stacked on the EKF's rf2o
correction (`sentry_localization/README.md`); fix that, don't drop the EKF.

1. Add `mapping` to the drift harness's backends (it isn't offered today,
   since nothing scored a map-building run) and score it against truth with
   the map frame aligned at spawn: the built map's origin is wherever the
   run starts. Then run it with and without `--use-rf2o` on today's stack
   (`sentry_v2`, A2M8, per-scan rf2o).
2. Fix the EKF stacking, for example by pointing slam_toolbox's
   `odom_frame` at raw odometry, then retune `slam.yaml`.
3. Carry the map across games. After each game, serialize the pose graph
   (slam_toolbox's `serialize_map`) and load it at the next boot with
   `load_map:=true` in `mapping` mode, starting from our known spawn pose
   (`map_start_pose`). Before the Battle, give it a mapping window: a short
   scripted lap, if the rules allow moving then (check the Setup Period
   rules). Moving robots from past games must not pile up in the map.
4. A game-like scenario: a full 5-minute Battle on the field with other
   `sentry_v2` copies driving, spinning and blocking the lidar (track A's
   opponents), our robot driving a match-like route with finite
   acceleration (`real_accel`'s 1.2 m/s^2), including the high ground. Score pose error against
   truth throughout, and check the built map doesn't keep robots as walls
   (T3).

**Done when:** SLAM with the EKF passes the drift scenarios amcl passes,
each within 0.05 m of amcl's error, and stays within 0.05 m of amcl on the
game-like scenario too (run both there). Run that scenario as three games
in a row on one carried-over map: the error must not grow from game to
game, and the map must not collect robots or duplicate walls.

## Caveats

- Sim detection noise is 0.005 m against a D435's centimetres, and no sim
  test runs YOLO, so every CV rate here runs optimistic. The benches rank
  changes; they don't predict the field.
- Estimation bench runs stray up to 2x from each other, so compare changes
  over three runs, not one, until T17 cuts the spread.
- `odom_stuck` loses the robot at 4 m/s with `/odom` frozen, accepted as a
  limit (2026-09-25).
- Neither CV bench runs gz; the drift suite does. SAPIEN is out for good.
- Nobody has checked what `sentry_v2` does when driven into a wall. That
  matters once obstacle avoidance has to be demonstrated.
