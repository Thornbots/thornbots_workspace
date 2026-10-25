# rf2o drift reliability comparison — 2026-10-25

No higher shared-suite failure rate was observed for B or C than for the specified nightly baseline A. This sample does not establish noninferiority: eight runs per build leave broad uncertainty. Prefer the default-off B configuration for further integration review; this evidence provides no reason to release the separate references-ON C hold. Physical parked/panning/shove acceptance is still outstanding. Nothing was merged or run on a robot.

## Frozen builds and method

- A: workspace `7b17b54`, rf2o `ddb64de`, sim `c5aa4ba`, localization `496e09f`.
- B: workspace #96 `68a2422`, rf2o #18 `92c7978`, sim #44 `dd98580`, localization `496e09f`; references default OFF.
- C: workspace #97 `1becf58`, B binaries plus localization #18 `eefb817`; references ON.
- Mac mini, sole agent container `isaac-agent-drift-flake-ab`, 4-CPU quota / 8 GiB, domain 167, unique partition. `agent_container.sh ls`, smoke, package prefixes, binary hashes and YAML retained. Independent immutable source archives and install overlays prevent changing the build under a trial. B/C rf2o binaries have the same SHA-256.
- Eight full drift suites per arm, rotating A/B/C, B/C/A, C/A/B; original gates, AMCL, rf2o, headless and no Foxglove. A has nine scenarios; B/C have ten. All 24 full attempts count: zero lockstep-timeout exclusions, retries or missing scenarios. Total 232 scenario trials.
- Each passing suite also passes native `check_bench_log`. Six failed suites retain their failed GTest/launch/native-checker verdicts. Shared-suite failure counts use only the nine shared scenarios: the checker rejects a whole suite when parked_push alone fails, so that known assertion must not be attributed to a shared scenario. No independent unexpected checker failure was found.
- Four additional standalone noise_correction trials per arm alternate separately. They are diagnostic follow-ups, excluded from the full-suite rates below.

## Failure rates

| Scenario | A failures | B failures | C failures |
| --- | --- | --- | --- |
| baseline | 0/8 | 0/8 | 0/8 |
| noise_correction | 0/8 | 0/8 | 0/8 |
| drift_correction | 0/8 | 0/8 | 0/8 |
| drift_correction_obstacle | 0/8 | 0/8 | 1/8 |
| moving_obstacles | 1/8 | 1/8 | 0/8 |
| real_accel | 0/8 | 0/8 | 1/8 |
| jerk_with_motion | 0/8 | 0/8 | 0/8 |
| odom_stuck | 1/8 | 0/8 | 0/8 |
| scan_degraded | 2/8 | 0/8 | 0/8 |
| parked_push | absent | 1/8 | 0/8 |
| suite_shared | 2/8 | 1/8 | 2/8 |
| suite_full | 2/8 | 2/8 | 2/8 |

For eight runs, rough 95% Wilson intervals are: 0/8 = 0% [0, 32.4%]; 1/8 = 12.5% [2.2, 47.1%]; 2/8 = 25% [7.1, 59.1%]. These binomial intervals are approximate; cases within a suite and successive runs need not be independent. All full suites failed 2/8 per arm; on the shared scenarios A/C failed 2/8 and B 1/8. The observed differences do not support a regression claim, and the intervals cannot rule out a material regression. Rates are not inferred from aggregate scenario counts.

## Counted failures and margins

- A round 5: moving_obstacles 0.8211 m vs 0.40 (margin -0.4211 m); scan_degraded before-error 3.0134 m vs 0.40 (-2.6134 m). Both are counted in the same failed suite.
- A round 7: odom_stuck and scan_degraded each fail startup after 30 s with map->nav_odom missing while odom->root and nav_odom->odom are ready. Numeric margins are unavailable; both failures count.
- B round 3: parked_push raw scan-odometry vector error 0.0169 m vs 0.015 (-1.9 mm). Localized error 8.6 mm passes, truth moves 40.6 mm, 102 scan matches and zero failed grades. This is additional coverage absent from A.
- B round 5: moving_obstacles 0.8621 m vs 0.40 (-0.4621 m).
- C round 1: real_accel 0.7656 m vs 0.40 (-0.3656 m).
- C round 7: drift_correction_obstacle 0.6410 m vs 0.40 (-0.2410 m).

`scenarios.tsv` records every verdict and numerical gate margin. Margins are reconstructed from printed precision; native verdicts remain authoritative. Composite gates use the tightest applicable numerical margin; startup failures retain an empty numerical margin. `rates.tsv` includes per-scenario counts and confidence limits, including an explicit absent A/parked_push row.

## Noise growth versus rf2o divergence

All 24 full-suite noise cases pass, as do all 12 separate standalone probes. No growth failure reproduced, so these runs cannot determine whether the historical 4.17/2.10 growth failures accompanied rf2o divergence. Do not claim those historical failures were harmless or caused by the ratio alone.

