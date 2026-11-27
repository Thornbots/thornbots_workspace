# mcb_match drive-phase tracker velocity (2026-11-27)

The [drive wall-clock investigation](drive-wallclock-2026-11-27.md#open) found
that, in the opening drive misses, the tracker estimated the target at
1.0–1.7 m/s while it moved at 0–0.5 m/s. Fix:
[MCBV3 #151](https://github.com/Thornbots/MCBV3/pull/151), with protocol docs in
[ros2_dji_serial_bridge #55](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/55).

## Cause

The problem is chassis tilt. It is not horizontal ego-motion, a TF stamp or
odometry latency.

- In seed 1 the velocity error is mostly vertical. At 18.66–18.76 s, the
  estimate is 1.6 m/s, `vel_err` is (0.0, −0.3, −1.6) m/s and the true
  target speed is 0.06–0.23 m/s.
- Over the same frames, the sentry brakes and re-accelerates (1.7 → 1.1 →
  1.7 m/s), and its chassis pitches up to 3.9° on the sprung carriers. The
  camera TF's pitch error against truth follows that tilt (+0.04 rad at
  18.64–18.81 s). The head yaw error stays under 0.005 rad, and TF translation
  error under 3 cm.
- POSE `head_pitch` was the encoder angle relative to the yaw link, and nothing
  else carried tilt. `root` is heading-fixed with level axes, so the
  `headpitch` joint left the camera off by the tilt. A changing tilt of about
  0.04 rad over 2 m moves panels vertically at about 1–1.5 m/s, and the
  tracker took that as target motion. The firmware's planner also aimed with
  the encoder pitch. The first drive shots landed 21 cm low (`panel_up_m`
  −0.21), then 12–20 cm to the side.
- Horizontal ego-motion is already handled: the filter runs in `odom`, and the
  lookup at capture time takes the moving camera into account. The median
  horizontal velocity error stayed about 0.3 m/s before and after the fix.

## Fix

The sentry firmware propagates world up through the yaw-link gyro (no
accelerometer, since acceleration causes the tilt). It projects that on the
barrel and high-passes it over 2 s, then adds it to the aim pitch. That aim
pitch drives the pitch controller and the planner's measured gate, and goes
out as sentry POSE `head_pitch`. Design:
[MCBV3 base tilt](../../firmware/MCBV3/README.md#base-tilt).

## Result

The table covers hosted `mcb_match`, `amcl_seed:=1..12`, alternating before
and after per seed in one container at 5 CPUs, on workspace #244. Three
baseline seeds (2, 5, 10) hit the known bring-up `nav_goal` ack timeout. Only
the 9 seeds accepted in both builds count.

| Build | Drive | Parked | Spin |
| --- | ---: | ---: | ---: |
| Before | 26/71 36.6%, 1.70 hits/s | 62/62 100% | 263/271 97.0% |
| After | 36/81 44.4%, 2.38 hits/s | 52/52 100% | 272/274 99.3% |

- With AMCL deterministic, every seed takes the same route, so the 9 pairs are
  near-replicas. Every seed went from 3/8 (one 2/7) to 4/9. Parked had fewer
  shots because opponents fell earlier, and its live time fell from 10.0 to
  9.15 s.
- Drive TF pitch error p95 fell from 0.044 to 0.005 rad. Tracker |vz| p90 fell
  from 1.20 to 0.32 m/s, and the median velocity error from 0.71 to 0.40 m/s.
- The drive misses that remain are lateral. They come with the
  [spin-up lag](sentry-shot-accuracy-2026-11-26.md#causes): the yaw-rate error
  is −3 to −4.5 rad/s while the ghost spins up.

Evidence: `~/Movies/sim-demo-2026-11-21/drive-tracker` (`RESULT.md`, `runs/`,
`agg.py`).

## Robot

The robot is affected: sentry pitch control and POSE change. The real chassis
also pitches under acceleration, but its tilt is unmeasured. The board IMU's
axes (`IMU_BARREL_FORWARD`, `PITCH_UP_SIGN`) are assumed to match sim's
yaw-link frame. Verify them with the
[base tilt check](../ROBOT_TESTS.md#consolidated-hardware-checks) before a
match.
