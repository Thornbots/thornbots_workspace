# Field-day SLAM to AMCL rehearsal — 2026-10-22

The operator workflow and a room rehearsal passed. A flat central circuit in the
sim field also passed AMCL accuracy gates after a full sim restart. Broad field
mapping failed with both fused and raw odometry; the successful map has partial
coverage. This is not a claim of competition readiness over the whole field.

The maintained operator procedure is
[sentry_localization's room and field workflow](../../sentry_localization/README.md#field-day-and-room-workflow).
Firmware, production routes, waypoints, odometry constants and drive behavior
were unchanged. Evidence-only teleop inputs exercised existing sim controls.

## Reproduction and artifacts

Host evidence: `~/ros2_ws/fieldday-slam-amcl-evidence-20261022/` on the Mac mini.
`HARNESS.md`, `run_field3.py`, `flat_field_harness.py`, `fieldday_harness.py`,
`compare_maps.py` and JSONL logs retain exact commands and scoring inputs.
The isolated agent container was `isaac-agent-fieldday-20261022`, ROS domain 120,
with its own Gazebo partition, source mount and build/install/log volumes.
Sim used the repository field, sentry_v2, headless Gazebo and real-time factor 1.
The ordinary-room SDF is evidence-only: 8 by 6 m walls plus an asymmetric box.
Room spawn was (-2, 0, 0); the successful field spawn was (0, 0, 0).

Mapping captured the stamped boot root and chassis heading before driving,
saved PGM/YAML plus `.posegraph/.data`, then prepared the occupancy bundle.
Room preparation retained the captured nonzero boot coordinates. Field
registration used simulated surveyed boot truth, not a fit to the reference map.
Each AMCL rehearsal restarted the entire sim at the captured physical start.
Raw wheel passthrough supplied SLAM in both successful runs. Room AMCL used
raw passthrough; field AMCL used the default rf2o/EKF input.

## Results

Scoring uses the existing parked/drift planar error contract and percentile
interpolation. Each localization pose is evaluated at the ground-truth capture
stamp using `map->root`; delayed TF is retried, missing samples remain in the
coverage denominator. Readiness requires TF discovery followed by three sim
seconds of settling before starting the scored interval. Parked acceptance is
coverage >=95%, p95 <=0.15 m, max <=0.20 m, chassis displacement <=0.03 m and
head travel >=1.5 rad. Scored intervals are not trimmed after measurement.

| Run | Distance / duration | p95 error | Max error | TF coverage |
| --- | --- | --- | --- | --- |
| Room parked, head slewing | 30 s | 0.01216 m | 0.01216 m | 300/300 |
| Room short drive | 5.861 m / 21.95 s | 0.02397 m | 0.02413 m | 99.09% |
| Field parked, head slewing | 30 s | 0.01158 m | 0.01172 m | 300/300 |
| Field short drive | 3.461 m / 13.98 s | 0.04034 m | 0.04416 m | 140/140 |

Parked head travel was 2.0003 rad in the room and 2.0004 rad on the field;
chassis displacement was 0.00037 m in each. Both operator convergence checks
reported `CONVERGED`. The room mapping circuit covered 11.826 m; the successful
field circuit covered 8.958 m, with 1.224 m minimum collision-grid clearance.
`field3-*` and `room-*` contain snapshots, registration manifests and scores.

Comparison against `clean_map` used occupied cell centres in YAML world
coordinates, with no ICP or other fitted transform. All 796 observed occupied
cells were within 0.15 m of the CAD reference: median 0.00895 m, p95 0.02942 m,
max 0.04802 m. Reverse coverage was only 60.19% within 0.15 m; reverse p95 was
2.996 m. This demonstrates placement of observed surfaces, not full coverage
or arbitrary-heading field registration on hardware. Rotation, raster sampling
and nonzero boot registration are covered by offline regression tests.

Build and registered tests passed: **201 tests, zero failures/errors/skips**.
Python 3.12 repository quality checks, explicit Ruff on the extensionless CLI,
and actionlint passed. Native sim log checking accepted the successful runs;
Gazebo parameter bridges reported exit -6 during teardown, recorded as shutdown
notes rather than runtime accuracy failures.

## Failures and limits

- The first broad field circuit with rf2o/EKF SLAM input diverged beyond 5.4 m
  and was stopped. The second, raw-input circuit completed about 50 m but
  reached 10.23 m error. Neither map is suitable for deployment. Terrain tilt
  is a suspected contributor: the raw run crossed a raised region with truth
  z around 0.083 m and chassis heading drift. The experiment does not isolate
  the cause. Planar matching, terrain and odometry need further investigation.
- The second run's subsequent alignment command also hit argparse's negative
  scientific-notation parsing (`--yaw -2e-05`); the final harness uses
  `--yaw=VALUE`. It never advanced to AMCL on the bad map.
- The initial room parked score failed 95% TF coverage (90.97%) because scoring
  began before discovery. The failed evidence remains; the explicit readiness
  wait above produced the reported repeat, without removing scored samples.
- Real hardware was not run. The
  [Oct 18 investigation](sentry-nightly-jetson-2026-10-18.md) observed 340–361
  beams and varying angular increments rejected by the localization stack.
  Current lidar configuration enables angle compensation, but its real stream
  remains unvalidated. The workflow rejects inconsistent geometry clearly.
- Wheel slip, surveyed heading, lidar extrinsics, dynamic obstacles and thin
  rasterized features remain real-hardware risks. Visual scan/wall inspection
  and adequate map coverage are mandatory. Filter convergence is not truth.
- Field registration affects localization only. Firmware START_X/Y, raw aim
  coordinates and routes remain the team's responsibility; the operator must
  supply current firmware odometry seeds separately from measured physical
  field pose. No movement or firmware adaptation was attempted.
- Saved graphs are preserved in their original boot frame. Transformed graph
  reload and the existing saved-graph zero-pose startup are not implemented or
  rehearsed. Recovery is remapping, or documented odometry-only operation with
  no map-localization claim. No PR was merged or main promotion performed.
