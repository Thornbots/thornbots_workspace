# Plan: end-to-end CV tests in sim

2026-09-25. Two tests, in order. E runs the whole CV stack as it stands, from
rendered pixels to a scored shot, with our robot parked. M adds our own
motion: we drive, turn and shoot at once. M needs the world-frame aim from
`CV_SPLIT_PLAN.md` "Hitting while we move"; E needs nothing new from the
robot code.

C1 and C2 each test one half against perfect inputs. Nothing today runs the
camera, YOLO, `roi_depth_node`, or the serial link in sim, and no test runs
more than the tracker and Part 1 together. E is where a wrong stamp, frame or
depth unit between two stages shows up.

## Before either: what C2 says today

Two gz C2 runs at 1x and one at 0.5x (2026-09-25, `../log/cv_runs/est_*`):

| Flat cell | 1x run A | 1x run B | 0.5x | offline |
|---|---|---|---|---|
| stationary | 0.041 | 0.013 | 0.013 | 0.008 |
| 0.5 m/s | 0.224 | 0.123 | 0.139 | 0.057 |
| 1 m/s | 0.180 | 0.179 | 0.125 | 0.080 |
| 2 m/s | 0.195 | 0.189 | 0.510 | 0.118 |
| 4 m/s | 0.306 | 0.432 | 0.250 | 0.116 |

Facing-panel p95 in metres. Run A predates the still hypothesis.

Unthrottled C2 reaches only 0.95-1.0x (the gz server is the ceiling; the box
sits 40% idle), and halving the speed changed nothing beyond run-to-run
spread. So speed doesn't cost accuracy. The gz moving cells are 2-4x worse
than offline and vary by 2x between runs. E would inherit that error, so
trace it first (`CV_SPLIT_PLAN.md` Next, step 1): the offline copy leaves out
the head slewing the camera, so the camera TF at capture time is the first
suspect.

## E: the whole CV stack, our robot parked

The chain under test, as `auto.launch.py` and
`isaac_ros_yolov8_realsense.launch.py` run it on the robot:

```
gz rgbd camera -> /color/image_raw, /depth/image_rect_raw
  -> DNN encoder -> TensorRT (YOLO11s, 8 classes) -> YoloV8 decoder -> /detections_output
  -> roi_depth_node -> /cv/panel_detections
  -> target_selector -> /cv/robot_panels
  -> target_tracker -> /cv/target_state
  -> point_to_cv_target -> /cv/target (CVTarget, root frame)
  -> mcb_relay -> dji_serial_bridge -> UART CV_MSG -> MCB -> gimbal, fire
```

The sim has the camera (640x480 at 60 Hz, `sim.launch.py camera:=true`). It
has nothing for that camera to see, and the last three hops don't run.

### What's missing

| Gap | Today | Fix |
|---|---|---|
| Something to detect | `target_driver` is a phantom; `actor_driver` spawns plain boxes | A gz model of `sentry_v2` with armor panels (plates, light bars, number stickers) at the S122 cant and the two pair heights. `actor_driver` gains spin and `target_driver`'s path profiles so E runs C1's cells |
| YOLO weights | Only the Jetson `.plan` exists, and a TensorRT engine is built for one GPU | Get the ONNX from whoever trained it and build an x86 engine in the container (RTX 1000 Ada, 6 GB) |
| Depth units | gz publishes 32FC1 metres; `roi_depth_node` reads 16UC1 millimetres | Convert in the sim bridge (a small node, or `roi_depth_node` accepting both). Check the encoding on a live topic first |
| Extrinsics | Nothing publishes `/extrinsics/depth_to_color` | Publish identity: gz's rgbd sensor shares one frame for colour and depth |
| Team colour | No `RefSysStatus` in sim, so `target_selector` keeps every class | A stub publishes our team so the enemy classes are the only ones kept, as on the field |
| The MCB | `cv_head_aim` reads `/cv/target` directly; `mcb_relay` and `dji_serial_bridge` are off | Stage E3: run `dji_serial_bridge` on a pty, and an MCB emulator on the other end that decodes `CV_MSG`, drives the gz head and fires, and sends `RobotPose` frames back |
| Shots | Only the Python harnesses fly shots | Score in the harness as C1 does (straight line, 25 m/s, from the gz muzzle TF at fire time), against the rendered model's gz pose |

### Stages

