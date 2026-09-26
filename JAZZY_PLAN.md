# Plan: move from ROS 2 Humble to Jazzy

ROADMAP.md Track D, 2026-09-25. Covers this superproject, all nine
submodules, the laptop and the three robots (`ts-nano-sentry`,
`ts-nano-hero`, `ts-nano-standard`). The test box is `ts-nano-dev`.

**Track D still goes last.** Steps 0 to 5 happen on `jazzy` branches and on
`ts-nano-dev`, so `main` and the robots stay on Humble and no suite verdict
gets mixed up with a distro change. Only step 6, the cutover, waits for
Tracks A to C.

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

## What breaks

### Container tooling

Upstream `isaac_ros_common` 4.x has no `docker/` and no `scripts/`. The
Dockerfiles and `run_dev` moved into a separate apt package,
[isaac-ros-cli](https://github.com/NVIDIA-ISAAC-ROS/isaac-ros-cli/tree/release-4.6).

- Our fork's `run_dev.sh`, `build_image_layers.sh`, `Dockerfile.ros2_humble`,
  `Dockerfile.x86_64`/`aarch64` and `Dockerfile.realsense` go away. The new
  chain is `isaac_ros` (prebuilt on NGC), then `realsense` (shipped by the
  CLI: librealsense v2.56.3, realsense-ros 4.56.3), then `thornbots`.
- The CLI finds our layer through `CONFIG_DOCKER_SEARCH_DIRS` in
  `.isaac_ros_common-config`, which it only looks for in
  `$ISAAC_ROS_WS/scripts/`, `$ISAAC_ROS_WS/../scripts/` and
  `/etc/isaac-ros-cli/`. The workspace YAML config is
  `$ISAAC_ROS_WS/.isaac-ros-cli/config.yaml`. `ISAAC_ROS_WS` is
  `isaac_ros-dev/`, outside this repo, so a setup script symlinks both in
  from `src/`. Search dirs resolve relative to the config file's
  unresolved path, so the entry is `../src/isaac_ros_common/docker`.
- `--context_dir` becomes the `context_overrides` key (image key to context
  dir), so `Dockerfile.thornbots` keeps `src/` as its context.
- The default container name is now `isaac_ros_dev_container`. `dexec.sh` and
  `kill_launch.sh` derive `isaac_ros_dev-$(uname -m)-container`. Setting
  `docker.run.container_name` to the old name keeps both scripts working.
- The workspace still mounts at `/workspaces/isaac_ros-dev`, and
  `/workspaces/ros2_ws` is ours, so in-container paths and the shadowing trap
  stay the same.
- The `isaac-ros-docker` skill forbids `run_dev.sh` in any form. It needs the
  same rule for `isaac-ros activate` and `--build-local`, and `reference.md`
  needs a new flag catalogue.

### Package code

| Where | Change | Why |
| --- | --- | --- |
| `sllidar_ros2`, `rf2o_laser_odometry` CMakeLists | `CMAKE_CXX_STANDARD 14` to `17` | Jazzy's rclcpp headers need C++17 |
| `image_snapshot_node.cpp`, `roi_depth_node.cpp` | `cv_bridge/cv_bridge.h` to `.hpp` | the `.h` header is deprecated |
| `rf2o` `CLaserOdometry2DNode.hpp` | check the `tf2/*.h` includes build clean | Jazzy still ships them |
| `image_snapshot_node.cpp`, bridge README | optional: `SharedPtr` `take()` overload, drop the Humble note | the overload landed in Iron; the current code compiles |
| `thornbots_pkg`, `sentry_localization` `setup.py` (`sim` is `ament_cmake` since 2026-09-25) | drop `tests_require`; `script-dir`/`install-scripts` to `script_dir`/`install_scripts` | Noble's setuptools warns on both; newer versions reject the dashed keys |
| `install-sim.sh` | `pip install trimesh` to apt `python3-trimesh`, via a rosdep key in `sim/package.xml` | Ubuntu 24.04 enforces PEP 668, so the bare `pip install` fails |
| 5 CMakeLists with `ament_target_dependencies` | leave | deprecated only from Kilted |

The NITROS bridge should port as is. The 4.6 headers for
`ManagedNitrosPublisher`, the `NitrosImageBuilder` methods we call,
`nitros_image_rgb8_t`, and the `TensorRTNode` / `YoloV8DecoderNode` plugin
names and parameters all match our launch file. 4.5's CUDA-stream change to
NITROS is the thing to watch at runtime.

### `sim`: Fortress to Harmonic

- `sentry.urdf.xacro`, `sentry_v2.urdf.xacro`: the `ignition-gazebo-*-system`
  plugin filenames (joint-position-controller, velocity-control,
  odometry-publisher, joint-state-publisher) to `gz-sim-*-system`, and
  `ignition::gazebo::systems::*` to `gz::sim::systems::*`.
- `head_slider_relay.py`: `ign topic` and `ignition.msgs.Double` to `gz topic`
  and `gz.msgs.Double`. Harmonic ships only the `gz` CLI.
- `drift_harness.py` and the skill's cleanup `ps | grep`: `ign gazebo` to
  `gz sim`. A stale pattern passes silently and leaves orphans.
- `sim.launch.py`: drop `IGN_GAZEBO_RESOURCE_PATH`; it already sets
  `GZ_SIM_RESOURCE_PATH`, and the `parameter_bridge` strings already use
  `gz.msgs.*`.
- Physics and sensor noise may differ between Fortress and Harmonic. If a
  drift verdict moves, look there before blaming ROS.

### Runtime and hardware

- `yolo11s_fp16.plan` is tied to the TensorRT version, and JetPack 7.2 brings
  a new one. Rebuild it from ONNX on each Orin; confirm the ONNX file is in
  hand before flashing anything.
- Our 60 fps `realsense_mono*.yaml` overwrite the same-named files in
  `isaac_ros_realsense/config`. Diff them against 4.6's before copying.
- Kernel 5.15 to 6.8: check `/dev/ttyTHS1` (DJI serial bridge) is still that
  UART, and that the RPLIDAR and RealSense enumerate.
- Fast DDS 2.6 to 2.14. `fastdds_cable.xml` should load unchanged, but its
  recorded invariants (239.255.0.1 in the peer list, `maxInitialPeersRange`
  32, SHM hiding local participants) were measured on 2.6. Measure again.
- Humble and Jazzy nodes on one DDS domain don't interoperate reliably. Jazzy
  machines run on `ROS_DOMAIN_ID=1` until cutover.
- The `Dockerfile.thornbots` rebuild is uncached anyway, so fold in the
  layer-budget item from `isaac_ros_common/AGENTS.md` (`COPY --parents
  */package.xml`, one `COPY` for sources, merged `bashrc` RUNs). Count layers
  on aarch64: the new base's count is unknown, and 128 is the cap.

## Steps

### 0. Humble baseline (laptop, no Jazzy yet)

On today's `main`, record what Track D's "done when" compares against: the
drift suite, `suite:=ekf`, the C1 aim bench and C2 once it has limits, and
`thornbots_pkg`'s `point_to_cv_target`, `target_selector` and
`target_tracker` tests. On a robot, record YOLO fps and camera-to-
`TargetState` latency. The numbers go in the commit message that opens the
`jazzy` branch.

### 1. Reflash `ts-nano-dev` to JetPack 7.2.1

1. Back up anything on it that isn't in git. An NVMe image (`dd` to the
   laptop, or a spare drive) is the rollback.
