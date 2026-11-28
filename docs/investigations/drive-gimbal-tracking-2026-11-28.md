# mcb_match drive-phase gimbal tracking (2026-11-28)

Follow-up to [drive-aim-2026-11-27](drive-aim-2026-11-27.md), which found that
firmware aim was the largest drive miss component (6.1 of 8.7 cm RMS) and that
the head trailed a moving yaw plan by 0.02–0.08 rad. We logged the yaw setpoint, feedforward,
IMU yaw, controller target velocity and the gate's predicted impact on each
1 ms aim tick in a hosted debug build, then compared paired runs on the same
encounters (`amcl_seed` = `detector_seed` 1–16, `red_delay_s` 0–1.5 s,
`detector_noise:=true`). Same-seed runs give identical shots.

## Where the lag comes from

- **The controller tracks a continuous plan.** Between target-state arrivals,
  drive ticks with `|plan rate| > 0.3 rad/s` trail by −5.6 mrad mean (6.9 RMS).
  The 8 ms IMU predictor is within 0.7 mrad RMS. The gate's 20 ms head
  extrapolation is within 6 mrad RMS at fire requests.
- **The plan is a staircase.** `target_manager` resent TARGET_STATE only when the
  MCB's held model drifted more than 100 mm (now or 200 ms ahead), or every
  200 ms. While driving, states reached the MCB every ~50 ms (median 48 ms), and each one
  moved the aim point by 74 mm RMS (48 mrad of yaw). The position loop
  (KP 13, ~77 ms) was always chasing the latest step. Over 50 ms windows
  the setpoint moved 0.35 rad/s faster than its feedforward.
- **The gate fires during the chase.** At drive fire requests the head was
  18 mrad behind the setpoint on average. Shots fired more than 20 mrad off the
  setpoint hit 43%; under 5 mrad, 93%.

## Changes tried

Paired on the 15 encounters where all three builds passed the bench checker:

| Build | Drive valid | Drive hits/s | Drive median miss | Parked | Spin | Spin hits/s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Baseline (workspace #253) | 80/144 55.6% | 3.66 | 5.5 cm | 89/96 92.7% | 418/497 84.1% | 2.59 |
| `drift_tolerance_m` 0.02 | 98/151 64.9% | 4.49 | 4.9 cm | 100/107 93.5% | 390/438 89.0% | 3.91 |
| 0.02 + gate tracking margin | 81/124 65.3% | 3.71 | 4.4 cm | 78/84 92.9% | 426/469 90.8% | 3.20 |

With 20 mm, states arrive every ~16 ms and the aim-point step falls to 36 mm RMS.
The rest of that step is detector noise, not bias: the mean step along the sentry's own velocity is 1–3 mm.
Drive miss RMS (right) fell from 8.4 to 7.3 cm: tracker 3.6 → 3.0 cm, prediction 2.5 → 1.1 cm.
`drift_tolerance_m` 0.05, on 10 paired encounters, fell between: drive 53.7 → 57.7%, against 62.5% at 0.02.

The gate tracking margin (sentry only) takes `|yaw setpoint − measured yaw| × range` off
the panel half-width. Offline it promised a higher hit rate, but the shots it
blocked were mostly replaced by later shots that hit no more often. It cost hits/s in every segment.
On its own (100 mm tolerance, 16 encounters) it gave drive 55.3 → 58.3% but
3.57 → 3.23 hits/s, and parked 5.12 → 4.67 hits/s. It is not shipped. We kept the
yaw/pitch gains: they are robot-tuned, and the yaw loop already tracks a
continuous plan.

## Open

- Sentry pitch has no velocity feedback (`KPV` = `KIV` = 0). In sim it settles
  ~11 mrad low of the plan. The gate accounts for it, but it costs vertical
  margin. Gains are robot-tuned, so we did not change them from sim.
- The UART load is ~60 Hz × 89 bytes, about half the Jetson → MCB link. The
  robot check is [B-target-state-rate](../ROBOT_TESTS.md#moving-aim).

Evidence: `~/Movies/sim-demo-2026-11-21/drive-aim3` (`RESULT.md`, `runs/`,
`fw-trk-debug.patch`, `trk.py`, `plan.py`, `extrap.py`, `gate.py`,
`rangegate.py`).
