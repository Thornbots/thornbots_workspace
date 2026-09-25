# Where the project is going

A localization suite that can be believed, and CV cut in half at `TargetState`
with a bench for each half, then the whole CV stack tested end to end in sim
(`E2E_PLAN.md`). Updated 2026-09-25: aiming is done on C1, C2 has had its
first runs, and Track A has two runs, a map check and S3 left.

## Where we actually are

| Thing | State |
|---|---|
| Test stack | **One gz session per run**, `sentry_v2` with collision and sprung wheels. Same verdicts shared, fresh per scenario, and alone |
| Localization drift suite (7 scenarios) | **7 pass** at `--backend amcl --use-ekf`, unthrottled, A2M8 lidar, per-scan rf2o (2026-09-24, 212 s with GUI): drift_correction 0.14 m, with obstacle 0.17 m, moving obstacles 0.18 m, against 0.40 m. `odom_stuck` passes its liveness check and loses the robot at 4 m/s, accepted as a limit (2026-09-25) |
| EKF fusion path | **63% better than raw `/odom`** at 4 m/s, real time (0.050 m vs 0.134 m mean), with rf2o's `fixed_heading` and `/odom` prior. Measured before the A2M8 lidar and per-scan rf2o; `suite:=ekf` needs a re-run (S4) |
| C1 aim bench (no gz) | **Done.** 40 per-cell floors from three runs each (2026-09-25), still and moving shooter, lateral, radial and diagonal paths, chase mode, 95-99% |
| C2 estimation bench (10 cells, gz) | **Three runs (2026-09-25), no limits yet.** Stationary cells 1.3 cm facing-panel p95; moving cells 0.12-0.51 m and 2x apart between runs, not yet traced. The tracker gained acceleration, a single-panel yaw measurement and a still-target hypothesis; see `CV_SPLIT_PLAN.md` "Where this stopped" |
| Whole CV stack in sim | Nothing runs the camera, YOLO, `roi_depth_node` or the serial link; planned in `E2E_PLAN.md` |
| Target in sim | Phantom: `target_driver` integrates a pose, no gz entity exists |
| CV seam | **Hard**: `point_to_cv_target` reads `TargetState` and `RobotPose` only. `TargetState` carries confidence, center, velocity, yaw, yaw_rate, and per-pair `radius[2]`/`z_offset[2]` |

## The sim

### Done: a sim that stays up (2026-09-24)

The drift suite runs every scenario against one gz process. Before each one,
`_reset_sim` stops the robot stack, teleports to spawn, removes spawned models,
resets `pose_emulator` and relaunches `part:=robot`; `restart_sim:=true` keeps
the old fresh-sim path. A scenario gives the same verdict alone, run sixth and
under `restart_sim:=true`. The suite is gz-only.

### Done: S2, move to `sentry_v2` (2026-09-24)

`urdf/sentry_v2`, generated from the mechanical team's Onshape export by
`tools/simplify_urdf.py`, is sim's default spawn, with collision on all ten
bodies. `thornbots_pkg`'s TF and the CV chain moved to it, and the drift suite
passes on it. Pitch limits, suspension travel and spring rate are still
placeholders, and the chassis picks up ~1° of yaw in hard corners (noted, not
acted on).

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

## Track A: Localization

### Done: A1, rf2o's sign, and A2, slip in velocity (2026-09-24)

rf2o was never backwards. Its wall-clock loop skipped scans in a fast sim and
matched pairs up to a metre apart; it now matches every scan in its callback.
`fixed_heading` pins its yaw, and `odom_prior_topic: /odom` seeds each match
with wheel odometry's motion, so every leg reads ×1.00 and the EKF beats raw
`/odom`. `odom_slip_ratio` now scales `/pose`'s velocity as well as its
position. `sentry_localization/README.md` has the measurements.

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

Part 1 went first, against perfect knowledge on C1, and is done
(`CV_SPLIT_PLAN.md` 1.0-1.8). Part 2 is on C2 now.

- **Corrected 2026-09-24:** this used to say Part 1 still had to pick a panel
  and time the shot against the spin. `plan_shot` already does both: above
  3 rad/s it aims on the center-to-shooter line and times the fire to the next
  quarter-turn, and every moving shot-hit cell spins faster than that. What it
  lacks is the arriving pair's own radius and `z_offset` (it aims at the mean
  radius and `center.z`), a latency budget that keeps up at 4 m/s, and a trace
  of the 2 to 4 cm sideways miss seen even on stationary targets.