2. Flash from the unified ISO on a USB stick. JetPack 7 has no SD-card image
   for Orin Nano.
3. Install Docker and the NVIDIA container toolkit, add the Isaac ROS apt repo
   (`release-4`, `noble`), then `sudo apt-get install isaac-ros-cli` and
   `sudo isaac-ros init docker`.
4. Check that `isaac-ros activate` starts the stock prebuilt image and that
   `tegrastats` works in it.

### 2. Container tooling: `isaac_ros_common` branch `jazzy`

Upstream's 4.x branches hold only ROS packages we don't build, so the old
reason for the fork, re-merging upstream's docker files, is gone. We keep the
submodule so every path stays `isaac_ros_common/docker/...` and
`isaac_ros_common/scripts/...`, and start `jazzy` from upstream
`release-4.6` with only our files on top:

```text
docker/Dockerfile.thornbots      FROM ${BASE_IMAGE}; ROS_SETUP=/opt/ros/jazzy; --rosdistro jazzy; layer merge
docker/config/*.yaml             60 fps RealSense profiles, rediffed against 4.6
docker/fastdds_cable.xml         unchanged until step 5 measures it
docker/scripts/install-sim.sh    jazzy paths, apt trimesh
docker/udev_rules/98-rplidar.rules, docker/scripts/hotplug-rplidar.sh
scripts/.isaac_ros_common-config CONFIG_DOCKER_SEARCH_DIRS=(../src/isaac_ros_common/docker)
.isaac-ros-cli/config.yaml       additional_image_keys [realsense, thornbots],
                                 context_overrides thornbots -> src/, container_name
scripts/dexec.sh, kill_launch.sh
scripts/setup_workspace.sh       symlinks isaac_ros-dev/scripts and .isaac-ros-cli into src/
```

