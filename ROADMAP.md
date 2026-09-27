# Where the project is going

A localization suite that can be believed, and CV cut in half at `TargetState`
with a bench for each half, then the CV stack from detections to gimbal
tested end to end in sim (`E2E_PLAN.md`). Updated 2026-09-26: Aiming is
finished, C2 runs on `bench_world` with limits on its ten cells, and `main`
is on Jazzy since 2026-09-27. Humble is frozen on the `humble` branches.

This file lists only work still to do. When an item is finished, delete it
outright rather than marking it done; git history and the package docs keep
the record.

## Where we actually are

| Thing | State |
|---|---|
| Test stack | **One gz session per run**, `sentry_v2` with collision and sprung wheels. Same verdicts shared, fresh per scenario, and alone |
| Localization drift suite (7 scenarios) | **7 pass** at `--backend amcl --use-ekf`, unthrottled, A2M8 lidar, per-scan rf2o (2026-09-24, 212 s with GUI): drift_correction 0.14 m, with obstacle 0.17 m, moving obstacles 0.18 m, against 0.40 m. `odom_stuck` passes its liveness check and loses the robot at 4 m/s, accepted as a limit (2026-09-25) |
| EKF fusion path | **95% better than raw `/odom`** (0.0075 m vs 0.1415 m mean, `suite:=ekf`, unthrottled, 2026-09-26), with rf2o's `fixed_heading` and `/odom` prior. Not yet re-run at real time (S4) |
| C2 estimation bench (60 cells, no gz) | **Runs on `bench_world`, with limits on every cell** (Jazzy, 2026-09-27): default, camera latency, moving shooter, radial, diagonal and blackout. Stationary under 2 cm facing-panel p95, moving 0.08-0.19 m; radial doubles along-ray error at 2-4 m/s, blackout is 2-3x worse. About a quarter of runs trip one limit on a spin-rate or radius outlier. See `CV_SPLIT_PLAN.md` "Where this stands" |
| CV stack end to end in sim | Nothing runs `roi_depth_node` or the serial link. `E2E_PLAN.md` plans the match test: sim plays only the MCB over a pty, a detector stand-in in place of YOLO, lidar and depth; our robot drives and shoots against other `sentry_v2` copies |
| Target in sim | Phantom: `target_driver` integrates a pose, no gz entity exists |
| CV seam | **Hard**: `point_to_cv_target` reads `TargetState` and `RobotPose` only. `TargetState` carries confidence, center, velocity, acceleration, yaw, yaw_rate, and per-pair `radius[2]`/`z_offset[2]` |
| Aiming (Part 1 on C1) | **Done.** 40 per-cell floors in `FLOORS`, chase mode the default |
| ROS 2 Jazzy | **`main` is Jazzy** (2026-09-27); Humble is frozen on `humble`. On the laptop builds, unit tests, drift suite, `suite:=ekf`, C1 and C2 match Humble. The Orin reflashes and hardware checks are left (Track D) |

## The sim

### S3: A localization scenario with finite acceleration

`drive()` steps `/cmd_vel` to 4 m/s at the start of each leg and stops within
about one 0.1 s tick, so every scenario corners with effectively infinite
acceleration. Add a scenario, or a `drive()` option, that ramps velocity under
an acceleration limit, so localization is scored on motion the chassis can
actually make.

### S4: Unthrottled has to score the same as real time

The suites time themselves in sim seconds, so `real_time_factor:=0` should only
save wall clock. It didn't: `drift_correction` read 4.02 m unthrottled and
0.42 m at 1×. rf2o's wall-clock loop was one known cause, and it now matches
every scan in its callback (`thornbots_workspace#11`). **Done when:** the drift
suite and `suite:=ekf` give the same verdicts at `real_time_factor:=0` and
`:=1`. The drift suite meets it. `suite:=ekf` passes unthrottled (0.0075 m
fused mean, 2026-09-26). **Left:** `suite:=ekf` at `real_time_factor:=1`. If
it differs, audit every node for wall-clock timers, rates and timeouts.

### S5: Benches that start and stop cleanly

Added 2026-09-25. Bringing a bench up or down takes hand-holding today:

- A fresh container has no gz until `install-sim.sh` runs, and nothing says
  so until a launch fails.
- Nodes cold-start into a live topic stream. TF has run 0.6 s behind at
  bring-up. A lifecycle reply lost in DDS can leave `amcl` or `map_server`
  unconfigured for good. The drift harness now restarts such a stack once;
  the robot's own boot has no such guard.
