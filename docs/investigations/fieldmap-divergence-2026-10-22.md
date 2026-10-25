# Full-field mapping divergence — 2026-10-22

The head-mounted lidar violated slam_toolbox's rigid-mount assumption. Changing
SLAM's tracking base from `root` to `lidar` fixes that localization bug. AMCL
caches the mount position too; the [follow-up](#amcl-moving-mount) refreshes it. A separate
Gazebo VelocityControl artifact sustains chassis tilt and drives the robot into
the air after rough crossings. Continuous planar scan insertion then corrupts
the map. Pausing insertion during transfers and observing from level, parked
stations produced a 48.7 m field map with 97.55% reverse coverage within 0.15 m.
All observed occupied cells were within 0.0465 m of `clean_map`, without a fitted
alignment. Hardware competition readiness is not established by this sim fixture.

The maintained operator instructions are
[broad-field coverage](../../sentry_localization/README.md#broad-field-coverage).
This follows the [original field-day rehearsal](fieldday-slam-amcl-2026-10-22.md),
whose broad failures did not isolate the cause. No robot movement, firmware,
production route, noise model, matcher search threshold or accuracy gate changed.

## Reproduction

Evidence on the Mac mini: `~/ros2_ws/fieldmap-divergence-evidence-20261022/`.
`HARNESS.md` and `experiment.py` retain commands, routes, lifecycle and parameters.
`localize_existing.py` compares AMCL inputs against an unchanged saved map.
JSONL retains truth quaternions, stamped map/root pose, raw/navigation displacement,
head motion, commands, pause toggles and station readiness. Rosbags retain scans,
TF, full truth and odometry. `analyze.py`, `scan_geometry.py` and
`flight_analysis.py` derive diagnostics; failures are retained.

Verified initial heads: workspace #90 `173776c`, sentry_localization #16
`50e8eb9`, thornbots_pkg #24 `e4e0fcd`; sim `c5aa4ba` and rf2o `ddb64de`.
The isolated container was `isaac-agent-fieldmap-divergence`, ROS domain 115,
Gazebo partition `agent-fieldmap-divergence-115`, on the mini's existing arm64
image with six VM CPUs. Gazebo was 8.15.0 and slam_toolbox was
`2.8.5-1noble.20260907.044142`. Overlay resolution was checked by `smoke.sh`.
Every experiment uses a fresh sim; its process groups are stopped in `finally`.

Raw odometry in this zero-slip, zero-noise fixture is derived from truth planar
position. Truth is used only to steer the evidence teleop route, check clearance,
register surveyed boot pose and score localization. It is never a localization
input. This isolates scan/backend errors; it does not validate hardware wheels.

## Moving-mount failure

slam_toolbox 2.8.5's
[`getLaser()`](https://github.com/SteveMacenski/slam_toolbox/blob/2.8.5/src/slam_toolbox_common.cpp#L625)
caches a laser by scan frame. Its
[`LaserAssistant`](https://github.com/SteveMacenski/slam_toolbox/blob/2.8.5/src/laser_utils.cpp)
sets one offset pose relative to the configured base. Our `root->lidar` transform
changes with the head, including the approximately 0.22 m horizontal lever arm.
Using a cached offset relative to `root` is incompatible with that mounting.
Refreshing TF alone does not refresh Karto's stored laser offset.

Controlled comparison: same 8.956 m central circuit, 0.30 m/s, raw odometry,
head sweeping approximately ±1 rad, unchanged matcher settings. Only the SLAM
base changed. The root-base run had truth roll/pitch below 0.002 rad, root yaw
below 0.0012 rad, and raw/navigation position error below 41 nm. It nevertheless
invented 0.583 rad of map-root yaw and reached 0.946 m position error.

| Run | SLAM base | Position p95 / max | Observed cells within 0.15 m | Reverse coverage |
| --- | --- | --- | --- | --- |
| `central-root-sweep-r2` | root | 0.7351 / 0.9459 m | 37.56% | 68.37% |
| `central-lidar-sweep` | lidar | 0.01154 / 0.01553 m | 100% | 69.64% |

With `base_frame: lidar`, the cached scan offset is identity. Each stamped
`nav_odom->lidar` lookup instead carries head translation and yaw. SLAM still
publishes `map->nav_odom`; the public pose, AMCL and rf2o retain the root frame.
The angular travel threshold now measures lidar/head rotation. Physical tilt
and height absent from the planar TF tree remain uncorrected.

This bug is hardware-relevant: deliberate head slew alone reproduced it on
flat ground. It is not explained by simulated wheel slip or the raised regions.

## Terrain and the artificial climb

`broad-lidar-raw` completed 48.565 m with the frame fix. Unlike the original
root-base broad failures, it recovered after crossings, but continuous insertion
still produced 0.4608 m p95 / 1.1013 m max mapping error and spurious map cells.
Truth reached z=0.6091 m, roll=0.7106 rad and pitch=0.1652 rad. Its raw/navigation
position stayed within 0.265 micrometres of truth, ruling out wheel-position
drift as the cause of that mapping error. All 2,410 recorded scans had 720 beams,
one angular increment and an endpoint consistency error below 0.4 microradians.
This is distinct from the malformed Oct 18 hardware scan stream.

The sustained climb is a simulator movement artifact. Gazebo 8.15.0
[`VelocityControl`](https://github.com/gazebosim/gz-sim/blob/gz-sim8_8.15.0/src/systems/velocity_control/VelocityControl.cc#L200)
sets linear and angular velocity every update. The
[`Physics` system](https://github.com/gazebosim/gz-sim/blob/gz-sim8_8.15.0/src/systems/physics/Physics.cc#L3054)
rotates the body command through the full chassis orientation. Zero commanded
body z therefore gives nonzero world z when tilted. Zero angular command holds
the acquired tilt; repeated velocity resets also prevent gravity accumulating.

At truth t=194–204 s, the robot moved up the west side lane while its chassis
remained rolled about 0.1394 rad. Across all 100 capture intervals:

- Mean vertical component of the rotated planar command: **0.0410640 m/s**.
- Observed mean climb: **0.0312642 m/s**.
- Subtracting one 1 ms gravity step, 0.0098 m/s, predicts the measured vertical
  speed with **0.00000436 m/s RMS residual**.

The root rose from about 0.23 to 0.48 m along that lane while field clearance
remained over 1 m. This is powered free-space motion from the velocity fixture,
not evidence that hardware would climb that trajectory. Stopping removes the
commanded vertical component, but this fixture then falls only about 1 cm/s.
Lowering the mapping speed to 0.15 m/s did not solve it: `broad-lidar-slow`
still lifted and eventually failed the unchanged no-progress guard.

Tilted scans can hit the floor, and an elevated lidar can see over obstacles
that belong in the nominal-height map. The emulator carries planar position and
yaw but discards chassis roll, pitch and height. Neither base-frame selection
nor a wider search window can turn those rays into the missing horizontal
observations. Correcting this fixture belongs to simulation movement, outside
this task. Real rough-ground scan tilt remains a hardware risk independently.

## Broad map from level stations

`broad-lidar-stationary-r2` used the same broad route and 0.30 m/s limit with
raw input and the lidar base. Before each transfer it paused new measurements.
At each destination it stopped, waited until roll/pitch were below 0.015 rad and
root height was within 0.025 m of its nominal settled height for two seconds,
then resumed insertion for a parked head sweep. These truth-based readiness
checks diagnose the sim; they are not an implemented hardware attitude sensor.
No localization samples were removed or gates changed.

| Mapping method | Truth distance | Mapping p95 / max | Observed cells within 0.15 m | Reverse coverage within 0.15 m |
| --- | --- | --- | --- | --- |
| Continuous, lidar base, raw input | 48.565 m | 0.4608 / 1.1013 m | 93.02% | 96.38% |
| Level stations, lidar base, raw input | 48.712 m | 0.04325 / 0.04325 m | 100% | **97.55%** |

The level-station map has 1,764 occupied cells; observed-to-CAD p95 is 0.03746 m
and max is 0.04648 m. CAD-to-observed p95 is 0.05008 m. Reverse coverage counts
all 10,428 CAD occupied-cell centres. Registration uses the captured surveyed
boot pose, with no ICP, fitted transform or post-hoc cropping. The remaining
2.45% is unobserved coverage, not a relaxed accuracy tolerance.

## AMCL input comparison and limits

AMCL uses a full simulator restart at the captured physical start. Every scored
sample uses `map->root` at truth capture time; missing TF stays in the denominator.
Gates remain TF coverage >=95%, p95<=0.15 m, max<=0.20 m. Parked scoring also
requires chassis displacement<=0.03 m and actual head travel>=1.5 rad; drive
requires >=2 m and return within 0.08 m.

On the identical continuous broad map, default rf2o/EKF AMCL passed parked
scoring (0.03687 m p95, 0.03735 m max) but failed the 21.062 m drive at
2.3884 m p95 / 2.6572 m max. Raw-input AMCL passed parked (0.000362 m p95),
and reduced the same 21.059 m drive to 0.15312 m p95 / 0.16793 m max.
That raw drive still **fails** the 0.15 m p95 gate. Improving the odometry input
does not make the continuously contaminated map a passing result.

The level-station map passed raw-input AMCL parked and drive scoring:

| Run | Duration / truth distance | p95 | Max | Stamped TF coverage |
| --- | --- | --- | --- | --- |
| `stationary-map-amcl-raw-parked` | 30 s, head travel 2.00035 rad | 0.000362 m | 0.000362 m | 300/300 |
| `stationary-map-amcl-raw-drive` | 21.059 m | 0.07529 m | 0.08266 m | 986/986 |

Parked chassis displacement was 0.000371 m; drive return error was 0.03455 m.
The drive extends from the west start through the centre and back, including
rough crossings; it does not visit every mapped side/end station. Passing the
coverage requirement is a map comparison, not an AMCL tour of every field cell.

## Follow-up, 2026-10-23

Evidence: `~/ros2_ws/fieldmap-finish-20261023/` on the Mac mini, container
`isaac-agent-fieldmap-finish` (domain 190), heads sentry_localization `90fd717`
plus this change and workspace `5d9f69d`. The guarded session workflow cannot
load the 2026-10-22 evidence map, so `localize_direct.py` launches
`auto.launch.py` with the arguments `localize` passes, on a fresh sim each run.
The scorer and gates are unchanged. `DRIVE_SWEEP` adds a ±1 rad, 8 s head sweep
to the drive. `PARKED_NOMOTION` requests AMCL updates at 1 Hz while parked,
as `convergence` does.

### AMCL moving mount

nav2_amcl Jazzy has a partial form of the SLAM bug.
[`addNewScanner`](https://github.com/ros-navigation/navigation2/blob/jazzy/nav2_amcl/src/amcl_node.cpp)
stores the `root->lidar` x/y from the first scan (at latest TF) and never
refreshes it; `updateFilter` re-reads only the mount yaw at each scan stamp.
The lidar is 0.22 m from the head axis (`lidarlink` origin), so a head turn of
Δ moves the true sensor origin up to 2·0.22·sin(Δ/2) m from the cached one.

Parked scoring cannot detect this. Without odometry motion AMCL adds no
motion noise, so particles cannot drift: forced parked updates with 2.0 rad of
head travel still scored 0.05 mm p95. Driving can:

| Raw-input AMCL, level-station map, 21.06 m drive | Head travel | p95 | Max | Result |
| --- | --- | --- | --- | --- |
| Cached mount, no sweep (`raw-r2`, `raw-r3`) | 0.11 rad | 0.0712 / 0.0776 m | 0.0846 / 0.0815 m | pass |
| Cached mount, head sweep (`raw-sweepdrive`) | 2.03 rad | 0.1404 m | **0.2048 m** | **fail** |
| Tracked mount, head sweep (`fix-sweepdrive-r1`, `-r2`) | 2.00 rad | 0.0724 / 0.0877 m | 0.0997 / 0.0992 m | pass |
| Tracked mount, no sweep (`fix-raw-r1`, `-r2`) | 0.10 rad | 0.0803 / 0.0794 m | 0.1024 / 0.0982 m | pass |

All have 100% stamped TF coverage and return within 0.035 m. Parked runs with the
tracked mount scored 0.02-0.03 mm p95. The fix is `TrackedMountAmcl` in
`localization_backend`: before AMCL's scan callback it sets the laser pose from
`root->lidar` at the scan stamp. AMCL keeps `root` as its base, so seeds,
`/amcl_pose` and convergence gates are unchanged. Switching AMCL's base to the
lidar or head would also remove the cache error but changes seed yaw semantics.

### Input default

On the same level-station map, with the cached mount:

| Input (`fused-r1`) | Parked p95 / max | Drive p95 / max |
| --- | --- | --- |
| rf2o/EKF | 0.0288 / 0.0305 m | **0.7599 / 1.0881 m** (fail) |
| Raw (`raw-r2`) | 0.00003 m | 0.0712 / 0.0846 m |

rf2o/EKF with the tracked mount and head sweep also failed (0.1342 m p95,
**0.5211 m** max). rf2o's fork already refreshes its mount per scan, so this is
not the cache bug. The workflow now defaults field mapping and localization to
raw wheel input, with `--rf2o` as opt-in. Sim raw odometry is exact, so this
comparison favours raw; on the robot, slip goes uncorrected in `nav_odom` and
is left to SLAM/AMCL. Why rf2o/EKF fails on this route is not yet isolated.

### Mapping pause

`operator_workflow pause|resume SESSION` replaces the hand-run toggle: it
reads `paused_new_measurements`, toggles only when needed and verifies the
parameter afterwards, against the live mapping session.

### Regressions

All with the lidar SLAM base, `TrackedMountAmcl` and the workflow changes.
`run_suite.sh` logs are under `sim_suite_*.log`; each passing suite was
trusted by `check_bench_log`.

- `colcon test --packages-select sentry_localization`: 115 tests, 0 failures.
- `drift` (AMCL backend, rf2o): 9/9 passed; `drift_correction` max change 0.0948 m.
- `ekf`: 1/1 passed.
- `mcb_parked`, hosted firmware build of the pinned, unchanged MCBV3 sources:
  12/12 passed; worst cell p95 0.119 m. This is within the
  [parked odometry spread](#parked-odometry-ab), not a regression.
- `drift backend:=mapping use_rf2o:=false`: **4/9 passed, 5 failed** with the
  lidar base. The same suite with `base_frame: root` restored also failed
  the same five: `drift_correction` 0.4268 vs 0.4476 m,
  `drift_correction_obstacle` 0.4547 vs 0.4350 m, `moving_obstacles` 0.4043 vs
  0.4410 m (root vs lidar, 0.4 m limit), `odom_stuck` 0 m spread in both and
  `scan_degraded` after-error 0.4368 vs 0.4553 m. This is an existing failure,
  not introduced here
  ([why map-based drift is hard](../../sentry_localization/README.md#why-the-map-based-drift-scenarios-are-hard)).
- Live `pause`/`resume` against slam_toolbox in a sim room session: each call
  produced the requested `paused_new_measurements`, repeats left it unchanged,
  and a mismatched session was refused without toggling.

Renode `mcb_parked` was not run: this arm64 image has no ARM GCC. The hosted
backend matches the workspace nightly runner.

### Parked odometry A/B

`mcb_parked` runs AMCL with rf2o/EKF (`sim/launch/e2e.launch.py`), not
slam_toolbox. Nine hosted runs on the Mac mini, three each of: this head
(`2f348c3`); the same with `base_frame: root`; and nightly `b88b4ce`'s
pins (sentry_localization `f3e4514`, thornbots_pkg `4054dd0`, firmware
`5950960`). All passed 12/12. Diagonal cells, p95 m:

| Variant | stationary | speed1 | speed2 | speed4 |
| --- | --- | --- | --- | --- |
| Head, 3 runs | 0.026-0.048 | 0.018-0.063 | 0.025-0.082 | 0.021-0.088 |
| `root` base, 3 runs | 0.034-0.085 | 0.017-0.081 | 0.024-0.092 | 0.022-0.133 |
| `b88b4ce` pins, 3 runs | 0.014-0.060 | 0.023-0.073 | 0.042-0.085 | 0.042-0.102 |
| `b88b4ce` nightly gate, 1 run | 0.022 | 0.020 | 0.038 | 0.042 |

Lateral and radial cells stayed at or below 0.072 m in every variant. The
error is `nav_odom` (rf2o/EKF) drift: AMCL's `map->nav_odom` correction
stayed at or below 0.008 m p95, because parked AMCL never reaches its motion
update thresholds. Odometry is not reset between cells and the diagonal cells
run last, so error grows with elapsed time, not head speed. `b88b4ce`
itself reached 0.102 m; the single gate run was a low draw. This is
[ROADMAP T39](../ROADMAP.md#h-slam-at-amcls-level). Evidence:
`~/ros2_ws/mcb-parked-ab-20261023/SUMMARY.md`.

## Hardware risks

Hardware risks remain fixed scan geometry, true lidar zero/blind sector,
extrinsics, surveyed heading, wheel slip, time synchronization and dynamic
obstacles. Pausing insertion requires enough wheel odometry and overlapping
views to reconnect at the next station. This fixture's exact raw planar input
does not establish that recovery margin on the robot. Filter convergence is
not measured field accuracy. AMCL's
tracked mount depends on accurate, timely head TF; a stale or wrong head angle
now moves the modelled sensor origin. Real rough-ground tilt is unmodelled in
SLAM and AMCL alike.
