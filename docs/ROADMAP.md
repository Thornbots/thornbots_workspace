# Where the project is going

Measure the real robot, run the matching sim scenario, find the differences and fix them (2026-11-05). Sim feature
work is paused; the only sim work left is making runs consistent, so sim/robot comparisons mean something.
This file owns unfinished Mini/software/sim work. Physical validation lives in [ROBOT_TESTS](ROBOT_TESTS.md); usage,
design and measurements stay in linked docs. Remove completed items once their implementation and integration have
landed.

## Where we actually are

| Area | Current evidence | Home |
| --- | --- | --- |
| Localization | Native suite passes recorded | [Drift](../sim/README.md#localization-drift-suite), [EKF](../sim/README.md#ekf-ground-truth-suite), [native validation](https://github.com/Thornbots/sim/commit/4e9445a6c1be7562e188d70a94435a47bad8043d) |
| Estimation | Bench baseline recorded | [Bench](../sim/README.md#run-the-tests), [baseline](../sim/docs/cv-bench-results-2026-09-28.md) |
| Firmware / CV | Raw aim is isolated from navigation; board stages pass diagnostic tier. Fresh Mac hosted repeats clear all spinning cells and improve every stage; three accepted board drive/match repeats improve hits over nightly | [Type C](../sim/README.md#type-c-board-execution-with-renode), [board verification](../sim/docs/mcb-auto-drive-2026-10-12.md), [accuracy repeats](../sim/docs/aim-accuracy-2026-10-12.md#spinning-correction-and-board-comparison) |
| Robots | All four Orins on JetPack 7.2.1/Jazzy; robot acceptance remains; each robot runs its own ROS domain ([T38](ROBOT_TESTS.md#robot-acceptance)) | [T38](ROBOT_TESTS.md#robot-acceptance) |

## Short todos

- **AMCL-map-odom — localization / thornbots_pkg — decision open:** First trace whether AMCL's `map->nav_odom`
  correction reaches the MCB through `mcb_relay`'s `/localization/odom` input; firmware drives absolute field routes.
  Then decide the relay input: keep `/localization/odom`, or consume `/localization/map_odom` (no reader today),
  whose AMCL covariance (0.17–0.30 m std in sim) never passes the relay's 0.02 m std gate. Do not loosen the gate
  without a user decision; validate the chosen policy against truth metrics and existing gates.
  [Interface](../sentry_localization/README.md#contract-with-thornbots_pkg), [relay](../thornbots_pkg/README.md#mcb_relay).
- **T29 — workspace / common — publication validation open:** Run the updated Mac/GitHub image-publication
  workflow end to end, including the offline overlay gate and the documented emergency local-build/shipping fallback; linting alone did not establish this acceptance. The documented laptop shipping fallback also lacks
  end-to-end evidence and requires external nonrobot capacity; Mini publication success cannot establish it.
  Equipped-robot startup is separately tracked in [ROBOT_TESTS](ROBOT_TESTS.md#robot-image-workflow).
  [Validation boundary](investigations/robot-overlay-2026-11-01.md).


## Tracks, in order of work

Order (2026-11-05): R, C, then the remaining software items and [issues found](#issues-found). Administration is
independent. Navigation waits until after the Midwest competition.

<a id="localization-policy"></a>
<a id="h-slam-at-amcls-level"></a>

**Localization (2026-11-05):** AMCL is the match backend; SLAM is second class. Track H (SLAM at amcl's level),
SLAM tuning and carried-map work are dropped. Map building for AMCL stays in scope.

### R. Real robot against sim

- **R-compare — robot / sim — open:** For each [ROBOT_TESTS](ROBOT_TESTS.md) measurement (drift, moving-aim
  delays, plant response, camera/lidar), run the same scenario in sim on consistent runs (track C), record the
  differences in a dated investigation, and fix whichever side is wrong. Prior comparison:
  [sim to real, 2026-10-18](investigations/sentry-sim-to-real-2026-10-18.md).
- **SIM-plant-model — sim / firmware — blocked on physical measurements:** Apply measured tire/braking/suspension
  and board gimbal/indexer response to the simulation, then rerun affected plant and combat regressions under
  existing limits. Depends on [SIM-plant-calibration](ROBOT_TESTS.md#consolidated-hardware-checks); measurement
  is physical, model implementation and regression remain software work. [Model](../sim/README.md#mcb-emulator).
- **B-timing — bridge / thornbots_pkg — software audit open:** Verify YOLO capture-stamp propagation
  through the tracker and latency parameters. Physical delay measurements remain in
  [robot acceptance](ROBOT_TESTS.md#moving-aim).

<a id="a-the-match-test"></a>
<a id="a-acceptance-details"></a>
<a id="d-and-e-acceptance-details"></a>

### C. Consistent sim runs

The only active sim work: the same inputs give the same results, and runs start and stop cleanly.

- **T17 — sim / thornbots_pkg — open, acceptance not met (2026-11-06):** Landed and validated on the hosted
  fixture, Mac mini: sim-time UART ([sim #79](https://github.com/Thornbots/sim/pull/79),
  [bridge #41](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/41)), the epoch-zero barrier with no
  wall-timed bring-up ([sim #80](https://github.com/Thornbots/sim/pull/80)), stamped, counted TF reads
  ([thornbots_pkg #64](https://github.com/Thornbots/thornbots_pkg/pull/64), [sim #81](https://github.com/Thornbots/sim/pull/81)),
  per-(seed, robot, stamp) noise ([sim #82](https://github.com/Thornbots/sim/pull/82)), the harness as a lockstep
  chain ([sim #83](https://github.com/Thornbots/sim/pull/83)) and now every Jetson-side UART producer as a chain:
  bridge TX acks and per-hold queue ([bridge #42](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/42)),
  none-marks, message clock and tracker delay ([thornbots_pkg #66](https://github.com/Thornbots/thornbots_pkg/pull/66),
  [nav_pkg #3](https://github.com/Thornbots/nav_pkg/pull/3)), a 34 ms simulation EKF
  ([sentry_localization #41](https://github.com/Thornbots/sentry_localization/pull/41)) and the coordinator,
  POSE-consumption hold, keyed lidar noise and `mmm` off ([sim #86](https://github.com/Thornbots/sim/pull/86)).
  All 12 `mcb_parked` cells and `mcb_drive` pass and `mcb_match` runs with 0 lockstep timeouts and 0 latest-TF
  fallbacks (it fails only its known 10% combat floor, paused combat work). **`shots.jsonl` is still not identical:**
  the Jetson-to-MCB read stream now matches for the first 19-68 lines (was 0) and its frame timing and order no
  longer differ; what remains is below it. rf2o's scan odometry differs at 1e-13 from its first graded scan with
  bit-identical inputs, which reaches CV_TARGET/RELOCALIZE as 1 ulp, and physics and the scan diverge by 1e-5 once the
  chassis moves at 14 s. Next: locate the rf2o difference, then the post-motion physics difference, re-trace with
  `MCB_UART_TRACE` and `/odom` CSVs until the streams match; then the full acceptance campaign (three unthrottled,
  one RTF=1, one gz two-core run over every cell, drive and match), which also needs a Mini with no other agent
  container (the 2026-11-06 runs shared it with a ~395% CPU container, so no RTF number was taken). Keep the 1 ms
  physics step and existing timeout limits; the original Mac/Archlinux same-hit-sequence comparison remains an
  external dependency (trace and document any per-shot difference to gz floating point) and is not claimed from Mini
  repeats. [Evidence and design](../sim/docs/t17-consistent-runs-2026-11-05.md),
  [original acceptance](E2E_LOCKSTEP_PLAN.md#approach-lockstep-as-the-estimation-bench-does).
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

<a id="b-hit-while-we-move"></a>
<a id="g-estimation-accuracy"></a>
<a id="j-lidar-and-camera"></a>
<a id="mapping-diagnostics"></a>

### Paused sim work

Paused 2026-11-05 until sim/robot comparisons show where it matters: match combat floors and sim model
(A-combat, A-model), estimation accuracy (G.1–G.3, T15, T7, T8), moving-aim floors (B-moving), suite speed
(D-speed), lidar-guided aiming stages 2–4 (T23), mapping diagnostics (E-map-graph, E-map-freshness), sim/hardware
producer selection (LAUNCH-producers), sim route checks (T40 ingress, NAV-route) and sim field integration under
RULES-S2. Full text: [previous roadmap](https://github.com/Thornbots/thornbots_workspace/blob/4331d436c84d02b9b983a616e2bb969b10e999f4/docs/ROADMAP.md).

### F. CV nodes into their own repo

- **F-split — thornbots_pkg / workspace — queued:** Move CV nodes/cores/tests to `thornbots_cv`, retaining
  hardware/TF/relay here. Update callers/build integration and rerun both benches.
  [Ownership](../thornbots_pkg/README.md#nodes), [integration](../docs/CI.md#coordinated-package-integration).

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

<a id="additional-mini-work"></a>

### Additional Mini work

- **E-discovery — startup / common — unassigned:** Isolate attached-shell DDS missing-node discovery; compare the
  running stack's bag and SHM mappings/ports with a freshly attached client, distinguish deleted SHM from transport
  discovery. Mini reproduction first; physical confirmation is in ROBOT_TESTS. Acceptance: expected nodes/topics
  remain discoverable with the supported profiles, or a documented measured cause and tested fix, without weakening
  the stack's DDS invariants. [Mechanism](../isaac-ros-startup/README.md#design-notes).
- **RF2O-format — rf2o — unassigned:** Migrate deprecated `package.xml` format 1 to format 3, preserving dependencies,
  build/export behavior and upstream diff discipline; pass package build/tests and host policy checks.
  [Owner](../rf2o_laser_odometry/AGENTS.md#scope).
- **PORTABILITY-WSL — common — external validation dependency:** The documented Windows/WSL2 workflow is untested
  end to end and requires an x86_64 NVIDIA GPU host. Preserve that validation commitment and prerequisite; it cannot
  be accepted from this Mini-only run and is not robot work. [Workflow](../isaac_ros_common/docker/README.md#windows-wsl2).
- **PORTABILITY-DDS — common — external validation dependency:** Verify the supported SIMPLE/initial-peers
  profile between two real machines over Tailscale, including node/topic discovery and delivered stamped data;
  loopback filler-participant success is insufficient. Requires a second nonrobot host, outside Mini-only scope.
  [Evidence boundary](../.claude/skills/isaac-ros-docker/reference.md#cross-machine-ros-2-over-tailscale).
- **COMMON-mounts — common — decision open:** Decide whether robot `.isaac_ros_dev-dockerargs` should be empty rather
  than mounting host configuration/credential directories. Inspect configuration paths only; this task never authorizes
  credential reads. Test the chosen mount contract without reading secrets. [Owner](../isaac_ros_common/AGENTS.md#scope).
- **RULES-S2 — firmware / workspace — unassigned:** Transcribe exact Sentry Tournament geometry and audit chassis
  limits against 80 W (3v3) and 120 W (Tournament). Unpublished Site Manual, armor style/mounting and zig-zag pole
  details remain external blockers under DOC14g.
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

<a id="later-needs-a-robot"></a>

Physical acceptance moved to [ROBOT_TESTS](ROBOT_TESTS.md#robot-acceptance). This compatibility anchor
keeps package links working until their owning repositories update them.
