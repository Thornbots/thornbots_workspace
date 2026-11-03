# Where the project is going

Prove the firmware-driven CV stack end to end in sim, improve estimation, then validate on robots. This file owns unfinished Mini/software/sim work. Physical validation lives in
[ROBOT_TESTS](ROBOT_TESTS.md); usage, design and measurements stay in linked docs.
Remove completed items once their implementation and integration have landed. An empty roadmap is only the
finish gate together with a separately verified complete applicable automated suite on integrated `nightly`.

## Where we actually are

| Area | Current evidence | Home |
| --- | --- | --- |
| Localization | Native suite passes recorded | [Drift](../sim/README.md#localization-drift-suite), [EKF](../sim/README.md#ekf-ground-truth-suite), [native validation](https://github.com/Thornbots/sim/commit/4e9445a6c1be7562e188d70a94435a47bad8043d) |
| Estimation | Bench baseline recorded | [Bench](../sim/README.md#run-the-tests), [baseline](../sim/docs/cv-bench-results-2026-09-28.md) |
| Firmware / CV | Raw aim is isolated from navigation; board stages pass diagnostic tier. Fresh Mac hosted repeats clear all spinning cells and improve every stage; three accepted board drive/match repeats improve hits over nightly | [Type C](../sim/README.md#type-c-board-execution-with-renode), [board verification](../sim/docs/mcb-auto-drive-2026-10-12.md), [accuracy repeats](../sim/docs/aim-accuracy-2026-10-12.md#spinning-correction-and-board-comparison) |
| Robots | All four Orins on JetPack 7.2.1/Jazzy; robot acceptance remains; each robot runs its own ROS domain ([T38](ROBOT_TESTS.md#robot-acceptance)) | [T38](ROBOT_TESTS.md#robot-acceptance) |

## Short todos

- **T40 — sentry_localization / thornbots_pkg — sim ingress open:** Team starts are now independent,
  per-robot Jetson launch configuration in `/etc/thornbots/launch.env`; firmware receives its start
  through RELOCALIZE and uses absolute field routes. Defaults remain unmeasured spooky scrim values;
  [survey them before the next event](ROBOT_TESTS.md#field-starts). sim keeps its ARCC spawn and passes matching team starts to
  bringup, resolving its former start mismatch.
  The scrim route still needs validation in the ARCC world: hosted parked ingress fails to reach
  centre ([sim validation](https://github.com/Thornbots/sim/pull/61)); start/relocalization gates pass.
  [Configuration](../thornbots_pkg/README.md#point_to_cv_target),
  [wire contract](../ros2_dji_serial_bridge/UART_PROTOCOL.md#message-types).
- **T25 — bridge / MCBV3 — design open:** Expose arbitrary MCB state in a bagged ROS message; decide struct/tags, rate
  and UART bandwidth, then specify and implement both ends.
  [Wire contract](../ros2_dji_serial_bridge/UART_PROTOCOL.md#message-types).
- **T29 — workspace / common — publication validation open:** Run the updated Mac/GitHub image-publication
  workflow end to end, including the offline overlay gate and the documented emergency local-build/shipping fallback; linting alone did not establish this acceptance. The documented laptop shipping fallback also lacks
  end-to-end evidence and requires external nonrobot capacity; Mini publication success cannot establish it.
  Equipped-robot startup is separately tracked in [ROBOT_TESTS](ROBOT_TESTS.md#robot-image-workflow).
  [Validation boundary](investigations/robot-overlay-2026-11-01.md).

## Tracks, in order of work

Sim first; robot work waits (2026-10-08). Order (2026-11-01): A, G, F, sim parts of B, D and E, H, sim parts of
J, then [issues found](#issues-found); D also supports A. Administration is independent. Robot checks are under
[ROBOT_TESTS](ROBOT_TESTS.md). Navigation waits until after the Midwest competition.

### A. The match test

- **T17 — sim / thornbots_pkg — open:** Finish remaining lockstep gates and repeat the board parked-cell sweep. Inspect
  lost tracks and stamped detection/odometry inputs before tracker tuning.
  [Lockstep order](E2E_LOCKSTEP_PLAN.md#order-and-done-when),
  [hosted baseline](../sim/docs/match-check-2026-10-11.md#parked-cells).
- **A-combat — sim / thornbots_pkg — open:** Add calibrated combat floors; drive rejects zero native hits, while
  match still uses diagnostic checks. Raw aim no longer follows EKF/RELOCALIZE. Spin alignment gating clears the
  hosted near-range spinning floors. Three accepted board drive/match repeats improve hits over nightly;
  calibrated combat floors and board parked-cell repeatability remain open. Retain navigation startup
  failures in the acceptance record.
  [Diagnostic design](../sim/README.md#driving-and-combat-diagnostics-mcb_drive).

### G. Estimation accuracy

- **G.1 — thornbots_pkg — open:** Finish radius/spin repair; tested radius-noise and initial-prior settings fail
  full-matrix acceptance. Test radius-constraint ordering after the facing-yaw pseudo-update, which can move
  correlated radius below the 0.18 m clamp. Diagnostics and trial controls are available; defaults and limits stay unchanged.
  [Trials and remaining gates](../sim/docs/cv-estimation-g1-2026-10-15.md), [tracker](../thornbots_pkg/README.md#target_tracker).
- **G.2 — thornbots_pkg — open:** Tune radial depth noise with ray covariance; repair staggered-panel handoff/parity
  after blackouts. [Tracker](../thornbots_pkg/README.md#target_tracker).
- **G.3 — thornbots_pkg — open:** Gate validity on settling; compare age/residual gates and aiming cost.
  [Tracker](../thornbots_pkg/README.md#target_tracker).
- **T15 — thornbots_pkg — open:** Fix yaw/radius loss on angled stationary targets, then add limits to default
  `stationary45` cells. [Bench limits](../sim/README.md#run-the-tests).
- **T7 — thornbots_pkg — open:** Sweep acceleration process noise against velocity error, including path ends.
  [Tracker](../thornbots_pkg/README.md#target_tracker).
- **T8 — sim — open:** Compare cells run alone and in sequence; keep input spin invariant under filtering
  (`speeds:=4` currently changes 1 Hz to 2 Hz without changing the cell key). [Estimation bench](../sim/README.md#run-the-tests).

G recovery has completed host preparation only: no new PR or accepted accuracy result. Numerical work remains
blocked on accepted D/E timing/reset harness behavior and shared Mini capacity.

Score each accuracy change over three runs in its own commit; tighten limits to new worst runs and require all cells to
pass, including hosted E2E nonregression. Preserve baseline radial/blackout error within 1.5x; fresh tracks become
valid only after facing-panel error
settles below 5 cm. [Bench](../sim/README.md#run-the-tests).

### B. Hit while we move

- **B-timing — bridge / thornbots_pkg — software audit open:** Verify YOLO capture-stamp propagation
  through the tracker and latency parameters. Physical delay measurements remain in
  [robot acceptance](ROBOT_TESTS.md#moving-aim).

- **B-moving — sim / thornbots_pkg — open:** Run radial/diagonal aiming paths and add missing floors; each moving match
  segment must finish within 10 percentage points of the same target cell with our robot parked.
  [Bench](../sim/README.md#run-the-tests).

### D. Faster suites

- **D-speed — sim — open:** Find the RTF bottleneck and render only scored inputs.
  [Speed acceptance](E2E_PLAN.md#speed), [lockstep gates](E2E_LOCKSTEP_PLAN.md#order-and-done-when).

### E. Benches that start and stop cleanly

- **E-teardown — sim — open:** Resolve DDS teardown races and SIGKILL-only shutdown; obtain a matching-library aarch64
  scan-bridge backtrace. [Shutdown findings](../sim/docs/mcb-hosted-check-2026-10-11.md#shutdown-findings),
  [later observations](../sim/docs/mcb-auto-drive-2026-10-12.md).
- **E-launch — sim — open:** Ensure one-command startup, gz checks, readiness and clean completion/Ctrl-C/shell-death
  cleanup, including children outside `kill_launch.sh`. [Build prerequisite](../sim/README.md#build).
  Estimation reset/pacing passed the finite quiet Mini batch (registered tests
  with no skips and nine native-accepted tracking runs); independent review and
  broader lifecycle/RTF gates remain open:
  [harness investigation](../sim/docs/de-harness-2026-11-02.md),
  [sim #68](https://github.com/Thornbots/sim/pull/68). This does not complete E-launch or D-speed.

### F. CV nodes into their own repo

- **F-split — thornbots_pkg / workspace — queued after G:** Move CV nodes/cores/tests to `thornbots_cv`, retaining
  hardware/TF/relay here. Update callers/build integration and rerun both benches.
  [Ownership](../thornbots_pkg/README.md#nodes), [integration](../docs/CI.md#coordinated-package-integration).

### H. SLAM at amcl's level

- **H-ekf — sentry_localization — open:** Test suspected stacked lidar corrections and raw odometry as SLAM input; retune while
  retaining EKF. [Investigation](../sentry_localization/README.md#slam---use-rf2o-worse).
- **H-map — sentry_localization — open:** Matches use a prebuilt event map, surveyed with MMM, loaded at the
  configured spawn and refined by SLAM (decided 2026-11-01). Save/load a quickly rasterizing pose graph there; expose
  the hard-coded spawn.
  [Map loading](../sentry_localization/README.md#launchlocalizationlaunchpy).
- **T3 — sentry_localization / sim — open:** Run five-minute Battle from blank map with moving/spinning lidar occluders,
  high ground and realistic acceleration; score truth error, inspect crossed cells for retained robots, repeat three
  games on one carried map. [Scenario harness](../sim/README.md#scenarios).
- **H-anomalies — sentry_localization / sim — unverified:** Recheck historical EKF/map anomalies on comparable
  truth-error metrics; bisect the field-frame change if reproduced. [Metrics](../sim/README.md#localization-drift-suite),
  [history](https://github.com/Thornbots/thornbots_workspace/blob/3b8163141f919e61b4bf5dafb857130b61d78869/ROADMAP.md#issues-found).

Acceptance: SLAM+EKF passes amcl drift and game scenarios within 0.05 m on the same metric; error does not grow across
carried-map games, and maps do not accumulate robots or duplicate walls.
[Drift metrics](../sim/README.md#localization-drift-suite).

### J. Lidar and camera

Physical camera/lidar checks live in [ROBOT_TESTS](ROBOT_TESTS.md#lidar-and-camera).

- **T23 — sentry_localization / thornbots_pkg / sim — stages 2–4 open:** Stage 1 (rate-capped idle looks:
  last enemy, hit hold, enemy zone) merged in [workspace #100](https://github.com/Thornbots/thornbots_workspace/pull/100).
  Implement and validate these distinct stages in order:

  1. **Stage 2 — lidar visibility:** Make sim lidar see other robots, providing robot returns for tracker input.
  2. **Stage 3 — visualization only:** Publish `lidar_tracker` output for visualization **without affecting the head**;
     depends on stage 2 visibility and the saved-map obstacle/cluster discrimination contract.
  3. **Stage 4 — head direction:** Direct the head toward ranked lidar tracks; depends on stage 3 validation,
     camera confirmation/checked-empty handling and the existing last-enemy/hit-hold priority and turn-rate cap.

  Stages 2–3 remain in [workspace #101](https://github.com/Thornbots/thornbots_workspace/pull/101); stage 4 remains open.
  Coordinate with S2-foundation acquisition/idle-look integration; do not duplicate its owned changes.
  [Tracker and head design](lidar-guided-aiming-2026-10-25.md#design),
  [moving lidar](../sentry_localization/README.md#contract-with-thornbots_pkg),
  [idle looks](../thornbots_pkg/README.md#point_to_cv_target).
  Robot rf2o steps with the head idle are [physical validation](ROBOT_TESTS.md#lidar-and-camera).
- **T23 (acceptance):** Compare sim match stages against patrol with no regression and time-to-first-detection
  before promotion. Physical enablement remains in ROBOT_TESTS.
- **SIM-returns — sim — open:** Sim lidar matches the real 720-bin grid ([sim #31](https://github.com/Thornbots/sim/pull/31))
  but has no no-return (`inf`) beams beyond the self-filter; real has about 40%. SLAM drift in sim rose from
  0.08–0.13 m to 0.15–0.22 m with the new grid (limit 0.40 m, 3 trials); cause unknown.
  Offline recorded-returns replay/model work is Mini-executable, owned by H. Scan-bearing local inputs under
  `/Users/blaise/ros2_ws/robot-session-20261026/rf2o-replay/inputs/` are
  `sentry-20261026__1__headturn-yaw.mcap` (1,645 raw scans),
  `sentry-20261026__1c__1c-old.mcap` (1,119) and `sentry-20261026__1d__1d-new.mcap` (1,105).
  H reports all 3,869 raw scans have 720 bins, with median raw `inf` fractions 41.5–41.9% and
  clustered/persistent missing bins. `sentry-20261026b__1-room-04-odom.mcap` and
  `sentry-20261026c__4-drive-v4.mcap` contain **no scans** and cannot support returns analysis.
  [H's exact provenance and measurements](https://github.com/Thornbots/thornbots_workspace/blob/7154d241844ea91e8cd869adb143a9b4b9222f4c/docs/investigations/slam-ekf-mini-2026-11-02.md#recorded-returns-available-on-the-mini)
  are observational evidence, not a causal conclusion or accepted replay/model pass; H owns the findings.

## Consolidated commitments

### Dependencies and ownership

- **S2-foundation — dependency owned elsewhere, not done:** [Season 2 implementation thread](t3-thread://v1/bd016d36-d212-4073-bd22-d12edd55a1b3)
  owns parked acquisition/idle-look integration, simulated pitch encoder conversion/regression, continuous-feed
  shot-counter/chamber-crossing timing, moving-obstacle spawn/clearance, `parked_push` scan liveness and map-save
  backend readiness/discovery. Dependencies: [sim #63](https://github.com/Thornbots/sim/pull/63),
  [localization #35](https://github.com/Thornbots/sentry_localization/pull/35),
  [bringup #52](https://github.com/Thornbots/thornbots_pkg/pull/52),
  [firmware #131](https://github.com/Thornbots/MCBV3/pull/131), then workspace integration and accepted tests.
  Owner checkpoint (2026-11-03 02:14 UTC): finite drift 10/10 plus native passes, including moving-obstacle
  drift 0.1824 < 0.4 and parked push; drive 1/1 and match 1/1 plus native passes. Parked has six passes and
  six moving failures; stationary is 281/281. Earlier corrected moving shots were 12/158 (<10% floor), not a pass.
  These are checkpoints, not final acceptance or merged foundations. The owner retains the uncompiled/untested
  plant correction: authoritative SENTRY indexer output shaft uses CURRENT_MAX 10 A, KT 0.3125 Nm/A,
  J 0.004 kg m², gear 36 and 1000 counts A, rather than the sim M3508 rotor/C620 819.2 model.
  Do not duplicate its fixes or campaigns. Bringup #53 is on hold until #52 lands;
  independent review must check equivalence before superseding it and rebasing workspace #159.
- A owns stamped-input audit, lockstep gates, board repeatability and combat calibration **after S2-foundation**.
  G owns estimator covariance/noise. H owns SLAM/EKF, carried maps and returns, avoiding S2 readiness fixtures.
  D/E owns broader launch/teardown/RTF, avoiding S2's specific readiness fix. T25 remains its own coordinated slice.
- Newly imported work below has no confirmed implementation assignment unless one is named. Routing to a track
  describes dependency/subject ownership, not proof an active agent has accepted the added scope.

### A acceptance details

- **T17 (continued):** Finish sim-time UART serialization (bytes × 10 / baud, shared explicit baud), POSE/EKF/scan/
  detection/aimer/environment consumption acknowledgments, fixed sim-time bring-up, zero latest-TF fallbacks and
  per-robot/frame seeded noise. Finish UART first, then wall-time-free bring-up/TF/seeds; test and commit each
  step with its own gitlink bump before the next. Preserve the 1 ms physics step and existing timeout limits.
  Validate `mcb_parked` stationary-lateral first, then **all** `mcb_parked` cells, `mcb_drive` and `mcb_match`.
  For that complete coverage, compare three unthrottled runs, one RTF=1 run and one gz two-core run using
  `compare_runs`: identical `shots.jsonl`, zero lockstep timeouts/latest-TF fallbacks. Each suite reports RTF,
  holds/wall wait per chain and its longest-holding chain. **Nothing in the scored loop sleeps on wall time.**
  The original Mac/Archlinux same-hit-sequence comparison remains an external dependency (trace and document any
  per-shot difference to gz floating point),
  not authority to use another host in a Mini-only task; do not claim it passed from Mini repeats.
  [Design and original acceptance](E2E_LOCKSTEP_PLAN.md#approach-lockstep-as-the-estimation-bench-does).
- **A-combat (continued):** After T17/S2-foundation, take three accepted runs per cell; floors are worst run minus
  10 percentage points, friendly intersections zero. Require one-session match segments to agree alone/in sequence;
  each segment stays within 10 points of its floor or identifies the failing hop. Preserve navigation startup failures.
  [Scoring design](E2E_PLAN.md#scoring).
- **A-model — sim — unassigned:** Add field/robot detector occlusion and non-chassis appendage shot blockers;
  tune ghost aim realism/repeated-run spread before giving damage-taken a pass gate. Implement and test missing
  referee heat/ammo/respawn behavior. Verify hurt-bearing response against the already passing
  [T31 injected-hit tests](../sim/docs/t31-hit-contract-2026-10-14.md#targeted-validation), avoiding duplicate repair.
  Accept realistic detection-error runs with the same combat floors and zero friendly shots; do not substitute truth
  stand-ins for YOLO hardware acceptance. Depends on T17/A-combat. [Original model](E2E_PLAN.md#what-sim-provides).

### D and E acceptance details

- **D-speed (continued):** Log bring-up/reset/scored wall time and mean RTF for every suite; bisect nodes/bridges to
  name the cap. Render only scored inputs (camera off until consumed), keep ghost collisions cheap, reuse one gz
  session/reset by teleport unless clean-stack isolation is needed, and score driving/localization/hits per match
  segment. Regular unit+match run ≤10 minutes, ≤5 minutes without match. Depends on repeatable T17 inputs;
  [speed design](E2E_PLAN.md#speed). No numerical limit may be relaxed to meet runtime.
- **E-discovery — startup / common — unassigned:** Isolate attached-shell DDS missing-node discovery; compare the
  running stack's bag and SHM mappings/ports with a freshly attached client, distinguish deleted SHM from transport
  discovery. Mini reproduction first; physical confirmation is in ROBOT_TESTS. Acceptance: expected nodes/topics
  remain discoverable with the supported profiles, or a documented measured cause and tested fix, without weakening
  the stack's DDS invariants. [Mechanism](../isaac-ros-startup/README.md#design-notes).

### Mapping diagnostics

- **E-map-graph — localization / bringup — OPEN, unassigned Mini investigation:** Diagnose the two
  `passthrough_odom_publisher` graph entries in the [original round 2 evidence](investigations/mapping-procedure-2026-10-26.md#round-2-source-re-audit-and-shorter-operator-card).
  Prerequisites: recover exact source/configuration and available logs from that checkpoint; coordinate with
  E-discovery/E-launch and S2-foundation before runtime work on accepted exact refs with granted capacity.
  Acceptance: correlate process/launch ownership, node identities and publisher endpoint identities over time;
  distinguish simultaneous real duplicate publishers from ROS daemon cache/discovery artifacts. CLI duplicate-name
  output alone proves neither. Record the measured cause and validate a correction, or provide an evidenced
  disposition (including exact later refs and reproduction limits if superseded). Preserve scan/TF behavior and
  clean launch/teardown. Missing attached-shell discovery and duplicate graph entries are distinct diagnostics.
- **E-map-freshness — localization / bringup — OPEN, unassigned Mini investigation:** Explain the original
  stale/non-increasing scan rejection at save in the [same round 2 evidence](investigations/mapping-procedure-2026-10-26.md#round-2-source-re-audit-and-shorter-operator-card)
  and the [operator-move retry](investigations/operator-workflow-move-2026-10-27.md#isolated-room-rehearsal).
  Prerequisites: recover failed/successful session artifacts and exact source/configuration; coordinate with
  S2-foundation's save-readiness owner and E-launch, then obtain runtime capacity separately. Acceptance: correlate
  scan capture/receipt stamps, simulation clock, pause/resume, save request and backend readiness around rejection;
  measure the cause and validate its correction or an evidenced disposition against the original failure boundary,
  retaining fresh-scan guards and numerical gates. A later successful save, parked settling or slower retry alone
  does not explain the failure. [MMM stale-scan guard tests](investigations/mmm-node-validation-2026-10-29.md#mini-only-review-fix-round)
  establish guard behavior, not this cause. Consume S2-owned readiness fixes without duplicating them; document
  exact evidence if they resolve this diagnostic. Both investigations remain software work, not robot acceptance.

### Additional Mini work

- **H-amcl-noise — localization — assigned H extension:** Re-derive `laser_sigma_hit` (0.08 is not final) on the
  current field/720-bin sensor model, including range/material/no-return sensitivity; verify sharper maps do not make
  AMCL brittle. Retain H's truth-error acceptance and existing drift gates, including `noise_correction` whole-suite
  growth behavior; isolated gains do not count as suite acceptance. Depends on SIM-returns and S2 field integration.
  [Rationale](../sentry_localization/README.md#configamclyaml).
- **H-graph-roundtrip — localization / bringup — assigned H extension:** Deserialize MMM-saved graph/data, reload
  at the configured spawn, verify raster/map registration and carried-map operation; nonempty files alone are
  insufficient. Depends on S2-foundation readiness (do not duplicate that fixture fix), H-map.
  [Evidence boundary](investigations/mmm-node-validation-2026-10-29.md#corrections-and-limits).
- **H-map-odom — localization / bringup — decision open:** Decide backend-covariance interpretation before changing
  the relay's 0.02 m std gate or consuming `/localization/map_odom`; it currently has no reader. Validate selected
  policy against common truth metrics and existing gates. This is an unresolved user decision, not authorization to
  loosen the gate. [Interface](../sentry_localization/README.md#contract-with-thornbots_pkg).
- **LAUNCH-producers — bringup — unassigned:** Add full-stack selection of sim/hardware detection producers in
  `auto.launch.py`; demonstrate one producer chain for each mode without duplicate pipelines, preserving capture
  stamps and existing launch behavior. [Owner](../thornbots_pkg/AGENTS.md#scope).
- **RF2O-format — rf2o — unassigned:** Migrate deprecated `package.xml` format 1 to format 3, preserving dependencies,
  build/export behavior and upstream diff discipline; pass package build/tests and host policy checks.
  [Owner](../rf2o_laser_odometry/AGENTS.md#scope).
- **MAC-gui — common — unassigned:** Validate native Mac GUI rendering with the documented setup and record actual
  success/failure, prerequisites and display behavior; no container/robot result substitutes for native rendering.
  [Setup](../isaac_ros_common/macos/README.md).
- **PORTABILITY-WSL — common — external validation dependency:** The documented Windows/WSL2 workflow is untested
  end to end and requires an x86_64 NVIDIA GPU host. Preserve that validation commitment and prerequisite; it cannot
  be accepted from this Mini-only run and is not robot work. [Workflow](../isaac_ros_common/docker/README.md#windows-wsl2).
- **PORTABILITY-DDS — common — external validation dependency:** Verify the supported SIMPLE/initial-peers
  profile between two real machines over Tailscale, including node/topic discovery and delivered stamped data;
  loopback filler-participant success is insufficient. Requires a second nonrobot host, outside Mini-only scope.
  [Evidence boundary](../.claude/skills/isaac-ros-docker/reference.md#cross-machine-ros-2-over-tailscale).
- **SIM-plant-model — sim / firmware — blocked on physical measurements:** Apply measured tire/braking/suspension
  and board gimbal/indexer response to the simulation, then rerun affected plant and combat regressions under
  existing limits. Depends on [SIM-plant-calibration](ROBOT_TESTS.md#consolidated-hardware-checks); measurement
  is physical, model implementation and regression remain software work. [Model](../sim/README.md#mcb-emulator).
- **COMMON-mounts — common — decision open:** Decide whether robot `.isaac_ros_dev-dockerargs` should be empty rather
  than mounting host configuration/credential directories. Inspect configuration paths only; this task never authorizes
  credential reads. Test the chosen mount contract without reading secrets. [Owner](../isaac_ros_common/AGENTS.md#scope).
- **NAV-publisher — navigation / sim — deferred, unassigned:** Implement the later route publisher through `NAV_GOAL`,
  replacing firmware-only route selection only when the planner exists; integrate callers and exercise driving/hitting
  under existing frame/wire and route gates. Depends on post-Midwest navigation scheduling and A/B/H readiness.
  `nav_pkg` currently has only a placeholder README; it does not establish a completed planner.
  [Boundary](E2E_PLAN.md#the-match-test), [wire](../ros2_dji_serial_bridge/UART_PROTOCOL.md#message-types).
- **RULES-S2 — sim / firmware / nav — dependency-owned plus unassigned remainder:** Integrate Season 2 3v3 field/maps/
  routes through S2-foundation; separately transcribe exact Sentry Tournament geometry and audit chassis limits
  against 80 W (3v3), 120 W (Tournament). Do not duplicate the active 3v3 field generator work. Validate new map/route
  geometry against cited drawings and package tests; rules geometry is a prerequisite for event-map/nav updates.
  Unpublished Site Manual, armor style/mounting and zig-zag pole details remain external blockers under DOC14g.
  [Sources](ARCC_2026_SENTRY_CONTEXT.md#not-yet-extracted--worth-pulling-in-later).

## Later: deferred

- **T35 — MCBV3 — deferred:** Leave branches as they are for now. Later, an admin makes `main` the default branch
  (it already contains all of `newMain`; nothing references `newMain`), then deletes `newMain`.
  [Repository](https://github.com/Thornbots/MCBV3), [branch policy](../AGENTS.md#branches).


## Issues found

Open findings from the [documentation audit](../docs/audits/docs-audit-2026-10-06.md):

- **DOC14a — lidar docs — unassigned:** Repair the remaining `$echo`/`$source` shell examples and verify executable
  setup snippets; the directory typo was fixed in sllidar #5. [Audit](audits/docs-audit-2026-10-06.md#14a--lidar-readme).
- **DOC14g — workspace — audit open:** Extract remaining event-map geometry from the figures and check unpublished Site Manual and armor details (#14g).
  Track the unpublished Site Manual, dot-matrix armor style/mounting/dimensions and zig-zag pole; transcribe exact
  event-map geometry from E27 Figs 3-3–3-13 and 4-3–4-4 in coordination with RULES-S2. Preserve exact
  source/page authority for each claim; older inferred rules must not appear as verified current requirements.
  Site Manual match formats/venue details, BS27 §2.1.4/§3.6.2 dot-matrix style/mounting/dimensions
  (needed for CV training and armor priors), and E27 §3.2.4.4 zig-zag pole details remain unpublished dependencies. [Unextracted sources](ARCC_2026_SENTRY_CONTEXT.md#not-yet-extracted--worth-pulling-in-later).
- **SIM-wall — sim — untested:** Establish wall-impact behavior before demonstrating avoidance.
  [Motion-model limits](../sim/README.md#sentry_v2urdfxacro-motion-model).

<a id="later-needs-a-robot"></a>

Physical acceptance moved to [ROBOT_TESTS](ROBOT_TESTS.md#robot-acceptance). This compatibility anchor
keeps package links working until their owning repositories update them.
