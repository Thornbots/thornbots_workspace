# Field-day operator safety rehearsal — 2026-10-22

Both real team starts passed the revised SLAM snapshot → field registration →
AMCL operator workflow after full simulator restarts. These are partial
start-area maps, not full-field coverage or hardware validation. The maintained
procedure is the [operator card](../../thornbots_pkg/README.md#field-day-and-room-workflow).

## Changes and checks

[sentry_localization e8e80cd](https://github.com/Thornbots/sentry_localization/commit/e8e80cd)
removes hand-entered navigation seeds, waits for fresh raw odometry before EKF
startup, validates team/sign/heading against boot/referee evidence, and ties boot,
save and registration to one live session ID. Explicit saves require returning
within 0.15 m/0.15 rad of boot. Autosaves use a separate backup directory; unsaved
stops warn. The session is portable as one directory. Localization runs check and
parked convergence automatically and prints a final verdict. Timeout diagnostics
include observed/expected pose and identify missing TF. The yaw guard rejects
degrees while accepting negative scientific notation and float32 noise at π.

[thornbots_pkg 71a5a19](https://github.com/Thornbots/thornbots_pkg/commit/71a5a19)
forwards safe seeding and backup paths and clarifies the AMCL y default. No tuning,
firmware, route, movement implementation or odometry-input research changed.

Host Python 3.12 dedicated tests: **48 passed**. Registered package tests:
**233 passed, zero errors/failures/skips**. Both changed packages and the workspace
passed repository quality checks and actionlint; extensionless Python helpers
also passed explicit Ruff. The wall-coordinate test checks occupied raster cell
positions after nonzero registration. Negative cases cover team, sign, heading,
degrees, seed mismatch, stale session/boot pose and scientific notation. Failed
localization is tested to stop its owned process without printing PASS.

## Reproduction and evidence

Host evidence is `~/ros2_ws/operator-safety-evidence-20261022/` on the Mac mini.
`rehearse.py`, `resume_blue.py`, `team_adapter.py`, `parked_harness.py`, JSONL,
boot records, maps, registration manifests and logs retain commands and inputs.
The source was this PR's workspace worktree. The owned container was
`isaac-agent-operator-safety-20261022`, ROS domain 121, partition
`agent-operator-safety-20261022-121`, capped at 6 CPUs/12 GiB. Build used the
existing `thornbots-mac` image and the container's isolated build/install volumes;
smoke confirmed package resolution to the live overlay. The container and volumes
were removed. Colima remained running because another agent's containers were up.

Red spawned at (-4.625, 0, 0); blue at (4.625, 0, π). A test-only adapter added
(+0.12, -0.08) m to raw pose and supplied each referee team, ensuring nonzero
registration without changing firmware or movement. The real-field sim used
headless Gazebo, sentry_v2 and real-time factor 1. Raw odometry supplied mapping;
default rf2o/EKF supplied AMCL relaunch. The blue live EKF `initial_state` began
at (4.7449998856, -0.0799999982), matching raw odometry, not the surveyed field pose.

Each map used an existing-controls circuit from the team start through
(sign×5.1, 0), (sign×5.1, 1), (sign×4.625, 1), then back to boot, followed by a
35-second parked head slew. No teleport/reset, firmware or production route
changes were used. Explicit save and field alignment passed. The transforms
were approximately (-0.12010, 0.07976, 0.0000188) for red and
(-0.11991, 0.08022, 0.0000181) for blue. Separate `backup/` directories contained
PGM/YAML plus serialized posegraph/data. Full sim restarts preceded localization.
Both automatic `LOCALIZE PASS` verdicts preceded scoring.

The existing parked harness scores `map->root` at ground-truth capture stamps,
retaining missing TF samples in the denominator. Readiness discovers TF, then
settles three sim seconds. Untrimmed 30-second intervals must have >=95% coverage,
p95 <=0.15 m, max <=0.20 m, head travel >=1.5 rad and chassis motion <=0.03 m.

| Team | TF coverage | p95 error | Max error | Head travel | Chassis displacement |
| --- | --- | --- | --- | --- | --- |
| Red | 300/300 | 0.009064 m | 0.009317 m | 2.00033 rad | 0.000369 m |
| Blue | 300/300 | 0.025796 m | 0.028868 m | 2.00035 rad | 0.000369 m |

The native bench-log checker accepted both teams. Blue mapping teardown included
Gazebo parameter-bridge exit -6 notes; these were shutdown notes, not runtime
accuracy failures. The final process check found no owned sim/localization
processes before container removal. A separate SIGTERM run emitted the unsaved
warning and backup path; its ad-hoc assertion initially raced ros2-run's exit
before the child flushed the warning, which is present in `unsaved-stop.log`.

## Failed attempts and limits

- A stationary-only red map left the start cell unknown. Alignment correctly
  refused it. The subsequent small mapping circuit observed the start cell;
  the occupancy gate was not weakened. Failed artifacts remain in `red-session/`.
- An intermediate evidence harness applied parked localization accuracy gates
  to the deliberately offset, unregistered mapping frame and stopped. Mapping
  metrics are diagnostic; only the registered AMCL runs above claim accuracy.
- Blue alignment exposed float32 π just above double π. The guard now permits
  1e-6 rad serialization noise, with a dedicated regression test, while still
  rejecting degrees. Blue resumed from its validated saved snapshot.
- Real hardware, lidar stream consistency, surveyed extrinsics, slip, terrain,
  full-field coverage and broad-field SLAM divergence remain outside this run.
  No autonomous movement/firmware changes or physical-robot runs occurred.
