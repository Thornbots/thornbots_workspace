# In-stack MMM validation — 2026-10-29

The Jetson coordinator runs inside the normal stack. Its maintained design and
usage are in [thornbots_pkg](../../thornbots_pkg/README.md#mcb-mapping-machine),
the [save service](../../sentry_localization/README.md#explicit-mapping-snapshots),
the [host shutdown mechanism](../../isaac-ros-startup/README.md#mmm-shutdown-opt-in)
and the [wire contract](../../ros2_dji_serial_bridge/UART_PROTOCOL.md#ping-id5--mcb-mapping-machine-and-link-check).

## Scope and environment

- Own isolated `isaac-agent-mmm-node` container, Mac arm64 Jazzy image,
  ROS domain 128 and partition `agent-mmm-node-128`; software rendering.
- `agent_container.sh` created and removed this container. No physical robot,
  host unit installation, real shutdown, firmware edits or sim edits.
- `operator_workflow` is byte-for-byte `origin/nightly` again.
- SLAM/AMCL/EKF backend behavior and noise parameters were unchanged, so the
  conditional localization drift/EKF suites were not required.
- Package source revisions: thornbots_pkg `b42af41`, bridge `09b0fb1`,
  localization `394e4b5`, startup `4ee08a4`.

## Commands and output

Host checks used a Python 3.12 venv populated from
`.github/quality/requirements.txt`, running the workspace's `check.py` with
that package as cwd (the packages do not contain their own checker copies).
`actionlint -shellcheck=""` passed in all five changed repositories.

```text
thornbots_pkg:        66 files checked; 0 existing diagnostics; 0 new.
ros2_dji_serial_bridge: 32 files checked; 0 existing diagnostics; 0 new.
sentry_localization: 37 files checked; 0 existing diagnostics; 0 new.
isaac-ros-startup:    27 files checked; 0 existing diagnostics; 0 new.
```

Container commands used `dexec.sh` against the task's own container:

```bash
colcon build --symlink-install --packages-select dji_serial_bridge rf2o_laser_odometry sllidar_ros2
colcon build --symlink-install --packages-select sentry_localization thornbots_pkg
# install-sim.sh installed missing rosdeps and built --packages-up-to sim.
colcon build --symlink-install --packages-select thornbots_pkg --cmake-args -DTHORNBOTS_MMM_SIM_TEST=ON
colcon test --packages-select dji_serial_bridge sentry_localization
colcon test --packages-select sentry_localization
colcon test --packages-select thornbots_pkg
colcon test-result --verbose
```

Final output excerpts:

```text
Summary: 3 packages finished [23.2s]
Summary: 2 packages finished [1min 46s]
Summary: 6 packages finished [3min 9s]  # install-sim.sh
Summary: 1 package finished [9.34s]    # final thornbots rebuild
[==========] 20 tests from 4 test suites ran. (0 ms total)
[  PASSED  ] 20 tests.
MMM INTEGRATION PASS: start -> ready -> mapping -> ready -> save
Ran 1 test in 21.785s
OK
100% tests passed, 0 tests failed out of 11  # thornbots_pkg
100% tests passed, 0 tests failed out of 9   # sentry_localization
100% tests passed, 0 tests failed out of 10  # dji_serial_bridge
Summary: 380 tests, 0 errors, 0 failures, 11 skipped
```

The 20 core tests cover odd acknowledgment before dispatch, sliding work gates,
all even retries/cooldowns, unsolicited/unknown echoes, heartbeat independence,
single-frame loss for 1/2/3/4/6, StartGate hysteresis/stamps/dwell, save selection,
latched parked guards, failed Ready save recovery through 4 before 2, and failed
or non-mapping setup through 6. The localization fake-backend service tests
cover valid bundles, invalid/stale maps, concurrent/busy saves, missing graph
files, serialize failure/timeout and destination races. The launch test starts
normal Gazebo and auto entrypoints, uses the matching `sentry_v2` robot and a
fake MCB, drives away, returns using captured map-frame pose, and verifies
nonempty serialized graph/image/YAML/boot metadata and a validated marker.

Startup native CMake/CTest ran in the same Linux container:

```text
100% tests passed, 0 tests failed out of 8
Total Test time (real) = 0.12 sec
```

## Corrections and limits

The first localization run lacked Pillow; the prescribed sim dependency helper
installed it and the full localization rerun passed. The initial sim build also
lacked nlohmann-json, resolved by the same helper. The first integration attempt
returned using raw odometry with the old ghost robot and did not regain the
map-frame gate. The final test uses the matching measured robot model and returns
against the captured map frame, as the implementation requires. Three launch
line-length findings were fixed before the passing package rerun.

Gazebo's `/clock` parameter bridge logged exit code -11 during teardown after
the successful flow. This is outside the changed packages' logic; it does not
establish clean simulator shutdown. Gazebo also left a child process after
launch teardown: the first failed run's exact known child was stopped after
checking its command line, and final container removal removed the successful
run's child. No foreign processes or containers were touched.

This tests application flow and file durability calls, not physical storage,
MCB shared-power timing, real systemd activation or actual Jetson power-off.
The graph files are checked for nonempty regular output; a graph deserialization
round-trip and physical field mapping acceptance remain separate checks.
