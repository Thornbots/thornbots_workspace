# MMM firmware-to-node validation — 2026-10-29

All execution was on `Blaises-Mini.tail2b35ba.ts.net`, using the task-owned
`isaac-agent-mmm-e2e` arm64 Jazzy container (domain 183). No SSH, physical
robot, operator bindings, shutdown or deployment was used. Host evidence is
`~/mmm-e2e-2026-10-29/`; the final archive contains frame traces, process logs,
measurements and the validated graph/image/metadata bundle.

## Execution path

The [MCB emulator](../../sim/README.md#mcb-emulator) already executes real
firmware: Renode runs the board ELF; the explicit hosted backend runs compiled
`SentryControl` with hardware inputs. This test uses the latter, not a protocol
reimplementation. Two PTYs and a fault relay connect the compiled executable
to the real bridge. `auto.launch.py real_hardware:=false` starts `mmm` but
omits the bridge, so the suite starts the real bridge separately. Gazebo
supplies sensor data; the actual mapping stack resets SLAM and saves the map.

The [one-command suite](../../sim/README.md#run-the-tests) uses a private hosted
socket for start/save and DBUS joystick inputs. Firmware unit checks prove
that the hardware source graph excludes `hosted/` and preprocessing its control
header without `MCB_HOSTED` exposes no interface. No UART field changed.

## Measurements and scenarios

- Telemetry load: 87.87 Hz POSE and 9.65 Hz REF_SYS. ROS-observer round-trip
  maxima for 0/2/4 were 10.260/5.247/5.188 ms; firmware-origin 1/3 reached
  5.175/6.711 ms including firmware consumption of the ACK. Setup-failure 6
  had a 0.328 ms wire round trip. Observer sampling uses five-tick batches;
  all maxima are well below the peers' 500 ms retry budgets. Main had 16
  zero probes and 16 replies, with no loss. Other numbers have deliberate
  faults/outages, not a claimed zero-loss link.
- Hosted loop periods: 1.032 ms active versus 1.040 ms inactive, averaged
  across five-tick batches including fixture pacing; execution work was
  45.47 versus 47.66 microseconds per tick. Nominal firmware time advances
  1 ms per control iteration. These numbers do not represent STM32 timing.
- Backpressure: 50 simulated seconds with the reader stalled caused 43,539
  failed UART writes. A pending start was delivered after draining; 721
  telemetry frames survived versus roughly 5,100 nominal opportunities.
  One truncated frame produced one CRC16 error and lost the first Ready
  echo at the boundary; one repeated Ready request recovered it. No extra
  state change occurred. This exposes the hosted PTY's partial-write behavior.
- Loss/retry coverage: the flow drops and corrupts one frame per direction
  for each of 1/2/3/4 (eight drops and eight corruptions); setup failure does
  the same for 1/6 (four of each). Every exchange completes, frame counts
  remain bounded, and the quiet observation finds no continuing echo loop.
  The full flow has two start work items, one incomplete save and two final
  save attempts; firmware restart's session has exactly eight state changes.
  Full-flow frame totals (C→J / J→C), including final legs and retries, are
  1: 8/6, 2: 10/12, 3: 12/8, 4: 8/10; setup-failure 6 totals 4/6.
- Restart recovery: stop/restart the bridge in Ready while leaving the start,
  and in Mapping while a save request is retrying. Both recover. Restart the
  firmware to Main with Jetson alive, respect the odd-request quiet gap, then
  start again: a distinct session directory is created and firmware reaches Ready.
- Graph ownership: exactly one `/dji_serial_bridge/ping_to_mcb` publisher,
  named `mmm`, in the launched auto graph. The test only subscribes.
- Restrictions: Setup/Done output zero translation; Ready and Mapping clamp
  diagonal full-stick demand to 0.400000 m/s. Gazebo measured 0.39962 m/s in
  Ready and 0.40069 m/s in Mapping. Every active state has zero indexer and
  flywheel CAN commands, no shot events, level pitch and a forward head
  target relative to the firmware's IMU/encoder chassis estimate. Ready's
  computed beep period is 1,000 ms; green LED is inferred from Ready state,
  because GPIO output is not exposed by this fixture.
- A pre-existing snapshot directory forces the real final save to fail:
  Done goes through 4 to Mapping, then returns to Ready. The next save
  reaches Done with `validated:true` and nonempty posegraph/data/PGM/YAML/
  boot metadata. Non-mapping setup forces Setup through 6 to Done.

## Validation output

```text
[  PASSED  ] 3 tests.   # real firmware / real MMM suite
[  PASSED  ] 53 tests.  # firmware unit
[  PASSED  ] 25 tests.  # hosted firmware regressions
[  PASSED  ] 95 tests.  # sim native UART fixture
Ran 2 tests ... OK     # hardware hook exclusion
MMM INTEGRATION PASS: transient boot scan -> ready -> restart -> ready -> transient Ready scan -> mapping -> ready -> save
Summary: 612 tests, 0 errors, 0 failures, 11 skipped
Start work items: 2; Save work items: 3; Main zero requests/replies: 16/16
```

The suite's native log checker reports `bench ok` for its process logs.
Host quality uses a Python 3.12 venv with the pinned workspace requirements;
no lint baseline was expanded. Firmware retains 33 previously baselined
diagnostics, including nonstandard legacy casts; this change adds none.
Workspace/sim/firmware quality respectively checked 88/198/194 tracked files;
`actionlint -shellcheck=""` passed in all three. The final localization/sim
rerun passed; bridge and thornbots passed in the preceding full package run.

## Corrections and limits

Early runs caught test defects: saving on the Mac bind mount failed inside
`std::filesystem::copy_file`, short departure motion could regain Ready before
the intended Mapping save, and the return controller needed chassis heading
in addition to the heading-fixed root transform. Final runs use Linux `$HOME`
for map files, require more than 0.4 m of observed departure and return in
the correct frame. An existing localization test had a service-discovery
failure on its first run; a new file's abbreviated license also needed the
repository's recognized Apache header. The existing fake-MCB integration left
its known Gazebo child; only that task-created process was terminated.

The simulation applies firmware velocity setpoints to Gazebo's velocity
controller. It verifies command restrictions and observed translation, not
the calibrated CAN motor plant. Head assertions observe the firmware target,
not physical gimbal tracking. Ready beep checks the real timer, not acoustic
output. Board scheduling, physical drive/head behavior, GPIO/buzzer hardware,
robot storage, field mapping and power-loss durability still require robot
acceptance. The hook exclusion check is a source-graph/preprocessor check;
this task does not claim a new ARM build or a Renode MMM run.
