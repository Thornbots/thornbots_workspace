# Documentation audit of main

Reviewed 2026-10-06 against workspace `main` at `59e5b2d`, with every package at that commit's gitlink. Review branch: `docs/audit-2026-10-06`.

Read the 66 available documentation files, including Markdown and the world-mesh instruction file (46 unique contents; generated modm documentation is repeated across platforms). Reviewed README, AGENTS, plans, runbooks, local skill documentation, contribution/security documents, and firmware documentation. Findings below concern main; differences introduced on unmerged branches are excluded. External rulebooks and upstream release claims were not independently revalidated. No containers, robot services, simulation suites, or flashing commands were run.

The main problem is maintenance: useful explanations are copied into several documents, then one copy gets updated while the others retain incompatible instructions. The technical rationale is often good, especially the timestamp contracts and explicit benchmark limitations, but the reader cannot consistently distinguish today's operating instructions from historical observations.

## Production launch findings

### 2. Resolved — full production launch recipe

Committed and pushed: ROI `0e3d21b`, YOLO `f7fdb3f`, workspace `fc3c080`.
One short recipe near the top of the [YOLO README](realsense-yolov8-nitros-bridge/README.md#full-robot-pipeline), linked from the ROI README, starts both launches with the YOLO serial bridge disabled. Resolved on the review branch; not yet merged into main.

Original finding: the ROI README directed readers to the YOLO launch for a full production pipeline, but that launch does not start selector, tracker, aimer, or mcb_relay.

Starting `auto.launch.py` alongside that example without changing defaults starts a second serial bridge on the same device. The boot service correctly uses two launches and sets `enable_serial_bridge:=False` on the YOLO half.

Validation: launch arguments, shell syntax, local links and whitespace checks passed. No hardware launch was run.

### 3. Resolved — obsolete inference diagram

Addressed with #2: removed the obsolete graph and linked to the maintained node diagram.

[realsense-yolov8-nitros-bridge/README.md:182](realsense-yolov8-nitros-bridge/README.md#full-inference-chain) sends the singular `/cv/panel_detection` into the tracker, says the aimer converts to root frame, assigns polygon publication to the aimer, and omits mcb_relay.

Current code subscribes the tracker to `/cv/robot_panels`; the aimer publishes an odom aim point; target_selector publishes the polygon; mcb_relay sends the aim to the bridge. The correct diagram already exists in [thornbots_pkg/README.md](thornbots_pkg/README.md#nodes).

Fix: correct the diagram or link to the single maintained diagram. This is an interface contract, so the obsolete graph is more damaging than ordinary prose drift.

### 4. Firmware quickstart defaults to a different robot than advertised

Out of scope for the current work (user, 2026-10-06).

[firmware/MCBV3/README.md:51](firmware/MCBV3/README.md#writing-and-flashing-code) says bare `scons run` builds the standard project. [parse_args.py](firmware/MCBV3/MCB-project/build_tools/parse_args.py) defaults to OLDINFANTRY; `standard` maps to INFANTRY, a different value.

Fix: use an explicit `scons build robot=sentry sysid=none` example for this workspace and describe the actual default. List accepted robot and sysid values. Also fix `MCB-Project/src/` to the actual `MCB-project/src/`.

## Incorrect operating contracts

### 5. Bridge exclusivity rules contradict the implementation

[thornbots_pkg/README.md:24](thornbots_pkg/README.md#nodes), thornbots_pkg AGENTS Scope, and [ros2_dji_serial_bridge/AGENTS.md:25](ros2_dji_serial_bridge/AGENTS.md#scope) say only mcb_relay may publish or subscribe on bridge topics. The adjacent node table and code give pose_translator and the aimer POSE subscriptions, and selector/aimer REF_SYS subscriptions.

Fix: scope exclusivity to application commands sent to the bridge, if that is the intended invariant. Explicitly permit the existing telemetry readers. An agent obeying today's wording would move working subscriptions unnecessarily.

### 6. Localization rationale confuses the chassis with the heading-fixed root frame

[sentry_localization/README.md:113](sentry_localization/README.md#launchlocalizationlaunchpy) says the chassis never turns; line 233 says it never rotates and attributes this to the context document. [ARCC_2026_SENTRY_CONTEXT.md:40](ARCC_2026_SENTRY_CONTEXT.md#our-sentrys-drivetrain-not-from-the-rulebook-our-hardware-choice) explicitly says the chassis spins while driving.

The explanation in thornbots_pkg is more accurate: root stays heading-fixed while chassis yaw is a joint below it. Fixed heading belongs to that frame contract, not a physically fixed chassis.

Fix: rewrite the rf2o/EKF rationale in terms of root. Check AGENTS and config comments for the same obsolete premise; ekf.yaml's introductory source summary also disagrees with its actual source-selection arrays.

### 7. Latency documentation describes an old bridge stamp

[thornbots_pkg/README.md:221](thornbots_pkg/README.md#target_tracker) justifies `pose_latency_s` as compensation for parse-time stamping; line 371 says odom is stamped on arrival. [UART_PROTOCOL.md](ros2_dji_serial_bridge/UART_PROTOCOL.md#mcb--jetson) and the bridge's `frame_stamp()` instead use last-byte read time minus frame wire time.

Fix: state exactly which residual delay remains: USB/read buffering and MCB sample-to-send delay are unmeasured. Keep sign, timestamp origin, and correction ownership together so future tuning does not compensate wire time twice.

### 8. No-target behavior is described two different ways

[thornbots_pkg/README.md:433](thornbots_pkg/README.md#point_to_cv_targetpy) says an absent/stale state or failed TF sends no CVTarget and holds the MCB still. The same section later describes patrol as enabled by default, and `on_publish_tick()` falls back to patrol when it has no aim, if the patrol's muzzle transform is available.

Fix: distinguish target-aim failure from final output behavior. Say when patrol starts, when a missing transform prevents even patrol, and when disabling patrol causes silence.

### 9. Firmware payload guidance is obsolete

[thornbots_pkg/README.md:485](thornbots_pkg/README.md#point_to_cv_targetpy) says the firmware struct still must grow before hardware timing works; its AGENTS says firmware still reads the target as root. The bridge README and protocol already document the matching 15-byte position-based-cv payload and firmware aiming from its odometry.

Fix: remove the obsolete struct-growth task. Keep actual remaining timing/frame coordination problems linked to the bridge's firmware status instead of maintaining another status copy.

## Onboarding and documentation structure

### 10. The branch-attachment command can change the version just cloned

[README.md:16](README.md) follows a recursive clone with `git checkout <configured branch>` in every submodule. That selects each branch tip, which need not be the superproject's pinned commit. The same instructions stress that gitlinks determine what teammates build. Recursive nested submodules without a configured branch also do not receive a meaningful branch name from this command.

Fix: separate reproducing the pinned workspace from starting development. Document creating a work branch at the checked-out commit; make advancing to package branch tips a deliberate update. Apply the same correction to JAZZY_FLASH step 8.

### 11. Main's README lists the wrong firmware branch

Out of scope for now (user, 2026-10-06).

[README.md:41](README.md) says `newMain`, but [.gitmodules](.gitmodules) specifies `position-based-cv` and main pins `0885a693`.

Fix: match the table to .gitmodules. This finding is present on main and is independent of pending branch documentation updates.

### 12. Resolved — conflicting hardware status copies

Fixed on the review branch: a dated hardware-status table in JAZZY_PLAN, linked from the roadmap and package notes. User confirmation on 2026-10-06: sentry, hero and dev flashed; standard pending; no checks run on the robot yet. Older run observations are explicitly historical.

JAZZY_PLAN says hero and sentry run Jazzy, then directs readers to capture a Humble baseline on hero before reflashing it, and says sentry's image is not built. ROADMAP records the built sentry image and live detections. The vision and ROI AGENTS still say no camera run; thornbots_pkg AGENTS says nothing has run on hardware.

Fix: keep one current machine/status table with dates and link to it. Mark older measurements as historical. Separate 'runs on hardware' from 'hardware acceptance checks still missing.' Do not infer new validation merely because a node has run.

### 13. Current Jazzy guidance is buried under Humble internals

[realsense-yolov8-nitros-bridge/README.md](realsense-yolov8-nitros-bridge/README.md) warns up front that its analysis was written for 3.2, but most of the document still recommends GXF stream pools and ManagedNitrosPublisher after declaring those obsolete for 4.6. The reader has to mentally patch every section with the preamble.

Fix: make the current pipeline and measured copy boundaries the primary documentation. Move the 3.2 investigation into a dated historical document. Label unimplemented zero-copy proposals separately from the shipped bridge.

### 14. Supporting docs are hard to follow from a fresh checkout

#### 14a — Lidar README

sllidar README's udev recipe uses nonexistent `src/rpldiar_ros/`; its shell setup examples include `$echo` and `$source`, which are not executable commands as written.

#### 14b — rf2o README

rf2o README describes the algorithm but sends all fork-specific setup, parameters and tests into AGENTS. Add a short human-facing fork usage section.

#### 14c — Common README

isaac_ros_common's README is upstream-only and never leads the reader to this fork's Docker or native Mac setup.

#### 14d — Firmware deployment docs

Firmware standalone deployment sends the reader to GitLab develop artifacts and a nonexistent build anchor, without identifying this GitHub repo's artifact location.

#### 14e — Package AGENTS

Several package AGENTS still refer to Dockerfile 'LAYER 5'; current Dockerfile has four named layers and builds packages in layer 3.

#### 14f — Simulation docs

The simulation README is over 1,100 lines and its AGENTS over 300. Current commands, interface rationale, July tuning history and September postmortems are interleaved. Split historical experiments out, and keep the running instructions and current limitations short.

#### 14g — Rules context

The rules context mixes ARCC 2026, 2024 mounting specifications, 2018 hardware dimensions, user observations and RMUC rules while acknowledging the actual 2026 base building specification has not been extracted. Label each claim's authority and exact source/page; do not present older inferred rules as verified current requirements. This is a provenance finding, not a verdict that any individual rule is false.

## Removed from scope

### 1. Disk backup verification

Removed the backup and restore procedures from the reflash runbook. The
user confirmed on 2026-10-06 that nothing important remains on standard;
its reflash is a clean install. No backup-verification work remains.

## Suggested order

Items #2, #3 and #12 are resolved on the review branch. Next: the remaining interface and frame/timestamp contracts, then historical analysis and the selected #14 follow-ups. Firmware build instructions (#4) and firmware branch naming (#11) remain out of scope. Disk backup procedures (#1) were removed at the user’s request.

## CV split plan retirement

Removed the completed split plan at the user's request (2026-10-06).
Unique open work and acceptance criteria moved to ROADMAP tracks B and G;
the CV interface lives in thornbots_pkg's README, shared-frame coordination
in the serial bridge README, and old measurements in
[dated CV bench observations](sim/docs/cv-bench-results-2026-09-28.md).
Updated incoming documentation and comment references. This also removes
#9's obsolete claim in thornbots_pkg AGENTS that firmware still reads root;
its separate README payload-growth claim remains open. #14f's broader
simulation-document shortening remains open.