The unchanged growth gate compares maxima of AMCL map->nav_odom correction in the second and first halves; it does not directly measure raw rf2o trajectory error. Diagnostics align scan_odom to interpolated sim truth at scan stamps, take the final 30 sim seconds before each verdict to exclude startup/teleport, and remove the initial position offset for accumulated displacement error. No fitted rotation or trajectory rescaling is used. All recorded grades in those windows are good.

Full-suite maxima across eight runs per arm:

| Arm | Maximum relative accumulated scan error | Maximum scan increment error | Growth-ratio range |
| --- | --- | --- | --- |
| A | 27.01 mm | 5.72 mm | 0.765–1.242 |
| B | 23.21 mm | 7.20 mm | 0.801–1.309 |
| C | 27.30 mm | 6.80 mm | 0.708–0.984 |

Standalone probes also show no increment error over 0.1 m, with maximum accumulated errors 16.37 / 19.98 / 22.36 mm for A/B/C. This rules out an observed large divergence in these recorded noise windows; it does not settle the unobserved historical failure mechanism. See `noise-diagnostics.{tsv,json}`, `noise-probe-noise-diagnostics.{tsv,json}`, timed events and recordings.

## Unit timeout fix

Signed rf2o #18 commit `312ac7deb75abe45736decf8ee671e52735c087c` is pushed after `92c7978`, without rewriting history. Workspace #96 gitlink bump is `dc0cd5c`; #97's is `9b04098`.

The earlier failure is an intermittent construction stall, not 58 tests consuming 60 seconds of normal matcher work: completed node suites take roughly one second, while retained prior-round logs stop during node initialization and hit the default 60 s limit. Each fixture constructs the wrapper node, the Node-derived matcher, and TransformListener's hidden node/thread. Multiple tests reconstruct fixtures inside loops, and invalid-parameter coverage constructs 16 additional wrappers. Repeated middleware/TF construction in one process is avoidable test overhead. The default TransformListener constructor also departs from tf2's recommendation to use the existing-node overload when a node is available. Production TF wiring is unchanged in this test-only change.

The exact blocked middleware stack was not reproduced in five GDB runs; no specific Fast DDS locking bug is claimed. The chosen fix is the explicitly permitted process boundary: retain all 34 node regressions in four separately registered GTest executables (startup, reference motion, reference lifecycle, clock reset), each with a 120 s CTest limit. The existing 24 matcher cases remain registered separately. A shared test-only library compiles node code once. CI and ordinary colcon discover all five executables with no shard variables or custom filters.

Splitting exposed float contraction/inlining changing synthetic angle_max by one ULP between calls. A constexpr angular grid now preserves consistent geometry; assertions and tolerances are unchanged. All 34 node test bodies were moved without assertion changes. Production src/include tree IDs are identical to `92c7978` (`production-trees.txt`).

`colcon test --packages-select rf2o_laser_odometry` passed unsharded three consecutive times with all 58 tests, zero skipped/disabled/error/failure cases and roughly 1.7–1.9 s CTest durations. Exact commands use the dedicated build/fixed directory and --return-code-on-test-failure; GTEST shard variables are unset. All five XML reports per run and result logs are retained. Host Python 3.12 quality/actionlint pass in rf2o and both workspace layers; no baseline was expanded. Signed commits use Blaise Baptist's configured identity/key.

## Retained setup attempts and cleanup

The first sim build hit the 8-GiB limit compiling unrelated registered test targets; setup resumed with one compiler and BUILD_TESTING=OFF for sim while retaining its full drift executable. This OOM predates the accepted runtime matrix. rf2o's separate fixed build has BUILD_TESTING=ON. Early split-fixture attempts failed unchanged assertions because of angular-grid rounding; a diagnostic RelWithDebInfo original-suite build also failed the existing 0.1-micrometre replay comparison. Those attempts are not claimed as passes; the requested final Release configuration passed all 58 cases three times. GDB and a retained grid-failure log remain in evidence.

The first A recorder shutdown waited after the native suite had already completed; status.tsv's 1801 s includes that idle recording wait. Its native timing and valid scenario data are retained. Recorder shutdown was fixed before the remaining trials. All later matrix durations are 134–184 s. The only runtime processes before cleanup were init/sleep and the inspection command. Own container and volumes were removed, then Colima stopped; no foreign container was touched.

Evidence: `~/ros2_ws/drift-flake-ab-20261025/` contains `rates.tsv`, `scenarios.tsv`, `source-manifest.tsv`, all native suite/detail logs, binary/config provenance, telemetry gzip files, timestamped events, analysis/run scripts, unit XML and logs, setup attempts and cleanup logs. `SUMMARY.md` is this report. No firmware or movement change, physical-robot run, PR merge, forced push or gate relaxation.
