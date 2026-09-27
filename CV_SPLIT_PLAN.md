# Plan: split CV at `TargetState`

ROADMAP.md Track B and C. Part 1 (`point_to_cv_target`) aims and fires from a
`TargetState`. Part 2 (`target_selector` + `target_tracker`) builds that
`TargetState` from detections. Updated 2026-09-26: Aiming is finished, and
what's left is Estimation, then hitting while we move.

## Where this stands

- **Aiming is done on the aiming bench.** `shot_hit_harness.py`'s `FLOORS` holds 40
  per-cell floors from three chase-mode runs each: still and moving shooter,
  lateral, radial and diagonal paths. `point_to_cv_target` reads only
  `TargetState` and `RobotPose`, and with `valid` false it aims at the
  measured panel with no lead and doesn't fire.
- **Part 2 model** (`thornbots_pkg`): `ArmorEKF` state is
  `[pos, vel, acc, yaw, w, r, dz]`, with Singer acceleration, a single-panel
  yaw measurement and a still hypothesis for a parked, non-spinning target.
  `thornbots_pkg/README.md` has the design.
- **The estimation bench runs on `bench_world`**, one C++ lockstep loop with no gz, paced by
  the nodes under test at ~5x: the ten cells take ~75 s. Five runs each on
  Humble and Jazzy (2026-09-26): stationary cells under 2 cm facing p95,
  moving cells 0.08-0.17 m medians, and runs agree within 10% except at
  4 m/s (0.13-0.27 m).
- **`LIMITS` covers all 60 the estimation bench cells** (`sim/test/cv/estimation_limits_data.py`,
  Jazzy, 2026-09-27): the default ten from six runs, each other case from
  three or four, at 2x the worst run and floored at 0.02. A run strays up
  to ~2x from the others, so 1.25x failed fresh runs. About a quarter of
  runs still trip on one outlier: a spin rate misread by 0.6-2 rad/s or the
  radius wandering, on a staggered or 4 m/s cell.
- **The other cases, facing-panel p95 against the default's 0.08-0.19 m:**
  camera latency 0.03 s, undone, matches it. Our chassis at
  1 m/s matches it. Radial doubles the error along the ray at 2-4 m/s
  (0.18-0.25 m against 0.09-0.11) while error across it drops, and
  stationary cells don't change, so it grows with speed along the ray, not
  with range. Diagonal falls between. Blackout (0.3 s of every 2 s) is
  2-3x worse, 0.14-0.35 m; staggered 0.5-1 m/s suffers most (0.28-0.30 m
  against 0.09).
- **The 4 m/s swing is the radius estimate wandering.** In the bad run of
  each 4 m/s cell (one of five each), radius error sits at 5-12 cm for
  10-20 s where the good runs hold ~2 cm, and facing-panel error follows it
  (correlation ~0.55). It isn't path ends, which come every ~1.9 s, and it
  isn't re-seeds: each case keeps one track.
- **Most of the old moving-cell error was the bench.** Until 2026-09-26
  `bench_world` paced on `TargetState`'s stamp, which the tracker sets at
  publish time, so it ran ahead while the tracker worked through a full
  queue 0.12-0.21 s behind capture. Moving cells read 0.29-0.33 m medians,
  with a quarter to a third of them past 0.5 m. It now paces on
  `/cv/tracker/measurement`.
- **`target_tracker` is the slowest node under test.** Profiled at ~8x:
  `ArmorTracker.step`'s small-matrix numpy is 46% of its main thread, its TF
  listener thread 27%. A C++ core would speed up the estimation bench and the Jetson; the
  user's call.

Next, in order:

1. Open for the user: whether to hold the radius tighter at 4 m/s, and
   why the spin rate is misread now and then (both above).
2. Open for the user: radial motion's along-ray error, and blackout
   recovery on staggered targets (above). Neither has a fix planned.
3. Open for the user: `valid` goes true after 2 updates, but a fresh track
   on a spinning target takes 0.3-3 s to lock (facing-panel error up to
   0.4 m in the first second). Spin-rate variance doesn't separate locked
   from not, so no threshold was added.

Left over from Aiming, none of it blocking:

- Chase mode (the default) needs the gimbal to jump ~7 deg per quarter turn
  and settle. Measure that on hardware and set `chase_settle_s` to it.
- Radial and diagonal paths with a moving shooter haven't run on the aiming bench.
- Flat 4 m/s misses cluster where the target's acceleration switches at its
  path ends, which nothing predicts.
