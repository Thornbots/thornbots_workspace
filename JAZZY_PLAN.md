# Plan: move from ROS 2 Humble to Jazzy

ROADMAP.md track C. Covers this superproject, all nine submodules, the
laptop and the three robots (`ts-nano-sentry`, `ts-nano-hero`,
`ts-nano-standard`). The test box is `ts-nano-dev`.

**`main` is Jazzy since 2026-09-27.** Every repo's default branch took its
`jazzy`, the `jazzy` branches are deleted, and the `humble` branches hold
the last Humble tree, **frozen**: no more work goes there.
The robots stay on Humble, running that frozen tree, until step 6.

## Where this stands (2026-09-28)

The laptop half (steps 0, 2, 3 and 4) is done. `isaac_ros_common`'s `main`
is upstream `release-4.6` plus our container files, and the image comes
from `isaac-ros activate` (the `isaac-ros-docker` skill). Laptop results,
the baseline step 5 and the robots compare against:

| Check | Humble | Jazzy |
| --- | --- | --- |
| `colcon build`, 8 packages, `-Wall` | clean | clean; warnings only in `sllidar_ros2`'s vendored SDK |
| `colcon test` | `dji_serial_bridge` lint fails | same lint failures, nothing else |
| CV tests (`point_to_cv_target`, `target_selector`, `target_tracker`) | pass | pass |
| Drift suite, unthrottled | 7/7 | 7/7 in each of the last three runs |
| `suite:=ekf` fused mean | 0.0075 m | 0.0079 m |
| The aiming bench, 10 cells | 10/10 | 10/10, every score within 0.004 |
| The estimation bench, five runs | 10/10; moving cells 0.10 m facing p95 median | 10/10; 0.10 m; each cell within 10% of Humble except the 4 m/s ones, which swing on both |

Left: step 1 (reflash `ts-nano-dev`, runbook `JAZZY_FLASH.md`), step 5 (the
hardware checks on it), and step 6 (the robots). Before step 1 wipes the board,
record the Humble YOLO numbers step 5 compares against; step 0 had no
camera.

## Target

| | Today | After |
| --- | --- | --- |
| ROS 2 | Humble | Jazzy |
| Isaac ROS | 3.2 (`nvcr.io/nvidia/isaac/ros:humble-3.2`) | 4.6.0, released 2026-08-18 |
| Ubuntu in the image | 22.04 | 24.04 |
| Jetson OS | JetPack 6.2.x, L4T R36.5, kernel 5.15 | JetPack 7.2.1, L4T R39.2, kernel 6.8 |
| Container tooling | our fork's `run_dev.sh` / `build_image_layers.sh` | `isaac-ros-cli` (`isaac-ros activate`) |
| Gazebo (`sim` only) | Fortress, `ros-humble-ros-gz` | Harmonic, `ros-jazzy-ros-gz` |

Isaac ROS 4.6 is the only Jazzy release that runs on Orin. 4.0 to 4.5
supported Thor and x86 only; 4.6 added Orin on JetPack 7.2.

Isaac ROS 5.0 came out on 2026-09-21 on ROS 2 Lyrical. We take 4.6 anyway:
5.0 was four days old when this was written, and Jazzy has a year of Nav2,
slam_toolbox and robot_localization binaries behind it. Both need the same
JetPack 7.2 reflash and Ubuntu 24.04 image, so a later hop to Lyrical is a
package-level port with no hardware work.

Measured 2026-09-25: `ts-nano-dev` is an Orin Nano Super devkit (8 GB),
JetPack 6.2.x (L4T R36.5), 70 GB used of a 456 GB NVMe. The laptop (RTX 1000
Ada, driver 615.71) already meets 4.6's driver 595+ floor.

## What still has to be checked on hardware

- `yolo11s_fp16.plan` is tied to the TensorRT version. Rebuild it on each
  Orin from `best.onnx` in `Thornbots/trained-models` (LFS,
  `detect/yolo11s_realsense/v1/weights/`).
- Kernel 5.15 to 6.8: check `/dev/ttyTHS1` (DJI serial bridge) is still that
  UART, and that the RPLIDAR and RealSense enumerate.
- Fast DDS 2.6 to 2.14. `fastdds_cable.xml` should load unchanged, but its
  recorded invariants (239.255.0.1 in the peer list, `maxInitialPeersRange`
  32, SHM hiding local participants) were measured on 2.6. Measure again.
- Humble and Jazzy nodes on one DDS domain don't interoperate reliably. Jazzy
  machines run on `ROS_DOMAIN_ID=1` until the last robot moves.
- The image's layer count on aarch64. It is 42 on x86_64 (8 ours) after the
  `Dockerfile.thornbots` merge; the Humble image hit 127 of the ~128 cap.
