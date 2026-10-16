# T30: localization startup, 2026-10-15–16

Status: startup fix validated; final scored repeats and CI are in progress.
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

## Startup counts

Counts are failures/attempts; no automatic stage reruns are included.

| Series | Nightly | Final fix |
| --- | --- | --- |
| Hosted drive startup-only, fresh launch each time | 0/20 | 0/20 |
| Full scored stage launches, including initial reproduction | 1/10 | pending |
| Abnormal final backend shutdowns in startup-only series | n/a | 0/20 |

The startup-only probe waits for lifecycle activation and all three TF links,
then stops its own process group. These are diagnostic launch trials, not scored
accuracy samples. Activation was 9.17–10.34 s before and 8.79–9.66 s after.
A lighter synthetic-clock/pose probe also had 0/20 failures before the fix and
did not reproduce the fault. An early observer that could consume queued TF or
miss its own get-state response was discarded and is excluded from these counts.

## Scored stages

All default parked cells and default drive/match durations are retained. Counts
are physical MCB hits/shots; ghost and requested-shot streams are excluded.

| Hosted stage | Nightly runs 1 / 2 / 3 | Final runs 1 / 2 / 3 |
| --- | --- | --- |
| mcb_parked | 361/432; 354/431; 358/419 | pending |
| mcb_drive | 31/32; 30/32; 29/31 | pending |
| mcb_match | 20/37; 20/36; 20/37 | pending |

All nine scheduled nightly stage runs passed GTest and the native log checker.
The initial failed drive reproduction is retained separately and has no scored
accuracy sample. Every scored run must pass the native checker before its
numbers are accepted.

## Drift, checks and remaining validation

Nightly drift completed 8/9 scenarios, with no startup retry. `moving_obstacles`
failed accuracy at 2.6547 m against 0.4 m; its whole-run checker rejected that
run, so it is diagnostic evidence rather than accepted accuracy evidence.
After drift, mapping startup and the on-demand EKF suite are pending.

Host Python 3.12 quality checks and actionlint pass in both packages without
baseline changes. Registered colcon tests report 237 tests, zero errors,
failures or skips. Package CI and the full scored after cohort are pending.
No physical robot work was performed. Existing Gazebo/bridge teardown failures
remain outside this startup change and are tracked separately in track E.
