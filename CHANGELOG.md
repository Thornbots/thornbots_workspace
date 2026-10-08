# Changelog

Changes integrated on `nightly` and awaiting promotion to `main`. Add entries
under Unreleased as changes land; move them into a dated release section when
promoting the workspace to main. Describe user-visible behavior and real-robot
impact, and link the corresponding package changes.

## Unreleased

### Added

- Repository quality checks and portable Jazzy CI on PRs and pushes to
  `nightly` and `main`; tested arm64 robot images published to GHCR with
  branch and exact workspace revision tags and cached base layers. Package
  CI changes build on their nightly tips, retaining current wire encoding.
  The workspace fast-forward check and post-merge package updater remain
  enabled on both branches; sim stays part of normal submodule checkout.
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
  two-versus-one combat with an ally and referee HP over the real Jetson UART
  (`mcb_match`). Runs record odometry disagreement per shot, and
  `tools/compare_runs.py` diffs two runs. These are diagnostics, not accuracy
  claims. See [sim a515ca6](https://github.com/Thornbots/sim/commit/a515ca6),
  [sim c4d47f5](https://github.com/Thornbots/sim/commit/c4d47f5),
  [sim c8f39a2](https://github.com/Thornbots/sim/commit/c8f39a2) and
  [sim bac0624](https://github.com/Thornbots/sim/commit/bac0624).
- `auto.launch.py` accepts `initial_x` and `initial_y` (default 0) so
  localization starts in the same field spawn frame as firmware odometry. See
  [thornbots_pkg be1af7e](https://github.com/Thornbots/thornbots_pkg/commit/be1af7e)
  and [sentry_localization 03e1e84](https://github.com/Thornbots/sentry_localization/commit/03e1e84).

### Changed

- Consolidated migration and hardware status in `JAZZY_FLASH.md`, CV interface
  details in package READMEs, and remaining work in `ROADMAP.md`. Retired
  duplicate plans while retaining nightly field-frame behavior and dated results.
- Integrated rf2o repository CI with repaired immutable workspace workflow pins.
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
  [ros2_dji_serial_bridge a302b6d](https://github.com/Thornbots/ros2_dji_serial_bridge/commit/a302b6d)
  and [thornbots_pkg 9d3b7fa](https://github.com/Thornbots/thornbots_pkg/commit/9d3b7fa).
- Every simulated E2E stage runs the compiled MCB firmware through the UART
  bridge, without a camera: `detector_standin` feeds gz truth in place of YOLO
  and depth. The old E1 stage, which scored simulated shots without the MCB,
  is gone. Stages are `mcb_parked`, `mcb_drive` and `mcb_match` (tests
  `test_mcb_*.py`). Scoring is back on field-safe paths checked against the
  field mesh, and patrol is always on so a lost or out-of-view opponent is
  reacquired. See [sim e834ba2](https://github.com/Thornbots/sim/commit/e834ba2),
  [sim 413502d](https://github.com/Thornbots/sim/commit/413502d),
  [sim e9caf20](https://github.com/Thornbots/sim/commit/e9caf20) and
  [sim aef5ab1](https://github.com/Thornbots/sim/commit/aef5ab1).
- The simulated referee reports RFID zones in Taproot's current bit layout
  (resupply zones at bits 19/20, central buff at 23), matching the regenerated
  firmware. See [sim 48455e2](https://github.com/Thornbots/sim/commit/48455e2).
- MCBV3 adds the `newMain` line: sentry CV and drive tuning, RFID
  relocalization, HitTracker-based turn-to-hit, radian angles, and unified
  controls. The hopper lid indicator and Ctrl-only lid closing are removed
  (intentional; servo behavior otherwise unchanged and not validated on
  hardware). The old infantry target is renamed `engineer`; `oldinfantry` and
  `oldstandard` build names are rejected, and engineer stays out of CI until
  its index offset and torque scale are measured. See
  [MCBV3 a2ea519](https://github.com/Thornbots/MCBV3/commit/a2ea519) and
  [MCBV3 5c68021](https://github.com/Thornbots/MCBV3/commit/5c68021).
- Firmware builds are warning-free (`-Werror`) on modern toolchains: GCC 13
  ARM, GCC 14 hosted. See
  [MCBV3 33e853e](https://github.com/Thornbots/MCBV3/commit/33e853e).

### Fixed

- Estimation pacing waits for model and aim consumption; seeded noise draws
  have explicit order, so tracker and bench results no longer differ between
  aarch64 and x86_64. Pacing expects the aim node's 40 Hz timer, restoring
  unthrottled runs without clock synchronization timeouts. Suite launches and
  log checks propagate failed tests and pacing timeouts. Full Gazebo lockstep
  remains unfinished. See [sim 80ddaa1](https://github.com/Thornbots/sim/commit/80ddaa1),
  [sim 6de33f1](https://github.com/Thornbots/sim/commit/6de33f1),
  [sim 9962e32](https://github.com/Thornbots/sim/commit/9962e32),
  [sim 469f711](https://github.com/Thornbots/sim/commit/469f711) and
  [thornbots_pkg 49bf285](https://github.com/Thornbots/thornbots_pkg/commit/49bf285).
- MCB UI drawing waits for its container before use, preventing a null-pointer
  crash when referee data arrives before UI setup. This fix also applies to a
  normal real-robot firmware build.
- Off-origin spawns no longer trigger a bogus startup relocalization to zero:
  EKF and AMCL start at the configured spawn, and rf2o initializes from the
  first raw odometry pose. See
  [sentry_localization 03e1e84](https://github.com/Thornbots/sentry_localization/commit/03e1e84).
- Target odometry twists are published in the child frame, so a spinning,
  translating target no longer violates `nav_msgs/Odometry` semantics. See
  [sim d39fa60](https://github.com/Thornbots/sim/commit/d39fa60).
- Firmware navigation no longer hits a null comparison that GCC 14 exposed as a
  crash; null command filtering and UART timeouts are wrap-safe. See
  [MCBV3 33e853e](https://github.com/Thornbots/MCBV3/commit/33e853e).

### Validation and limits

- Sim sweep, 2026-10-08 (Mac, workspace `a65e025`): 310 unit checks pass,
  aiming 10/10, estimation 12/12, drift 9/9, EKF 72-87% better than raw
  odometry (down from 90-95%). `mcb_parked` scores 8/12 and 7/12 with
  different cells failing, `mcb_drive` passes with no hits, and `mcb_match`
  failed bring-up. Numbers are in workspace `e0f2425`; open problems in
  [ROADMAP issues](ROADMAP.md#issues-found).
- [Nightly validation, 2026-10-06](docs/testing/nightly-2026-10-06.md): seven
  ROS packages build; 234 unit checks pass and eight cppcheck checks skip.
  Unthrottled aiming passes 10/10, estimation 11/12, localization 8/9.
  Remaining failures exceed unchanged accuracy limits; the report includes
  measurements, logs, tested revisions, and reproduction commands.
- Hosted release build with GCC 11; 16 native control, wire-format, and real ROS
  bridge tests passed. Gazebo smoke verified position within 0.01 m of truth,
  commanded gimbal bearing (0.0000 rad error), and 99 native indexer requests;
  the stack health check passed.
- Fake interfaces are active only in hosted builds. Gazebo controllers apply
  native setpoints; physical motor dynamics, STM32 timing, boot calibration,
  and measured projectile exit remain outside this test boundary. These
  changes have not been flashed or verified on a physical robot.
