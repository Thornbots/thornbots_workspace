# Open-work consolidation audit — 2026-11-02

Dated source-to-destination audit for workspace PR #160. This is a coverage/evidence record, not a third
open-work list. Live software commitments are in [ROADMAP](../ROADMAP.md); physical acceptance is in
[ROBOT_TESTS](../ROBOT_TESTS.md). IDs below are snapshot routing references; update their canonical homes.

## Method and boundaries

Enumerated versioned Markdown in the workspace and all twelve owning packages, including optional MCBV3 and
nav_pkg; searched headings, checkboxes, TODO/FIXME, next/future/remaining/open/deferred language and explicit
acceptance requirements, then inspected surrounding sections. Included README/AGENTS, dated reports, design
plans, rules-context gaps, Docker/native-Mac/WSL guidance and hidden Docker skill docs. Did not read memory,
Notion, credentials or remote-host artifacts. Upstream rulebook transcriptions, generated PDFs/layout/figures,
SDK/vendor dependency docs and ordinary install/run procedures are references, not Thornbots implementation plans.
No source filename alone determined inclusion. Pending Season 2 PR design scope was checked as a dependency;
its unmerged implementation is not completion evidence.

A documented approximation is not automatically a commitment to implement every possible physical detail.
Imported explicit planned work, required validation and named follow-ups. Kept unsupported hardware/peripheral
models and stated out-of-scope features as limits; did not invent work to implement them. Superseded dated
proposals are evidence only. Every surviving live action list below links directly to its canonical destination;
dated narrative/tables retain measurements and their original acceptance boundary.

## Coverage map

