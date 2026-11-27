# mcb_match drive accuracy and host CPU (2026-11-27)

The [match recheck](sentry-shot-accuracy-2026-11-26.md) found that, on one
nightly build, the hosted `mcb_match` drive hit rate was 51% at 5 container
CPUs and 66% at 10. Parked and spin stayed at 96–100% in both. The stack is
lockstepped, so some input to the drive phase still ran on wall time. That
input was AMCL. Changes:
[sentry_localization #54](https://github.com/Thornbots/sentry_localization/pull/54)
and [sim #127](https://github.com/Thornbots/sim/pull/127).

## Cause

- The drive score depends mostly on when the route reaches the drive leg,
  not on aim accuracy. In 28 earlier 5-CPU runs the drive segment started at
  18.25, 18.35, 18.45 or 18.55 s. The 100 ms steps are `waypoint_nav`'s ticks.
  The earlier the start, the lower the score: 33%, 45%, 57% and 61%. Within one
  start time, 5 and 10 CPUs agreed within noise. The early starts add an opening
  burst of misses at the 100 ms launcher limit.
- Runs diverged at a waypoint corner about 14 s into the approach. AMCL's map
  pose already differed by centimetres at 12 s. AMCL corrections reach the
  firmware as RELOCALIZE and also move the arrival position that `waypoint_nav`
  uses ([relay](../../thornbots_pkg/README.md#mcb_relay)).
- AMCL ran outside the lockstep in four ways:
  1. `map_pose_publisher` used the newest `/amcl_pose` that had *arrived*, so
     AMCL's compute time picked the EKF tick that saw each correction.
  2. `initial_pose_setter` sends `/initialpose` every wall second until AMCL
     answers. The pose landed at sim 1.6–4.9 s.
  3. `pf_init`'s Gaussian calls `srand48(++counter)`. The counter counts those
     `/initialpose` messages (14 at 5 CPUs, 11 at 10), so the particle draws
     differed by CPU even with a fixed seed. `pf_alloc` also seeds from
     `time()`.
  4. nav2 registers the laser on its first scan from latest TF, not the scan
     stamp.

  A tf2 sample hit exactly at a scan stamp also reads 1 ulp differently once a
  newer sample arrives.

## Fix

These apply in the sim only (all parameters default off):
- AMCL answers every scan, in stamp order, once TF reaches 1 ms past it.
- The `scan` chain waits for `map_pose_publisher` to have seen each scan.
- An EKF tick waits for AMCL's answers to every scan at least 50 ms
  (`AMCL_DELAY_S`) older than it, and uses no newer sample.
- AMCL starts at the first scan from 5 s, from the spawn prior with its own
  seeded draws (`amcl_seed`), and registers the laser at the scan stamp.

Design: [sim lockstep notes](../../sim/README.md#lockstep-waits-and-load) and
[lockstep AMCL](../../sentry_localization/README.md#configamclyaml).

## Result

Hosted `mcb_match` (`run_suite.sh mcb_match backend:=hosted headless:=true`),
counted with the recheck's `summarize.py`. Seeds were `amcl_seed:=1..12`, with
configurations alternated in blocks while a video render ran on the host.

| Config | Accepted | Drive | Parked | Spin | Drive start |
| --- | ---: | ---: | ---: | ---: | --- |
| Fixed, 5 CPUs | 11/12 | 37/89 41.6% | 73/74 | 319/330 | 18.35 s in all |
| Fixed, 10 CPUs | 12/12 | 37/95 38.9% | 81/83 | 350/364 | 18.35 s in all |
| Nightly, 5 CPUs | 12/12 | 56/96 58.3% | 78/78 | 334/343 | 18.35–18.55 s |
| Nightly, 10 CPUs | 10/12 | 40/75 53.3% | 64/64 | 284/295 | 18.15–18.55 s |

- The CPU dependence is gone. Before the fix, two 5-CPU runs differed from
  12 s. With it, the same seed at 5 and 10 CPUs gives the same route and AMCL
  results and the same drive start. Shots usually match through most of the
  drive leg.
- Today's nightly runs showed no 5-vs-10 gap. Achieved RTF was about 0.97 in
  both, against 0.66–0.79 at 5 CPUs in the recheck. The gap needs a
  saturated quota; the mechanism does not.
- The fixed drive rate is lower than nightly's because every run now takes the
  18.35 s start. In those runs the first five shots miss while the sentry
  accelerates. Moving `AMCL_DELAY_S` to 40, 70 and 100 ms gave 3/8, 4/8 and
  4/10. The modelled latency is not tuned to pick a start.
- Rejected runs: 3 nightly bring-up `nav_goal` ack timeouts and 1 fixed AMCL
  activation hang. Lock-order changes followed the hang, and none recurred in
  25 later runs.

## Open

- **Drive-phase tracker velocity.** In the opening misses, the tracker
  estimated 1.0–1.7 m/s for a target moving at 0–0.5 m/s. The error is about the
  sentry's own speed. The same error appears at both CPU caps and before the
  fix (median drive velocity error 0.74 m/s). This looks like ego motion leaking
  into the odom-frame target, and it is the next drive-accuracy lead.
- **Residual sim nondeterminism.** Paired runs still split by about 1e-5 m in
  chassis state from about 18.7 s in some seeds. It changed the drive score in
  3 of 23 fixed runs. Locate it with `MCB_UART_TRACE` diffs
  ([sim](../../sim/README.md#lockstep-waits-and-load)).
- **Robot.** The robot keeps the newest arrived AMCL sample (all new
  parameters default off). Its RELOCALIZE timing therefore follows Jetson load
  in the same way. The adapter composes each correction at its stamp, so that
  timing is not an error, but it is not repeatable. Real AMCL latency is
  unmeasured.
