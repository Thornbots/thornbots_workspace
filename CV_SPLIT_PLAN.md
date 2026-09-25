# Plan: split CV at `TargetState`

ROADMAP.md Track B and C, 2026-09-24. Part 1 (`point_to_cv_target`) aims and
fires from a `TargetState`. Part 2 (`target_selector` + `target_tracker`) builds
that `TargetState` from detections. **We start with Part 1, the hitting side.**
It is the half that misses today. **The sim tests it on perfect models:**
`target_state_truth` publishes the target's true `TargetState`, the tracker is
not launched, and every miss left is Part 1's own. Part 2 waits until Part 1's
floors are measured.

## Where Part 1 actually stands

The roadmap used to say Part 1 still had to pick a panel and time the shot
against the spin. `plan_shot` (`thornbots_pkg/point_to_cv_target_core.py`)
already does both. Above `spin_enter_rad_s` (3 rad/s) it aims at a point on the
center-to-shooter line and sets `delay_ms` to land on the next quarter-turn
alignment, firing only when that delay fits inside one publish tick. Below it,
it leads the tracked panel and fires at once. Every moving shot-hit cell spins
at 1 to 2 Hz (6 to 12.6 rad/s), so every moving cell already runs in spin mode.

What Part 1 lacks:

1. Spin mode aims at the mean radius `(r + other_r)/2` and at `center.z`. It
   never works out which pair arrives at the next alignment, so it uses neither
   that pair's radius nor its `z_offset`. Non-spin mode ignores `z_offset` too.
   That is the aim side of the staggered collapse (98% to 30%), and it can be
   fixed now: `TargetState` already carries per-pair heights.
2. At 4 m/s shots trail the panel by about 0.23 m. That number came from the
   tracker. On a perfect model the velocity is exact, so any trail left there
   is Part 1's own horizon: fire decision to muzzle exit (`firmware_latency_s`,
   0.05 s) plus flight time.
3. Every case, stationary included, lands 2 to 4 cm to one side. A stationary
   run on a perfect model pins it to TF/muzzle geometry.
4. It still subscribes to raw `/cv/panel_detection` for liveness, confidence and
   track id, and aims at `state.panel` while the tracker is unconverged. That
   path fires with `delay 0`.

## Aiming: Part 1 on C1

Every Aiming run is `shot_hit.launch.py` (gz-free since 2026-09-25). No
tracker, no tracker comparison: those belong to Estimation, on C2.

### 1.0 Harden the seam; the sim publishes the perfect model

**Done 2026-09-24.** Later the same day C1 dropped gz altogether: a point
shooter with a perfect gimbal (`sim/README.md`), and `target_state_truth`
publishes each sample as it arrives, not on a timer that sent it ~17 ms late.

Today `target_state_truth` publishes only when a `/cv/robot_panels` message
arrives, so C1 still runs `cv_target_emulator` and `target_selector`, and Part 1
still reads raw panels for liveness. The perfect model should stand alone, which
needs Part 1 to stop reading panels first. This goes first because every later
step is measured on it, and because 1.3's pair logic should be written against
the new fields once rather than twice.

One logical change across three submodules, pushed in this order, then one
gitlink bump:

| Package | Change |
|---|---|
| `ros2_dji_serial_bridge` | `TargetState`'s header comment says the stamp is the time the state describes (its publish time), and it gains `float32 confidence`, renames `centre` to `center`, and replaces `radius`/`other_radius` and `z_offset`/`other_z_offset` with `float32[2] radius` and `float32[2] z_offset`, indexed by panel pair `k % 2` (`[0]` is the tracked panel's pair). Every user in `thornbots_pkg` and `sim` follows, including `ArmorEKF`'s `other_r` and `plan_shot`'s `other_r` argument |
| `thornbots_pkg` tracker | Publishes on every `/cv/robot_panels` message, before convergence too, with `valid=false`, `confidence` from the selector's winning panel, and center/yaw seeded from the raw panel |
| `thornbots_pkg` Part 1 | Drops the `panel_topic` subscription. Liveness is `TargetState` age, track id and confidence come off the message. `!valid` aims at the tracked panel with no lead. `/cv/panel_polygon` moves to `target_selector` |
| `sim` | `target_state_truth` publishes on its own timer at `publish_rate_hz` (60, the emulator's camera rate) from `/target/ground_truth_odom` alone: the target's current state, stamped with its own sample time and published at once, with no added latency. `valid=true`, `confidence=1`, one fixed track id, no field of view or occlusion. `shot_hit.launch.py target_state:=truth` stops launching `target_selector` and `cv_target_emulator` |

A test in `test_point_to_cv_target.py` pins the contract: the node subscribes to
`TargetState` and `RobotPose` only. Done when a truth run fires with nothing
upstream of `/cv/target_state` but `target_driver` and `target_state_truth`.

### 1.1 Make the bench trustworthy

**Resolved 2026-09-24.** The leak was Part 1: stationary aim went to panel 0,
whichever way the previous case left the target facing. It now aims at the
facing panel, and the gz-free bench has no head or chassis state to carry.

Shot-hit scores depend on the case before them: staggered stationary read 0.3%
right after flat 4 m/s and 99% twice alone. Until that is fixed, a before/after
comparison means nothing.

- Candidates, cheapest first: `point_to_cv_target`'s `spinning` hysteresis and
  `last_fire_time`; `target_state_truth`'s 2 s `history_s` (gone if 1.0 drops
  the history); `target_driver`'s pose at the switch; the head still slewing
  when `SETTLE_S` ends.
- Fix: `run_case` resets whatever carries over, through a `~/reset` service like
  `pose_emulator`'s, and settles until the head is on target rather than for a
  fixed time.
- Done when a cell scores the same run alone and run after flat 4 m/s.

Then take the first C1 baseline, both layouts. Nobody has run C1 yet, and every change
below is measured against it. Each run needs the user's go-ahead
(`sim/AGENTS.md`).

### 1.2 Fixed lateral offset (stationary)

**Not Part 1's.** On the perfect model stationary shots miss by 2 mm (gz) and
0 mm (point bench). The 2 to 4 cm came with the tracker; it moves to Estimation.

Read `panel_right_of_shot_m` from `shots.jsonl`. If the 2 to 4 cm survives on
the perfect model, it is geometry: `muzzle` against `root`, the `headlink` yaw
offset, or the harness's duplicated FK chain disagreeing with the URDF since the
`sentry_v2` move. Fix it at the source, not with an aim trim.

### 1.3 Pair-aware aim: radius and height

**Done 2026-09-24.** Staggered matches flat. In spin mode the pair also has to
hold until its last shot has left the muzzle: switching it on the aim horizon
moved gz's gun under that shot (staggered 0.5 m/s 58% to 97%).

In `plan_shot`, spin mode picks the pair that lines up at the next quarter-turn
(parity of the step count from the tracked panel) and aims at `radius[k % 2]`
and `center.z + z_offset[k % 2]`. Non-spin mode adds `z_offset[0]`. Unit-test
both against the armor model in `TargetState.msg`. Done when staggered
stationary matches flat (about 99%) and staggered moving cells come within a few
points of flat.

### 1.4 Lead at speed

**Done 2026-09-24, not as planned.** The overshoot at speed was the gimbal,
not the firmware: gz's head reaches a moving setpoint in 35 ms, and the aim
led by 62 ms. Part 1 now leads by `gimbal_lag_s` plus half the publish tick,
and times the fire over `firmware_latency_s`.

If 4 m/s still trails, the velocity is exact, so the missing time is latency.
Measure fire decision to muzzle exit in sim (the harness logs `fire` and
`t_fire`) and set `firmware_latency_s` from it. Whatever trail the tracker adds
on top is Part 2's velocity error, in 2.3.

### 1.5 Path-end braking

**Done 2026-09-24.** `TargetState` gained `acceleration`; the truth node fills
it, Part 1 solves the intercept on the curved path, and flat 4 m/s went from
17% to 46% on gz. The tracker publishes 0 until Estimation adds it. The
misses left cluster where the acceleration switches, which nothing predicts.

Bin 1 to 2 m/s misses by the target's position on its path. If they cluster at
the 6 m/s² braking ends, constant-velocity extrapolation is the limit. Record
it and move on: fixing it needs acceleration in `TargetState`.