| Source / section | Disposition and canonical destination |
| --- | --- |
| [E2E_LOCKSTEP_PLAN](../E2E_LOCKSTEP_PLAN.md#order-and-done-when), numbered design | T17: stationary-lateral first → all parked cells → drive → match, no scored-loop wall-time sleeps, `compare_runs`, tested per-step commits/gitlink bumps, UART wire time, acknowledgments, deterministic bring-up, seeded inputs, no latest-TF fallback, three unthrottled/RTF=1/two-core comparison. Original cross-host parity remains an external nonrobot dependency; Mini-only work cannot establish it. Live ordered gates replaced by [A acceptance](../ROADMAP.md#a-acceptance-details). Implemented native MCB/diagnosis/emulator-every-stage parts retained as design/evidence, not reopened. |
| [E2E_PLAN speed](../E2E_PLAN.md#speed) | D-speed: timing splits, named RTF cap, scored rendering, cheap collisions, one gz session, unit+match ≤10 min / without match ≤5 min. Live list replaced by [D/E acceptance](../ROADMAP.md#d-and-e-acceptance-details). |
| [E2E match/scoring](../E2E_PLAN.md#the-match-test) | A-combat/T17: three repeats, worst minus 10-point floors, zero friendly shots, alone/sequence parity; B-moving retains ≤10-point parked-relative requirement. Explicit build gaps become A-model (occlusion/blockers/ghost realism/referee model), NAV-publisher. Design table/scoring retained as reference; live done list points to [A](../ROADMAP.md#a-acceptance-details). T31 hurt-bearing verification already has injected-hit evidence; do not duplicate its repair. |
| [Lidar aiming stages/acceptance](../lidar-guided-aiming-2026-10-25.md#stages) | T23 stage 2 sim lidar robot visibility → stage 3 visualization-only `lidar_tracker` output (no head effect) → stage 4 ranked-track head direction remain [software](../ROADMAP.md#j-lidar-and-camera); stage 1 merged workspace #100. Sim patrol/time-to-first-detection comparison preserved. Robot idle-head ~0.7 mm steps, hit-turn/referee observation, detection range and stage-4 enablement are [physical](../ROBOT_TESTS.md#consolidated-hardware-checks). Stage/acceptance live lists replaced by canonical links; design/settings retained. |
| [Rules context unextracted sources](../ARCC_2026_SENTRY_CONTEXT.md#not-yet-extracted--worth-pulling-in-later) | DOC14g/RULES-S2: exact map drawing extraction, unpublished Site Manual/armor/zig-zag details, 80/120 W chassis audit. Active 3v3 map/route work belongs to S2-foundation; Tournament/unpublished remainder not assigned. Live extraction list replaced by [canonical links](../ROADMAP.md#additional-mini-work). Existing citations/publication boundaries retained. |
| [Documentation audit](docs-audit-2026-10-06.md#open-supporting-docs-are-hard-to-follow-from-a-fresh-checkout-14) | DOC14a shell examples still unresolved; directory typo fixed sllidar #5. DOC14f history separation remains. DOC14g narrowed by rules #153/#157. DOC14b completed rf2o #23/workspace #157. Replaced stale open descriptions with [canonical links](../ROADMAP.md#issues-found). |
| [Localization README notes](../../sentry_localization/README.md#notes), AGENTS Open | H-ekf/H-map/T3/H-anomalies remain; H-amcl-noise imports sigma_hit/current-sensor remeasurement and whole-suite noise_correction caveat; H-map-odom retains unresolved covariance-gate decision; H-graph-roundtrip imports graph deserialization. Fixed-heading hardware yaw and near-return/mount checks go to [robot tests](../ROBOT_TESTS.md#consolidated-hardware-checks). Live follow-up prose/Open list replaced by links. |
| [Bringup README](../../thornbots_pkg/README.md#notes), AGENTS Open | LAUNCH-producers software arg; G tracker work; physical mount, mailbox, gimbal/indexer, fire receipt/HP/heat/power to T21/B/LIDAR-mount. T39 link repaired. Existing operational checks remain procedures, not a second implementation backlog. Open list replaced by canonical links. |
| [rf2o AGENTS](../../rf2o_laser_odometry/AGENTS.md#open), README | RF2O-format migration imported; estimated covariance caveat retained as design (H tuning owns measurement). T39 physical validation remains; optional references/default-off not mislabeled default success. Open list replaced by canonical links. |
| [Common AGENTS](../../isaac_ros_common/AGENTS.md#open), Docker/native Mac docs | T29 publication/fallback validation stays software (laptop shipping needs external nonrobot capacity); equipped-robot restart stays physical. COMMON-mounts is a configuration decision with no credential-read authorization. MAC-gui imported. WSL end-to-end validation is PORTABILITY-WSL with an external x86/NVIDIA prerequisite, not a robot test. Host stale-Humble check remains an execution rule. |
| [Startup AGENTS](../../isaac-ros-startup/AGENTS.md#open), README | E-discovery Mini investigation plus robot confirmation; T27 clock/Wi-Fi and T34 GPU recovery, physical pruning/MCAP durability acceptance preserved. T20 host log/diagnostics/pruning tests completed #154; hardware confirmation is not claimed. Open list replaced by canonical links; timesyncd/nv-tee rules retained. |
| [YOLO README](../../realsense-yolov8-nitros-bridge/README.md), [ROI README](../../Realsense_ROI_Depth_Rectifier/README.md), AGENTS | T19/T37/T38 physical depth-vs-color, copy latency/cost, per-Orin plan/camera/YOLO/capture latency. Existing pages already describe interfaces/procedures and point to robot acceptance; old roadmap anchor retained as redirect. No new software plan found in these package docs. |
| [Lidar README](../../sllidar_ros2/README.md), AGENTS | DOC14a unresolved `$echo`/`$source` example; device hotplug/scan acceptance T38. Upstream model/run matrix is reference. No driver behavior task invented. |
| [MCBV3 README](../../firmware/MCBV3/README.md), AGENTS, isolated-deploy | Engineer calibration→MCB-engineer physical prerequisite; T21 timing/fire gates; S2 shot/pitch work dependency-owned. T35 branch administration remains deferred. Board/host limitations and flashing recipe are reference/procedure, not authorization to flash or add peripheral models. |
| [nav_pkg README](../../nav_pkg/README.md) | Placeholder only; no evidence of a completed planner. Explicit later NAV_GOAL publisher commitment imported from E2E/MCB drive design as NAV-publisher. |
| [Docker skill](../../.claude/skills/isaac-ros-docker/SKILL.md), reference | Execution rules/reference, no independent plan. Attached-client discovery maps to E-discovery; two-real-machine Tailscale validation is PORTABILITY-DDS; robot links remain valid through the compatibility anchor. No containers used. |

## Dated investigation coverage

| Evidence source | Current destination / resolved status |
| --- | --- |
| [T30 startup](../t30-localization-startup-2026-10-16.md#shared-sim-comparison-and-acceptance-2026-10-18) | Completed; workspace #132 removed T30. Later acceptance supersedes original draft/pending language. Historical record marked accordingly. Broader teardown remains E. |
| [Sentry sim-to-real](../investigations/sentry-sim-to-real-2026-10-18.md) | Scan guard merged rf2o #10, angle compensation merged bringup #18; T39/SENTRY-drift physical, B-timing software audit + physical timing. Serial recalibration pause explained, no fix planned. Replaced recommendation lists; retained complete timing table/evidence. |
| [Jetson measurements](../investigations/sentry-nightly-jetson-2026-10-18.md#remaining-acceptance) | T38 delivery/calibrated depth/TF/engine; T21 controller interlocks/distance/shots; SENTRY-drift; T27/T34 boot/GPU; E-discovery; interrupted MCAP. Replaced remaining-acceptance action list with links; original failed/draft checkpoints retained as history. |
| [T39](../investigations/t39-parked-drift-2026-10-25.md), [fieldmap divergence](../investigations/fieldmap-divergence-2026-10-22.md) | T39 physical references-off/on acceptance; H-anomalies/raw-x and H-map. Existing default-off limits and shove evidence preserved, not promoted. |
| [CAD](../investigations/sentry-cad-2026-10-26.md), [mount](../investigations/lidar-mount-2026-10-26.md), [flipped mount](../investigations/lidar-flip-2026-10-31.md) | Integrated CAD/workspace #103 and flipped mount #146 are not reopened. LIDAR-mount physical yaw/full-pitch/height and map slice remain; SIM-plant-calibration physical; estimator robustness remains G/H. Upright visual mesh is a documented sensor-ignored cosmetic limit, not an explicit implementation promise. |
| [Mapping procedure](../investigations/mapping-procedure-2026-10-26.md), [operator move](../investigations/operator-workflow-move-2026-10-27.md) | MMM-field physical, H-map/H-graph-roundtrip software, E-discovery/teardown. Old Notion URL placeholder superseded by current maintained-home link in AGENTS; Notion was not accessed and publication is not newly authorized. |
| [Fieldday SLAM/AMCL](../investigations/fieldday-slam-amcl-2026-10-22.md), [safety](../investigations/fieldday-operator-safety-2026-10-22.md), [round 2](../investigations/fieldday-round2-2026-10-23.md) | H-map/T3 broad/carried-map software; MMM-field physical wall/scan/controller/survey/slip/terrain/referee boot. Partial-map/fixture skips remain historical evidence, not passes. |
| [MMM firmware E2E](../investigations/mmm-firmware-e2e-2026-10-29.md), [node validation](../investigations/mmm-node-validation-2026-10-29.md) | H-graph-roundtrip software; E-teardown; MMM-field storage/shared-power/systemd/power-off physical. Current retry protocol is already in bridge UART contract; do not reopen stale coordination warning. |
| [Robot overlay](../investigations/robot-overlay-2026-11-01.md#acceptance-boundary-and-robot-state) | T29 software publication end-to-end/fallback and equipped-robot stack acceptance split; recorded Orin build/pull measurements remain evidence. |
| [Sim G1](../../sim/docs/cv-estimation-g1-2026-10-15.md#remaining-work), [bench baseline](../../sim/docs/cv-bench-results-2026-09-28.md) | G.1/G.2/G.3/T15/T7/T8; rejected trials retained. Live remaining-work list replaced with canonical G link. Latest G three attempts invalid from timing/reset: no radial numerical failure established; D/E owns harness investigation. Recovery is host prep only; no new PR/accepted accuracy result. |
| Sim aim accuracy/followup/coupling/panel-choice/patrol reports | A/T17/A-combat, G, B-moving and physical calibration. Low hits and startup failures stay evidence; no calibrated floors claimed. Fresh-stamp decisions vs capture-stamped states remain B-timing audit. |
| Sim match/hosted/auto-drive/motor-plant/type-C/indexer/parked reports | A board repeatability, T40 ingress, D/E timing/teardown; S2-foundation pitch/counter/acquisition/readiness dependency. Do not duplicate active fixes. Unmodeled MCU peripherals/deadlines are stated backend limits, not a commitment to implement every peripheral. |
| Sim real-field/boot-heading/video/hit-contract/suite-names reports | S2 updates supersede older field fixtures; H-map integration still tested by its owner. T31 hit contract has injected-hit verification. Video recording delivered. T24 suite names completed sim #65/workspace #158; removed from open work. Reports remain evidence with canonical pointers. |

## Routing snapshot and dependencies

- Confirmed active A: T17/A-combat after S2-foundation; G: G.1/G.2/G.3/T15/T7/T8; D/E: D-speed/E-launch/E-teardown;
  H: H-ekf/H-map/T3/H-anomalies/SIM-returns, with H-amcl-noise and H-graph-roundtrip explicitly routed by coordinator;
  T25 remains coordinated firmware/bridge/sim/startup/package integration (#155 and package PRs).
- S2-foundation is owned by thread `bd016d36-d212-4073-bd22-d12edd55a1b3`: sim #63, localization #35,
  bringup #52, firmware #131. Parked acquisition/idle fixture, pitch conversion, continuous-feed shot counting,
  moving-obstacle clearance, parked_push liveness and map-save readiness must land/test there before dependents.
  Bringup #53 stays held; verify equivalence after #52 before superseding; preserve unique A work in workspace #159.
- No confirmed active assignment: T40 ingress remainder (depends S2), T29 publication/fallback, B-timing audit,
  B-moving (after A/G), T23 stages 2–4 (after S2), F-split (after G), A-model (after T17/A), E-discovery, H-map-odom decision,
  LAUNCH-producers, RF2O-format, MAC-gui, COMMON-mounts decision, NAV-publisher (post-Midwest/A/B/H),
  RULES-S2 remainder (after S2/drawing extraction), SIM-plant-model (after physical calibration), DOC14a/DOC14f/DOC14g, SIM-wall, T35 administration.
  PORTABILITY-WSL, PORTABILITY-DDS, laptop fallback shipping and T17 cross-host parity need external nonrobot capacity; Mini success is not their validation.
- Unpublished manuals/armor/zig-zag information is an external dependency, not completed work and not robot-only.
  Numerical guards (G three repeats/1.5× radial-blackout/<5 cm validity, H 0.05 m comparison, parked 0.15 m p95,
  B 10 points, runtime 10/5 min) remain at their canonical owners; no baselines were grown.

H reports three scan-bearing October 26 MCAP inputs: headturn-yaw (1,645), 1c-old (1,119), 1d-new (1,105).
All have 720 bins and median raw infinity 41.5–41.9%, clustered/persistent. Room-04 and drive-v4 contain no scans
and are excluded from returns analysis (exact filenames/provenance boundary in ROADMAP SIM-returns).
Offline returns replay/model work remains Mini software work; no new investigation or accepted result is claimed here.
Season 2's corrected moving counter is 12/158, below the 10% floor, so A/S2 remains unfinished.

## Complete nonrobot ID snapshot

Canonical acceptance remains in ROADMAP; this snapshot checks inventory coverage, not completion.

- A: T17, A-combat, A-model; G: G.1, G.2, G.3, T15, T7, T8; B: B-timing, B-moving.
- D/E: D-speed, E-teardown, E-launch, E-discovery; F: F-split.
- H/J: H-ekf, H-map, T3, H-anomalies, H-amcl-noise, H-graph-roundtrip, H-map-odom, T23, SIM-returns.
- Integration/other: T40, T25, T29, S2-foundation, LAUNCH-producers, RF2O-format, MAC-gui,
  PORTABILITY-WSL, PORTABILITY-DDS, COMMON-mounts, SIM-plant-model, NAV-publisher, RULES-S2,
  T35, DOC14a, DOC14f, DOC14g, SIM-wall.
- G's radius-constraint ordering and filter-dependent spin input are explicitly retained under G.1/T8.
  Physical measurements blocking SIM-plant-model stay in ROBOT_TESTS; the subsequent model work stays software.

## Integration and validation checkpoint

Workspace #160 depends on docs-only package PRs: sim #67, localization #36, rf2o #24, bringup #55,
common #22 and startup #25. Review packages first; replace proposed head pins with merged nightly commits
before landing workspace integration. No implementation agent merges. No other thread's fixes are included as
completed work. Host quality/actionlint/link checks are documentation validation only; final completion still needs
an empty ROADMAP **and** a separately verified complete applicable automated suite on integrated nightly.

## Versioned document manifest

The following enumerates the first-party Markdown inspected or classified. Source paths are relative to the
workspace; package revisions are the reviewed nightly starting points plus docs-only changes. `CHANGELOG` is
completion evidence, `CLAUDE` imports already-read AGENTS, and operational procedures are not copied into open work.

### Workspace

- `.claude/skills/isaac-ros-docker/SKILL.md`
- `.claude/skills/isaac-ros-docker/reference.md`
- `AGENTS.md`
- `CHANGELOG.md`
- `CLAUDE.md`
- `README.md`
- `docs/ARCC_2026_SENTRY_CONTEXT.md`
- `docs/CI.md`
- `docs/E2E_LOCKSTEP_PLAN.md`
- `docs/E2E_PLAN.md`
- `docs/ROADMAP.md`
- `docs/ROBOT_TESTS.md`
- `docs/audits/docs-audit-2026-10-06.md`
- `docs/audits/rules-pdf-layout-2026-10-15.md`
- `docs/investigations/fieldday-operator-safety-2026-10-22.md`
- `docs/investigations/fieldday-round2-2026-10-23.md`
- `docs/investigations/fieldday-slam-amcl-2026-10-22.md`
- `docs/investigations/fieldmap-divergence-2026-10-22.md`
- `docs/investigations/lidar-flip-2026-10-31.md`
- `docs/investigations/lidar-mount-2026-10-26.md`
- `docs/investigations/mapping-procedure-2026-10-26.md`
- `docs/investigations/mmm-firmware-e2e-2026-10-29.md`
- `docs/investigations/mmm-node-validation-2026-10-29.md`
- `docs/investigations/operator-workflow-move-2026-10-27.md`
- `docs/investigations/robot-overlay-2026-11-01.md`
- `docs/investigations/sentry-cad-2026-10-26.md`
- `docs/investigations/sentry-nightly-jetson-2026-10-18.md`
- `docs/investigations/sentry-sim-to-real-2026-10-18.md`
- `docs/investigations/t39-parked-drift-2026-10-25.md`
- `docs/lidar-guided-aiming-2026-10-25.md`
- `docs/t30-localization-startup-2026-10-16.md`

### Realsense_ROI_Depth_Rectifier

- `Realsense_ROI_Depth_Rectifier/AGENTS.md`
- `Realsense_ROI_Depth_Rectifier/CLAUDE.md`
- `Realsense_ROI_Depth_Rectifier/CONTRIBUTING.md`
- `Realsense_ROI_Depth_Rectifier/README.md`

### firmware/MCBV3

- `firmware/MCBV3/AGENTS.md`
- `firmware/MCBV3/CLAUDE.md`
- `firmware/MCBV3/README.md`
- `firmware/MCBV3/isolated-deploy/README.md`

### isaac-ros-startup

- `isaac-ros-startup/AGENTS.md`
- `isaac-ros-startup/CLAUDE.md`
- `isaac-ros-startup/README.md`

### isaac_ros_common

- `isaac_ros_common/AGENTS.md`
- `isaac_ros_common/CLAUDE.md`
- `isaac_ros_common/README.md`
- `isaac_ros_common/SECURITY.md`
- `isaac_ros_common/docker/README.md`
- `isaac_ros_common/isaac_ros_common/jetson_spark_compute_tests/README.md`
- `isaac_ros_common/macos/README.md`
- `isaac_ros_common/scripts/usb_installer/README.md`
- `isaac_ros_common/tests/fixtures/efi/README.md`

### nav_pkg

- `nav_pkg/README.md`

### realsense-yolov8-nitros-bridge

- `realsense-yolov8-nitros-bridge/AGENTS.md`
- `realsense-yolov8-nitros-bridge/CLAUDE.md`
- `realsense-yolov8-nitros-bridge/CONTRIBUTING.md`
- `realsense-yolov8-nitros-bridge/README.md`

### rf2o_laser_odometry

- `rf2o_laser_odometry/AGENTS.md`
- `rf2o_laser_odometry/CLAUDE.md`
- `rf2o_laser_odometry/README.md`

### ros2_dji_serial_bridge

- `ros2_dji_serial_bridge/AGENTS.md`
- `ros2_dji_serial_bridge/CLAUDE.md`
- `ros2_dji_serial_bridge/CONTRIBUTING.md`
- `ros2_dji_serial_bridge/README.md`
- `ros2_dji_serial_bridge/UART_PROTOCOL.md`

### sentry_localization

- `sentry_localization/AGENTS.md`
- `sentry_localization/CLAUDE.md`
- `sentry_localization/README.md`

### sim

- `sim/AGENTS.md`
- `sim/CHANGELOG.md`
- `sim/CLAUDE.md`
- `sim/README.md`
- `sim/docs/aim-accuracy-2026-10-12.md`
- `sim/docs/aim-followup-2026-10-12.md`
- `sim/docs/aim-localization-coupling-2026-10-11.md`
- `sim/docs/boot-heading-2026-10-30.md`
- `sim/docs/cv-bench-results-2026-09-28.md`
- `sim/docs/cv-estimation-g1-2026-10-15.md`
- `sim/docs/e2e-video-2026-10-13.md`
- `sim/docs/match-check-2026-10-11.md`
- `sim/docs/mcb-auto-drive-2026-10-12.md`
- `sim/docs/mcb-hosted-check-2026-10-11.md`
- `sim/docs/mcb-indexer-recovery-2026-10-12.md`
- `sim/docs/mcb-motor-plant-2026-10-11.md`
- `sim/docs/mcb-parked-ingress-2026-10-31.md`
- `sim/docs/mcb-parked-results-2026-10-03.md`
- `sim/docs/mcb-type-c-2026-10-11.md`
- `sim/docs/panel-choice-2026-10-11.md`
- `sim/docs/patrol-flag-2026-10-11.md`
- `sim/docs/real-field-2026-10-19.md`
- `sim/docs/suite-names-2026-11-01.md`
- `sim/docs/t31-hit-contract-2026-10-14.md`

### sllidar_ros2

- `sllidar_ros2/AGENTS.md`
- `sllidar_ros2/CLAUDE.md`
- `sllidar_ros2/README.md`

### thornbots_pkg

- `thornbots_pkg/AGENTS.md`
- `thornbots_pkg/CLAUDE.md`
- `thornbots_pkg/README.md`
- `thornbots_pkg/docs/hit-permission-2026-10-15.md`


## Recovery validation — Mac Mini, 2026-11-02

Recovered the prior local patch without changing its retained worktree; rebuilt this docs branch on
workspace nightly `53ccdb2d93598d9ca3187222d833a2d55b779dec`, preserving T24 removal and package pins.
All six docs package heads are pushed; sim includes the follow-up canonical G.1/T8 pointer.
Python 3.12 isolated host quality passes: workspace 95 files, sim 204, localization 40, rf2o 16,
bringup 71, common 169, startup 38; zero new diagnostics (rf2o retains 46 baseline diagnostics).
Actionlint passes in all seven repositories. Changed-document local links and anchors pass (731 checked),
as does `git diff --check`. Package checks use the workspace checker from each package's working directory,
as package repositories consume reusable tooling and do not contain `.github/quality/check.py` themselves.
Evidence logs: `/tmp/t3-558f-docs-checks/`; link-check helper: `/tmp/t3-558f-links.py`.
No containers, simulation, feature implementation, remote hosts or physical robots were used.
These are docs checks, not the final integrated software acceptance suite; no numerical gates or baselines changed.

## Round 1 implementation response

- T23 coverage loss: restored canonical ordered stage 2 robot visibility in sim lidar, stage 3 visualization-only
  `lidar_tracker` output without affecting the head, and stage 4 ranked-track head direction. Preserved software
  and physical acceptance, dependencies and direct design links; the design document describes interfaces and
  points to the roadmap for live status. Corrected its old stage-2 head-look cross-reference to stage 4.
- H provenance: replaced room-04/drive-v4 as scan inputs with exact 1c-old/1d-new filenames, retained the explicit
  no-scan boundary for room-04/drive-v4, and linked H's immutable dated report. Recorded observational counts only;
  no causal or replay/model acceptance claim.
- Six approved package heads remain unchanged. No containers/runtime, feature changes, self-approval or merge.
- The supplied review child timeline returned `thread_not_found` for encoded and decoded IDs; this response uses
  the findings quoted in the follow-up brief. Required GitHub contexts remain unresolved, not bypassed.

Follow-up host checks: Python 3.12 quality (95 files, zero diagnostics), actionlint, 776 local links/anchors
and `git diff --check` pass. These documentation checks do not resolve required GitHub contexts.

## R1/R2 implementation responses and R3 handoff — 2026-11-03

- R1: retained `511a515` T23 stage 2 visibility → stage 3 visualization only/no head effect → stage 4 head
  direction, plus the three scan-bearing H inputs and explicit exclusion of room-04/drive-v4.
- R2: restored the removed lockstep done-when suite order and complete coverage, no scored-loop wall-time
  sleeps, `compare_runs`, longest-holding-chain report and tested per-step commit/gitlink order under
  [T17](../ROADMAP.md#a-acceptance-details). A-combat floors remain downstream of those gates.
- Re-audited every removed Markdown hunk against nightly in the workspace and all six package docs PRs,
  including AGENTS/README open lists, design acceptance and dated remaining-work sections. Additional
  explicit preservation: G's hosted E2E nonregression, DOC14g source/page authority and exact figure/spec
  references, and E2E speed design/measurement history. Other removed commitments retain the destinations
  in the coverage tables above: match/model → A; speed → D/E; lidar → T23/robot; package configuration →
  Additional Mini work; timing/mount/boot/map/hardware → B/H or ROBOT_TESTS. No package head changed.
- Current owner checkpoint replaces stale S2 drift failures in ROADMAP; six moving parked failures and
  uncompiled/untested plant correction remain open. D/E has the quiet slot; T25 follows D/E, H follows
  foundations, G waits for accepted exact D/E refs and a new capacity grant. No runtime run was attempted.
- External nonrobot portability, cross-host parity and unpublished rules stay open; the complete nonrobot
  ID snapshot and routing dependencies above remain applicable. No completed item was inferred from docs.
- Implementation handoff only: R3 must independently compare original source acceptance, R1/R2 findings
  and these responses at the new exact workspace head, retaining the six conditional package approvals.
  No implementation self-approval, merge or integrated-suite pass is claimed.

Validation for this follow-up: host Python 3.12.14 with the pinned quality requirements checked 95 workspace
files, zero existing/new diagnostics; actionlint and repository policy passed; 778 changed-document local links
and anchors passed; whitespace passed. Logs: `/tmp/t3-43bd-docs-checks/`. Unchanged package checks/conditional
approvals are the R2 checkpoint, not newly claimed runtime evidence. Read-only current workspace nightly
policy query reports protection disabled, no required status contexts and no applicable branch rules; PR status
rollup is empty (no named pending check). Signing and push hooks remain enabled.

Owner-reported dependency heads (not pins/approval): sim #63 `03ade7d170d8a4a496734bfe455327f63ab20b5a`,
bringup #52 `1b34b0d5fe647e54e4445caf06a72aeb687c1d5c`, localization #35
`6786d341f46d0773b2eae5034440df1c9c28b8a1`, MCB #131 `8125d4677e12e02397c5c90098796990fb11a565`.
Plant correction remains owner-local, not compiled/tested. These reports do not supersede exact final integrated
suite acceptance or authorize a package head change in this docs follow-up.
