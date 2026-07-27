# ARCC 2026 rules — Sentry-relevant context

Distilled from the ARCC 2026 rulebook (76 pages, RoboMaster-style 3v3 combat
competition), fetched from:
https://e0398dbe-f5cb-43f1-8df9-3f2f243ba559.filesusr.com/ugd/df0c37_304dcbb3e08c422b987a1b627110d767.pdf

This is a starting-context doc for `sentry_pkg` / `sim` work — pulls out only
what's relevant to building an autonomous Sentry, not the full rulebook (pit
crew procedures, other robot types, appeals process, etc. are omitted). Read
the source PDF directly if you need something not covered here.

Current dev priority: **CV (target detection/tracking) first, timing-based
firing second** — localization is considered good enough for now (see
`SESSION_NOTES.md` for the full goals/status/open-issues log this section
summarizes).

## Dev status (as of 2026-07-27; individual bullets keep their own dates
where those still matter — see `SESSION_NOTES.md` for the full log)

**Working:**
- Full sim pipeline end-to-end: `ros2 launch sim sim.launch.py` spawns the
  robot in the `ARCC_Field_2026` gz-sim world, bridges raw `/scan`,
  `/sim/raw_odom`, `/sim/raw_joint_states`, `/cmd_vel`, `/clock`, head-pan
  control.
- rviz visualization confirmed working end-to-end: laser scan renders, and
  the SLAM map loads correctly when starting `sentry_pkg`.
- **`sentry_pkg` owns pose and TF end-to-end now (2026-07-20)**: sim's
  `pose_emulator` repackages its raw ground truth into the same
  `dji_serial_bridge/msg/RobotPose` `/pose` interface real hardware's
  Type-C board speaks; `sentry_pkg`'s `pose_translator` is the single
  consumer of that, for sim or real hardware alike, and `sentry_pkg` runs
  its own `robot_state_publisher` off its own URDF. `sentry_pkg`'s SLAM
  (`auto.launch.py`) runs off `/pose` + `/scan` only — no direct
  real-hardware dependency, works against sim or a real driver
  interchangeably. (The real `dji_serial_bridge_node` itself still needs a
  one-line update to publish flat `/pose` instead of `~/pose` to match —
  tracked as a TODO in its source, not yet done.) `auto.launch.py` launches
  the real drivers (`dji_serial_bridge_node` + `sllidar_ros2`, RPLIDAR
  A2M8 on `/dev/ttyUSB0` @ 115200 by default) directly now, on by default
  (`real_hardware:=true`); pass `real_hardware:=false` when running
  against sim instead.
- Autonomous frontier-biased exploration (`sim/auto_explore.py`) with
  stuck-detection/escape logic and immediate reaction to a physical contact
  sensor (`/body_contact`), not just map-inferred walls.
