# Changelog

Changes integrated on `nightly` and awaiting promotion to `main`. Add entries
under Unreleased as changes land; move them into a dated release section when
promoting the workspace to main. Describe user-visible behavior and real-robot
impact, and link the corresponding package changes.

## Unreleased

- Add opt-in strict simulator lockstep startup: it holds to the first positive
  scheduled deadline, stops on missing acknowledgments, and adds an epoch-zero
  readiness barrier with a bounded startup timeout and missing-topic
  diagnostics. The detector acknowledges epoch-zero initialization and consumed
  truth at scheduled capture stamps, rounded up to the next 1 ms physics step
  ([sim #73](https://github.com/Thornbots/sim/pull/73)). Scored T17 acceptance
  and downstream deterministic consumption gates remain open.

- Add an opt-in paused-world spawn readiness gate to the simulator
  `opponent_driver`: it publishes epoch-zero `~/ready` only after a single
  correctly posed opponent is confirmed at sim time zero, and exits on
  collision, wrong pose, nonzero epoch or timeout
  ([sim #73](https://github.com/Thornbots/sim/pull/73)). It does not establish a
  scored T17 run.

- Add opt-in paused epoch-zero initialization for the aim publisher's timers,
  with a latched readiness acknowledgment
  ([thornbots_pkg #59](https://github.com/Thornbots/thornbots_pkg/pull/59)), and
  a UART clock bootstrap where the bridge reports actual clock receipt and the
  simulator waits for it and detector readiness before plugin readiness
  ([bridge #37](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/37),
  [sim #73](https://github.com/Thornbots/sim/pull/73)). The opt-in parked E2E
  diagnostic uses both, plus paused robot/opponent scene verification and MCB
  bootstrap before lockstep release. Scored acceptance and downstream
  first-data gates remain open.

- Add an opt-in sim-time UART relay fixture with a shared bridge baud for T17;
  Jetson input observed during a firmware cycle is deferred to the next cycle.
  The bridge provides opt-in verified capture stamps and publication
  acknowledgments ([bridge #37](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/37));
  an experimental simulator metadata and acknowledgment path is under
  validation ([hosted diagnostic](sim/docs/uart-coordination-2026-11-03.md)).
  Scored integration and match repeatability remain open.

- Firmware developers can send opaque 0-128 byte debug blobs with a nonblocking
  MCB API; the bridge stamps them at estimated UART send start and publishes
  `/dji_serial_bridge/debug`, recorded in normal and match per-run bags. Debug
  uses spare UART budget and may delay one telemetry frame by up to 10 ms
  while keeping all 90 Hz POSE / 10 Hz REF_SYS slots; scheduler gaps over
  100 ms restart a fresh cycle. No production values or sender are enabled.
  The bridge also adds T20 throttled logs and `Serial link` diagnostics with a
  `debug_msgs_pub` counter, and portable ROS CI pins use the merged T25
  workspace revision. Deploy matching firmware and bridge revisions together
  ([wire contract](ros2_dji_serial_bridge/UART_PROTOCOL.md#debug-id6--opaque-firmware-debug),
  [bridge #34](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/34),
  [bridge #35](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/35),
  [startup #23](https://github.com/Thornbots/isaac-ros-startup/pull/23),
  [MCBV3 #130](https://github.com/Thornbots/MCBV3/pull/130),
  [sim #62](https://github.com/Thornbots/sim/pull/62),
  [hosted verification](sim/docs/mcb-debug-bag-2026-11-01.md)).

- [Season 2 rule figures and power audit](docs/rules/season2-geometry.md)
  separate printed dimensions, derived placements and implementation
  estimates; side-wall face placement is corrected, the central-road 15 mm
  printed-chain conflict is preserved, and pole-height and building-spec page
  authority are clarified. Unpublished-source and package acceptance stay under
  DOC14g/RULES-S2.

- Separate sim README experiment narratives into [dated history](sim/docs/simulation-history-2026-11-02.md), retaining current instructions and compatibility headings ([sim #71](https://github.com/Thornbots/sim/pull/71), DOC14f; independently reviewed and completed).

- Estimation harness reset acknowledgement ordering and scorer pacing handoffs
  are corrected without changing scored watchdogs or numeric limits
  ([sim #68](https://github.com/Thornbots/sim/pull/68),
  [validation status](sim/docs/de-harness-2026-11-02.md)).

- The sim suite wrapper and T3 shortcuts use `localization_drift`, `ekf`, `aim` and `tracking`; `mcb_*` stage names are unchanged ([sim #65](https://github.com/Thornbots/sim/pull/65), [sim tests](sim/README.md#run-the-tests)).

- Open work now routes to two canonical homes: unfinished Mini/software/sim
  tasks in [ROADMAP](docs/ROADMAP.md) and physical validation in
  [ROBOT_TESTS](docs/ROBOT_TESTS.md). Completed items are removed after
  integration; final completion also requires a separate full automated-suite
  pass on integrated nightly. [Consolidation coverage](docs/audits/open-work-consolidation-2026-11-02.md)
  records sources and dependencies, including the open T23, T17 and mapping
  duplicate-graph/save-freshness items.

- Document [rf2o fork usage](rf2o_laser_odometry/README.md#thornbots-fork-and-usage), move [October 3 parked results](sim/docs/mcb-parked-results-2026-10-03.md) into a dated report, and narrow the [remaining documentation audit](docs/ROADMAP.md#issues-found) with sourced Season 2 match timing ([rf2o #23](https://github.com/Thornbots/rf2o_laser_odometry/pull/23), [sim #64](https://github.com/Thornbots/sim/pull/64)).

- Adding a package submodule no longer needs a `reviewed_history` line; the policy hook and CI trust the imported history and check later bumps ([policy](docs/CI.md#repository-policy)).

- New [`nav_pkg`](https://github.com/Thornbots/nav_pkg) package submodule (tracks `nightly`) for navigation work; it contains only a README so far and changes no robot behavior.

- Low-space startup pruning explicitly protects the active run even with zero retained runs ([startup #22](https://github.com/Thornbots/isaac-ros-startup/pull/22), [pruning](isaac-ros-startup/README.md#design-notes)).

- Repeated rf2o warnings now show the first event and sample repeats every five seconds, retaining totals in log samples and publishing counters under stable event IDs in match-quality diagnostics ([rf2o #21](https://github.com/Thornbots/rf2o_laser_odometry/pull/21), [warning logs](rf2o_laser_odometry/README.md#warning-logs)).

- Bridge referee and CRC logs now sample repeats every five seconds while retaining lifetime counters; rare RELOCALIZE corrections and operator PING checks log every event. Standard ROS `/diagnostics` reports interval-based serial health and every DIAG counter, including recovery and stalled links ([bridge #34](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/34), [levels](ros2_dji_serial_bridge/README.md#diagnostics)).

- The [Sentry rules context](docs/ARCC_2026_SENTRY_CONTEXT.md) now follows the ARCC Season 2 (2027) manuals V1.0 of 2026-11-01 instead of ARCC 2026. Changes that matter to the robot: the 3v3 Sentry chassis limit drops to 80 W, there is a new Sentry Tournament (5×5 m, 120 W, 250 rounds, 2 minutes, no respawn, healing from damage dealt), armor hit faces are dot-matrix screens (style not yet published), the 3v3 field has Limbo Bars (420/300 mm) and object-scoring with Scoring-Area Penalty Zones instead of a Capture Point, and the Sentry weight limit is 28 kg including the referee system. Firmware, sim and nav defaults have not been changed yet.

- Robots now use an explicitly pulled registry image as their dependency base and build current source as an offline overlay. Startup pins the prepared image and rejects missing or shadowed overlay packages; image publication also checks the offline build. Ordinary source changes no longer require image builds or pulls. Local image building/shipping is an emergency fallback; equipped-robot startup acceptance remains open ([common #21](https://github.com/Thornbots/isaac_ros_common/pull/21), [startup #24](https://github.com/Thornbots/isaac-ros-startup/pull/24), [workflow](isaac_ros_common/docker/README.md#building-the-robots-image), [Orin measurements](docs/investigations/robot-overlay-2026-11-01.md)).

- The sentry and infantry MCB pitch solver (same gimbal) no longer shoots high close and low far: it uses the CAD pivot height and bore length (0.4035 m, 0.173 m) instead of the 0.28 m height retune, adds horizontal drag, and corrects a 0.042 rad shot launch bias fit to robot misses at 1 m and 3 m; confirmed on the sentry. Refit the bias, not the pivot height, if a range-dependent miss remains ([MCBV3 #127](https://github.com/Thornbots/MCBV3/pull/127), [aiming](firmware/MCBV3/README.md#aim-and-navigation-odometry)).

- The Jetson owns independent `red_start_x/y` and `blue_start_x/y` launch configuration, overridable per robot through `/etc/thornbots/launch.env`. Navigation, EKF/AMCL/saved-map SLAM priors, idle enemy-zone looks and operator registration use the same values. Defaults remain the unmeasured scrim starts ([ROADMAP T40](docs/ROADMAP.md#short-todos)). Firmware routes use field-centred coordinates and return to the boot point the Jetson's RELOCALIZE places, even after a mid-match reschedule; PURDUE2V2 is removed. Hosted firmware no longer sends a start in its simulator handshake; sim keeps its ARCC spawn and passes matching launch arguments to bringup ([MCBV3 #128](https://github.com/Thornbots/MCBV3/pull/128), [#129](https://github.com/Thornbots/MCBV3/pull/129), [localization #33](https://github.com/Thornbots/sentry_localization/pull/33), [bringup #50](https://github.com/Thornbots/thornbots_pkg/pull/50), [sim #61](https://github.com/Thornbots/sim/pull/61), [UART docs #33](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/33), [startup #21](https://github.com/Thornbots/isaac-ros-startup/pull/21)).

- Firmware tuning from the robots: every robot's flywheel PID returns to the earlier `{30, 0.1}`; hero flywheel max 4600 RPM (about 11.5 m/s); hero and standard drive without spin-follow and with a zero yaw offset (no yaw encoder; only the sentry reads one); sentry and standard pitch-down limit 5° (was 21°), sentry pitch offset 0.18 (was 0.52); hero bottom indexer on motor 7; sentry and standard aim projection offsets adjusted (sentry still aims high up close and low far away). Not covered by tests ([MCBV3 nightly](https://github.com/Thornbots/MCBV3/compare/e708e50...533642d)).

- MCBV3 dev container: one config that mounts the whole workspace, so git and the policy hooks work from `firmware/MCBV3` (standalone clones are no longer supported); CMSIS-DAP hardware debugging targets the STM32F407IG and the selected robot; `.vscode` drops stale Windows-only settings ([MCBV3 #121](https://github.com/Thornbots/MCBV3/pull/121), [#122](https://github.com/Thornbots/MCBV3/pull/122), [#123](https://github.com/Thornbots/MCBV3/pull/123), [README](firmware/MCBV3/README.md)).

- Sentry's lidar is now mounted upside down. A new `lidar_inverted` launch arg (default `true`) sets the driver's `inverted` flag, and the defaults move to the Oct 31 CAD mount: yaw 2.579 rad, self-filter -1.927..-0.171 rad. The robot needs this to localize and map again. Nose-up/down sectors and a head-turn fit still need measuring ([thornbots_pkg #47](https://github.com/Thornbots/thornbots_pkg/pull/47), [sim #59](https://github.com/Thornbots/sim/pull/59), [measurement](docs/investigations/lidar-flip-2026-10-31.md)).

- Commit signing is no longer required: the policy hooks and CI `policy` job drop the signature and `commit.gpgsign` checks, so unsigned commits push and pass. Gitlink fast-forward, reviewed-history and `.msg` stamp checks are unchanged ([repository policy](docs/CI.md#repository-policy)).

- The sentry MCB's raw odometry and aim boot at `(0, 0)` for either team, both facing the field's +y (`pi/2`), and the Jetson relocalizes navigation from the referee team's start. EKF seeding, passthrough navigation and AMCL wait for a valid REF_SYS team, then start at red `(-4.625, 0)` or blue `(4.625, 0)`; `mcb_relay` sends each confident absolute fix four times at least 0.3 s apart. Firmware routes, position commands and NAV_GOAL driving stay off until the first RELOCALIZE. On the robot, navigation does not start without referee team data; the `initial_x/y` and `amcl_initial_*` launch arguments are deprecated and ignored. MMM parking checks measure from that raw zero. Sim fixtures model the zero raw boot, and the drift and parked E2E suites drive from the team start to center before scoring ([MCBV3 #119](https://github.com/Thornbots/MCBV3/pull/119), [thornbots_pkg #42](https://github.com/Thornbots/thornbots_pkg/pull/42), [sentry_localization #30](https://github.com/Thornbots/sentry_localization/pull/30), [ros2_dji_serial_bridge #30](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/30), [sim #58](https://github.com/Thornbots/sim/pull/58), [startup relocalization](ros2_dji_serial_bridge/UART_PROTOCOL.md#message-types)).

- The robot service's Foxglove bridge takes a `FOXGLOVE_ADDRESS` listen IP (default `0.0.0.0`, unchanged); `192.168.55.1` exposes it only on the USB tether ([isaac-ros-startup #20](https://github.com/Thornbots/isaac-ros-startup/pull/20), [watch live](isaac-ros-startup/README.md#use)).

- Field mapping now follows MMM: the root README "Map a new field" procedure is removed, the [Notion mapping doc](https://app.notion.com/p/fff357611caa4131b216742bb7c6e048) covers the MMM operator steps with a [state diagram](docs/images/mmm-states.png), MMM drivers need no speed rule because the MCB caps drive speed, and the manual workflow allows 0.4 m/s instead of 0.2 m/s ([thornbots_pkg #44](https://github.com/Thornbots/thornbots_pkg/pull/44)).

- MMM validated saves now allow re-parking within 0.50 m and 15° of the
  SLAM boot pose, with 0.60 m/18° exit hysteresis and a 0.50 m raw-odometry
  spawn guard. Boot capture still requires raw odometry within 0.30 m of the
  team start; parked stability and chassis-yaw checks are unchanged
  ([thornbots_pkg #45](https://github.com/Thornbots/thornbots_pkg/pull/45),
  [MMM](thornbots_pkg/README.md#mcb-mapping-machine)).

- Agents run tests, sim integration tests, sim benches and reruns, and start
  laptop containers, VMs and stacks, without asking, and may restart a robot's
  `thornbots` stack. Other physical-robot runs and restarting or stopping what
  an agent did not start still need the user; a delegation brief naming
  user-approved actions counts as that approval
  ([AGENTS](AGENTS.md#containers-and-runs)).

- CV firing waits for one second of confident tracking of the same robot
  (`fire_lock_s`, now an `auto.launch.py` argument so a robot can set it in
  `launch.env`'s `AUTO_LAUNCH_ARGS`), with an immediate bypass for nonspinning
  targets below `fire_stationary_speed_mps` (0.1 m/s). Brief stale, unconverged
  or low-confidence gaps on the same track preserve the timer for
  `fire_lock_grace_s` (0.3 s); gap time counts, but firing remains blocked.
  Longer gaps, target timeout or switched tracks restart the wait. The minimum
  fire exit delay increases from 25 to 40 ms to give the gimbal time to acquire
  each aim ([thornbots_pkg #43](https://github.com/Thornbots/thornbots_pkg/pull/43),
  [thornbots_pkg #48](https://github.com/Thornbots/thornbots_pkg/pull/48)).

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

- Mapping save-now finishes staging cleanup before reporting completion,
  including collision and backend failures. Timeout failures still respond
  promptly and keep the saver busy until the backend replies and the abandoned
  staging directory is removed ([sentry_localization #27](https://github.com/Thornbots/sentry_localization/pull/27)).

- CV targeting requests fire on every eligible 40 Hz publish tick instead of
  throttling requests to 2 Hz; the MCB filters pending requests. Confidence,
  detection freshness, planner shot windows and the minimum fire delay remain
  in force ([thornbots_pkg #37](https://github.com/Thornbots/thornbots_pkg/pull/37)).
  The sim aiming bench uses the same policy without a fire-rate override
  ([sim #55](https://github.com/Thornbots/sim/pull/55)).

- The workspace [AGENTS](AGENTS.md) no longer sets delegation rules; agents follow their own harness and user defaults.
- Sentry MMM now owns indicators and restrictions in its command, keeps odometry pods pointing in every mapping state while the remote is connected, and services pings through Jetson UART refresh ([MCBV3 #111](https://github.com/Thornbots/MCBV3/pull/111)). Turning the remote off now stops every motor, gimbal and pods included, without leaving the mapping state ([MCBV3 #114](https://github.com/Thornbots/MCBV3/pull/114)).
- Sentry MMM starts from the controller: left switch down and the right stick held up for 5 s. Inside MMM, each later 5 s hold (after a release) tries to save; no input leaves MMM ([MCBV3 #113](https://github.com/Thornbots/MCBV3/pull/113), [firmware README](firmware/MCBV3/README.md#mcb-mapping-machine-sentry)).

### Added

- The Mac mini's [nightly run](docs/CI.md#nightly-tests) now builds and tests
  the robots' JetPack image on the registry's shared base layers after a local
  PASS, publishing immutable workspace SHA and nightly tags with bounded local
  cache and old registry-tag cleanup.

- A [hosted MMM end-to-end suite](sim/README.md#run-the-tests) connects the
  compiled sentry firmware to the real bridge and in-stack mapping node, covering
  telemetry load, UART faults/backpressure, restarts, restrictions and validated
  saving. Start/save inputs are private to the hosted fixture; the hardware
  target excludes the hook. [Mini validation](docs/investigations/mmm-firmware-e2e-2026-10-29.md).

- The C++ [`mmm` node](thornbots_pkg/README.md#mcb-mapping-machine) starts
  inside `auto.launch.py` with the normal stack. It resets the live mapping
  graph, captures stationary boot evidence, sends setup-failure PING 6, and
  delegates asynchronous map writing to localization's save-now service. Ready
  saves stay guarded until durable completion; failed saves return the MCB
  through 4 then 2. Transient bad lidar scans restart fresh evidence instead of
  permanently blocking saves; fresh start requests create another session, and
  starts during a save send setup failure without interrupting it. The manual
  Python workflow is restored without MMM/snapshot commands. Host shutdown is
  opt-in through startup's fixed request-file watcher and never requested by
  an incomplete save. The
  [PING contract](ros2_dji_serial_bridge/UART_PROTOCOL.md#ping-id5--mcb-mapping-machine-and-link-check)
  specifies ACKs and retry rules; sentry firmware retries unacknowledged 1/3
  every 500 ms, PING 4 returns Done to Mapping after a failed final save
  (restricted manual drive, pending save work cancelled), and PING 6 moves
  Setup to Done and stops start retries. The UART payload is unchanged; a save
  ACK permits MCB-side power-off before storage completes, so data loss remains
  possible. See the [validation record](docs/investigations/mmm-node-validation-2026-10-29.md);
  [thornbots_pkg #35](https://github.com/Thornbots/thornbots_pkg/pull/35),
  [bridge #26](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/26),
  [localization #26](https://github.com/Thornbots/sentry_localization/pull/26),
  [startup #15](https://github.com/Thornbots/isaac-ros-startup/pull/15),
  [MCBV3 #111](https://github.com/Thornbots/MCBV3/pull/111),
  [sim #54](https://github.com/Thornbots/sim/pull/54).

- Operator workflow now lives in `thornbots_pkg`: use
  `ros2 run thornbots_pkg operator_workflow` with the existing subcommands and
  flags. Mapping/localize also supervise the image-provided read-only Foxglove
  bridge on port 8765 and stop it with the workflow; localization gates and
  robot movement are unchanged
  ([thornbots_pkg #33](https://github.com/Thornbots/thornbots_pkg/pull/33),
  [sentry_localization #24](https://github.com/Thornbots/sentry_localization/pull/24),
  [startup #12](https://github.com/Thornbots/isaac-ros-startup/pull/12);
  [validation](docs/investigations/operator-workflow-move-2026-10-27.md)).

- The [field-mapping procedure](docs/investigations/mapping-procedure-2026-10-26.md)
  (deliberately mirrored to the Notion mapping doc) covers boot-pose provenance
  and the SLAM save gate, stopping boot mapping, clock sync, capture, save,
  registration, AMCL check and match-boot recheck, using the baked release image
  with manual head controls and CV suppression. The
  [package workflow](https://github.com/Thornbots/sentry_localization/pull/23)
  owns the gate rationale ([sentry_localization #21](https://github.com/Thornbots/sentry_localization/pull/21));
  match boot keeps rf2o off after false-motion head-sweep replay findings. No
  behavior changes.

- Launch-time lidar translation/yaw and scan-frame blind-sector overrides,
  including sectors across scan zero. Defaults use the Oct 26 CAD mount and
  robot-measured scan zero/self-filter; the spawned sim sensor matches the TF
  ([thornbots_pkg #32](https://github.com/Thornbots/thornbots_pkg/pull/32),
  [sim #50](https://github.com/Thornbots/sim/pull/50),
  [measurement and validation](docs/investigations/lidar-mount-2026-10-26.md)).

- [CAD odometry pod identities](docs/investigations/sentry-cad-2026-10-26.md#odometry-pods),
  with wheel positions, rolling directions and firmware encoder/field signs.
  The missing motor-to-CAD yaw datum limits source-part assignment. The models
  omit the pods.

- Passive parked room health checks with dated evidence and PASS/FAIL/SKIP for
  serial/head TF rates, scan geometry, rf2o output, stamps and stationary drift,
  plus optional camera and stale-CV blocks
  ([thornbots_pkg #26](https://github.com/Thornbots/thornbots_pkg/pull/26)).
  Run from the robot container using the
  [bring-up command reference](thornbots_pkg/README.md#parked-room-health-check);
  the observer issues no motion commands or MCB probes.

- Container-terminal room/field SLAM snapshot, occupancy registration and AMCL
  convergence workflow, with live raw-odometry EKF seeding and measured AMCL
  starts ([sentry_localization #16](https://github.com/Thornbots/sentry_localization/pull/16),
  [thornbots_pkg #24](https://github.com/Thornbots/thornbots_pkg/pull/24);
  [initial results](docs/investigations/fieldday-slam-amcl-2026-10-22.md),
  [follow-up](docs/investigations/fieldmap-divergence-2026-10-22.md)).
  Full-field mapping uses level observation stations with `pause`/`resume`
  scan insertion; field mapping and localization default to raw wheel input
  (`--rf2o` opts in). The operator card uses one session directory, derives the
  referee team, rejects wrong-side/heading registrations and stale boot
  captures, retains separate autosave backups, warns on unsaved stops, and runs
  parked gates automatically during localization
  ([operator safety results](docs/investigations/fieldday-operator-safety-2026-10-22.md)).
  Room sessions capture and prepare without referee input (`robot_id: 0`);
  practice fields can select `--no-referee --team red|blue` while keeping the
  raw-odometry start check. Field startup verifies team/start before the
  backend and gates EKF seeding on referee re-anchoring; contract starts are
  the default, surveyed refinements are bounded to 0.3 m, automatic parked gates
  use 3 s freshness, and EKF/unsaved-launch exits are supervised. After save,
  the NEXT prompt selects `prepare-room` for rooms and the yaw-only alignment
  step for fields ([round-2 validation and limits](docs/investigations/fieldday-round2-2026-10-23.md)).
  No firmware or movement changes.

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

- Unofficial English translations of the RoboMaster 2027 RMUL and RMUC Rules
  and Participant manuals, the shared Robot Building Specifications Manual and
  the rule-change preview, as six PDF editions beside their Chinese sources,
  checked against rendered pages, with translated contents/table/figure lists,
  English flowcharts and a reproducible renderer. See the
  [translation index](docs/rules/rm2027/README.md); the game context gains an
  [RMUL 2027 summary](docs/ARCC_2026_SENTRY_CONTEXT.md#robomaster-2027-rmul-base-rules)
  of Sentry, field and armor changes.

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
- MCBV3 shared headers now live at `MCB-project/src/util/HitTracker.hpp`,
  `MappingMachine.hpp` and `ImuRecalibration.hpp`; includes and firmware
  coordination docs use the matching paths. Firmware behavior is unchanged.

- Correct the hosted parked E2E idle-look zone to match its existing scene
  frame, restoring camera acquisition after patrol removal without changing
  paths or acceptance gates ([evidence](docs/investigations/sentry-cad-2026-10-26.md#e2e-idle-zone-regression)).
- Adopt the team's 2026-10-26 low-resolution sentry CAD for robot/sim head,
  lidar, IR camera, muzzle and armor geometry, with a matching self-filter and
  nominal map-slice height
  ([thornbots_pkg #30](https://github.com/Thornbots/thornbots_pkg/pull/30),
  [sim #48](https://github.com/Thornbots/sim/pull/48),
  [sentry_localization #20](https://github.com/Thornbots/sentry_localization/pull/20)).
  The Oct 26 five-pose robot fit replaces the authored FOV-marker yaw with scan
  zero 0.5907 rad (33.84°) and the verified scan-frame blind sector
  -0.5585..1.0123 rad; the muzzle keeps its pitch-axis aiming contract with the
  CAD lateral offset. The supplied CAD's 103.885 mm armor lower-edge stagger
  exceeds the 2027 manual's S124 limit of 100 mm; it was accepted on
  2026-10-26 as a mechanical deviation with no material CV impact, and the sim
  test pins a temporary 104 mm bound until the plates are corrected. The
  [dated investigation](docs/investigations/sentry-cad-2026-10-26.md) holds the
  archive SHA256, frame derivation and tests. Scan-plane height and estimator
  robustness remain separate acceptance work.
  Follow-up: `camera` is the D435's RGB lens (32.5 mm left of the CAD cover
  centre) in both URDFs, and detections are deprojected from it, so the real
  robot's aim shifts 32.5 mm left at any range (it had landed 32.5 mm right;
  the sim hid it because its detector shared the frame). The firmware barrel
  offset uses the 1.9 mm bore, `sim`'s `simplify_urdf` generator, config and
  vendored decimator are removed (edit `urdf/sentry_v2` directly), and the CAD
  map-slice height is pinned
  ([sim #53](https://github.com/Thornbots/sim/pull/53),
  [thornbots_pkg #36](https://github.com/Thornbots/thornbots_pkg/pull/36),
  [MCBV3 #110](https://github.com/Thornbots/MCBV3/pull/110)).

- Raise host quality tooling to pytest 9.0.3 for CVE-2025-71176 (insecure
  temporary-directory handling), retaining the other tooling pins. Package CI
  uses the patched tooling snapshot; the native Mac environment requires
  pytest >=9.0.3 and locks 9.1.1; firmware CI keeps its existing snapshot
  ([isaac_ros_common #19](https://github.com/Thornbots/isaac_ros_common/pull/19)).

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
  non-target frame is non-firing with `turn_to_hit` set. Firing requires a
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

- Simulation and AMCL use the real field assembly (sim #29, preserving the
  field frame; [sim #30](https://github.com/Thornbots/sim/pull/30)) for Gazebo
  geometry and match shot occlusion, with the corrected export that restores
  the bar near y = +3 m. Localization ships one canonical `clean_map`,
  regenerated at 2 cm resolution with one-cell obstacle growth; the alternate
  map and old annotated image are removed, and the map YAML and tuning are
  unchanged. See [sim #37](https://github.com/Thornbots/sim/pull/37),
  [field geometry](sim/README.md#the-world-frame),
  [saved map](sentry_localization/README.md#saved-map) and
  [sentry_localization #14](https://github.com/Thornbots/sentry_localization/pull/14).
  Clearance for every firmware route is not established.

- Sim lidar uses the measured angle-compensated sentry A2M8 grid (720 bins),
  range limits and cadence, with scan timing and infinity return handling
  before the shared self-filter. Model approximations remain documented at the
  [sensor owner](sim/README.md#lidar-format-and-model-limits)
  ([sim #31](https://github.com/Thornbots/sim/pull/31)).

- The sim MCB emulator's PTY link is unique per stack
  (`/tmp/mcb_emulator_pty-<GZ_PARTITION>-<ROS_DOMAIN_ID>`), so concurrent sim
  stacks no longer steal each other's UART. A link owned by a live stack is
  refused, but a new stack replaces a stale link pointing to its own reused
  `/dev/pts` number after an interrupted teardown, so one failed teardown no
  longer aborts later E2E stages. Sim only; no robot or wire change
  ([sim #32](https://github.com/Thornbots/sim/pull/32),
  [sim #40](https://github.com/Thornbots/sim/pull/40),
  [workspace #87](https://github.com/Thornbots/thornbots_workspace/pull/87)).

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
- USB installs hand boot control back to the installed NVMe after NVIDIA's
  boot-order rewrite, remove the temporary installer entry, and validate
  passwordless sudo ([package change](https://github.com/Thornbots/isaac_ros_common/commit/daddcde43b663f811de1e7d80c29894a25d4f182)).
  The NVMe boot entry uses a full hardware device path (short `HD()` entries
  fail to boot after the 39.2.1 firmware update;
  [1ebf714](https://github.com/Thornbots/isaac_ros_common/commit/1ebf714),
  [bb8ba8a](https://github.com/Thornbots/isaac_ros_common/commit/bb8ba8a)).
  Firstboot marks host setup done only after it succeeds
  ([4f8616b](https://github.com/Thornbots/isaac_ros_common/commit/4f8616b)) and
  waits for tailscaled before logging in
  ([c95e286](https://github.com/Thornbots/isaac_ros_common/commit/c95e286)).
  Rebuild existing installer ISOs to include these fixes. Reflash guidance adds
  the serial-console route, reinstall-loop diagnosis, safe capsule-variable
  writes and corrected ISO paths. Standard now runs JetPack 7.2.1 on firmware
  39.2.1.

- isaac_ros_common's README now links this fork's clone, image and Mac
  setup ([isaac_ros_common #8](https://github.com/Thornbots/isaac_ros_common/pull/8)).
  Standalone MCB flashing points at this repo's GitHub CI ELF artifacts and
  the current build path instead of GitLab
  ([MCBV3 #95](https://github.com/Thornbots/MCBV3/pull/95)).

- Construct localization backends and their lifecycle managers in one process
  to avoid startup service-response discovery races, and remove the drift suite's
  automatic robot restart. Startup errors identify the missing TF link.
  The sim clock bridge uses UDP-only DDS so a stale shared-memory reader
  port cannot block global time publication. Portable CI dependency pins follow
  the integrated UART contract. See
  [localization #9](https://github.com/Thornbots/sentry_localization/pull/9),
  [sim #26](https://github.com/Thornbots/sim/pull/26) and
  [T30 validation](docs/t30-localization-startup-2026-10-16.md), which
  predates the later field/map and parked-localization fixes.

- Add opt-in tracker innovation diagnostics and estimation-bench radius/prior
  controls; defaults are numerically identical to before and tracker tuning,
  validity and estimation limits are unchanged. See
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

- Hit reporting: firmware retains the latest hit through control cycles until a
  complete REF_SYS write reports it, in radians relative to the current chassis
  heading, positive CCW (the next report uses 123 until another hit); the wire
  payload is unchanged, and one-cycle control/UI reactions stay independent of
  the latch. The Jetson grants hit-turn permission per frame: any held target
  estimate, including coasting/predicted tracks, clears `turn_to_hit`, while no
  estimate permits it without a cooldown; the incorrect gun-relative Jetson hit
  reaction is removed. See [MCBV3 #93](https://github.com/Thornbots/MCBV3/pull/93),
  [firmware latch](https://github.com/Thornbots/MCBV3/pull/94),
  [emulator tests](https://github.com/Thornbots/sim/pull/22),
  [thornbots_pkg #14](https://github.com/Thornbots/thornbots_pkg/pull/14),
  [wire contract](ros2_dji_serial_bridge/UART_PROTOCOL.md#ref_sys-id3--referee-system-status),
  [T31 validation](sim/docs/t31-hit-contract-2026-10-14.md) and the
  [hosted comparison](thornbots_pkg/docs/hit-permission-2026-10-15.md).

- E2E GUI stages use a dedicated RViz view and scene-only gz layout. The
  sim recorder produces synchronized 1080p H.264 demos retimed from `/clock`,
  with stage/time/score captions and scored shot markers. See
  [recording workflow](sim/README.md#record-an-e2e-demo)
  ([sim #20](https://github.com/Thornbots/sim/pull/20)).

- Aim defaults to spin alignment gating: hold a steady center-to-shooter line
  and schedule fire for the predicted facing panel; nonspinning prediction
  retains panel lead and hysteresis. Board lockstep learns one 5 ms batch ahead
  while retaining wall deadlines and timeout rejection, Renode installation
  avoids the temporary-directory cleanup prefix that deleted writable fixtures,
  and firmware sleeps between SysTick interrupts during the three-second
  power-on guard. The hosted and Renode board measurements are historical
  simulation results, not physical-board or final-release acceptance; see the
  [spinning and board investigation](sim/docs/aim-accuracy-2026-10-12.md#spinning-correction-and-board-comparison).

- Calibrate the hosted direct-sensor aim fixture's 8 ms gyro age (fixture-specific;
  board execution uses its full IMU filter) and add inherited muzzle motion and
  pose-latency controls. Firmware yaw prediction uses geared torque and
  configured friction, control integration uses the actual 1 ms interval, and
  sim models estimated passive rolling resistance. Native failures remain
  failures, not accepted accuracy results; moving-shot accuracy remains an
  acceptance gate. See the [dated accuracy investigation](sim/docs/aim-accuracy-2026-10-12.md).

- Sim pose diagnostics distinguish local EKF field-alignment error from
  globally corrected localization error, retain capture-time TF exceptions,
  and retry delayed pose telemetry for up to one simulated second. `mcb_parked`
  bounds displacement at 0.03 m (tightened from 0.10 m); capture-stamp and
  native accuracy failures remain visible. See the
  [follow-up investigation](sim/docs/aim-followup-2026-10-12.md).

- Aim and tracking use raw, never-relocalized MCB `odom`; EKF and RELOCALIZE
  correct only navigation `nav_odom` through a translation-only
  `nav_odom->odom`. The EKF no longer feeds its own heading back, the relay
  sends RELOCALIZE only when the navigation offset changes, and a team-start
  reanchor or sim clock reset is never interpolated across. POSE and CV_TARGET
  retain their current UART layouts but require matching firmware and Jetson
  updates. `mcb_drive` rejects zero native hits. The
  [controlled comparison and repeats](sim/docs/aim-localization-coupling-2026-10-11.md)
  predate the current firmware auto-drive route. See [MCBV3 #89](https://github.com/Thornbots/MCBV3/pull/89),
  [bridge #8](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/8),
  [thornbots_pkg #13](https://github.com/Thornbots/thornbots_pkg/pull/13),
  [sentry_localization #6](https://github.com/Thornbots/sentry_localization/pull/6), and
  [sim #16](https://github.com/Thornbots/sim/pull/16).

- MCB driving stages select firmware waypoints and spin through DBUS instead of
  scripted chassis velocities. Renode board execution is the stage default;
  hosted execution remains an explicit fixture. The emulator supplies three-axis
  IMU samples and derives traction from gz model mass. Jetson UART is unchanged.
  All three board stages pass at diagnostic tier; calibrated combat accuracy and
  repeatability remain open. See
  [sim #19](https://github.com/Thornbots/sim/pull/19),
  [MCBV3 #92](https://github.com/Thornbots/MCBV3/pull/92),
  [bridge #11](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/11), and
  [board-stage verification and limits](sim/docs/mcb-auto-drive-2026-10-12.md).

- Automatic firmware aiming releases the indexer's stop flag when shooting
  becomes allowed after calibration/SETUP. Existing shot-eligibility gates and
  manual aiming are retained. Sim models a loaded-cartridge reverse homing
  stop and checks CAN output as well as issued requests. Physical-robot
  validation and repeatability remain open. See
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

- Sim runs one native MCB control tick per gz physics step, supplies DJI motor
  feedback and applies motor outputs as forces instead of gz setpoint
  controllers. The UART bridge waits for the PTY. See
  [sim #14](https://github.com/Thornbots/sim/pull/14),
  [MCBV3 #88](https://github.com/Thornbots/MCBV3/pull/88),
  [bridge #7](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/7) and the
  [motor validation](sim/docs/mcb-motor-plant-2026-10-11.md).

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

- A fresh clone stays on the pinned package commits; the README no longer
  checks out every submodule's branch tip. Start work with `git switch -c` in
  the package. See [Working with submodules](README.md#working-with-submodules).

- Non-spinning aiming holds the most face-on physical panel until another
  faces the shooter more squarely. The measured 0.3 rad margin suppresses
  noise-driven panel flips; track changes, invalid states, spinning and timeout
  clear the hold. See [thornbots_pkg #9](https://github.com/Thornbots/thornbots_pkg/pull/9),
  [sim #11](https://github.com/Thornbots/sim/pull/11) and the
  [panel-choice measurements and compiled-firmware timing checks](sim/docs/panel-choice-2026-10-11.md).

- Sim temporary-world cleanup tolerates repeated shutdown events, and the native
  log checker rejects launch exceptions. See [sim #10](https://github.com/Thornbots/sim/pull/10) and the
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
  Inside this workspace pick "MCBV3 (Isaac ROS workspace)" so the policy hooks
  run. Untested against a board: no flash yet.
  [MCBV3 #112](https://github.com/Thornbots/MCBV3/pull/112)

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
  fire delay under `min_fire_delay_s` (now 40 ms). The MCB holds a pending
  shot instead of letting the next non-fire frame cancel it, and the sim
  indexer exits balls 20 ms into a feed. Real robot: verify shot timing and
  that no shots drop.
  [MCBV3 #110](https://github.com/Thornbots/MCBV3/pull/110),
  [thornbots_pkg #36](https://github.com/Thornbots/thornbots_pkg/pull/36),
  [bridge #27](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/27),
  [sim #53](https://github.com/Thornbots/sim/pull/53).

- Sentry auto-aim turns the barrel's line through the CV aim point: the
  firmware adds the barrel's 12.8 mm left-of-yaw-axis offset (sentry_v2 CAD)
  to its yaw solve, a real-robot aim change of about 0.6 deg at 1.2 m; verify
  on the robot. Shots still land about 15 mm low and 8 mm left from gimbal
  settling error, which stays with the hardware-tuned gains. Sim `shots.jsonl`
  records each shot's position on its panel.
  [MCBV3 #110](https://github.com/Thornbots/MCBV3/pull/110),
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

- Sentry firmware reports POSE `odom_status` 2 before the first successful
  Pico I2C read or when its age reaches 500 ms; healthy reads report 0. The
  threshold accommodates the measured 260 ms Pico cadence without changing
  odometry values ([MCBV3 #105](https://github.com/Thornbots/MCBV3/pull/105),
  [bridge #24](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/24)).

- Sim's CV bench armor validation checks ground clearance and the 400 mm
  maximum lower-edge height instead of an unsupported 60 mm minimum; rule
  citations link to the verified workspace comparison
  ([sim #51](https://github.com/Thornbots/sim/pull/51)).

- Launch stopping lists and signals only verified container-owned ROS
  launch/run trees, including when the container shares the host PID namespace.
  PID 1, host processes and non-ROS roots are refused; the force bypass is gone.
  Stop matching trees directly with `kill_launch.sh --match <literal-substring>`
  ([isaac_ros_common #17](https://github.com/Thornbots/isaac_ros_common/pull/17)).

- rf2o no longer carries a permanent offset when the robot moves before its
  first scan, or when rf2o restarts while moving: it seeds at that scan's own
  odometry stamp, waits in a bounded queue for scan-time TF and odom, and caps
  that wait at 1 s so a stalled `/odom` or joint stream degrades rather than
  stopping rf2o. Failed matches without wheel fallback retain the coherent
  scan/pose/head reference so recovery preserves the full displacement.
  Startup topic aliases and remaps use resolved subscription names. This
  affects the normal rf2o/EKF launch; the competition `localize` default (raw
  wheel odometry) does not use rf2o.
  [rf2o_laser_odometry #16](https://github.com/Thornbots/rf2o_laser_odometry/pull/16).

- rf2o's `reference_scans` is available but off by default; this workspace
  keeps sentry_localization at `nightly` without enabling it. When enabled, it
  matches parked scans against earlier scans from the same head angle once
  `/odom` has held still for 2 s; wheel motion returns it to consecutive-scan
  matching. The combined matcher retains scan-time startup and transactional
  failure recovery, caps its reference bank, and grades speed independently of
  anchor age. `/scan_odom` twist reports robot-frame vx/vy from consecutive
  accepted poses, with no robot consumer. Sim results with references enabled
  do not describe the default configuration and are unverified on hardware. See
  the [investigation](docs/investigations/t39-parked-drift-2026-10-25.md),
  [rf2o_laser_odometry #17](https://github.com/Thornbots/rf2o_laser_odometry/pull/17),
  [sim #43](https://github.com/Thornbots/sim/pull/43).

- SLAM and AMCL no longer treat head motion as robot motion. Both cached the
  head-mounted lidar's mount from the first scan; slam_toolbox now tracks the
  `lidar` frame (`slam.yaml`, also the default robot launch) and AMCL refreshes
  the mount position each scan. Start new mapping sessions; old serialized
  graphs used the `root` base. See the
  [investigation](docs/investigations/fieldmap-divergence-2026-10-22.md) and
  [sentry_localization #16](https://github.com/Thornbots/sentry_localization/pull/16).

- E2E referee parameter requests have a two-second response deadline and
  bounded retries of the current desired state, so a lost bring-up response
  no longer permanently blocks a later `drive=simple` update. Sim fixture
  only; see [sim #39](https://github.com/Thornbots/sim/pull/39) and
  [workspace #85](https://github.com/Thornbots/thornbots_workspace/pull/85).

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
  `mcb_parked` fails any cell whose map localization has p95 above 0.15 m,
  max above 0.20 m or under 95% stamped coverage
  ([sim #41](https://github.com/Thornbots/sim/pull/41)). Slow scan-odometry
  drift while parked is still uncorrected below AMCL's update thresholds
  (0.1 m translation or 0.05 rad odometry rotation); see the
  [rf2o notes](sentry_localization/README.md#configrf2oyaml) and
  [robot validation T39](docs/ROBOT_TESTS.md#parked-localization). See
  [workspace #88](https://github.com/Thornbots/thornbots_workspace/pull/88)
  for revisions and measurements.

- The sentry's rough auto-drive route keeps the spinning chassis clear of the
  wall end beside its start: the wall leg moves from 2.236 m to 2.5 m to the
  side, and only its two waypoints use a 0.2 m arrival tolerance (others keep
  0.5 m). The old route could strike the wall end and wedge until the 15 s
  stuck timer. Not yet driven on the real field. See
  [MCBV3 #101](https://github.com/Thornbots/MCBV3/pull/101).

- The UART bridge drops CV decisions aged 200 ms or more, invalid/future
  stamps and frames behind a busy TX queue at the final nonblocking write
  boundary. Fresh aim/fire payloads and ROS/simulation decision stamps stay
  intact. See [bridge #19](https://github.com/Thornbots/ros2_dji_serial_bridge/pull/19)
  and the [freshness contract](ros2_dji_serial_bridge/UART_PROTOCOL.md#cv-decision-freshness).
  The real-bridge PTY fixtures stamp each newly created decision to follow this
  contract ([sim #38](https://github.com/Thornbots/sim/pull/38)).

- Nightly results require a zero runner exit and the complete valid stage
  report, so interrupted runs cannot pass after setup alone. Failure-driven
  SKIPs remain visible; malformed, duplicate or impossible records fail.
  See [nightly tests](docs/CI.md#nightly-tests).

- Automatic agent-container cleanup removes only resources labelled for
  the creating invocation, including partial startup; duplicate task refusal
  preserves the existing container and volumes. Interruptible command waits
  let signal cleanup run while the helper is active and preserve piped input.
  Existing volumes are not silently reused. See
  [isaac_ros_common #15](https://github.com/Thornbots/isaac_ros_common/pull/15).

- RF2O skips scans whose range count or angular geometry differs from its
  initialized grid, with a throttled warning, instead of reading past the
  scan. See [rf2o_laser_odometry #10](https://github.com/Thornbots/rf2o_laser_odometry/pull/10).

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
