# Where the project is going

A localization suite that can be believed, and CV cut in half at `TargetState`
with a bench for each half, then the whole CV stack tested end to end in sim
(`E2E_PLAN.md`). Updated 2026-09-25: C2 has had its first runs, and Track A
has two runs, a map check and S3 left.

This file lists only work still to do. When an item is finished, delete it
outright rather than marking it done; git history and the package docs keep
the record.

## Where we actually are

| Thing | State |
|---|---|
| Test stack | **One gz session per run**, `sentry_v2` with collision and sprung wheels. Same verdicts shared, fresh per scenario, and alone |
| Localization drift suite (7 scenarios) | **7 pass** at `--backend amcl --use-ekf`, unthrottled, A2M8 lidar, per-scan rf2o (2026-09-24, 212 s with GUI): drift_correction 0.14 m, with obstacle 0.17 m, moving obstacles 0.18 m, against 0.40 m. `odom_stuck` passes its liveness check and loses the robot at 4 m/s, accepted as a limit (2026-09-25) |
| EKF fusion path | **63% better than raw `/odom`** at 4 m/s, real time (0.050 m vs 0.134 m mean), with rf2o's `fixed_heading` and `/odom` prior. Measured before the A2M8 lidar and per-scan rf2o; `suite:=ekf` needs a re-run (S4) |
| C2 estimation bench (10 cells, no gz) | **Three gz runs (2026-09-25), no limits yet.** Stationary cells 1.3 cm facing-panel p95; moving cells 0.12-0.51 m and 2x apart between runs, not yet traced. Now on `bench_world` (C++): all ten cells in 54 s with rviz, 10/10, stationary 0.9 cm, moving cells in gz's spread and still swinging, so the swing is the tracker's. The tracker gained acceleration, a single-panel yaw measurement and a still-target hypothesis; see `CV_SPLIT_PLAN.md` "Where this stopped" |
| Whole CV stack in sim | Nothing runs the camera, YOLO, `roi_depth_node` or the serial link; planned in `E2E_PLAN.md` |
| Target in sim | Phantom: `target_driver` integrates a pose, no gz entity exists |
| CV seam | **Hard**: `point_to_cv_target` reads `TargetState` and `RobotPose` only. `TargetState` carries confidence, center, velocity, yaw, yaw_rate, and per-pair `radius[2]`/`z_offset[2]` |

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
`:=1`. **Drift suite met 2026-09-24:** 6/6 unthrottled, drift_correction
0.17 m against 0.23–0.26 m at real time before the lidar change. **Left:**
`suite:=ekf` hasn't been re-run. If it differs, audit every node for
wall-clock timers, rates and timeouts.

### S5: Benches that start and stop cleanly

Added 2026-09-25. Bringing a bench up or down takes hand-holding today:

- A fresh container has no gz until `install-sim.sh` runs, and nothing says
  so until a launch fails.
- Nodes cold-start into a live topic stream. TF has run 0.6 s behind at
  bring-up, and one bring-up in six left `amcl` unconfigured.
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

What's left is Part 2, on C2.

- Part 2: `ArmorEKF` estimates a per-pair z. It put all four panels at
  one height, which is why staggering them 9 cm dropped the stationary case
  from 98% to 30%. `TargetState.z_offset[2]` is the field. **Built
  2026-09-25**, unit-tested; C2 scores it.
- Part 2 owns all hardware latency. `TargetState` describes the target now:
  the tracker works out capture time, predicts forward to its publish time and
  stamps that. Part 1 only extrapolates into the future, over fire-to-impact
  time. **Built 2026-09-25** (`camera_latency_s` in tracker and emulator), not
  run.

`CV_SPLIT_PLAN.md` names the two phases: **Aiming** (Part 1 on C1) and
**Estimation** (Part 2 on C2).

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

The end-to-end tests that follow them, the whole CV stack from rendered
pixels (E) and then moving while shooting (M), are planned in
[`E2E_PLAN.md`](E2E_PLAN.md).

### C2: Estimation bench, fake detections

Detections are synthesized from the target's true pose (no YOLO in the loop),
with D435-like ray noise, and nothing fires. Part 2 is benchmarked only on how close its
`TargetState` gets to truth, compared at its own stamp (`CV_SPLIT_PLAN.md` 2.0):

- panel error, the four implied panel positions against the true four
- center, velocity, yaw, yaw_rate, radius and z_offset error
- time from first detection until panel error settles

