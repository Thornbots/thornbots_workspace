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
| Opponents | One `sentry_v2` copy, `opponent_0` (`opponent_driver`, E1), moved along `target_driver`'s path by `OpponentMover`; no aiming or shooting back. `actor_driver` still spawns plain boxes | Spawn N `sentry_v2` copies, each with a team. One `opponent_driver` node moves them all along `target_driver`'s path profiles with chassis spin, aims each head at our panels from truth with added noise, and fires at a set rate |
| An ally | None | One copy on our team, so the selector has to drop its panels and we must never fire at it |
| Detector stand-in | `detector_standin` (`sim/src/detector_standin.cpp`) publishes `/cv/panel_detections` for E1 with no camera, in `roi_depth_node`'s place (the user, 2026-10-05) | Every 60 Hz sim tick: each panel on every other robot that faces the camera (the 145 deg exposure cone) and lands in the D435's image, its true centre and corners in `camera`, class by team (blue 0-3, red 4-7). Ray noise is a parameter, off by default. Occlusion by the field and other robots: not done (the depth check went with the camera) |
| MCB emulator | E1: `pose_emulator` publishes `/dji_serial_bridge/pose` and `cv_head_aim` reads `/cv/target`, both skipping the wire. E2 (`stage:=e2`): `sim/mcb_emulator/`, a port of MCBV3 `position-based-cv`, on a pty | ROADMAP.md track I: a node on the other end of a pty from `dji_serial_bridge`, copied from the real firmware (`Thornbots/MCBV3`), where it and this row differ the firmware wins. Sends `POSE` at 100 Hz from gz wheel odometry with `pose_emulator`'s noise model, and `REF_SYS` at 5 Hz from the referee emulator. Decodes `CV_TARGET`, drives the gz head to the `odom` point from its own odometry, and fires on `fire` after `delay_ms`. Applies `RELOCALIZE` to its odometry origin. Replaces `pose_emulator` and `cv_head_aim` in this test |
| Driving | The drift harness ramps `/cmd_vel` at 20 m/s^2 (`real_accel`: 1.2) | The test drives our chassis through the MCB emulator from a scripted route, ramped at 2 m/s^2 (`drive(accel=)` in `drift_harness.py`; the user, 2026-09-28). The MCB holds yaw within 2 deg over a match |
| Referee emulator | No `RefSysStatus` in sim | Tracks every robot's HP. A scored hit costs 20 HP, and on our robot sets `delta_angle_got_hit_in`. Also sets team, game stage and time left. Feeds the MCB emulator's `REF_SYS` |
| Shots | Only the Python harnesses fly shots | Every shot, ours or an opponent's, flies a straight line at 25 m/s from the gz muzzle at fire time. The first thing it crosses wins: a panel's canted square, a robot hull, or nothing. A panel hit counts only above 12 m/s normal speed and 50 ms after that panel's last hit, per the rules. The aiming bench already scores the canted square (`off_face` in `shot_hit_harness.py`) |

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
   it hits nothing yet: the MCB's odometry and our `odom` differ by a turn (ROADMAP track I).
3. E3, driving while shooting. Our robot drives the scripted route: straight
   at 1 and 2 m/s, a 90 deg turn while driving, and spinning in place.
   Localization from gz lidar is in the loop, so its error at fire time
   lands in the score. The aim is an `odom` point; `RobotPose.chassis_yaw`
   reads 0 until the firmware sends it, which the turn and the spin measure.
4. E4, the match, 2v2: two opponents and one ally (the user, 2026-09-28),
   with opponents shooting back and the referee emulator counting HP. One fixed-seed scenario of set
   length, split into scored segments.
The world-frame aim that follows E3 is ROADMAP.md track B
(`CV_SPLIT_PLAN.md` W.1-W.5). Its done bar: each moving segment comes within
10 points of the same target cell with our robot parked.

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