Check on the laptop first (faster, no layer-cap problem), then on
`ts-nano-dev`: `isaac-ros activate --build-local` builds the three-layer
chain, `dexec.sh` finds the container, and the aarch64 layer count is well
under 128. Rewrite the `isaac-ros-docker` skill and
`isaac_ros_common/AGENTS.md` on the superproject's `jazzy` branch.

### 3. Port the packages, one `jazzy` branch each

Every row of the package table, then `colcon build` of the seven image
packages plus `sim` with warnings on, then `colcon test`. The superproject's
`jazzy` branch points `.gitmodules` at the `jazzy` branches, so a teammate
checks it out with the README one-liner. `main` never sees a Jazzy gitlink
before cutover.

Dependency order: `ros2_dji_serial_bridge`, `sllidar_ros2`,
`rf2o_laser_odometry`, `sentry_localization`,
`Realsense_ROI_Depth_Rectifier`, `realsense-yolov8-nitros-bridge`,
`thornbots_pkg`, `sim`.

### 4. Sim suites on the laptop

`install-sim.sh`, then the drift suite, `suite:=ekf`, both benches and the CV
tests. Compare with step 0. Explain any moved verdict before step 6, whether
it comes from Harmonic physics or a Nav2/slam_toolbox default that changed
(diff `sentry_localization/config/*.yaml` against the Jazzy defaults).

### 5. Hardware on `ts-nano-dev`

1. RealSense at 60 fps with our profiles.
2. Rebuild the TensorRT engine, run `isaac_ros_yolov8_realsense.launch.py`,
   and compare fps and latency with step 0.
3. Serial bridge on `/dev/ttyTHS1` and the RPLIDAR, if the parts fit on the
   dev box. Otherwise these move to the first robot in step 6.
4. DDS: repeat the 2026-09-14 and 2026-09-20 measurements recorded in
   `fastdds_cable.xml`, between `ts-nano-dev` and the laptop, on domain 1.
5. Time a full `colcon build` on the 8 GB Orin Nano. The `-j6` / 3-worker
   caps were set for the old toolchain.

### 6. Cutover, after Tracks A to C

1. Merge each package's `jazzy` into its default branch and push, then merge
   the superproject's `jazzy`. `isaac_ros_common`'s `.gitmodules` branch
   becomes `jazzy`, and the README table follows. That bump is one commit.
2. Reflash `ts-nano-sentry` first, with an NVMe image taken beforehand. Run
   the step 5 checks and a full `auto.launch.py`.
3. Then `ts-nano-hero` and `ts-nano-standard`. Every machine goes back to
   `ROS_DOMAIN_ID=0` once the last Humble one is gone.
4. Remove the Humble images from the robots, rewrite every `humble` reference
   left in the docs, and delete Track D from ROADMAP.md.

## Done when

Track D's bar: the drift suite, `suite:=ekf` and both benches give the same
verdicts on Jazzy as on Humble, and `point_to_cv_target`, `target_selector`
and `target_tracker` pass. Added for hardware: YOLO fps and detection latency
on the Orin are no worse than step 0.

## Risks

| Risk | Answer |
| --- | --- |
| 4.6's Orin support is one release old; the JetPack 7.2 Orin Nano forum thread is still active | Step 5 runs on the spare box; the robots are untouched if it fails |
| The aarch64 image still hits the 128-layer cap | Count layers in step 2, before porting any package |
| Harmonic moves a sim verdict | Step 4 catches it while Humble is still the reference |
| A competition date lands mid-migration | Robots stay on Humble until step 6, each with an NVMe image to roll back to |

## Sources

- [Isaac ROS 4.6 getting started](https://nvidia-isaac-ros.github.io/v/release-4.6/getting_started/index.html): Jazzy, Orin on JetPack 7.2, driver 595+
- [Isaac ROS release notes](https://nvidia-isaac-ros.github.io/releases/index.html): 4.6 adds Orin; 5.0 moves to Lyrical
- [Docker mode configuration](https://nvidia-isaac-ros.github.io/v/release-4.6/concepts/dev_env/index.html)
- [isaac-ros-cli release-4.6](https://github.com/NVIDIA-ISAAC-ROS/isaac-ros-cli/tree/release-4.6)
- [JetPack 7.2 on Orin Nano forum thread](https://forums.developer.nvidia.com/t/jetpack-7-2-jetson-linux-r39-2-on-jetson-orin-nano-developer-kit-getting-started-and-feedback-thread/372151), [JetPack 7.2.1 notes](https://jetsonhacks.com/2026/08/12/jetpack-7-2-1-released/)
