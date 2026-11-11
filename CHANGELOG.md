# Changelog

Changes integrated on `nightly` and awaiting promotion to `main`. Add entries
under Unreleased as changes land; move them into a dated release section when
promoting the workspace to main. Describe user-visible behavior and real-robot
impact, and link the corresponding package changes.

## Unreleased

- Refresh package CI dependency pins for `thornbots_pkg`, `sim` and the serial
  bridge so their ROS jobs include `thornbots_nav` and build compatible
  `CVTarget` consumers ([thornbots_pkg #73](https://github.com/Thornbots/thornbots_pkg/pull/73),
  [sim #100](https://github.com/Thornbots/sim/pull/100),
  [serial bridge #44](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/44)).

- Serial bridge checks decision freshness after acquiring the transmit lock,
  preventing stale aim data from being sent after contention
  ([serial bridge #43](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/43)).

- Nightly tests include `nav_pkg` in checkout, dependency resolution and builds,
  fixing setup failures on the `thornbots_nav` dependency. MCBV3 is a standard
  workspace submodule; remove the former local firmware opt-out as described in
  [clone setup](README.md#mcb-firmware).

- Add an opt-in CAN bus health diagnostic to the MCB firmware. Building with
  `scons build robot=<robot> can-bus-health=true` sends one DEBUG message per
  second with each bus's not-ready command cycles, per-motor feedback rates
  and bxCAN error state. Normal builds don't change. `tools/decode_can_health.py`
  decodes bags or hex, and `--command-frames CAN1,CAN2` adds a lower-bound
  bus-load estimate
  ([usage](firmware/MCBV3/README.md#optional-can-bus-health-layout-v1);
  [MCBV3 #134](https://github.com/Thornbots/MCBV3/pull/134)). Not yet
  exercised on a physical robot.
- Simulation: the Renode board backend runs again. sim `9360b27` (T17 "identical hosted runs") stalled every Renode stage
  at its first release (`lockstep timeout: gz not held at 0.020 s`): `OpponentMover` waited 5 s wall for a path sample no
  producer makes, because the first sample, stamped with the producer's first tick, reached it during the board boot
  before the clock had left zero ([sim #96](https://github.com/Thornbots/sim/pull/96)). Hosted runs are unchanged
  (identical `shots`/`states` again, 0 lockstep timeouts and latest-TF fallbacks). `lifecycle_check.sh --repeat 4` on
  the board backend then passed 80 of 80 ([sim #97](https://github.com/Thornbots/sim/pull/97),
  [record](sim/docs/lifecycle-2026-11-05.md)); roadmap track C is complete.

- **Behavior change, robots:** off-machine DDS is now off by default and Foxglove on. The robot service sets
  `THORNBOTS_REMOTE_DDS=false` (no Fast DDS profile with Tailscale peers, `ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST`;
  `thornbots_pkg`'s pinned UDP-only nodes and `sentry_localization`'s two use loopback-only profile twins), so
  `ros2 topic`/`node` from a laptop sees nothing; `THORNBOTS_FOXGLOVE` (default `true`) keeps the read-only Foxglove
  bridge on port 8765. Cross-machine `ros2` returns with `THORNBOTS_REMOTE_DDS=true` in `/etc/thornbots/launch.env`
  (and a service restart); manual launches take `remote_dds:=true`. Sim, test launches and agent containers have both
  off (`foxglove:=true`, `remote_dds:=true`, `agent_container.sh up -F/-T` turn them on). The image's bashrc applies
  the switch after the next image build; `dexec.sh` applies it to agent containers now. Cause: bridged agent
  containers' SPDP to the robots' Tailscale IPs (~125 packets/s per `ros2` process) hung Colima twice on 2026-11-06;
  the Colima VM also drops bridged traffic to `100.64.0.0/10` unless a task opts out with `-T`
  ([investigation](docs/investigations/colima-dds-egress-2026-11-06.md)).

- Simulation: repeated hosted runs now write identical `shots.jsonl` and `states.jsonl` for every
  `mcb_parked` cell, `mcb_drive` and `mcb_match` (three unthrottled runs each; 0 lockstep timeouts, 0 latest-TF
  fallbacks). New package `robot_localization`, a fork of upstream 3.8.3 with two options that are off
  by default (`deterministic_measurement_order`, `publish_queued_stamps`), added as a submodule on `nightly`;
  only the simulation enables them (`sentry_localization`'s `ekf_deterministic_order`) and the E2E stack refuses to
  start on the stock package. The robot image and overlay do not build it, so robots keep the apt 3.8.3. `sim`
  gains exact-stamp coordinator acks, tick-keyed path, truth and parameter handling, a tick-counted scorer and
  `run_suite.sh` waits for the previous run's gz advertisements; `target_tracker` gains `tf_lookahead_s` and orders
  empty frames; `waypoint_nav` gains `epoch_zero_ready`. The RTF=1 and gz two-core runs of the T17 acceptance now pass (hosted; Renode bring-up regressed and was fixed, see
  [the T17 record](sim/docs/t17-consistent-runs-2026-11-05.md#cause-and-fix-2026-11-07),
  [robot_localization #1](https://github.com/Thornbots/robot_localization/pull/1),
  [sim #92](https://github.com/Thornbots/sim/pull/92),
  [sentry_localization #45](https://github.com/Thornbots/sentry_localization/pull/45),
  [thornbots_pkg #70](https://github.com/Thornbots/thornbots_pkg/pull/70),
  [nav_pkg #4](https://github.com/Thornbots/nav_pkg/pull/4)). No robot behavior changes.

- Simulation runs now stop with one SIGINT per process and leave nothing behind, on completion, Ctrl-C, SIGTERM,
  SIGHUP and a killed shell, for the hosted and Renode board backends: `run_suite.sh` forwards the signals and starts
  the launch behind a parent-death guard, gz sim starts without the `sh -c` wrapper that orphaned it, the `gz_bridge`
  executable replaces `parameter_bridge` (which crashed in Fast DDS teardown), the lockstep gate, firmware waits, board
  adapter and Renode honour a stop request, and `tools/lifecycle_check.sh` is the acceptance test. `seeded_ekf`
  exits 0 when interrupted during startup, absorbing a `robot_localization` startup abort. The early-interrupt bridge
  crash (about 1 of 20) came from `ros_gz_bridge`'s node never being destroyed, so Fast DDS's participant was torn down
  against rmw's listener thread at exit; `gz_bridge` now frees its context first and bounds its teardown with a
  logged 3 s watchdog, and the estimation and shot-hit suites drop their clock callback (it kept a node past `main`)
  on every exit. Hosted `lifecycle_check.sh --repeat 5`: 100 of 100; early-interrupt hunt: 0 bridge deaths in 1,200
  iterations (3 of 150 before). `tools/bridge_teardown_stress.py` repeats it
  ([sim #78](https://github.com/Thornbots/sim/pull/78), [sim #88](https://github.com/Thornbots/sim/pull/88),
  [sim #89](https://github.com/Thornbots/sim/pull/89),
  [sentry_localization #42](https://github.com/Thornbots/sentry_localization/pull/42)).

- **Behavior change, robots and sim:** with remote DDS off (the default since #185), `auto.launch.py` and the sim launches
  now give every node `thornbots_pkg/config/fastdds_local.xml` (shared memory and loopback UDP, initial peer `127.0.0.1`,
  `maxInitialPeersRange` 128) and no `ROS_AUTOMATIC_DISCOVERY_RANGE`, instead of the `LOCALHOST` range with no profile.
  Under `LOCALHOST` the 37-participant sim stack did not find itself (a hosted `mcb_parked` cell timed out its first
  lockstep hold in a fresh container), and a 32-id range lost a hold in about 2% of runs. Still no packet to
  `100.64.0.0/10` (a defaults-off cell showed none on `docker0`; only gz-transport multicast left the container).
  Not yet run on a robot ([thornbots_pkg #68](https://github.com/Thornbots/thornbots_pkg/pull/68),
  [#69](https://github.com/Thornbots/thornbots_pkg/pull/69), [sim #91](https://github.com/Thornbots/sim/pull/91)).

- Simulation: rf2o's scan odometry no longer varies between runs and its result reaches the
  EKF at a fixed lockstep hold. rf2o gains `extrinsic_lookahead_s` (default 0; the robot is
  unchanged) and `sentry_localization` gains the simulation launch arguments
  `rf2o_extrinsic_lookahead_s` and `scan_navigation_odom_topic`; `sim` adds `scan_odom_gate` and
  the `ekf_pre` chain. The Jetson-to-MCB stream now matches for 800+ lines (was 19) and `/odom`
  for about 26 s (was 14 s). T17 is still open: equal-stamp measurement order inside the stock EKF
  ([investigation](sim/docs/t17-consistent-runs-2026-11-05.md#2026-11-06-pass-2-rf2o-the-ekf-hand-off-and-what-is-left),
  [rf2o #28](https://github.com/Thornbots/rf2o_laser_odometry/pull/28),
  [sentry_localization #43](https://github.com/Thornbots/sentry_localization/pull/43),
  [sim #87](https://github.com/Thornbots/sim/pull/87)).

- Simulation: every Jetson-side producer of a UART frame is now a lockstep chain, so
  frames reach the firmware on a fixed 1 ms step instead of whenever a callback ran.
  `dji_serial_bridge` publishes a TX ack per frame and, in the simulator's
  `sim_tx_queue` mode, writes its frames when the coordinator flushes each hold, in a
  fixed order and gated on the hold time. The coordinator accepts any-of and counted
  ack groups and lagged holds; producers (`point_to_cv_target`, `target_selector`,
  `target_tracker`, `mcb_relay`, `waypoint_nav`) publish a none-mark when they send
  nothing; the MCB plugin holds physics at a delivered POSE until `/odom`, the EKF
  input, the relay and TF carry it. The E2E stack no longer launches `mmm` (its ping
  protocol runs on wall time), sets the stock EKF to a 34 ms period and the tracker to
  a fixed 25 ms processing delay (simulation only; robot defaults unchanged).
  T17 is still open: see the [investigation](sim/docs/t17-consistent-runs-2026-11-05.md)
  for what still differs between runs
  ([bridge #42](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/42),
  [thornbots_pkg #66](https://github.com/Thornbots/thornbots_pkg/pull/66),
  [nav_pkg #3](https://github.com/Thornbots/nav_pkg/pull/3),
  [sentry_localization #41](https://github.com/Thornbots/sentry_localization/pull/41),
  [sim #86](https://github.com/Thornbots/sim/pull/86)).

- Simulation: ROADMAP T17 status recorded. Sim UART, epoch-zero bring-up, stamped TF
  reads, keyed noise and a lockstep harness have landed; runs are still not
  bit-identical because Jetson-to-MCB frames arrive on different 1 ms steps
  ([investigation](sim/docs/t17-consistent-runs-2026-11-05.md),
  [sim #84](https://github.com/Thornbots/sim/pull/84),
  [sim #85](https://github.com/Thornbots/sim/pull/85)).

- The scored simulation harness is now a lockstep chain: it holds physics at a 50 ms
  tick until it has decided, bring-up ends at a fixed 10 s of sim time, cells start
  on whole simulated seconds, and the MCB plugin applies harness parameter changes
  on a known step. `point_to_cv_target` gains `nav_tf_lookup_lag_s` for its
  stamped-TF mode (robot default unchanged)
  ([sim #83](https://github.com/Thornbots/sim/pull/83),
  [thornbots_pkg #65](https://github.com/Thornbots/thornbots_pkg/pull/65)).

- Simulation detector and ghost-aim noise is drawn per (seed, robot, stamp) instead
  of from one shared stream, so it no longer depends on message arrival order
  ([sim #82](https://github.com/Thornbots/sim/pull/82)).

- Simulation E2E stages read `point_to_cv_target`'s TF at a stamp, not the
  newest to arrive, and fail on any miss (`allow_latest_tf:=false`,
  `tf_lookup_lag_s`; the robot keeps reading the newest TF)
  ([thornbots_pkg #64](https://github.com/Thornbots/thornbots_pkg/pull/64),
  [sim #81](https://github.com/Thornbots/sim/pull/81)).

- Simulation E2E stages now start from an epoch-zero barrier by default: gz
  starts paused and is released only once the detector, aim timer, opponents,
  MCB, robot spawn and every stack node are up, so no robot-start or spawn
  timer sets the simulated start time. The EKF starts at epoch zero from the
  spawn team's start (new simulation-only `seed_known_team`; robots unchanged),
  and Renode board runs are accepted by the same path
  ([sim #80](https://github.com/Thornbots/sim/pull/80),
  [sentry_localization #40](https://github.com/Thornbots/sentry_localization/pull/40),
  [thornbots_pkg #63](https://github.com/Thornbots/thornbots_pkg/pull/63)).

- Simulation E2E stages (`mcb_parked`, `mcb_drive`, `mcb_match`) now default to
  coordinated sim-time UART: frames are serialized at bytes x 10 / baud with
  per-frame bridge acknowledgments, and the bridge gates Jetson-to-MCB
  decisions on the same simulated wire. `uart_deterministic:=false` keeps the
  old PTY. Robot UART behavior is unchanged
  ([sim #79](https://github.com/Thornbots/sim/pull/79),
  [bridge #41](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/41);
  [T17 record](sim/docs/t17-consistent-runs-2026-11-05.md)).

- Move aim planning to the MCB. The Jetson now sends the tracked enemy armor
  model as a new 80-byte `TARGET_STATE` UART frame on every tracker update, and
  the MCB does lead, panel choice, spin shot windows, fire lock, confidence and
  detection-age gates, and shot timing every 25 ms. `CV_TARGET` shrinks to a
  13-byte idle look point and can no longer request fire. This breaks wire
  compatibility: deploy firmware and Jetson packages together. Planner tuning
  is now in firmware constants. `auto.launch.py` drops `lead_enabled`,
  `firmware_latency_s`, `chase_settle_s`, `chase_margin_s`, `v_muzzle`,
  `fire_lock_s` and `gimbal_lag_s`, and robot startup drops `EXIT_VELOCITY`
  ([contract](ros2_dji_serial_bridge/UART_PROTOCOL.md#target_state-id7--tracked-enemy-armor-model);
  [MCBV3 #133](https://github.com/Thornbots/MCBV3/pull/133),
  [bridge #40](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/40),
  [thornbots_pkg #61](https://github.com/Thornbots/thornbots_pkg/pull/61),
  [sim #77](https://github.com/Thornbots/sim/pull/77),
  [isaac-ros-startup #26](https://github.com/Thornbots/isaac-ros-startup/pull/26)).
  The aiming bench now models the MCB holding aim while a shot is pending, so
  its moving-target floors drop to about 0.62 with per-shot hit rates
  unchanged. Hosted E2E parked hit rates regressed (speed 4: 2/28 against
  9/15-15/19), most likely because the fixture's zero-lag chase tuning is now
  board-default firmware constants; this is unverified and open
  ([measurement](sim/docs/mcb-aim-planner-2026-11-04.md)).

- Add opt-in strict simulator lockstep startup: it holds to the first positive
  scheduled deadline, stops on missing acknowledgments, and adds an epoch-zero
  readiness barrier with a bounded startup timeout and missing-topic
  diagnostics. The detector acknowledges epoch-zero initialization and consumed
  truth at scheduled capture stamps, rounded up to the next 1 ms physics step
  ([sim #73](https://github.com/Thornbots/sim/pull/73)). Scored T17 acceptance
  and downstream deterministic consumption gates remain open.

- `waypoint_nav` gains an off-field test route: `nav_route:=square` on `auto.launch.py` (or
  `route:=square` standalone) loops a 1 m square from the robot's first localized pose, +x then +y,
  for either team and without referee data. The match route stays the default
  ([nav_pkg #2](https://github.com/Thornbots/nav_pkg/pull/2),
  [bringup #62](https://github.com/Thornbots/thornbots_pkg/pull/62)).

- Sim's hosted MCB plant now round-trips sentry's real pitch encoder offset, counts successive
  physical chamber exits and models the indexer output shaft
  ([sim #76](https://github.com/Thornbots/sim/pull/76)). With it, `mcb_drive` scores hits again on the
  Season 2 field: it had scored 0 because the plant's pitch offset (1.62 rad) did not match the
  firmware's (0.18 rad). Sim only; no robot behavior change.

- **Real-robot behavior:** the sentry's waypoints move from the MCB to the Jetson. `thornbots_nav`'s
  `waypoint_nav`, started by `auto.launch.py` with `real_hardware:=true`, publishes NAV_GOALs. Its route
  runs from the Starting Zone centre, north to the doorway, east through it, and on to a pipes point +y
  of the bucket at (0, −2.4). The robot returns at HP ≤ 55% and heads out again above 99%. Outbound
  steps wait for IN_GAME. The remote's right switch up now schedules the firmware's `AutoDriveCommand`.
  `SimpleAutoDriveCommand` and its onboard routes are removed. The robot holds a field quarter turn
  while travelling, because the 0.745 m doorway is narrower than its spin sweep, and spins only at a
  goal. Flash the matching firmware with this workspace. Older firmware ignores the goals and runs its own route.
  ([nav_pkg](nav_pkg/README.md), [MCBV3 #132](https://github.com/Thornbots/MCBV3/pull/132)).
  Arrival is judged on `/localization/odom`. Not yet run on the robot.

- Season 2 3v3 field: the sim default world, localization `clean_map` and team starts (±5.25, −3.0)
  ([sim #63](https://github.com/Thornbots/sim/pull/63),
  [localization #35](https://github.com/Thornbots/sentry_localization/pull/35),
  [bringup #52](https://github.com/Thornbots/thornbots_pkg/pull/52)). The bucket of pipes and the pipe
  arrangement are CAD estimates.

- Restore green nightly CI: reformat the bridge's coordinated clock callback
  for `uncrustify` ([bridge #38](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/38))
  and refresh all seven portable package CI workspace pins to an integration
  that includes the bridge's `SimFrameMetadata`, so sim's package CI builds.
  No behavior change.

- Extend the E2E epoch-zero diagnostic to `mcb_drive` and `mcb_match`: every
  ghost spawns at its scenario t=0 pose and yaw, and target and match timers
  start at zero ([sim #74](https://github.com/Thornbots/sim/pull/74)). Fixes the
  intermittent Gazebo abort, caused by one test launch's surviving gz server
  latching stale MCB readiness for the next. The aim phase can still slip 1 ms;
  scored acceptance remains open.

- Wire the opt-in parked E2E diagnostic to paused epoch-zero robot and opponent
  scene verification, detector and aim timer initialization, and MCB bootstrap
  before lockstep release ([sim #73](https://github.com/Thornbots/sim/pull/73)).
  The verifier safely tears down its transport callbacks and the diagnostic pins
  the expected timer phases. Scored acceptance and downstream first-data gates
  remain open.

- Add opt-in simulated epoch-zero initialization for the aim publisher’s
  timers, with a latched readiness acknowledgment
  ([thornbots_pkg #59](https://github.com/Thornbots/thornbots_pkg/pull/59)).
  Downstream E2E consumption gates remain open.

- Add opt-in paused epoch-zero UART clock bootstrap: the bridge reports actual
  clock receipt and the simulator waits for it and detector readiness before
  reporting plugin readiness ([bridge #37](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/37),
  [sim #73](https://github.com/Thornbots/sim/pull/73)). Scored acceptance remains open.

- Add an opt-in epoch-zero readiness barrier to strict simulator lockstep
  startup, with a separate bounded startup timeout and missing-topic diagnostics
  ([sim #73](https://github.com/Thornbots/sim/pull/73)). Scored T17 acceptance remains open.

- Add an opt-in paused-world spawn readiness gate to the simulator
  `opponent_driver`: it publishes epoch-zero `~/ready` only after a single
  correctly posed opponent is confirmed in a paused world at sim time zero, and
  exits on collision, wrong pose, nonzero epoch or timeout
  ([sim #73](https://github.com/Thornbots/sim/pull/73)). This does not establish a scored T17 run.

- Add an opt-in strict simulator lockstep startup primitive that holds to the
  first positive scheduled deadline and stops on missing acknowledgments
  ([sim #73](https://github.com/Thornbots/sim/pull/73)). The detector can
  independently acknowledge epoch-zero initialization and consumed truth at
  scheduled capture stamps, rounded up to the next 1 ms physics step; downstream
  deterministic consumption gates are still open.

- Add an opt-in sim-time UART relay fixture with a shared bridge baud for T17;
  Jetson input observed during a firmware cycle is deferred to the next cycle.
  The bridge now provides opt-in verified capture stamps and publication
  acknowledgments ([bridge #37](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/37));
  An experimental opt-in simulator metadata and acknowledgment path is under
  validation; its dedicated ROS clock path emits once per physics step and
  bridge matching is event-driven ([hosted diagnostic](sim/docs/uart-coordination-2026-11-03.md));
  scored integration and match repeatability remain open.

- Firmware developers can send opaque 0–128 byte debug blobs with a nonblocking
  MCB API; the bridge stamps them at estimated UART send start and publishes
  `/dji_serial_bridge/debug`, recorded in normal and match per-run bags.
  Portable ROS CI dependency pins now use the merged T25 workspace revision.
  The bridge includes T20 throttled logs and `Serial link` diagnostics with a
  `debug_msgs_pub` counter ([bridge #34](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/34)).
  Debug uses available UART budget and may delay one telemetry frame by up to
  10 ms while preserving all 90 Hz POSE / 10 Hz REF_SYS slots;
  scheduler service gaps over 100 ms restart a fresh cycle instead of replaying
  paused deadlines; no production values or sender are enabled. Deploy matching firmware and
  bridge revisions together ([wire contract](ros2_dji_serial_bridge/UART_PROTOCOL.md#debug-id6--opaque-firmware-debug),
  [bridge #35](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/35),
  [startup #23](https://github.com/Thornbots/isaac-ros-startup/pull/23),
  [MCBV3 #130](https://github.com/Thornbots/MCBV3/pull/130),
  [sim #62](https://github.com/Thornbots/sim/pull/62),
  [hosted verification](sim/docs/mcb-debug-bag-2026-11-01.md)).
- Correct Season 2 side-wall face placement, preserve the central-road 15 mm printed-chain conflict, and clarify pole-height and building-spec page authority.
- Transcribe [Season 2 rule figures and power audit](docs/rules/season2-geometry.md), separating printed dimensions, derived placements and implementation estimates; retain unpublished-source and package acceptance under DOC14g/RULES-S2.

- Separate sim README experiment narratives into [dated history](sim/docs/simulation-history-2026-11-02.md), retaining current instructions and compatibility headings ([sim #71](https://github.com/Thornbots/sim/pull/71), DOC14f; independently reviewed and completed).

- Estimation harness reset acknowledgement ordering and scorer pacing handoffs
  are corrected without changing scored watchdogs or numeric limits
  ([sim #68](https://github.com/Thornbots/sim/pull/68),
  [validation status](sim/docs/de-harness-2026-11-02.md)).

- The sim suite wrapper and T3 shortcuts use `localization_drift`, `ekf`, `aim` and `tracking`; `mcb_*` stage names are unchanged ([sim #65](https://github.com/Thornbots/sim/pull/65), [sim tests](sim/README.md#run-the-tests)).

- Unfinished plans, package open-work lists and dated follow-ups now route to two canonical homes;
  [consolidation coverage](docs/audits/open-work-consolidation-2026-11-02.md) records sources and dependencies, including distinct T23 visibility/visualization/head stages corrected H scan-bag provenance, and complete T17 suite-order/no-wall-time-sleep gates. Distinct mapping duplicate-graph and transient save-freshness investigations remain explicitly open with source evidence and acceptance.
- Open work now separates unfinished Mini/software/sim tasks in [ROADMAP](docs/ROADMAP.md) from physical validation in [ROBOT_TESTS](docs/ROBOT_TESTS.md). Completed items are removed after integration; final completion also requires a separate full automated-suite pass on integrated nightly.

- Document [rf2o fork usage](rf2o_laser_odometry/README.md#thornbots-fork-and-usage), move [October 3 parked results](sim/docs/mcb-parked-results-2026-10-03.md) into a dated report, and narrow the [remaining documentation audit](docs/ROADMAP.md#issues-found) with sourced Season 2 match timing ([rf2o #23](https://github.com/Thornbots/rf2o_laser_odometry/pull/23), [sim #64](https://github.com/Thornbots/sim/pull/64)).

- Adding a package submodule no longer needs a `reviewed_history` line; the policy hook and CI trust the imported history and check later bumps ([policy](docs/CI.md#repository-policy)).

- New [`nav_pkg`](https://github.com/Thornbots/nav_pkg) package submodule (tracks `nightly`); it now holds `thornbots_nav` (below), built and tested by workspace ROS CI.

- Low-space startup pruning explicitly protects the active run even with zero retained runs. Regression tests prove oldest-first bag/log deletion, stopping when space recovers, retention, and active-run/latest-link preservation ([startup #22](https://github.com/Thornbots/isaac-ros-startup/pull/22), [pruning](isaac-ros-startup/README.md#design-notes)).

- Repeated rf2o warnings now show the first event and sample repeats every five seconds, retaining totals in log samples and publishing counters under stable event IDs in match-quality diagnostics ([rf2o #21](https://github.com/Thornbots/rf2o_laser_odometry/pull/21), [warning logs](rf2o_laser_odometry/README.md#warning-logs)).

- Bridge referee and CRC logs now sample repeats every five seconds while retaining lifetime counters; rare RELOCALIZE corrections and operator PING checks log every event. Standard ROS `/diagnostics` reports interval-based serial health and every DIAG counter, including recovery and stalled links ([bridge #34](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/34), [levels](ros2_dji_serial_bridge/README.md#diagnostics)).

- The [Sentry rules context](docs/ARCC_2026_SENTRY_CONTEXT.md) now follows the ARCC Season 2 (2027) manuals V1.0 of 2026-11-01 instead of ARCC 2026. Changes that matter to the robot: the 3v3 Sentry chassis limit drops to 80 W, there is a new Sentry Tournament (5×5 m, 120 W, 250 rounds, 2 minutes, no respawn, healing from damage dealt), armor hit faces are dot-matrix screens (style not yet published), the 3v3 field has Limbo Bars (420/300 mm) and object-scoring with Scoring-Area Penalty Zones instead of a Capture Point, and the Sentry weight limit is 28 kg including the referee system. Firmware, sim and nav defaults have not been changed yet.

- Robots now use an explicitly pulled registry image as their dependency base and build current source as an offline overlay. Startup pins the prepared image and rejects missing or shadowed overlay packages; image publication also checks the offline build. Ordinary source changes no longer require image builds or pulls. Local image building/shipping is an emergency fallback; equipped-robot startup acceptance remains open ([common #21](https://github.com/Thornbots/isaac_ros_common/pull/21), [startup #24](https://github.com/Thornbots/isaac-ros-startup/pull/24), [workflow](isaac_ros_common/docker/README.md#building-the-robots-image), [Orin measurements](docs/investigations/robot-overlay-2026-11-01.md)).

- The sentry and infantry MCB pitch solver (same gimbal) no longer shoots high close and low far: it uses the CAD pivot height and bore length (0.4035 m, 0.173 m) instead of the 0.28 m height retune, adds horizontal drag, and corrects a 0.042 rad shot launch bias fit to robot misses at 1 m and 3 m; confirmed on the sentry. Refit the bias, not the pivot height, if a range-dependent miss remains ([MCBV3 #127](https://github.com/Thornbots/MCBV3/pull/127), [aiming](firmware/MCBV3/README.md#aim-and-navigation-odometry)).

- The Jetson now owns independent `red_start_x/y` and `blue_start_x/y` launch configuration, overridable per robot through `/etc/thornbots/launch.env`. Navigation, EKF/AMCL/saved-map SLAM priors, idle enemy-zone looks and operator registration use the same values. Defaults remain the unmeasured scrim starts ([ROADMAP T40](docs/ROADMAP.md#short-todos)). Firmware routes use field-centred coordinates and return to the boot point the Jetson's RELOCALIZE places, even after a mid-match reschedule; PURDUE2V2 is removed. Hosted firmware no longer sends a start in its simulator handshake; sim keeps its ARCC spawn and passes matching launch arguments to bringup ([MCBV3 #128](https://github.com/Thornbots/MCBV3/pull/128), [#129](https://github.com/Thornbots/MCBV3/pull/129), [localization #33](https://github.com/Thornbots/sentry_localization/pull/33), [bringup #50](https://github.com/Thornbots/thornbots_pkg/pull/50), [sim #61](https://github.com/Thornbots/sim/pull/61), [UART docs #33](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/33), [startup #21](https://github.com/Thornbots/isaac-ros-startup/pull/21)).

- Firmware tuning from the robots: every robot's flywheel PID returns to the earlier `{30, 0.1}`; hero flywheel max 4600 RPM (about 11.5 m/s); hero and standard drive without spin-follow and with a zero yaw offset (no yaw encoder; only the sentry reads one); sentry and standard pitch-down limit 5° (was 21°), sentry pitch offset 0.18 (was 0.52); hero bottom indexer on motor 7; sentry and standard aim projection offsets adjusted (sentry still aims high up close and low far away). Not covered by tests ([MCBV3 nightly](https://github.com/Thornbots/MCBV3/compare/e708e50...533642d)).

- MCBV3 dev container: one config that mounts the whole workspace, so git and the policy hooks work from `firmware/MCBV3` (standalone clones are no longer supported); CMSIS-DAP hardware debugging targets the STM32F407IG and the selected robot; `.vscode` drops stale Windows-only settings ([MCBV3 #121](https://github.com/Thornbots/MCBV3/pull/121), [#122](https://github.com/Thornbots/MCBV3/pull/122), [#123](https://github.com/Thornbots/MCBV3/pull/123), [README](firmware/MCBV3/README.md)).

- `fire_lock_s` (same-track dwell before firing, default 1.0 s) is now an `auto.launch.py` argument, so a robot can set it in `launch.env`'s `AUTO_LAUNCH_ARGS` ([thornbots_pkg #48](https://github.com/Thornbots/thornbots_pkg/pull/48)).

- Sentry's lidar is now mounted upside down. A new `lidar_inverted` launch arg (default `true`) sets the driver's `inverted` flag, and the defaults move to the Oct 31 CAD mount: yaw 2.579 rad, self-filter -1.927..-0.171 rad. The robot needs this to localize and map again. Nose-up/down sectors and a head-turn fit still need measuring ([thornbots_pkg #47](https://github.com/Thornbots/thornbots_pkg/pull/47), [sim #59](https://github.com/Thornbots/sim/pull/59), [measurement](docs/investigations/lidar-flip-2026-10-31.md)).

- Commit signing is no longer required: the policy hooks and CI `policy` job drop the signature and `commit.gpgsign` checks, so unsigned commits push and pass. Gitlink fast-forward, reviewed-history and `.msg` stamp checks are unchanged ([repository policy](docs/CI.md#repository-policy)).

- The sentry MCB's raw odometry and aim now boot at `(0, 0)` for either team, both facing the field's +y (`pi/2`), and the Jetson relocalizes navigation from the referee team's start. EKF seeding, passthrough navigation and AMCL wait for a valid REF_SYS team, then start at red `(-4.625, 0)` or blue `(4.625, 0)`; `mcb_relay` sends each confident absolute fix four times at least 0.3 s apart, so a lost first frame recovers. Firmware routes, position commands and NAV_GOAL driving stay off until the first RELOCALIZE. On the robot, navigation does not start without referee team data; the `initial_x/y` and `amcl_initial_*` launch arguments are deprecated and ignored. MMM parking checks measure from that raw zero. Sim fixtures model the zero raw boot, and the drift and parked E2E suites drive from the team start to center before scoring ([MCBV3 #119](https://github.com/Thornbots/MCBV3/pull/119), [thornbots_pkg #42](https://github.com/Thornbots/thornbots_pkg/pull/42), [sentry_localization #30](https://github.com/Thornbots/sentry_localization/pull/30), [ros2_dji_serial_bridge #30](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/30), [sim #58](https://github.com/Thornbots/sim/pull/58), [startup relocalization](ros2_dji_serial_bridge/UART_PROTOCOL.md#message-types)).

- The robot service's Foxglove bridge takes a `FOXGLOVE_ADDRESS` listen IP (default `0.0.0.0`, unchanged); `192.168.55.1` exposes it only on the USB tether ([isaac-ros-startup #20](https://github.com/Thornbots/isaac-ros-startup/pull/20), [watch live](isaac-ros-startup/README.md#use)).

- Field mapping now follows MMM: the root README "Map a new field" procedure is removed, the [Notion mapping doc](https://app.notion.com/p/fff357611caa4131b216742bb7c6e048) covers the MMM operator steps with a [state diagram](docs/images/mmm-states.png), MMM drivers need no speed rule because the MCB caps drive speed, and the manual workflow allows 0.4 m/s instead of 0.2 m/s ([thornbots_pkg #44](https://github.com/Thornbots/thornbots_pkg/pull/44)).

- MMM validated saves now allow re-parking within 0.50 m and 15° of the
  SLAM boot pose, with 0.60 m/18° exit hysteresis and a 0.50 m raw-odometry
  spawn guard. Boot capture still requires raw odometry within 0.30 m of the
  team start; parked stability and chassis-yaw checks are unchanged
  ([thornbots_pkg #45](https://github.com/Thornbots/thornbots_pkg/pull/45),
  [MMM](thornbots_pkg/README.md#mcb-mapping-machine)).

- Agents may restart a robot's `thornbots` stack without asking; other physical-robot runs still need approval ([AGENTS](AGENTS.md#containers-and-runs)).

- CV firing now waits for one second of confident tracking of the
  same robot (`fire_lock_s`), with an immediate bypass for nonspinning targets
  below `fire_stationary_speed_mps` (0.1 m/s). Brief stale, unconverged or
  low-confidence gaps on the same track preserve the timer for
  `fire_lock_grace_s` (0.3 s); gap time counts, but firing remains blocked.
  Longer gaps, target timeout or switched tracks restart the wait. The minimum fire exit
  delay increases from 25 to 40 ms to give the gimbal time to acquire each aim
  ([thornbots_pkg #43](https://github.com/Thornbots/thornbots_pkg/pull/43)).

- The robot service starts again on images with the in-stack MMM coordinator: `auto.launch.py` failed with `launch configuration 'real_hardware' does not exist` whenever `real_hardware` was not passed, and `thornbots-launch.sh` stopped YOLO with it, so the service restart-looped. Sim always passed the argument ([thornbots_pkg #41](https://github.com/Thornbots/thornbots_pkg/pull/41)).

- Each robot's stack now defaults to its own `ROS_DOMAIN_ID`: sentry 7, standard 3, hero 1, chosen by hostname when `launch.env` leaves it blank. Sharing domain 1 over the tailscale peers let the sentry's `ref_sys` and TF reach standard, flipping its team colour filter. Shells joining a robot export its domain; the image's shells still start on 1 ([isaac-ros-startup #18](https://github.com/Thornbots/isaac-ros-startup/pull/18), [domain per robot](isaac-ros-startup/README.md#design-notes)).

- Hero and standard MCBs now send POSE with x/y/velocity 0 and `odom_status` 2, so the Jetson gets gimbal angles and an `odom` frame for CV aiming; before, they sent only REF_SYS and standard's tracker had no frame ([MCBV3 #117](https://github.com/Thornbots/MCBV3/pull/117), [UART protocol](ros2_dji_serial_bridge/UART_PROTOCOL.md#pose-id2--chassis-pose-and-gimbal-angles), [ros2_dji_serial_bridge #29](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/29)). The same MCBV3 pin re-enables standard's auto-fire on left switch up (right mouse aims manually), lets a new CV target that wants to fire replace a pending one that doesn't, and corrects standard's pitch offset (0.32 to 1.26 rad), which had tilted its camera TF about 60° off.

- The sentry now localizes with AMCL on the saved map by default instead of
  mapping from a blank graph: `auto.launch.py`, `localization.launch.py` and
  the service's `LOCALIZATION_MODE` default to `amcl`. MMM sessions still need
  `LOCALIZATION_MODE=mapping`; existing `/etc/thornbots/launch.env` files keep
  their value ([thornbots_pkg #40](https://github.com/Thornbots/thornbots_pkg/pull/40),
  [sentry_localization #29](https://github.com/Thornbots/sentry_localization/pull/29),
  [isaac-ros-startup #17](https://github.com/Thornbots/isaac-ros-startup/pull/17),
  [sim #57](https://github.com/Thornbots/sim/pull/57)).

- Add an opt-in [match Wi-Fi guard](thornbots_pkg/README.md#match_wifi_guard)
  and [host disconnect watcher](isaac-ros-startup/README.md#match-wi-fi-disconnect-opt-in):
  three consecutive referee battle messages disconnect every Wi-Fi device
  until reboot. Default launches remain unaffected. A host eduroam helper
  reuses system profiles and prioritizes autoconnect without handling passwords
  ([thornbots_pkg #38](https://github.com/Thornbots/thornbots_pkg/pull/38),
  [isaac-ros-startup #16](https://github.com/Thornbots/isaac-ros-startup/pull/16)).

- Mapping save-now now finishes staging cleanup before reporting completion,
  including collision and backend failures. Timeout failures still respond
  promptly and keep the saver busy until the backend replies and the abandoned
  staging directory is removed ([sentry_localization #27](https://github.com/Thornbots/sentry_localization/pull/27)).

- CV targeting now requests fire on every eligible 40 Hz publish tick instead
  of throttling requests to 2 Hz; the MCB filters pending requests. Confidence,
  detection freshness, planner shot windows and the 25 ms default delay floor
  remain in force ([thornbots_pkg #37](https://github.com/Thornbots/thornbots_pkg/pull/37)).
  The sim aiming bench uses the same policy without a fire-rate override
  ([sim #55](https://github.com/Thornbots/sim/pull/55)).

- The workspace [AGENTS](AGENTS.md) no longer sets delegation rules; agents follow their own harness and user defaults.
- Sentry MMM now owns indicators and restrictions in its command, keeps odometry pods pointing in every mapping state while the remote is connected, and services pings through Jetson UART refresh ([MCBV3 #111](https://github.com/Thornbots/MCBV3/pull/111)). Turning the remote off now stops every motor, gimbal and pods included, without leaving the mapping state ([MCBV3 #114](https://github.com/Thornbots/MCBV3/pull/114)).
- Sentry MMM starts from the controller: left switch down and the right stick held up for 5 s. Inside MMM, each later 5 s hold (after a release) tries to save; no input leaves MMM ([MCBV3 #113](https://github.com/Thornbots/MCBV3/pull/113), [firmware README](firmware/MCBV3/README.md#mcb-mapping-machine-sentry)).

### Added

- The Mac mini's [nightly run](docs/CI.md#nightly-tests) now builds and tests
  the robots' JetPack image on the registry's shared base layers after a local
  PASS, publishing immutable workspace SHA and nightly tags with bounded local
  cache and old registry-tag cleanup. Containerd base content is fetched before
  retagging so snapshot reuse cannot send missing-blob export requests to nvcr.

- A [hosted MMM end-to-end suite](sim/README.md#run-the-tests) connects the
  compiled sentry firmware to the real bridge and in-stack mapping node, covering
  telemetry load, UART faults/backpressure, restarts, restrictions and validated
  saving. Start/save inputs are private to the hosted fixture; the hardware
  target excludes the hook. [Mini validation](docs/investigations/mmm-firmware-e2e-2026-10-29.md).

- The C++ [`mmm` node](thornbots_pkg/README.md#mcb-mapping-machine) now starts
  inside `auto.launch.py` with the normal stack. It resets the live mapping graph,
  captures stationary boot evidence, sends setup-failure PING 6, and delegates
  asynchronous map writing to localization's new save-now service. Ready saves
  remain guarded until durable completion; failed saves return the MCB through
  4 then 2. The manual Python workflow is restored without MMM/snapshot commands.
  Transient bad lidar scans now restart fresh evidence instead of permanently
  blocking saves. Fresh start requests create another session; starts during
  a save send setup failure without interrupting the save. Startup forwards
  the shutdown opt-in into the mapping node.
  Host shutdown is explicitly opt-in through startup's fixed request-file watcher;
  incomplete saves never request shutdown. See the
  [validation record](docs/investigations/mmm-node-validation-2026-10-29.md).
  Revalidated after merging nightly `33d0ef8` on the Mac mini: ROS reports
  612 tests, zero errors/failures and 11 skips; the updated MMM integration
  flow passes. GCC 14 firmware unit/control tests and all 95 UART fixture
  cases pass, as do the eight Linux startup tests and host quality checks.
  [PING contract](ros2_dji_serial_bridge/UART_PROTOCOL.md#ping-id5--mcb-mapping-machine-and-link-check)
  specifies ACKs for every peer-originated 1/3 or 2/4/6 in any state, including
  retries and final legs; originators send a final leg only once while awaiting
  the matching echo, then ignore further echoes to terminate the exchange.
  Odd retries use intervals >=0.5 s; the sliding five-second same-number
  window gates work only, ACKing distinct requests within it without execution.
  Main-only reply 0 remains the exception; unknown numbers are never echoed.
  Sentry firmware retries unacknowledged 1/3 every 500 ms and ignores late odd
  echoes, including ACKs of its final leg. The sim fixture runs this firmware
  and checks Main-only 0, unknown-number rejection and unconditional 2/4/6 ACKs.
  PING 4 returns Done to Mapping after a failed final save, restoring restricted
  manual drive and cancelling pending/queued save work. PING 6 (fail) moves
  Setup to Done and stops start retries; Done keeps drive stopped and head forward.
  The UART payload is unchanged; save ACK permits
  independent MCB-side power-off before storage completes, so data loss remains possible.
  [thornbots_pkg #35](https://github.com/Thornbots/thornbots_pkg/pull/35),
  [bridge #26](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/26),
  [localization #26](https://github.com/Thornbots/sentry_localization/pull/26),
  [startup #15](https://github.com/Thornbots/isaac-ros-startup/pull/15),
  [MCBV3 #111](https://github.com/Thornbots/MCBV3/pull/111),
  [sim #54](https://github.com/Thornbots/sim/pull/54).

- Operator workflow now lives in `thornbots_pkg`: use
  `ros2 run thornbots_pkg operator_workflow` with the existing subcommands and
  flags. Mapping/localize also supervise the image-provided read-only Foxglove
  bridge on port 8765 and stop it with the workflow. The operator reference,
  tests, startup link and mirrored mapping card follow the new package;
  localization gates and robot movement are unchanged.
  [thornbots_pkg #33](https://github.com/Thornbots/thornbots_pkg/pull/33),
  [sentry_localization #24](https://github.com/Thornbots/sentry_localization/pull/24),
  [startup #12](https://github.com/Thornbots/isaac-ros-startup/pull/12);
  [validation](docs/investigations/operator-workflow-move-2026-10-27.md).

- Clarify the [field-mapping procedure](docs/investigations/mapping-procedure-2026-10-26.md): boot-pose
  provenance and SLAM save gate, session/room terms, still-head and slow-drive
  checks, controller continuity, and post-flash power/clock/container recovery.
  The [package workflow](https://github.com/Thornbots/sentry_localization/pull/23)
  owns the gate rationale; match boot keeps rf2o off
  after false-motion head-sweep replay findings.

- Launch-time lidar translation/yaw and scan-frame blind-sector overrides,
  including sectors across scan zero. Defaults use the Oct 26 CAD mount and
  robot-measured scan zero/self-filter; the spawned sim sensor matches the TF
  ([thornbots_pkg #32](https://github.com/Thornbots/thornbots_pkg/pull/32),
  [sim #50](https://github.com/Thornbots/sim/pull/50),
  [measurement and validation](docs/investigations/lidar-mount-2026-10-26.md)).

- Complete [Map a new field](docs/investigations/mapping-procedure-2026-10-26.md) operator procedure,
  deliberately mirrored to the Notion mapping doc: stop boot mapping, synchronize
  the clock, capture/map/save/register, check AMCL and configure/recheck match boot.
  Ten steps use the baked release image (verified by image ID), explicit manual
  head controls and CV suppression, plus Oct 25 odometry/head-motion gates and a
  technical reference correction ([sentry_localization #21](https://github.com/Thornbots/sentry_localization/pull/21)).
  [Verification](docs/investigations/mapping-procedure-2026-10-26.md) records the
  isolated room-sim rehearsal and remaining robot-side acceptance. No behavior changes.

- [CAD odometry pod identities](docs/investigations/sentry-cad-2026-10-26.md#odometry-pods),
  with wheel positions, rolling directions and firmware encoder/field signs.
  Firmware and Oct 25 motion data establish the start-frame axes; the missing
  motor-to-CAD yaw datum limits source-part assignment. The models omit the pods.

- Passive parked room health checks with dated evidence and PASS/FAIL/SKIP for
  serial/head TF rates, scan geometry, rf2o output, stamps and stationary drift,
  plus optional camera and stale-CV blocks
  ([thornbots_pkg #26](https://github.com/Thornbots/thornbots_pkg/pull/26)).
  Run from the robot container using the
  [bring-up command reference](thornbots_pkg/README.md#parked-room-health-check);
  the observer issues no motion commands or MCB probes.

- Container-terminal room/field SLAM snapshot, occupancy registration and AMCL
  convergence workflow, with live raw-odometry EKF seeding and measured AMCL starts
  ([sentry_localization #16](https://github.com/Thornbots/sentry_localization/pull/16),
  [thornbots_pkg #24](https://github.com/Thornbots/thornbots_pkg/pull/24)).
  Room and flat central-field sim rehearsals are in the
  [initial results](docs/investigations/fieldday-slam-amcl-2026-10-22.md).
  Full-field mapping uses level observation stations with `pause`/`resume`
  scan insertion; field mapping and localization default to raw wheel input
  (`--rf2o` opts in). A sim full-field map reached 97.55% `clean_map` coverage
  and passed raw-input AMCL parked/drive gates; see the
  [follow-up](docs/investigations/fieldmap-divergence-2026-10-22.md).
  The operator card now uses one session directory, derives the referee team,
  rejects wrong-side/heading registrations and stale boot captures, retains
  separate autosave backups, warns on unsaved stops, and runs parked gates
  automatically during localization. No firmware or movement changes.
  Both team-start rehearsals passed after nonzero registration and restart;
  see the [operator safety results](docs/investigations/fieldday-operator-safety-2026-10-22.md).
  Room sessions now capture and prepare without referee input (`robot_id: 0`);
  practice fields can explicitly select `--no-referee --team red|blue` while
  retaining the raw-odometry start check.
  Field startup now verifies team/start before the backend and gates EKF seeding
  on referee re-anchoring; field maps support either live team. Contract starts
  are the default, surveyed refinements are bounded to 0.3 m, automatic parked
  gates use 3 s freshness, and EKF/unsaved-launch exits are supervised explicitly.
  After save, the NEXT prompt selects `prepare-room` for room sessions and the
  yaw-only alignment step for fields.
  See the [round-2 validation and remaining limits](docs/investigations/fieldday-round2-2026-10-23.md).

- Lidar range documentation and a real-format rf2o test. No behavior change:
  the 0.15 m SLAM/AMCL range floor stays (the A2M8 minimum is 0.05 m; the
  self-filter's body coverage is unproven on hardware, see
  [sentry_localization #11](https://github.com/Thornbots/sentry_localization/pull/11)),
  rf2o gains a 720-beam -pi..+pi scan test
  ([rf2o #11](https://github.com/Thornbots/rf2o_laser_odometry/pull/11)), and stale
  sim/lidar text is corrected
  ([thornbots_pkg #20](https://github.com/Thornbots/thornbots_pkg/pull/20),
  [sim #34](https://github.com/Thornbots/sim/pull/34)).

- Untested step-by-step setup for running the Isaac ROS container on Windows
  with Docker Desktop on WSL2; an NVIDIA GPU is required. See
  [Windows (WSL2)](isaac_ros_common/docker/README.md#windows-wsl2),
  [isaac_ros_common #9](https://github.com/Thornbots/isaac_ros_common/pull/9),
  [#10](https://github.com/Thornbots/isaac_ros_common/pull/10) and
  [#11](https://github.com/Thornbots/isaac_ros_common/pull/11).

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

- `firmware/MCBV3` is now a default submodule: `clone --recurse-submodules`
  and `submodule update --init` fetch it (robot firstboot included). It stays
  out of colcon and the image; [skip it](README.md#mcb-firmware) per checkout.
- Firmware: controller-driven IMU recalibration on hero, infantry and sentry;
  sentry left switch DOWN looks by joystick with an offset, and auto-aim takes
  newMain's CV tuning (pivot-space target offsets, 20 ms firing latency now also
  on infantry, unmeasured there). Shot speed stays 22 m/s and the RMUL 3v3
  pre-match referee gate stays active. Untested on a robot
  ([MCBV3 7c524a9](https://github.com/Thornbots/MCBV3/commit/7c524a9)).
- MCBV3 shared headers now live at `MCB-project/src/util/HitTracker.hpp` and
  `MCB-project/src/util/MappingMachine.hpp`; includes and current firmware
  coordination docs use the matching paths. Firmware behavior is unchanged.
- MCBV3 IMU recalibration now lives in `MCB-project/src/util/ImuRecalibration.hpp`; class text and behavior are unchanged.

- Correct the hosted parked E2E idle-look zone to match its existing scene
  frame, restoring camera acquisition after patrol removal without changing
  paths or acceptance gates ([evidence](docs/investigations/sentry-cad-2026-10-26.md#e2e-idle-zone-regression)).
- Refresh the [Sentry rules context](docs/ARCC_2026_SENTRY_CONTEXT.md) against
  ARC 2026 V1.6 / building diff V1.3.1 and RMUS/RMUL 2027 V1.0.0; correct
  armor citations, distinguish actual rule changes from stale 2024 values,
  and flag the English 2026 basis and October 31 event rules as unconfirmed.
  ARC's September 2027 preview is separate from the RMUL comparison.
- Adopt the team's 2026-10-26 low-resolution sentry CAD for robot/sim head,
  lidar, IR camera, muzzle and armor geometry, with a matching self-filter and
  nominal map-slice height
  ([thornbots_pkg #30](https://github.com/Thornbots/thornbots_pkg/pull/30),
  [sim #48](https://github.com/Thornbots/sim/pull/48),
  [sentry_localization #20](https://github.com/Thornbots/sentry_localization/pull/20)).
  The lidar moves only 16.6 mm in XY. The Oct 26 five-pose robot fit replaces
  the authored FOV-marker yaw (-8.568°) with scan zero 0.5907 rad (33.84°)
  and the verified scan-frame blind sector -0.5585..1.0123 rad. The
  [dated investigation](docs/investigations/sentry-cad-2026-10-26.md)
  records the archive SHA256, frame derivation and before/after tests.
  Round 2 preserves the muzzle's pitch-axis aiming contract with the CAD
  lateral offset; the unchanged aiming acceptance tests now pass. Independent
  mesh checks establish a 103.885 mm armor lower-edge stagger in the supplied
  CAD, exceeding the 2027 manual's physical S124 limit of 100 mm. Accepted
  on 2026-10-26 as a mechanical deviation with no material CV impact; the
  sim test pins a temporary 104 mm bound until the plates are corrected.
  The earlier position-only fit's 10.6 cm discrepancy is retained as provenance;
  the joint fit supports the CAD radius and measured scan-zero orientation.
  The armor spread is no longer a merge blocker. Keep the integration draft;
  scan-plane height and estimator robustness remain separate acceptance work.

- Raise host quality tooling to pytest 9.0.3 for CVE-2025-71176 (insecure
  temporary-directory handling), retaining the other tooling pins. Package CI
  uses the patched tooling snapshot; the native Mac environment now requires
  pytest >=9.0.3 and locks 9.1.1
  ([isaac_ros_common #19](https://github.com/Thornbots/isaac_ros_common/pull/19)).
  Firmware CI remains on its existing snapshot.

- Removed `docs/JAZZY_FLASH.md` now that all four Orins run JetPack 7.2.1/Jazzy;
  it remains in git history. Remaining robot acceptance and the `ROS_DOMAIN_ID`
  0 switch are [robot acceptance T38](docs/ROBOT_TESTS.md#robot-acceptance).

- Stop tracing installer and firstboot commands that load provisioning
  credentials into journals ([package change](https://github.com/Thornbots/isaac_ros_common/commit/f498503783de23e98e6e9ea9f9ea1dab5a698b4b)).
  Rebuild existing installer ISOs to include this change.

- Complete the [local firmware check instructions](docs/CI.md#local-checks-for-prs-into-nightly)
  by linking the GCC 14 unit tests, hosted build and hosted UART/control tests.

- Replace the Jetson head patrol with idle looks (stage 1 of the
  [lidar-guided aiming design](docs/lidar-guided-aiming-2026-10-25.md)). With no
  camera target the head holds the last enemy for 3 s, holds where a hit turn
  left it for 2 s, then faces the enemy starting zone (`auto.launch.py`
  `idle_direction:=zone|hold`). The patrol launch argument is gone. Every
  non-target frame is non-firing with `turn_to_hit` set. Firing now requires a
  detection at most 0.15 s old (new `TargetState.detection_stamp`), and
  `room_check` `stale_cv` is diagnostic only. The wire format and firmware are
  unchanged ([thornbots_pkg #28](https://github.com/Thornbots/thornbots_pkg/pull/28),
  [ros2_dji_serial_bridge #21](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/21),
  [sim #45](https://github.com/Thornbots/sim/pull/45)).

- Clean up the YOLO bridge package description and RealSense configuration:
  remove an unused JSON preset and Humble-only bare `profile` keys. Launch
  behavior is unchanged. See
  [YOLO bridge #6](https://github.com/Thornbots/realsense-yolov8-nitros-bridge/pull/6)
  and [workspace #38](https://github.com/Thornbots/thornbots_workspace/pull/38).

- Simulation and AMCL use the corrected field export, including the restored
  bar near y = +3 m. Localization ships one canonical `clean_map`, regenerated
  at 2 cm resolution with one-cell obstacle growth; the alternate map and old
  annotated image are removed. The map YAML and localization tuning stay
  unchanged. See [sim #37](https://github.com/Thornbots/sim/pull/37),
  [field geometry](sim/README.md#the-world-frame),
  [saved map](sentry_localization/README.md#saved-map) and
  [sentry_localization #14](https://github.com/Thornbots/sentry_localization/pull/14).
  At integration, host geometry and 16 map checks passed, the portable
  workspace built and all 267 sim/localization colcon tests passed. Subsequent
  runtime checks exposed head-slew localization errors, addressed by the
  parked-localization fixes below; the map itself was not the cause.

- Simulation uses the real field assembly (sim #29) for Gazebo geometry and
  match shot occlusion while preserving the field frame. This initial
  integration preceded the corrected export and regenerated map above; it
  does not establish clearance for every firmware route. See
  [the sim world frame](sim/README.md#the-world-frame) and
  [sim #30](https://github.com/Thornbots/sim/pull/30).

- Sim lidar uses the measured angle-compensated sentry A2M8 grid (720 bins),
  range limits and cadence, with scan timing and infinity return handling
  before the shared self-filter. Model approximations remain documented at the
  [sensor owner](sim/README.md#lidar-format-and-model-limits)
  ([sim #31](https://github.com/Thornbots/sim/pull/31)).

- The sim MCB emulator's PTY link is unique per stack
  (`/tmp/mcb_emulator_pty-<GZ_PARTITION>-<ROS_DOMAIN_ID>`), so concurrent sim
  stacks no longer steal each other's UART; a link owned by a live stack is
  refused, except when a stale link points to the new stack's own reused PTY
  (see the fix below). Sim only; no robot or wire change
  ([sim #32](https://github.com/Thornbots/sim/pull/32)).

- The sentry drivetrain matches `main` again: the default stop command cuts
  wheel current and centred manual drive holds a zero wheel-velocity setpoint;
  the earlier nightly latched pod-position hold was removed. The sim
  parked-hold checks pin that behaviour. Nightly's chassis-power and peek gates moved to
  `feat/drivetrain-power-and-peek-gates`. See
  [MCBV3 #98](https://github.com/Thornbots/MCBV3/pull/98) and
  [sim #28](https://github.com/Thornbots/sim/pull/28).

- Each agent task makes and removes its own container (`isaac-agent-<task>`)
  instead of attaching to the user's, with a unique ROS domain, gz partition,
  worktree mount and build volumes enforced by `agent_container.sh`; stale ones
  are cleaned by label. On the Mac mini Colima runs only while an agent
  container does ([AGENTS](AGENTS.md#containers-and-runs),
  [skill](.claude/skills/isaac-ros-docker/SKILL.md#your-own-container),
  [isaac_ros_common #12](https://github.com/Thornbots/isaac_ros_common/pull/12)).

- Full GitHub CI and robot-image builds run on `main` pushes, PRs into
  `main` and manual dispatch; `nightly` runs its tests
  each night on the Mac mini (hosted firmware, colcon tests and the
  `mcb_parked`/`mcb_drive` sim E2E, then a dispatch of GitHub CI on nightly).
  PRs into `nightly` run no CI; authors run the
  [local checks](docs/CI.md#local-checks-for-prs-into-nightly) first.
  Build a nightly image on demand with `gh workflow run`; see
  [Nightly tests](docs/CI.md#nightly-tests) and the package PRs
  (e.g. [sim #36](https://github.com/Thornbots/sim/pull/36)).
- USB installs now hand boot control back to the installed NVMe after
  NVIDIA's boot-order rewrite, remove the temporary installer entry, and
  validate passwordless sudo ([package change](https://github.com/Thornbots/isaac_ros_common/commit/daddcde43b663f811de1e7d80c29894a25d4f182)).
  Rebuild existing installer ISOs to include the fix. Reflash guidance adds
  the serial-console route,
  reinstall-loop diagnosis, safe capsule-variable writes and corrected ISO paths.
- The installer's NVMe boot entry now uses a full hardware device path
  ([1ebf714](https://github.com/Thornbots/isaac_ros_common/commit/1ebf714),
  [bb8ba8a](https://github.com/Thornbots/isaac_ros_common/commit/bb8ba8a)):
  after the 39.2.1 firmware update, short `HD()` entries fail to boot. Firstboot
  marks host setup done only after it succeeds
  ([4f8616b](https://github.com/Thornbots/isaac_ros_common/commit/4f8616b)) and
  waits for tailscaled before logging in
  ([c95e286](https://github.com/Thornbots/isaac_ros_common/commit/c95e286)).
  Standard now runs JetPack 7.2.1 on firmware 39.2.1.

- isaac_ros_common's README now links this fork's clone, image and Mac
  setup ([isaac_ros_common #8](https://github.com/Thornbots/isaac_ros_common/pull/8)).
  Standalone MCB flashing points at this repo's GitHub CI ELF artifacts and
  the current build path instead of GitLab
  ([MCBV3 #95](https://github.com/Thornbots/MCBV3/pull/95)).

- Construct localization backends and their lifecycle managers in one process
  to avoid startup service-response discovery races, and remove the drift suite's
  automatic robot restart. Startup errors identify the missing TF link.
  The sim clock bridge now uses UDP-only DDS so a stale shared-memory reader
  port cannot block global time publication; a focused clock-delivery test
  checks fresh contexts and the transport invariant.
  At the T30 revision, two final full drift confirmations passed 9/9 each
  without startup retries or relaxed limits; large simulator yaw excursions
  also reproduced. These results predate the field/map and parked-localization
  fixes below and do not validate the final release candidate.
  Portable CI dependency pins now follow the integrated current UART contract. See
  [localization #9](https://github.com/Thornbots/sentry_localization/pull/9),
  [sim #26](https://github.com/Thornbots/sim/pull/26) and
  [T30 validation](docs/investigations/t30-localization-startup-2026-10-16.md).

- Add opt-in tracker innovation diagnostics and estimation-bench radius/prior
  controls. G.1 trials expose regressions in the full matrix, so tracker tuning,
  validity and estimation limits stay unchanged; defaults are numerically
  identical to before. See
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
  At the linked investigation revision, three Mac hosted repeats cleared
  every spinning cell, with pooled hits of 97.1% versus the then-nightly
  baseline's 17.3%; parked, drive, match and moving reached 85.5%, 93.5%,
  54.5% and 79.6%. Failed baseline accuracy checks remained diagnostic
  observations; clock-invalid attempts were excluded.
  Nonspinning prediction retains panel lead and hysteresis. Board lockstep learns one 5 ms batch ahead while retaining wall
  deadlines and timeout rejection. Renode installation now avoids the
  temporary-directory cleanup prefix that deleted writable fixtures. Firmware
  sleeps between SysTick interrupts during the three-second power-on guard;
  three complete Mac board boots take 102–116 wall seconds under the unchanged
  600-second startup limit. Three native-accepted Renode board repeats in that
  investigation improved drive hits from 30.5% to 85.1% and match from 23.7% to 54.1%, with zero
  lockstep timeouts in the selected runs. These are historical simulation
  measurements, not physical-board or final-release acceptance. See the
  [spinning and board investigation](sim/docs/aim-accuracy-2026-10-12.md#spinning-correction-and-board-comparison).

- Calibrate the hosted direct-sensor aim fixture's 8 ms gyro age and model
  projectile speed at 24 m/s, matching the firmware solver; add inherited
  muzzle motion and pose-latency controls. The 8 ms delay is fixture-specific;
  board execution uses its full IMU filter. Firmware yaw prediction now uses
  geared torque and configured friction, control integration uses the actual
  1 ms interval. That experiment introduced a zero-wheel-velocity parked
  hold and a 3 cm displacement limit, with estimated passive rolling
  resistance in sim. The later drivetrain reversion above removed the
  automatic hold: the default stop cuts wheel current; centred manual drive
  still holds zero wheel velocity. Three hosted pre-track-I repeats measured
  maximum chassis displacement of 19.2, 28.9 and 22.4 mm versus the 132.0 mm coasting observation. These
  scores are not controlled comparisons with the new board auto-drive route.
  Native failures remain failures, not accepted accuracy results; moving-shot
  accuracy remains an acceptance gate. See the [dated accuracy investigation](sim/docs/aim-accuracy-2026-10-12.md).

- Sim pose diagnostics distinguish local EKF field-alignment error from
  globally corrected localization error, retain capture-time TF exceptions,
  and retry delayed pose telemetry for up to one simulated second. The
  [follow-up investigation](sim/docs/aim-followup-2026-10-12.md) checks TF
  composition, startup gaps, nightly localization behavior and combat
  repeatability. `mcb_parked` first used a 0.10 m displacement bound; the
  accuracy experiment tightened it to 0.03 m and added powered velocity
  holding, which the later drivetrain reversion above removed. Those earlier
  measurements are not acceptance evidence for the current stop behavior.
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
  stop and checks CAN output as well as issued requests. The Renode board parked
  cell passed at that revision; physical-robot validation and repeatability
  remain open. See
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

- At the T32/T33 revision, all three hosted-firmware match stages were
  checked: parked moving cells failed, while drive/match passed diagnostic
  completion with zero native hits. Later aim and board-stage work above
  superseded these results; retain the historical
  [per-cell/segment results and native checker verdicts](sim/docs/match-check-2026-10-11.md).

- Sim runs one native MCB control tick per gz physics step, supplies DJI motor
  feedback and applies motor outputs as forces instead of gz setpoint
  controllers. The UART bridge waits for the PTY. This completed track I's
  motor path at that revision; the later Renode board and firmware auto-drive
  work above completed those simulation paths. See
  [sim #14](https://github.com/Thornbots/sim/pull/14),
  [MCBV3 #88](https://github.com/Thornbots/MCBV3/pull/88),
  [bridge #7](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/7) and the
  [motor validation](sim/docs/mcb-motor-plant-2026-10-11.md). Drive/match diagnostics
  passed at that revision; parked hit-path repeatability remained unresolved.

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
  JAZZY_FLASH no longer check out every
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
  still need the user. A delegation brief naming other user-approved actions
  counts as that approval ([runs](AGENTS.md#containers-and-runs)).
- Sim temporary-world cleanup tolerates repeated shutdown events, and the native
  log checker rejects launch exceptions. Fresh hosted MCB builds, UART traffic
  and live gimbal aiming were verified on x86_64. See
  [sim #10](https://github.com/Thornbots/sim/pull/10) and the
  [verification and shutdown findings](sim/docs/mcb-hosted-check-2026-10-11.md).

- `.claude/settings.local.json` is no longer tracked and is now gitignored; it
  held one maintainer's personal permissions and paths. Pulling this removes
  the tracked copy, so keep a backup first if you edited it locally.

### Fixed

- Firmware: setting the first UI container no longer dereferences a null
  container; sentry now schedules its draw command at startup like hero and
  infantry ([MCBV3 3a98bf0](https://github.com/Thornbots/MCBV3/commit/3a98bf0)).
- Firmware: Ctrl+Shift+B builds and flashes from the MCBV3 VS Code dev
  container. It now matches CI's toolchain, adds openocd and pipenv, sees the
  host's USB probe, runs as the host user and defaults the robot to SENTRY.
  Inside this workspace pick "MCBV3 (Isaac ROS workspace)" so commits are
  signed and run the policy hooks. Untested against a board: no flash yet.
  [MCBV3 #112](https://github.com/Thornbots/MCBV3/pull/112)

- Sim and robot description use the team's 2026-10-26 low-resolution CAD
  (from sim #48 / thornbots_pkg #30), with `camera` on its RGB FOV apex and
  the firmware barrel offset at its 1.9 mm bore. `sim`'s `simplify_urdf`
  generator, config and vendored decimator are removed; edit `urdf/sentry_v2`
  directly. The CAD map-slice height (sentry_localization #20) is pinned too.
  [sim #53](https://github.com/Thornbots/sim/pull/53),
  [thornbots_pkg #36](https://github.com/Thornbots/thornbots_pkg/pull/36),
  [MCBV3 #110](https://github.com/Thornbots/MCBV3/pull/110),
  [sentry_localization #20](https://github.com/Thornbots/sentry_localization/pull/20).

- The `camera` frame is now the D435's RGB lens, 32.5 mm to the camera's left
  of the CAD cover centre, in both URDFs. Detections are deprojected from
  that lens, so real-robot aim points had landed 32.5 mm right of the panel;
  the sim hid it because its detector shared the frame. Real robot: aim
  shifts 32.5 mm left at any range.
  [thornbots_pkg #36](https://github.com/Thornbots/thornbots_pkg/pull/36),
  [sim #53](https://github.com/Thornbots/sim/pull/53).

- The sentry's shot speed is 22 m/s everywhere: the MCB's pitch solve (was
  24), Jetson `v_muzzle` (was 25) and the robot service's `launch.env`
  `EXIT_VELOCITY=22.0`, plus sim ballistics and the aiming bench. Real robot:
  pitch rises slightly for the slower shot.
  [startup #14](https://github.com/Thornbots/isaac-ros-startup/pull/14),
  [MCBV3 #110](https://github.com/Thornbots/MCBV3/pull/110),
  [thornbots_pkg #36](https://github.com/Thornbots/thornbots_pkg/pull/36),
  [sim #53](https://github.com/Thornbots/sim/pull/53).

- Sentry firing uses the 20 ms indexer request-to-exit timed on the robot
  (was the sim's 94 ms): the MCB subtracts 20 ms and Jetson never sends a
  fire delay under 25 ms (`min_fire_delay_s`). The MCB now holds a pending
  shot instead of letting the next non-fire frame cancel it, and the sim
  indexer exits balls 20 ms into a feed. Hosted parked sim: hits 368/411 ->
  403/421. Real robot: verify shot timing and that no shots drop.
  [MCBV3 #110](https://github.com/Thornbots/MCBV3/pull/110),
  [thornbots_pkg #36](https://github.com/Thornbots/thornbots_pkg/pull/36),
  [bridge #27](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/27),
  [sim #53](https://github.com/Thornbots/sim/pull/53).

- Sentry auto-aim now turns the barrel's line through the CV aim point: the
  firmware adds the barrel's 12.8 mm left-of-yaw-axis offset (sentry_v2 CAD)
  to its yaw solve. In the hosted-MCB parked stage this cut the leftward hit
  bias from 19 to 8.5 mm; shots still land about 15 mm low and 8 mm left from
  gimbal settling error, which stays with the hardware-tuned gains for
  real-robot testing. Sim `shots.jsonl` now records each shot's position on
  its panel. Changes real-robot aim by about 0.6 deg at 1.2 m; verify on the
  robot. [MCBV3 #110](https://github.com/Thornbots/MCBV3/pull/110),
  [sim #53](https://github.com/Thornbots/sim/pull/53).

- Portable package CI now builds against the current nightly dependency
  workspace, restoring matching target-message and localization launch
  interfaces. Keep immutable dependency pins separate from reusable tooling
  pins; [CI policy](docs/CI.md) describes when to refresh them
  ([thornbots_pkg #34](https://github.com/Thornbots/thornbots_pkg/pull/34),
  [sentry_localization #25](https://github.com/Thornbots/sentry_localization/pull/25),
  [sim #52](https://github.com/Thornbots/sim/pull/52),
  [rf2o #20](https://github.com/Thornbots/rf2o_laser_odometry/pull/20),
  [serial bridge #25](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/25),
  [ROI rectifier #10](https://github.com/Thornbots/Realsense_ROI_Depth_Rectifier/pull/10),
  [sllidar #11](https://github.com/Thornbots/sllidar_ros2/pull/11)).

- Sentry firmware now reports POSE `odom_status` 2 before the first successful
  Pico I2C read or when its age reaches 500 ms; healthy reads report 0. The
  threshold accommodates the measured 260 ms Pico cadence without changing
  odometry values ([MCBV3 #105](https://github.com/Thornbots/MCBV3/pull/105),
  [bridge #24](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/24)).

- Sim's CV bench armor validation now checks ground clearance and the 400 mm
  maximum lower-edge height instead of an unsupported 60 mm minimum; rule
  citations link to the verified workspace comparison
  ([sim #51](https://github.com/Thornbots/sim/pull/51)).

- Launch stopping now lists and signals only verified container-owned ROS
  launch/run trees, including when the container shares the host PID namespace.
  PID 1, host processes and non-ROS roots are refused; the force bypass is gone.
  Stop matching trees directly with `kill_launch.sh --match <literal-substring>`
  ([isaac_ros_common #17](https://github.com/Thornbots/isaac_ros_common/pull/17)).

- rf2o no longer carries a permanent offset when the robot moves before its
  first scan, or when rf2o restarts while moving. It used to latch the first
  `/odom` pose and initialize from a later scan; it now seeds at that scan's
  own odometry stamp, waits in a bounded queue for scan-time TF and odom, and
  caps that wait at 1 s so a stalled `/odom` or joint stream degrades rather
  than stopping rf2o. Failed matches without wheel fallback retain the coherent
  scan/pose/head reference so recovery preserves the full displacement.
  Startup topic aliases and remaps use resolved subscription names.
  In sim, moving 1.5 m before the first scan left 1.0 m on
  the old pin and 0.004-0.010 m now. This affects the normal rf2o/EKF launch;
  the competition `localize` default (raw wheel odometry) does not use rf2o.
  [rf2o_laser_odometry #16](https://github.com/Thornbots/rf2o_laser_odometry/pull/16).

- rf2o's `reference_scans` is available but off by default; this workspace
  keeps sentry_localization at `nightly` without enabling it. When explicitly
  enabled, it matches parked scans against earlier scans from the same head
  angle once `/odom` has held still for 2 s; wheel motion returns it to
  consecutive-scan matching. Earlier sim runs with references enabled reduced
  `mcb_parked` p95 from up to 0.090 m to about 0.01 m and tracked a 4 cm shove
  with the wheels held still (`parked_push`). These results do not describe
  the default configuration and remain unverified on hardware.
  The combined matcher retains scan-time startup and transactional failure
  recovery, caps its reference bank, and grades speed independently of anchor
  age. `/scan_odom` twist reports robot-frame vx/vy from consecutive accepted
  poses, with no robot consumer. See the
  [investigation](docs/investigations/t39-parked-drift-2026-10-25.md),
  [rf2o_laser_odometry #17](https://github.com/Thornbots/rf2o_laser_odometry/pull/17),
  [sim #43](https://github.com/Thornbots/sim/pull/43).

- SLAM and AMCL no longer treat head motion as robot motion. Both cached the
  head-mounted lidar's mount from the first scan; slam_toolbox now tracks the
  `lidar` frame (`slam.yaml`, also the default robot launch) and AMCL refreshes
  the mount position each scan. In sim, a flat head-sweep SLAM circuit went
  from 0.735 m to 0.012 m p95 error, and a head-sweeping AMCL drive from
  0.205 m to 0.10 m max. Start new mapping sessions; old serialized graphs used
  the `root` base. See the
  [investigation](docs/investigations/fieldmap-divergence-2026-10-22.md) and
  [sentry_localization #16](https://github.com/Thornbots/sentry_localization/pull/16).

- E2E referee parameter requests have a two-second response deadline and
  bounded retries of the current desired state, so a lost bring-up response
  no longer permanently blocks a later `drive=simple` update. Sim fixture
  only; see [sim #39](https://github.com/Thornbots/sim/pull/39) and
  [workspace #85](https://github.com/Thornbots/thornbots_workspace/pull/85).

- A new sim stack replaces a stale MCB PTY link pointing to its own reused
  `/dev/pts` number after an interrupted teardown. Links to other live PTYs
  remain protected, preventing one failed teardown from aborting subsequent
  E2E stages. Sim fixture only; see
  [sim #40](https://github.com/Thornbots/sim/pull/40) and
  [workspace #87](https://github.com/Thornbots/thornbots_workspace/pull/87).

- Fix the head-TF timing and rf2o head-motion handling that caused 0.1-0.4 m
  parked-localization errors during simulated target-acquisition slews. The
  shared robot path receives the same fixes; hardware validation is pending.
  The head TF now publishes at the 90 Hz POSE rate, not the 20 Hz
  `robot_state_publisher` default
  ([thornbots_pkg #23](https://github.com/Thornbots/thornbots_pkg/pull/23)).
  rf2o seeds and dead-reckons through the head's swing between scans, and
  skips scans whose head TF is more than 50 ms stale
  ([rf2o #14](https://github.com/Thornbots/rf2o_laser_odometry/pull/14),
  [sentry_localization #15](https://github.com/Thornbots/sentry_localization/pull/15)).
  `mcb_parked` now fails any cell whose map localization has p95 above 0.15 m,
  max above 0.20 m or under 95% stamped coverage
  ([sim #41](https://github.com/Thornbots/sim/pull/41)). Slow scan-odometry
  drift while parked is still uncorrected below AMCL's update thresholds
  (0.1 m translation or 0.05 rad odometry rotation); see the
  [rf2o notes](sentry_localization/README.md#configrf2oyaml) and
  [robot validation T39](docs/ROBOT_TESTS.md#parked-localization). The merged-package
  tree passed three hosted parked runs (12/12 cells each) and 560 colcon
  tests; earlier fix validation also passed AMCL `drift_correction`. See
  [workspace #88](https://github.com/Thornbots/thornbots_workspace/pull/88)
  for revisions and measurements.

- The sentry's rough auto-drive route keeps the spinning chassis clear of the
  wall end beside its start. The wall leg moves from 2.236 m to 2.5 m to the
  side. Only the two wall-leg waypoints use a 0.2 m arrival tolerance; all
  other waypoints retain 0.5 m, preventing corner cutting near the wall without
  tightening other routes. The old route could strike the wall end and wedge
  until the 15 s stuck timer. Not yet driven on the real field. See
  [MCBV3 #101](https://github.com/Thornbots/MCBV3/pull/101).

- The UART bridge drops CV decisions aged 200 ms or more, invalid/future
  stamps and frames behind a busy TX queue at the final nonblocking write
  boundary. Fresh aim/fire payloads and ROS/simulation decision stamps stay
  intact. See [bridge #19](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/19)
  and the [freshness contract](ros2_dji_serial_bridge/UART_PROTOCOL.md#jetson--mcb-freshness).
  The real-bridge PTY fixtures stamp each newly created decision to follow this
  contract ([sim #38](https://github.com/Thornbots/sim/pull/38)).

- Nightly results require a zero runner exit and the complete valid stage
  report, so interrupted runs cannot pass after setup alone. Failure-driven
  SKIPs remain visible; malformed, duplicate or impossible records fail.
  See [nightly tests](docs/CI.md#nightly-tests).

- Automatic agent-container cleanup now removes only resources labelled for
  the creating invocation, including partial startup; duplicate task refusal
  preserves the existing container and volumes. Interruptible command waits
  let signal cleanup run while the helper is active and preserve piped input.
  Existing volumes are not
  silently reused. See [isaac_ros_common #15](https://github.com/Thornbots/isaac_ros_common/pull/15).

- RF2O skips scans whose range count or angular geometry differs from its
  initialized grid, with a throttled warning, instead of reading past the
  scan. Regression tests cover shorter/longer scans, angle changes and
  recovery. See [rf2o_laser_odometry #10](https://github.com/Thornbots/rf2o_laser_odometry/pull/10).

- The sentry hardware launch enables lidar angle compensation, so RF2O and
  slam_toolbox receive a fixed angular grid (720 bins on the measured A2M8)
  rather than a varying beam count. Stationary drift after this change still
  needs a robot run. See [thornbots_pkg #18](https://github.com/Thornbots/thornbots_pkg/pull/18).

### Real-robot impact and validation limits

- Deploy matching firmware and ROS packages together: this batch separates
  raw aiming odometry from navigation corrections, changes hit-turn/reporting
  behavior, and rejects stale CV decisions at UART transmission. Head-TF/rf2o
  fixes and lidar angle compensation also affect robot localization. The
  default drivetrain stop cuts wheel current; centred manual drive holds
  zero wheel velocity.
- No physical-robot validation has been performed for this batch. Historical
  hosted/Renode results above and package test runs do not establish final
  release, camera/GPU, physical drivetrain, firing or combat acceptance. Final
  candidate CI/image checks remain release checks; see [CI limits](docs/CI.md#validation-boundaries).
- Slow parked scan-odometry drift remains open under
  [robot validation T39](docs/ROBOT_TESTS.md#parked-localization). The sim parked gate
  requires p95 ≤ 0.15 m, max ≤ 0.20 m and at least 95% stamped coverage;
  passing it does not establish long-duration stationary accuracy on hardware.

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
  `detector_standin` feeding gz truth instead of YOLO. The former non-MCB stage is gone;
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
- Results and revisions: [nightly validation, 2026-10-06](https://github.com/Thornbots/thornbots_workspace/blob/6bd0692ddd6f553a156eab624f7c85975c501136/docs/testing/nightly-2026-10-06.md),
  the 2026-10-08 sim sweep in
  [workspace e0f2425](https://github.com/Thornbots/thornbots_workspace/commit/e0f2425) (open problems in
  [ROADMAP issues](docs/ROADMAP.md#issues-found)), and firmware validation at
  [MCBV3 a2ea519](https://github.com/Thornbots/MCBV3/commit/a2ea519).