**Built (sim `main`, 2026-09-25):** `estimation.launch.py`, three runs on
gz, then moved off it. C2 only fakes detections, so `bench_world`, one C++
lockstep loop, now stands in for gz: clock, phantom target, our chassis and
head, `/pose`, head controller and detections. It holds sim time only for
the nodes under test and runs the ten cells in 54 s with rviz (~6x; gz took
~6 min). Metrics as above, plus the facing panel's error, which is what
Part 1 aims at. On gz, stationary cells read 1.3 cm facing p95 and moving
cells 0.12-0.51 m, 2x apart between runs. On `bench_world` stationary reads
0.9 cm and moving cells land in gz's spread, still 2x apart
(`flat-speed1` 0.19 m alone, 0.31 m in the suite). `target_tracker` is the
speed ceiling (a saturated core at ~8x); a C++ core for it is the user's
call (`CV_SPLIT_PLAN.md`). `LIMITS` is empty until the error is traced and
three runs fill it.

### C3: The two cases neither bench had, on C2

- **We are moving** (`shooter_speed:=1.0`): odom-frame filtering while
  `root` moves.
- **Depth changes** (`target_path:=radial`/`diagonal`): depth error grows
  with range squared while bearing error stays near a pixel, which is why
  `ray_covariance` is anisotropic. Center error along the ray should grow
  and error across it should not.

## Track D: ROS 2 Jazzy (last)

The image is built on Humble: `nvcr.io/nvidia/isaac/ros:humble-3.2`,
`Dockerfile.ros2_humble`, `CONFIG_IMAGE_KEY=ros2_humble.realsense.thornbots`,
and `--rosdistro humble` in rosdep. The target is Isaac ROS 4.6, the only
Jazzy release that runs on Orin: Ubuntu 24.04 in the image, a JetPack 7.2.1
reflash on every Jetson, the `isaac-ros-cli` tooling in place of our
`run_dev.sh` fork, and gz Harmonic for `sim`. The step-by-step plan, with
every file that changes, is [`JAZZY_PLAN.md`](JAZZY_PLAN.md).

The cutover waits until every other track is done, so no suite result gets
mixed up with a distro change. Steps 0 to 5 of the plan run on `jazzy`
branches and on `ts-nano-dev` and can start earlier. **Done when:** the drift
suite, `suite:=ekf` and both benches give the same verdicts on Jazzy as on
Humble, and `thornbots_pkg`'s CV tests (`point_to_cv_target`,
`target_selector`, `target_tracker`) pass.

## Order of work

Finished items come off this list, and off the file; the next one is always 1.

1. **C2:** trace the moving-cell error and its run-to-run swing. The camera
   TF at capture is ruled out (the tracker never waited for it on gz); next
   are the 4-7 m/s velocity-error bursts on a 1 m/s target, against the
   path ends and the tracker's re-seeds. Then three runs fill `LIMITS`, and
   camera latency, C3's cases and blackout each run three times
   (`CV_SPLIT_PLAN.md` Next).
2. **The rest of Track A:** run A3's metric under `--backend none`, re-run
   `suite:=ekf` for S4, then A4's `slam` occupancy-grid check and S3's
   finite-acceleration scenario.
3. **E, the whole CV stack with our robot parked** (`E2E_PLAN.md`): E1 with a
   detector stand-in, E2 with real YOLO, E3 over the serial link. E1 can
   start without the YOLO ONNX.
4. **Hit while we move:** our pose and the aim command in the world frame
   (`CV_SPLIT_PLAN.md` W.1-W.5), after both benches have limits, then M,
   moving and shooting at once, on E's stack.
5. **Move from ROS 2 Humble to Jazzy,** once everything above is done. See
   Track D and `JAZZY_PLAN.md`; its steps 0 to 5 don't touch the robots and
   can run earlier.

Unscheduled: the CV nodes' move to their own package (Track B), between
bench runs, and S5, clean bench start and stop.

## Caveats

- **Armor panels are canted 15 degrees in the game (S122: normal 75 degrees
  from up), and the hit scoring has lost that.** The emulator, the aim
  bench's facing test and both rviz views keep it (rviz
  since 2026-09-25). A hit is scored as the ray passing within 0.05 m of
  the panel centre, not as crossing the canted 0.1 m square. Not fixed.

- Detection noise in sim is 0.005 m against a D435's centimetres, so every CV
  rate here runs optimistic. The benches rank changes; they don't predict the
  field.
- Rendered detections stay out of both benches. E2 puts YOLO in the loop
  (`E2E_PLAN.md`).
- Neither CV bench runs gz; the drift suite does. SAPIEN was tested against
  gz, came out worse, and is out for good (removed 2026-09-24).
- `sentry_v2` collides, but what it does when driven into a wall hasn't been
  checked. That matters the day obstacle *avoidance* becomes something to
  demonstrate.
- The EKF numbers above predate the A2M8 lidar (800 beams, 0.01 m noise; was
  3000 beams, 0.03 m) and rf2o's per-scan matching. Re-run before quoting
  them. The drift suite was re-run 2026-09-24.
- C2 moves 2x between runs on the same cell, so compare C2 changes over
  three runs, not one.