- **Done 2026-09-24 (`CV_SPLIT_PLAN.md` 1.0):** Part 1 no longer reads raw
  panels. Liveness is the state's age; confidence and track id ride on
  `TargetState`. Before convergence the tracker publishes `valid=false` and
  Part 1 aims at `panel` without leading or firing. `/cv/panel_polygon` moved
  to `target_selector`.
- *Then* part 2: `ArmorEKF` estimates a per-pair z. It put all four panels at
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

### Done: C1, aim bench with perfect knowledge

The sim publishes ground-truth `TargetState` straight from
`/target/ground_truth_odom`: all four panels, exact center, velocity, yaw,
yaw_rate, both radii, both heights. The tracker is not launched, so a miss is
an aiming defect and nothing else.

**Passing (2026-09-24):** `shot_hit.launch.py` runs no gz:
a `/clock`, our shooter point, `target_driver`'s phantom target and
`target_state_truth`, with each shot leaving toward the newest aim (a perfect
gimbal). 10/10 at 96-99% in chase mode, every tick firing. Floors are per
cell from three runs, 2026-09-25 (`CV_SPLIT_PLAN.md` 1.7).

### C2: Estimation bench, fake detections

Detections are synthesized from the target's true pose (no YOLO in the loop),
with D435-like ray noise, and nothing fires. Part 2 is benchmarked only on how close its
`TargetState` gets to truth, compared at its own stamp (`CV_SPLIT_PLAN.md` 2.0):

- panel error, the four implied panel positions against the true four
- center, velocity, yaw, yaw_rate, radius and z_offset error
- time from first detection until panel error settles

**Built (sim `main`, 2026-09-25), three runs:** `estimation.launch.py` on
gz. The target is still `target_driver`'s phantom, since its truth is exact
and a `set_pose` entity's gz pose would lag; a visual opponent from
`sentry_v2` comes with E2E. Metrics as above, plus the facing panel's error,
which is what Part 1 aims at. Stationary cells read 1.3 cm facing p95. Moving
cells read 0.12-0.51 m and vary 2x between runs, and half speed scored within
that spread. `LIMITS` is empty until the error is traced and three more runs
fill it.

### C3: The two cases neither bench had (passing on C1, not run on C2)

- **We are moving.** Drive a scripted leg while engaging. Closes the
  `shooter_vel` hole (today only its wiring is pinned, its magnitude is
  untested) and exercises odom-frame filtering while
  `root` moves.
- **Depth changes.** `target_driver` only traverses laterally. Add radial and
  diagonal paths. Depth error grows with range squared while bearing error stays
  near a pixel, which is the entire reason `ray_covariance` is anisotropic, and
  nothing currently drives a target along the ray.

Both run on both benches. On C1 they test the aim solve; on C2 they test the
estimate.

**Passing on C1 (2026-09-25), three runs each:** `shooter_speed:=` bounces the aim
bench's `root` along y (±1 m) through every case, and each shot carries its
velocity. Part 1 aimed as if still, ~0.15 m off at 1 m/s; it now aims for our
own motion (`CV_SPLIT_PLAN.md` 1.8). `target_path:=radial`/`diagonal` turns
`target_driver`'s path by `path_angle_deg`, with presets that keep the near
panel past ~1.2 m. Moving shooter 95-99%; radial and diagonal 99%, above
lateral, since the target barely crosses the view.

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

Finished items come off this list; the next one is always 1.

1. **C2:** trace the moving-cell error and its run-to-run swing, starting
   with the camera TF at capture time while the head slews. Then three runs
   fill `LIMITS`, and camera latency, C3's cases and blackout each run three
   times (`CV_SPLIT_PLAN.md` Next).
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
bench runs.

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
- Both benches are gz-only. SAPIEN was tested against gz, came out worse, and
  is out for good (removed 2026-09-24).
- `sentry_v2` collides, but what it does when driven into a wall hasn't been
  checked. That matters the day obstacle *avoidance* becomes something to
  demonstrate.
- The EKF numbers above predate the A2M8 lidar (800 beams, 0.01 m noise; was
  3000 beams, 0.03 m) and rf2o's per-scan matching. Re-run before quoting
  them. The drift suite was re-run 2026-09-24.
- C2 moves 2x between runs on the same cell, so compare C2 changes over
  three runs, not one.
