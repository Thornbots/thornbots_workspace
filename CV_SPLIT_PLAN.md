# Plan: split CV at `TargetState`

ROADMAP.md tracks G and B and the Estimation todos. Part 1 (`point_to_cv_target`)
aims and fires from a `TargetState`. Part 2 (`target_selector` +
`target_tracker`) builds that `TargetState` from detections. Updated
2026-09-28: Aiming is done, Estimation is down to todos, and hitting while
we move is the long work left.

## Where this stands

- Aiming is done on the aiming bench: `shot_hit_harness.py`'s `FLOORS`
  holds 40 per-cell floors, chase mode is the default, and Part 1 reads only
  `TargetState` and `RobotPose`.
- Part 2's `ArmorEKF` state is `[pos, vel, acc, yaw, w, r, dz]`, with Singer
  acceleration, per-pair z and a still hypothesis (`thornbots_pkg/README.md`).
  `target_tracker` stamps each `TargetState` with its publish time and
  predicts to it; `camera_latency_s` backs capture time out of the
  detection stamp. Part 1 does no latency correction.
- The estimation bench (`sim/launch/estimation.launch.py`, `bench_world`,
  one C++ lockstep loop, no gz) runs ten cells in ~75 s. `LIMITS`
  (`sim/test/cv/estimation_limits_data.py`, 2026-09-27) covers all 60
  cells at 2x the worst of three to six runs, floored at 0.02.
- Results: stationary under 2 cm facing-panel p95; moving 0.08-0.19 m.
  Camera latency 0.03 s and our chassis at 1 m/s match the default. Radial
  motion doubles along-ray error at 2-4 m/s (0.18-0.25 m); blackout (0.3 s
  of every 2 s) is 2-3x worse, worst on staggered 0.5-1 m/s (0.28-0.30 m).
- About a quarter of runs trip one limit on a spin rate misread by
  0.6-2 rad/s or a wandering radius. In the bad 4 m/s runs radius error sits
  at 5-12 cm for 10-20 s against ~2 cm, and facing-panel error follows it.
- `target_tracker` is the slowest node under test: `ArmorTracker.step`'s
  numpy is 46% of its main thread, its TF listener 27%.

## Todos

- Per-pair z: staggered cells' `z_offset` and panel error should match flat
  cells'.
- Velocity lag: sweep `process_noise_accel:=` on the estimation bench
  against the per-case velocity error in `estimation.jsonl`.
- Confirm a cell scores the same run alone as in sequence.
- On hardware: measure the RealSense stamp against capture (metadata
  timestamps, or a blinking LED), then set `camera_latency_s`.
- On hardware: measure the gimbal's ~7 deg chase jump settling and set
  `chase_settle_s` to it.
- Aiming bench: radial and diagonal paths with a moving shooter haven't run.

## Estimation accuracy (ROADMAP.md track G)

The user's call (2026-09-28): all three of these get fixed. Each is its own
commit, scored on the estimation bench over three runs.

| Step | Problem | Where to start |
|---|---|---|
| G.1 | In about one 4 m/s run in five, radius error sits at 5-12 cm for 10-20 s (normally ~2 cm) and facing-panel error follows. The spin rate is sometimes misread by 0.6-2 rad/s | Hold the radius tighter: `process_noise_radius` (0.02 m/sqrt(s)) down, and a prior at the armor radius. Log innovations around each spin misread to find what triggers it |
| G.2 | Radial motion doubles along-ray error at 2-4 m/s (0.18-0.25 m against 0.09-0.11). Blackouts (0.3 s of every 2 s) run 2-3x worse, worst on staggered 0.5-1 m/s (0.28-0.30 m against 0.09) | Radial: `ray_covariance` already splits depth from lateral noise; tune `meas_noise_base_m` / `meas_noise_range_coeff` against the bench's depth noise. Blackout: check what the `dz` pair handoff does across a gap |
| G.3 | `valid` goes true after 2 updates (`target_tracker.py`), but a fresh track on a spinner takes 0.3-3 s to settle, up to 0.4 m off in the first second. Spin-rate variance doesn't separate settled from not | Gate `valid` on settling, not a count: try a minimum track age, or the facing panel's predicted-vs-measured residual. Check the cost on the aiming bench |

Done when a fresh run of every cell passes `LIMITS` tightened to the new
worst runs, with radial and blackout cells within 1.5x of the default and
no fresh track `valid` before its facing-panel error settles under 5 cm.

## Open for the user

- A C++ core for `target_tracker`, after ROADMAP.md T10 measures its cost.

Flat 4 m/s misses cluster where the target's acceleration switches at path
ends, which nothing predicts. Known, no plan.

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
| W.5 | `sim`, `thornbots_pkg` | Floors and limits for the new cells, like the aiming bench's `FLOORS` and the estimation bench's `LIMITS` |

W.3's open issues (our side switched 2026-09-27):

1. **Which `odom` the MCB holds in.** The docs call it POSE_MSG's frame, but
   the Jetson's `odom->root` is `/localization/odom` (EKF-fused with rf2o
   when `use_rf2o`), not the MCB's raw odometry, and `mcb_relay`'s
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
