# Field-day round-2 operator checks — 2026-10-23

The maintained [operator card](../../thornbots_pkg/README.md#field-day-and-room-workflow)
contains the room, field and explicit practice-field commands. This record covers
the review fixes; it does not establish hardware or full-field accuracy.

## Changes

- Finding 1 shipped first as sentry_localization `90fd717`, integrated by workspace
  `5d9f69d`: room sessions persist `frame_mode: room`, capture `team: null`, and
  save/prepare without referee assignment. Explicit practice-field team selection
  still checks raw odometry against the contract start.
- Findings 2 and 3: field startup checks live team/raw start using only UART input
  and pose translation, then stops that bootstrap before launching the backend.
  There is no command producer or relay during bootstrap. EKF requires a nonzero
  referee assignment followed by a newer raw sample within 0.3 m of the team
  start. Practice mode skips assignment but independently checks its explicit
  team's seed after restart. Alignment defaults x/y to contract starts; surveyed
  refinements over 0.3 m from captured raw odometry fail.
- Findings 4 and 5: automatic convergence uses the standalone 3 s freshness limit.
  Field maps retain registration provenance but initialize AMCL from the live
  team's contract root, checked against live raw odometry.
- Findings 6–8: EKF executes its installed binary directly, seed timeout logs an
  error and shuts down launch, and spontaneous mapping exits warn with the backup
  path. Bootstrap signal cleanup stops the owned process group.

Findings 2–8 are in sentry_localization `a1d96c5`; thornbots_pkg `2f46adb`
adds the guarded input-only bootstrap and forwards the seed options. They retain
the concurrent moving-lidar fix `2f348c3`, raw-wheel defaults and pause/resume
workflow. All three pull requests remain drafts targeting `nightly`.
Follow-up sentry_localization `b23289c` prints `prepare-room` after a room save
and the yaw-only alignment command after a field save.

In AMCL mode, `/localization/odom` comes from raw passthrough by default. With
`--rf2o`, EKF fuses raw velocity/fixed heading and rf2o position into that topic.
AMCL supplies `map->nav_odom`; its correction does not repair an incorrectly
seeded navigation odometry topic consumed by `mcb_relay`.

## Validation and evidence

Evidence is `~/ros2_ws/round2-workflow-evidence-20261023/` on the Mac mini:
scripts, maps, session/boot records, process logs and stamped JSONL scoring.
The owned container was `isaac-agent-round2-workflow`, domain 121, partition
`agent-round2-workflow-121`, capped at 6 CPUs/12 GiB. Smoke verified the live
overlay. A parallel build exhausted memory; rebuilding with two compile jobs
succeeded. No firmware, movement implementation or physical robot changed.
Final process inspection found no owned ROS/Gazebo processes. The container and
its volumes were removed; Colima remained running because another task's
container was active.

Room telemetry came from Gazebo/pose_emulator and a test-only referee adapter
publishing `robot_id: 0`. The complete mapping → boot → manual sim circuit →
save → prepare-room → full sim restart → AMCL sequence printed `LOCALIZE PASS`.
The existing 30 s parked/head-slew scorer retained all samples and thresholds.
The final repeat after integrating the moving-lidar changes passed 300/300
stamped TF samples, p95 0.000239 m, max 0.000239 m, head travel 2.00032 rad and
chassis displacement 0.000369 m. The native bench-log checker accepted the room
and delayed-referee runs.

The late-blue fixture initially supplied zero-ID referee telemetry and red-side
raw coordinates, then assigned blue and supplied blue raw coordinates after
12 wall seconds. Direct seeded launch had no EKF node before assignment and
then seeded near (4.6249, -0.00034), rather than the previous red position.
The operator workflow also passed boot capture and EKF seeding with this delayed
assignment. Direct graph discovery verified bootstrap had no relay, CV command
producers or localization backend. Fixture adapters change telemetry only.

Focused unit tests include zero-ID room/field behavior, explicit practice team,
late-assignment/re-anchor ordering, seed timeout, direct exec, typo rejection,
live blue start on red registration, matching convergence defaults, spontaneous
exit warnings and SIGTERM process cleanup.
After rebasing onto the moving-lidar changes and correcting NEXT prompts, host
tests passed 94 with the two fixture skips below; registered container tests
passed 265 with zero failures,
errors or skips. Both package repository checks, workspace checks, actionlint,
explicit helper Ruff and diff checks passed. No baselines changed.

## Limits and discarded attempts

- The available guarded red deployment map covers only x near the red start;
  blue's x = 4.625 lies outside its 84×163 raster. Cross-team start validation is
  unit-tested; localizing that partial map on blue was skipped. The other mapping
  investigation's broad map predates guarded session provenance; it was not
  relabeled as a validated operator bundle.
- Two host map-fixture tests skip without `FIELD_MAP_WORLD`; registered container
  tests supply the fixture and do not skip them.
- An evidence-script assertion initially compared the literal text `4.625` to a
  real floating-point seed near 4.6249. Its corrected numeric assertion passed.
  Another assertion queried stale ROS CLI daemon entries; final graph checks use
  `--no-daemon` and process inspection. Neither discarded assertion established
  a runtime localization failure.
- The first post-rebase room repeat rejected a stale/non-increasing scan during
  save. That run stopped without a deployment bundle. A fresh full mapping and
  localization repeat passed with the scan gate unchanged.
- Sim convergence and the unchanged parked gates do not validate real lidar
  geometry, surveyed extrinsics, wheel slip or referee behavior on hardware.
