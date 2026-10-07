# Plan: end-to-end tests in sim, and faster benches

ROADMAP.md tracks A and D, 2026-09-26. The goal is one test, the match
test, that runs the robot's code as `auto.launch.py` runs it on the field.
Sim plays only what sits outside the Jetson:

- the MCB, on the far side of a real UART link (a pty), speaking
  `ros2_dji_serial_bridge/UART_PROTOCOL.md`;
- YOLO, as a detector stand-in that publishes `/detections_output` from gz
  truth;
- the sensors: gz lidar for `/scan` and gz depth for
  `/depth/image_rect_raw`.

Everything between those is the real code: `dji_serial_bridge`,
`mcb_relay`, `pose_translator`, localization (amcl + EKF + rf2o),
`roi_depth_node`, `target_selector`, `target_tracker` and
`point_to_cv_target`. Our robot drives and shoots in the same run, against
other `sentry_v2` copies that move, spin and shoot back. One run then
scores localization, tracking and hitting together, and a wrong stamp,
frame or unit between any two stages shows up as a lost hit.

Nothing runs YOLO. The stand-in's boxes are perfect up to the noise we add.

We are compute-limited, so suites run one at a time, never in parallel. The
speed work below makes each run cheaper and makes one run cover more.

## Speed

Today: the drift suite takes ~285 s for 9 scenarios, the estimation bench about 30 s for 12
cells on `bench_world` (Mac), and the aiming bench runs 40 cells. The full gz stack caps at RTF
~1.55 for a reason nobody has found (`sim/AGENTS.md` Open), and
the estimation bench scores at ~20x with the C++ `target_tracker`.

1. Measure first. Each suite logs its wall time split into bring-up,
   per-case reset and scored time, plus the mean RTF. Numbers go in the
   commit message, as usual.
2. Find the RTF cap by bisecting the stack's nodes and bridges. Every gz
   suite, the match test included, gains from it.
3. Render only what gets scored. Until a suite consumes camera images, the
   camera stays off everywhere (`camera:=false`, the default), the match
   test included: its stand-in reads truth and stands in for
   `roi_depth_node` too (the user, 2026-10-05).
   Only our robot carries a camera and a lidar; the other sentries carry
   neither. A subscribed 60 Hz
   RGB-D camera alone caps a bare server near RTF 2.2. Depth alone at 60 Hz
   takes the Mac's bare `sim.launch.py` from RTF 2.66 to 1.1 (llvmpipe,
   2026-09-29); settle its rate once E1 runs.
4. Keep the other sentries cheap in physics. Box collisions cost about
   2 us per shape per step, so each copy gets one hull for the body and one
   box per panel, not the full collision set.
5. One gz session per suite, reset by teleport, as the drift suite already
   does. Restart the robot stack only when a case needs a clean one.
6. Cover more per run. The match test scores driving, localization and
   hitting in one session, each segment on its own, so it replaces a set
   of single-purpose cases in the regular run. The benches stay for
   diagnosis: run them when a match segment drops or when their half of the
   code changes.
7. `target_tracker` is C++ (2026-09-28): the estimation bench scores at
   ~20x, up from ~14x, and the tracker is no longer the ceiling.

Done when each suite's time split is logged, the RTF cap has a named cause,
and the regular run (unit tests, then the match test) fits 10 minutes, and
5 without the match test (the user, 2026-09-28).

## Before the match test

- Armor panels are on both URDFs (2026-09-27): `armor_0` to `armor_3` on
  the diagonals at 45 deg + k x 90 deg, 0.252 m out, at 0.230 and 0.136 m,
  each a 135 x 125 mm Small module (`sim/README.md`). Both benches' target
  uses them, with `FLOORS` and `LIMITS` rerun on it.

## The match test

### What sim provides

