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

## Lidar scan format

Evidence: `~/sentry-deploy/2026-10-18/lidar-scan-format/` (files 00–21, `source_refs`). Robot `ts-nano-sentry`, RPLIDAR
Express mode, 60 s probes.

| | Real default | Real `angle_compensate:=true` | Sim |
| --- | --- | --- | --- |
| `/scan_raw` beams | 340–359, 13 distinct counts | 720 fixed | pending |
| `/scan` after self filter | 340–359 | 720 | pending |
| Angle increment | ~1.00–1.01° | 0.5007° | pending |
| slam_toolbox `expected N` warnings | warning counter 174 → 181 in the probe window; per-run logs (`11_`) show up to 499 `expected` mismatches per run | counter 194 → 195 across the 60 s probe without restarting slam_toolbox; fresh-start acceptance not measured (`21_` holds only the start count, 0; the probe was cut off) | pending |

- Sim: scans are a fixed 800 beams (source: `localization-drift/report.md`). Sim lidar measurement is in progress by
  another agent.

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

## Pending

- Serial / camera / stamp timing: in progress.
- Mac-mini sim measurements: in progress.