- The CLI mounts each host's `~/.bashrc` and `~/.profile` into the
  container, and on apt installs `~/.config`, `~/.ssh` and `~/.cache`.
  Check each robot's dotfiles before its first Jazzy run
  (`isaac_ros_common/AGENTS.md`).

## Steps

### 1. Reflash `ts-nano-dev` to JetPack 7.2.1

1. Back up anything on it that isn't in git. An NVMe image (`dd` to the
   laptop, or a spare drive) is half the rollback: the installer moves QSPI
   firmware to 39.x, and an R36 NVMe won't boot on it until R36.5 firmware
   is reflashed from an Ubuntu 22.04 host in recovery mode.
2. Flash from the unified ISO on a USB stick. JetPack 7 has no SD-card image
   for Orin Nano.
3. Install Docker and the NVIDIA container toolkit, add the Isaac ROS apt
   repo (`release-4`, `noble-jetpack` on Jetson; `noble` is x86), then
   `sudo apt-get install isaac-ros-cli` and `sudo isaac-ros init docker`.
4. Check that `isaac-ros activate` starts the stock prebuilt image and that
   `tegrastats` works in it. Then `scripts/setup_workspace.sh` and
   `isaac-ros activate --build-local` for our three-layer chain, and count
   its layers.

`JAZZY_FLASH.md` is the runbook for all of this.

### 5. Hardware on `ts-nano-dev`

1. RealSense at 60 fps with our profiles (`docker/config/*_60fps.yaml`).
2. Rebuild the TensorRT engine, run `isaac_ros_yolov8_realsense.launch.py`,
   and compare YOLO fps and camera-to-`TargetState` latency with the Humble
   numbers taken before step 1.
3. Serial bridge on `/dev/ttyTHS1` and the RPLIDAR, if the parts fit on the
   dev box. Otherwise these move to the first robot in step 6.
4. DDS: repeat the 2026-09-14 and 2026-09-20 measurements recorded in
   `fastdds_cable.xml`, between `ts-nano-dev` and the laptop, on domain 1.
5. Time a full `colcon build` on the 8 GB Orin Nano. The `-j6` / 3-worker
   caps were set for the old toolchain.

### 6. The robots

The branches moved on 2026-09-27 (`main` is Jazzy, `humble` frozen).

1. Reflash `ts-nano-sentry` first, with an NVMe image taken beforehand. Run
   the step 5 checks and a full `auto.launch.py`.
2. Then `ts-nano-hero` and `ts-nano-standard`. Every machine goes back to
   `ROS_DOMAIN_ID=0` once the last Humble one is gone.
3. Remove the Humble images from the robots, rewrite every `humble`
   reference but the README's pointer to the `humble` branch, and delete
   track C from ROADMAP.md.

## Done when

The drift suite, `suite:=ekf` and both benches give the same verdicts on
Jazzy as on Humble, and `point_to_cv_target`, `target_selector` and
`target_tracker` pass (met on the laptop). Added for hardware: YOLO fps and
detection latency on the Orin are no worse than on Humble.

## Risks

| Risk | Answer |
| --- | --- |
| 4.6's Orin support is one release old; the JetPack 7.2 Orin Nano forum thread is still active | Step 5 runs on the spare box; the robots are untouched if it fails |
| The aarch64 image hits the 128-layer cap | Count layers in step 1, before any hardware check |
| A lost lifecycle reply stalls the robot's localization at boot | Seen only in sim so far, on Humble too. Watch for it in step 6's `auto.launch.py` runs |
| A competition date lands mid-migration | Robots stay on Humble until step 6, each with an NVMe image and R36.5 firmware to roll back to |

## Sources

- [Isaac ROS 4.6 getting started](https://nvidia-isaac-ros.github.io/v/release-4.6/getting_started/index.html): Jazzy, Orin on JetPack 7.2, driver 595+
- [Isaac ROS release notes](https://nvidia-isaac-ros.github.io/releases/index.html): 4.6 adds Orin; 5.0 moves to Lyrical
- [Docker mode configuration](https://nvidia-isaac-ros.github.io/v/release-4.6/concepts/dev_env/index.html)
- [isaac-ros-cli release-4.6](https://github.com/NVIDIA-ISAAC-ROS/isaac-ros-cli/tree/release-4.6)
- [JetPack 7.2 on Orin Nano forum thread](https://forums.developer.nvidia.com/t/jetpack-7-2-jetson-linux-r39-2-on-jetson-orin-nano-developer-kit-getting-started-and-feedback-thread/372151), [JetPack 7.2.1 notes](https://jetsonhacks.com/2026/08/12/jetpack-7-2-1-released/)