| Piece | Today | Build |
|---|---|---|
| Opponents | E1/E2 use one red ghost on field-safe diagnostic paths. E3 approaches center from red spawn. E4 has two red ghosts on separate routes, with truth-fed noisy aim and 2 Hz fire | Tune ghost aim realism and repeated-run spread |
| An ally | E4 has one blue ghost, routed from blue spawn and firing at red panels. The selector drops its blue detections; first-impact scoring detects unintended intersections | Zero firmware shots intersecting the ally; intermittent failures remain |
| Detector stand-in | `detector_standin` (`sim/src/detector_standin.cpp`) publishes `/cv/panel_detections` for E1 with no camera, in `roi_depth_node`'s place (the user, 2026-10-05) | Every 60 Hz sim tick: each panel on every other robot that faces the camera (the 145 deg exposure cone) and lands in the D435's image, its true centre and corners in `camera`, class by team (blue 0-3, red 4-7). Ray noise is a parameter, off by default. Occlusion by the field and other robots: not done (the depth check went with the camera) |
| MCB emulator | E1 bypasses the wire. E2 and `mcb.launch.py` run the checked-out MCBV3 C++ hosted executable on a pty; fake IMU, pods, encoders, CAN and remote/referee interfaces supply hardware. The Python control port is removed | Physical motor dynamics and STM32 timing remain to model (ROADMAP track I). POSE/REF_SYS scheduling, CV_TARGET aiming/firing, RELOCALIZE and drive behaviour come directly from the firmware code; rebuild after firmware edits |
| Driving | E3/E4 use `match_driver` scripted `/cmd_vel` at 2 m/s²; native firmware owns aim/fire. Provisional team spawn routes end in center maneuvers, with AMCL/rf2o/EKF active | Navigation publisher and native drive handoff remain later work |
| Referee emulator | E4 tracks 400 HP per robot, 20 HP per hit. HP, team, stage, time and hurt panel enter the physical referee parser; HP and team are checked on returning UART `REF_SYS` | Verify `delta_angle_got_hit_in`; heat, ammo and respawn are not modeled |
| Shots | E4 advances ballistic 25 m/s shots from truth muzzles. The first field, chassis hull or canted panel impact absorbs the shot. Damage needs >12 m/s relative normal speed, the exposure cone and 50 ms per-panel dead time | Non-chassis appendage blockers and detector occlusion remain unmodeled |

Driving comes from sim for now. `NAV_GOAL` goals have no publisher in this
workspace, and navigation comes after the Midwest competition. Once a
planner exists, a later stage hands the route to it over `NAV_GOAL`.

Opponents run a truth-fed aimer, not a copy of our stack, because two full
stacks don't fit the compute budget. A red-against-blue run with two real
stacks is out of scope.

### Stages

Each stage adds hops and is its own commit and bump. Scoring stays the same
from stage to stage, so a drop belongs to the hops that stage added.

1. E1, the stand-in to the gimbal, our robot parked. Panels on the URDF, one
   opponent running the aiming bench's cells, the stand-in and a team
   stub in place of the referee. The real selector, tracker and
   `point_to_cv_target` feed `cv_head_aim`.
2. E2, the wire. `dji_serial_bridge` and `mcb_relay` on a pty against the
   MCB emulator, which replaces `pose_emulator`, `cv_head_aim` and the team
   stub. Tests the `CV_TARGET` packing, the stamps both ways, the fire path,
   and `REF_SYS` into the selector. `stage:=e2` runs it (2026-10-01);
   it scores through the compiled MCB firmware on field-safe paths. The
   stationary lateral cell passes; moving tracking accuracy remains open.
3. E3, driving while shooting. Our robot drives the scripted route: straight
   at 1 and 2 m/s, a 90 deg turn while driving, and spinning in place.
   Localization from gz lidar is in the loop, so its error at fire time
   lands in the score. The aim is an `odom` point; `RobotPose.chassis_yaw`
   comes from the hosted firmware. Robots start at their provisional team
   spawns and travel around the south walls to center.
4. E4, the match, 2v2: two opponents and one ally (the user, 2026-09-28),
   with opponents shooting back and the referee emulator counting HP. One fixed-seed scenario of set
   length, split into scored segments.
The world-frame aim that follows E3 is ROADMAP.md track B
(`CV_SPLIT_PLAN.md` W.1-W.5). Its done bar: each moving segment comes within
10 points of the same target cell with our robot parked.

E3 and E4 now run on nightly. E4 includes ballistic first impacts against
the field, chassis hulls and armor, per-panel damage dead time, HP and
referee UART feedback. `sim/README.md` documents commands and model limits.
E3 diagnostic completion passes; moving combat accuracy does not. E4's
strict zero-friendly-intersection assertion exposes intermittent failures.
Repeated-run floors and standalone-versus-sequence equivalence remain open.

### Scoring

One `sim/launch/e2e.launch.py` and a pytest suite in `sim/test/e2e/`. Per
segment:

- hit rate on enemy panels, the pass condition, with floors from three runs
  minus 10 points, like the aiming bench's `FLOORS`;
- shots at the ally, which must be zero;
- for E3 on: route error and localization error (EKF against gz truth) at
  each fire time;
- damage taken, logged only, with no pass condition until opponents' aim is
  tuned to something realistic.

Diagnostics logged beside each segment: ROI depth error against truth,
`TargetState` error (`estimation_metrics`), and each hop's stamp against
the image stamp. Each miss is split into our pose error, `TargetState`
error and aim error, so a drop names localization, Part 2 or Part 1
without a second run.

### Done when

E4 runs in one gz session, every segment scores the same alone and in
sequence, and each segment's hit rate is within 10 points of its floor or
has a diagnostic that names the hop that lost it.
