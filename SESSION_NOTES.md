# Sim/SLAM status

Goals, what's done, and what's still open for the `sim` (gz-sim) and
`sentry_pkg` (SLAM) packages. Written for future-me (or a future Claude
session) picking this back up — read this before continuing that work.

This file itself (along with `CLAUDE.md`, `DOCKER.md`,
`ARCC_2026_SENTRY_CONTEXT.md`, and `.claude/`) lives in its own repo,
[`Thornbots/sentry_workspace`](https://github.com/Thornbots/sentry_workspace)
(2026-07-24) — separate from `sim`/`sentry_pkg`/`sentry_localization`, which
each remain their own repos.

## Overall goal

Get a gz-sim simulation of the "sentry" robot running, driveable, and mapping
a room autonomously via `slam_toolbox`, inside the `isaac_ros_dev-x86_64-container`
Docker container (attach via `isaac_ros_common/scripts/run_dev.sh`).

Current dev priority: **CV (target detection/tracking) first, timing-based
firing logic second** — localization is considered good enough for now (see
`ARCC_2026_SENTRY_CONTEXT.md` for why firing logic needs a heat/ammo budget
model once it starts). Don't front-run firing logic while CV is still in
progress unless explicitly asked.

## Standing procedural rules

- **Always fully restart `sim` (fresh spawn) before restarting SLAM/explorer**
  — partial restarts tend to leave stale TF/pose state ("pos desync").
- Launch `sim` with its GUI, not headless — user watches the gz sim window
  during testing. This includes `sim/test/localization/
  run_localization_drift_tests.py` (renamed from `run_slam_drift_tests.py`
  once it grew `--backend amcl`/`--backend ekf` alongside its original
  slam_toolbox-only coverage) — GUI is now its default (2026-07-20: was
  headless-by-default with an opt-in `--gui`, flipped since the user wants
  to watch/sanity-check scenario behavior live; pass `--headless` to opt
  back out, e.g. for a quick unattended run). Always launch it as `-u
  admin` via `dexec.sh -d`, not a bare `docker exec -d`, or the gz-sim
  window fails to open — see the `isaac-ros-docker` skill's "Launching GUI
  apps" section.
- `docker exec` sessions need `ROS_DOMAIN_ID=42` exported explicitly (login
  shells get it from `/etc/bash.bashrc`, non-interactive `docker exec -lc`
  invocations don't reliably) — see `DOCKER.md` / the `isaac-ros-docker`
  skill.

## What's done

- Core sim pipeline works end-to-end: `ros2 launch sim sim.launch.py` spawns
  the robot in `ARCC_Field_2026.sdf`, bridges raw `/scan`, `/sim/raw_odom`,
  `/sim/raw_joint_states`, `/cmd_vel`, `/clock`, head-pan control between gz
  and ROS.
- **Pose ownership moved entirely to `sentry_pkg` (2026-07-20 refactor)**:
  `sentry_pkg` no longer depends on sim's URDF/TF or raw `/odom` at all.
  - `sim/pose_emulator.py` (new) repackages sim's raw ground-truth
    `/sim/raw_odom` + `/sim/raw_joint_states` into
    `dji_serial_bridge/msg/RobotPose` on `/pose` — the exact same
    topic/message real hardware's Type-C board publishes (via
    `ros2_dji_serial_bridge`'s `dji_serial_bridge_node`, currently still on
    `~/pose` i.e. `/dji_serial_bridge/pose` — **that node still needs
    updating to publish flat `/pose` to match**, tracked as a `TODO` in
    `dji_serial_bridge_node.cpp`; sim and `pose_translator` were switched
    first since that's the code actually being iterated on right now).
  - `sentry_pkg/pose_translator.py` (pre-existing, previously unwired into
    any launch file) is now the sole consumer of `/pose`, for both sim and
    real hardware — same code path either way. It publishes `/odom`,
    `/joint_states`, and `odom->root` TF, replacing `odom_to_tf.py` (now
    deleted).
  - `sentry_pkg/launch/auto.launch.py` now also runs its own
    `robot_state_publisher`, off `sentry_pkg/urdf/sentry.urdf.xacro` (a
    separate, previously-unused, Onshape-exported copy of the URDF — not
    `sim/urdf/sentry.urdf.xacro`), fed by `pose_translator`'s
    `/joint_states`. `sim.launch.py` no longer runs `robot_state_publisher`
    at all — sim's URDF is now only used for spawning geometry into gz, not
    for any ROS TF.
  - Net effect: `sentry_pkg` is now genuinely hardware-agnostic — it only
    ever consumes `/pose` + `/scan`, identically whether that `/pose` comes
    from real Type-C hardware or `sim/pose_emulator.py`.
  - `auto.launch.py` now also directly launches the real drivers behind a
    `real_hardware` arg, **default `true`**: `dji_serial_bridge_node`
    (`/pose`, device/baud left at its own defaults) and `sllidar_ros2`'s
    driver (`/scan`, via `lidar_serial_port`/`lidar_baudrate` args,
    defaulting to `/dev/ttyUSB0`/`115200` for the RPLIDAR A2M8).
    `use_sim_time` is no longer its own arg — it's derived from
    `real_hardware` (false/wall-clock when real hardware is running, true
    when it's not, since that's exactly when sim's `/clock` exists to use).
    Run against sim with `real_hardware:=false`.
- `sentry_pkg`'s SLAM (`auto.launch.py`) depends only on `/pose` (via
  `pose_translator`) + `/scan`, no direct real-hardware dependency — works
  against `sim` or a real driver.
- `sentry_pkg/config/slam.yaml` tuned from scratch.
- `sim/auto_explore.py`: frontier-biased autonomous exploration with
  stuck-detection/escape logic, now reads its own pose from TF (`map ->
  root`) instead of `/odom` (see fixed bugs below for why).
- Chassis redesigned to a free-floating 6DOF `root` body (no joint chain,
  gravity disabled) driven by a single `VelocityControl` plugin off
  `/cmd_vel`; earlier kinematic joint-chain approach (`world -> planar_x ->
  planar_y -> yaw_base -> suspension_z -> root`) was removed entirely.
- Lidar tuned to match a real RPLIDAR A2M8 (min range 0.15m, max 12m, bumped
  noise stddev).
- Spawn height settled at `z = 0.03` (the chassis floats with no ground
  contact, so this is effectively its permanent resting height).
- `docker/fastdds_cable.xml`'s `useBuiltinTransports` fixed to `true` (was
  `false`, which silently killed all local multicast discovery/transport —
  see `DOCKER.md`/`isaac-ros-docker` skill for the full symptom writeup).
- **rviz/TF now confirmed working end-to-end** (2026-07-20): scan renders in
  rviz, and the SLAM map loads correctly when starting `sentry_pkg`. Root
  cause was `fastdds_cable.xml`'s `<initialPeersList>` (hardcoded real-robot
  IP) breaking local discovery — removed. Committed as `4598976 "fixed
  fastdds bugs"` (also drops `RMW_FASTRTPS_PUBLICATION_MODE=ASYNCHRONOUS`
  from `Dockerfile.thornbots`, and disables the `sentry_pkg` apt/clone/build
  block in LAYER 6, now commented out — presumably intentional since
  `sentry_pkg` isn't meant to be baked into the dev image, but worth
  double-checking that wasn't accidental if `sentry_pkg` ever fails to be
  found in the container). Full root-cause writeup, including the
  `PS1`/`bash.bashrc`-sourcing gap that hid this bug for a long debugging
  session, is in `DOCKER.md`'s Troubleshooting section and the
  `isaac-ros-docker` skill — worth reading in full if anything like this
  ("topics/nodes look matched but no data" or "rviz TF empty") recurs.
