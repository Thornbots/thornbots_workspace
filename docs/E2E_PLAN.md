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

The full gz stack's RTF cap has no named cause yet
([ROADMAP track D](ROADMAP.md#d-faster-suites)).

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
   2026-09-29); settle its rate once a stage consumes images.
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
7. Lockstep the gz stack so results don't depend on machine speed:
   [`E2E_LOCKSTEP_PLAN.md`](E2E_LOCKSTEP_PLAN.md) (the user, 2026-10-08).
   Partly on nightly (`lockstep:=true` by default); its done bar isn't met.

Done when each suite's time split is logged, the RTF cap has a named cause,
and the regular run (unit tests, then the match test) fits 10 minutes, and
5 without the match test (the user, 2026-09-28).

## The match test

### What sim provides

| Piece | Today | Build |
|---|---|---|
| Opponents | `mcb_parked` uses one red ghost on field-safe diagnostic paths. `mcb_drive` approaches center from red spawn. `mcb_match` has two red ghosts on separate routes, with truth-fed noisy aim and 2 Hz fire | Tune ghost aim realism and repeated-run spread |
| An ally | `mcb_match` has one blue ghost, routed from blue spawn and firing at red panels. The selector drops its blue detections; first-impact scoring detects unintended intersections | Zero firmware shots intersecting the ally; intermittent failures remain |
| Detector stand-in | `detector_standin` (`sim/src/detector_standin.cpp`) publishes `/cv/panel_detections` for every stage with no camera, in `roi_depth_node`'s place (the user, 2026-10-05) | Every 60 Hz sim tick: each panel on every other robot that faces the camera (the 145 deg exposure cone) and lands in the D435's image, its true centre and corners in `camera`, class by team (blue 0-3, red 4-7). Ray noise is a parameter, off by default. Occlusion by the field and other robots: not done (the depth check went with the camera) |
| MCB emulator | Every stage and `mcb.launch.py` run checked-out MCBV3 on a pty inside each gz physics step. The parked stage and MCB launch optionally execute the normal board ELF in [Renode](../sim/README.md#type-c-board-execution-with-renode) | The owner documents peripheral/timing and plant limits. POSE/REF_SYS, CV_TARGET, RELOCALIZE and motor control come from the firmware; rebuild after firmware edits |
| Driving | `mcb_drive`/`mcb_match` select firmware auto-drive through DBUS; ghosts own their routes. The board ELF defaults to Renode with CAN motor feedback/forces and AMCL/rf2o/EKF active. [Design](../sim/README.md#driving-and-combat-diagnostics-mcb_drive) | [Acceptance evidence](../sim/docs/mcb-auto-drive-2026-10-12.md); navigation publisher is later work |
| Referee emulator | `mcb_match` tracks 400 HP per robot, 20 HP per hit. HP, team, stage, time and hurt panel enter the physical referee parser; HP and team are checked on returning UART `REF_SYS` | Verify `delta_angle_got_hit_in`; heat, ammo and respawn are not modeled |
| Shots | `mcb_match` advances ballistic 25 m/s shots from truth muzzles. The first field, chassis hull or canted panel impact absorbs the shot. Damage needs >12 m/s relative normal speed, the exposure cone and 50 ms per-panel dead time | Non-chassis appendage blockers and detector occlusion remain unmodeled |

Driving comes from sim for now. `NAV_GOAL` goals have no publisher in this
workspace, and navigation comes after the Midwest competition. Once a
planner exists, a later stage hands the route to it over `NAV_GOAL`.

Opponents run a truth-fed aimer, not a copy of our stack, because two full
stacks don't fit the compute budget. A red-against-blue run with two real
stacks is out of scope.

### Stages

Each stage adds hops and is its own commit and bump. Scoring stays the same
from stage to stage, so a drop belongs to the hops that stage added. Every
stage runs the MCB emulator (the user, 2026-10-08); the former E1, which
skipped it, is gone. Older records use E2-E4 for these stages.

1. `mcb_parked` (E2), the wire, our robot parked. The detector stand-in,
   the real selector, tracker and `point_to_cv_target`, then
   `dji_serial_bridge` and `mcb_relay` on a pty against the MCB emulator.
   Tests the `CV_TARGET` packing, the stamps both ways, the fire path, and
   `REF_SYS` into the selector, scoring through the compiled firmware on
   field-safe paths.
2. `mcb_drive` (E3), driving while shooting. The firmware's own auto-drive
   takes our robot from its provisional team spawn around the south walls to
   center. Fused navigation from gz lidar is measured beside the shot score.
   Aim uses raw `odom`; chassis yaw is still absent from the current POSE wire
   payload.
3. `mcb_match` (E4), the match, 2v2: two opponents and one ally (the user,
   2026-09-28), with opponents shooting back and the referee emulator
   counting HP. One fixed-seed scenario of set length, split into scored
   segments.

Remaining moving-shooter work and its acceptance bar are in
[ROADMAP track B](ROADMAP.md#b-hit-while-we-move).

All three stages run on nightly. Commands and model limits are in
[sim's README](../sim/README.md#driving-and-combat-diagnostics-mcb_drive);
current results and open work are in [ROADMAP track A](ROADMAP.md#a-the-match-test).

### Scoring

One `sim/launch/e2e.launch.py` and a C++ suite in `sim/test/e2e/`. Per
segment:

- hit rate on enemy panels, the pass condition, with floors from three runs
  minus 10 points, like the aiming bench's `FLOORS`;
- shots at the ally, which must be zero;
- for `mcb_drive` on: route error and localization error (`map->root` against gz truth) at
  each fire time;
- damage taken, logged only, with no pass condition until opponents' aim is
  tuned to something realistic.

Diagnostics logged beside each segment: ROI depth error against truth,
`TargetState` error (`estimation_metrics`), and each hop's stamp against
the image stamp. Each miss is split into raw pose error, `TargetState`
error and aim error; navigation truth error is recorded separately.

Aim uses raw odometry independently of navigation corrections. See
[the wire frame contract](../ros2_dji_serial_bridge/UART_PROTOCOL.md#message-types)
and [the frame tree and `root` choice](../thornbots_pkg/README.md#pose_translator).

### Done when

`mcb_match` runs in one gz session, every segment scores the same alone and in
sequence, and each segment's hit rate is within 10 points of its floor or
has a diagnostic that names the hop that lost it.
