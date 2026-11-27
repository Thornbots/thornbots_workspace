# Sentry shot accuracy in `mcb_match` (2026-11-26)

We measured the sentry's valid armor contacts in the hosted headless
`mcb_match` and traced the misses to their sources. Three are sim fidelity
errors. Two are firmware timing errors. One is tracker lag on spin-ups.
Changes: [MCBV3 #150](https://github.com/Thornbots/MCBV3/pull/150),
[sim #122](https://github.com/Thornbots/sim/pull/122),
[thornbots_pkg #83](https://github.com/Thornbots/thornbots_pkg/pull/83) and
[ros2_dji_serial_bridge #52](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/52).

## Result

The table covers five checker-accepted runs each of
`run_suite.sh mcb_match backend:=hosted headless:=true`.

- **Attempts** exclude contacts with defeated robots and shots fired after both opponents fell.
- **Hits/s** is valid contacts divided by the segment's route time before both opponents fell.
- **Before** is workspace `nightly` (sim `a9a8b99`, MCBV3 `332a097`, thornbots_pkg `abf2c60`).
- **After** adds the four PRs.

| Segment | Before: valid/attempts | Before: hit rate | Before: hits/s | After: valid/attempts | After: hit rate | After: hits/s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Drive | 20/37 | 54.1% | 2.27 | 25/36 | 69.4% | 2.89 |
| Parked | 26/30 | 86.7% | 4.81 | 33/34 | 97.1% | 5.41 |
| Spin | 149/169 | 88.2% | 4.50 | 137/142 | 96.5% | 5.25 |

These runs are close to deterministic: repeated runs of one build fire at nearly
the same instants. Changes were therefore compared over eight detector-noise
seeds per configuration through a local, uncommitted launch hook. On the
corrected sim (bias and ghost hull fixed):

- **Firmware and tracker changes.** Spin rose from 86.6% (4.54 hits/s) to 97.9% (5.25 hits/s). Drive rose from 46.6% (1.92) to 60.7% (2.69). Parked stayed at about 98%. These seeded runs used a tracker spin noise of 15 rad/s², not the final 10.
- **Fire margin, tried and rejected.** A 2–3 cm inset of the firmware's panel gate left spin unchanged and lowered drive hits/s (2.69 → 2.54 / 2.10). The firmware keeps its documented full-outline gate.

## Causes

1. **Sim launch bias.** The firmware aims against the robot-fitted
   `SHOT_PITCH_DOWN_BIAS` (0.042 rad). The scorer launched along the bore, so
   shots landed about 0.042 rad × range high. Opponent_1 misses crossed 6.6–7.4
   cm above centre at about 1.6 m. Fixed in sim.
2. **Ghost hull covering armor.** The 0.75-scaled hull hid half of `armor_0`.
   Opponent_1 late-spin misses had the panel face-on (phase 0 ± 0.06 rad) and
   recurred every 0.67 s, one ghost revolution. E27 R42 forbids self-obscured
   armor. The scale is now 0.65, the largest tested scale that hides nothing
   within ±45°.
3. **TARGET_STATE airtime.** The age is written before the first byte; receipt
   is stamped after the last, 7.7 ms later. Early-spin opponent_0 shots landed
   about 7 cm left of the panel edge on every seed. With the fix, 57 of 58 hit.
4. **POSE yaw latency.** POSE sent raw IMU yaw, 8 ms behind the head in hosted
   sim. The Jetson's camera TF lagged truth by 8–10 ms (best fit); it now lags
   about 2 ms. Median drive-phase TF yaw error fell from about 0.4° to 0.15°.
5. **Tracker spin-up lag.** The ghosts spin up at 20 rad/s² while we drive. At
   5 rad/s² of spin noise, the estimate stayed near 0 for over a second;
   logged true and estimated rates differ by up to 5 rad/s. 10 rad/s² halves the
   lag and passes the estimation limits that 5 passes. 15 rad/s² broke the
   steady-state spin-rate limits.

## Open

- **Ball position at the measured exit time.** Hits on near targets still arrive
  with the panel about 0.15 rad past face-on, about 16 ms late at 9.42 rad/s.
  The firmware assumes the ball leaves the bore front (0.173 m ahead of the
  pitch axis) at `FIRING_LATENCY_TIME`. The sim releases it at the pitch axis
  at that time, which accounts for about 8 ms. Which is right depends on what
  the robot's 20 ms "chamber exit" measured. Measure on the robot before
  changing either side.
- **Real Pico odometry refresh.** The real Pico pods refresh about every 260 ms
  ([MCBV3 odometry](../../firmware/MCBV3/README.md#aim-and-navigation-odometry));
  the hosted sim feeds pods every 1 ms. Drive-phase aim on the robot sees stale
  pivot and ego-velocity that sim does not model. Modeling it changes
  navigation and localization suites too, so it needs its own change.
- **Target-manager resend tolerance.** The MCB often propagates TARGET_STATE
  130–260 ms old. That is the accepted 100 mm resend tradeoff in the
  [TARGET_STATE contract](../../ros2_dji_serial_bridge/UART_PROTOCOL.md#proposed-target-assignment-update-and-clear),
  which we left unchanged.
- **Benches on this host.** The aim bench passes 10/10 in all 12 runs, but
  shot-floor cells vary run to run. The estimation bench's shooter_speed 1 and
  chassis_spin 9 stationary cells fail identically with and without the
  tracker change. The [aim-bench floor comparison](#aim-bench-floors) is below.

## Aim-bench floors

We ran three runs each of lateral, radial, diagonal and lateral with
`shooter_speed:=1.0` on this host, once with the PR build and once with
nightly. Every suite passed 10/10 with `bench ok`. `shot_floors` (lowest score
minus 0.10) put 11 of 40 cells below the checked-in `FLOORS` for each build,
in different cells. The mean floor was 0.880 for the PR build and 0.881 for
nightly. Per-run scores within a cell spread up to 0.09 (for example 0.996,
0.902 and 0.970). The aim bench feeds truth target states through the target
manager to the firmware `AimPlanner`, and none of the PRs changes that path.
The checked-in floors are not reproducible on this host for either build.