- The container's `/dev/dri/card0`/`card1` (two GPUs — NVIDIA is `card0`,
  Intel iGPU is `card1`) had a host/container `video` group GID mismatch
  blocking gz-sim's GPU lidar rendering even though `renderD128`/`129` were
  already world-writable — same class of issue as before, container-local,
  doesn't survive container recreation, fixed for now via `chmod o+rw`
  (will need redoing after the next container recreation).
- **gz-sim defaulting to the Intel iGPU instead of NVIDIA, confirmed fixed
  (2026-07-20)**: this is a laptop with Intel iGPU driving the actual
  display and NVIDIA as a secondary PRIME-offload GPU. Setting only
  `__EGL_VENDOR_LIBRARY_FILENAMES` (first attempt) was **not** enough — gz
  sim's on-screen GUI window uses GLX, not EGL, so it kept landing on Intel
  regardless (verified via `nvidia-smi` showing 0% util / no processes even
  with the EGL var set). Fix: also set the same vars the host's `prime-run`
  wrapper uses — `__NV_PRIME_RENDER_OFFLOAD=1`,
  `__GLX_VENDOR_LIBRARY_NAME=nvidia`, `__VK_LAYER_NV_optimus=NVIDIA_only` —
  alongside the EGL var. All four are in `~/.isaac_ros_dev-dockerargs`
  (host-side, not `Dockerfile.thornbots`, per the earlier reasoning: this is
  this dev machine's own dual-GPU quirk, not something the real robot
  needs). Verified via `nvidia-smi`: `ign gazebo server`/`gui` now show up
  as real GPU processes using several hundred MB and nonzero utilization,
  and the earlier `libEGL warning: failed to open /dev/dri/card0` /
  `failed to create dri2 screen` log spam is gone.

- **Code comment cleanup (2026-07-26)**: trimmed every in-code comment/
  docstring over 10 lines across `sentry_pkg`, `sentry_localization`,
  `sim`, `realsense-yolov8-nitros-bridge`, and `ros2_dji_serial_bridge`
  down to interface facts only; moved the removed tuning
  history/postmortems/design rationale (including the 260-line module
  docstring and 89-line `CORRECTION_FRACTION` postmortem in
  `run_localization_drift_tests.py`, and the `amcl.yaml`/`ekf.yaml` tuning
  histories) into each package's own `README.md` under a `## Notes`
  section, with `# see README.md` pointers left in code where that
  history still matters for future tuning. `ros2_dji_serial_bridge/
  README.md` was previously empty and now has real content (message
  table, wire-format diagram, diagnostic decision table). Committed and
  pushed per-package (`sentry_pkg@d2a45a8`, `sentry_localization@8ab0de1`,
  `sim@f08740f`, `realsense-yolov8-nitros-bridge@3605d5f`,
  `ros2_dji_serial_bridge@34c7901`) — purely comment/doc changes, no logic
  touched.

### Bugs found and fixed (for context, not still open)

