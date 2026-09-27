# Plan: end-to-end tests in sim, and faster benches

2026-09-26. The goal is one test, the match test, that runs the robot's
code as `auto.launch.py` runs it on the field. Sim plays only what sits
outside the Jetson:

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

Today: the drift suite takes 227 s for 7 scenarios, C2 about 54 s for 10
cells on `bench_world`, and C1 runs 40 cells. The full gz stack caps at RTF
~1.55 for a reason nobody has found (`sim/AGENTS.md` Open), and
`target_tracker` caps C2 near 8x.

1. Measure first. Each suite logs its wall time split into bring-up,
   per-case reset and scored time, plus the mean RTF. Numbers go in the
   commit message, as usual.
2. Find the RTF cap by bisecting the stack's nodes and bridges. Every gz
   suite, the match test included, gains from it.
3. Render only what gets scored. The stand-in reads truth, so the camera
   becomes a depth-only sensor with no colour image. Only our robot carries
   a camera and a lidar; the other sentries carry neither. A subscribed 60 Hz
   RGB-D camera alone caps a bare server near RTF 2.2, so check what depth
   alone costs before settling its rate.
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
7. A C++ core for `target_tracker` lifts C2's ceiling and the match test's.
   Still the user's call (`CV_SPLIT_PLAN.md`).

Done when each suite's time split is logged, the RTF cap has a named cause,
and the regular run (unit tests, then the match test) fits the time budget
the user sets once the numbers are in.

## Before the match test: C2's moving-cell error

C2's moving cells are poor and swing 2x between runs (`CV_SPLIT_PLAN.md`
"Where this stands"). The match test would inherit that error, so trace it
first.

## Panels on the URDF

The stand-in needs each armor panel as a frame it can look up, and depth
needs something solid to see. Today the panel layout lives only as
constants in `cv_target_emulator` and `bench_world.cpp`.

- `sentry_v2.yaml` gains an `armor` section and `simplify_urdf.py` emits
  four links, `armor_front`, `armor_left`, `armor_back` and `armor_right`,
  fixed to the chassis. Each link's origin sits at the panel face centre
  with +x along the outward normal, canted 15 deg (S122), so a panel's
  corners are its centre plus or minus half the size along y and z.
- Positions and heights come from the CAD if the export has the armor
  modules, otherwise from the rules (S122 cant, pairs up to 100 mm apart in
  height). The face size is the Large Armor Module's.
- Each link has a thin box visual and collision, so the depth camera sees
  it and shots can be scored against it.
- `thornbots_pkg`'s URDF gets the same frames, and `test_urdf_constants.py`
  pins `cv_target_emulator`'s and `bench_world.cpp`'s panel constants to
  them, as it does the head chain now.

## The match test

### What sim provides

| Piece | Today | Build |
|---|---|---|
| Opponents | `target_driver` is a phantom; `actor_driver` spawns plain boxes | Spawn N `sentry_v2` copies, each with a team. One `opponent_driver` node moves them all along `target_driver`'s path profiles with chassis spin, aims each head at our panels from truth with added noise, and fires at a set rate |
| An ally | None | One copy on our team, so the selector has to drop its panels and we must never fire at it |
| Detector stand-in | Nothing publishes `/detections_output` in sim | For every panel on every other robot: look up its pose at the depth image's stamp, project the corners through `CameraInfo`, and keep it if it faces the camera (the 145 deg exposure cone), lands in the image, and the rendered depth at its centre agrees with its projected depth. The depth check gives occlusion by the field and other robots for free. Publishes the `Detection2DArray` YOLO would, in network space with the 640x640 letterbox `roi_depth_node` now undoes, class by team (blue 0-3, red 4-7), stamped with the image stamp. Pixel jitter and dropout are parameters, off at first |
| Depth units | gz publishes 32FC1 metres; `roi_depth_node` reads 16UC1 millimetres | Convert in a small sim node, or let `roi_depth_node` accept both. Check the encoding on a live topic first |
| Extrinsics | Nothing publishes `/extrinsics/depth_to_color` | Publish identity, since the stand-in's boxes are in the depth camera's frame |
| MCB emulator | `pose_emulator` publishes `/pose` and `cv_head_aim` reads `/cv/target`, both skipping the wire | A Python node on the other end of a pty from `dji_serial_bridge`. Sends `POSE_MSG` at 100 Hz from gz wheel odometry with `pose_emulator`'s noise model, and `REF_SYS_MSG` at 5 Hz from the referee emulator. Decodes `CV_MSG`, drives the gz head to the root-frame point, and fires on `fire` after `delay_ms`. Applies `RELOCALIZE` to its odometry origin. Replaces `pose_emulator` and `cv_head_aim` in this test |
| Driving | The drift harness steps `/cmd_vel` | The test drives our chassis through the MCB emulator from a scripted route with finite acceleration (ROADMAP S3), the way the MCB's own drive would move it |
| Referee emulator | No `RefSysStatus` in sim | Tracks every robot's HP. A scored hit costs 20 HP, and on our robot sets `deltaAngleGotHitIn`. Also sets team, game stage and time left. Feeds the MCB emulator's `REF_SYS_MSG` |
| Shots | Only the Python harnesses fly shots | Every shot, ours or an opponent's, flies a straight line at 25 m/s from the gz muzzle at fire time. The first thing it crosses wins: a panel's canted square, a robot hull, or nothing. A panel hit counts only above 12 m/s normal speed and 50 ms after that panel's last hit, per the rules. Scoring against the canted square fixes ROADMAP's Caveat that hits are scored as distance to the centre |