### 1.6 Spin fire window

**Superseded 2026-09-24 by chase mode** (`chase_settle_s >= 0`): lead the
facing panel and fire every tick, leaving mid-hold of the aim current at exit.
Point bench, every tick: 96-99% of shots hit, against center aim's one tick
in five. Chase needs the gimbal to jump ~7 deg per quarter turn, so the node
default stays center aim until that is measured on hardware.

The delay must fit inside one tick (25 ms at 40 Hz), and a quarter-turn at
12.6 rad/s takes 125 ms, so the node fires on about one tick in five. Check with
`panel_hits.jsonl` that shots land on the aligned panel inside its 145° cone. If
they arrive late, fire on the alignment after next when that one fits.

### 1.7 Floors

**Open.** The point bench passes 10/10 at 96-99% (2026-09-24, one run).

Replace `MOVING_MIN_HIT_RATE = 0.25` with per-cell floors from the final truth
run: lowest of three runs minus 10 points. Part 2 never gets hit-rate floors;
it gets error thresholds on C2.

### 1.8 C3 cases on C1

**Open.** The point bench has a fixed shooter, so `shooter_speed` needs a
moving `root` there first.

`shooter_speed:=1.0` and `target_path:=radial`/`diagonal`, already built. A drop
with `shooter_speed` points at `shooter_vel`'s sign or frame
(`sim/CV_TEST_GAPS.md` gap 2); a drop on radial points at the lead solve along
the ray. Each gets its own floor.

## Estimation: Part 2 on C2

Part 2 is benchmarked only on how close its `TargetState` gets to the truth.
Nothing fires on C2, and shot-hit rates are not how Part 2 is judged: a miss
there mixes both halves, and Aiming already owns the aim.

### All hardware latency belongs to Part 2

`TargetState` describes the target now. Part 2 owns every delay between the
target being somewhere and the state reaching Part 1: exposure, readout, USB,
YOLO, `roi_depth_node`, the tracker itself and delivery. It works out when the
image was captured, predicts the model forward to the moment it publishes, and
stamps the message with that moment. Part 1 does no latency correction. It
extrapolates from the stamp into the future: the part of a frame since the
state arrived, `firmware_latency_s`, and flight time.

**Built 2026-09-25, not run.** The tracker used to stamp its output with the
detection stamp, so Part 1 covered Part 2's delay. The RealSense stamp's
relation to capture time is still unmeasured.

- `target_tracker`'s `camera_latency_s` (0): capture time = detection stamp -
  `camera_latency_s`, used for the EKF update and the camera TF lookup. It
  predicts to its publish time and stamps that.
- `cv_target_emulator`'s `camera_latency_s` (0, `cv_camera_latency_s` in
  `sim.launch.py`) stamps each detection that much after its sample, on top
  of the `publish_latency_s` delivery delay.
- Measure the real camera's latency on hardware (RealSense metadata timestamps,
  or a blinking LED against the stamp) before trusting a field number.
- C1 carries none of this: `target_state_truth` publishes the current true
  state, which is the contract Part 2 has to meet.

### 2.0 C2 estimation bench

**Built 2026-09-25, not run as a suite** (`sim/launch/estimation.launch.py`,
`test_estimation.py`). One change from below: the target stays
`target_driver`'s phantom, and the emulator and scorer read its exact truth.
An entity moved by `set_pose` steps at the call rate and its gz pose lags the
integrator, so it would give worse truth, not better; spawn a visual one
once YOLO sees rendered frames. Our robot, head and camera are real gz. Each
case restarts the track by switching detections off for 1 s. The facing
panel's error (the one Part 1 aims at) was added: on a still target only
that panel is observable, so convergence is measured on it. `LIMITS` is
empty; `sim/tools/estimation_limits.py` fills it from three runs. A headless
probe (8 s cases, not a baseline): staggered stationary 1.2 cm facing p95;
2 m/s with blackout, and 1 m/s with our chassis moving, ~35 cm p95 and
~10 s to converge.

- Spawn one opponent from `sentry_v2`, driven by `actor_driver`, which gains yaw
  (spin) and `target_driver`'s path profiles so C2 runs the same cells as C1.
