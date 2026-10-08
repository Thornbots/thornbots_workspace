# Plan: E2E tests independent of machine speed

**Status: unfinished plan, not current behavior (2026-10-08).** The done
bar below is not met. The lockstep gate and coordinator are WIP on sim
branch `t3code/lockstep-wip`, not on nightly, and haven't been rebuilt or
rerun on nightly's stages. E1-E4 below predate the rename to `mcb_parked`,
`mcb_drive` and `mcb_match` ([`E2E_PLAN.md`](E2E_PLAN.md)); E1 is gone and
every stage runs the MCB emulator, so step 8 is done.

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
The cell was `stage:=e2 speeds:=0 paths:=lateral duration:=10`, with the
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

The hit path crosses wall-time boundaries, so the order and sim time of its
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
   (`point_to_cv_target.py:333`). `_gun_pose` always uses the latest.
6. **Bring-up runs on wall timers.** `ROBOT_DELAY_S` and the bridge's 2 s
   `TimerAction` move sim time under the robot's start, so the first shot
   falls anywhere from 22 to 26 s.
7. **The harness blames localization.** `segment_diagnostics` blames
   `map->root` error before checking aim and barrel (`e2e_harness.py:726`).
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

Add `sim/src/lockstep_gate.cpp`. `e2e.launch.py` loads it into the world
when `lockstep:=true`, which is the default for e2e.

- In `PreUpdate`, it stops at the next hold point and blocks until a release
  arrives. Releases come on a gz-transport topic,
  `/sim/lockstep/release` (`gz.msgs.Time`, released-until).
- Make sure the `/clock` ROS sees while held equals the hold time. Check
  this with a test; don't assume it.
- A wait longer than `max_wait_s` of wall time (2 s) is a **lockstep
  timeout**. Log it and count it. The harness fails a run with any.
- Don't use the world-control `multi_step` service: each call costs a full
  service round trip.

### 2. The MCB firmware inside the physics step

Add a C++ gz system plugin, `sim/src/mcb_firmware_system.cpp`, that owns the
hosted firmware process. It replaces `mcb_emulator_node` in e2e:

- **One firmware cycle per 1 ms physics step,** in `PreUpdate`. Readings
  come from the ECM at that step: chassis pose and twist, plus
  `headlink`/`headpitch` position and velocity. Use the mapping in
  `mcb_firmware.Firmware.gz_readings` and `GzHardware`.
- **Gimbal commands apply in the same step.** Run the head PD inside the
  plugin, with the gains `JointPositionController` has now
  (`sentry_v2.urdf.xacro`: p 75, d 2.1 yaw, d 1.2 pitch, +-50 N m), as
  joint force commands. Drop those two controllers from the model when the
  plugin is loaded. Chassis drive goes straight to the velocity command
  that `VelocityControl` sets now.
- **Pipe protocol:** reimplement the `INPUT`/`OUTPUT` structs and the `MCB1`
  handshake from `sim/mcb_firmware.py`. Keep the Python `Firmware` class
  only where `test/mcb` and `mcb.launch.py` still need it, or port them.
  Don't keep two stepping paths for e2e.
- **Shots:** publish each shot stamped with its firmware cycle's sim time,
  on the topic the scorer reads now (`/mcb_emulator/shot`).
- **Referee state:** today these are ROS parameters on `mcb_emulator`. Move
  them to a gz topic, or to a thin ROS node that forwards them. The scorer's
  `_sync_referee` sets them.
- **Physics step:** keep it at 1 ms (`sim/AGENTS.md`: 2-4 ms sent the head
  PID unstable).

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

Add `sim/src/lockstep_coordinator.cpp`, in C++. It generalizes
`sim_clock.py`'s `pace_topics` into a schedule of hold points, each waiting
on acks:

| Chain started at T | Hold until |
|---|---|
| POSE frame (plugin announces its cycle) | `/dji_serial_bridge/pose` and `/odom` stamped k |
| EKF tick (30 Hz) | `/localization/odom`, and `odom->root` on `/tf`, at that tick |
| `/scan` (10 Hz) | rf2o's output stamped T |
| `detector_standin` tick (60 Hz) | `/cv/tracker/measurement` echoes T, as on the estimation bench |
| `point_to_cv_target` tick (40 Hz) | its `tick_pub` header at T, then the plugin reports any CV_TARGET bytes read |
| `match_driver` (100 Hz), scorer fire tick (10 Hz) | their outputs for T |
| AMCL | pace only, up to a slack. It is not on the hit path |

