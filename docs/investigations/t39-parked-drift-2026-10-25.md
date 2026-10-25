# Parked rf2o drift (T39) — 2026-10-25

Current workspace #95 keeps `reference_scans` available but off by default:
sentry_localization remains at nightly `496e09f`, without #18. The runs below
are historical opt-in experiments, not validation of this default configuration.
Job A changes only workspace pins and documentation; it reruns host quality
and actionlint, not the sim suites. Evidence:
`~/ros2_ws/rf2o-ref-followups-20261025/job-a/`.

A parked robot's navigation pose wandered because rf2o integrates
scan-to-scan match noise and the EKF takes rf2o's x/y as its only position.
Wheel odometry held still. rf2o's new `reference_scans` matches a parked
scan against an earlier scan from the same head angle instead of the one
before it, so the error stops integrating. In sim, `mcb_parked` p95 fell from
0.005-0.090 m to 0.002-0.009 m in every cell. Drive, AMCL drift and EKF
suites did not regress, and a 4 cm shove with the wheels held still moves
the estimate. No movement, firmware, noise model or gate changed. Hardware
is untested.
Mechanism and parameters: [rf2o README](../../rf2o_laser_odometry/README.md);
tuning rationale: [sentry_localization](../../sentry_localization/README.md#configrf2oyaml).

## Evidence

Mac mini, own container (2 CPUs) on nightly `7b17b54` pins plus this change;
`~/ros2_ws/t39-parked-drift-20261025/` holds scripts, logs, bags and
`status.txt`. A/B runs alternate arms in one container; "off" sets
`reference_scans: false` on the same build.

## Cause

- Nine earlier `mcb_parked` runs
  ([A/B, 2026-10-23](fieldmap-divergence-2026-10-22.md#parked-odometry-ab)):
  net `nav_odom` drift averaged 0.54 mm/s with the head still and
  0.62-0.65 mm/s with it slewing at 23-48 deg/s. Head motion is not the cause.
- Bags of one run per arm (`on-r1-bag`, `off-r1-bag`, 274 s after bring-up),
  largest distance from the starting x/y:

  | Topic | off | on |
  | --- | --- | --- |
  | `/odom` (wheels) | 0.0023 m | 0.0020 m |
  | `/scan_odom` (rf2o) | 0.0688 m | 0.0078 m |
  | `/localization/odom` (EKF) | 0.0621 m | 0.0030 m |

- AMCL's correction stayed under 0.008 m p95: parked, it never reaches
  `update_min_d`, so nothing bounds the drift.

## Design iterations

1. References kept until rf2o moved 5 cm. Parked error fell as below, but
   AMCL drift-suite corrections rose while driving slowly (`real_accel`
   0.079-0.228 m over 7 runs vs 0.063-0.097 m off): matching across up to
   5 cm read short. The constant-velocity prior after a reference match also
   spanned the whole reference, not one scan (fixed and unit-tested).
2. References dropped at 2 cm of rf2o or odom motion: still higher
   `real_accel` (0.078-0.091 m vs 0.052-0.097 m), and 2 of 9 drift runs
   failed (`moving_obstacles` 0.437 m, `scan_degraded` 0.951 m) against 0 of 9
   off. Neither was traced to a reference, but neither could be ruled out.
3. Final: references only while parked, i.e. `/odom` within 5 mm for 2 s.
   Odom moving clears them, so driving, including the drift suite's 1 s
   corner dwells, runs the unchanged scan-to-scan path. Results below.

## Results (final)

`mcb_parked`, p95 m. All 12 cells passed in every run.

| Arm | Runs | Diagonal cells | All cells | Shots / hit rate |
| --- | --- | --- | --- | --- |
| off | 5 | 0.032-0.090 | 0.005-0.090 | 2074 / 0.896 |
| on | 5 | 0.002-0.009 | 0.002-0.009 | 2068 / 0.907 |

Same final build, references on:

- `mcb_drive` 3/3 passed.
- `ekf` 8/8 passed, fused mean error 0.006-0.029 m (average 0.019).
  Off, 8 alternating runs on the previous build (the off path is identical),
  8/8 passed at 0.012-0.067 m (average 0.033). The gate saw a scan
  divergence fail 1 of 15 off runs.
- AMCL `drift` 9/9 passed, every scenario, alternating with 4 off runs (3
  passed; one `real_accel` divergence read 2.59 m). Corrections on vs off:
  `real_accel` 0.071-0.086 vs 0.087-0.097 m, `drift_correction` 0.090-0.128
  vs 0.110-0.130 m, `scan_degraded` during the blackout 0.354-0.432 vs
  0.425-0.499 m. The previous build's 9 off runs all passed.
- `parked_push` (`odom_slip_ratio` 1, 1 cm/s for 4 s): truth moved
  0.041 m; the estimate missed by 0.0042-0.0063 m on (9 runs) and
  0.0025-0.0113 m off (13 runs). The estimate follows a shove.

## Combined startup and review validation

The combined rf2o head `d6a3888` stacks this change on startup/failure-recovery
head `ee3ff63` ([rf2o #16](https://github.com/Thornbots/rf2o_laser_odometry/pull/16));
merge #16 before #17. The historical combined validation used
sentry_localization `20a6f01` (references enabled) and sim `9221884`
(stronger `parked_push`). Workspace #95 still stacks on #94 and pins that
rf2o and sim state, but now keeps localization nightly `496e09f` without #18.
PR bases remain `nightly`. Historical evidence:
`~/ros2_ws/rf2o-combined-20261025/`.

The integration preserves the pending scan queue and 1 s give-up rule, rejects
stamps before substituting an anchor, and restores the accepted consecutive
pyramid after failed anchored matching/fallback. Missing or nonfinite wheel
priors cannot seed an anchor. Review fixes judge speed and report robot-frame
x/y/yaw twist over consecutive accepted robot poses and stamps, independently
of anchor age; reference tolerances are validated and the bank is bounded.
`/scan_odom` twist carries robot-frame vx/vy from consecutive accepted poses;
there is no robot consumer of that twist.

Mac mini, own 3-CPU container, gates unchanged:

- All 47 rf2o tests pass, including long-park false alignment and twist, failed
  fallback plus moving-head recovery, bumps, long wheel-slip push, wheel creep,
  non-repeating head angles, obstacle capture and prior-loss recovery.
- AMCL drift 3/3, all 30 scenarios including the stronger raw scan-odometry
  displacement/quality assertions in `parked_push`. No `real_accel` failure.
- `mcb_parked` 3/3, all 36 cells. Diagonal p95 ranges by run:
  0.00184-0.00411, 0.00787-0.01003 and 0.00064-0.00255 m; the largest
  all-cell p95 is 0.01099 m, consistent with the approximately 0.01 m target.
- EKF 5/5. The native checker accepts its recorded shutdown notes.
- Drive initially 2/3: run 2 never reached center or fired, with 0.0315 m
  localization p95 and 0.0157 m final navigation error. Three alternating
  follow-ups pass on both `ddb64de` and the combined build. Combined total
  5/6; the original route-completion failure remains unexplained and counted.
  This small comparison does not establish that it predates these fixes.
- No lockstep timeouts in any revised or comparison run. Existing gates stay
  unchanged; `parked_push` adds raw scan-odometry displacement/quality checks.
- Live move-before-init, restart while moving and delayed restart settled
  offsets: 0.00723, 0.00757 and 0.00209 m. The same replay scripts run with
  references enabled. Moving-base/moving-head 2.5 s odometry stall: final and
  tail-max error 0.01374 m against the unchanged 0.02 m gate.

Pre-review combination evidence remains under `pre-review/`: its first drift
run failed `noise_correction` at 2.0215 m; two more passed. All three revised
runs pass that scenario. No cause is established by these small samples.
The corrected build supersedes an early conflict-cleanup error caught in diff
review; initial expanded unit logs also retain two overly strict new fixture
assertions (17.3 mm error over a 150 mm shove, and scan-to-scan drift with
non-repeating angles). Existing suite gates and lint baselines did not change. Host Python 3.12
quality/actionlint pass in rf2o, sim and workspace; repository policy and changed
local links pass. Commits use the configured signing key and author identity.

## Limits

- Sim lidar noise is constant 1 cm Gaussian; the real RPLIDAR's error model,
  dropouts and dynamic obstacles may change match grades and how often
  references drop.
- References need `/odom` still for 2 s; a robot that creeps more than 5 mm
  in 2 s (slipping wheels, encoder jitter) falls back to scan-to-scan.
- A parked shove reads up to 0.011 m short of 0.041 m with or without
  references: rf2o blends each match with the still wheel prior.
