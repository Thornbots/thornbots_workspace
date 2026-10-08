# Changelog

Changes integrated on `nightly` and awaiting promotion to `main`. Add entries
under Unreleased as changes land; move them into a dated release section when
promoting the workspace to main. Describe user-visible behavior and real-robot
impact, and link the corresponding package changes.

## Unreleased

### Added

- A coordinated `nightly` branch in the workspace and all eleven top-level
  submodule repositories. The nightly workspace tracks those branches in
  `.gitmodules` and pins their integrated commits.
- A hosted MCB hardware fixture that executes the actual checked-out sentry
  C++ control code with fake sensor, UART, referee/DBUS, CAN, ADC, and clock
  interfaces. See [MCBV3 #82](https://github.com/Thornbots/MCBV3/pull/82).
- `mcb.launch.py` runs compiled firmware against Gazebo and the real ROS bridge.
  The T3 **MCB: run firmware** action builds this worktree's sources before
  launching. See [sim #3](https://github.com/Thornbots/sim/pull/3) and
  [workspace #13](https://github.com/Thornbots/thornbots_workspace/pull/13).

### Changed

- Consolidated migration and hardware status in `JAZZY_FLASH.md`, CV interface
  details in package READMEs, and remaining work in `ROADMAP.md`. Retired
  duplicate plans while retaining nightly field-frame behavior and dated results.
- Integrated rf2o repository CI with repaired immutable workspace workflow pins.

- Removed the Python copy of MCB control logic; firmware edits are now exercised
  by rebuilding the hosted executable.
- Integrated the matching field-frame changes from
  [workspace #12](https://github.com/Thornbots/thornbots_workspace/pull/12).
  Firmware, ROS bridge, robot stack, localization, and sim use coordinates
  centred on the field, with x toward blue's base. These change real-robot
  odometry, aiming, relocalization, and drive coordinates; deploy the matching
  firmware and ROS stack together.
- E1 uses a detector stand-in without a camera. E1/E2 scoring remains disabled
  because the current opponent paths cross field obstacles.

### Fixed

- Estimation bench lockstep pacing now expects the aim node's existing 40 Hz
  timer, restoring unthrottled runs without clock synchronization timeouts.
  See [sim 4a8d92d](https://github.com/Thornbots/sim/commit/4a8d92d).

- Hosted MCB fixture Python files pass the sim package's copyright, import,
  formatting and docstring checks. See [sim 1c5e4c5](https://github.com/Thornbots/sim/commit/1c5e4c5).

- MCB UI drawing waits for its container before use, preventing a null-pointer
  crash when referee data arrives before UI setup. This fix also applies to a
  normal real-robot firmware build.

### Validation and limits

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
