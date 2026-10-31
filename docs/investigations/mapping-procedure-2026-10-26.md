# Mapping procedure verification — 2026-10-26

The operator procedure was the root README "Map a new field" section,
then mirrored to the Notion mapping doc; it was removed on 2026-10-31 in favor of MMM. This record describes verification,
not robot acceptance. No physical robot runs or behavior changes were made.

## Source audit

Base workspace `d0fd482`; sentry_localization `496e09f`, thornbots_pkg and startup
at that workspace's pins. Audited `scripts/operator_workflow`, localization and
robot launch declarations, `thornbots-launch.sh`, `thornbots-start.sh`,
`thornbots.service` and `launch.env`. Read startup draft #10 and localization
draft #19 diffs; retain mapping boot default and the explicit host stop command.
Boot options were independently cross-checked against these same sources.

- Operator mapping/localize default to raw passthrough. Hardware `auto.launch.py`
  defaults to mapping with rf2o/EKF; these are different defaults.
- Deployment uses `deployment/field` without extension; AMCL loads its YAML.
  Blue chassis registration uses pi, but AMCL root yaw is zero for both teams.
- Raw boot has no equivalent to the workflow's referee/start gate. EKF seed
  flags have no effect with raw passthrough. Standalone convergence after reboot
  supplies the parked team/raw-start, scan/TF and covariance checks.
- Service stop restarts timesyncd; manual activation neither stops NTP nor
  installs the service clock watcher. Synchronize before ROS and freeze NTP for
  the manual run. Missing overlay setup silently falls back to baked packages.
- Hardware development launch defaults to `/dev/ttyUSB0`; verify the actual
  lidar device. The boot service passes `/host-dev/rplidar` explicitly.

## Oct 25 evidence and round 1 instructions (historical step numbers)

Read `~/ros2_ws/robot-session-20261025/RUNBOOK.md` step 2, `REPORT.md`, attempt
1–4 launch logs and boot captures, and attempt 4's deployed bundle.

| Evidence | Reflected in operator steps |
| --- | --- |
| Initial host date was Oct 18; service stopped NTP | 2: stop stack, synchronize UTC, prevent steps during manual ROS |
| Boot service restarted at power cycles | 2–4 and 12–13: explicit service/container ownership handoff |
| Attempt 1 boot already differed from raw by about 0.4 m/0.41 rad; return failed 0.51 m/0.60 rad | 5 and 8: capture before movement, inspect initial agreement, reject bad return |
| Attempt 2 head turns shifted SLAM 15–17 cm and ratcheted yaw | 1, 6–8 and package reference: head centred, no parked head sweeps |
| Attempt 3 raw x froze after strafing; save correctly refused at 22 cm SLAM offset | 6 and troubleshooting: monitor both axes, stop on frozen raw x, no gate relaxation |
| Straight run produced 1.38 m invented sideways SLAM motion, recovered at loop closure | 6 and 8: level stations, overlap, inspect moving matches and return closure |
| Attempt 4 save/prepare/localize passed within 5.6 cm of boot, but boot capture occurred after movement | 5: do not copy the late-capture deviation; 8–11: explicit save/prepare/AMCL gates |
| AMCL parked during patrol did not prove moving-head robustness | 1 and 11: keep head still; covariance alone is not accuracy |

No odometry, firmware, head-control or mount fix is claimed.

## Isolated room simulation

Created `isaac-agent-mapping-procedure` with `agent_container.sh up`, domain 146,
partition `agent-mapping-procedure-146`, six CPUs/12 GiB, current worktree mounted.
Installed sim dependencies, built from this checkout, and ran `smoke.sh` before
measurements: source package resolution and clean graph passed. Reused the
Oct 23 evidence-only 8 by 6 m asymmetric room SDF and sim harness through the
supported `world:=` launch argument. Referee adapter supplied room ID zero.
No robot DDS domain or hardware was used.