- The 2-4 cm sideways offset seen with the tracker in the loop is gone on
  the perfect model, so it belongs to Estimation.

## Estimation: Part 2 on the estimation bench

Part 2 is benchmarked only on how close its `TargetState` gets to the truth.
Nothing fires on the estimation bench, and shot-hit rates are not how Part 2 is judged: a miss
there mixes both halves, and Aiming already owns the aim.

### All hardware latency belongs to Part 2

`TargetState` describes the target now. Part 2 owns every delay between the
target being somewhere and the state reaching Part 1: exposure, readout, USB,
YOLO, `roi_depth_node`, the tracker itself and delivery. It works out when the
image was captured, predicts the model forward to the moment it publishes, and
stamps the message with that moment. Part 1 does no latency correction. It
extrapolates from the stamp into the future: the part of a frame since the
state arrived, `firmware_latency_s`, and flight time.

**Built 2026-09-25, not run.** The RealSense stamp's relation to capture time
is still unmeasured.

- `target_tracker`'s `camera_latency_s` (0): capture time = detection stamp -
  `camera_latency_s`, used for the EKF update and the camera TF lookup. It
  predicts to its publish time and stamps that.
- `cv_target_emulator`'s `camera_latency_s` (0, `cv_camera_latency_s` in
  `sim.launch.py`) stamps each detection that much after its sample, on top
  of the `publish_latency_s` delivery delay.
- Measure the real camera's latency on hardware (RealSense metadata timestamps,
  or a blinking LED against the stamp) before trusting a field number.
- The aiming bench carries none of this: `target_state_truth` publishes the current true
  state, which is the contract Part 2 has to meet.

### 2.0 Estimation bench

**Built, runs as a suite** (`sim/launch/estimation.launch.py`,
`test_estimation.py`). `bench_world` (`sim/src/bench_world.cpp`) is the
whole world in one C++ lockstep loop: the phantom target with exact truth,
our chassis and head (gz's joint PD on the arm inertias), `/pose`, the head
controller and the detections. Each case restarts the track by switching
detections off for 1 s. `LIMITS` holds the ten default cells, printed by
`sim/tools/estimation_limits.py` from five runs (2026-09-26).

- `test/cv/test_estimation.py` over `estimation_harness.py`. Each published
  `TargetState` is compared with the truth at its own `header.stamp`, so a
  wrong stamp shows up as error. Per cell, mean and p95 of panel error (all
  four, and the facing one Part 1 aims at), center, velocity, yaw (mod a
  quarter-turn), `yaw_rate`, `radius` and `z_offset` per pair, and the time
  until the facing panel's error stays under 5 cm.
- Limits per metric come from three or more runs: the worst p95 x 1.25,
  never under 0.01, like Aiming's floors.
- Done when the estimation bench runs every aiming-bench cell in one session and scores the same run
  alone and in sequence.

### 2.2 Per-pair z

**Built, unit-tested.** `ArmorEKF` carries `dz`, the tracked pair's height
above the centre, with the other pair at `-dz` (only their difference is
observable); an odd handoff flips it. Published as `z_offset = [dz, -dz]`.
Done when staggered cells' `z_offset` and panel error match flat cells' on
the estimation bench.

### 2.3 Velocity lag

**Built**, unit-tested; the estimation bench hasn't passed it yet. Tuning
`process_noise_accel` alone couldn't fix it: the lag is at the path ends,
and a filter fed only panel positions can't tell the centre accelerating
from the panel spinning over less than a spin period. A slow Singer
acceleration tracks the 6 m/s^2 braking without that confusion.

**Ready to run:** `process_noise_accel:=` sweeps the tracker on the estimation bench; the
velocity error is in `estimation.jsonl` per case and per state.

Tune `process_noise_accel` against the estimation bench's velocity-error trace, path ends
included.

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
  `odom`, including our velocity.
- **Aim output: in the world on our side.** Since 2026-09-27 `CVTarget`
  carries an `odom` point (same bytes), and `sim`'s readers hold it at
  their own pose. The firmware and the shared frame are W.3's open issues
  below.
- **Our pose: incomplete.** `RobotPose` has no chassis yaw (`head_yaw` is the
  gimbal's), the stack assumes a fixed heading (`sim/AGENTS.md`: the
  chassis already picks up ~1 deg in sim), and the stamp is Jetson arrival.

What it needs, in order:

| Step | Package | Change |
|---|---|---|
| W.1 | `ros2_dji_serial_bridge`, firmware | `RobotPose` gains chassis yaw and yaw rate, and a capture stamp (Stamps table below: first-byte time less wire time, later an MCB clock). `odom->root` carries the yaw |
| W.2 | `thornbots_pkg` | Every TF lookup at the time the data was true: the camera at capture (Part 2 does this), our pose at the fire horizon in Part 1, not `Time()` |
| W.3 | `ros2_dji_serial_bridge`, firmware | `CVTarget` becomes a world-frame aim: the intercept point in `odom` (or gimbal yaw/pitch relative to the world) plus its stamp. The MCB holds it with its IMU and odometry while the chassis moves and turns, the usual RoboMaster split. Needs the firmware's `CVData` to follow (`thornbots_pkg/AGENTS.md`) |
| W.4 | `sim` | The aiming bench: our `root` turns as well as translates (`shooter_speed` only slides it along y today), and the shooter carries the aim in `odom` the way W.3's MCB would. The estimation bench: our gz chassis turns while tracking |
| W.5 | `sim`, `thornbots_pkg` | Floors and limits for the new cells, like the aiming bench's `FLOORS` and 2.0 |

W.3's open issues (our side switched 2026-09-27):

1. **Which `odom` the MCB holds in.** The docs call it POSE_MSG's frame, but
   the Jetson's `odom->root` is `/localization/odom` (EKF-fused with rf2o
   when `use_ekf`), not the MCB's raw odometry, and `mcb_relay`'s
   RELOCALIZE resets the MCB's origin when the two drift apart. An aim point
   in flight across a relocalize lands where the old origin was. Pick one
   frame both sides share, or send the aim relative to a pose the MCB also
   has. Without W.1's chassis yaw the rotations aren't shared either.
