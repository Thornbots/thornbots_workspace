# Lidar mount measurement — 2026-10-26

The Oct 26 robot session supersedes the old zero-yaw mount and CAD-only
self-filter. Evidence is on the Mac mini at
`~/ros2_ws/robot-session-20261026/evidence-1/`; the robot was not run again
for this implementation. Maintained usage lives in the
[filter owner](../../thornbots_pkg/README.md#lidar_self_filter).

- Translation in `head`: (-0.105, -0.193326, 0.101293) m from the team's
  new CAD, XY radius 0.220 m.
- `headturn-yaw-joint.txt`: joint five-pose head-turn fit gives scan zero
  0.5907 rad (33.84 degrees) CCW of the gun, radius 0.2225 m. Leave-one-out
  yaw spans 33.33..34.55 degrees. Oct 25 registration gave 34.2 degrees and
  the CAD head-outline fit 35.0 degrees. The authored FOV-marker yaw
  -0.149533673 rad (-8.57 degrees) does not describe the driver's scan zero.
- Self-filter: -0.5585..1.0123 rad (-32..58 degrees) in the scan frame.
  Both Oct 25 bags leaked zero head hits with this sector; the live
  `1a-level-probe.txt` likewise recorded zero near returns on `/scan`.
  The old 0.09..1.41 sector leaked approximately 8.5 head hits per scan
  at -10..-1 degrees and blanked real returns at 53..81 degrees.
- `1c-old-shift.txt` / `1d-new-shift.txt`: head-turn SLAM displacement at
  +90/-90 degrees fell from 18.7/14.0 cm to 3.6/2.6 cm with yaw 0.597.
  That A/B used the provisional yaw, rather than the final joint-fit 0.5907.

## Integration

`thornbots_pkg` #32 retains launch overrides and uses the measured defaults
in launch, xacro and the standalone filter. Sim spawns a separate URDF:
its `lidarlink` must match TF, and its gpu lidar has no additional pose.
Robot visuals are excluded from the sensor, so the shared hardware/sim
self-filter supplies the blind sector. The degraded-scan fixture restores
the measured sector after its temporary occlusion.

The CAD drafts retain all other imported geometry and the existing armor
stagger hold. Merging the measured-mount package branch into the CAD package
branch preserves the launch API and identical lidar defaults whichever
draft merges second.

## Implementation validation

Measured-mount package pins: thornbots_pkg `1c8f9f8` (#32) and sim `280d252`
(#50), on workspace base `c3ae0e8`. In task-owned container
`isaac-agent-measured-lidar-20261026`, ROS domain 100, the package tests pass:
thornbots_pkg 142 tests, zero failures/errors/skips; sim 224 tests, zero
failures/errors, 87 skips. The first unrestricted sim compilation was killed;
the two-job rebuild succeeds. No quality baseline was expanded.

The expanded default xacro gives the expected lidar xyz and yaw; an explicit
translation/yaw override also renders correctly. The existing sim URDF
consistency test now checks `lidarlink` against the xacro defaults.
`smoke.sh` resolves the packages to this task's overlay and finds a clean graph.
One `localization_tests.launch.py scenario:=baseline` AMCL/rf2o integration
case passes in 10.98 s. The native checker accepts both sim and robot logs;
the post-run process check finds no remaining stack or installed nodes.
This is an integration check, not a repeated localization-accuracy claim.

Host Python 3.12 quality and `actionlint -shellcheck=""` pass in each changed
repository. No robot was contacted or run, and no movement logic was changed.
