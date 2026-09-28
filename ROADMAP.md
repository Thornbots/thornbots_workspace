# Where the project is going

A localization suite we can believe, CV split at `TargetState` with a bench
for each half, then the CV stack from detections to gimbal tested end to
end in sim. Updated 2026-09-28. Aiming is done, the estimation bench has
limits on all 60 cells, and `main` has been Jazzy since 2026-09-27. Humble
is frozen on the `humble` branches.

This file lists only work still to do. Delete an item when it's finished;
don't mark it done. Git history and the package docs keep the record.

## Where we actually are

| Thing | State |
|---|---|
| Localization drift suite (7 scenarios) | **7 pass** at `--backend amcl --use-ekf`, unthrottled, A2M8, per-scan rf2o (2026-09-24): drift_correction 0.14 m, with obstacle 0.17 m, moving obstacles 0.18 m, against 0.40 m. One gz session per run, `sentry_v2` with collision and sprung wheels |
| EKF fusion | **95% better than raw `/odom`** (0.0075 m vs 0.1415 m mean, `suite:=ekf`, unthrottled, 2026-09-26) |
| Estimation bench (60 cells, no gz) | **Limits on every cell** (2026-09-27). Stationary under 2 cm facing-panel p95, moving 0.08-0.19 m. About a quarter of runs trip one limit on a spin-rate or radius outlier. `CV_SPLIT_PLAN.md` has the detail |
| CV end to end in sim | Nothing runs `roi_depth_node` or the serial link yet (track 1) |
| Jazzy | Laptop matches Humble on every suite and bench. Orin reflash and robots left (track 3) |

## Short todos

Nearly finished work, numbered T1-T9 so they aren't confused with tracks.
Pointers lead to the detail. Numbers stay put when items are deleted.

Localization (`sim/README.md` has the scenarios):

- T1: Run the ground-truth metric under `--backend none`. Built 2026-09-25:
  `noise_correction` and the three cornering-loop scenarios score
  `odom->root` against `/sim/raw_odom`. Done when six scenarios pass there.
  `odom_stuck` stays a liveness check (the user's call).
- T2: Run `suite:=ekf` at `real_time_factor:=1`. Done when it gives the same
  verdict as unthrottled; if it doesn't, audit every node for wall-clock
  timers, rates and timeouts.
- T3: Moving obstacles under `slam`: sample the grid cells the actors
  crossed and check none stayed walls (the `TODO` in `_run_cornering_loop_scenario`).
- T4: rf2o match grading (built 2026-09-27): run `scan_degraded` at
  `--backend amcl --use-ekf` and set the thresholds from the
  `/scan_odom/quality` distributions. Done when it passes, the other seven
  and `suite:=ekf` are no worse, and over 99% of clean matches grade good.
- T5: A scenario, or a `drive()` option, that ramps `/cmd_vel` under an
  acceleration limit. Today every leg steps to 4 m/s within one 0.1 s tick.
  The match test's driving (track 1, E3) wants the same ramp.

Estimation (`CV_SPLIT_PLAN.md` "Todos"):

- T6: Score per-pair z: staggered cells' `z_offset` and panel error against
  flat cells'.
- T7: Sweep `process_noise_accel` against the velocity-error trace, path ends
  included.
- T8: Check the bench scores the same with a cell run alone as in sequence.

Stamps (`CV_SPLIT_PLAN.md` "Stamps"):

- T9: `mcb_relay`'s relocalize and the bridge's `~/nav_goal` become
  `PointStamped`.

## Open for the user

- The estimation bench's three open questions: the radius wandering at
  4 m/s, radial and blackout error, and a fresh track's slow lock on a
  spinner (`CV_SPLIT_PLAN.md` "Open for the user").
- A C++ core for `target_tracker`, the slowest node on the estimation bench.
- Moving both benches' target onto the URDF's armor panels, with fresh
  `FLOORS` and `LIMITS` runs (`E2E_PLAN.md` "Panels on the URDF").
- The match test's open questions (`E2E_PLAN.md`).

## Tracks, in order of work

Finish the short todos first. Tracks 1-3 run in order; 4 runs alongside 1,
and 5-6 are unscheduled. Navigation comes after the Midwest competition;
until then the match test drives our robot from sim.

### 1. The match test

[`E2E_PLAN.md`](E2E_PLAN.md), stages E1-E4. Sim plays only the MCB over a
pty, a detector stand-in for YOLO, lidar and depth. Our robot drives and
shoots against other `sentry_v2` copies with the real code in between.
Stages: the stand-in to the gimbal with our robot parked, then the serial
link against an MCB emulator, then driving while shooting, then opponents
that shoot back.

### 2. Hit while we move

[`CV_SPLIT_PLAN.md`](CV_SPLIT_PLAN.md) "Hitting while we move", steps
W.1-W.5, after track 1's E3. The target, the aim solve and `CVTarget`'s aim
point are already in `odom`. `RobotPose` still lacks chassis yaw and a
capture stamp, and the MCB has to hold a world-frame aim. W.1 and W.3 change
the wire protocol and firmware, so agree them with the firmware side first.

### 3. Jazzy on the robots

[`JAZZY_PLAN.md`](JAZZY_PLAN.md) steps 1, 5 and 6: reflash `ts-nano-dev`
(runbook [`JAZZY_FLASH.md`](JAZZY_FLASH.md)), run the hardware checks on it,
then each robot. Until then the robots run frozen Humble. Done when YOLO fps
and detection latency on the Orin are no worse than on Humble.

### 4. Faster suites

[`E2E_PLAN.md`](E2E_PLAN.md) "Speed". Log each suite's wall-time split,
find why the full gz stack caps at RTF ~1.55, render only what gets scored.
Suites run one at a time; we are compute-limited.

### 5. Benches that start and stop cleanly

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

### 6. CV nodes into their own package

Move `target_selector`, `target_tracker` and `point_to_cv_target`, their
`*_core.py` and tests from `thornbots_pkg` to a new `thornbots_cv`.
`thornbots_pkg` keeps the hardware interface, URDF, TF and `mcb_relay`. A
new submodule means a new `Thornbots/` repo, a `.gitmodules` entry and a
`Dockerfile.thornbots` build line. Everything naming
`package='thornbots_pkg'` for those nodes follows: `auto.launch.py` (with
its UDP-only DDS pinning) and `sim`'s `sim.launch.py`, `shot_hit.launch.py`
and `estimation.launch.py`. Do it between bench runs, and re-run both
benches after to show nothing moved.

## Caveats

- Armor panels are canted 15 degrees (S122), and hit scoring ignores that:
  a hit is the ray passing within 0.05 m of the panel centre, not crossing
  the canted square. Track 1's shot model fixes it.
- Sim detection noise is 0.005 m against a D435's centimetres, and no sim
  test runs YOLO, so every CV rate here runs optimistic. The benches rank
  changes; they don't predict the field.
- Estimation bench runs stray up to 2x from each other, so compare changes
  over three runs, not one.
- `odom_stuck` loses the robot at 4 m/s with `/odom` frozen, accepted as a
  limit (2026-09-25).
- Neither CV bench runs gz; the drift suite does. SAPIEN is out for good.
- Nobody has checked what `sentry_v2` does when driven into a wall. That
  matters once obstacle avoidance has to be demonstrated.