- Nodes whose timers decide something (`point_to_cv_target`, `match_driver`,
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
- The first `map->odom->root->camera` chain is in TF.

`ROBOT_DELAY_S` and the 2 s bridge timer then can't move sim time. Use event
handlers instead (the pty exists, then start the bridge). Start each cell on
a fixed sim-time boundary, as `case_align_s` does on the estimation bench.

### 6. The other non-deterministic inputs

- **`point_to_cv_target`:** add `allow_latest_tf` (default true for the
  robot, false in e2e). Count fallbacks, and have the harness assert 0. This
  also applies to `_gun_pose`, which feeds the patrol and hit-turn. The
  workspace stamping rule calls for this; flag the hardware default in its
  `README.md`.
- **Seeds:** draw `detector_standin` noise (when enabled), ghost aim noise
  and ghost fire timing per (seed, robot, frame or shot index), not from one
  stream, as `bench_world` does.
- **Message loss:** under lockstep a dropped message shows up as a timeout,
  not a silent miss. Keep it that way.

### 7. Harness and diagnosis

- **Diagnosis order** in `segment_diagnostics`:
  1. no shots
  2. `aim_off_panel_m` (tracker / `point_to_cv_target`)
  3. head TF error (stamps)
  4. `barrel_off_aim_deg` (MCB / gimbal)
  5. otherwise none

  `map->root` error is logged, never a diagnosis.
- **New metric, `odom_disagreement_m`:** at each shot, the MCB's POSE
  position against TF `odom->root` at the same stamp. That agreement is what
  a hit depends on.
- **Run comparison:** add `tools/compare_runs.py <log_dir_a> <log_dir_b>`.
  It diffs `shots.jsonl`, `states.jsonl` and `route.jsonl` record by record
  and prints the first divergence.

### 8. The MCB emulator for every stage

E2 already runs E1's cells through the MCB. Remove E1's
`cv_head_aim` + `pose_emulator` + `team_stub` path from `e2e.launch.py` and
`e2e_harness.py`, and make the parked-robot stage the MCB stage. Update
`E2E_PLAN.md`'s Stages and the `sim` docs to match.

Keep `pose_emulator` and `cv_head_aim` themselves. The drift suite and the
benches still use them (`sim/AGENTS.md`).

## Order and done-when

Each step is its own commit and gitlink bump, tested before the next:

1. Fix the diagnosis order and add the metrics and `compare_runs.py`
   (step 7). It's cheap, and it makes every later run readable.
2. Add `LockstepGate` and the coordinator, with the current Python MCB
   node's 5 ms batch as a hold point and acks on its output. This proves
   the mechanism.
3. Move the MCB into the physics step and model the UART in sim time
   (steps 2 and 3). Remove the Python stepping path from e2e.
4. Bring-up without wall time, `allow_latest_tf`, and the seeds (steps 5
   and 6).
5. E1 on the MCB (step 8).

Done when, for E2 stationary-lateral first, then all E2 cells, E3 and E4:

- On one machine, three unthrottled runs, one at `real_time_factor:=1` and
  one with gz pinned to two cores (`taskset -c 0,1`) give identical
  `shots.jsonl`, compared with `compare_runs.py`.
- Mac and Archlinux give the same hit sequence. Any per-shot difference is
  traced to gz physics floating point and written down.
- No run has a lockstep timeout or a latest-TF fallback.
- Each suite's timing table shows its RTF and which chain held it longest.
  Nothing in the scored loop sleeps on wall time.

Only then take three runs per cell for `FLOORS` (`E2E_PLAN.md` Scoring).

## Running it

- **Mac mini (`blaises-mini`, container `isaac_ros_jazzy_container`,
  workspace `~/ros2_ws`):** the user allowed runs there when it's idle,
  installing sim and starting the container if missing (2026-10-08).
  Check for a live session first.
- **This laptop:** ask before any sim run (`sim/AGENTS.md`).
- **Firmware:** rebuild it after edits with `sim/tools/build_mcb_firmware.sh`.
