# Changelog

Changes integrated on `nightly` and awaiting promotion to `main`. Add entries
under Unreleased as changes land; move them into a dated release section when
promoting the workspace to main. Describe user-visible behavior and real-robot
impact, and link the corresponding package changes.

## Unreleased

### Added

- Workspace CI validates pinned native startup/common helpers and builds hosted
  sentry firmware for UART and ROS-bridge tests. Startup CI runs CTest after its
  C++ port; firmware CI covers nightly pushes with the current C++ UART fixture.
  The opt-in protection policy names every ARM robot/sysid check. See
  [workspace #20](https://github.com/Thornbots/thornbots_workspace/pull/20),
  [startup #4](https://github.com/Thornbots/isaac-ros-startup/pull/4), and
  [MCBV3 #84](https://github.com/Thornbots/MCBV3/pull/84).
- Repository quality checks and portable Jazzy CI on PRs and pushes to
  `nightly` and `main`. A native arm64 workflow builds robot images, runs
  registered package tests, then publishes branch and exact workspace revision
  tags to GHCR; base layers are cached. GPU package validation still requires
  the manual Isaac ROS workflow and a provisioned runner. Package CI changes
  retain the current wire encoding; sim stays part of normal submodule checkout.
  See [CI coverage and limits](docs/CI.md) and
  [workspace 5e2d584](https://github.com/Thornbots/thornbots_workspace/commit/5e2d584).
- A coordinated `nightly` branch in the workspace and all eleven top-level
  submodule repositories. The nightly workspace tracks those branches in
  `.gitmodules` and pins their integrated commits.
- A hosted MCB hardware fixture that executes the actual checked-out sentry
  C++ control code with fake sensor, UART, referee/DBUS, CAN, ADC, and clock
  interfaces. See [MCBV3 #82](https://github.com/Thornbots/MCBV3/pull/82) and
  [MCBV3 fff0c06](https://github.com/Thornbots/MCBV3/commit/fff0c06).
- `mcb.launch.py` runs compiled firmware against Gazebo and the real ROS bridge.
  The T3 **MCB: run firmware** action builds this worktree's sources before
  launching. See [sim #3](https://github.com/Thornbots/sim/pull/3) and
  [workspace #13](https://github.com/Thornbots/thornbots_workspace/pull/13).
- Simulated E2E stages cover spawn-to-center driving (`mcb_drive`) and
  two-versus-two combat with an ally, two opponents and referee HP over the
  real Jetson UART (`mcb_match`). Only our robot runs the real CV stack;
  the other three use truth-fed aim and fire. `match_driver` supplies our
  chassis route; firmware controls aim and fire. Runs record odometry
  disagreement per shot, and `ros2 run sim compare_runs` diffs two runs. These
  are diagnostics, not combat accuracy or firmware navigation validation. See
  [sim a515ca6](https://github.com/Thornbots/sim/commit/a515ca6),
  [sim c4d47f5](https://github.com/Thornbots/sim/commit/c4d47f5),
  [sim c8f39a2](https://github.com/Thornbots/sim/commit/c8f39a2) and
  [sim bac0624](https://github.com/Thornbots/sim/commit/bac0624).
- `auto.launch.py` accepts `initial_x` and `initial_y` (default 0) so
  localization starts in the same field spawn frame as firmware odometry. See
  [thornbots_pkg be1af7e](https://github.com/Thornbots/thornbots_pkg/commit/be1af7e)
  and [sentry_localization 03e1e84](https://github.com/Thornbots/sentry_localization/commit/03e1e84).
- A repository policy check in hooks and the CI `policy` job: commits must be
  signed by their committer (GitHub-verified in CI), gitlinks must
  fast-forward, and first-party top-level `.msg` files need a documented
  `std_msgs/Header`. Install hooks with
  `python3 scripts/install_policy_hooks.py --recursive`; see
  [repository policy](docs/CI.md#repository-policy),
  [workspace #18](https://github.com/Thornbots/thornbots_workspace/pull/18) and
  [workspace #19](https://github.com/Thornbots/thornbots_workspace/pull/19).

### Changed

- `pose_translator` publishes `/odom` and `/joint_states` with the incoming
  `RobotPose` stamp; the wall-clock fallback for zero stamps is gone, so
  upstream poses must carry a real stamp. See
  [thornbots_pkg 61725e1](https://github.com/Thornbots/thornbots_pkg/commit/61725e1).

- `humble` is read-only in thornbots_workspace, sentry_localization, sim
  and thornbots_pkg: a GitHub ruleset blocks pushes and deletion for admins
  too. The other repos with `humble` are in [ROADMAP T36](ROADMAP.md#short-todos).
- Workspace merges no longer update package branches automatically. Merge
  package PRs before updating and merging workspace gitlinks; see
  [coordinated package integration](docs/CI.md#coordinated-package-integration).
- Robot and simulation runtime nodes, scoring harnesses, offline tools and
  startup helpers now build as C++17. Launch API adapters and CI/lint tooling
  remain Python. ROS node names, topic interfaces and scoring thresholds stay
  the same; localization now uses `ament_cmake`, and native GTests replace
  the core and integration pytest suites. See the
  [node graph](thornbots_pkg/README.md#nodes) and
  [native sim port map](sim/README.md#native-port-map) and
  [workspace #17](https://github.com/Thornbots/thornbots_workspace/pull/17).

- Consolidated migration and hardware status in `JAZZY_FLASH.md`, CV interface
  details in package READMEs, and remaining work in `ROADMAP.md`. Retired
  duplicate plans while retaining nightly field-frame behavior and dated results.
- Updated package guidance for compiled firmware, enabled match-stage patrol,
  current estimation coverage and saved-map startup. Removed obsolete frame
  workarounds, E1 scoring instructions and the pose-graph blocker for blank-map
  actor checks. Hit-angle unit/reporting fixes and nonzero saved-map spawn remain
  open in ROADMAP. See
  [bridge 4e3274f](https://github.com/Thornbots/ros2_dji_serial_bridge/commit/4e3274f),
  [thornbots_pkg 5892c61](https://github.com/Thornbots/thornbots_pkg/commit/5892c61),
  [localization 02707ad](https://github.com/Thornbots/sentry_localization/commit/02707ad)
  and [sim bad5c8d](https://github.com/Thornbots/sim/commit/bad5c8d).
- Integrated rf2o repository CI with repaired immutable workspace workflow pins.
  See [rf2o 3a2c91e](https://github.com/Thornbots/rf2o_laser_odometry/commit/3a2c91e)
  and [rf2o 961ff26](https://github.com/Thornbots/rf2o_laser_odometry/commit/961ff26).
- Removed the Python copy of MCB control logic; firmware edits are now exercised
  by rebuilding the hosted executable. See
  [sim e594f56](https://github.com/Thornbots/sim/commit/e594f56).
- Integrated the matching field-frame changes from
  [workspace #12](https://github.com/Thornbots/thornbots_workspace/pull/12).
  Firmware, ROS bridge, robot stack, localization, and sim use coordinates
  centred on the field, with x toward blue's base. These change real-robot
  odometry, aiming, relocalization, and drive coordinates; deploy the matching
  firmware and ROS stack together. Localization maps are rotated into that
  frame and ARCC26's pose graph no longer ships, so `slam` needs a pose graph
  saved from a mapping run. The `mcb_x_right` axis swap is gone. See
  [sentry_localization 66a1143](https://github.com/Thornbots/sentry_localization/commit/66a1143),
  [ros2_dji_serial_bridge a302b6d](https://github.com/Thornbots/ros2_dji_serial_bridge/commit/a302b6d),
  [thornbots_pkg 9d3b7fa](https://github.com/Thornbots/thornbots_pkg/commit/9d3b7fa)
  and [MCBV3 b8b0f5b](https://github.com/Thornbots/MCBV3/commit/b8b0f5b).
- Every simulated E2E stage runs the compiled MCB firmware through the UART
  bridge, without a camera: `detector_standin` feeds gz truth in place of YOLO
  and depth. The old E1 stage, which scored simulated shots without the MCB,
  is gone. Stages are `mcb_parked`, `mcb_drive` and `mcb_match` (tests
  `e2e_suite`). Scoring is back on field-safe paths checked against the
  field mesh, and patrol is enabled so the gun can sweep for a lost or
  out-of-view opponent. See [sim e834ba2](https://github.com/Thornbots/sim/commit/e834ba2),
  [sim 413502d](https://github.com/Thornbots/sim/commit/413502d),
  [sim e9caf20](https://github.com/Thornbots/sim/commit/e9caf20) and
  [sim aef5ab1](https://github.com/Thornbots/sim/commit/aef5ab1).
- The simulated referee reports RFID zones in Taproot's current bit layout
  (resupply zones at bits 19/20, central buff at 23), matching the regenerated
  firmware. See [sim 48455e2](https://github.com/Thornbots/sim/commit/48455e2).
- MCBV3 integrates the `newMain` history and uses HitTracker for hit reactions
  and the UI hit ring. `CV_TARGET` bit 2 enables a 500 ms hit turn that can
  interrupt a live CV aim; clearing the bit ends an active turn. The Jetson
  still sends its fixed `turn_to_hit` parameter (default true); per-frame
  gating remains open (ROADMAP T31). HitTracker's extra radian scaling and
  one-cycle hit reporting also need repair; see
  [current firmware limitations](ros2_dji_serial_bridge/README.md#where-the-firmware-stands).
  See
  [MCBV3 529fc4e](https://github.com/Thornbots/MCBV3/commit/529fc4e)
  and [MCBV3 f66a3a8](https://github.com/Thornbots/MCBV3/commit/f66a3a8).
- Removed the hopper lid indicator and Ctrl-only lid closing (intentional;
  servo behavior otherwise unchanged and not validated on hardware). The old
  infantry target is renamed `engineer`; `oldinfantry` and `oldstandard`
  build names are rejected, and engineer stays out of CI until its index
  offset and torque scale are measured. See
  [MCBV3 a2ea519](https://github.com/Thornbots/MCBV3/commit/a2ea519) and
  [MCBV3 5c68021](https://github.com/Thornbots/MCBV3/commit/5c68021).
- Firmware builds are warning-free (`-Werror`) on modern toolchains: GCC 13
  ARM, GCC 14 hosted. See
  [MCBV3 33e853e](https://github.com/Thornbots/MCBV3/commit/33e853e).

### Fixed

- Native harnesses retain service responses while reading their results and
  handle worker shutdown after the ROS context stops. CI fetches disable
  background Git maintenance before removing temporary repositories;
  `COLCON_IGNORE` keeps host startup helpers out of robot-image ROS tests.
  See [sim 4e9445a](https://github.com/Thornbots/sim/commit/4e9445a),
  [workspace 0f928af](https://github.com/Thornbots/thornbots_workspace/commit/0f928af)
  and [startup 57a1f94](https://github.com/Thornbots/isaac-ros-startup/commit/57a1f94).

- Estimation pacing waits for model and aim consumption. Seeded noise draws
  now have explicit order, fixing compiler-dependent assignment of samples
  to axes in the tracker tests and simulated detections. Cross-machine metrics
  and repeated-run moving-cell errors still differ; runtime determinism is
  not established. Pacing expects the aim node's 40 Hz timer, restoring
  unthrottled runs without clock synchronization timeouts in the recorded
  validation. Suite launches and log checks propagate failed tests and pacing
  timeouts. Full Gazebo lockstep remains unfinished. See
  [sim 80ddaa1](https://github.com/Thornbots/sim/commit/80ddaa1),
  [sim 6de33f1](https://github.com/Thornbots/sim/commit/6de33f1),
  [sim 9962e32](https://github.com/Thornbots/sim/commit/9962e32),
  [sim 469f711](https://github.com/Thornbots/sim/commit/469f711),
  [thornbots_pkg 705840a](https://github.com/Thornbots/thornbots_pkg/commit/705840a)
  and [thornbots_pkg 49bf285](https://github.com/Thornbots/thornbots_pkg/commit/49bf285).
- MCB UI drawing waits for its container before use, preventing a null-pointer
  crash when referee data arrives before UI setup. This fix also applies to a
  normal real-robot firmware build. See
  [MCBV3 fff0c06](https://github.com/Thornbots/MCBV3/commit/fff0c06).
- Firmware aiming subtracts the pitch pivot's 0.39 m height from ground-frame
  `CV_TARGET.z` before solving ballistics, correcting the height reference
  that previously aimed shots too high. This requires physical shot
  validation. See [MCBV3 d792a61](https://github.com/Thornbots/MCBV3/commit/d792a61).
- Off-origin spawns no longer trigger a bogus startup relocalization to zero:
  EKF and AMCL start at the configured spawn, and rf2o initializes from the
  first raw odometry pose. See
  [sentry_localization 03e1e84](https://github.com/Thornbots/sentry_localization/commit/03e1e84).
- Target odometry twists are published in the child frame, so a spinning,
  translating target no longer violates `nav_msgs/Odometry` semantics. See
  [sim d39fa60](https://github.com/Thornbots/sim/commit/d39fa60).
- Gimbal control reads the updated Taproot IMU's radians directly, removing
  the extra degrees-to-radians scaling from yaw, pitch and angular rates.
  This changes real-robot gimbal feedback and needs hardware validation. See
  [MCBV3 c1922aa](https://github.com/Thornbots/MCBV3/commit/c1922aa).
- Removed a navigation comparison against null that GCC 14 exposed as a crash.
  Command mappings filter null commands safely, and UART timeouts survive
  boot-clock wraparound. Chassis velocity histories also start at zero rather
  than indeterminate values. See
  [MCBV3 33e853e](https://github.com/Thornbots/MCBV3/commit/33e853e) and
  [MCBV3 948cf88](https://github.com/Thornbots/MCBV3/commit/948cf88).

### Validation and limits

- Sim sweep, 2026-10-08 (Mac, workspace `a65e025`): 310 reported unit/lint
  checks, zero failures and eight skips; aiming 10/10, estimation 12/12,
  drift 9/9, EKF 72-87% better than raw odometry (down from 90-95%). `mcb_parked` scores 8/12 and 7/12 with
  different cells failing, `mcb_drive` passes with no hits, and `mcb_match`
  failed bring-up. The two default `stationary45` estimation cells have
  liveness checks but no p95 accuracy limits; 12/12 is not full accuracy
  coverage. Numbers are in workspace
  [e0f2425](https://github.com/Thornbots/thornbots_workspace/commit/e0f2425);
  open problems in [ROADMAP issues](ROADMAP.md#issues-found).
- [Nightly validation, 2026-10-06](docs/testing/nightly-2026-10-06.md): seven
  ROS packages build; 234 unit checks pass and eight cppcheck checks skip.
  Unthrottled aiming passes 10/10, estimation 11/12, localization 8/9.
  Remaining failures exceed unchanged accuracy limits; the report includes
  measurements, logs, tested revisions, and reproduction commands.
- Hosted fixture validation, 2026-10-06 (GCC 11,
  [MCBV3 fff0c06](https://github.com/Thornbots/MCBV3/commit/fff0c06) and
  [sim e594f56](https://github.com/Thornbots/sim/commit/e594f56)): 16 native
  control, wire-format and real ROS bridge tests passed. Gazebo smoke verified
  position within 0.01 m of truth, commanded gimbal bearing (0.0000 rad error)
  and 99 native indexer requests; the stack health check passed.
- Firmware validation, 2026-10-08 at the pinned
  [MCBV3 a2ea519](https://github.com/Thornbots/MCBV3/commit/a2ea519): all 12 ARM
  configurations (GCC 13), the GCC 14 hosted build, 31 control cases, four
  regressions, 23 pinned-fixture and 16 current-sim UART cases passed without
  skips. Physical servo behavior and UI rendering remain unvalidated.
- Fake interfaces are active only in hosted builds. Gazebo controllers apply
  native setpoints; physical motor dynamics, STM32 timing, boot calibration,
  and measured projectile exit remain outside this test boundary. These
  changes have not been flashed or verified on a physical robot.
