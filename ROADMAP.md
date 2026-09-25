# Where the project is going

A localization suite that can be believed, and CV cut in half at `TargetState`
with a bench for each half. 2026-09-23, updated the same evening: a sim that
stays up now comes first. Updated 2026-09-24: the sim stays up, runs
`sentry_v2`, and the drift suite passes.

## Where we actually are

| Thing | State |
|---|---|
| Test stack | **One gz session per run**, `sentry_v2` with collision and sprung wheels. Same verdicts shared, fresh per scenario, and alone |
| Localization drift suite (7 scenarios) | **7 pass** at `--backend amcl --use-ekf`, unthrottled, A2M8 lidar, per-scan rf2o (2026-09-24, 212 s with GUI): drift_correction 0.14 m, with obstacle 0.17 m, moving obstacles 0.18 m, against 0.40 m. `odom_stuck` passes its liveness check but loses the robot (ground-truth error up to 4.3 m) |
| EKF fusion path | **63% better than raw `/odom`** at 4 m/s, real time (0.050 m vs 0.134 m mean), with rf2o's `fixed_heading` and `/odom` prior |
| Shot-hit bench (10 cells) | **C1 aim bench (no gz) passes 10/10**, 96-99% every cell, chase mode (2026-09-24). The gz tracker bench hasn't run since Part 1's rewrite |
| Target in sim | Phantom: `target_driver` integrates a pose, no gz entity exists |
| CV seam | **Hard**: `point_to_cv_target` reads `TargetState` and `RobotPose` only. `TargetState` carries confidence, center, velocity, yaw, yaw_rate, and per-pair `radius[2]`/`z_offset[2]` |

The two suites fail for different reasons and only one of them is a real
defect. `drift_correction`'s threshold measures `map->odom` residual semantics,
so under `--backend none` it reads the robot's own motion around the loop and
fails without indicating anything. The shot-hit cells are red because aiming at
a spinning chassis center with no shot timing genuinely misses.

## Done: a sim that stays up

Every drift scenario and every `suite:=ekf` run starts gz, spawns the robot and
brings up localization from scratch. Six scenarios means six bring-ups, and any
one of them can come up badly. The target is one gz session per test run: each
scenario puts the robot back at spawn, resets `pose_emulator`'s noise state, and
restarts only the localization stack.

The catch is the standing rule in `sim/AGENTS.md`, "always fully restart `sim`
before restarting SLAM/explorer", written because partial restarts left stale TF
and pose state. A persistent sim has to make that reset real: sim time keeps
running forward (no TF jump), `pose_emulator`'s slip, drift and stuck state are
cleared, and spawned obstacles are removed.

**Built (sim `main`, 2026-09-23):** pytest starts `part:=sim` once. Before each
scenario, `_reset_sim` stops the robot stack, teleports to spawn, removes
spawned models, sets `pose_emulator`'s params and calls its new `~/reset`, then
launches `part:=robot`. `restart_sim:=true` keeps the old path. Lint and test
collection pass; no sim has been launched with it yet. The drift suite is
gz-only now: the reset goes through gz services, and sapien is no longer
supported.

**First run (amcl + EKF, 1×, 230 s, one gz process):** baseline and
noise_correction pass; drift_correction 0.42 m and drift_correction_obstacle
0.50 m fail against 0.40 m (unthrottled read 3–4 m); `jerk_with_motion`'s robot
stack never produced `/scan` (cause not captured, logs now kept per scenario);
`odom_stuck` failed only on an rviz log line, now skipped.

**Done when:** the drift suite runs all six scenarios against one gz process,
and a scenario gives the same verdict run alone, run sixth, and under
`restart_sim:=true`. **Met 2026-09-24** on `sentry_v2`, after two fixes: a
`pose_emulator` race (slip switched on between `set_parameters` and `~/reset`
crashed it), and the obstacle now spawns after the robot leaves spawn, since a
box inside the colliding chassis stalls gz.

### S2: Move to the new 3D model, for collision and suspension

`urdf/sentry_v2`, generated from the mechanical team's Onshape export by
`tools/simplify_urdf.py`, replaces `sentry.urdf.xacro` as what spawns. It has
collision shapes on all ten bodies, which answers the collision-proxy question
C2 and A4 were waiting on from the other direction. Pitch limits, suspension
travel and spring rate are still placeholders.

**Wired in (sim `main`, 2026-09-24):** `sentry_v2` is sim's default spawn,
and `thornbots_pkg`'s TF and the CV chain (head IK, emulator, shot-hit scoring)
moved to it. The drift suite passes on it. The chassis picks up ~1° of yaw
in hard corners (noted, not acted on).

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
0.17 m against 0.23–0.26 m at real time before the lidar change. `suite:=ekf`
hasn't been re-run. If it differs, audit every node for wall-clock timers,
rates and timeouts.

## Track A: Localization (paused)

Paused on 2026-09-23 so the sim can be made reliable first. Where it stopped:

### A1 (done): rf2o's sign was never wrong

`suite:=ekf` now scores each leg's displacement *vector* for `/scan_odom`,
`/odom` and the EKF against `/sim/raw_odom`. At 4 m/s:

| Run | `/scan_odom` per leg | EKF mean error |
|---|---|---|
| unthrottled, stock rf2o | ×0.40–1.00, drifts to −19° | 3.68 m |
| unthrottled, `73744a3`'s inverted warping | ×2–7, up to 179° off | 49.6 m |
| real time, stock rf2o | ×0.94–1.00, drifts to −5° | 0.205 m (raw `/odom` 0.169 m) |
| unthrottled, 1 m/s, stock rf2o | ×1.00, 0.3° mean | 0.025 m (raw `/odom` 0.37 m) |

The "backwards" reading was a test artifact. rf2o's loop runs at 20 Hz on the
wall clock and keeps only the newest scan, so a sim running 2–3× real time makes
it skip scans and match pairs up to a metre apart. `73744a3` is reverted.
rf2o has matched every scan in its callback since `thornbots_workspace#11`;
until S4 confirms it, compare unthrottled EKF numbers against a real-time run.

**Left:** rf2o's yaw drift, on a chassis that never rotates, corrupts its x/y,
and the EKF trusts them at 0.02². Either stop rf2o's heading from drifting or
stop fusing its absolute position. **Done when:** EKF error ≤ raw `/odom` at
real time, and `noise_correction` passes with `use_ekf` on.

**Met 2026-09-24.** `fixed_heading` pins rf2o's yaw. Pinning alone left legs
from rest short (×0.86–0.98): rf2o's prior is the last scan's motion, which is
"stopped" at every leg start. `odom_prior_topic: /odom` seeds each match with
wheel odometry's motion instead, and every leg reads ×1.00.

### A2 (done): Slip corrupts velocity

Landed, not yet measured. `odom_slip_ratio` now scales `/pose`'s `vel_x`/`vel_y`
by the same `(1 − ratio)` as position. Every EKF number before this was taken
with true velocity under slip.

### A3: One metric per backend

`MAX_DELTA_THRESHOLD` stays the assertion where a backend owns `map->odom`.
Under `--backend none` the watched edge becomes `odom->root` and the scenarios
switch to ground-truth error against `/sim/raw_odom`; `test_ekf_ground_truth.py`
becomes that assertion rather than a side experiment.

**Done when:** six scenarios green at the target config, and every failure
elsewhere points at a real defect.

### A4: New scenario: moving obstacles

Other robots driving around while we drive the cornering loop. Needs machinery
the sim does not have yet: an entity that moves. `spawn_box_obstacle` already
proves the inline-SDF `ros_gz_sim create` path works mid-scenario; what's
missing is something to drive what it spawns.

Build one node, `actor_driver`, that spawns N entities and walks each along a
path by `set_pose`, the same teleport `auto_explore` uses. Two or three crossing
at 0.5–2 m/s through the loop.

Two pass conditions, because a moving obstacle can hurt localization two ways:

- AMCL pose error against truth stays under threshold while transient returns
  come and go.
- Under `slam`, the occupancy grid does not keep the actors' paths as walls.
  Sample the cells they crossed at the end of the run.

This node is the shared piece: Track C's opponent robot is the same mechanism
with one entity and a different path.

**Built and passing (sim `main`, 2026-09-24):** `actor_driver` walks three
boxes across the south, west and north edges at 0.5–2 m/s, through a
`set_pose` bridge, and keeps them clear of the robot's next second of route.
The boxes have no collision, since `gpu_lidar` renders visuals and contact
with the field mesh cost ~3× sim speed. `moving_obstacles` scores like
`drift_correction`: 0.18 m against 0.40 m. The SLAM occupancy-grid check is
still to do.

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

**Part 1 goes first.** It is the half that misses today, it is the half that can
be tested against perfect knowledge, and it tells us how much of the
moving-target miss is even estimation's fault before we touch estimation.

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
- *Then* part 2: `ArmorEKF` estimates a per-pair z. It puts all four panels at
  one height today, which is why staggering them 9 cm drops the stationary case
  from 98% to 30%. `TargetState.z_offset[2]` is the field.
- Part 2 owns all hardware latency. `TargetState` describes the target now:
  the tracker works out capture time, predicts forward to its publish time and
  stamps that. Part 1 only extrapolates into the future, over fire-to-impact
  time. Today Part 1 adds the state's age instead, covering Part 2's delay.

## Track C: Two benches, one per half

### C1: Aim bench, perfect knowledge (standalone, not run)

The current shot-hit bench with its input replaced. A new emulator mode
publishes ground-truth `TargetState` straight from `/target/ground_truth_odom`:
all four panels, exact center, velocity, yaw, yaw_rate, both radii, both
heights. The tracker is not launched. Scoring geometry stays as it is.

With perfect knowledge, a miss is an aiming defect and nothing else. That makes
the floors real numbers instead of the placeholder
`MOVING_MIN_HIT_RATE = 0.25`, which was written to state an intent and has never
been measured against a working stack.

