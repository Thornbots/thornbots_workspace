# Changelog

Changes integrated on `nightly` and awaiting promotion to `main`. Add entries
under Unreleased as changes land; move them into a dated release section when
promoting the workspace to main. Describe user-visible behavior and real-robot
impact, and link the corresponding package changes.

## Unreleased

### Changed

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
  [JAZZY_FLASH](JAZZY_FLASH.md#8-our-image) no longer check out every
  submodule's branch tip. Start work with `git switch -c` in the package. See
  [Working with submodules](README.md#working-with-submodules).

- Non-spinning aiming holds the most face-on physical panel until another
  faces the shooter more squarely. The measured 0.3 rad margin suppresses
  noise-driven panel flips; track changes, invalid states, spinning and timeout
  clear the hold. See [thornbots_pkg #9](https://github.com/Thornbots/thornbots_pkg/pull/9),
  [sim #11](https://github.com/Thornbots/sim/pull/11) and the
  [panel-choice measurements and compiled-firmware timing checks](sim/docs/panel-choice-2026-10-11.md).

- Agents run tests, sim integration tests, sim benches and reruns as they see
  fit without asking; physical-robot runs and laptop container/VM lifecycle
  still need the user. Delegated agents never wait on user input: a brief
  naming user-approved lifecycle actions counts as that approval, and anything
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
  bit 2 enables a 500 ms hit turn that can interrupt a live CV aim. Per-frame
  gating (T31) and HitTracker's radian scaling remain open; see
  [firmware limitations](ros2_dji_serial_bridge/README.md#where-the-firmware-stands)
  and [MCBV3 529fc4e](https://github.com/Thornbots/MCBV3/commit/529fc4e).
- MCBV3 drops the hopper lid indicator and Ctrl-only lid closing. The old
  infantry target is now `engineer`; `oldinfantry` and `oldstandard` build
  names are rejected. See [MCBV3 a2ea519](https://github.com/Thornbots/MCBV3/commit/a2ea519).
- Firmware builds are warning-free (`-Werror`) on GCC 13 ARM and GCC 14
  hosted. See [MCBV3 33e853e](https://github.com/Thornbots/MCBV3/commit/33e853e).
- `humble` is read-only in thornbots_workspace, sentry_localization, sim and
  thornbots_pkg (a ruleset blocks pushes and deletion, admins included); other
  repos are in [ROADMAP T36](ROADMAP.md#short-todos).
- Workspace merges no longer advance package branches automatically; merge
  package PRs first. See
  [coordinated package integration](docs/CI.md#coordinated-package-integration).
- Docs: migration and hardware status consolidated in `JAZZY_FLASH.md`, CV
  interfaces in package READMEs and open work in `ROADMAP.md`; package
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
  [ROADMAP issues](ROADMAP.md#issues-found)), and firmware validation at
  [MCBV3 a2ea519](https://github.com/Thornbots/MCBV3/commit/a2ea519).