- TF tree had two nodes both broadcasting `root`'s parent transform
  (`robot_state_publisher` via the old joint chain, `odom_to_tf` via
  `/odom`) — caused `slam_toolbox` "queue is full" / stale-transform spam.
  Fixed by having sim skip `odom_to_tf` and point `slam_toolbox` at `world`
  directly (later moot once the joint chain was removed and `odom_to_tf`
  became the sole `root`-parent source again).
- gz-sim's `OdometryPublisher` plugin hardcoded `/odom`'s Y field to 0 for
  the old joint-constrained base, breaking `auto_explore.py`'s position
  tracking — confirmed gone on the free-floating body; fixed generally by
  reading pose from TF instead of `/odom` directly.
- A `/joint_states` velocity field pegged at the 10 rad/s limit looked like
  a runaway spin (undamped near-massless connector link) but turned out to
  be a `JointStatePublisher` reporting glitch — real position barely moved.
  Kept the mass/inertia/damping bump anyway since it's harmless.
- `ros_gz_sim create -topic` hung waiting for `/robot_description`; switched
  spawning to `-string` (raw URDF text in process args).
- `headlink` joint's WASD slider moved the whole robot instead of just the
  head — needed a real `<limit>` (was `continuous`, giving gz's GUI slider a
  ±1e16 sentinel range).
- `head_sweep.py` (slow head sweep to reduce lidar blind spot) corrupted the
  map via TF timing slack during fast rotation — code/bridge kept, removed
  from the default launch.
- `ros-humble-ros-gz` (provides `ros_gz_sim`/`ros_gz_bridge`/`ros_gz_image`,
  needed by `sim`) went missing after a container recreation — same
  container-local-install-doesn't-survive-recreation pattern as the
  `robot_localization` fix above, since LAYER 2b in `Dockerfile.thornbots`
  intentionally doesn't install it by default (real hardware never launches
  gz-sim). Symptom: `ros2 launch sim ...` fails immediately with
  `PackageNotFoundError: "package 'ros_gz_sim' not found`, which cascades
  into `run_localization_drift_tests.py`'s (then still named
  `run_slam_drift_tests.py`) `wait_for_scans_flowing` timing out on
  every scenario (sim never actually started). Fixed by rerunning
  `sudo isaac_ros_common/docker/scripts/install-sim.sh` (reinstalls the apt
  package + rebuilds `sim`) — this is the documented fix for exactly this
  situation, not a new workaround. If this recurs after another container
  recreation, run that script before assuming a real SLAM regression.

## Currently open / next up

- **Found (2026-07-24): the robot drives straight through obstacles in sim,
  by design, not a bug** — investigated after the user noticed the "test
  bench" (`sim/test/localization/run_localization_drift_tests.py`'s
  `drift_correction_obstacle` scenario, via `spawn_box_obstacle()`) letting
  the robot pass through its spawned `unmapped_test_obstacle` box.
  `sim/urdf/sentry.urdf.xacro`'s `root` link comment (~line 112) explains
  why: **no link in the model carries any `<collision>` geometry at all**,
  deliberately — an earlier kinematic joint-chain design that gave `root` a
  hard rotation lock broke `set_pose` teleporting (gz-physics only honors
  direct pose writes, needed by `auto_explore.py`'s grid sweep, on a link
  its FreeGroup API sees as genuinely free-floating; a jointed link doesn't
  qualify). The fix made `root` free-floating *and* stripped all collision
  geometry, specifically so no contact torque could ever reach it and
  defeat the soft (inertia-based) rotation lock. That solved tipping/
  teleporting, but as a side effect the chassis has zero physical presence
  in gz-physics — it can't collide with anything, mapped wall or
  `drift_correction_obstacle`'s spawned box alike. The box itself does have
  real `<collision>` geometry, so lidar/SLAM see it as expected; only the
  robot's own body passes through it. Not yet decided whether/how to fix
  (e.g. a collision-only proxy shape that doesn't feed torque back into
  `root`) — revisit if obstacle-avoidance behavior (not just
  obstacle-*mapping*) becomes something `auto_explore.py` needs to
  demonstrate.