| Procedure action | Result |
| --- | --- |
| `mapping SESSION --room --sim-time real_hardware:=false rviz:=false` | PASS: new supervised mapping session, raw input |
| `boot-pose SESSION --sim-time --timeout 90` before movement | PASS: 720 fixed-bin fresh scans, stationary stamped capture near (-2, 0) |
| `pause` / `resume`, each with `--sim-time` | PASS: insertion state confirmed |
| Centred-head overlapping mapping circuit and return | PASS: 11.8267 m travelled, return 0.0342 m from start, head range below 0.000001 rad |
| `save SESSION --sim-time` while mapping remains live | PASS: explicit occupancy/graph/boot snapshot, `SAVE OK` |
| `prepare-room SESSION`, then `check SESSION` | PASS: deployment raster/YAML/registration verified |
| Stop mapping and all owned sim processes | PASS: supervised process-group SIGINT teardown |
| Restart sim at original mark; `localize SESSION --sim-time --timeout 90 real_hardware:=false rviz:=false` | PASS: `LOCALIZE PASS` |
| `convergence SESSION --sim-time --hold 30 --samples 20` | PASS: `CONVERGED`, fresh covariance/pose/scan/TF gates |

Mapping circuit truth diagnostics: all 425 sampled transforms available, p95
map-root error 0.0231 m, maximum 0.0351 m. These are room-sim measurements, not
hardware or full-field accuracy. Inspected the exported raster: one rectangular
perimeter and obstacle/shadow region. This was headless; live RViz scan/wall
inspection and the post-localization operator away-and-back check remain
robot-side acceptance steps. Room preparation substitutes for field `align`;
physical team/start, heading and full-field coverage were not rehearsed here.

Systemd, `/etc/thornbots`, host-clock synchronization, actual boot service/YOLO,
reboot persistence, battery, operator controls, physical odometry and lidar
extrinsics are unverifiable in this sim run. Their commands/configuration were
source-audited; the procedure requires robot-side verification before the match.

Evidence: `~/ros2_ws/mapping-procedure-20261026/` contains `rehearse.py`, room SDF,
adapter/harness, per-step logs, session bundle, circuit samples and exported PNG.
Removed this task's container and all its volumes; no containers remained, so
`agent_container.sh down` stopped Colima. No other container was touched.

## Repository checks and open acceptance

- Python 3.12 repository checker: workspace 83 tracked files, localization 37; zero diagnostics. Package uses the shared workspace checker
  because it has no local `.github/quality/check.py`.
- `actionlint -shellcheck=""` passed in both repositories; no baselines changed.
- Localization build and `colcon test`: 135 tests, zero errors/failures/skips.
- Changed Markdown links/anchors and exact README/standalone text equality checked;
  `NOTION_URL_TBD` is the requested unresolved external placeholder.

Before Oct 31: confirm field dimensions and contract starts; resolve raw-x loss
and lidar mount acceptance; confirm the approved release image is installed and selected;
rehearse boot/reboot with the actual referee and team; replace `NOTION_URL_TBD`
and publish/synchronize the Notion copy. Boot's full stack is not interlocked by
operator gates. Verify the documented manual controller mode holds the head still on the deployed
revision; patrol removal in other PRs is not assumed to be installed.

## Round 2: source re-audit and shorter operator card

The root card and standalone Notion text now have ten steps: release/manual head
control, sole owner/clock sync, image-only shells, mapping plus pre-motion boot
capture, slow coverage/raw check with pause/resume, return/save, yaw registration,
AMCL plus sustained convergence, match config/start, reboot acceptance.

- No host overlay is required by source: `Dockerfile.thornbots` builds
  `sentry_localization` and `thornbots_pkg` into `/workspaces/ros2_ws/install`.
  Manual `activate --start-only` shells explicitly source that install and check
  prefixes/workflow help. `thornbots-launch.sh` sources the same install when
  `USE_WS_OVERLAY` is absent (default false). The card removes any environment
  assignment for that key. It pins boot `THORNBOTS_IMAGE` to the approved immutable
  GHCR workspace-revision tag and compares Docker image IDs for initial runtime,
  manual container, restarted runtime and rebooted runtime. The CLI's local tag
  covers Dockerfiles, not source; the log's host workspace commit is not baked
  provenance. Image delivery is a precondition, not a claimed outcome of this task.
- `operator_workflow` mapping/localize first reject an existing stack. Field mode
  temporarily launches `operator_inputs_only:=true` for raw/referee validation,
  then launches the regular `auto.launch.py` graph. That graph includes CV
  selector/tracker/aim, patrol and the hardware relay by default; it does not
  launch YOLO. The service runs this graph plus YOLO. The new `HEAD_OFF` arguments
  disable all three CV nodes and patrol in both manual workflow commands.