Driving comes from sim for now. `ROS_MSG` goals have no publisher in this
workspace, and navigation comes after the Midwest competition. Once a
planner exists, a later stage hands the route to it over `ROS_MSG`.

Opponents run a truth-fed aimer, not a copy of our stack, because two full
stacks don't fit the compute budget. A red-against-blue run with two real
stacks is out of scope.

### Stages

Each stage adds hops and is its own commit and bump. Scoring stays the same
from stage to stage, so a drop belongs to the hops that stage added.

1. E1, the stand-in to the gimbal, our robot parked. Panels on the URDF, one
   opponent running C1's cells, the stand-in, depth, extrinsics, and a team
   stub in place of the referee. The real `roi_depth_node`, selector,
   tracker and `point_to_cv_target` feed `cv_head_aim`.
2. E2, the wire. `dji_serial_bridge` and `mcb_relay` on a pty against the
   MCB emulator, which replaces `pose_emulator`, `cv_head_aim` and the team
   stub. Tests the `CV_MSG` packing, the stamps both ways, the fire path,
   and `REF_SYS_MSG` into the selector.
3. E3, driving while shooting. Our robot drives the scripted route: straight
   at 1 and 2 m/s, a 90 deg turn while driving, and spinning in place.
   Localization from gz lidar is in the loop, so its error at fire time
   lands in the score. Aim is still the root-frame point, which measures
   what the current wire format costs while moving.
4. E4, the match. Several opponents and the ally, with opponents shooting
   back and the referee emulator counting HP. One fixed-seed scenario of set
   length, split into scored segments.
5. E5, the world-frame aim. `RobotPose` stamped at capture with chassis yaw
   and yaw rate, every TF lookup at the data's own time, and the aim as a
   world-frame command the MCB emulator holds with its IMU
   (`CV_SPLIT_PLAN.md` W.1-W.5). Agree the wire change with the firmware
   side before it goes past the emulator.

### Scoring

One `sim/launch/e2e.launch.py` and a pytest suite in `sim/test/e2e/`. Per
segment:

- hit rate on enemy panels, the pass condition, with floors from three runs
  minus 10 points, like C1's `FLOORS`;
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
has a diagnostic that names the hop that lost it. E5 is done when each
moving segment comes within 10 points of the same target cell with our
robot parked.

## Open questions for the user

| Question | Recommendation |
|---|---|
| Time budget for the regular run | Set it after the speed work's first measurements |
| How many robots in E4 | The full 3v3, three opponents and two allies, if the RTF holds; one of each if it doesn't |
| MCB emulator in Python or a firmware build on the host | Python first; a host build of the real firmware later, if the firmware side can produce one |
| How the MCB's own drive behaves (acceleration, yaw hold) | Ask the firmware side before E3, so the emulator matches it |