2. **Firmware: `CVData`** treats `x/y/z` as `odom` and re-aims as the
   chassis moves and turns. The layout doesn't change, so a mismatch fails
   no length check (`ros2_dji_serial_bridge/README.md`).

W.1 and W.3 change the wire protocol and the MCB firmware, which live
outside this workspace; agree them with the firmware side first. W.2 and
W.4 can start now.

## Stamps

Workspace rule (`CLAUDE.md` § Timestamps): every internal message is stamped as
well as its node can. Audit of 2026-09-24. The CV chain mostly complies:
`roi_depth_node` and `target_selector` carry the detection stamp through,
`target_tracker` predicts to its publish time and stamps that,
`cv_target_emulator` stamps sample time, `CVTarget` stamps decision time,
`lidar_self_filter` and `pose_translator` pass the input's stamp on. The gaps:

| Where | Today | Best the node can do | When |
|---|---|---|---|
| `dji_serial_bridge` → `RobotPose`, `RefSysStatus` | `now()` after the frame is parsed | Stamp when the frame's first byte is read, minus its wire time at the baud rate. Later, an MCB millisecond clock on the wire, the mirror of `CV_MSG`'s `stamp_ms`, mapped to ROS time by offset | Before any field test of Part 1 while we move: `odom->root` TF and our velocity both come from it. The MCB half is firmware work outside this workspace |
| Camera → `Detection2DArray` | Image stamp carried through the YOLO chain, not verified end to end; its relation to capture unmeasured | Verify the stamp survives the chain, then measure capture latency | Estimation, on hardware |
| `mcb_relay` → relocalize | Bare `geometry_msgs/Point` | `PointStamped` with the stamp of the localization pose it came from; the bridge's subscriber follows | Own change, not CV-blocking |
| `dji_serial_bridge` `~/nav_goal` | Bare `geometry_msgs/Point` | `PointStamped`, stamped when the goal was chosen | Same change as relocalize |

`/cmd_vel` stays a bare `Twist`: gz's diff-drive plugin and the harnesses expect
it, which is the standard-interface exception in the rule.

## Commits

Each step is its own commit per package, pushed in dependency order
(`ros2_dji_serial_bridge`, `thornbots_pkg`, `sim`), then one bump with the estimation bench
before/after numbers in the message. Update this file and ROADMAP.md in that
bump. `thornbots_pkg` is shadowed in `/workspaces/ros2_ws`: rebuild it in
`isaac_ros-dev` and check `ros2 pkg prefix` before any run.

Sim detection noise is 0.005 m and the aiming bench has no estimation noise at all, so the aiming bench's
floors describe the aim solve alone. Neither bench predicts field hit rates;
they rank changes.