- **Add an EKF fusing `/odom` + `/scan` for `odom->root`** — replace
  `pose_translator`'s plain republish (see the pose-ownership refactor
  above) with real fusion. Planned out in detail 2026-07-20 (see
  `ARCC_2026_SENTRY_CONTEXT.md`'s "Next up" section for the clean summary;
  this entry is the log of how the plan got there):
  - Step 1: **done (2026-07-20)** — `ekf_node` now runs cleanly. Turned out
    not to be a genuine ABI mismatch: `ros-humble-robot-localization` was
    never actually installed in the container (stale apt index made it look
    absent-with-conflict), and the installed `ros-humble-diagnostic-updater`
    4.0.6 was a header-only build missing `libdiagnostic_updater.so`
    entirely (`ekf_node` failed with "cannot open shared object file", not
    an ABI error). Fixed via `apt-get update` (refreshes the index) +
    `apt-get install ros-humble-robot-localization` +
    `apt-get install --only-upgrade ros-humble-diagnostic-updater` (pulls
    4.0.7, which restores the `.so`). No source rebuild needed — apt has a
    working combo now. Added `robot_localization` to
    `sentry_pkg/package.xml` (`exec_depend`) and to
    `isaac_ros_common/docker/Dockerfile.thornbots`'s commented-out LAYER
    IKD block (still disabled, for consistency with the rest of that list —
    not installed into the baked image). **Caveat**: this apt install is
    container-local (like the GPU/udev fixes elsewhere in this doc) — will
    need redoing after the next container recreation unless LAYER IKD gets
    reactivated.
  - Step 2: **done (2026-07-20)** — vendored `rf2o_laser_odometry` (upstream
    `MAPIRlab/rf2o_laser_odometry`, `ros2` branch, no Thornbots fork needed)
    as a new Dockerfile layer, and wired an `rf2o_laser_odometry_node` into
    `auto.launch.py` publishing `/scan_odom`, `publish_tf: false` (EKF will
    own `odom->root`, not this node). Verified live: publishes at ~10 Hz,
    no errors beyond one benign startup race. Not consumed by anything yet.
  - **Lidar is on the head, and the head moves independently of SLAM** —
    corrected understanding during planning: it's not the unused
    `head_sweep.py` placeholder (dead code, not wired into any launch).
    Real head motion (owl-like scanning with a camera, presumably for
    CV/targeting) is controlled by firmware on the MCB/Type-C board, not
    readable or characterizable from this repo at all. That means the
    scan-matcher/EKF pipeline must be defensive by construction rather than
    tuned to a known head-motion profile.
  - **Important correction (2026-07-20, discovered while implementing step
    3)**: the original plan assumed a per-scan TF-freshness check would be
    enough to protect `rf2o` from head motion. Reading `rf2o`'s actual
    source (`CLaserOdometry2DNode.cpp`, `setLaserPoseFromTf()`) shows it
    only queries the `lidar->base_frame_id` transform **once**, on its
    first received scan, and caches it for the node's entire lifetime —
    it never re-queries TF per scan at all. So a per-scan freshness gate
    can't fix anything here; `rf2o` structurally assumes a rigidly-fixed
    sensor mount, which our head-mounted lidar isn't. Three options were
    considered:
    - **(a) — chosen and implemented.** Gate `rf2o`'s input scans so it
      only ever sees scans (including its first, which fixes the cached
      transform) while the head is near its home (yaw ≈ 0) position. New
      node `sentry_pkg/sentry_pkg/head_home_scan_gate.py`: subscribes
      `/joint_states` + raw `/scan`, republishes onto `/scan_gated` only
      while `|head_yaw| <= home_yaw_tolerance` (launch arg, default 0.05
      rad). `rf2o`'s `laser_scan_topic` now points at `/scan_gated`
      instead of raw `/scan`. Cheapest option; only produces `/scan_odom`
      updates during head-home windows, which is fine given the EKF only
      needs occasional corrections anyway (wheel odometry drifts slowly;
      see the fusion-frequency discussion below).
    - **(b) — rejected.** Only trust corrections when the head happens to
      be at whatever angle it started at (no explicit "home" homing) —
      not viable per the user: the head changes angle too often for this
      to produce usable windows. (a) above is the viable version of this
      idea, since the robot can be commanded to park the head at home
      periodically, unlike relying on incidental startup angle.
    - **(c) — not implemented, noted for later.** Fork `rf2o` to re-query
      the `lidar->root` transform every scan instead of caching it once —
      the actually-correct fix, letting `rf2o` work at any head angle, not
      just home. Bigger effort (maintaining a patched fork rather than
      vanilla upstream) — revisit if head-away-from-home time turns out to
      dominate and (a)'s home-only windows aren't producing enough
      corrections in practice.
    - Also still worth doing regardless of (a)/(c): add a `laser_filters`
      chain upstream of the scan matcher (already a `package.xml`
      dependency, currently unused in `auto.launch.py`) to strip
      physically-implausible points from mid-turn self-obstruction.
    - Also still worth doing: sanity-gate `rf2o`'s output against wheel
      odometry's delta before it reaches the EKF — but **asymmetrically**:
      per the user, wheel odometry only drifts slowly under normal
      conditions but slips on the ARCC field's "Bumpy Road" zone, and lidar
      data quality itself is good, so `rf2o`/`odom` disagreement during a
      slip event is exactly the signal the EKF should trust, not discard.
      The gate should only catch `rf2o`'s own failure modes, not arbitrate
      normal disagreement between the two sources.
  - Step 4: `sentry_pkg/config/ekf.yaml` + `ekf_node` fusing `/odom` (x, y,
    vx, vy) and gated `/scan_odom` (x, y, yaw), publishing `odom->root`.
    Chassis heading is fixed (holonomic, never rotates) so yaw process noise
    can stay low/tightly trusted. Given (a) above, `/scan_odom` updates will
    already be infrequent/bursty (only during head-home windows) — this
    lines up with the "occasional correction, not continuous" fusion model
    discussed with the user, so `ekf_node`'s default handling of a
    lower-rate absolute-ish correction source should need little extra
    tuning beyond normal covariance work.
  - Step 5: wire into `auto.launch.py` behind a `localization_backend`
    launch arg (`ekf`/`passthrough`) so `pose_translator`'s plain republish
    stays available as an instant fallback rather than being deleted.
  - Step 6: add `robot_localization` to `sentry_pkg/package.xml` — **done**
    (step 1). Vendor `rf2o_laser_odometry` similar to `sllidar_ros2` —
    **done** (step 2, see above).
  - Step 7: verify in sim — watch `odom->root` vs `map->root` drift in
    rviz, confirm `slam_toolbox`'s map quality holds up, tune covariances.
  - Steps 1-2 done, gating (a) implemented; next session should verify (a)
    end-to-end in sim (does the head actually return home often enough for
    useful correction windows?), then move to step 4 (`ekf.yaml` +
    `ekf_node`).
