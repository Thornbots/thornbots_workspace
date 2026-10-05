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
  one C++ lockstep loop, no gz) runs 12 cells in ~30 s. `LIMITS`
  (`sim/test/cv/estimation_limits_data.py`, 2026-09-27) covers all 60
  cells at 2x the worst of three to six runs, floored at 0.02.
- Results: stationary under 2 cm facing-panel p95; moving 0.08-0.19 m.
  Camera latency 0.03 s and our chassis at 1 m/s match the default. Radial
  motion doubles along-ray error at 2-4 m/s (0.18-0.25 m); blackout (0.3 s
  of every 2 s) is 2-3x worse, worst on staggered 0.5-1 m/s (0.28-0.30 m).
- About a quarter of runs trip one limit on a spin rate misread by
  0.6-2 rad/s or a wandering radius. In the bad 4 m/s runs radius error sits
  at 5-12 cm for 10-20 s against ~2 cm, and facing-panel error follows it.
- `target_tracker` is C++ since 2026-09-28: 33% of a core on the Mac's
  bench at ~27x, down from 110% at ~14x in Python.

## Todos

- A still target seen at an angle (ROADMAP.md T15). `stationary45` holds
  it at 45 deg (sim f47c84a): two panels in view, so no facing
  pseudo-measurement, and two panel positions don't fix centre, yaw and
  both radii. Yaw p95 0.12 rad, staggered centre 0.064-0.071 m. Needs a
  tracker fix, then `LIMITS` for `stationary45`.
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
| G.2 | Radial motion doubles along-ray error at 2-4 m/s (0.18-0.25 m against 0.09-0.11). Blackouts (0.3 s of every 2 s) run 2-3x worse, worst on staggered 0.5-1 m/s (0.28-0.30 m against 0.09) | Radial: `ray_covariance` already splits depth from lateral noise; tune `meas_noise_base_m` / `meas_noise_range_coeff` against the bench's depth noise. Blackout: check what the `dz` pair handoff does across a gap. Staggered blackout cells at 1-4 m/s read `z_offset` p95 0.012-0.062 m (median of runs) against flat's 0.002 (stagger 0.095 m), and 1.4-1.6x flat's panel error at 2-4 m/s: the pair parity likely comes back wrong. Without blackout, staggered matches flat (panel error within 0.9-1.2x, `z_offset` under 4 mm) |
| G.3 | `valid` goes true after 2 updates (`target_tracker.cpp`), but a fresh track on a spinner takes 0.3-3 s to settle, up to 0.4 m off in the first second. Spin-rate variance doesn't separate settled from not | Gate `valid` on settling, not a count: try a minimum track age, or the facing panel's predicted-vs-measured residual. Check the cost on the aiming bench |

Done when a fresh run of every cell passes `LIMITS` tightened to the new
worst runs, with radial and blackout cells within 1.5x of the default and
no fresh track `valid` before its facing-panel error settles under 5 cm.

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
- **Our pose: chassis yaw in, not on the wire.** `RobotPose` has
  `chassis_yaw` and `chassis_yaw_rate`, driving a `chassis_yaw` joint under a
  heading-fixed `root` (`thornbots_pkg/README.md`); the head hangs off `root`
  at the MCB's world `head_yaw`. Sim sends it; the wire doesn't yet
  (`UART_PROTOCOL.md` "Proposed: POSE chassis yaw"). The stamp is when
  the MCB started sending, less unmeasured USB latency.

What it needs, in order:

| Step | Package | Change |
|---|---|---|
| W.1 | `ros2_dji_serial_bridge`, firmware | `RobotPose` gains chassis yaw and yaw rate (ROS side done 2026-09-29, wire proposed), and a capture stamp (Stamps table below: first-byte time less wire time, later an MCB clock). The yaw is a joint under a heading-fixed `root`, not in `odom->root` |
| W.2 | `thornbots_pkg` | Every TF lookup at the time the data was true: the camera at capture (Part 2 does this), our pose at the state's stamp in Part 1, carried to the fire horizon by our velocity (done 2026-09-29) |
| W.3 | `ros2_dji_serial_bridge`, firmware | `CVTarget` becomes a world-frame aim: the intercept point in `odom` (or gimbal yaw/pitch relative to the world) plus its stamp. The MCB holds it with its IMU and odometry while the chassis moves and turns, the usual RoboMaster split. Needs the firmware's `CvTarget` to follow (`thornbots_pkg/AGENTS.md`) |
| W.4 | `sim` | Done 2026-09-29 on the estimation bench: `chassis_spin:=9` spins our chassis under a world-held head, with optional bearing drag. Every cell scores like its spin-0 twin. The aiming bench gets no spin: under a heading-fixed `root` its perfect point gimbal makes a spin a no-op |
| W.5 | `sim` | Done 2026-09-29: `LIMITS` has the 12 `-chassis9` cells. Radial or diagonal with a moving shooter still has no aiming-bench floor (`sim/AGENTS.md`) |

W.3's open issues (our side switched 2026-09-27):

1. **Which `odom` the MCB holds in: ours, by RELOCALIZE** (read
   2026-10-04, not measured). `mcb_relay` relocalizes the MCB onto
   `/localization/odom`, the `odom->root` the aim point is built in, so
   the gap is the MCB's drift since the last one: under ~6 cm while
   localization is confident (5 cm, or 3 sigma with sigma <= 2 cm). A
   relocalize during an aim moves the MCB toward the point's frame, so
   it helps; the cost is the mailbox (a CV_TARGET in the same 1 ms is
   lost). Chassis yaw isn't needed: `root` is heading-fixed and the
   gimbal yaw is the IMU's world yaw on both sides.
2. **Firmware: POSE's axes.** `0885a69` aims at `x/y/z` less its own
   odometry, which is x right, y forward. Worked around on the Jetson
   since 2026-10-04 (`thornbots_pkg` `mcb_x_right`, README.md "MCB
   axes"), not on the robot. rep-105 (here and in MCBV3, `thornbots_pkg`,
   the bridge, `sentry_localization`, `sim`) retired it: one field frame
   everywhere, REP-105, (0, 0) at the field centre, x
   toward blue's base, the MCB starting at its team's start. The layout
   doesn't change, so no length check catches a mismatch.

W.1's wire half and W.3 change the wire protocol and the MCB firmware,
which live outside this workspace; agree them with the firmware side
first. Everything on our side is done.

## Stamps

Workspace rule (`CLAUDE.md` § Timestamps): every internal message is stamped as
well as its node can. Audit of 2026-09-24. The CV chain mostly complies:
`roi_depth_node` and `target_selector` carry the detection stamp through,
`target_tracker` predicts to its publish time and stamps that,
`cv_target_emulator` stamps sample time, `CVTarget` stamps decision time,
`lidar_self_filter` and `pose_translator` pass the input's stamp on. The gaps:

| Where | Today | Best the node can do | When |
|---|---|---|---|
| `dji_serial_bridge` → `RobotPose`, `RefSysStatus` | Since 2026-09-29, the last byte's read time less the frame's wire time at the baud; USB-serial latency not taken off | An MCB millisecond clock on the wire (`CV_TARGET` dropped its `stamp_ms` 2026-10-03), mapped to ROS time by offset; until then, measure the USB latency on the robot | Before any field test of Part 1 while we move: `odom->root` TF and our velocity both come from it. The MCB half is firmware work outside this workspace |
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