- Free-floating 6DOF chassis (no joint chain) driven by `/cmd_vel`, matching
  the real holonomic, non-rotating-heading drivetrain design (see "Our
  Sentry's drivetrain" below).
- Docker dev environment is stable: NVIDIA GPU rendering (was silently
  falling back to the Intel iGPU), FastDDS local discovery (was broken by a
  stale robot-IP peer in the profile baked into every shell), and
  container-local device permissions all fixed. Full writeup in
  `DOCKER.md`'s Troubleshooting section and the `isaac-ros-docker` skill.

**Next up:**
- **Publish `slam_toolbox`'s corrections back onto a real odometry topic**,
  not just `map->odom` TF. Right now a correction only exists as that
  transform — anything wanting the robot's best current pose has to do its
  own `map->root` TF lookup rather than just subscribing to a topic. Not
  started; worth doing once the EKF/correction pipeline below is settled,
  since it's a natural place to also publish a single best-estimate
  `Odometry` message downstream consumers (e.g. Nav2, once set up) can use
  directly instead of each doing their own TF lookup.
- **Fuse `/odom` + `/scan` into localization via an EKF**, replacing
  `pose_translator`'s current plain republish of `/pose` onto `odom->root`.
  Plan (full detail/rationale in `SESSION_NOTES.md`):
  1. **Done (2026-07-20)**: `ekf_node` runs — was a stale apt index +
     old `diagnostic_updater` 4.0.6 build missing its `.so`, not a real ABI
     mismatch; fixed with `apt-get update` + `robot_localization` install +
     `diagnostic_updater` upgrade to 4.0.7. Container-local fix, not yet
     baked into the image.
  2. **Done (2026-07-20)**: vendored `rf2o_laser_odometry` (upstream
     `MAPIRlab/rf2o_laser_odometry`, `ros2` branch) as a new Dockerfile
     layer, wired into `auto.launch.py` publishing `/scan_odom`
     (`publish_tf: false`, EKF will own `odom->root`).
  3. **Done (2026-07-20)**: since the lidar is head-mounted and the head
     moves independently under firmware control, `rf2o` turned out to
     sample the `lidar->root` TF only *once* at startup, not per scan — so
     the originally-planned "drop scans if `head->lidar` TF isn't fresh"
     gate wasn't actually possible without patching `rf2o` itself. Instead
     added `sentry_pkg/sentry_pkg/head_home_scan_gate.py`, which only
     forwards `/scan` onto `/scan_gated` (rf2o's input) while the head is
     near its home yaw (`home_yaw_tolerance` launch arg, default 0.05 rad).
     Verified live: `/scan_gated` correctly stops/resumes as the head
     leaves/returns to home. A real per-scan-TF fix would require forking
     `rf2o`; deferred (see `SESSION_NOTES.md` option (c)).
  4. **Done (2026-07-25)**: `sentry_pkg/config/ekf.yaml` + `ekf_node` fuse
     `/odom` (velocity+yaw) and gated `/scan_odom` (absolute x/y) into
     `odom->root` — measured +89% over raw wheel odometry under slip; full
     writeup and remaining caveats in `SESSION_NOTES.md`'s 2026-07-25 and
     "Open after the 2026-07-25 EKF work" sections.
- **CV target detection now has a working sim path** (2026-07-27, see
  `SESSION_NOTES.md`): `sim`'s `target_driver.py` + `cv_target_emulator.py`
  feed `sentry_pkg/point_to_cv_target.py` (unmodified) end-to-end,
  launchable standalone via `spawn_target:=true`.
- **Decided (2026-07-27): `sentry_pkg` owns launching the whole stack**
  (sim/SLAM/CV together) — matches its existing role owning pose/TF and
  `auto.launch.py`'s `real_hardware`/`localization_mode` args, which
  already toggle between sim and real drivers from one place. Not yet
  built — `auto.launch.py` needs a new arg to also bring up `sim`'s
  `spawn_target`/CV nodes (and, for real hardware, whatever the real
  `realsense-yolov8-nitros-bridge` chain needs) alongside SLAM.
- **Set up Nav2** on top of `slam_toolbox`'s localization/map output, once
  it's reliably corrected (see EKF work above) — path planning/costmaps for
  autonomous navigation around the arena. Not started. Since the chassis is
  holonomic and never rotates (see "Our Sentry's drivetrain" below), the
  planner can treat orientation as constant and optimize purely over (x, y)
  — costmaps/footprints should still account for the fixed heading's
  asymmetric footprint, since it never rotates to present a different
  profile toward obstacles.

## Sentry robot spec (§3.1.3)

- **Must operate fully autonomous during the match — no pilot, no teleop.**
  A debug remote controller is allowed only before the match; it must be
  physically removed from the Battlefield entrance once the match starts and
  cannot be used after the Five-Second Countdown (R23).
- **No inter-robot communication** — unlike Hero/Infantry, the Sentry cannot
  talk to teammates. All perception/decision-making must be self-contained.
- Launcher: 17mm only, muzzle speed capped at 25 m/s.
- Initial/Max HP: 400 (highest of the three robot types).
- Chassis power limit: 100W.
- Max barrel heat: 260, cooling rate: 30/s (best cooling of the three robot
  types).
- Projectile allowance: 750, preloaded during the 3-minute Setup Period,
  **fixed for the whole match** — Sentry cannot buy more via the Economy
  System mid-match the way Hero/Infantry can (that requires occupying the
  Resupply Zone with a live Pilot exchange, which a fully autonomous Sentry
  doesn't do here).
- Can occupy the Capture Point and the Resupply Zone (25% max-HP/sec
  recovery while inside).

## Our Sentry's drivetrain (not from the rulebook — our hardware choice)

- **Holonomic chassis** (e.g. mecanum/omni wheels) — can translate in any
  direction without changing heading.
- **Does not turn/rotate its chassis heading during matches.** Heading stays
  fixed; all repositioning is pure translation. This is a deliberate design
  choice (likely so the gimbal/turret handles aim independently of chassis
  facing, and to keep armor-panel orientation predictable/consistent toward
  expected threat directions).
- **Implication for SLAM/nav**: no need to plan or reason about heading
  changes — the planner can treat orientation as constant and optimize
  purely over (x, y) translation. Costmaps/footprints should still account
  for the fixed heading's asymmetric footprint (if any) since it never
  rotates to present a different profile.
- **Implication for firing-timing (later)**: since chassis heading is fixed,
  gimbal/turret aim is fully decoupled from chassis motion — no need to
  coordinate "stop translating before firing" the way a differential-drive
  robot might need to stop turning to stabilize aim.

## Battlefield geometry (§3.2) — relevant to SLAM/nav

- Battlefield: **12m × 8m**, mirrored layout about the centerline (Red/Blue
  symmetric).
- Each team has a **Starting Zone == Resupply Zone**, inlaid with RFID
  Interaction Module Cards (used for HP recovery and Capture Point
  detection — robots must physically sense the RFID card, not just be in
  the right XY region).
- One shared **Capture Point** at the center, also RFID-carded. **RFID
  dead zones exist** — the rulebook explicitly says teams must handle this
  (don't assume 100% detection reliability inside the zone; a robot that
  loses RFID contact loses occupation after 2 seconds).
- **Bumpy Road**: PVC flooring with evenly spaced bumps around the Capture
  Point — expect wheel odometry noise/slip here; may want extra localization
  weight from other sensors when crossing it.
- **High Ground** exists as a terrain feature (elevation change).
- Environment is explicitly **not fully symmetrical in practice** — non-uniform
  magnetic fields, wind, venue lighting are called out as real conditions
  (relevant if using a magnetometer or vision-based localization that assumes
  uniform lighting).
- An extra flooring layer sits over the RFID zones (minor height change to
  model if doing precise wheel/lidar odometry calibration).

## Combat mechanics — relevant to firing-timing phase (later)

- **Barrel heat**: each 17mm shot fired adds +10 heat; cools at rate/10 per
  100ms tick (30/s cooling rate → -3 per 100ms). Exceeding the limit (260)
  locks the launcher until heat drains to 0; exceeding limit+100 (360) locks
  the launcher for the rest of the round. **Firing-rate logic needs a heat
  budget model**, not just "fire when target acquired."
- **Projectile speed limit** (25 m/s): overspeed locks the launcher 15–20s
  depending on margin, or for the rest of the round if >10 m/s over. Muzzle
  velocity calibration/control matters as much as aim.
- **Damage**: 17mm hit = 20 HP to target's armor module (detection requires
  >12 m/s normal-component impact speed on the armor panel).
- **Projectile budget is fixed at 750 for the whole match** with no
  resupply path for a fully autonomous Sentry — firing logic should treat
  ammo as a scarce resource to ration across the 5-minute Battle, not spend
  freely early.
- **Respawn**: on defeat, barrel heat resets to 0, robot respawns with 20%
  HP, 30s invincibility, and a "Weakened" state (launcher locked, can't
  capture points) until it reoccupies its Resupply Zone.
- **Referee System disconnection**: if the Sentry's main control module goes
  offline, launcher/gimbal/chassis power off and HP drains 5%/sec — so the
  autonomy stack's reliability directly costs HP, independent of combat.

## Not yet extracted / worth pulling in later

- Exact Battlefield zone coordinates/drawings (Figures 3-1–3-9 are diagrams,
  not extracted as text — need the actual PDF pages if building a precise
  arena map for `sim`).
- Full Referee System data interface / UART protocol spec (likely in the
  companion "Robot Building Specification" doc referenced throughout, not in
  this rulebook).
- Round timing/countdown details (§7.5–7.9) if precise match-phase state
  machine timing is needed later.

Full extracted plaintext of the rulebook (`pdftotext -layout`) was produced
2026-07-19 but only saved to a session-scratchpad path that does not persist
across sessions — re-fetch the PDF and re-run `pdftotext -layout` if deeper
detail is needed later.
