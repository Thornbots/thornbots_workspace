# T30: localization startup, 2026-10-15–17

Status: PRs remain draft pending full drift acceptance. The orchestrator accepted
drive non-regression: both pooled cohorts have eleven misses and the ranking
reverses between cohorts. The clock follow-up identifies a blocked Fast DDS SHM
publication in the global clock bridge and removes that transport path. See
[clock follow-up](#clock-transport-follow-up-2026-10-17) for current evidence.
Package changes: [localization #9](https://github.com/Thornbots/sentry_localization/pull/9)
and [sim #26](https://github.com/Thornbots/sim/pull/26).

## Revisions and isolation

The controlled baseline is workspace `3b5a8ca2e93205fd86e21063d1657f2d7de93d0f`:

| Package | Baseline |
| --- | --- |
| sentry_localization | `955bfda27c5afc3e8cb1b2b3dfaa7f4d690f948c` |
| sim | `a769930ac0bc2503e1b22d8fef760b7cee41a316` |
| thornbots_pkg | `e54361a512fdc2e53ae0248a2c219e68c6705342` |
| MCBV3 | `ad13759007491ebfb666c5e8c93087882922d9c3` |

The after cohort uses the same robot/firmware and T30's localization/sim changes.
The final sim branch also retains the newer nightly Track G commit, whose changes
are documentation and estimation-launch trial controls, outside these stages.
The workspace integration preserves newer nightly gitlinks, including Track G's
robot-package pin; those later dependency changes are not the controlled baseline.

Runs used a separate clone and `thornbots_t30_20261015`, the existing Mac image,
ROS domain 130, a 2 GiB private shared-memory mount, and the checkout's own overlay.
The image had Nav2 1.3.13 and rmw_fastrtps_cpp 8.4.4. The VM has ten CPUs and 24 GiB;
the host has twelve CPUs. Track A ran concurrently in its existing container.
The one-minute VM load sampled by the hosted startup probes ranged 2.16–7.35
before and 2.67–7.16 after. Wall timings include the existing eight-second sim
head start. Colima's socket forwarding stalled repeatedly; no shared VM,
container or forward was restarted. A separate task-owned forward was used.

## Observed failure and cause

The first scored hosted `mcb_drive` run failed startup. Its `stack.log` records:

| Event | Wall timestamp in log |
| --- | --- |
| Map image load begins | `1792102307.673679984` |
| Map image read completes | `1792102307.676685874` |
| AMCL configure begins | `1792102307.684123783` |
| AMCL subscribes to map | `1792102307.696978635` |
| AMCL cannot send configure response | `1792102307.802687546` |

Map reading took 3.0 ms. AMCL reached its last initialization log in 12.9 ms,
then reported that the client would not receive its `/amcl/change_state` response.
The manager never activated the nodes; E2E exhausted its existing 30-second
map-to-root wait. This is the same service-response failure class as the reported
map_server stall, reproduced here at AMCL.

The [matching RMW source](https://github.com/ros2/rmw_fastrtps/blob/8.4.4/rmw_fastrtps_shared_cpp/src/rmw_response.cpp#L116-L141)
waits for the service response writer to discover the client's response reader.
It returns a timeout without sending the response when that reader has not
matched by the writer's blocking deadline. Discovery of the request direction
does not establish readiness of the response direction. The observed error came
105.7 ms after AMCL's final initialization log, not after slow map I/O.

A rejected dynamic-composition trial reproduced the same error on
`/localization_container/_container/load_node`: 1/20 startup failures. That failed
trial already had `odom->root` at 9.95 s and `nav_odom->odom` at 9.98 s, but no
active backend or map transform by 40 s. Moving the race to another remote
startup service was insufficient.

Raw `root` was present in every before/after hosted startup probe, including
the rejected trial's failed startup. Current nightly's `pose_translator` emits
raw odometry; `odom_tf_broadcaster` owns its TF. The harness's complete
`map->root` lookup conflated missing backend activation with missing raw TF.
No persistent raw-root omission was reproduced, and no replacement or fallback
TF publisher was added.

## Fix

The [localization owner](../sentry_localization/README.md#launchlocalizationlaunchpy)
now directly constructs and links each backend with its lifecycle manager in one
C++ process, with a separate executor per node. Backend nodes exist before the
manager starts. Lifecycle service endpoints share a DDS participant, and startup
has no remote component-loading RPC. Node names, YAML scopes, initial pose and
existing deadlines are preserved. There are no added retries or timeout changes.

An intermediate local plugin-factory loader had clean startups but reproducible
shutdown SIGSEGVs. It was rejected. The final directly linked backend has zero
abnormal shutdowns across its smoke run and twenty startup trials.

The [sim harness](../sim/README.md#more-on-the-tests) now fails a shared-sim robot
startup after its existing single 30-second wait. It no longer restarts that
robot to rescue the case. Drift and E2E errors distinguish the raw, navigation
and map links. The old automatic retry masked a broken startup and was not an
acceptable reliability mechanism.

## Original startup counts

Counts are failures/attempts; no automatic stage reruns are included.

| Series | Nightly | Final fix |
| --- | --- | --- |
| Hosted drive startup-only, fresh launch each time | 0/20 | 0/20 |
| Full scored stage launches, including initial reproduction | 1/10 | 0/9 |
| Drift scenario startup failures (single attempt each) | 0/9 | 0/9 |
| Abnormal final backend shutdowns in startup-only series | n/a | 0/20 |

The startup-only probe waits for lifecycle activation and all three TF links,
then stops its own process group. These are diagnostic launch trials, not scored
accuracy samples. Activation was 9.17–10.34 s before and 8.79–9.66 s after.
These small cohorts do not establish a statistical failure-rate reduction: the
full drive failure and the rejected remote-loader failure provide direct fault
evidence, while the final batch verifies the new path.
A lighter synthetic-clock/pose probe also had 0/20 failures before the fix and
did not reproduce the fault. An early observer that could consume queued TF or
miss its own get-state response was discarded and is excluded from these counts.

## Original scored stages

All default parked cells and default drive/match durations are retained. Counts
are the harness's scored physical MCB hits/shots (`scores.jsonl`, and match
segment summaries); ghost, requested-shot and unscored boundary events are excluded.

| Hosted stage | Nightly runs 1 / 2 / 3 | Final runs 1 / 2 / 3 |
| --- | --- | --- |
| mcb_parked | 359/428; 351/428; 354/415 | 359/429; 366/432; 366/422 |
| mcb_drive | 31/32; 30/32; 29/31 | 31/32; 30/31; 25/31 |
| mcb_match | 20/37; 20/36; 20/37 | 20/35; 20/37; 20/36 |

All nine scheduled stage runs in each cohort passed GTest and the native log checker.
There were zero lockstep timeouts. Aggregates were parked 1064/1271 to 1091/1283,
drive 90/95 to 86/94, and match 60/110 to 60/108. The drive decline means the
requested per-stage non-regression gate is **not established**. No extra scored
repeats replace these results. Concurrent load reached a one-minute VM average
of 18.81 during the after drive cohort; this confounds timing and does not
justify dismissing the accuracy decline.
The initial failed drive reproduction is retained separately and has no scored
accuracy sample. Every scored run must pass the native checker before its
numbers are accepted.

## Drift, checks and remaining validation

Nightly drift completed 8/9 scenarios, with no startup retry. `moving_obstacles`
failed accuracy at 2.6547 m against 0.4 m; its whole-run checker rejected that
run, so it is diagnostic evidence rather than accepted accuracy evidence.
After drift also completed 8/9 scenarios without startup failure or retry.
`moving_obstacles` passed; `scan_degraded` instead crossed its 0.5000 m limit
at 0.5012 m. This whole-run checker also rejected accuracy acceptance. All three alternating focused control repeats and all three fixed repeats
passed their native checkers. During-degradation maxima were 0.4539/0.4677/0.4576 m
for control and 0.4002/0.3881/0.4386 m for fixed. These diagnostic repeats
do not replace the failed full-suite result. No threshold or covariance was changed. Mapping baseline startup and the on-demand
EKF suite both passed their native checkers. Mapping had zero map drift over
ten simulated seconds; no backend shutdown fault occurred. An existing
parameter_bridge exit -6 appeared during EKF sim teardown and was accepted by
the native checker; it is not a clean whole-stack teardown claim.

The first manually dispatched sim portable CI build exposed a stale dependency
workspace pin: it supplied a pre-`patrol` CVTarget message to the existing current
wire-contract test. Both changed packages now pin current nightly `63a2453` for
CI dependencies. The test and message contract were retained. Fresh portable
ROS CI passed for [localization](https://github.com/Thornbots/sentry_localization/actions/runs/38897508783)
and [sim](https://github.com/Thornbots/sim/actions/runs/38897515514).
Final package heads are `6822eeb28ee65400befe064541ad3a508e40eb8b` and
`d58b1b5933a7dab5840fbc42afe9baa44fa12472`, respectively.

Host Python 3.12 quality checks and actionlint pass in both packages without
baseline changes. Registered colcon tests report 237 tests, zero errors,
failures or skips. Workspace PR policy, quality and both host-helper jobs pass;
nightly policy skips the GPU/image jobs. No GPU or board-firmware execution
acceptance is claimed.

At original closeout, drive non-regression and full drift acceptance remained
open. The follow-up below reports the additional comparisons and current blockers.
No thresholds, baselines, tuning or UART compatibility were relaxed.
No physical robot work was performed. Existing Gazebo/bridge teardown failures
remain outside this startup change and are tracked separately in track E.

## Evidence retention

Original raw logs, probe results, scored JSON and runner scripts remain in
`/Users/blaise/ros2_t30_evidence_20261016.tar.gz`. Follow-up logs, per-second
VM/host load, shot analysis, CI-head verification and cleanup records are in
`/Users/blaise/ros2_t30_followup_evidence_20261016.tar.gz`. The latter includes
the original six drive runs needed to reproduce pooling; rejected experiments
remain labeled in the original archive and are excluded from acceptance counts.

The original T30 container could not be deleted at the first closeout because
shared Colima was stopped. During the follow-up, Track A started that shared VM
externally. Both `thornbots_t30_20261015` and `thornbots_t30_followup_20261016`
were then removed and verified absent through their respective Docker daemons.
The private `t30-followup` VM was stopped and deleted. Shared Colima and Track A
containers were not stopped or restarted. Task-owned clones and the host venv
are removed after publication.

## Alternating follow-up, 2026-10-16

An additional three hosted drive runs per side ran in the order nightly/fixed,
nightly/fixed, nightly/fixed. The control is the captured nightly localization
launch at `955bfda`; the fixed launch is `6822eeb`. Both use the same built
T30 sim harness (`d58b1b5`), robot (`e54361a`) and firmware (`ad13759`) as the
original controlled comparison. The sim runtime/scoring is unchanged; its
readiness diagnostics and no-retry harness are shared. Each run starts a fresh
stack. No scored attempt was discarded or replaced.

The shared default Colima VM was stopped at setup. A separate task-owned
`t30-followup` VM (10 CPUs, 24 GiB) and `thornbots_t30_followup_20261016` container
used the same host, 2 GiB shared memory, ROS domain 137 and the checkout overlay.
A fresh `ros:jazzy-ros-base` container received the manifest dependencies; Nav2
1.3.13 and rmw_fastrtps_cpp 8.4.4 match the original cohort. The image digest and
all installed package versions are archived. No image was built.

Each new drive run waited for private-VM one-minute load to fall to 3 or below
(up to 180 seconds), then sampled load every second. Track A started the shared
VM and its containers externally during the first nightly run. They were not
stopped or restarted. Host load was also sampled from the end of that first
run onward. Consequently this is a paired comparison under concurrent load,
not a claim of identical CPU scheduling or an exact replay of the first cohort.
Pooled six-run counts below are descriptive across both environments.

| New run | Nightly hits/shots | VM load start / max | Fixed hits/shots | VM load start / max |
| --- | --- | --- | --- | --- |
| 4 | 29/33 | 2.93 / 5.13 | 31/32 | 2.91 / 4.11 |
| 5 | 30/30 | 2.94 / 5.04 | 31/31 | 2.76 / 4.20 |
| 6 | 30/32 | 2.77 / 5.82 | 28/30 | 2.98 / 5.17 |

| Cohort | Nightly hits/shots | Fixed hits/shots |
| --- | --- | --- |
| Original three | 90/95 (94.74%) | 86/94 (91.49%) |
| New alternating three | 89/95 (93.68%) | 90/93 (96.77%) |
| Pooled six | **179/190 (94.21%)** | **176/187 (94.12%)** |

All six new runs passed GTest and native log checks, with zero lifecycle
response failures and zero lockstep timeouts. Both pooled sides have eleven
misses; the fix issued three fewer scored shots. The new cohort favors the fix,
but its pooled hit rate is still 0.09 percentage points lower. The literal
non-regression gate therefore remains unmet; these samples do not establish
statistical equivalence. No further repeats replace the low runs.

### Inspection of the low drive runs

The original fixed run 3 (25/31) had zero invalid tracks at issued-shot times,
a maximum tracker age of 47 ms and one normal tracker reseed. Its six misses
were 0.0708–0.0934 m, with head TF attitude errors 0.071–2.126 degrees. The
native diagnostic flags head-pitch attitude error, not a startup failure.
Its first shot was 7.444 s after the first scored route sample; other original
fixed runs began at 7.594–7.644 s. No lost-track or lockstep-timeout evidence
explains the six misses.

New nightly run 4 was also low (29/33), with valid tracks at every shot, one
reseed, tracker age at most 55 ms and head TF errors of 1.16–2.63 degrees on
its misses. New fixed run 6 (28/30) had valid tracks at every shot and tracker
age at most 47 ms; its two misses have 1.07/2.76 degree head TF error. It has
three shot gaps above 0.8 s (maximum 1.170 s). Such gaps are not unique to the
fix: the perfect nightly run 5 (30/30) has two (maximum 1.028 s). No new drive
run fired with an invalid track. In the three low runs above, invalid route
samples all precede the first physical shot; none occur after firing begins.
Detailed shot records and gaps are archived
in `followup-summary.json`.

Activation from the first ROS log was 8.67–9.35 s nightly and 8.39–8.92 s fixed,
including the existing sim head start. Scored-stage starting sim time varies
in both directions across the paired runs; first-shot delays overlap. Static
composition plausibly changes message scheduling and initial scan/physics phase,
so an indirect timing effect cannot be ruled out. However, the reversed ranking
in the new cohort, ordinary head-attitude misses on both sides and absence of
a track-loss/startup pattern do not support a systematic accuracy regression
caused by the localization change. That inference does not waive the numerical
gate.

### Back-to-back full drift and disposition

The full drift suites ran back to back without an intervening test, tuning
change or automatic startup retry:

| Backend path | Native full-suite result | scan_degraded before / during / after error |
| --- | --- | --- |
| Nightly | **9/9 pass**, native checker accepted | 0.1813 / 0.4028 / 0.1976 m; pass |
| Fixed | **8/9 pass**, native checker rejected | Not measured: startup failed after 30 seconds |

The fixed run passed its first eight scenarios. At `scan_degraded`, raw
`odom->root` was ready, while `nav_odom->odom` and `map->nav_odom` were missing.
`robot_9.log` shows an additional failure class:

| Event | Wall timestamp |
| --- | --- |
| EKF logs “Waiting for clock to start...” | `1792185334.562353240` |
| Lifecycle manager starts bring-up | `1792185334.587439584` |
| Nav2 logs “Managed nodes are active” | `1792185334.819586273` |
| RF2O receives its first laser scan | `1792185335.668513032` |
| Harness interrupts the failed startup | `1792185364.263000537` |

Nav2 activated in 232 ms, with no lifecycle response timeout. EKF stayed in its
clock-start wait for the entire readiness window. On SIGINT it threw an invalid
rcl context publisher exception and exited -6; that happened after the startup
failure. The static backend exited cleanly. The new logs localize the missing
navigation TF to EKF clock initialization but do not establish whether clock
discovery/delivery, constructor/executor initialization or machine load caused
it. This does not validate the original fixed `scan_degraded` accuracy miss:
the new attempt never reached accuracy scoring.

Private-VM load start/max was 5.17/9.54 for nightly drift and 7.29/12.01 for
fixed drift; simultaneous host load ranges were 7.54–12.57 and 9.09–13.29.
The original lifecycle fault was not reproduced in the follow-up, but the
additional fixed startup failure means whole-stack startup acceptance is still
incomplete. Follow-up drive startup failures were 0/3 per side; drift startup
failures were 0/9 nightly and 1/9 fixed. No failed attempt was retried.

Both package portable ROS runs were verified successful on the unchanged pushed
heads: localization `6822eeb` in run 38897508783 and sim `d58b1b5` in run
38897515514 (linked above). PRs into nightly intentionally skip the reusable ROS
job; these successful manual-dispatch runs include the portable build and tests.
No redundant dispatch was required. Host Python 3.12 quality checks and actionlint
also pass without baseline growth.

**Merge recommendation: hold all three draft PRs.** The pooled drive hit rate
remains numerically lower, although the new cohort favors the fix and the shot
inspection gives no consistent causal regression signal. More decisively, the
fixed full drift rerun exposes an unresolved EKF clock-start bring-up stall.
Investigate that owner path and obtain full-suite acceptance before promotion;
do not add a retry or weaken the accuracy limits. No runtime change was made
in this follow-up, and both package heads remain unchanged.

## Clock transport follow-up, 2026-10-17

The earlier hold recommendation is superseded here. The orchestrator accepted
the pooled drive comparison; the remaining requested gates are two full 9/9
drift suites and three drive confirmations after diagnosing the clock stall.

### Clock wait and transport evidence

The two previously archived nightly drift cohorts logged `Waiting for clock to
start` in all nine scenarios and continued. That message alone is normal during
startup. EKF is still a separate `robot_localization` process with its own ROS
context and clock subscription; the static backend's executors do not spin it.
One hundred fresh EKF starts with a plain clock publisher and one hundred with
the Gazebo bridge all initialized. An additional 1,000 in-process clock waits
completed. None of these probes reproduced an intrinsic clock-wait wakeup bug.

A full fixed-backend diagnostic reproduced the failure: five scenarios passed,
then four consecutive scenarios failed startup without retries. An independent
observer saw the last `/clock` value freeze at 202.512 s; its clock age grew to
162 s. EKF was blocked in `rclcpp::Clock::wait_until_started`. The clock bridge's
Gazebo callback was blocked in `SharedMemTransport::push_discard`, beneath DDS
publication. Its mutex address `0xf9f3e32f8188` falls inside the mapped interval
`0xf9f3e32f3000–0xf9f3e3300000` for the deleted
`/dev/shm/fastrtps_port41943`. DDS discovery threads were waiting behind the
publisher's locks. This is a blocked global publisher, not an EKF executor
waiting to process an otherwise advancing clock.

The installed Fast DDS 2.14.6 source acquires the port's `empty_cv_mutex` in
[`SharedMemGlobal::Port::try_push`](https://github.com/eProsima/Fast-DDS/blob/v2.14.6/src/cpp/rtps/transport/shared_mem/SharedMemGlobal.hpp#L521).
Deleted mappings identify departed port lifetimes; they do not establish which
process deleted the file or the exact interleaving that stranded the mutex.
The latter was not captured, so this investigation does not attribute deletion
to logind, a suite cleanup script, or another container.

A subsequent full nightly-backend diagnostic passed 9/9, with maximum observer
clock age 0.854 s. Eight scenarios logged the initial clock wait and recovered.
Thus the fatal runtime stall has been captured only with the fixed backend;
it has **not** been reproduced on nightly. The bridge implementation and SHM
transport are unchanged between backends. The backend-free focused comparison
below confirms that nightly already exposes this shared-memory publication
path. Composition can change participant churn and scheduling, but it neither
owns the bridge nor introduces that transport hazard. Treat this as a common
transport vulnerability exposed by the new launch timing, rather than claiming
an observed nightly stall or proving that composition has no timing effect.

### Fix and focused check

Sim commit `fcb998e` pins only the clock bridge to the existing
`thornbots_pkg/config/fastdds_udp_only.xml`. The same node factory serves the
full sim launch and a focused bridge launch; the original process-start event
and two-second robot-spawn delay remain intact. The discovery peers, `/clock`
QoS, Gazebo timestamps, EKF/backend settings, timeouts and no-retry policy are
unchanged. Existing readers can use UDP even when they also enable SHM.

The registered C++ `test_clock_bridge` supplies Gazebo clock messages without a
world or localization backend, creates five fresh ROS contexts in sequence,
requires each clock to start and advance, checks that the bridge maps no
Fast DDS SHM ports, and requires clean shutdown. With the original bridge
transport it receives time but fails the SHM invariant; with the fix it passes.
This checks the removed failure path without relying on a stochastic deadlock.

### Acceptance runs

Runs reuse `thornbots_t30_clock_20261016` on the already-running shared Colima
VM (six CPUs, 8 GiB). The default Docker context has a dead socket; commands use
the `colima` context. Track A and the user's containers are left untouched.
Each run records VM load once per wall second. Host load at confirmation setup
was 8.52 / 5.47 / 3.26; shared-machine load is a timing confounder.

The first full fixed drift suite completed 8/9 with **zero startup failures**.
`scan_degraded` reached scoring; `real_accel` failed the unchanged 0.4 m bound
at 2.4695 m. Its measured chassis yaw was −109.47 to −103.77 degrees rather
than the nominal −90 degrees. This is a scored accuracy failure, not a clock
wait. It is retained and is not replaced by a retry.

| Full fixed drift run | Result | Startup failures | `scan_degraded` truth error before / during / after | VM load start / max |
| --- | --- | --- | --- | --- |
| 1 | 8/9; `real_accel` accuracy failure | 0/9 | 0.2093 / 0.4239 / 0.2568 m | 4.26 / 25.12 |
| 2 | 9/9; native checker passes | 0/9 | 0.2650 / 0.4538 / 0.3091 m | 12.79 / 26.23 |

Both `scan_degraded` cases pass their unchanged 0.4 / 0.5 / 0.4 m limits.
There are no lifecycle-response timeouts or clock-start failures in these
eighteen fixed startups. Two full 9/9 results have **not** been obtained. The
`real_accel` yaw excursion's cause is not established; estimator tuning and
accuracy-floor changes are outside this clock fix.

The clock change can affect drive timing, so three nightly/fixed drive pairs
ran alternately with the same robot `e54361a`, firmware `ad13759`, hosted
backend, lockstep, zero target translation/spin and existing default duration.
The nightly side restores the original localization launch and clock transport;
the sim no-retry harness remains common. Neither source is edited mid-run.

| Drive attempt | Nightly hits/shots | Fixed hits/shots | Nightly VM load start / max | Fixed VM load start / max |
| --- | --- | --- | --- | --- |
| 1 | 30/32 | 26/30 | 23.13 / 23.13 | 17.72 / 19.73 |
| 2 | Startup failure; unscored | 30/32 | 18.71 / 24.40 | 21.23 / 21.23 |
| 3 | 25/29 | 31/34 | 20.16 / 20.16 | 14.89 / 16.87 |

All three fixed runs pass native checks, with zero startup failures and zero
lockstep timeouts. The two scored controls also pass with zero lockstep
timeouts. The unscored control is retained as a startup failure:
AMCL completed configuration but could not send its `/amcl/change_state`
response. That reproduces the original lifecycle fault, not the clock stall.
No replacement attempt was run. Scored totals are nightly 55/61 (90.16%) and
fixed 87/96 (90.63%); these unequal small cohorts provide confirmation, not a
new calibrated accuracy floor. Startup failures are 1/3 nightly and 0/3 fixed.

Final sim head is `6a97660` (the follow-up adds explicit test headers only).
The focused clock test plus registered copyright/flake8/pep257 checks pass:
four tests, zero failures. Host Python 3.12 quality checks and actionlint pass
for sim and workspace with zero new diagnostics and no baseline growth; changed
local documentation paths and the new anchor resolve. The sim PR's lint job is
green. [Portable ROS validation at the implementation commit](https://github.com/Thornbots/sim/actions/runs/39084258551)
is recorded separately from PR lint; PRs into nightly intentionally skip ROS.
Localization code remains at its previously validated `6822eeb`.

**Merge recommendation: keep all three PRs draft.** The clock failure path is
removed and the requested drive confirmations pass, but the required pair of
9/9 full drift results is not met. Investigate `real_accel`'s scored yaw/position
excursion before declaring full acceptance. The exact natural interleaving that
stranded the old SHM mutex, and a fatal clock-stall reproduction on nightly,
remain unproven; the captured transport block and removed SHM path are the
evidence for this narrowly scoped fix.

Raw clock diagnosis, both full drift runs (including the failed one), all six
drive attempts, per-second VM load, focused before/after checks and final test
reports are preserved in
`/Users/blaise/ros2_t30_clock_evidence_20261017.tar.gz`, with a SHA-256 sidecar.
Earlier archives remain separate. Only the T30 clock container and isolated
checkout are cleaned up; shared Colima, Track A and the user's container remain
running.