- **Added AMCL as a second, opt-in map->odom localization backend
  (2026-07-20)**: new `auto.launch.py` arg `map_localizer` (later
  consolidated into `localization_mode`, see below) — `amcl` mode
  launches `nav2_map_server` (serving
  `map_file`'s `.yaml`, same basename as the existing posegraph files) +
  `nav2_amcl` (new `sentry_pkg/config/amcl.yaml`, `robot_model_type:
  nav2_amcl::OmniMotionModel` since the chassis is holonomic) + a
  `nav2_lifecycle_manager` node to autostart both; `slam_toolbox` isn't
  launched at all in this mode (AMCL only localizes against a map, never
  builds one). Added `nav2_amcl`/`nav2_map_server`/`nav2_lifecycle_manager`
  to `sentry_pkg/package.xml` and to
  `isaac_ros_common/docker/Dockerfile.thornbots`'s LAYER 8 apt install
  list (all three were already present as transitive deps in the running
  container, just needed an explicit version bump/upgrade — see below).
  **Verified end-to-end in sim (2026-07-20)**: `ros2 launch sentry_pkg
  auto.launch.py real_hardware:=false localization_mode:=amcl` — `map_server`
  loaded `ARCC26.yaml`/`.pgm` correctly, `lifecycle_manager` brought both
  `map_server` and `amcl` to `active`, `map->odom`/`map->root` TF
  published (identity at spawn, as expected), and driving the robot via
  `/cmd_vel` moved `/amcl_pose` correspondingly (x: 0.0 → ~1.93 after
  driving forward) — confirms AMCL is actively scan-matching against the
  map, not just parked at its initial pose. One transient "Message Filter
  dropping message ... timestamp earlier than all the data in the
  transform cache" warning at startup (single occurrence, matches the
  same class of benign startup race already noted for `rf2o` above) —
  not a recurring issue.
  Hit (and fixed) the **exact same `libdiagnostic_updater.so` missing
  bug** documented in step 1 above, this time breaking
  `nav2_lifecycle_manager` instead of `ekf_node` — same root cause
  (`ros-humble-diagnostic-updater` 4.0.6 is a header-only build missing
  the `.so`), same fix (`apt-get update` to refresh the index, then
  `apt-get install --only-upgrade ros-humble-diagnostic-updater` to pull
  4.0.7). Confirms this is a recurring container-local footgun, not a
  one-off — worth checking `diagnostic_updater`'s installed version
  first if *any* nav2/robot_localization node dies with a "cannot open
  shared object file" error after a container recreation.
  `amcl.yaml`'s particle-filter params (`alpha1-5`, `z_hit`/`z_max`/
  `z_rand`/`z_short`, `min_particles`/`max_particles`, etc.) are still
  stock nav2 defaults, not yet tuned against this robot/map — next step
  is comparing AMCL's localization quality/covariance against the
  existing `slam` mode's default over a longer run (drift under the
  arena's "Bumpy Road" zone, recovery from a bad initial pose) before
  tuning further.
