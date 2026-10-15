# Plan: E2E tests independent of machine speed

**Status: partial implementation (2026-10-15).** The done bar below is not
met. The pinned sim implements the [native MCB-batch gate and coordinator](sim/README.md#mcb-emulator),
with zero-phase scheduling, timeout rejection and transport/physics tests.
Firmware runs inside each 1 ms physics step with CAN motor feedback and force
outputs ([motor plant](sim/README.md#mcb-emulator)). UART in sim time, other consumption chains,
and deterministic bring-up remain open. An opt-in sim-time UART fixture has
byte-deadline and bridge-stamp tests; its first whole-stack attempt was
[rejected for late outgoing delivery](sim/docs/track-a-uart-2026-10-15.md).
E1-E4 below predate the rename to `mcb_parked`,
`mcb_drive` and `mcb_match` ([`E2E_PLAN.md`](E2E_PLAN.md)); E1 is gone and
every stage runs the MCB emulator, so step 8 is done.

The optional [Type C backend](sim/README.md#type-c-board-execution-with-renode)
executes the normal board ELF and its drivers during each virtual step. This
does not establish cycle-accurate STM32 deadlines or finish the remaining UART
serialization and consumption-chain gates.

Asked by the user, 2026-10-08: fix the E1-E4 tests so a result doesn't
depend on how fast the machine runs, and make them run as fast as the
machine allows. This plan covers that, plus two related asks from the same
day:

- E1 runs on the MCB emulator, like the other stages.
- Localization error never costs a hit: the robot only needs its parts to
  agree on where it is.

`E2E_PLAN.md` still owns the stages and the scoring.

## Why results don't repeat

Measured on the Mac mini, 2026-10-08, workspace `8588660`, sim `c8f39a2`.
The cell was `stage:=mcb_parked speeds:=0 paths:=lateral duration:=10`, with the
opponent parked:

| Run | Hits | Barrel off aim, p50/max | Head TF error, p50/max | Scored RTF |
|---|---|---|---|---|
| unthrottled A | 12/20 | 1.99/3.81 deg | 0.15/1.41 deg | 0.87 |
| unthrottled B | 16/20 | 1.67/3.20 deg | 0.13/1.84 deg | 0.96 |
| `real_time_factor:=1` | 8/20 | 1.84/8.09 deg | 0.83/5.76 deg | 0.77 |

The 10-07 Mac run of the same cell hit 20/20. The aim itself was good in
every run, 4-7 mm (p50) off the panel. The barrel missing that aim is what
varies. The full stack runs below real time here even unthrottled, so this
isn't only a fast-machine problem. Logs are in `/tmp/lockstep_baseline/` in
the mini's container.

That revision's hit path crossed wall-time boundaries, so the order and sim time of its
events depend on scheduling:

1. **The firmware is stepped in batches with stale readings.**
   `mcb_emulator_node._tick` runs on a 5 ms sim timer. It hands the firmware
   1-100 cycles, all with the latest `/sim/raw_odom` and joint readings, and
   publishes one gimbal command per batch.
2. **Gimbal commands take two async hops.** They go out on ROS
   `/head_pan_cmd`, then through `ros_gz_bridge`, then gz-transport, to
   `JointPositionController`. The loop's lag in sim time is a wall latency
   times the RTF.
3. **UART stamps are arrival times.** `dji_serial_bridge` stamps a frame
   with the sim time it reads it, minus 34 bytes of 115200-baud wire time
   (`frame_stamp`). The pty has no wire time, and the frame's data is up to
   a batch older than the stamp. That stamp becomes `odom->root` and the head
   TF.
4. **CV_TARGET reaches the firmware whenever the pty delivers it,** and
   `delay_ms` counts from there.
5. **The stack falls back to latest TF.** `point_to_cv_target` uses the
   latest `odom<-root` when the stamped one isn't in yet
   (`point_to_cv_target_node.cpp`, the `tf2::TimePointZero` lookup). `_gun_pose` always uses the latest.
6. **Bring-up runs on wall timers.** `ROBOT_DELAY_S` and the bridge's 2 s
   `TimerAction` move sim time under the robot's start, so the first shot
   falls anywhere from 22 to 26 s.
7. **The harness blamed localization.** `segment_diagnostics` blamed
   `map->root` error before checking aim and barrel. It now follows the order
   in step 7 (`sim/test/e2e/e2e_harness.cpp`).
   Every hop that aims uses `odom`, and `mcb_relay` relocalizes the MCB from
   the EKF's `odom` estimate, not AMCL's. So `map` error can't cost a hit,
   and that diagnosis hid the gimbal and stamp losses above.

## Approach: lockstep, as the estimation bench does

`bench_world` repeats to 1.03x because nothing advances `/clock` until the
nodes under test have consumed the last step (`sim/README.md`, estimation
bench). The same works for gz: hold physics at each scheduled event until
that event's chain has finished, then release. A slow machine waits longer
in wall time but computes the same thing. A fast one never waits on a sleep.

### 1. LockstepGate: a gz system plugin that holds physics

Done: `sim/src/lockstep_gate.cpp`, loaded into the world when
`lockstep:=true`, the default for e2e. It holds at 5 ms MCB batch deadlines
only; the remaining hold points are in step 4. Its contract:

- It stops at the next hold point and blocks until a release arrives.
  Releases come on a gz-transport topic,
  `/sim/lockstep/release` (`gz.msgs.Time`, released-until). Move the hold
  from `PostUpdate` to `PreUpdate` when the firmware runs in the step.
- Make sure the `/clock` ROS sees while held equals the hold time. Check
  this with a test; don't assume it.
- A wait longer than `max_wait_s` of wall time (2 s) is a **lockstep
  timeout**. Log it and count it. The harness fails a run with any.
- Don't use the world-control `multi_step` service: each call costs a full
  service round trip.

### 2. The MCB firmware inside the physics step

Implemented with CAN feedback and motor forces; usage and limits live in
[sim's MCB emulator](sim/README.md#mcb-emulator). The following is the original
proposal; its setpoint PD and chassis-velocity shortcut were replaced by the
motor plant so firmware motor control is exercised.

Add a C++ gz system plugin, `sim/src/mcb_firmware_system.cpp`, that owns the
hosted firmware process. It replaces `mcb_emulator_node` in e2e:

- **One firmware cycle per 1 ms physics step,** in `PreUpdate`. Readings
  come from the ECM at that step: chassis pose and twist, plus
  `headlink`/`headpitch` position and velocity. Use the mapping in
  `Firmware::gz_readings` and `GzHardware` (`mcb_firmware.hpp`).
- **Gimbal commands apply in the same step.** Run the head PD inside the
  plugin, with the gains `JointPositionController` has now
  (`sentry_v2.urdf.xacro`: p 75, d 2.1 yaw, d 1.2 pitch, +-50 N m), as
  joint force commands. Drop those two controllers from the model when the
  plugin is loaded. Chassis drive goes straight to the velocity command
  that `VelocityControl` sets now.
- **Pipe protocol:** reuse the `Input`/`Output` structs and the `MCB1`
  handshake from `sim/include/sim/mcb_firmware.hpp` (the Python port is
  removed). Don't keep two stepping paths for e2e.
- **Shots:** publish each shot stamped with its firmware cycle's sim time,
  on the topic the scorer reads now (`/mcb_emulator/shot`).
- **Referee state:** today these are ROS parameters on `mcb_emulator`. Move
  them to a gz topic, or to a thin ROS node that forwards them. The scorer's
  `Scorer::sync_referee()` (`sim/test/e2e/e2e_harness.cpp`) sets them.
- **Physics step:** keep it at 1 ms (2-4 ms sent the head PID unstable;
  [sim rules](sim/AGENTS.md#standing-rules)).

### 3. UART in sim time

The firmware's UART fd becomes a socketpair the plugin owns. The plugin
relays bytes to and from the pty master on a modeled wire:

- **MCB to Jetson:** bytes the firmware writes in cycle k reach the pty at
  k plus their wire time (bytes x 10 / baud), a hold point. The gate holds
  there until the bridge has published the frame. The bridge's stamp, read
  time less wire time, is then exactly k.
- **Jetson to MCB:** bytes the plugin reads from the pty while held at t
  enter the firmware's fd at cycle t plus their wire time, plus
  `mcb_read_delay_ms` (default 0).
- **Baud:** set `dji_serial_bridge`'s `baudrate` explicitly in
  `e2e.launch.py` to the robot's, so both sides use one wire model.

### 4. A coordinator that decides when to release

`sim/src/lockstep_coordinator.cpp` exists and schedules only the MCB batch
ack. Extend it, generalizing `sim_clock.cpp`'s `pace_topics`, into a schedule
of hold points, each waiting on acks:

| Chain started at T | Hold until |
|---|---|
| POSE frame (plugin announces its cycle) | `/dji_serial_bridge/pose` and `/odom` stamped k |
| EKF tick (30 Hz) | `/localization/odom`, and `nav_odom->odom` on `/tf`, at that tick |
| `/scan` (10 Hz) | rf2o's output stamped T |
| `detector_standin` tick (60 Hz) | `/cv/tracker/measurement` echoes T, as on the estimation bench |
| `point_to_cv_target` tick (40 Hz) | its `tick_pub` header at T, then the plugin reports any CV_TARGET bytes read |
| `match_environment` (100 Hz), scorer fire tick (10 Hz) | their outputs for T |
| AMCL | pace only, up to a slack. It is not on the hit path |

- Nodes whose timers decide something (`point_to_cv_target`, `match_environment`,
  the ghosts) get a `clock_ack_topic`, like `target_tracker`. That way a
  tick is never skipped or doubled when `/clock` moves.
- Hold-point times are known ahead: firmware cycles and fixed rates. Merge
  coincident ones.
- Log per run: holds per sim second, wall time held per chain (which hop
  sets the speed), and timeout count.

### 5. Bring-up without wall time

gz starts held at t = 0. The coordinator releases only once all of these are
true:

- Every e2e node is up.
- The localization lifecycle nodes are active.
- The first `map->nav_odom->odom->root->camera` chain is in TF.

`ROBOT_DELAY_S` and the 2 s bridge timer then can't move sim time. Use event
handlers instead (the pty exists, then start the bridge). Start each cell on
a fixed sim-time boundary, as `case_align_s` does on the estimation bench.

### 6. The other non-deterministic inputs

- **`point_to_cv_target`:** implemented `allow_latest_tf` (default true for the
  robot, false in E2E), a cumulative fallback counter and a present/zero
  assertion in the harness. Aim uses the target-state stamp, patrol uses
  the carried raw POSE stamp, and hit turns use the REF_SYS stamp. Zero stamps
  cannot silently request latest TF. The [aimer](thornbots_pkg/README.md#point_to_cv_target)
  owns the robot default. This guard does not establish deterministic delivery.
- **Seeds:** draw `detector_standin` noise (when enabled), ghost aim noise
  and ghost fire timing per (seed, robot, frame or shot index), not from one
  stream, as `bench_world` does.
- **Message loss:** under lockstep a dropped message shows up as a timeout,
  not a silent miss. Keep it that way.

### 7. Harness and diagnosis

- **Diagnosis order** in `segment_diagnostics` (done):
  1. no shots
  2. `aim_off_panel_m` (tracker / `point_to_cv_target`)
  3. head TF error (stamps)
  4. `barrel_off_aim_deg` (MCB / gimbal)
  5. otherwise none

  `map->root` error is logged, never a diagnosis.
- **New metric, `odom_disagreement_m`:** done in the harness (the MCB's POSE
  position against TF `odom->root` at the stamp).
- **Run comparison:** done, `ros2 run sim compare_runs LOG_DIR_A LOG_DIR_B`
  (`sim/tools/compare_runs.cpp`) prints the first divergence per jsonl log.
  Missing/empty shot or state logs fail comparison. The harness also records
  capture/arrival stamps and valid/invalid tracks in
  [`inputs.jsonl`](sim/README.md#mcb-emulator), before any tracker tuning.

### 8. The MCB emulator for every stage

Done: every stage runs the MCB emulator and E1's `cv_head_aim` +
`pose_emulator` + `team_stub` path is gone from `e2e.launch.py` and
`sim/test/e2e/e2e_harness.cpp`; `E2E_PLAN.md`'s Stages match.

Keep `pose_emulator` and `cv_head_aim` themselves. The drift suite and the
benches still use them (`sim/AGENTS.md`).

## Order and done-when

Each step is its own commit and gitlink bump, tested before the next:

1. Finish UART in sim time (step 3). The native MCB already runs in each
   physics step; e2e's ROS timer stepping path is removed (step 2).
2. Bring-up without wall time, `allow_latest_tf`, and the seeds (steps 5
   and 6).

Done when, for E2 stationary-lateral first, then all E2 cells, E3 and E4:

- On one machine, three unthrottled runs, one at `real_time_factor:=1` and
  one with gz pinned to two cores (`taskset -c 0,1`) give identical
  `shots.jsonl`, compared with `compare_runs`.
- Mac and Archlinux give the same hit sequence. Any per-shot difference is
  traced to gz physics floating point and written down.
- No run has a lockstep timeout or a latest-TF fallback.
- Each suite's timing table shows its RTF and which chain held it longest.
  Nothing in the scored loop sleeps on wall time.

Only then take three runs per cell for `FLOORS` (`E2E_PLAN.md` Scoring).

## Running it

- Container lifecycle, sim/bench approval and live-session checks follow
  [workspace rules](AGENTS.md#containers-and-runs).
- **Firmware:** rebuild it after edits with `sim/tools/build_mcb_firmware.sh`.