- Firmware audited at workspace pin `8d46da5` using `SentryControl.hpp`,
  `JoystickMoveCommand.cpp` and `AutoAimAndFireCommand.cpp`. Left UP schedules
  auto aim/fire; its falling edge selects joystick gimbal control. Right MID
  schedules no-spin manual drive and joystick gimbal control. Neutral right-stick
  yaw input supplies zero increment to the held gimbal target. Thus the mechanism
  is controller ON, left MID/right MID, centre using right stick then neutral,
  verified physically. No ROS workflow head-lock exists. `patrol_enabled:=false`
  alone leaves target aim enabled; sending no new CV frames is not a substitute
  for leaving firmware automatic mode. The card retains manual control during
  boot acceptance even though boot's CV/YOLO nodes run. Draft workspace #100's
  patrol removal is explicitly not assumed to be on nightly.
- Rechecked all procedure commands, parser flags, launch args, package/install
  paths, environment keys, lifecycle/parameter names against the pinned sources,
  startup unit/scripts/config and image publish/pull script. Oct 25 artifacts
  remain evidence of unresolved raw-x, head/mount and moving-match failures;
  nothing here claims those are fixed.

Round 2 sim: created `isaac-agent-mapping-round2`, domain 173, partition
`agent-mapping-round2-173`, six CPUs/12 GiB, isolated source/work volumes. Installed
sim dependencies and built six packages; smoke confirmed this checkout's package
resolution and a clean graph. The Mac image has no baked `/workspaces/ros2_ws`;
Jetson image-only operation is source-verified, not exercised by this simulation.

- First fresh session: boot capture, explicit CV suppression, pause/resume and
  11.8269 m circuit passed; return 3.45 cm, sampled mapping p95 1.16 cm. Save
  correctly rejected `lidar scan stamp is stale or non-increasing`. Preserved
  evidence under `~/ros2_ws/mapping-procedure-20261026/round2/`; stopped all owned
  processes. This transient freshness failure is not diagnosed or claimed fixed.
- Second fresh session, with two seconds of parked settling before save: boot
  capture before movement, pause/resume, 11.8265 m circuit, `SAVE OK`, room
  preparation/check, full sim restart, `LOCALIZE PASS` and `CONVERGED` with
  `--hold 30 --samples 20` all passed, with default gates unchanged. Return
  3.44 cm; all 425 sampled transforms available, p95 error 1.15 cm, max 2.07 cm,
  head range below 0.000001 rad. Both mapping and localize node lists exclude
  `point_to_cv_target`, `target_selector`, `target_tracker` with the exact card
  flags. Evidence under `~/ros2_ws/mapping-procedure-20261026/round2-attempt2/`.
- The second run's node CLI warned of duplicate names and listed two
  `passthrough_odom_publisher` entries. This deserves follow-up; duplicate node
  names are undesirable. No behavior change was made to address it here.
- Room preparation substitutes for field `align`; physical field/referee/yaw,
  live RViz inspection, controller hold, away-and-back AMCL acceptance, actual
  release-image delivery and systemd/reboot remain robot-side checks. Sim cannot
  establish moving-head robustness or resolve raw-x/mount failures.
- Python 3.12 venv using `.github/quality/requirements.txt`: workspace checker
  83 files, package shared checker 37 files, zero diagnostics; actionlint passed
  in both repos. No new runtime tests were added for these documentation edits.
  Local links/anchors, Bash snippet syntax, ten-step count and exact README/Notion
  equality passed; requested `NOTION_URL_TBD` remains open. Round 1's 135 package
  tests remain recorded above, not presented as a round 2 rerun.
- Verified no sim/ROS processes remained, removed this task's container and
  volumes; no containers remained, so the helper stopped Colima. No other
  container was touched. No physical robot runs.

Open acceptance: approved release image installation/ID match, physical field
contract and controller behavior, raw-x loss, lidar extrinsics/moving matches,
attached-shell DDS, transient sim freshness/duplicate-name diagnostics, actual
referee match boot/reboot and future Notion URL/publication. No host overlay is
needed by the audited release-image path.
