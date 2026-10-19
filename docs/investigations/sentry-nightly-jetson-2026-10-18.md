# Sentry nightly Jetson checks — 2026-10-18

The initial run observed the already-running Jetson stack without firmware
changes, controller use or actuation. Later explicitly authorized firmware
flashes and follow-ups are recorded below. This is partial hardware evidence,
not acceptance of aiming, firing or controller interlocks.

## Configuration and evidence

Initial workspace: `4f9e73a945c99292eaa869d4c38d44dc2b991d1e` (`nightly`, clean
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
MCB. During the initial run the MCB ran its previous firmware; its exact flashed
revision was unknown. Initial POSE/REF_SYS frame and semantic values remain
untrusted. The follow-up below identifies the subsequently flashed build.
No controller-on tests were performed.

Raw evidence is on archlinux at
`/home/blaise/sentry-deploy/2026-10-18/jetson-validation/`:

- [Preflight and startup log extracts](#a1-preflight-and-startup-log-extracts).
- [65-second topic summary and schemas](#a2-baseline-topic-summary-65-s).
- [Per-message timestamps, metadata, positions and TF](#a3-baseline-per-message-log).
- [Collector source](#a4-collector-observe-script).
- [USB disconnect evidence](#a5-usb-disconnect).

The [Appendix](#appendix-evidence) inlines the evidence cited below. Raw payload images were not streamed for the baseline;
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
  nano-sentry@ts-nano-sentry 'systemctl show thornbots -p ActiveState -p NRestarts'
```

The Docker skill's `dexec.sh` targeted `thornbots-runtime`. Probes cleared
host-overlay `AMENT_PREFIX_PATH`, `COLCON_PREFIX_PATH`, `PYTHONPATH`,
`CMAKE_PREFIX_PATH` and `LD_LIBRARY_PATH`, then sourced `/opt/ros/jazzy/setup.bash`
and `/workspaces/ros2_ws/install/local_setup.bash`, selecting the baked
`thornbots_pkg/config/fastdds_udp_only.xml` DDS profile. The first mixed-overlay
probe failed importing custom type support before sending anything.
Collector sources and command evidence are retained with the raw data.

Additional evidence:

- [Postboot panel summary](#a6-postboot-panel-capture) and [decoded messages](#a6-postboot-panel-capture).
- [Same-Jetson header samples](#a7-same-jetson-header-samples-and-ping-summary) and [PING summary](#a7-same-jetson-header-samples-and-ping-summary).
- [Processed topic/depth/latency summary](#a8-processed-summary).
- [Health samples](#a9-health-samples-and-tegrastats) and [tegrastats](#a9-health-samples-and-tegrastats).
- [Postboot journal](#a10-postboot-journal).
- [Hand-push and stationary CSV](#a11-hand-push-and-stationary-csv).

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
capture→update mean 50–57 ms. A second serial gap at 19:47:40 UTC repeated
the pattern (34 and 191 drops in two windows, then zero; see
[A10](#a10-postboot-journal)). This transient is a warning, not a persistent
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
[Exact boundaries and positions](#a12-stationary-analysis)
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

## Initial bugs and warnings

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

## Initial sim-to-real differences and promotion

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
  Controller/MCB behavior, aiming, firing and flashing were excluded from
  the initial observation; later flashes are recorded below.

**Initial promotion assessment: no-go.** Localization drift, serial diagnostic
loss/delay, unresolved raw-depth delivery, calibrated depth and matched-firmware
acceptance remain open. The user's promotion decision is separate. No main
merge was performed by this investigation.

## Authorized firmware follow-up — 20:10 UTC onward

The user explicitly authorized the parked-hold fix build from
[MCBV3 PR #97](https://github.com/Thornbots/MCBV3/pull/97), commit
**`276e99e0144472d7225f8e0a39776d9749dd7f66`**, instead of raw nightly
`3f14d5b`. No fallback artifact was used and no firmware source was changed.
For this first flash the Jetson image/workspace stayed at the revisions above;
the running localization stack was not reset around the MCB flash, so its previous state
and absolute offsets persisted. Compare increments, not absolute positions.

### Physical setup, backup and build

The user confirmed controller OFF and staying off; wheels raised or chassis
chocked; flywheel/indexer/gimbal clear. Motor/main power **remained on**.
The connected probe was Horco CMSIS-DAP, VID:PID `faed:4870`, firmware v0.2,
not ST-Link. A deployment-only copy of `isolated-deploy/openocd.cfg` selected
`interface/cmsis-dap.cfg` and `transport select swd`; the repository source
configuration was untouched. OpenOCD identified Cortex-M4, device
`0x10076413`, 1024 KiB flash. It reported SWD at 2000 kHz.

The pre-flash full backup is retained at:

`/home/blaise/sentry-deploy/2026-10-18/firmware/mcb-before-276e99e-20261018.bin`

Size: **1,048,576 bytes**. SHA-256:
`3c2d8280bf2452d49dbda52fdf02445ce7447674135cd6669f96ea4399a398d9`.
The saved `backup.log` ends after a halt-state warning and does not document
successful dump/verify; the retained binary's size and checksum were checked.
No new full backup was taken for either later flash.

The initial build attempts failed on removed `telnetlib` and an RWX
LOAD-segment warning. The successful build selected CI's Ubuntu linker;
its build log and deployment-only OpenOCD config are retained beside the ELF.

The flash began **20:10:51 UTC**. OpenOCD logged **Programming Finished**
and **Verified OK**, then the deployment procedure issued `reset run`.
ELF:

`/home/blaise/sentry-deploy/2026-10-18/firmware/hold-fix-276e99e/MCB-project.elf`

SHA-256:
**`281ad265e459817d7ac3072896f59f2316d8dc347a5e1fb82c075137d5b67ce2`**.

[Backup log](#a13-hold-fix-firmware-276e99e-backup-build-and-flash),
[successful build log](#a13-hold-fix-firmware-276e99e-backup-build-and-flash),
[flash/verify log](#a13-hold-fix-firmware-276e99e-backup-build-and-flash)
and the exact deployment config are retained beside the ELF.

The user reported **“motors are all still off”** after reboot. No motion was
reported and the controller remained off. Motor current was not independently
instrumented; this is a physical observation, not proof of zero CAN current
words. Disconnect/reconnect interlock acceptance remains outside this
controller-off run.

### Serial after flash

PASS for the short diagnostic exchange: **10/10 PINGs** returned in
**3.877120–10.808032 ms**, median **8.129328 ms**; none unanswered in the
25.006 s sample. POSE and REF_SYS continued flowing.

The subsequent two-minute sample received POSE at **87.006148 Hz** and
REF_SYS at **9.668519 Hz**, including a serial interruption. Maximum receipt
gaps were **4.008811 s** for POSE and **4.088794 s** for REF_SYS.
At **20:14:09 UTC**
the journal again logged `NO DATA ... ~1000 ms` and rf2o's missing odom-at-scan
prior fallback. Therefore the initial good PING exchange does **not** close
the intermittent serial-stability finding. Frame wiring/calibration accuracy
is still unaccepted despite the known firmware revision.

### Stationary chassis with moving people: graded stability result

The robot was confirmed physically stationary while people moved nearby.
**Raw MCB `/odom`: PASS**, exactly still over the 120 s analysis window.
**rf2o/EKF/map stability in a dynamic scene: FAIL. Distance accuracy: UNTESTED.**
The user skipped the clean stationary rerun and tape-measured push; neither
is claimed here. The changing estimates below are software motion, with no
reported chassis movement.

Analysis uses a common 120 s interval beginning **20:12:28.719 UTC**, with
per-topic received spans below. Moving people are part of this stability
result; the data do not establish clean-scene drift or its cause.

| Output | Messages / received span | Rate | Net reported displacement |
| --- | --- | --- | --- |
| `/odom` | 10,441 / 119.990248 s | 87.007071 Hz | **0.000000 m** |
| `/scan_odom` | 1,335 / 119.867650 s | 11.128941 Hz | **2.065879 m** |
| `/localization/odom` | 3,524 / 119.967848 s | 29.366202 Hz | **2.022134 m** |
| `/localization/map_odom` | 3,525 / 119.995610 s | 29.367741 Hz | **2.022808 m** |

POSE stayed at `(-4.625, 0)` m, `odom_status=ODOM_PODS` for all 10,440
samples. Accumulated XY paths were 0 m raw, 9.484391 m rf2o and about
2.300 m EKF/map. Moving people can confound scan matching; robust
rejection/uncertainty handling remains open. The stability failure does not
assign a root cause or establish physical distance accuracy.
The old-firmware initial drift result above is a separate historical window;
its lidar-scene control was not independently documented.

Decoded `/scan_odom/quality` (1,336 messages, 11.130078 Hz):

| Grade / reason | Count |
| --- | --- |
| good | 976 (73.05%) |
| degraded total | 360 (26.95%) |
| degraded: valid_fraction | 315 |
| degraded: valid_fraction,sigma | 2 |
| degraded: extrinsic_stale | 27 |
| degraded: valid_fraction,extrinsic_stale | 16 |
| failed | 0 |

All 1,336 reported `applied=true`, `increment=scan`; 43 flagged stale
extrinsics. Valid-point fraction min/median/max: **0.432787 / 0.527869 /
0.568852**. Reported speed median **0.062480 m/s**, p95 **0.277872 m/s**,
max **0.754533 m/s**. Quality was mostly good despite aggregate false motion;
its internal match grade is not ground-truth position confidence.

### Confirmed SLAM beam-count rejection / sim-to-real gap

Still present after flash: repeated
`LaserRangeScan contains 356 range readings, expected 580` (also 343–359
in the journal). The observer received **1,335 scans with 340–361 beams**;
none had 580. Angular increments also varied **0.017152745–0.017601019 rad**.

In [Karto 2.8.5 LaserRangeFinder::Validate](https://github.com/SteveMacenski/slam_toolbox/blob/2.8.5/lib/karto_sdk/src/Karto.cpp#L209),
the exact message is followed by `return false` when the incoming count
differs from the registered sensor count. Thus these are rejected scans,
not harmless log noise. Logs alone do not quantify all rejected scans or
prove no map updates occurred. Fixed-beam simulated scans do not exercise
this variable-count hardware registration problem. Normalize/validate scan
geometry or sensor registration in a separate change, then verify map updates
and saved-map reload on hardware. The suspected cause is `angle_compensate`
being false in `thornbots_pkg/launch/auto.launch.py`; that setting is under
test. SLAM scan rejection remains open in this record.

[Full post-flash journal](#a14-post-flash-journal),
[decoded raw messages](#a15-post-flash-raw-messages-stationary-run),
[diagnostic PING results](#a16-post-flash-diagnostic-ping-results)
and [processed measurements](#a17-post-flash-processed-measurements)
are retained with the collector and analysis sources. The saved analysis's
`NOT SCORED` verdict predates the delegating agent's revised grades above;
its measurements are retained unchanged. The finite observers
exited; the original stack remained active with `NRestarts=1` (the earlier
clock-guard restart), and no manual stack restart was performed.

## Later firmware flashes and controller-off checks

[MCBV3 #97](https://github.com/Thornbots/MCBV3/pull/97) and
[workspace #63](https://github.com/Thornbots/thornbots_workspace/pull/63)
are closed as superseded by [MCBV3 #98](https://github.com/Thornbots/MCBV3/pull/98).
The first flash above remains part of today's history. The replacement
restores main's parked hold: main's controller-on hold is the behavior already
confirmed on the real robot, per the delegating agent's verified report.
Today's follow-ups kept the controller off and do not repeat that acceptance.

Both later ELFs were programmed and verified with OpenOCD via CMSIS-DAP;
each `flash.log` records **Programming Finished** and **Verified OK**.

| Flash start (UTC) | MCBV3 source commit | ELF SHA-256 |
| --- | --- | --- |
| 20:59:02 | `412d10268844e50834c0ae368a3721397d38fd8f` | `45c2efd8663a07b2e2c5a1e6d949cd74ded3c35630ff44de414e71a26715fac1` |
| 21:17:59 | `0e421d8484f44644f133979b3d6745c4e943053a` (#98 head) | `60490d955e543e7cea6a087a2fda8b634b6063672185f10a0d4c645c6f19555e` |

At `0e421d8`, sentry drivetrain and controls match main exactly, as described
in #98. Source IDs, timestamps, checksums and flash logs are retained in
[restore-main-412d102](#a18-restore-main-and-main-only-firmware-flashes)
and [main-only-0e421d8](#a18-restore-main-and-main-only-firmware-flashes).
The former's `backup.log` records a failed CMSIS-DAP probe attempt, not a new
backup; the pre-first-flash binary above remains the full backup.

The delegating agent verified that after each flash bridge POSE resumed at
about **90 Hz** following an approximately **15 s** reset gap. Separate saved
raw `/odom` captures confirm exactly constant x **−4.625 m**, y **0 m**, yaw
**0 rad** and zero twist, with the controller off:

| Firmware | Samples | Header-stamp span | Result / evidence |
| --- | --- | --- | --- |
| `412d102` | 2,000 | 22.267073 s | PASS: still; [CSV](#a19-raw-odom-after-412d102) |
| `0e421d8` | 3,000 | 33.316804 s | PASS: still; [CSV](#a20-raw-odom-after-0e421d8) |

These short raw-odom checks do not regrade rf2o/EKF/map or measure distance
accuracy. Controller-on, aiming and firing tests were not performed here.

## Robot workspace and full build follow-up

Per the delegating agent's verified report, the robot source workspace was
updated to nightly **`6f7a166`**; `sim` and `firmware/MCBV3` were deinited and
marked inactive on the Jetson. A full workspace build in a throwaway
container from the robot image passed **19/19 packages**, **`BUILD_RC=0`**, in
about **8 min**. Only vendored sllidar SDK warnings and GCC psabi notes were
reported. These build and deployment details are attributed to that report;
the local evidence set does not contain their build log.

The image remains the initial **`sha-4f9e73a…`** image identified above: pulling
the `6f7a166` image failed because the robot had no ghcr login. The workspace
diff from `4f9e73a` to `6f7a166` contains CHANGELOG documentation and an
`isaac_ros_common` pin update whose package diff changes only README files;
the effective change is docs-only. A successful source build does not imply
that a new runtime image was installed.

## Remaining acceptance

Flash/verify, the short diagnostic PING exchange and raw-odom stillness passed.
Dynamic-scene rf2o/EKF/map stability failed; physical distance accuracy remains
untested. SLAM scan rejection, rf2o/EKF stationary drift and intermittent
POSE/REF_SYS gaps remain open. See [ROADMAP](../ROADMAP.md) for ongoing work.
Raw image delivery and calibrated depth also remain unresolved. This record
does not establish promotion readiness. No main merge was performed here.

## Appendix: evidence

The evidence behind this record is inlined here because the original files
live only on archlinux. Each entry gives the production method, the original
path (plain text, not a link) and the numbers the sections above cite. Large
raw files are summarized by row counts, time spans and the statistics used.
The summaries were computed with throwaway scripts kept outside the repo.
Journals use the Jetson's local time (EDT, UTC−4): 15:37 EDT = 19:37 UTC.
Original paths are relative to `archlinux:~/sentry-deploy/2026-10-18/`.
Identifiers of personal devices, Wi-Fi details and other hosts are omitted.

### A1. Preflight and startup log extracts

`jetson-validation/preflight.txt` (189 lines). Captured on
`ts-nano-sentry` at 19:37:28 UTC just before the baseline, plus journal
extracts from the running stack. It records:

| Item | Value |
| --- | --- |
| L4T | R39 (release), revision 2.1, kernel `6.8.12-1021-tegra` |
| Power mode | `MAXN_SUPER` |
| Clock | `NTPSynchronized=yes` |
| Workspace | `4f9e73a945c99292eaa869d4c38d44dc2b991d1e` (package pins match the table above) |
| Service | `ActiveState=active`, `NRestarts=0`, container `thornbots-runtime` up 37 min |
| Image | `ghcr.io/thornbots/isaac-ros:sha-4f9e73a…-arm64-jetpack`, ID `sha256:aef7f2d8…`, `layers=42 bytes=36786722123 architecture=arm64` |
| Disk | `/dev/nvme0n1p1` ext4, 489,529,253,888 B, 219,429,081,088 B available (53% used); NVMe `SHGP31-500GM` |

Warnings cited above (journal lines, EDT):

```text
[ 1698.945 15:00:20.778?] [rf2o_laser_odometry_node-13] [WARN] … Publisher already registered for node name: 'rf2o_laser_odometry'. …
[ 1700.719 15:00:22.553?] [component_container_mt-1] [WARN] … [TRT]: TRT WARNING: Using an engine plan file across different models of devices is not supported and is likely to affect performance or even cause errors or deadlock.
[ 3542.212 15:31:04.045?] [dji_serial_bridge_node-1] [WARN] … CRC8 mismatch (seq=0, got=0x07 expected=0x5c) — dropping byte
```

`NO DATA from MCB for ~1000 ms` appears 12 times in this file, at 3-minute
steps (15:01:56, 15:04:56, 15:07:56, 15:10:56, 15:13:56 EDT, …), each next to
an rf2o `No /odom pose at both scan stamps (…)` warning. The RX counter line
for the CRC8 event was not located in the retained text.

### A2. Baseline topic summary (65 s)

`jetson-validation/20261018T193615Z-baseline.json` (180 KB). Written by
`observe_jetson.py` ([A4](#a4-collector-observe-script)) at 19:36:15 UTC with
`--duration 65 --label baseline`: `duration_s` 65.166, Foxglove
`ws://192.168.55.1:8765`, no decode errors, empty connection graph. Rate is
`(N−1)/received span`. Header age is bridge or archlinux receipt time minus the
header stamp. "Missing" is the sum of `round(interval/16.667 ms)−1`.

| Topic | Messages | Span (s) | Rate (Hz) | Max header interval (ms) | Missing 60 fps intervals | Bridge age p50 / p95 / max (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| `/color/image_raw/compressed` | 3,858 | 64.781037 | 59.539028 | 16.843506 | 0 | 33.183 / 43.937 / 67.870 |
| `/color/camera_info` | 3,862 | 64.893946 | 59.497075 | 50.393555 | 5 | 29.199 / 31.192 / 44.201 |
| `/depth/camera_info` | 3,845 | 64.780266 | 59.339059 | 134.376953 | 13 | 9.195 / 10.250 / 22.277 |
| `/camera/color/metadata` | 3,859 | 64.825798 | 59.513344 | 50.393554 | 2 | 29.316 / 31.316 / 44.222 |
| `/camera/depth/metadata` | 3,811 | 64.838591 | 58.761302 | 167.967774 | 50 | 9.292 / 10.401 / 22.696 |
| `/detections_output` (YOLO) | 3,827 | 64.769027 | 59.071445 | 134.378663 | 31 | 47.767 / 51.435 / 68.746 |
| `/cv/panel_detections` (ROI) | 3,826 | 64.906452 | 58.930967 | 168.030274 | n/a | 48.131 / 52.001 / 68.729 |
| `/scan` | 720 | 64.626882 | 11.125401 | 98.323601 | n/a | 88.557 / 96.961 / 99.471 |
| `/scan_odom` | 722 | 64.778843 | 11.130177 | 98.323601 | n/a | 89.543 / 98.041 / 115.211 |
| `/localization/odom` | 1,948 | 64.899290 | 30.000328 | 42.553442 | n/a | 13.389 / 19.882 / 41.563 |
| `/odom` | 5,840 | 64.923211 | 89.937018 | 44.549671 | n/a | 3.976 / 5.336 / 12.042 |
| `/dji_serial_bridge/pose` | 5,836 | 64.846010 | 89.982406 | 48.050423 | n/a | 3.387 / 4.143 / 10.767 |
| `/dji_serial_bridge/ref_sys` | 649 | 64.764360 | 10.005503 | 103.520747 | n/a | 2.355 / 3.352 / 31.674 |

Archlinux receipt age p50: compressed color 214.479 ms, YOLO 229.311 ms,
ROI 229.494 ms, `/odom` 184.730 ms. Zero nonpositive stamp intervals on
the image topics. `/cv/target_state` and `/cv/tracker/measurement` had no
messages in this window (no target in view); no stamped topic had a decode
error.

### A3. Baseline per-message log

`jetson-validation/20261018T193615Z-baseline.jsonl` (20 MB, 64,115 rows),
the raw record behind A2. Each row is one decoded message with
`receipt_ns`, `bridge_ns`, `header_ns`, small payload fields, positions, or
TF transforms. Receipt span 64.953592 s. Rows per topic match A2, plus
`/tf` 12,158, `/tf_static` 2, `/localization/map_odom` 1,945,
`/localization/ekf_input` 5,835, `/scan_raw` 721, `/scan_odom/quality` 721,
`/diagnostics` 129.

TF bridge-receipt age (bridge time minus transform header; negative means
future-dated):

| Transform | Count | Median (ms) | Min / max (ms) |
| --- | --- | --- | --- |
| `odom`→`root` | 5,838 | 4.527 | 3.698 / 41.824 |
| `nav_odom`→`odom` | 1,946 | 14.203 | 5.392 / 41.943 |
| `map`→`nav_odom` | 3,243 | −863.696 | −911.807 / −809.931 |

The doc's 14.205 ms for `nav_odom`→`odom` differs from this recomputed
14.203 ms by 2 µs. Static TF contains `armor_0–3`, `camera`, camera color/depth
(optical) frames, `carrier_0–3`, `lidar`, `muzzle` and `wheel_0–3`.

Camera metadata frame counters (all 3,859 / 3,811 messages):

| Stream | First → last counter | Missed values | Gaps | Largest jump |
| --- | --- | --- | --- | --- |
| Color | 127712 → 131572 | 2 | 1 | 3 |
| Depth | 127709 → 131569 | 50 | 11 | 10 |

All 3,826 `/cv/panel_detections` rows had `panels: []`. Example rows:

```json
{"topic": "/odom", "receipt_ns": 1792352176118758020, "bridge_ns": 1792352175786203449, "bytes": 716, "header_ns": 1792352175782152638, "frame_id": "odom", "child": "root", "position": [2.236967086791992, -3.8223001956939697, 0.0], "orientation": [0.0, 0.0, 0.0, 1.0]}
{"topic": "/cv/panel_detections", "receipt_ns": …, "header_ns": 1792352175747545410, "frame_id": "camera", "panels": []}
```

### A4. Collector (observe script)

`jetson-validation/observe_jetson.py` (179 lines of Python,
`asyncio` and `websockets`). It connects to the Jetson's Foxglove bridge with
subprotocol `foxglove.sdk.v1`, subscribes to 24 topics (camera info and
metadata, compressed color, YOLO, ROI/panel/target/tracker topics, `/scan*`,
`/odom`, `/localization/*`, `/tf`, `/tf_static`, POSE, REF_SYS,
`/diagnostics`) and decodes the CDR payload of small messages in-process.
Images are not decoded or stored: only header stamps and byte counts. For each
message it writes `receipt_ns` (archlinux), `bridge_ns` (bridge clock) and
`header_ns`, then a JSON summary with per-topic count, received span,
rate, header-interval and age percentiles, nonpositive intervals, estimated
60 fps gaps and net/maximum displacement for odometry topics.

```bash
python observe_jetson.py --duration 65 --label baseline     # → <ts>-baseline.json/.jsonl
python observe_jetson.py --duration 30 --label panel-postboot
# options: --url ws://192.168.55.1:8765  --out <dir>
```

Companion scripts used later (same directory) are `local_observer.py` and
`health_observer.py` (on the Jetson), `motion_observer.py`, `postflash_observer.py`
and the analysis scripts `analyze_evidence.py` and `analyze_postflash.py`.

### A5. USB disconnect

`jetson-validation/connectivity-loss.txt`, captured on archlinux at
19:40:58 UTC after the Jetson disappeared. Kernel log excerpt (EDT):

```text
Oct 18 15:37:46 archlinux kernel: usb 3-3: USB disconnect, device number 20
Oct 18 15:37:46 archlinux kernel: cdc_ncm 3-3:1.5 enp0s20f0u3i5: unregister 'cdc_ncm' usb-0000:00:14.0-3, CDC NCM (NO ZLP)
```

15:37:46 EDT is 19:37:46 UTC. The same capture shows the USB-network
link gone (the route to the Jetson's USB address `192.168.55.1` resolving via
the laptop's Wi-Fi) and the Tailscale peer list showing `ts-nano-sentry` as
`offline, last seen 1m ago`. The user confirmed the battery died.

### A6. Postboot panel capture

`jetson-validation/20261018T194512Z-panel-postboot.json` (184 KB) and
`…-panel-postboot.jsonl` (14 MB, 36,156 rows). Produced by
`observe_jetson.py --duration 30 --label panel-postboot` starting 19:45:12
UTC (`duration_s` 30.088) with the illuminated panel in view.

| Topic | Messages | Span (s) | Rate (Hz) |
| --- | --- | --- | --- |
| `/cv/panel_detection` (selected panel) | 1,759 | 29.822670 | 58.948445 |
| `/cv/panel_detections` | 1,712 | 29.748096 | 57.516286 |
| `/cv/robot_panels` | 1,761 | 29.825160 | 59.010579 |
| `/cv/tracker/measurement` | 1,612 | 29.712321 | 54.219932 |
| `/cv/target_state` | 1,652 | 29.793361 | 55.415031 |
| `/detections_output` | 1,735 | 29.927185 | 57.940631 |
| `/color/image_raw/compressed` | 1,775 | 29.810292 | 59.509648 |
| `/dji_serial_bridge/pose` | 2,691 | 29.925715 | 89.889247 |
| `/dji_serial_bridge/ref_sys` | 298 | 29.698349 | 10.000556 |
| `/scan` | 329 | 29.694245 | 11.045911 |
| `/localization/odom` | 892 | 29.699902 | 30.000099 |

The panel depth, tracking validity and track ID statistics derived from
these rows are in [A8](#a8-processed-summary). The saved panel image
(`panel-view.jpg`) shows a blue illuminated “3” plate. An earlier 19:38 and a
19:44 capture (`…193849Z-panel-current.jsonl`, `…194415Z-panel-postboot.jsonl`)
are empty, 0 bytes, and are not used.

### A7. Same-Jetson header samples and PING summary

`jetson-validation/postboot-local/local-headers.jsonl` (17,108 rows) and
`local-summary.json`. Produced by `local_observer.py`, run inside the
`thornbots-runtime` container on the Jetson (raw DDS subscribers, Python,
best-effort QoS, UDP-only FastDDS profile) for 70.008 s after the postboot
restart. Rows hold only `topic`, `receipt_ns`, `header_ns` and `bytes`:

```json
{"topic": "/detections_output", "receipt_ns": 1792352722020185986, "header_ns": 1792352721945203613, "bytes": 500}
{"topic": "/color/image_raw", "receipt_ns": 1792352722030645218, "header_ns": 1792352721978802002, "bytes": 921672}
```

Summary: 10 PINGs sent, 7 echoed, 3 unanswered (162–164).

| PING | RTT (ms) |
| --- | --- |
| 160 | 5.281248 |
| 161 | 5.650496 |
| 165 | 3517.828960 |
| 166 | 3014.874880 |
| 167 | 2522.284736 |
| 168 | 2020.226176 |
| 169 | 1520.774208 |

Message counts and received spans (also in [A8](#a8-processed-summary)):

| Topic | Messages | Span (s) |
| --- | --- | --- |
| `/color/image_raw` | 2,488 | 67.237830 |
| `/depth/image_rect_raw` | 2,936 | 67.190489 |
| `/detections_output` | 3,900 | 67.248913 |
| `/cv/tracker/measurement` | 3,891 | 67.212980 |
| `/cv/target_state` | 3,893 | 67.217628 |

### A8. Processed summary

`jetson-validation/processed-summary.json`, computed offline from A6 and A7
(analysis script retained as `analyze_evidence.py`). "Capture age" is local receipt time minus header
stamp. Missing intervals are inferred from header spacing at 60 fps.

| Same-Jetson topic | Messages | Rate (Hz) | Capture age min / median / p95 / max (ms) | Max stamp interval (ms) | Inferred missing |
| --- | --- | --- | --- | --- | --- |
| `/color/image_raw` | 2,488 | 36.988106 | 18.826 / 29.629 / 32.191 / 63.108 | 201.548584 | 1,517 |
| `/depth/image_rect_raw` | 2,936 | 43.681778 | 8.061 / 10.204 / 12.327 / 26.785 | 134.394287 | 1,065 |
| `/detections_output` | 3,900 | 57.978632 | 40.042 / 47.728 / 53.688 / 97.921 | 50.404297 | 106 |
| `/cv/tracker/measurement` | 3,891 | 57.875726 | 44.844 / 52.724 / 74.722 / 213.691 | 83.989746 | 114 |
| `/cv/target_state` | 3,893 | 57.901478 | 0.316 / 1.098 / 2.564 / 9.676 | 156.488896 | n/a |

All five topics had zero nonpositive stamp intervals.

| Derived quantity | n | Min | Median | p95 | Max |
| --- | --- | --- | --- | --- | --- |
| TargetState capture-age proxy (ms) | 3,878 | 42.851 | 52.844 | 75.096 | 213.960 |
| Pairing receipt gap (ms) | 3,878 | 0.079 | 0.174 | 0.793 | 2.990 |
| Selected-panel depth (m) | 1,759 | 0.807420 | 0.812209 | 0.817603 | 0.823248 |

Tracking: 1,652 TargetState messages, 1,652 valid, track ID 1 for all 1,652.
The proxy pairs each TargetState with the nearest measurement receipt within
3 ms.

### A9. Health samples and tegrastats

`jetson-validation/prepowerloss-health/health.jsonl` (9 rows) and
`tegrastats.txt` (16 lines). Produced on the Jetson at 19:37:29–19:37:45
UTC by `health_observer.py`: `tegrastats --interval 1000` plus, every 2 s, the
bag directory size, MCAP file count, `/proc/stat`, `/proc/meminfo` and thermal
zones. Recorder: `/home/nano-sentry/logs/thornbots-run00112/bag`.

| Quantity | Samples | Min | Median | Max |
| --- | --- | --- | --- | --- |
| Mean CPU over 6 cores (%) | 16 | 34.167 | 37.583 | 42.167 |
| GPU `GR3D_FREQ` (%) | 16 | 85 | 88.5 | 96 |
| RAM used (MiB of 7485) | 16 | 2502 | 2506.5 | 2520 |
| CPU temperature (°C) | 16 | 66.250 | 66.547 | 66.937 |
| GPU temperature (°C) | 16 | 68.218 | 68.375 | 68.531 |
| `VDD_IN` (mW) | 16 | 19143 | 19222 | 19301 |

Bag size: 4,816,122,073 B at 19:37:29.438 UTC → 4,849,627,353 B at
19:37:45.477 UTC, +33,505,280 B in 16.039180 s = 2,088,964.596 B/s
(1.992 MiB/s); 38 MCAP files at both ends. First tegrastats line:

```text
10-18-2026 15:37:30 RAM 2520/7485MB (lfb 1x256kB) CPU [42%@1728,39%@1728,38%@1728,43%@1728,36%@1728,36%@1728] GR3D_FREQ 88% cpu@66.468C/66.468C … gpu@68.468C/68.468C tj@68.468C/68.468C … VDD_IN 19301mW/19301mW/19301mW …
```

### A10. Postboot journal

`jetson-validation/postboot-full-journal.txt` (4,927 lines), 15:37:35–15:48:29
EDT (19:37:35–19:48:29 UTC), the `thornbots` service journal from `ts-nano-sentry`
after recovery. Clock recovery and restart:

```text
15:37:35 [clock] NTP not synced: wall times marked ? until it is
15:44:15 [clock] NTP synced, wall 2026-10-18 15:44:15 EDT (stepped +293.4 s)
15:44:15 [clock] wall clock stepped +293.4 s; restarting the stack
15:44:20 systemd[1]: thornbots.service: Main process exited, code=exited, status=75/TEMPFAIL
15:44:25 systemd[1]: thornbots.service: Scheduled restart job, restart counter is at 1.
15:44:26 [clock] NTP not synced: wall times marked ? until it is
```

Other cited lines (EDT):

```text
15:44:31 [component_container_mt-1] [WARN] [TRT]: TRT WARNING: Using an engine plan file across different models of devices is not supported …
15:44:31 [foxglove_bridge]: no .msg definition for isaac_ros_tensor_list_interfaces/msg/TensorList, falling back to IDL
15:44:39 … (messenger-libusb.cpp:42) control_transfer returned error, index: 768, error: Resource temporarily unavailable
15:44:40 [dji_serial_bridge_node-1] [WARN] read_loop: NO DATA from MCB for ~1000 ms (poll_ms=10 × 100 polls). …
15:44:40 [target_tracker-4] [ERROR] TF odom<-camera at capture 1792352680.030 unavailable after 0.251 s (tf_max_wait_s=0.25) -- dropping …
15:44:15 [async_slam_toolbox_node-16] LaserRangeScan contains 359 range readings, expected 500
```

Counts in this file: 14 libusb control-transfer warnings, 4 `expected 500`
SLAM warnings (359–364 readings), 2 `NO DATA` lines (15:44:40 and 15:47:40 EDT).
Target tracker 5 s windows (`camera TF wait … dropped N; capture to update mean`),
67 windows, those with drops:

| Window end (EDT) | Detections timed | Dropped | Capture→update mean (s) / max (s) |
| --- | --- | --- | --- |
| 15:44:40 | 0 | 1 | 0.000 / 0.000 |
| 15:44:45 | 117 | 192 | 0.064 / 0.281 |
| 15:47:40 | 250 | 34 | 0.050 / 0.086 |
| 15:47:45 | 122 | 191 | 0.063 / 0.277 |

All other windows reported `dropped 0` with capture→update mean 0.048–0.056 s.
The 15:44:15 window logged TF unavailable after 293.403 s: the +293.4 s clock
step. The 15:47:40 drops follow the second `NO DATA` gap and also cleared
within one further window. Earlier-run `NO DATA` lines (preboot, A1) recur
every 3 minutes.

### A11. Hand-push and stationary CSV

`jetson-validation/motion-wifi/motion-20261018T195051Z.csv` (40,572 rows,
5.2 MB) with `motion-20261018T195051Z.json`. Columns
`receipt_ns,topic,stamp_ns,frame,child,x,y,z,qx,qy,qz,qw`. Produced on the
Jetson by `motion_observer.py` (detached, writing to SSD) starting 19:50:51
UTC; it kept recording while USB networking was down and the operator used
Wi-Fi. Total `duration_s` 255.230 s.

| Topic | Rows | Receipt span (s) | First XY (m) | Last XY (m) | First→last straight line (m) |
| --- | --- | --- | --- | --- | --- |
| `/odom` | 22,605 | 255.138 | (3.826, −2.264) | (6.003, −5.507) | 3.906 |
| `/localization/odom` | 7,578 | 255.100 | (3.829, −2.267) | (6.019, −5.531) | 3.931 |
| `/scan_odom` | 2,823 | 254.739 | (3.863, −2.303) | (6.064, −5.594) | 3.960 |
| `/localization/map_odom` | 7,566 | 254.694 | (3.832, −2.270) | (6.019, −5.531) | 3.927 |

Marker files: `endpoint-status.txt` 19:51:26 UTC;
`stationary-start.txt` stamp `1792353145161214498` = 19:52:25 UTC;
`stationary-end.txt` stamp `1792353175296120770` = 19:52:55 UTC (30 s later).
Both also record `NRestarts=1`, `ActiveState=active`. The 60 s analysis window
in [A12](#a12-stationary-analysis) extends to 19:53:25 UTC, beyond the end
marker, so the marker files alone cover only 30 s of it.

### A12. Stationary analysis

`jetson-validation/motion-wifi/stationary-analysis.json`. The 60 s
window is 19:52:25.164–19:53:25.158 UTC (`start_ns` 1792353145164435106 …
`end_ns` 1792353205158423554 for `/odom`), taken from A11 after the user
confirmed no movement.

| Topic | Messages | Span (s) | Start XY (m) | End XY (m) | Net (m) | Path (m) |
| --- | --- | --- | --- | --- | --- | --- |
| `/odom` | 5,401 | 59.993988 | (4.547107, −3.411627) | (5.070267, −4.135113) | 0.892820 | 0.897208 |
| `/scan_odom` | 665 | 59.933380 | (4.627194, −3.493406) | (5.096912, −4.197595) | 0.846473 | 4.418863 |
| `/localization/odom` | 1,800 | 59.966903 | (4.566002, −3.431353) | (5.073721, −4.141997) | 0.873380 | 0.880791 |
| `/localization/map_odom` | 1,800 | 59.966425 | (4.566002, −3.431353) | (5.073721, −4.141997) | 0.873380 | 0.880791 |

### A13. Hold-fix firmware (`276e99e`) backup, build and flash

`firmware/hold-fix-276e99e/` and `firmware/mcb-before-276e99e-20261018.bin`.
Source `SOURCE_COMMIT`: `276e99e0144472d7225f8e0a39776d9749dd7f66` (MCBV3
PR #97). Flash start (`flash-time.txt`): `Sun Oct 18 20:10:51 UTC 2026`.

Pre-flash backup binary: 1,048,576 B, SHA-256
`3c2d8280bf2452d49dbda52fdf02445ce7447674135cd6669f96ea4399a398d9`
(recomputed with `sha256sum` and equal to the saved `.sha256`). `backup.log`
(OpenOCD 0.12.0, CMSIS-DAP v2 Horco v0.2, SWD at 2000 kHz, Cortex-M4 detected)
ends with

```text
Warn : [stm32f4x.cpu] target was in unknown state when halt was requested
shutdown command invoked
```

with no dump or verify messages.

Build: `build-ubuntu-linker.log` (successful, SENTRY, `no_sysid`) ends
`Linking········ build/hardware/scons-release/MCB-project.elf` then
`scons: done building targets.` The ELF hash is
`281ad265e459817d7ac3072896f59f2316d8dc347a5e1fb82c075137d5b67ce2`
(`ELF.sha256`, `MCB-project.elf.sha256`). The deployment-only
`isolated-deploy/openocd.cfg` sources `interface/cmsis-dap.cfg`, selects
`transport select swd`, `adapter speed 1000`, `reset_config none` and
`target/stm32f4x.cfg`.

`flash.log` (probe identifiers omitted):

```text
Info : CMSIS-DAP: FW Version = Horco v0.2
Info : clock speed 2000 kHz
Info : SWD DPIDR 0x2ba01477
Info : [stm32f4x.cpu] Cortex-M4 r0p1 processor detected
** Programming Started **
Info : device id = 0x10076413
Info : flash size = 1024 KiB
** Programming Finished **
** Verify Started **
** Verified OK **
shutdown command invoked
```

### A14. Post-flash journal

`jetson-validation/postflash-final-journal.txt` (2,933 lines),
the `thornbots` service journal on the Jetson after the first flash. Cited lines
(EDT; add 4 h for UTC):

```text
16:10:52 [dji_serial_bridge_node-1] [WARN] read_loop: NO DATA from MCB for ~1000 ms …
16:14:09 [rf2o_laser_odometry_node-13] [WARN] No /odom pose at both scan stamps (1792354448.906, 1792354449.001; buffer 181, …
16:14:09 [dji_serial_bridge_node-1] [WARN] read_loop: NO DATA from MCB for ~1000 ms …
16:11:06 [async_slam_toolbox_node-16] LaserRangeScan contains 356 range readings, expected 580
16:11:10 [async_slam_toolbox_node-16] LaserRangeScan contains 353 range readings, expected 580
```

There are 38 `LaserRangeScan … expected 580` lines in the file, all with 343–359
readings. Other counts: 2 `NO DATA` lines (16:10:52 and 16:14:09 EDT, that is
20:10:52 and 20:14:09 UTC). `postflash-end-status.txt` (20:15:00 UTC):
`NRestarts=1`, `ActiveState=active`, so there was no manual restart.

### A15. Post-flash raw messages (stationary run)

`jetson-validation/20261018T201227Z-postflash-stationary.jsonl` (28 MB,
35,711 rows) and `….json`. Produced by `postflash_observer.py`, a ROS 2 subscriber
(optional `--ping` mode) run on the Jetson, 130.001 s (`start_ns` 1792354347541170882 … `end_ns`
1792354477542478914), with the chassis stationary and people moving nearby.
Message counts over the full capture:

| Topic | Messages |
| --- | --- |
| `/dji_serial_bridge/pose` | 11,286 |
| `/odom` | 11,281 |
| `/dji_serial_bridge/ref_sys` | 1,254 |
| `/localization/odom` | 3,796 |
| `/localization/map_odom` | 3,789 |
| `/scan`, `/scan_odom`, `/scan_odom/quality` | 1,435 each |

The doc's grades use the common 120 s window of A17.

### A16. Post-flash diagnostic PING results

`jetson-validation/20261018T201154Z-postflash-serial.json` (+ `.jsonl`, 5.4 MB,
6,947 rows), 25.006 s from 20:11:55 UTC. 10 PINGs sent, 10 echoed, none
unanswered. POSE 2,168, REF_SYS 241, `/odom` 2,254 messages in the sample.

| PING | 200 | 201 | 202 | 203 | 204 | 205 | 206 | 207 | 208 | 209 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RTT (ms) | 8.208 | 9.907 | 8.051 | 8.873 | 4.290 | 6.979 | 10.808 | 8.040 | 9.887 | 3.877 |

Minimum 3.877120 ms, median 8.129328 ms, maximum 10.808032 ms.

### A17. Post-flash processed measurements

`jetson-validation/postflash-analysis.json` from `analyze_postflash.py` over
A15, common 120 s window starting `start_ns` 1792354348719385346 (20:12:28.719
UTC). The saved `localization_verdict` is `NOT SCORED; clean rerun and measured
push deferred by user`, with `scene_contaminated_by_moving_people: true`; the
grades in the main text are the delegating agent's.

| Topic | Messages | Span (s) | Rate (Hz) | Max receipt gap (s) | Net (m) | Path (m) |
| --- | --- | --- | --- | --- | --- | --- |
| `/dji_serial_bridge/pose` | 10,440 | 119.980028 | 87.006148 | 4.008811 | 0 | n/a |
| `/odom` | 10,441 | 119.990248 | 87.007071 | 4.008965 | 0.000000 | 0.000000 |
| `/dji_serial_bridge/ref_sys` | 1,161 | 119.977014 | 9.668519 | 4.088794 | n/a | n/a |
| `/scan_odom` | 1,335 | 119.867650 | 11.128941 | 0.104543 | 2.065879 | 9.484391 |
| `/localization/odom` | 3,524 | 119.967848 | 29.366202 | 0.165836 | 2.022134 | 2.300139 |
| `/localization/map_odom` | 3,525 | 119.995610 | 29.367741 | 0.167126 | 2.022808 | 2.300980 |

POSE stayed at (−4.625, 0) with `odom_status` 0 (`ODOM_PODS`) for all 10,440
samples. `/scan_odom/quality` (1,336 messages, 11.130078 Hz):

| Grade (reason) | Messages |
| --- | --- |
| good | 976 |
| degraded (valid_fraction) | 315 |
| degraded (valid_fraction,sigma) | 2 |
| degraded (extrinsic_stale) | 27 |
| degraded (valid_fraction,extrinsic_stale) | 16 |
| failed | 0 |

`applied` true 1,336; `increment` `scan` 1,336; `extrinsic_stale` true 43.

| Quantity | Min | Median | p95 | Max |
| --- | --- | --- | --- | --- |
| Valid fraction | 0.432787 | 0.527869 | 0.552459 | 0.568852 |
| Reported speed (m/s) | 0.000003 | 0.062480 | 0.277872 | 0.754533 |
| Max sigma (m) | 0.000007 | 0.001577 | 0.004634 | 0.010967 |

`/scan` beam counts over 1,335 scans: 340–361, never 580; most frequent 359
(240 scans), 360 (160), 356 (155), 355 (140), 352 (136). Angle increment
0.017152745–0.017601019 rad. PING over the window: 10 sent, 10 received,
RTT 3.877120 / 8.129328 / 10.808032 ms (min / median / max).

### A18. Restore-main and main-only firmware flashes

`firmware/restore-main-412d102/` and `firmware/main-only-0e421d8/`: each holds
`SOURCE_COMMIT`, `flash-time.txt`, `flash.log`, `build.log`, `MCB-project.elf`
and `MCB-project.elf.sha256`.

| Directory | `SOURCE_COMMIT` | `flash-time.txt` | ELF SHA-256 |
| --- | --- | --- | --- |
| `restore-main-412d102` | `412d10268844e50834c0ae368a3721397d38fd8f` | 2026-10-18 20:59:02 UTC | `45c2efd8663a07b2e2c5a1e6d949cd74ded3c35630ff44de414e71a26715fac1` |
| `main-only-0e421d8` | `0e421d8484f44644f133979b3d6745c4e943053a` | 2026-10-18 21:17:59 UTC | `60490d955e543e7cea6a087a2fda8b634b6063672185f10a0d4c645c6f19555e` |

Both builds end `Linking········ build/hardware/scons-release/MCB-project.elf`
and `scons: done building targets.` Both `flash.log` files show the same
OpenOCD sequence as A13 (CMSIS-DAP Horco v0.2, 2000 kHz, device id
`0x10076413`, 1024 KiB) ending `** Programming Finished **`,
`** Verified OK **`. `restore-main-412d102/backup.log` contains only

```text
Info : Using CMSIS-DAPv2 interface with VID:PID=0xfaed:0x4870, …
Error: CMSIS-DAP command CMD_INFO failed.
```

so it is a failed probe attempt, not a backup. `main-only-0e421d8` has no
`backup.log`.

### A19. Raw odom after `412d102`

`postflash-412d102/odom.csv` (2,000 rows, no header), a `/odom` capture on
the Jetson with the controller off. Columns: stamp sec, stamp nsec, frame,
child, x, y, z, qx, qy, qz, qw, 36 pose covariances, 6 twist values, 36 twist
covariances. First row (covariances trimmed):

```text
1792356467,828659158,odom,root,-4.625,0.0,0.0,0.0,0.0,0.0,1.0,0.0001,0.0,0.0,…
```

Header-stamp span 22.267073 s. Over all rows: `odom`→`root`; x only
−4.625, y 0.0, z 0.0; quaternion (0, 0, 0, 1) (yaw 0 rad); all six twist values 0.0.

### A20. Raw odom after `0e421d8`

`firmware/main-only-0e421d8/odom.csv` (3,000 rows, same format as A19).
Header-stamp span 33.316804 s. Over all rows: `odom`→`root`; x only −4.625,
y 0.0, z 0.0; quaternion (0, 0, 0, 1); all six twist values 0.0. First row stamp
`1792357606,650153750`.
