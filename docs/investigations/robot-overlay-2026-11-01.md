# Robot registry base and offline overlay — 2026-11-01

T29 chooses occasional registry pulls and local source overlay builds as the
supported robot workflow. The image retains its tested baked application for
explicit recovery; ordinary source updates no longer rebuild the image.
The maintained procedure is the [image workflow](../../isaac_ros_common/docker/README.md#building-the-robots-image).

## Scope and environment

- Host: `ts-nano-dev`, NVIDIA Jetson Orin Nano Engineering Reference Developer
  Kit Super, aarch64, 8 GB RAM, six online CPU cores, NVMe, 311 GB free
  before pulling. Power mode `MAXN_SUPER`; no clock or power settings changed.
- Network: campus Wi-Fi (`wlP1p1s0`), SSH over Tailscale; no controlled
  bandwidth benchmark. Docker already held a preceding nightly and local base
  images. These numbers describe a changed-layer pull, not a cold installation.
- Source: workspace branch `t3/robot-overlay-workflow`; all seven application
  packages copied from its pinned gitlinks into an isolated
  `/home/nano-dev/workspaces/t29-overlay/src` checkout. No firmware or sim run.
- Registry manifest: `ghcr.io/thornbots/isaac-ros@sha256:11e516ae74448627dd6d64e9f5b488c26452566dd7efdfd2039de239adcbe4f1`,
  42 layers, 12,482,061,239 compressed bytes across the entire image. Seven
  layers downloaded; their manifest payload sizes total 6,747,095,382 compressed
  bytes. The remaining layers were already present. These descriptor sizes
  exclude protocol overhead and are not a measured network-byte counter.

## Measurements and checks

| Operation | Wall time | Result |
| --- | --- | --- |
| Changed-layer nightly pull | 416.212 s (6 min 56 s) | Updated registry tag; existing base layers reused |
| Cached pull plus offline compatibility check and pin | 2.640 s | New nightly matches source dependency inputs |
| Clean offline overlay, supported defaults | 426.881 s (7 min 7 s) | All seven packages built; matching image readiness marker written |
| Offline incremental C++ rebuild | 47.470 s | Touched `dji_serial_bridge_node.cpp`; same image, networking and GPU injection disabled |
| Initial clean build, before CUDA toolchain fix | 152.668 s | Failed safely at YOLO bridge CUDA architecture detection; no ready marker |

The initial container smoke check passed with an isolated ROS domain and no
running launch. Before building, package prefixes resolved to the image-baked
`/workspaces/ros2_ws/install`, reproducing the documented shadowing hazard.
The offline compatibility check rejected the preceding image because its
`sentry_localization/package.xml` differed from current source. This is the
intended signal to pull a newer compatible base.

The first build exposed a clean-environment CUDA configuration issue:
CMake could not infer a default architecture with the image's CUDA 13.2.2.
The supported build now selects `/usr/local/cuda/bin/nvcc` and Orin `sm_87`
explicitly, and caps concurrency at two colcon workers and `MAKEFLAGS=-j2`
for this 8 GB board. The failed attempt never wrote `.robot-overlay-image`.
The successful clean build reported seven packages finished in 7 min 0 s;
426.881 s is the complete host helper wall time, including compatibility
checks, container creation/removal and prefix validation. All seven package
prefixes resolved under `/workspaces/isaac_ros-dev/install`.
The incremental run touched `ros2_dji_serial_bridge/src/dji_serial_bridge_node.cpp`
to force one real translation-unit rebuild without changing behavior. It
finished the seven-package colcon invocation in 41.2 s (47.470 s host helper
wall time), rebuilt the bridge in 39.3 s, reused the other package outputs,
and never pulled an image. Docker inspection confirmed `NetworkMode=none`
and no GPU device requests (`ISAAC_AGENT_GPU=none`).
Vendor lidar warnings include zero-length arrays (a C++ extension) and ignored
return values; these are existing departures from standard practice.

## Acceptance boundary and robot state

`ts-nano-dev` initially had no `thornbots.service`, camera, lidar, or model
assets, and no running containers. It can validate compilation and package
resolution but cannot validate the physical stack. SSH to `ts-nano-sentry`,
`ts-nano-standard`, and `ts-nano-hero` timed out during banner exchange; no
commands ran there. Physical stack startup/restart acceptance remains open.
The final startup-helper environment check passed: all seven application
prefixes resolved inside the overlay and `AMENT_PREFIX_PATH` contained no
`ros2_ws` entry. The allocated domain/partition were preserved. It ran no
launches. All task-owned containers and volumes were removed. Dev retains the
prepared image (also protected by its immutable local base tag) and isolated
workspace (140 MB build, 6.1 MB install, 1.8 MB
logs), with matching image/readiness markers; its original workspace and
absent service installation were left unchanged. No robot stack was stopped
or started. Thus the requested working-stack end state cannot be claimed.
No driving, firing, or MCB flashing was performed.

## Decision

Keep registry pulls explicit and infrequent: before an event and whenever the
offline dependency-input check reports a mismatch. Source-only changes build
against the last pinned compatible image with networking disabled. A changed
Dockerfile/configuration or dependency manifest needs a compatible published
image; an upstream CLI/base change also requires a new pull and remains a
manual check for existing images. Never attempt a dependency update for the
first time without internet at an event. Keep the previous compatible source,
image and ready overlay available in a separate prepared workspace as a recovery
set; a rebuild invalidates and mutates its own workspace artifacts.

Local full-image builds and their compression/cache/USB-versus-reverse-SSH
optimization questions leave the normal workflow. The legacy build/ship helper
remains an emergency fallback when the registry cannot supply a compatible
image; it is not needed for an ordinary application edit.
