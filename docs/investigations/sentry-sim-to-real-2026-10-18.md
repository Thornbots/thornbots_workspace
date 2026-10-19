# Sentry sim-to-real measurements, 2026-10-18

Artifacts are on the laptop `archlinux` (not in git): `~/workspaces/isaac_ros-jazzy/test-hold-ab-2026-10-18/` and
`~/sentry-deploy/2026-10-18/`. Numbers below are copied from those files.

## Parked hold (firmware)

Sim stage `mcb_parked`, hosted backend, lockstep. Limit: chassis displacement ≤ 0.03 m. Logs:
`test-hold-ab-2026-10-18/main-hold-412d102/{logs,logs-moving}/parking.jsonl` and `scores.jsonl`,
`main-only/logs/parking.jsonl`, with `launch*.log` beside them.
Firmware: [MCBV3#98](https://github.com/Thornbots/MCBV3/pull/98), sim: [sim#28](https://github.com/Thornbots/sim/pull/28).

| MCBV3 | Cells | Result | Max chassis displacement (m) | Stationary hits |
| --- | --- | --- | --- | --- |
| 412d102 (main's hold, nightly's peek/power gates) | 3 stationary | 3 passed | 0.000 / 0.024 / 0.015 (lateral / radial / diagonal) | 122/122 (40 + 41 + 41) |
| 412d102 | 9 moving (speeds 1/2/4 × 3 directions) | 9 passed | 0.0005–0.0011 | n/a |
| 0e421d8 (#98 head, main exactly) | 3 stationary | 0 passed, 3 failed | 0.070 / 0.070 / 0.067 | 120/120 (40 × 3) |

- 0e421d8 hits every shot but fails the limit: main's peek release boots centred manual into keyboard beyblade
  (fixture spin −12).
- Real robot (user report): main's hold spins in place for minutes without wandering. Raw `/odom` is exactly still after
  both flashes (controller off).

### Mac mini, 12 cells per firmware

Evidence: `~/sentry-deploy/2026-10-18/mini-sim/report.md` (`part-b-0e421d8/`, `part-b-f9895ab/`). Mini ran an unrelated
`sushi serve` load during the 0e421d8 run. ELF per `stack.log`. Spin: unwrapped gz-truth yaw, median per cell.

| MCBV3 | Pass | Max chassis displacement (m) | Chassis spin |
| --- | --- | --- | --- |
| 0e421d8 (main) | 5/12 | 0.016–0.073 (7 cells over 0.03) | −12.02 rad/s in every cell |
| f9895ab (`feat/drivetrain-power-and-peek-gates`) | 12/12 | 0.0004–0.0232 | 0.00 rad/s |

- Main's peek release reproduces the −12 rad/s spin on the mini; f9895ab does not spin.
- Laptop and mini displacements for 0e421d8 differ per direction (laptop 0.067–0.070 stationary; mini 0.069 / 0.050 /
  0.025 lateral / radial / diagonal), so the spin rate is constant while the displacement is not.

## Lidar scan format

Evidence: `~/sentry-deploy/2026-10-18/lidar-scan-format/` (files 00–30, `source_refs`), `~/sentry-deploy/2026-10-18/mini-sim/`
(`report.md`, `part-a/scan-summary.json`). Robot `ts-nano-sentry`, RPLIDAR Express mode, 60 s probes. Sim: Mac mini, 85 s.

| | Real default | Real `angle_compensate:=true` | Sim |
| --- | --- | --- | --- |
| `/scan_raw` beams | 340–359, 13 distinct counts | 720 fixed | 800 fixed |
| `/scan` after self filter | 340–359 | 720 | 800 |
| Angle increment | ~1.00–1.01° | 0.5007° | 0.4503° |
| Angle min / max (rad) | −3.1413…−3.0128 / 2.8733…3.1416 | −π / π | −3.14 / 3.14 |
| Range min / max (m) | 0.05 / 12.0 | 0.05 / 12.0 | 0.15 / 12.0 |
| Invalid returns | inf, 0.36–0.42 of beams | inf, 0.38–0.44 | none (inf fraction 0) |
| `scan_time` (s) | 0.084–0.096 | 0.085–0.097 | 0.0 |
| Rate (Hz) | 11.19 | 11.20 | 10.0 |
| Stamp age at receipt (s) | 0.086–0.100 | 0.086–0.100 | 0.037–0.108 |
| slam_toolbox `expected N` warnings | warning counter 174 → 181 in the probe window; per-run logs (`11_`) show up to 499 `expected` mismatches per run | counter 194 → 195 across the 60 s probe without restarting slam_toolbox | n/a (Karto expected is constant 800) |

Sim vs real mismatches: beam count, increment, angle range, range min, invalid-return convention (inf vs none),
`scan_time`, rate. Sim never triggers `expected N`, so the real warning cannot reproduce there.

### Fresh slam_toolbox with a fixed grid (robot, 2026-10-18 ~17:50–17:55, robot stationary)

Files `30_*` in the lidar-scan-format directory. `sllidar_node` was stopped and run by hand with the stack's parameters
plus `angle_compensate:=true`; slam_toolbox was restarted with its normal params (lifecycle configure/activate by hand).
The stack was restored afterwards with `systemctl restart thornbots.service`.

| | Baseline (normal stack, slam since 17:21) | Fixed grid, fresh slam_toolbox |
| --- | --- | --- |
| Window | 60 s | 120 s |
| `expected N` warnings | 87 → 91 (+4) | 0 in the fresh slam log (no warning lines of any kind) |
| `/scan` | 11.2 Hz, 340–359 beams | 11.21 Hz, 336 scans in 30 s, 720 beams every scan |
| `/map` messages | 13 (239×168) | 25 (239×171) |
| Graph vertices / `/pose` messages | 1 / 0 | 1 / 0 |

- Result: with the fixed grid slam_toolbox emits no `expected N` warnings and keeps publishing map updates.
- Not shown: acceptance of later scans. The robot did not move (minimum travel 0.1 m / 0.05 rad), so the graph stays at
  one vertex in both cases, and `/pose` is silent in both.
- Side effect: the hand-started slam_toolbox wrote to the stack's save path
  `/workspaces/isaac_ros-dev/maps/20261018-172133/map.posegraph` at start.

## Stationary localization drift

Evidence: `~/sentry-deploy/2026-10-18/localization-drift/{report.md,comparison.json,code-analysis.md}`. Endpoint planar
displacement of the scored window; the robot/sim is parked.

| Case | Raw (m) | rf2o (m) | EKF (m) | Map→root (m) |
| --- | --- | --- | --- | --- |
| Real rerun, 180 s | 0.000 | 1.020 | 1.025 | 1.024 |
| Archived real, 120 s | 0.000 | 2.176 | 2.091 | 2.091 |
| Sim, still target, 180 s | 0.000 | 0.039 | 0.040 | 0.040 |
| Sim, moving target, 180 s | 0.000 | 0.054 | 0.055 | 0.055 |

Mechanism (leading cause, associational):
- Real scans have 335–358 beams (archived 340–361) with `angle_compensate=false`; sim is a fixed 800.
- rf2o fixes width/FOV from the first scan (`rf2o_laser_odometry/src/CLaserOdometry2D.cpp:69`) and maps that width over every
  later scan (`:210`), so a shorter scan is read past its valid vector and a longer one is truncated.
- EKF fuses raw yaw/vx/vy but no raw x/y, and rf2o x/y absolute (`sentry_localization/config/ekf.yaml`), so zero raw
  odom does not anchor position.

Recommendations (not applied):
- Normalize the scan grid first and reject/reset incompatible count/angle metadata before the Eigen map.
- Add a raw-stationary gate in `CLaserOdometry2DNode::process()` with fresh-odom checks; missing/stale odom disables it.
  Needs a policy for slip/push cases; untested.

## Serial, camera and stamps

Evidence: `~/sentry-deploy/2026-10-18/timing-sim-to-real/report.md`. Robot passive; sim on the Mac mini (190 s, camera
off, `sushi serve` at ~220% CPU). Clean robot rates come from the run without image subscriptions.

| | Real | Sim |
| --- | --- | --- |
| POSE rate | 88.1 Hz | 87.3 Hz |
| POSE max gap | 3999 ms (1 gap) | 34.9 ms |
| REF_SYS rate / max gap | 9.8 Hz / 4091 ms | 9.7 Hz / 158 ms |
| CV_TARGET TX | 40.0 Hz, max gap 57 ms | 38.8 Hz, max gap 49 ms |
| CRC errors | crc8 = 1 of ~241k frames | not exposed |
| `/scan` age p50 / max | 91 / 134 ms | 24 / 31 ms |
| `/odom` age p50 / max | 6.6 / 231 ms | 3.0 / 7 ms |

- Serial stall: one 4.09 s receive stall at a fixed 180.0 s period, covering POSE and REF_SYS. The bridge RX byte counter
  stops while `cv_target` TX continues. The period survives a service restart but its phase changed after the MCB flash
  reset, which points at the MCB or its UART transmit path. The hosted firmware in sim shows none.
  Explained (2026-10-19, team): the MCB's periodic IMU recalibration
  ([`ImuRecalibration`](../../firmware/MCBV3/MCB-project/src/drivers.hpp)) pauses its UART output. It does not run in
  matches, so no fix is planned.
- Camera (robot, no image subscription): color and depth `camera_info` 59.6 Hz, no gap over 100 ms, stamp skew 0.10 ms.
  `/detections_output` 55.6 Hz, age p50 52.5 / max 251 ms. `roi_depth_node` rejections (`Depth too stale`, 0.050 s): 91 in the
  journal, 82 in the first run with no observer.
- Timestamp candidates (needs author confirmation): `/cv/target` and `/dji_serial_bridge/cv_target` carry a fresh
  stamp (age 1.8–2.7 ms against 52 ms on the detections they derive from); sim `/cv/target_state` repeats a stamp on
  66% of messages (7246 of 11025).
- TF: lookups at the message stamp mostly fail as "future" on both sides; 250 ms later real is 98–100% OK for non-camera
  topics. Camera frames to `odom` fail on the robot in every run (not investigated).

Recommendations (not applied):
- Confirm whether `/cv/target` is a prediction (fresh stamp allowed) or a measurement echo (stamp should be capture time).
- Run the robot lidar with `angle_compensate:=true` ([LIDAR-grid](../ROADMAP.md)), then repeat the slam acceptance with
  the robot driven, to see later scans accepted.

## Not measured

- Real PING RTT, real capture-to-`/cv/target` latency, sim camera/YOLO timing, slam scan acceptance while moving.