**Passing (2026-09-24):** `shot_hit.launch.py target_state:=truth` runs no gz:
a `/clock`, a fixed shooter point, `target_driver`'s phantom target and
`target_state_truth`, with each shot leaving toward the newest aim (a perfect
gimbal). 10/10 at 96-99% in chase mode, every tick firing. Floors are still
the placeholder (`CV_SPLIT_PLAN.md` 1.7).

### C2: Estimation bench, real target, fake detections

A real entity in the world, spawned from the sentry URDF as the opponent, driven
by `actor_driver`. Detections are still synthesized rather than rendered (no
YOLO in the loop), but they come off the entity's true pose instead of a phantom
integrator. Nothing fires. Part 2 is benchmarked only on how close its
`TargetState` gets to truth, compared at its own stamp (`CV_SPLIT_PLAN.md` 2.0):

- panel error, the four implied panel positions against the true four
- center, velocity, yaw, yaw_rate, radius and z_offset error
- time from first detection until panel error settles

> **The old snag, answered by S2.** The old sentry URDF had no collision
> geometry, so a lidar couldn't see it and the opponent needed a proxy.
> `sentry_v2` has collision on all ten bodies and `root` still has no parent
> joint, so `set_pose` teleports work and an opponent spawned from it is
> visible. The same goes for A4's actors.

### C3: The two cases neither bench has (built, not run)

- **We are moving.** Drive a scripted leg while engaging. Closes the
  `shooter_vel` hole in `CV_TEST_GAPS.md` gap 2 (today only its wiring is
  pinned, its magnitude is untested) and exercises odom-frame filtering while
  `root` moves.
- **Depth changes.** `target_driver` only traverses laterally. Add radial and
  diagonal paths. Depth error grows with range squared while bearing error stays
  near a pixel, which is the entire reason `ray_covariance` is anisotropic, and
  nothing currently drives a target along the ray.

Both run on both benches. On C1 they test the aim solve; on C2 they test the
estimate.

**Built (sim `main`, 2026-09-23):** `shooter_speed:=` bounces our chassis along
y (±1 m) through every case. `target_path:=radial`/`diagonal` turns
`target_driver`'s path by `path_angle_deg`, with presets that keep the near
panel past ~1.2 m. Both work with either `target_state:=`, so they're ready for
C2 as well.

## Track D: ROS 2 Jazzy (last)

The image is built on Humble: `nvcr.io/nvidia/isaac/ros:humble-3.2`,
`Dockerfile.ros2_humble`, `CONFIG_IMAGE_KEY=ros2_humble.realsense.thornbots`,
and `--rosdistro humble` in rosdep. Moving to Jazzy means an Isaac ROS release
built on it and Ubuntu 24.04, a new gz pairing for `sim` (Jazzy pairs with
Harmonic), and a pass over every package for API changes.

It waits until every other track is done, so no suite result gets mixed up
with a distro change. **Done when:** the drift suite, `suite:=ekf` and both
benches give the same verdicts on Jazzy as on Humble, and `thornbots_pkg`'s CV
tests (`point_to_cv_target`, `target_selector`, `target_tracker`) pass.

## Order of work

1. **A sim that stays up.** Done 2026-09-24.
2. **C1 aim bench.** The sim publishes the perfect `TargetState`; no tracker,
   selector or detection emulator. Needs no new sim entity, so nothing blocks
   it.
3. **B part 1: pair-aware aim, lead at speed, the sideways offset,** measured
   on C1 after the bench's case-to-case leak is fixed. This is where the moving
   cells turn.
4. **C3's moving-shooter and depth cases on C1,** while the bench is still the
   only thing in the loop.
5. **S2, move to `sentry_v2`** (wired in 2026-09-24), then
   `actor_driver`. Together they unblock C2 and A4.
6. **C2 estimation bench,** with camera latency in the emulator, then B part
   2's latency correction and per-pair z scored on it, then C3's cases again
   against the estimate.
7. **Back to Track A:** A3's per-backend metric, then A4 moving obstacles,
   and why `odom_stuck` loses the robot while passing (`sim/AGENTS.md`).
   rf2o's yaw drift was fixed in A1.
8. **Move from ROS 2 Humble to Jazzy,** once everything above is done. See
   Track D.

## Caveats

- Detection noise in sim is 0.005 m against a D435's centimetres, so every CV
  rate here runs optimistic. The benches rank changes; they don't predict the
  field.
- Rendered detections stay out of scope for both benches. A third bench,
  someday, with YOLO in the loop.
- Both benches are gz-only. SAPIEN was tested against gz, came out worse, and
  is out for good (removed 2026-09-24).
- `sentry_v2` collides, but what it does when driven into a wall hasn't been
  checked. That matters the day obstacle *avoidance* becomes something to
  demonstrate.
- The EKF and shot-hit numbers above predate the A2M8 lidar (800 beams,
  0.01 m noise; was 3000 beams, 0.03 m) and rf2o's per-scan matching. Re-run
  before quoting them. The drift suite was re-run 2026-09-24.
- Shot-hit results were bimodal on 2026-09-21: two runs swapped 98%/1% and
  2%/84%. Worth understanding before trusting a single-run comparison on C1.