- Ctrl-C prints a traceback from every Python node: each `main()` is a bare
  `rclpy.spin` with no shutdown handling.
- A launch whose host shell dies leaves its nodes orphaned (parent 1,
  invisible to `kill_launch.sh -l`). Once, nine stacks were all publishing
  `/clock`.

**Done when:** each bench (drift suite, C1, C2) starts with one command,
says what's missing if gz isn't installed, and waits until the stack is
ready before it scores anything. Ctrl-C or the end of the tests stops every
node it started, with no tracebacks, and a check afterwards finds no
orphans.

## Track A: Localization

### A3: One metric per backend

`MAX_DELTA_THRESHOLD` stays the assertion where a backend owns `map->odom`.
Under `--backend none` the watched edge is `odom->root`, the robot's own
position, so the scenarios there score ground-truth error against
`/sim/raw_odom`.

**Done when:** six scenarios green at the target config, and every failure
elsewhere points at a real defect.

**Built (sim `main`, 2026-09-25), not yet run:** under `none`,
`noise_correction` and the three cornering-loop scenarios score `odom->root`
against `/sim/raw_odom` (`_truth_error`). `test_ekf_ground_truth.py` stays as
it is: it asks a different question, whether the EKF beats raw `/odom`.
`odom_stuck` stays a liveness check (the user's call): with `/odom` frozen,
rf2o's seed freezes too, and 0.4 m between 10 Hz scans at 4 m/s is too far to
match unseeded, so the robot is lost. Matching from rf2o's own last motion as
well was tried and didn't help. `sim/README.md` has the details.

### A4: Moving obstacles

Other robots driving around while we drive the cornering loop, with two pass
conditions:

- AMCL pose error against truth stays under threshold while transient returns
  come and go.
- Under `slam`, the occupancy grid does not keep the actors' paths as walls.
  Sample the cells they crossed at the end of the run.

**The first passes (sim `main`, 2026-09-24):** `actor_driver` walks three
boxes across the loop's south, west and north edges at 0.5–2 m/s by
`set_pose`, keeping them clear of the robot's next second of route. They have
no collision, since `gpu_lidar` renders visuals and contact with the field
mesh cost ~3× sim speed. `moving_obstacles` reads 0.18 m against 0.40 m.
**Left:** the `slam` occupancy-grid check (a `TODO(A4)` in
`_run_cornering_loop_scenario`).

## Track B: Split CV at `TargetState`

> **Part 1: hit it.** `point_to_cv_target`. `TargetState` plus our own pose in,
> aim point and fire timing out. Extends the given motion into the future; owns
> no perception.
>
> **Part 2: build the model.** `target_selector` + `target_tracker`. Detections
> in, one `TargetState` out: where the robot is, how fast it moves, how fast it
> spins, where its four panels sit.

Both stay nodes in `thornbots_pkg`. The work is making the seam *hard*. The
step-by-step plan is [`CV_SPLIT_PLAN.md`](CV_SPLIT_PLAN.md).

Aiming (Part 1 on C1) is done. What's left is Estimation (Part 2 on C2):
per-pair z and the camera-latency model are built and unit-tested, and C2
hasn't scored either yet.

- **Wanted: the CV nodes move out of `thornbots_pkg` into their own
  package** (added 2026-09-25), say `thornbots_cv`. `thornbots_pkg` keeps
  the hardware interface, URDF, TF and `mcb_relay`; the new package takes
  `target_selector`, `target_tracker` and `point_to_cv_target`, their
  `*_core.py` and their three tests. It is a new submodule, so a new
  `Thornbots/` repo, a `.gitmodules` entry and a `Dockerfile.thornbots`
  COPY and build line beside `thornbots_pkg`'s. Everything that names
  `package='thornbots_pkg'` for those nodes follows: `auto.launch.py` (and
  its UDP-only DDS pinning for `target_tracker` and `point_to_cv_target`),
  and `sim`'s `sim.launch.py`, `shot_hit.launch.py` and `estimation.launch.py`. README.md and
  AGENTS.md split the same way. Do it between bench runs, not during one,
  and re-run both benches after to show nothing moved.
- **Next: hit while we move** (added 2026-09-25). The target and the aim
  solve are already in `odom`; the aim still leaves as a `root`-frame point
  the MCB holds while the chassis moves, and `RobotPose` has no chassis yaw.
  The fix puts our pose (with yaw, stamped at capture) and the aim command
  in the world frame, and lets the MCB hold it; `CV_SPLIT_PLAN.md`
  "Hitting while we move" has the steps. Wire and firmware changes, so
  agree them with the firmware side.

## Track C: Two benches, one per half

The match test that follows them, with sim playing only the MCB, YOLO and
the sensors while our robot drives and shoots, is planned in
[`E2E_PLAN.md`](E2E_PLAN.md) with the speed work for every suite. It
doesn't run YOLO.

### C2: Estimation bench, fake detections

Detections are synthesized from the target's true pose (no YOLO in the loop),
with D435-like ray noise, and nothing fires. Part 2 is benchmarked only on how close its
`TargetState` gets to truth, compared at its own stamp (`CV_SPLIT_PLAN.md` 2.0):

- panel error, the four implied panel positions against the true four
- center, velocity, yaw, yaw_rate, radius and z_offset error
- time from first detection until panel error settles

**Built:** `estimation.launch.py` on `bench_world`, one C++ lockstep loop
that stands in for gz: clock, phantom target, our chassis and head, `/pose`,
head controller and detections. It holds sim time only for the nodes under
test, the tracker's input among them, and runs the ten cells in ~75 s.
Metrics as above, plus the facing panel's error, which is what Part 1 aims
at. `target_tracker` is the slowest node under test; a C++ core for it is
the user's call (`CV_SPLIT_PLAN.md`). `LIMITS` covers all 60 cells, the
C3 cases (moving shooter, radial, diagonal), latency and blackout included,
at 2x the worst of three to six runs.

## Track D: ROS 2 Jazzy (last)

Isaac ROS 4.6 on Jazzy, Ubuntu 24.04 in the image, `isaac-ros-cli` in place
of our `run_dev.sh` fork, gz Harmonic for `sim`, and a JetPack 7.2.1 reflash
on every Jetson. `main` is Jazzy since 2026-09-27, and `JAZZY_PLAN.md` is
the plan for the hardware. **Humble is frozen:** the `humble` branches take
no more work, and a robot on Humble runs that frozen tree until it is
reflashed.

**Where it stands (2026-09-27):** the port builds clean and passes every
unit test. On the laptop the drift suite, `suite:=ekf`, C1 and C2 give
Humble's verdicts. Left: reflash `ts-nano-dev` (step 1), the hardware checks
on it (step 5: RealSense, YOLO fps, serial, DDS), then the robots (step 6). **Done when:** the drift suite,
`suite:=ekf` and both benches give the same verdicts on Jazzy as on Humble,
`thornbots_pkg`'s CV tests pass, and YOLO fps and detection latency on the
Orin are no worse.

## Order of work

Finished items come off this list, and off the file; the next one is always 1.

1. **The rest of Track A:** run A3's metric under `--backend none`, run
   `suite:=ekf` at real time for S4, then A4's `slam` occupancy-grid check
   and S3's finite-acceleration scenario.
2. **The match test, E1 to E4** (`E2E_PLAN.md`): armor panels on the URDF
   and the detector stand-in, then the serial link against an MCB
   emulator, then driving while shooting, then opponents that shoot back.
   The speed work in the same file runs alongside.
3. **Hit while we move, E5:** our pose and the aim command in the world
   frame (`CV_SPLIT_PLAN.md` W.1-W.5), after both benches have limits.
4. **Move the robots to Jazzy** (Track D): `ts-nano-dev` first (steps 1
   and 5), then each robot. Until then the robots run frozen Humble code.

Unscheduled: the CV nodes' move to their own package (Track B), between
bench runs, and S5, clean bench start and stop. Navigation comes after the
Midwest competition; until then the match test drives our robot from sim.

## Caveats

- **Armor panels are canted 15 degrees in the game (S122: normal 75 degrees
  from up), and the hit scoring has lost that.** The emulator, the aim
  bench's facing test and both rviz views keep it (rviz
  since 2026-09-25). A hit is scored as the ray passing within 0.05 m of
  the panel centre, not as crossing the canted 0.1 m square. Not fixed.

- Detection noise in sim is 0.005 m against a D435's centimetres, so every CV
  rate here runs optimistic. The benches rank changes; they don't predict the
  field.
- No sim test runs YOLO; its detections come from truth. YOLO is checked on
  hardware only.
- Neither CV bench runs gz; the drift suite does. SAPIEN was tested against
  gz, came out worse, and is out for good (removed 2026-09-24).
- `sentry_v2` collides, but what it does when driven into a wall hasn't been
  checked. That matters the day obstacle *avoidance* becomes something to
  demonstrate.
- C2 runs stray up to 2x from each other (radius and spin-rate outliers),
  so compare C2 changes over three runs, not one.
