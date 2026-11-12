# Absolute field RELOCALIZE — 2026-11-11

Status: gate values approved by the user and integrated on `nightly`
2026-11-12; no physical robot run yet ([T41](../ROBOT_TESTS.md#parked-localization)). Baseline workspace:
`2c48a8237d42403370b95a6d334a53a6bcb256d6` (`origin/nightly`).

## Decision and frame contract

RELOCALIZE carries the AMCL-corrected absolute field position. The local EKF
pose alone cannot correct global drift. Firmware already interprets x/y as an
absolute position and replaces a translation-only navigation offset; the UART
payload and board behavior require no change.

The localization adapter pairs backend `map->root` with interpolated local
`nav_odom->root` **at backend capture time**, derives their planar correction,
and composes it with each current EKF input. This avoids AMCL's future-dated TF
and removes the old unbounded latest-TF fallback. The relay rotates raw
**displacement** by this correction's yaw when predicting application time.
Neither raw aim odometry nor `nav_odom->odom` receives a yaw correction.

Blank mapping has no absolute field source. Mapping, blank-map SLAM and `none`
retain team-start navigation, independently of the local-zero map. Waypoint
arrival reads the relay's nominal held-position estimate, including its
thresholds, step limit and predicted application delay. UART provides no
acknowledgement: temporary disagreement after a lost fix remains possible
until a fresh retry. This estimate is not actual navigation feedback.

Each EKF input produces one map result. Missing history or expired covariance
produces NaN position and infinite covariance at that input stamp, so the
relay emits a none-mark and releases the lockstep chain. No chain waits for a
scan while physics is held. AMCL particle/callback timing remains nondeterministic.

Maintained contracts: [localization](../../sentry_localization/README.md#contract-with-thornbots_pkg),
[relay](../../thornbots_pkg/README.md#mcb_relay),
[arrival](../../nav_pkg/README.md#frames),
[UART](../../ros2_dji_serial_bridge/UART_PROTOCOL.md#message-types).

## Measurement method

The new both-team moving case uses Gazebo scans, the real rf2o/EKF/AMCL stack,
real UART bridge and compiled hosted sentry firmware. It drops the first
startup RELOCALIZE, then drives two 0.6 × 1.2 m loops at 0.4 m/s while pods
have 15% scale error plus 0.025 m/s accumulating x bias. No physical robot is
involved. Each trace retains delivered corrections, global samples and held
position vs truth.

The score comes from **actual firmware `odo.getX()/getY()`**, exposed only
through the private hosted MappingStatus socket. The fixture compares its last
received status (one 5 ms fixture tick old) with current hardware truth. It
includes gate holds, dropped frames and firmware's single receive slot. It is
not reconstructed from TF, the last requested fix or the relay's estimate.
The test also records local/global pose error, xy covariance's largest
eigenvalue, pose/backend age and delivered wire targets' distance from the
last observed firmware position. This last metric includes observation lag
and does not prove that every target survived the firmware mailbox. Truth and firmware
retain that observation lag; pose-age effects are included rather than removed
by retrospective alignment. At 0.4 m/s, the nominal one-tick lag is 2 mm.

Before runs use unmodified nightly runtime sources plus the same measurement
readout/test fixture. On resumption, both localization and relay packages were
rebuilt from the baseline gitlinks in an isolated overlay inside this worktree's
ignored `log/absolute-amcl/` directory. Package-resolution paths, executable
SHA-256s and source revisions were captured before three new both-team runs.
These runs supply the final before values; the inherited three before runs
remain in the raw archive. The existing supplied archive
`/tmp/amcl-boot-baseline-2026-11-11.tar.gz` covers the original four startup and
blank-mapping cases; it has no held-position metric and is not used to invent
moving before values. Before/after moving cases each need three trusted runs
per team. Native log-check failures invalidate a case even when its accuracy
assertion passes.

## Proposed gate values and evidence

| Policy | Proposed value | Evidence and limit |
| --- | --- | --- |
| xy standard deviation ceiling | 0.35 m | Rebuilt before runs reached 0.231 m; final after runs reached 0.219 m; prior trace saw 0.17–0.30 m. The old 0.02 m ceiling rejects AMCL. 0.35 m is a review margin, not a calibrated confidence bound. |
| Pose/raw age | 0.20 s; future pose tolerance 0.05 s | Final repeated pose age is at most 0.059 s, leaving scheduling margin while bounding prediction. |
| Backend covariance lifetime | 1.0 s | Final backend-age p95 is 0.556–0.736 s. Samples reach 1.103 s and correctly produce invalid map results until fresh data arrives; the lifetime is not extended. Request fresh AMCL no-motion scan updates once age reaches 0.5 s, at most twice per ROS second, including when the initial publication was missed. |
| Startup | stable offset for 0.10 s within 0.15 m; within 1.0 m of referee-selected start + raw displacement | Preserves both field starts and permits a zero-offset first fix. A repeat exposed an initially uncertain AMCL basin about 9 m away that later became confident; stability/covariance alone accepted it. The new prior rejects that basin. Startup is exempt from normal step caps. |
| Update trigger | max(0.10 m, 0.5 × predicted std) | A 3-sigma AMCL deadband would hold roughly 0.6–0.9 m error. Measured held-position improvement supports the smaller trigger; it is not a statistical significance test. |
| Post-start jump / step | 1.0 m / 0.30 m | Final delivered target vs observed-held steps reach 0.108 m; unit tests prove jump rejection and bounded convergence. These bounds are not calibrated against kidnapping or high-speed physical faults. |
| Hold / periodic refresh | 0.30 s / 1.0 s | Bounds rate, limits time held between valid fixes and permits recovery from loss without an acknowledgement. Three extra sends recompute fresh absolute positions. |

Prediction uncertainty combines the xy covariance eigenvalue, speed × latency
spread, and yaw variance × squared predicted displacement. UART latency (5 ms),
firmware read delay (2 ms) and spread (3 ms) remain robot timing estimates.
The mapping fallback retains the existing 0.02 m / 0.05 m / 3-sigma policy.
The moving fixture's separate proposed accuracy gate is held-position p95
below 0.35 m. These runs validate the joint policy; they do not isolate the
contribution of each threshold or calibrate AMCL covariance coverage.

## Findings during implementation

- AMCL's zero-spread stationary prior can report covariance near −1e-12 m².
  A narrow 1e-9 roundoff tolerance accepts this; materially negative or
  nonfinite covariance is still rejected.
- Exact lookup of AMCL TF at the current input stamp cannot bootstrap reliably:
  the first transform is future-dated by transform_tolerance. Same-stamp
  backend/local composition removes that timing dependency.
- A parked AMCL backend publishes no further pose unless requested. In a red
  startup diagnostic only 12 inputs (about 0.37 s) were usable before the
  initial covariance expired: the first fix was dropped and there was no
  fresh retry. No-motion scan requests restore a fresh source rather than
  extending covariance lifetime.
- The firmware's shared receive mailbox is a nonstandard loss point; a
  successful Jetson publish is not proof of application. The new metric reads
  actual firmware state, and arrival's nominal estimate documents this limit.
- A replacement run missed the initial backend publication and remained parked
  without a map result. No-motion refresh now also handles a missing backend,
  with an installed-node regression. Another repeat produced an incorrect
  AMCL basin (held-position p95 9.856 m before the startup prior was added).
  A regression feeds that observed wrong position with small covariance and
  proves startup remains unlocalized until a plausible field fix arrives.
  No automatic global reset is introduced; persistent basin failure requires
  source recovery or operator intervention.
- The unchanged EKF fixture failed before and after the relay work because
  truth booted at the loop centre while navigation used the blue team start;
  it also compared raw-zero POSE directly with absolute field truth. The
  original launch reproduced 4.251 m fused mean error. The repaired fixture
  uses its known spawn for seeding and raw translation; the existing positive
  improvement gate then measures both estimators in the same field frame.
- Exploratory runs exposed an occasional PING round-trip over the existing
  100 ms gate and Gazebo teardown requiring SIGTERM/SIGKILL. Gates and baselines
  were not relaxed; affected cases are excluded from trusted accuracy results
  and retained in the evidence archive.

## Validation and open decisions

The user approved the gate values below on 2026-11-12. The current low-speed
simulation does not establish doorway clearance, high-speed physical
relocalization, robot UART timing, or behavior after a sustained >1 m global
jump. Large jumps remain rejected until a plausible source returns or an
operator recovers localization. Package CI dependency pins must be refreshed
as part of coordinated integration before promotion; draft branches do not
change nightly.

The final combined package test run reports **740 tests, zero errors/failures,
14 existing skips**. Firmware separately passed 92 unit tests, 45 hosted
regressions and three handshake tests. All six packages and the workspace pass
the host Python 3.12 quality checker and `actionlint -shellcheck=""`; no baseline
was expanded. Changed local Markdown links/anchors were checked.

The full AMCL/rf2o localization/drift suite passed its existing gates and native
checker. With the fixture frame repair, the EKF ground-truth test passed over
24 legs: raw mean/RMS/max **0.2354/0.2588/0.4852 m**, fused
**0.0618/0.0619/0.0658 m**, mean improvement **73.7%**. EKF displacement direction
error averaged 0.1 degrees, maximum 0.2 degrees.

The final hosted parked cell used the normal scoring duration and passed:
**250/252 shots hit**, **16,188 lockstep holds**, **zero timeouts**, no latest-TF
fallback. The earlier five-second diagnostic missed its only shot and failed
the unchanged hit-rate gate. Neither result implies a full combat-grid pass.

The final six-case both-team run passed all startup, first-fix-drop, moving and
blank-mapping cases with native log checks. The remaining repeated moving
measurements and artifact identity are listed below.

## Resume audit — 2026-11-12

The failure fixes and six package draft PRs already existed when this task
resumed. No further runtime change was needed. The continuation verified the
failure artifacts, completed executable-identified baseline measurements,
reran host checks, recorded this evidence and published the workspace draft.

The failed `replacement` run has `backend=0` throughout: a missed initial
AMCL publication left no source to refresh. Localization commit `a57f186`
extends no-motion requests to that missing-source case, and its installed-node
test observes the request before publishing any backend pose. The failed
`replacement-2` run accepted a wrong AMCL basin despite small covariance;
held-position RMS/p95/max was **8.841/9.856/9.990 m**. Relay commit `2aace64`
adds the referee-start plausibility prior and a regression with that wrong
position. The three final repeats follow both fixes; earlier successful runs
are not substituted for these repeats.

Both final startup cases drop exactly one fix, recover through a fresh retry,
and preserve the overridden red/blue starts. At a field goal equal to the
accepted fix, actual firmware commanded speed was **0.00141/0.00138 m/s**.
Both blank-map cases publish map `(0, 0)` and hold actual firmware positions
within 0.001 m of their field starts. The supplied baseline archive's four
startup/mapping cases also pass their native checkers; it predates the actual
firmware-position readout in the mapping assertion.

All seven repositories pass the host Python **3.12.14** quality checker with
the pinned requirements and `actionlint -shellcheck=""`. Package repositories
use the workspace checker from their own working directories. Their workflows
currently target PRs into `main`, so the package drafts into `nightly` have no
GitHub checks scheduled; local results above are the validation evidence.

## Final moving comparison

Actual firmware-held position versus current truth, metres. Each cell gives
**RMS / p95 / max**; every case dropped one startup fix and passed its native
log checker. Before uses the rebuilt baseline overlay; after uses the final
package heads listed in the [artifact manifest](absolute-relocalize-2026-11-11-artifacts.json).

| Team | Repeat | Before | After |
| --- | --- | --- | --- |
| Red | 1 | 0.3074 / 0.5543 / 0.5840 | 0.0845 / 0.1377 / 0.1501 |
| Red | 2 | 0.3083 / 0.5563 / 0.5876 | 0.0875 / 0.1413 / 0.1534 |
| Red | 3 | 0.3080 / 0.5560 / 0.5874 | 0.0879 / 0.1624 / 0.1729 |
| Blue | 1 | 0.2954 / 0.5388 / 0.5548 | 0.0848 / 0.1612 / 0.1961 |
| Blue | 2 | 0.2871 / 0.5296 / 0.5470 | 0.0935 / 0.1628 / 0.1982 |
| Blue | 3 | 0.2501 / 0.4440 / 0.4773 | 0.0831 / 0.1612 / 0.1787 |

Sample-weighted RMS falls **0.3079 → 0.0867 m (71.9%)** for red and
**0.2782 → 0.0873 m (68.6%)** for blue. These are pooled RMS values, not an
average of percentiles. Per-run p95 stays below the proposed 0.35 m accuracy
gate. Before delivers 3–5 fixes per case; after delivers 23–27, including fresh
retries. The [measurement CSV](absolute-relocalize-2026-11-11-measurements.csv)
retains sample counts, local/global errors, uncertainty, age and target-step
measurements at full precision.

The raw archive is retained in this worktree at
`log/absolute-amcl/evidence.tar.gz` (ignored build/evidence output, not a Git
object). SHA-256:
`c07357dfc54142ef0c11341ff59e5ede50353d05670cc33bee1f2571eef560b0`.
It includes the failed exploratory runs, three inherited before runs, three
new baseline repeats, final repeats, startup/mapping traces, lockstep traces,
suite logs, CTest XML, source snapshots and runtime identities. The manifest
records its byte size and the relevant executable/source hashes. The original
startup baseline archive is included unchanged.

The task-owned `isaac-agent-absolute-amcl` container and its build/install/log
volumes are removed after archiving. With no other container running, its
cleanup helper also stops Colima. Nothing was merged or pushed to `nightly`.

## Draft review stack

Package changes are pushed before their workspace gitlink bump:

- [Firmware hosted readout](https://github.com/Thornbots/MCBV3/pull/139)
- [Absolute localization adapter](https://github.com/Thornbots/sentry_localization/pull/48)
- [Relay and startup prior](https://github.com/Thornbots/thornbots_pkg/pull/74)
- [Held-position arrival](https://github.com/Thornbots/nav_pkg/pull/5)
- [Simulation metric and fixture frames](https://github.com/Thornbots/sim/pull/101)
- [UART contract](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/45)
