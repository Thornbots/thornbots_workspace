# Changelog

Changes integrated on `nightly` and awaiting promotion to `main`. Add entries
under Unreleased as changes land; move them into a dated release section when
promoting the workspace to main. Describe user-visible behavior and real-robot
impact, and link the corresponding package changes.

## Unreleased

### Added

- Six English RoboMaster 2027 PDF editions and their original Chinese sources,
  linked from the [translation index](docs/rules/rm2027/README.md), with a
  reproducible renderer and English flowcharts. Completed the RMUC page review
  and translated contents lists across the full document set.

- Unofficial English translations of the RoboMaster 2027 RMUL and RMUC
  Rules and Participant manuals, the shared Robot Building Specifications
  Manual and the rule-change preview, checked against rendered pages. The RMUL
  Rules Manual includes translated contents, table and figure lists. The game context
  gains an [RMUL 2027 summary](docs/ARCC_2026_SENTRY_CONTEXT.md#robomaster-2027-rmul-base-rules)
  of Sentry, field and armor changes. See the
  [translation index](docs/rules/rm2027/README.md).

### Changed

- Add opt-in tracker innovation diagnostics and estimation-bench radius/prior
  controls. G.1 trials expose regressions in the full matrix, so tracker tuning,
  validity and estimation limits stay unchanged. The hosted three-stage
  nonregression gate remains pending. See
  [tracker #16](https://github.com/Thornbots/thornbots_pkg/pull/16),
  [sim #25](https://github.com/Thornbots/sim/pull/25) and the
  [dated investigation](sim/docs/cv-estimation-g1-2026-10-15.md).

- English RoboMaster PDFs now preserve each Chinese source's page count,
  page breaks, tables and artwork positions. Contents, table and figure lists
  link to their destination pages; source-region translations prevent reflow
  from moving material onto different pages.

- Move standalone workspace reference documents into `docs/` and update
  incoming links in the workspace and its packages. Conventional root files
  (README, CHANGELOG, AGENTS and CLAUDE) stay at the repository root.

- Complete T31 reporting: firmware retains the latest hit through control cycles
  until a complete REF_SYS write reports it. The report uses radians relative
  to the current chassis heading, positive CCW; the next report uses 123 until
  another hit. One-cycle control/UI reactions remain independent of this latch.
  See [firmware latch](https://github.com/Thornbots/MCBV3/pull/94),
  [emulator tests](https://github.com/Thornbots/sim/pull/22),
  [wire contract](ros2_dji_serial_bridge/UART_PROTOCOL.md#ref_sys-id3--referee-system-status)
  and [T31 validation](sim/docs/t31-hit-contract-2026-10-14.md).

- Pair the chassis-relative firmware hit-angle correction with per-frame Jetson
  hit-turn permission. Any held target estimate, including coasting/predicted
  tracks, clears `turn_to_hit`; no estimate, including patrol, permits it without
  a cooldown. Remove the incorrect gun-relative Jetson hit reaction. See
  [thornbots_pkg #14](https://github.com/Thornbots/thornbots_pkg/pull/14) and its
  [three-run hosted comparison](thornbots_pkg/docs/hit-permission-2026-10-15.md).

- REF_SYS hit angles now use radians relative to the current chassis heading,
  positive CCW, with firmware and hosted UART tests at nonzero head and chassis
  yaw. The wire payload is unchanged.
  See [firmware correction](https://github.com/Thornbots/MCBV3/pull/93) and
  [hit-angle contract](ros2_dji_serial_bridge/UART_PROTOCOL.md#ref_sys-id3--referee-system-status).

- E2E GUI stages use a dedicated RViz view and scene-only gz layout. The
  sim recorder produces synchronized 1080p H.264 demos retimed from `/clock`,
  with stage/time/score captions and scored shot markers. See
  [recording workflow](sim/README.md#record-an-e2e-demo)
  ([sim #20](https://github.com/Thornbots/sim/pull/20)).

- Aim now defaults to spin alignment gating: hold a steady center-to-shooter
  line and schedule fire for the predicted facing panel. The yaw rate filter,
  zero residual hosted lead and 94 ms indexing calibration remain unchanged.
  Three fresh Mac hosted repeats clear every spinning cell, with pooled hits
  of 97.1% versus nightly's observed 17.3%; parked, drive, match and moving
  improve to 85.5%, 93.5%, 54.5% and 79.6%. Failed nightly accuracy checks
  remain diagnostic observations; clock-invalid attempts are excluded.
  Nonspinning prediction retains panel lead and hysteresis. Board lockstep learns one 5 ms batch ahead while retaining wall
  deadlines and timeout rejection. Renode installation now avoids the
  temporary-directory cleanup prefix that deleted writable fixtures. Firmware
  sleeps between SysTick interrupts during the three-second power-on guard;
  three complete Mac board boots take 102–116 wall seconds under the unchanged
  600-second startup limit. Three native-accepted board repeats improve drive
  hits from 30.5% to 85.1% and match from 23.7% to 54.1%, with zero lockstep
  timeouts in the selected runs. See the
  [spinning and board investigation](sim/docs/aim-accuracy-2026-10-12.md#spinning-correction-and-board-comparison).

- Calibrate the hosted direct-sensor aim fixture's 8 ms gyro age and model
  projectile speed at 24 m/s, matching the firmware solver; add inherited
  muzzle motion and pose-latency controls. The 8 ms delay is fixture-specific;
  board execution uses its full IMU filter. Firmware yaw prediction now uses
  geared torque and configured friction, control integration uses the actual
  1 ms interval, and the in-game parked command holds zero wheel velocity.
  Sim adds estimated passive rolling resistance and a 3 cm parked-displacement
  limit. Three hosted pre-track-I repeats measured maximum chassis displacement
  of 19.2, 28.9 and 22.4 mm versus the 132.0 mm coasting observation. These
  scores are not controlled comparisons with the new board auto-drive route.
  Native failures remain failures, not accepted accuracy results; moving-shot
  accuracy remains an acceptance gate. See the [dated accuracy investigation](sim/docs/aim-accuracy-2026-10-12.md).

- Sim pose diagnostics distinguish local EKF field-alignment error from
  globally corrected localization error, retain capture-time TF exceptions,
  and retry delayed pose telemetry for up to one simulated second. The
  [follow-up investigation](sim/docs/aim-followup-2026-10-12.md) checks TF
  composition, startup gaps, nightly localization behavior and combat
  repeatability. `mcb_parked` first used a 0.10 m displacement bound; the
  accuracy work tightens it to 0.03 m and adds powered velocity holding.
  Capture-stamp and native accuracy failures remain visible.

- Aim and tracking use raw, never-relocalized MCB `odom`; EKF and RELOCALIZE
  correct only navigation `nav_odom` through a translation-only
  `nav_odom->odom`. The EKF no longer feeds its own heading back, the relay
  sends RELOCALIZE only when the navigation offset changes, and a team-start
  reanchor or sim clock reset is never interpolated across. POSE and CV_TARGET
  retain their current UART layouts but require matching firmware and Jetson
  updates. `mcb_drive` rejects zero native hits. The
  [controlled comparison, repeats and review-fix rerun](sim/docs/aim-localization-coupling-2026-10-11.md)
  predate the current firmware auto-drive route and are not controlled
  comparisons against it. See [MCBV3 #89](https://github.com/Thornbots/MCBV3/pull/89),
  [bridge #8](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/8),
  [thornbots_pkg #13](https://github.com/Thornbots/thornbots_pkg/pull/13),
  [sentry_localization #6](https://github.com/Thornbots/sentry_localization/pull/6), and
  [sim #16](https://github.com/Thornbots/sim/pull/16).

- MCB driving stages select firmware waypoints and spin through DBUS instead of
  scripted chassis velocities. Renode board execution is the stage default;
  hosted execution remains an explicit fixture. The emulator supplies three-axis
  IMU samples and derives traction from gz model mass. Jetson UART is unchanged.
  Track I is complete; all three board stages pass at diagnostic tier, while
  calibrated combat accuracy and repeatability remain open. See
  [sim #19](https://github.com/Thornbots/sim/pull/19),
  [MCBV3 #92](https://github.com/Thornbots/MCBV3/pull/92),
  [bridge #11](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/11), and
  [board-stage verification and limits](sim/docs/mcb-auto-drive-2026-10-12.md).

- Automatic firmware aiming now releases the indexer's stop flag when shooting
  becomes allowed after calibration/SETUP. Existing shot-eligibility gates and
  manual aiming are retained. Sim models a loaded-cartridge reverse homing
  stop and checks CAN output as well as issued requests. The real-board parked
  cell passes; repeatability remains open. See
  [MCBV3 #91](https://github.com/Thornbots/MCBV3/pull/91),
  [sim #18](https://github.com/Thornbots/sim/pull/18),
  [bridge #10](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/10), and
  [the recovery verification](sim/docs/mcb-indexer-recovery-2026-10-12.md).

- Sim runs the Type C board ELF under pinned Renode through its own calibration
  and peripheral drivers, with separate CAN motor feedback and command capture
  for each bus. CAN2 software reset preserves CAN1 receive filters so wheel
  feedback reaches the board drivers. DBUS remains absent through calibration
  so firmware samples its yaw home. The bridge drops queued frames whose send
  start precedes clock zero. Startup sysid generators are constructed in place
  to avoid exhausting the board's startup stack; normal control gains and wire
  payloads are unchanged. See [sim #17](https://github.com/Thornbots/sim/pull/17),
  [MCBV3 #90](https://github.com/Thornbots/MCBV3/pull/90),
  [bridge #9](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/9), and
  [verification and model limits](sim/docs/mcb-type-c-2026-10-11.md).

- Moving RELOCALIZE corrections now predict to their estimated apply stamp
  without counting the inbound UART leg twice. This removes a velocity-times-
  UART-latency position bias; stationary corrections are unchanged. See
  [thornbots_pkg #12](https://github.com/Thornbots/thornbots_pkg/pull/12) and
  [relay timing](thornbots_pkg/README.md#mcb_relay).

- Verified all three hosted-firmware match stages after T32/T33. Parked
  moving cells still fail; drive/match pass diagnostic completion with zero
  native hits. Current status links the
  [per-cell/segment results and native checker verdicts](sim/docs/match-check-2026-10-11.md).

- Sim runs one native MCB control tick per gz physics step, supplies DJI motor
  feedback and applies motor outputs as forces instead of gz setpoint
  controllers. The UART bridge waits for the PTY. This completes track I's
  motor path; STM32 execution and firmware auto-drive remain. See
  [sim #14](https://github.com/Thornbots/sim/pull/14),
  [MCBV3 #88](https://github.com/Thornbots/MCBV3/pull/88),
  [bridge #7](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/7) and the
  [motor validation](sim/docs/mcb-motor-plant-2026-10-11.md). Drive/match diagnostics
  pass; parked hit-path repeatability remains unresolved.

- `CVTarget.patrol` identifies every Jetson sweep and hit-turn patrol point
  on UART bit 3. The 15-byte payload and current firmware behavior stay
  unchanged; compiled-firmware tests verify all flag combinations and gates.
  Bridge diagnostic interval zero now disables its timer; negatives are
  rejected during startup.
  See [bridge #5](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/5),
  [thornbots_pkg #10](https://github.com/Thornbots/thornbots_pkg/pull/10),
  [MCBV3 #86](https://github.com/Thornbots/MCBV3/pull/86),
  [sim #12](https://github.com/Thornbots/sim/pull/12) and the
  [firmware verification](sim/docs/patrol-flag-2026-10-11.md).

- A fresh clone stays on the pinned package commits; the README and
  [JAZZY_FLASH](docs/JAZZY_FLASH.md#8-our-image) no longer check out every
  submodule's branch tip. Start work with `git switch -c` in the package. See
  [Working with submodules](README.md#working-with-submodules).

- Non-spinning aiming holds the most face-on physical panel until another
  faces the shooter more squarely. The measured 0.3 rad margin suppresses
  noise-driven panel flips; track changes, invalid states, spinning and timeout
  clear the hold. See [thornbots_pkg #9](https://github.com/Thornbots/thornbots_pkg/pull/9),
  [sim #11](https://github.com/Thornbots/sim/pull/11) and the
  [panel-choice measurements and compiled-firmware timing checks](sim/docs/panel-choice-2026-10-11.md).

- Agents run tests, sim integration tests, sim benches and reruns as they see
  fit, and start laptop containers, VMs and stacks as needed, without asking.
  Physical-robot runs and restarting or stopping what an agent did not start
  still need the user. Delegated agents never wait on user input: a brief
  naming other user-approved actions counts as that approval, and anything
  else is skipped and reported. See [delegation](AGENTS.md#delegation) and
  [runs](AGENTS.md#containers-and-runs).
- Sim temporary-world cleanup tolerates repeated shutdown events, and the native
  log checker rejects launch exceptions. Fresh hosted MCB builds, UART traffic
  and live gimbal aiming were verified on x86_64. See
  [sim #10](https://github.com/Thornbots/sim/pull/10) and the
  [verification and shutdown findings](sim/docs/mcb-hosted-check-2026-10-11.md).

- PRs into `nightly` run only cheap CI (lint, policy, host helpers, MCBV3
  hosted tests). Jazzy ROS builds, the robot image and MCBV3 ARM builds run on
  `nightly`/`main` pushes, PRs into `main` and manual dispatch, and nightly
  branch protection requires only the cheap checks. See
  [CI](docs/CI.md), [thornbots_pkg #8](https://github.com/Thornbots/thornbots_pkg/pull/8),
  [sim #9](https://github.com/Thornbots/sim/pull/9),
  [sentry_localization #4](https://github.com/Thornbots/sentry_localization/pull/4),
  [rf2o_laser_odometry #8](https://github.com/Thornbots/rf2o_laser_odometry/pull/8),
  [ros2_dji_serial_bridge #4](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/4),
  [Realsense_ROI_Depth_Rectifier #4](https://github.com/Thornbots/Realsense_ROI_Depth_Rectifier/pull/4),
  [sllidar_ros2 #4](https://github.com/Thornbots/sllidar_ros2/pull/4) and
  [MCBV3 #85](https://github.com/Thornbots/MCBV3/pull/85).
- `.claude/settings.local.json` is no longer tracked and is now gitignored; it
  held one maintainer's personal permissions and paths. Pulling this removes
  the tracked copy, so keep a backup first if you edited it locally.

## 2026-10-10

### Added

- Native MCB batch lockstep for sim's three E2E stages, with stamped
  acknowledgments and timeout rejection. This changes simulation timing; full
  hit-path repeatability is open (T17). See [sim #8](https://github.com/Thornbots/sim/pull/8) and the
  [MCB emulator](sim/README.md#mcb-emulator).
- Repository quality checks and Jazzy CI on PRs and pushes to `nightly` and
  `main`: native arm64 robot-image build and package tests, GHCR publishing by
  branch and workspace revision, hosted sentry firmware tests, and CTest for
  startup helpers. GPU validation stays manual. See
  [CI coverage and limits](docs/CI.md),
  [workspace 5e2d584](https://github.com/Thornbots/thornbots_workspace/commit/5e2d584),
  [workspace #20](https://github.com/Thornbots/thornbots_workspace/pull/20),
  [startup #4](https://github.com/Thornbots/isaac-ros-startup/pull/4) and
  [MCBV3 #84](https://github.com/Thornbots/MCBV3/pull/84).
- A coordinated `nightly` branch in the workspace and all eleven top-level
  submodule repositories; `.gitmodules` tracks them and the workspace pins
  their integrated commits.
- A hosted MCB fixture that runs the checked-out sentry C++ control code
  against fake sensor, UART, referee/DBUS, CAN, ADC and clock interfaces. See
  [MCBV3 #82](https://github.com/Thornbots/MCBV3/pull/82).
- `mcb.launch.py` runs compiled firmware against Gazebo and the real ROS
  bridge; the T3 **MCB: run firmware** action builds this worktree first. See
  [sim #3](https://github.com/Thornbots/sim/pull/3) and
  [workspace #13](https://github.com/Thornbots/thornbots_workspace/pull/13).
- Simulated E2E stages `mcb_drive` (spawn-to-center) and `mcb_match` (two
  versus two over the Jetson UART; only our robot runs the real CV stack).
  `ros2 run sim compare_runs` diffs two runs. These are diagnostics, not
  combat-accuracy validation. See [sim a515ca6](https://github.com/Thornbots/sim/commit/a515ca6) and
  [sim c4d47f5](https://github.com/Thornbots/sim/commit/c4d47f5).
- `auto.launch.py` accepts `initial_x` and `initial_y` (default 0) so
  localization starts in firmware's spawn frame. See
  [thornbots_pkg be1af7e](https://github.com/Thornbots/thornbots_pkg/commit/be1af7e).
- A repository policy check in hooks and the CI `policy` job: signed commits,
  fast-forward gitlinks, and a documented `std_msgs/Header` in first-party
  `.msg` files. Install hooks with
  `python3 scripts/install_policy_hooks.py --recursive`. See
  [repository policy](docs/CI.md#repository-policy).

### Changed

- Field-frame coordinates (origin at field centre, x toward blue's base) in
  firmware, ROS bridge, robot stack, localization and sim, replacing the
  `mcb_x_right` axis swap. This changes real-robot odometry, aiming,
  relocalization and drive coordinates: deploy matching firmware and ROS stack
  together. Maps are rotated into the new frame and ARCC26's pose graph no
  longer ships, so `slam` needs one saved from a mapping run. See
  [workspace #12](https://github.com/Thornbots/thornbots_workspace/pull/12) and
  [UART protocol](ros2_dji_serial_bridge/UART_PROTOCOL.md#message-types).
- Robot and simulation nodes, scoring harnesses and startup helpers build as
  C++17 (launch adapters and lint tooling stay Python). Node names, topics and
  scoring thresholds are unchanged; localization uses `ament_cmake`; GTests
  replace the core pytest suites. See the [node graph](thornbots_pkg/README.md#nodes),
  [native port map](sim/README.md#native-port-map) and
  [workspace #17](https://github.com/Thornbots/thornbots_workspace/pull/17).
- Every simulated E2E stage (`mcb_parked`, `mcb_drive`, `mcb_match`; test
  `e2e_suite`) runs the compiled MCB firmware through the UART bridge, with
  `detector_standin` feeding gz truth instead of YOLO. The E1 stage is gone;
  scoring uses field-safe paths and patrol is on. See
  [sim e834ba2](https://github.com/Thornbots/sim/commit/e834ba2) and [sim aef5ab1](https://github.com/Thornbots/sim/commit/aef5ab1).
- Sim's Python copy of MCB control logic is removed; firmware edits are tested
  by rebuilding the hosted executable. See [sim e594f56](https://github.com/Thornbots/sim/commit/e594f56).
- The simulated referee reports RFID zones in Taproot's current bit layout. See
  [sim 48455e2](https://github.com/Thornbots/sim/commit/48455e2).
- `pose_translator` stamps `/odom` and `/joint_states` with the incoming
  `RobotPose` stamp; the wall-clock fallback for zero stamps is gone, so
  upstream poses must carry a real stamp. See
  [thornbots_pkg 61725e1](https://github.com/Thornbots/thornbots_pkg/commit/61725e1).
- MCBV3 uses HitTracker for hit reactions and the UI hit ring. `CV_TARGET`
  bit 2 enables a 500 ms hit turn during no-estimate patrol. Per-frame
  gating, radian scaling and report latching were completed by T31 above; see
  [firmware limitations](ros2_dji_serial_bridge/README.md#where-the-firmware-stands)
  and [MCBV3 529fc4e](https://github.com/Thornbots/MCBV3/commit/529fc4e).
- MCBV3 drops the hopper lid indicator and Ctrl-only lid closing. The old
  infantry target is now `engineer`; `oldinfantry` and `oldstandard` build
  names are rejected. See [MCBV3 a2ea519](https://github.com/Thornbots/MCBV3/commit/a2ea519).
- Firmware builds are warning-free (`-Werror`) on GCC 13 ARM and GCC 14
  hosted. See [MCBV3 33e853e](https://github.com/Thornbots/MCBV3/commit/33e853e).
- `humble` is read-only in thornbots_workspace, sentry_localization, sim and
  thornbots_pkg (a ruleset blocks pushes and deletion, admins included); other
  repos are in [ROADMAP T36](docs/ROADMAP.md#short-todos).
- Workspace merges no longer advance package branches automatically; merge
  package PRs first. See
  [coordinated package integration](docs/CI.md#coordinated-package-integration).
- Docs: migration and hardware status consolidated in `JAZZY_FLASH.md`, CV
  interfaces in package READMEs and open work in `docs/ROADMAP.md`; package
  guidance updated for compiled firmware, match-stage patrol and saved-map
  startup.
- rf2o repository CI integrated with repaired workflow pins. See
  [rf2o #7](https://github.com/Thornbots/rf2o_laser_odometry/pull/7).

### Fixed

- Native harnesses keep service responses while reading results and shut down
  cleanly after the ROS context stops; CI disables background Git maintenance
  before cleanup, and `COLCON_IGNORE` keeps host startup helpers out of
  robot-image ROS tests. See [sim 4e9445a](https://github.com/Thornbots/sim/commit/4e9445a) and
  [workspace 0f928af](https://github.com/Thornbots/thornbots_workspace/commit/0f928af).
- Estimation pacing waits for model and aim consumption, seeded noise draws
  have a fixed order, and suite launches propagate failed tests and pacing
  timeouts. Runtime determinism and full Gazebo lockstep remain open. See
  [sim 80ddaa1](https://github.com/Thornbots/sim/commit/80ddaa1) and
  [thornbots_pkg 705840a](https://github.com/Thornbots/thornbots_pkg/commit/705840a).
- MCB UI drawing waits for its container, fixing a null-pointer crash when
  referee data arrives first (also affects real-robot builds). See
  [MCBV3 fff0c06](https://github.com/Thornbots/MCBV3/commit/fff0c06).
- Firmware aiming subtracts the pitch pivot's 0.39 m height from ground-frame
  `CV_TARGET.z`, correcting shots that aimed too high; needs physical shot
  validation. See [MCBV3 d792a61](https://github.com/Thornbots/MCBV3/commit/d792a61).
- Off-origin spawns no longer trigger a bogus startup relocalization to zero.
  See [sentry_localization 03e1e84](https://github.com/Thornbots/sentry_localization/commit/03e1e84).
- Target odometry twists are published in the child frame. See
  [sim d39fa60](https://github.com/Thornbots/sim/commit/d39fa60).
- Gimbal control no longer applies an extra degrees-to-radians scaling to the
  Taproot IMU's radians; this changes real-robot gimbal feedback and needs
  hardware validation. See [MCBV3 c1922aa](https://github.com/Thornbots/MCBV3/commit/c1922aa).
- Fixed a null comparison in navigation that GCC 14 exposed as a crash,
  null-safe command mappings, UART timeouts across boot-clock wraparound and
  uninitialized chassis velocity histories. See
  [MCBV3 33e853e](https://github.com/Thornbots/MCBV3/commit/33e853e) and
  [MCBV3 948cf88](https://github.com/Thornbots/MCBV3/commit/948cf88).

### Validation and limits

- Fake interfaces are active only in hosted builds. Physical motor dynamics,
  STM32 timing, boot calibration and projectile exit are outside the test
  boundary; none of this was flashed or verified on a physical robot.
- Results and revisions: [nightly validation, 2026-10-06](docs/testing/nightly-2026-10-06.md),
  the 2026-10-08 sim sweep in
  [workspace e0f2425](https://github.com/Thornbots/thornbots_workspace/commit/e0f2425) (open problems in
  [ROADMAP issues](docs/ROADMAP.md#issues-found)), and firmware validation at
  [MCBV3 a2ea519](https://github.com/Thornbots/MCBV3/commit/a2ea519).
