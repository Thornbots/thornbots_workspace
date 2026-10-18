# Sentry nightly Jetson checks — 2026-10-18

Jetson-only observation of the already-running sentry stack. No firmware
flash, controller use, actuation, or MCB behavior changes. This is partial
hardware evidence, not acceptance of aiming, firing, or matched firmware.

## Configuration and evidence

Workspace: `4f9e73a945c99292eaa869d4c38d44dc2b991d1e` (`nightly`, clean
robot source tree). Runtime uses the image's `/workspaces/ros2_ws/install`,
with `USE_WS_OVERLAY=false`, ROS domain 1, mapping and `use_rf2o:=true`.

Image:
`ghcr.io/thornbots/isaac-ros:sha-4f9e73a945c99292eaa869d4c38d44dc2b991d1e-arm64-jetpack`.
Local image ID:
`sha256:aef7f2d8acb4af975dbc2a8e8da2e158b21bf5bdb87dcceeb9d80e43ca355e3e`.
42 layers, 36,786,722,123 bytes, arm64. L4T R39.2.1,
kernel `6.8.12-1021-tegra`, MAXN_SUPER. TensorRT Python runtime: `10.16.2.10`.

| Package | Pinned revision |
| --- | --- |
| Realsense_ROI_Depth_Rectifier | `a2e3cb4698fccee0832166f0eefeb502960aa0ac` |
| realsense-yolov8-nitros-bridge | `a8d2aafeb46a1b555f10e842a5bd7ac3b1d70c9a` |
| thornbots_pkg | `23db221064911b8d730710a368d5392d157bf931` |
| ros2_dji_serial_bridge | `3bdba2db51e7140299ed2ab67d98baea0466fbdb` |
| sentry_localization | `955bfda27c5afc3e8cb1b2b3dfaa7f4d690f948c` |
| rf2o_laser_odometry | `a2d858a5053790bc2add4edf2daa22d2097d0af5` |
| sllidar_ros2 | `da06ba0f51132d074c6ca7ed71c4a39ccc54ab67` |
| isaac-ros-startup | `efe5e525dfc3060f676b44327aa73ca0b376d495` |
| isaac_ros_common | `b8b55c5fb407da42c11a27be437b5436a7b5dbc2` |
| sim | `b4be627f6c9d10bb264c5f386e569b7c08f82369` |
| firmware/MCBV3 source pin | `3f14d5b4e5c5ae06541229452af4338943d6e8ae` |

The source firmware pin does **not** identify the firmware running on the
MCB. The MCB still runs its previous firmware; its exact flashed revision
is unknown. POSE/REF_SYS frame and semantic values remain untrusted until
firmware matches. No controller-on tests were performed.

Raw evidence is on archlinux at
`/home/blaise/sentry-deploy/2026-10-18/jetson-validation/`:

- [Preflight and startup log extracts](ssh://archlinux/home/blaise/sentry-deploy/2026-10-18/jetson-validation/preflight.txt).
- [65-second topic summary and schemas](ssh://archlinux/home/blaise/sentry-deploy/2026-10-18/jetson-validation/20261018T193615Z-baseline.json).
- [Per-message timestamps, metadata, positions and TF](ssh://archlinux/home/blaise/sentry-deploy/2026-10-18/jetson-validation/20261018T193615Z-baseline.jsonl).
- [Collector source](ssh://archlinux/home/blaise/sentry-deploy/2026-10-18/jetson-validation/observe_jetson.py).
- [USB disconnect evidence](ssh://archlinux/home/blaise/sentry-deploy/2026-10-18/jetson-validation/connectivity-loss.txt).

SSH links identify host files; use the commands below if the reader does
not open them. Raw payload images were not streamed for the baseline;
the collector retained header timestamps and decoded small-message fields.

## Method and power recovery

Baseline: 19:36:15–19:37:20 UTC (65.166 s). The observer used Foxglove
`foxglove.sdk.v1`; rates are `(N-1)/(last receipt-first receipt)` on each
topic's received span. Small messages and image headers were retained.
No stack parameters, models, launch configuration or firmware were changed.

At 19:37:46 UTC USB disappeared. The user confirmed the battery died.
Power returned and USB reappeared at 19:42:22. NTP corrected the clock by
+293.4 s at 19:44:15. The launcher's clock guard deliberately exited with
75/TEMPFAIL and systemd restarted it at 19:44:26 (`NRestarts=1`). This was
an automatic recovery, not an unexplained process crash. Shutdown SIGINT
errors in that interval must not be counted as independent crashes.

Postboot panel capture: 19:45:12 UTC, 30 s. A separate same-Jetson raw DDS
subscriber ran for 70.008 s, with received spans about 67.2 s. A detached
SSD CSV subscriber captured hand movement and stationary drift, including
while USB networking was disconnected. Wi-Fi SSH worked through the team
Tailscale daemon on archlinux; ordinary archlinux SSH to the peer address
uses a different daemon/route and timed out.

Commands (archlinux unless specified):

```bash
EVIDENCE=~/sentry-deploy/2026-10-18/jetson-validation
python "$EVIDENCE/observe_jetson.py" --duration 65 --label baseline
python "$EVIDENCE/observe_jetson.py" --duration 30 --label panel-postboot
tailscale --socket=/run/tailscale-thornbots/tailscaled.sock ping --timeout=4s --c=2 ts-nano-sentry
ssh -o 'ProxyCommand=tailscale --socket=/run/tailscale-thornbots/tailscaled.sock nc %h %p' \
  nano-sentry@100.110.38.3 'systemctl show thornbots -p ActiveState -p NRestarts'
```

The Docker skill's `dexec.sh` targeted `thornbots-runtime`. Probes cleared
host-overlay `AMENT_PREFIX_PATH`, `COLCON_PREFIX_PATH`, `PYTHONPATH`,
`CMAKE_PREFIX_PATH` and `LD_LIBRARY_PATH`, then sourced `/opt/ros/jazzy/setup.bash`
and `/workspaces/ros2_ws/install/local_setup.bash`, selecting the baked
`thornbots_pkg/config/fastdds_udp_only.xml` DDS profile. The first mixed-overlay
probe failed importing custom type support before sending anything.
Collector sources and command evidence are retained with the raw data.

Additional evidence:

- [Postboot panel summary](ssh://archlinux/home/blaise/sentry-deploy/2026-10-18/jetson-validation/20261018T194512Z-panel-postboot.json) and [decoded messages](ssh://archlinux/home/blaise/sentry-deploy/2026-10-18/jetson-validation/20261018T194512Z-panel-postboot.jsonl).
- [Same-Jetson header samples](ssh://archlinux/home/blaise/sentry-deploy/2026-10-18/jetson-validation/postboot-local/local-headers.jsonl) and [PING summary](ssh://archlinux/home/blaise/sentry-deploy/2026-10-18/jetson-validation/postboot-local/local-summary.json).
- [Processed topic/depth/latency summary](ssh://archlinux/home/blaise/sentry-deploy/2026-10-18/jetson-validation/processed-summary.json).
- [Health samples](ssh://archlinux/home/blaise/sentry-deploy/2026-10-18/jetson-validation/prepowerloss-health/health.jsonl) and [tegrastats](ssh://archlinux/home/blaise/sentry-deploy/2026-10-18/jetson-validation/prepowerloss-health/tegrastats.txt).
- [Postboot journal](ssh://archlinux/home/blaise/sentry-deploy/2026-10-18/jetson-validation/postboot-full-journal.txt).
- [Hand-push and stationary CSV](ssh://archlinux/home/blaise/sentry-deploy/2026-10-18/jetson-validation/motion-wifi/motion-20261018T195051Z.csv).

## Camera and YOLO

PASS below means the stated stream/load observation succeeded. It does not
mean zero loss or complete 60 fps raw color/depth acceptance.

| Baseline output | Messages / received span | Rate | Result |
| --- | --- | --- | --- |
| Compressed color | 3,858 / 64.781037 s | 59.539028 Hz | PASS: nominal 60 fps stream |
| Color camera info | 3,862 / 64.893946 s | 59.497075 Hz | PASS: present |
| Depth camera info | 3,845 / 64.780266 s | 59.339059 Hz | PASS: present |
| Color metadata | 3,859 / 64.825798 s | 59.513 Hz | WARN: 2 missing counter values |
| Depth metadata | 3,811 / 64.838591 s | 58.761 Hz | WARN: 50 missing counter values |
| YOLO arrays | 3,827 / 64.769027 s | 59.071445 Hz | PASS: output present |
| ROI arrays | 3,826 / 64.906452 s | 58.930967 Hz | Empty in baseline; target test below |

Compressed color had zero inferred missing capture intervals, max interval
16.843506 ms. Color metadata counters 127712→131572 missed 2 values;
depth 127709→131569 missed 50 across 11 gaps, maximum jump 10.
Camera-info inferred gaps: 5 color, 13 depth; YOLO: 31. These are observer
receipt gaps and do not independently establish physical sensor drops.

| Postboot same-Jetson raw subscriber | Messages / span | Delivered rate | Inferred missing capture intervals / max gap |
| --- | --- | --- | --- |
| `/color/image_raw` | 2,488 / 67.237830 s | 36.988106 Hz | 1,517 / 201.548584 ms |
| `/depth/image_rect_raw` | 2,936 / 67.190489 s | 43.681778 Hz | 1,065 / 134.394287 ms |
| `/detections_output` | 3,900 / 67.248913 s | 57.978632 Hz | 106 / 50.404297 ms |

**FAIL to demonstrate 60 fps raw delivery:** the raw observer received much
less than the concurrent compressed/inference streams. It subscribed to both
large images using Python, best-effort DDS and UDP; subscriber/transport
capacity is a plausible limitation. Do not label these counts sensor
hardware loss or conclude that the camera ran at 37 fps. Publisher-side
versus observer loss remains unresolved; depth 60 fps acceptance is open.
No nonpositive raw capture-stamp intervals occurred in this local sample.

PASS: the 38 MiB TensorRT engine loaded and initialized successfully from
`/workspaces/isaac_ros-dev/isaac_ros_assets/models/yolo11/yolo11s_fp16.plan`.
Python runtime version: **10.16.2.10**. WARN: startup explicitly warned about
using an engine plan across device models. No engine rebuild was performed.

| Capture header → robot receipt | Median | p95 | Max |
| --- | --- | --- | --- |
| Baseline compressed → Foxglove | 33.183116 ms | 43.936791 ms | 67.869669 ms |
| Baseline YOLO → Foxglove | 47.766905 ms | 51.435463 ms | 68.745709 ms |
| Postboot YOLO → local subscriber | 47.728457 ms | 53.687763 ms | 97.920755 ms |

These include driver/pipeline/receipt time; they are not isolated inference
benchmarks. Baseline archlinux YOLO receipt age was 229.310699 ms median;
postboot arch timestamps showed about 8 ms clock offset. Inter-host receipt
ages are not used as Jetson processing latency.

## Tracking and ROI depth

PASS for visible-panel detection, ROI depth availability and steady tracking.
The user supplied an illuminated panel but instructed continuing without a
measured distance. A saved image shows a blue illuminated “3” plate.
Baseline empty arrays preceded this confirmed-view capture and establish no
visibility bug.

Postboot 30 s capture: 1,759 selected-panel messages; depth median
**0.812209 m**, range **0.807420–0.823248 m**, p95 0.817603 m.
All **1,652/1,652 TargetState messages were valid**, with track ID 1 throughout.
Foxglove delivered measurement/state at 54.219932/55.415031 Hz; the longer
local observer delivered **57.875726/57.901478 Hz** (3,891/3,893 messages).
A physical target's apparent motion in `odom` cannot validate tracking
accuracy while the robot localization itself drifts.

| Capture → local receipt | Median | p95 | Max |
| --- | --- | --- | --- |
| `/cv/tracker/measurement` | 52.723511 ms | 74.722482 ms | 213.690701 ms |
| TargetState, nearest-measurement proxy | 52.844184 ms | 75.096011 ms | 213.959501 ms |

The tracker publishes TargetState then echoes the input capture header on
`/cv/tracker/measurement`. TargetState's own header is publication time,
not capture time. The proxy paired 3,878 states with the nearest measurement
receipt within 3 ms (median separation 0.173920 ms, p95 0.793312 ms).
There is no shared capture ID, so this is an estimate, not exact per-frame
association. State publication→receipt age alone was 1.098080 ms median,
2.563776 ms p95; it must not be presented as camera→state latency.
See the [tracker timestamp contract](../../thornbots_pkg/README.md#target_tracker).

Startup/serial interruption caused TF lookup drops: 192 dropped detections
in the first reported window; latest odom TF lag exceeded 0.4 s and eventually
1 s. Subsequent 5 s windows recovered without intervention: zero TF drops,
capture→update mean 50–57 ms. This transient is a warning, not a persistent
failure of steady tracking. **Depth accuracy at 1/2/4 m remains untested**.

## Lidar, localization and TF

| Baseline output | Messages / received span | Rate | Result |
| --- | --- | --- | --- |
| `/scan` | 720 / 64.626882 s | 11.125401 Hz | PASS: delivery |
| `/scan_odom` | 722 / 64.778843 s | 11.130177 Hz | PASS: rf2o output |
| `/localization/odom` | 1,948 / 64.899290 s | 30.000328 Hz | PASS: EKF output |

TF `map→nav_odom→odom→root` and URDF camera/lidar/muzzle links were present.
Median bridge ages: odom→root 4.527 ms, nav_odom→odom 14.205 ms.
map→nav_odom was future-dated about 0.864 s, consistent with SLAM's 1 s
transform tolerance; this alone is not a TF freshness bug.

The user hand-pushed approximately 1 m, then explicitly confirmed stationary
at the endpoint. No tape measurement, movement start/stop marks or heading
measurement were supplied. Wi-Fi SSH was confirmed with USB interfaces down;
all four streams continued recording to SSD. Approximate travel comparison
is contaminated by drift and is not a calibrated scale-accuracy test.

Stationary interval: **19:52:25.161–19:53:25.161 UTC**. First/last
received samples span slightly less than the full 60 s window:

| Output | Samples / observed span | Net reported motion while stationary | Accumulated XY path |
| --- | --- | --- | --- |
| `/odom` | 5,401 / 59.993988 s | **0.892820 m** | 0.897208 m |
| `/scan_odom` | 665 / 59.933380 s | **0.846473 m** | 4.418863 m |
| `/localization/odom` | 1,800 / 59.966903 s | **0.873380 m** | 0.880791 m |
| `/localization/map_odom` | 1,800 / 59.966425 s | **0.873380 m** | 0.880791 m |

These are first/last sample XY distances, not tape-measured robot movement.
The large rf2o accumulated path also shows jitter. The user confirmed no
physical movement during this interval. The approximate 1 m push cannot be
accepted as a scale comparison: no synchronized movement boundaries were
provided and the subsequent stationary drift is nearly that distance.
[Exact boundaries and positions](ssh://archlinux/home/blaise/sentry-deploy/2026-10-18/jetson-validation/motion-wifi/stationary-analysis.json)
are retained alongside the full CSV.

**FAIL: localization acceptance; experimental.** Large drift with the robot
confirmed stationary is an acceptance blocker. Old firmware frame/semantic
values remain untrusted; do not assign the fault specifically to EKF, rf2o,
firmware or frame conversion without isolating those inputs. The aim/navigation
frame split remains experimental. No localization or MCB behavior was changed.

## Serial, health and SSD recording

- PASS, receipt only: baseline POSE **89.982406 Hz**, REF_SYS **10.005503 Hz**.
  Their frames and semantics are untrusted with the unmatched old firmware.
- FAIL/WARN diagnostic link: 10 PINGs sent, 7 echoes, 3 unanswered within
  70 s. RTTs (ms), number order: 160=5.281248, 161=5.650496,
  165=3517.828960, 166=3014.874880, 167=2522.284736,
  168=2020.226176, 169=1520.774208; 162–164 unanswered.
  This establishes loss/delay at the observation boundary, not its root cause.
- PASS availability: complete baseline Foxglove capture; Wi-Fi SSH later
  worked through the team Tailscale daemon. Tailscale handshake now succeeds.
- PASS sampled health before battery loss: 16 tegrastats samples and 9 host
  samples over 16.039180 s. Mean utilization across 6 CPU cores median
  **37.5833%**; GPU **85–96%, median 88.5%**; RAM **2502–2520/7485 MiB**.
  CPU **66.250–66.937°C**; GPU **68.218–68.531°C**; input power
  **19.143–19.301 W**, median **19.222 W**. No thermal-limit acceptance
  is inferred from this short window.
- PASS SSD write observation: bag **4,816,122,073→4,849,627,353 bytes**,
  +33,505,280 bytes / 16.039180 s = **2,088,964.596 bytes/s (1.992 MiB/s)**.
  38 MCAP files at both endpoints; recorder uses 60 s splits. NVMe
  SHGP31-500GM, `/dev/nvme0n1p1`, ext4, nonrotating; available
  **219,429,081,088 bytes** at preflight. Recovered evidence survived the
  battery loss. Full interrupted-MCAP integrity/replay was not tested.
- No unexplained crash loop observed: preloss service/container restarts 0;
  postboot service restarts 1 due to the documented clock guard. Camera,
  YOLO, tracker, serial, lidar, localization and TF outputs were observed;
  direct docker-exec graph enumeration remains incomplete and is not used
  as proof that nodes are missing.

## Bugs and warnings

1. **Localization blocker:** stationary position drift quantified above.
   Approximate push cannot establish distance accuracy under this drift.
2. **Serial diagnostic blocker:** 3/10 PINGs unanswered; five echoes delayed
   1.5–3.5 s. Recurring `NO DATA ... ~1000 ms` warnings approximately every
   180 s coincide with rf2o missing odom-at-scan-time/constant-velocity-prior
   fallback. Correlation is not a diagnosis; firmware is unmatched.
3. **Camera delivery unresolved:** raw observer rates below 60 fps, metadata
   gaps and repeated RealSense libusb EAGAIN warnings. Transport/subscriber
   loss versus source/pipeline loss needs isolation.
4. **Engine portability:** TensorRT cross-device-model warning despite
   successful load. Validate/rebuild for this Jetson before performance
   acceptance if required by the owning model workflow.
5. Transient TF drops after restart/serial gap recovered. One preboot CRC8
   mismatch at 19:31:04 (CRC8=1, CRC16=0); duplicate rf2o logger name and
   Foxglove TensorList schema warning remain. Standard tested topics worked.
6. Postboot SLAM serialization logged variable lidar range counts (for
   example 359 readings, expected 500). Impact on saved-map integrity is
   untested; retain the journal and verify reload before map acceptance.

## Sim-to-real differences and promotion

- Hardware provides ~59.53 fps rather than an exact simulated 60 Hz; raw
  DDS observer delivery, USB warnings and real depth validity need separate
  acceptance. No comparable Humble hardware FPS/latency baseline exists here.
- Physical stationary drift and real UART stalls are not covered by a sim
  fixture's idealized odometry/serial timing. Hardware localization failed
  this check even though its topics and TF chain were present.
- A visible real armor plate produced depth and a stable valid track, but
  simulated geometry does not validate calibrated depth or physical aiming.
- Cold boot without valid clock led to a deliberate clock-guard restart;
  battery exhaustion and USB disconnection were physical interruptions.
- Hosted firmware fixtures cannot establish controller-loss behavior.
  Controller/MCB behavior, aiming, firing and flashing were excluded.

**Promotion: no-go from this record.** Localization drift, serial diagnostic
loss/delay, unresolved raw-depth delivery, calibrated depth and matched-firmware
acceptance remain open. The user's promotion decision is separate. No main
merge was performed by this investigation.