Each stage adds hops and is its own commit and bump. Scoring stays the same
throughout, so a drop between stages belongs to the hops that stage added.

1. E1, a detector stand-in. A node projects the rendered model's panel
   corners from gz truth into the camera image and publishes
   `/detections_output` as YOLO would. From there on the real nodes run:
   `roi_depth_node` on gz depth, selector, tracker, Part 1, `cv_head_aim`.
   Needs the model, the depth conversion, the extrinsics and the team stub.
   This tests every stage except the network.
2. E2, real YOLO. Swap the stand-in for the TensorRT chain on rendered
   frames. Score detection recall and box error against the stand-in's boxes
   per cell. If a model trained on real frames misses rendered panels, fix it
   on the render side (textures, lighting), not by training on sim frames.
3. E3, the wire. `mcb_relay` and `dji_serial_bridge` on a pty against the MCB
   emulator, which replaces `cv_head_aim`. Tests the `CV_MSG` packing, the
   stamps both ways, and the fire path.

### Scoring

The same cells as C1 (both layouts, stationary and 0.5-4 m/s, spin 1-2 Hz),
each launched from one `sim/launch/e2e.launch.py` with a pytest suite in
`sim/test/e2e/`. Per cell:

- hit rate, the pass condition, with floors from three runs minus 10 points
  like 1.7;
- per-hop diagnostics logged beside it: detection recall, ROI depth error
  against truth, `TargetState` error (`estimation_metrics`), and each hop's
  stamp against the image stamp, so a latency or stamp bug is visible without
  a second run.

The head reset from C2 (aim at the truth during each case's reset) carries
over. At 60 Hz rendering plus TensorRT, the run will likely go slower than
1x. That's fine: the check above shows speed doesn't change scores, and
TensorRT's wall-clock time only matters if the sim outruns it.

### Done when

E3 runs every C1 cell in one gz session, scores the same alone and in
sequence, and each cell's hit rate is within 10 points of its C1 floor or has
a diagnostic that names the hop that lost it.

## M: moving and shooting at once

Our chassis drives and turns while it tracks and shoots. This is the test for
`CV_SPLIT_PLAN.md` W.1 to W.5 and it runs on E's stack, so it waits for E1 at
least.

### What changes from E

- Our robot moves. Scripted drive legs with finite acceleration (ROADMAP S3's
  ramp), translating and rotating: straight at 1 and 2 m/s, a 90 deg turn
  while driving, and spinning in place (our own chassis spin, the common
  RoboMaster defence).
- Our pose comes from the real localization stack (`sentry_localization`,
  amcl + EKF), not gz truth. Localization error at fire time then lands in
  the score, as it will on the field.
- `RobotPose` carries chassis yaw and yaw rate with a capture stamp (W.1).
  Until firmware exists, the MCB emulator from E3 builds it from gz's IMU and
  wheel odometry at the MCB's rate.
- The aim is a world-frame command (W.3) that the MCB emulator holds with its
  IMU while the chassis moves, as the real MCB would.

### Stages

1. M0, the baseline. E's stack with our robot moving, aim still the
   root-frame point. This measures how much the current wire format costs
   while moving. No code changes to the robot side.
2. M1, stamps and lookups (W.2). Every TF lookup at the time the data was
   true, `RobotPose` stamped at capture.
3. M2, the world-frame aim (W.3), in the MCB emulator first. Agree the wire
   change with the firmware side before it goes past the emulator.

### Scoring

Cells are (our motion) x (target cell): four chassis motions against C1's
stationary, 1 m/s and 4 m/s target cells, flat layout first. Per cell, the
hit rate, plus a split of each miss into our pose error at fire time (EKF
against gz truth), `TargetState` error, and aim error. That split says
whether a drop belongs to localization, Part 2 or Part 1. Floors come from
three M2 runs, like E.

### Done when

M2 runs every cell in one gz session, and each moving-shooter cell comes
within 10 points of the same target cell in E.

## Open questions for the user

| Question | Recommendation |
|---|---|
| Where the YOLO ONNX lives, and who can share it | Needed before E2; E1 can start without it |
| Where the armor textures come from | Photos of our own panels, cropped and mapped onto the plates |
| Where E and M live | `sim/test/e2e/` and one `e2e.launch.py`, like C2; the CV package split (ROADMAP Track B) doesn't change that |
| MCB emulator in Python or a firmware build on the host | Python first; a host build of the real firmware later, if the firmware side can produce one |