- `cv_target_emulator` takes panel poses from the entity's true pose (gz pose
  bridge) instead of `target_driver`'s integrator. `target_driver` stays for C1
  until C2 is proven.
- `test/cv/test_estimation.py` over `estimation_harness.py`. Each published
  `TargetState` is compared with the truth at its own `header.stamp`, so a
  wrong stamp shows up as error. Per cell, mean and p95 of:
  - panel error: the four panel positions the state implies against the true
    four, the one number that says what Part 1 would be handed;
  - center and velocity error;
  - yaw error (mod a quarter-turn, matching pairs) and `yaw_rate` error;
  - `radius` and `z_offset` error per pair;
  - time from first detection until panel error stays under a threshold.
- Thresholds per metric come from the first working run, lowest of three plus
  a margin, like Aiming's floors.
- Dropout and handoff cases by masking detections in the emulator.
- Done when C2 runs every C1 cell in one gz session and scores the same run
  alone and in sequence.

### 2.1 Camera latency on C2

**Ready to run:** `estimation.launch.py camera_latency_s:=0.03` against the
default 0; `tracker_camera_latency_s:=0` shows the error left undone.

Turn on the emulator's camera-latency offset alongside its delivery delay.
Done when the tracker, with `camera_latency_s` set to match, publishes states
whose error at their own stamp matches the zero-latency numbers.

### 2.2 Per-pair z

**Built 2026-09-25, unit-tested.** `ArmorEKF` carries `dz`, the tracked
pair's height above the centre, with the other pair at `-dz` (only their
difference is observable); an odd handoff flips it. Published as
`z_offset = [dz, -dz]`.

Per-pair z in `ArmorEKF`, mirroring the per-pair radius, published into the
`z_offset` array. Done when staggered cells' `z_offset` and panel error match
flat cells'.

### 2.3 Velocity lag

**Ready to run:** `process_noise_accel:=` sweeps the tracker on C2; the
velocity error is in `estimation.jsonl` per case and per state.

The 0.23 m trail at 4 m/s, minus whatever 1.4 found in Part 1's horizon, is
Part 2's: velocity error, or latency it didn't predict across. Tune `process_noise_accel` against C2's velocity-error trace,
path ends included.

### 2.4 C3 cases

**Ready to run:** `shooter_speed:=1.0` drives our gz chassis, `target_path:=`
radial or diagonal; `center_along_m` and `center_across_m` split the center
error on the ray from us.

C3's shooter-moving and radial cases on C2, scored the same way. Radial is the
case `ray_covariance` exists for: depth error grows with range squared, so
center error along the ray should grow and error across it should not.

## Hitting while we move: target and aim in the world

Added 2026-09-25 at the user's request: we have to hit while our own chassis
drives and turns, so the target and our aim both live in a world frame and
only the last step turns the aim into gimbal angles.

The world frame for aiming is `odom`, not `map`. REP-105 keeps `odom`
continuous; `map` jumps each time localization corrects, and a jump
mid-shot moves the aim. `map` is for strategy (zones, where the enemy is
on the field). Where it stands:

- **Target: already in the world.** `TargetState` is in `odom`, and Part 2
  places each detection with the camera's TF at capture time.
- **Aim solve: already in the world.** `plan_shot` solves the intercept in
  `odom`, including our velocity (1.8).
- **Aim output: not in the world.** `CVTarget` is a `root`-frame point,
  converted with the newest TF (`point_to_cv_target.py`, `Time()` lookups).
  The MCB holds that point while the chassis moves on, so the aim drifts in
  the world by our motion over the command's age.
- **Our pose: incomplete.** `RobotPose` has no chassis yaw (`head_yaw` is the
  gimbal's), the stack assumes a fixed heading (`sim/AGENTS.md`: the
  chassis already picks up ~1 deg in sim), and the stamp is Jetson arrival.

What it needs, in order:

| Step | Package | Change |
|---|---|---|
| W.1 | `ros2_dji_serial_bridge`, firmware | `RobotPose` gains chassis yaw and yaw rate, and a capture stamp (Stamps table below: first-byte time less wire time, later an MCB clock). `odom->root` carries the yaw |
| W.2 | `thornbots_pkg` | Every TF lookup at the time the data was true: the camera at capture (Part 2 does this), our pose at the fire horizon in Part 1, not `Time()` |
| W.3 | `ros2_dji_serial_bridge`, firmware | `CVTarget` becomes a world-frame aim: the intercept point in `odom` (or gimbal yaw/pitch relative to the world) plus its stamp. The MCB holds it with its IMU and odometry while the chassis moves and turns, the usual RoboMaster split. Needs the firmware's `CVData` to follow (`thornbots_pkg/AGENTS.md`) |
| W.4 | `sim` | C1: our `root` turns as well as translates (`shooter_speed` only slides it along y today), and the shooter carries the aim in `odom` the way W.3's MCB would. C2: our gz chassis turns while tracking |
| W.5 | `sim`, `thornbots_pkg` | Floors and limits for the new cells, like 1.7 and 2.0 |

W.1 and W.3 change the wire protocol and the MCB firmware, which live
outside this workspace; agree them with the firmware side first. W.2 and
W.4 can start now. Until W.3 lands, sim can score the gap by holding the
last root-frame aim while our chassis moves.

## Stamps

Workspace rule (`CLAUDE.md` § Timestamps): every internal message is stamped as
well as its node can. Audit of 2026-09-24. The CV chain mostly complies:
`roi_depth_node` and `target_selector` carry the detection stamp through,
`cv_target_emulator` stamps sample time, `CVTarget` stamps decision time,
`lidar_self_filter` and `pose_translator` pass the input's stamp on. The gaps:

| Where | Today | Best the node can do | When |
|---|---|---|---|
| `target_tracker` → `TargetState` | Detection stamp, not the time the state describes | Publish time, after predicting forward | **Done 2026-09-25** (`camera_latency_s`, stamp at publish) |
| `dji_serial_bridge` → `RobotPose`, `RefSysStatus` | `now()` after the frame is parsed | Stamp when the frame's first byte is read, minus its wire time at the baud rate. Later, an MCB millisecond clock on the wire, the mirror of `CV_MSG`'s `stamp_ms`, mapped to ROS time by offset | Before any field test of Part 1 while we move (1.8): `odom->root` TF and our velocity both come from it. The MCB half is firmware work outside this workspace |
| Camera → `Detection2DArray` | Image stamp carried through the YOLO chain, not verified end to end; its relation to capture unmeasured | Verify the stamp survives the chain, then measure capture latency | Estimation, on hardware |
| `mcb_relay` → relocalize | Bare `geometry_msgs/Point` | `PointStamped` with the stamp of the localization pose it came from; the bridge's subscriber follows | Own change, not CV-blocking |
| `dji_serial_bridge` `~/nav_goal` | Bare `geometry_msgs/Point` | `PointStamped`, stamped when the goal was chosen | Same change as relocalize |

`/cmd_vel` stays a bare `Twist`: gz's diff-drive plugin and the harnesses expect
it, which is the standard-interface exception in the rule.

## Decisions for the user

| Question | Recommendation |
|---|---|
| Fire before the tracker converges? Today it fires at the raw panel, unled | Aim, don't fire until `valid` |
| `confidence` as a `TargetState` field, or keep Part 1's panel subscription? | New field; the subscription keeps the seam soft |
| Floor margin under the measured truth score | Lowest of three runs minus 10 points |

## Commits

1.0 is `ros2_dji_serial_bridge`, `thornbots_pkg`, `sim`, pushed in that order,
then one bump. 1.1 is `sim` (plus `thornbots_pkg` if the leak is in a node) and
one bump. 1.2 to 1.6 each get their own commit and bump, with C1 before/after
numbers in the message. Update this file and ROADMAP.md in the bump for the
step they describe.
`thornbots_pkg` is shadowed in `/workspaces/ros2_ws`: rebuild it in
`isaac_ros-dev` and check `ros2 pkg prefix` before any run.

Sim detection noise is 0.005 m and C1 has no estimation noise at all, so C1's
floors describe the aim solve alone. Neither bench predicts field hit rates;
they rank changes.