- **Consolidated `auto.launch.py`'s 3 separate localization args into one
  (2026-07-20)**: `map_localizer` (`slam_toolbox`/`amcl`, who owns
  `map->odom`), `slam_mode` (`mapping`/`localization`, only meaningful
  when `map_localizer:=slam_toolbox`), and `localization_backend`
  (`passthrough`/`ekf`, who owns `odom->root`) replaced by a single
  `localization_mode` arg with 4 mutually-exclusive values: `slam`
  (default, same as the old `map_localizer:=slam_toolbox` +
  `slam_mode:=localization` + `localization_backend:=passthrough`),
  `mapping` (old `slam_mode:=mapping`), `amcl` (old
  `map_localizer:=amcl`), `ekf` (old `localization_backend:=ekf`, but
  now also implies no map->odom node runs at all — previously
  `localization_backend:=ekf` could be combined with either
  `map_localizer` value, a combination nobody actually used). Default
  behavior (`localization_mode:=slam`) is unchanged from before this
  refactor. Also gated `slam_toolbox`'s `use_map_saver` param (was
  unconditionally `true` in `config/slam.yaml`) to only actually be
  `true` when `localization_mode:=mapping` — map saving/updating is now
  structurally only possible when deliberately in mapping mode, never
  as a side effect of ordinary `slam`/`amcl`/`ekf` running. Verified all
  4 values launch the expected node set with no errors, live in sim
  (build + smoke-launch each, checked process list + a relevant TF
  lookup for each — `map->odom` for slam/mapping/amcl, `odom->root` for
  ekf — plus `use_map_saver`'s actual runtime value for mapping).
  Renamed `sentry_pkg/test/slam_integration/run_slam_drift_tests.py` to
  `run_localization_drift_tests.py` and added a `--backend
  {slam,amcl,ekf}` flag (default `slam`) so its 4 scenarios
  (baseline/continuous_drift/jerk_with_motion/jerk_stationary) can run
  against any of them, not just slam_toolbox — `jerk_with_motion`/
  `jerk_stationary` are SKIPPED (not asserted) for `--backend ekf`,
  since ekf_node fuses `/odom` directly with no distance-traveled gate
  analogous to slam_toolbox/amcl's, so its jerk response isn't
  characterized yet; asserting either "must not change" or "must change"
  there would just be a guess pending the EKF pipeline's own
  tuning/verification (still open work, see the EKF section above). Not
  yet run end-to-end against amcl/ekf (only the launch-level smoke test
  above) — next session should actually run the suite with `--backend
  amcl` (all 4 scenarios) and `--backend ekf` (baseline/
  continuous_drift only) to see whether the existing slam_toolbox-tuned
  thresholds (e.g. `CORRECTION_FRACTION`, `DRIFT_THRESHOLD`) hold up
  against amcl's different particle-filter noise characteristics, or
  need their own backend-specific constants.
- **Still undecided: what should be responsible for launching the whole
  stack** (sim/SLAM/CV together) — no single package/launch file owns this
  yet. No longer blocks CV work, though: `sim.launch.py spawn_target:=true`
  plus `point_to_cv_target` (run by hand) now exercises the full CV
  detection path standalone, independent of `auto.launch.py`'s SLAM/AMCL/EKF
  stack — see the 2026-07-27 section below.
- **Then build that top-level launch integration**, once the above is
  decided.
- **Rotation lock on the free-floating chassis is soft (inertia-based
  only)** — under a real wall collision during exploration it can tumble to
  extreme angles (observed ~86° roll / 31° pitch / 15° yaw). User explicitly
  chose to accept occasional flips rather than reintroduce a kinematic
  constraint. Revisit only if flips start meaningfully blocking exploration
  in practice, not preemptively.
- From `ARCC_2026_SENTRY_CONTEXT.md`'s "not yet extracted" list: exact
  Battlefield zone coordinates/drawings (Figures 3-1–3-9) aren't pulled into
  `sim`'s world yet if a precise arena map is needed; Referee System
  UART/data-interface spec not yet sourced (needed before real firing-timing
  work starts).
- **RESOLVED (2026-07-25): `ekf` mode now beats raw wheel odometry by 89%**
  — supersedes the 2026-07-24 entry that used to live here (which
  concluded rf2o's missing covariance was why fusion showed no
  improvement). Covariance was a real bug but **not** the cause; the
  actual root cause was a lidar scan-convention mismatch. Full chain of
  findings, in the order they were peeled back:
  - **`ekf_node` was not running at all.** It exited immediately with
    code 127, `error while loading shared libraries:
    libdiagnostic_updater.so`. Same recurring 4.0.6-is-header-only
    footgun documented in step 1 of the EKF section above, back again
    after a container recreation. Now pinned in
    `Dockerfile.thornbots` LAYER 8 as `ros-humble-diagnostic-updater
    (>= 4.0.7)` (`isaac_ros_common` commit `3986f9b`) so it stops
    recurring. Note it silently takes out `ekf` *and* `amcl` while
    `slam` keeps working, which reads like a localization regression
    rather than a packaging problem.
  - **Root cause: `sim`'s gpu_lidar published `angle_min=0.0,
    angle_max=6.28`.** rf2o ignores `angle_min` outright and assumes the
    scan is symmetric about the sensor's forward axis — see
    `CLaserOdometry2D.cpp`, which derives each beam's bearing as
    `fovh = |angle_max - angle_min|; tita = -0.5*fovh + u*fovh/(cols-1)`.
    So beam 0 was assigned `-pi` when its true bearing was `0`, i.e.
    every beam off by exactly pi. rf2o therefore perceived the world
    rotated 180 degrees and published `/scan_odom` displacement with the
    correct *magnitude* in precisely the wrong *direction* (measured:
    179.81 deg mean rotation from ground-truth displacement, over all
    four drive axes). Since `/scan_odom` is the EKF's only absolute
    position source, fusion was far worse than doing nothing. Fixed in
    `sim/urdf/sentry.urdf.xacro` to `-3.14..3.14` (`sim` commit
    `8609d04`), which also matches what real RPLIDAR ROS drivers
    publish — sim and hardware had silently disagreed on the scan
    convention. `sentry_pkg`'s `lidar_self_filter` derives bearings as
    `angle_min + i*angle_increment`, so it was unaffected either way.
  - **`ekf.yaml` fusion assignment was also wrong** (`sentry_localization`
    commit `0289165`). `/odom` was fused as absolute x/y, but wheel
    odometry's dominant error here is *slip* — an error in integrated
    distance that accumulates monotonically — so its absolute position
    baked slip permanently into the filter and no covariance tuning let
    `/scan_odom` pull it back. Measured: driving ~42m straight with
    `odom_slip_ratio=0.05`, ekf tracked `/odom` to within 0.001m while
    both sat 2.02m (= 5% of 42m) behind ground truth. Now `/odom`
    supplies **velocity + yaw** and `/scan_odom` supplies **absolute
    x/y**. Yaw is pinned from `/odom` deliberately: its orientation is
    always identity, but that is the *true* heading (holonomic chassis,
    never rotates), and `robot_localization` rotates odom0's body-frame
    velocity into the world using the filter's yaw — a wrong yaw
    integrates velocity backwards. rf2o's yaw is no longer fused at all.
  - **Result**, vs `/sim/raw_odom` with `odom_slip_ratio=0.05` driving
    the cornering loop: raw `/odom` mean error 0.171m, ekf-fused 0.019m
    (**+89%**). Before the fixes: 2.97m.
  - Drift suite with `--backend ekf`: `baseline` and `noise_correction`
    PASS, `jerk_with_motion` SKIPs by design, `drift_correction`/
    `drift_correction_obstacle` FAIL — still the known-bogus metric (see
    the open item below), not a regression.

## Open after the 2026-07-25 EKF work

- **rf2o's covariance fix is still container-local.** rf2o publishes
  all-zero covariance upstream, which reads as "infinitely certain" to
  the EKF. Patched in-container (x/y variance `0.02**2`, yaw `0.05**2`,
  unobserved axes `1e6`) via `~/workspaces/isaac_ros-dev/rf2o_cov_patch.py`,
  which must be re-run **and rf2o rebuilt** after every container
  recreation — already lost once this way. Needs a real commit to
  `Thornbots/rf2o_laser_odometry` to stop recurring. Worth knowing: on
  its own this fix changed measured accuracy by essentially nothing; the
  scan convention was doing all the damage.
- **`/workspaces/ros2_ws` overrides the bind-mounted `src/` in
  `AMENT_PREFIX_PATH`.** Editing `src/sentry_localization/config/*.yaml`
  has NO effect on a running stack — the image-baked GitHub clone from
  LAYER 8 is what actually loads. This silently invalidated a full round
  of measurements before it was spotted (the ekf output kept matching
  `/odom` to 3 decimals, which was the tell). Check with
  `ros2 pkg prefix sentry_localization`; to test a config change, copy it
  into `/workspaces/ros2_ws/src/...` as root. Worth deciding whether the
  isaac_ros-dev overlay should take precedence instead.
- **`drift_correction`/`drift_correction_obstacle` still need an
  ekf-appropriate metric.** Their `MAX_DELTA_THRESHOLD=0.30m` ("delta
  from pre-loop pose") is calibrated for `map->odom`'s
  residual-correction semantics; for `odom->root` that delta is mostly
  the robot's own real motion around the ~2m loop (measured 1.82m), so
  both reliably FAIL without indicating a problem.
  `sim/test/localization/ekf_ground_truth_diag.py` is the right metric
  (scores against `/sim/raw_odom` with slip actually enabled) and should
  probably become these scenarios' assertion for `--backend ekf`.
- **rf2o degrades at the speed the drift suite drives.** Speed sweep:
  tracks to within ~1% up to 2.0 m/s, but reports 12% short at 4.0 m/s
  (`ratio 0.879`), which is what the suite's legs use. rf2o is a
  range-flow method that linearizes on small inter-scan motion, so this
  is a suitability ceiling rather than a bug. Options if it matters:
  raise the sim lidar's 10Hz update rate, cap speed, or swap the scan
  matcher. It also drifts ~2cm over 20s while completely stationary.
- **Sim's slip model corrupts position but NOT velocity**
  (`pose_emulator.py` applies `odom_slip_ratio` to `_slipped_x/y` only;
  `vel_x`/`vel_y` pass through as true twist). The new velocity-only
  wheel fusion therefore looks better in sim than it will on real
  hardware, where encoder *velocity* is wrong during a slip too. Worth
  making the slip model corrupt velocity before trusting the +89% number
  as a hardware prediction.
- **Beware magnitude-only validation.** An early speed sweep compared
  `|displacement|` and scored rf2o as healthy at ~1% error while it was
  pointing exactly backwards. Comparing displacement *vectors* (the angle
  between them) is what found it — worth doing for any odometry source.

## 2026-07-26 — decoupled EKF from `localization_mode`

`localization_mode:=ekf` no longer exists as a value. It was a 4-way
choice conflating two decisions: who owns `map->odom` (slam_toolbox/amcl)
and who owns `odom->root` (raw `/odom` passthrough, or EKF fusion of
`/odom` + `/scan_odom`). Split into two independent launch args:
- `localization_mode`: `slam` (default) / `mapping` / `amcl` / `none` —
  map->odom owner (or nobody, for `none`).
- `use_ekf` (new bool, default `false`) — whether `odom->root` is
  EKF-fused instead of passed through raw.

The old map-free EKF-only configuration (the one that produced the
89%-over-wheel-odometry result above, and what
`run_localization_drift_tests.py --backend ekf` exercises) is unchanged in
behavior, just reached as `localization_mode:=none use_ekf:=true` now
instead of `localization_mode:=ekf`.

New, previously unlaunchable combination: `slam`/`amcl` + `use_ekf:=true`
— a map backend with EKF-fused odometry underneath it. Not exercised by
any automated test yet (flagged as a coverage gap in
`sim/README.md`/this refactor's plan, not a bug). Worth noting for future
testing: `mcb_relay`'s `relocalize` path compares `/localization/odom`
against `/odom`; today `slam`/`amcl`/`mapping` all pass `/odom` through
unchanged, so that drift check is structurally near-zero and the
relocalize path is dormant in map-backend runs. Once `slam`/`amcl` +
`use_ekf:=true` is actually run, `/localization/odom` diverges from
`/odom` for the first time in a map-backend config, making that
relocalize path live rather than dormant — no code change needed, just
something to watch for if testing that combination on real hardware.

## 2026-07-27 — CV target simulation (ground truth + noise, no gz entity)

Per user reprioritization (see `## Overall goal`'s flipped priority line),
built the pieces to exercise `sentry_pkg/point_to_cv_target.py` (unmodified)
end-to-end in sim: a fast-moving target's ground truth → simulated noisy
detection → `/cv/target`.

**Built:**
- `sim/sim/target_driver.py` — publishes `nav_msgs/Odometry` on
  `/target/ground_truth_odom` directly; no gz entity/model/plugin at all,
  same "plain ROS node doing its own kinematics" approach `pose_emulator.py`
  uses for robot pose. Bounces along a fixed-distance lateral traverse
  (default: x=3.0m, y∈[-2,2], z=0.3m) sized against the camera's static
  1.5184 rad FOV so dwell time stays well above the ~10-sample EMA warm-up
  floor even at high sweep speeds (measured: min 47 consecutive in-frustum
  samples at 8 m/s, the top of the default sweep). Advances state from
  `self.get_clock().now()` deltas, not timer period, so RTF≠1.0 doesn't
  mislabel `target_speed`.
- `sim/sim/cv_target_emulator.py` — FK chain (root→body→head→head_pitch→
  camera, matching sentry.urdf.xacro's fixed joint offsets, no TF) computes
  the target's REP-103 position relative to the camera, gates on FOV/range,
  injects configurable Gaussian noise + dropout + latency, publishes
  `roi_point`/`roi` — exactly what `point_to_cv_target.py` subscribes to.
  Stamps `roi_point` from its own clock, never forwarded from ground truth.
- `sim/setup.py`, `sim/launch/sim.launch.py` — new `spawn_target` (default
  `false`)/`target_speed`/`cv_noise_*` args and `Node` actions, independent
  of `auto.launch.py`'s SLAM/AMCL/EKF stack in both directions (confirmed:
  `spawn_target:=true` runs standalone against bare `sim.launch.py`).
- `sim/test/cv/run_cv_detection_tests.py` — speed-sweep test script
  (`LaunchTree` pattern borrowed from `run_localization_drift_tests.py`),
  reports tracking error vs. speed, and hard-fails if any speed's
  consecutive-in-frustum dwell count drops below `--min-dwell` (default 10)
  — the guard the plan called out as required, not optional. Default sweep
  (1/2/4/6/8 m/s) passes; `vel_err` mean grows from 0.71 m/s at 1 m/s to
  1.34 m/s at 8 m/s, the expected EMA-lag-vs-speed tracking-degradation
  trend.

**Verified:** `/target/ground_truth_odom` publishes and moves;
`/cv/target` reports sane nonzero velocity/acceleration while in-frame and
a zero-confidence watchdog message once the target leaves the frustum;
vector/bearing check (comparing `/cv/target`'s direction against true
bearing from `/target/ground_truth_odom`, not magnitude-only — see the
rf2o note above for why that check matters) passed 20/20 samples with no
180°-class sign flip.

**Environment footguns hit and fixed, both real (not the already-documented
`AMENT_PREFIX_PATH` one below — a different failure mode each):**
- `sim`'s `gz-sim`/`ros_gz` deps aren't installed by default in this
  container (`DOCKER.md`'s "Which image gets built" section already
  documents this — `sudo isaac_ros_common/docker/scripts/install-sim.sh`
  fixes it once per container).
- `sentry_pkg`'s build under `/workspaces/isaac_ros-dev/install` was a
  **stale colcon symlink-install pointing at a deleted git worktree**
  (`.../sentry_pkg/.claude/worktrees/cv-target-publisher/...`, left over
  from an earlier session) — broken symlinks, so both `ros2 run
  sentry_pkg point_to_cv_target` and a plain Python import of
  `sentry_pkg.point_to_cv_target` failed outright. Fixed by `rm -rf
  build/sentry_pkg install/sentry_pkg && colcon build --packages-select
  sentry_pkg --symlink-install`, which relinks against the real
  bind-mounted `src/sentry_pkg`. After that rebuild, `ros2 pkg prefix
  sentry_pkg` and `ros2 run sentry_pkg point_to_cv_target` both correctly
  resolve to `/workspaces/isaac_ros-dev/install/sentry_pkg` via
  `dexec.sh` (re-verified 2026-07-27, after the section below's rviz
  addition) — the stale-symlink issue above was the whole story, not a
  deeper `AMENT_PREFIX_PATH`-resolution-order problem; no absolute-path
  workaround needed once the reinstall is clean.

**rviz visualization added (2026-07-27, later in the same day):**
`cv_target_emulator.py` now also publishes a `MarkerArray` on
`target_markers` (world frame: green sphere = ground truth, yellow sphere
= noisy detection, yellow absent when out of frustum/dropped), and a new
`sim/rviz/cv_target.rviz` config (Fixed Frame `odom`, since this is CV-only
testing with no SLAM map running) adds that display plus `/sim/raw_odom`
and `/target/ground_truth_odom` arrows. Launch with
`ros2 launch sim sim.launch.py spawn_target:=true rviz_config:=$(ros2 pkg
prefix sim)/share/sim/rviz/cv_target.rviz`. Verified live: `target_markers`
publishes at ~58Hz, the yellow detection sphere visibly tracks the green
ground-truth trail in rviz, and Gazebo's entity tree correctly shows no
target entity (confirms the "no gz entity" design held).

**Open:** no aim/lead controller or fire logic yet (explicitly deferred,
see the plan this section implements).
