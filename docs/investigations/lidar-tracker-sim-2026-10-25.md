# Lidar tracker in sim (aiming stages 2-3) — 2026-10-25

Stages 2 and 3 of [lidar-guided aiming](../lidar-guided-aiming-2026-10-25.md#stages):
our sim lidar sees opponents, and `lidar_tracker` publishes map-frame robot
tracks without moving the head. Design and parameters:
[lidar_tracker](../../thornbots_pkg/README.md#lidar_tracker); opponent
rendering: [sim lidar visibility](../../sim/README.md#both-robot-models-the-lidar-does-not-scan-its-own-model).
Hardware is untested.

## Evidence

Mac mini, own container (3 CPUs). `~/ros2_ws/aiming-stage23-20261025/` holds
the bench source (`bench-source/lidar_tracker_scenario.cpp`, not a registered
suite), diagnostics (`diag/`), `scenario-final/` (parked and driving),
`scenario-drive2/` (driving, per-scan rows) and `suites-A/` (regression suites).

## Opponent geometry in the scan plane

`opponent_driver` drew every opponent link from its collision hull. In the
lidar plane (opponent-local z about 0.345 m) the head and gun hulls measured
0.35-0.48 m and the 75%-scaled chassis hull 0.36 x 0.30 m. The CAD head,
lidar arm included, measures 0.16-0.33 m, and the CAD chassis ends below
0.32 m. A spinning opponent at 2 m returned 0.40-0.42 m clusters and was
detected on 45% of scans. Opponents now keep the CAD head and gun meshes and
hide the chassis hull from the lidar. A front-on head at 2 m returns 10
points, 0.154 m wide.

## Scenario

Sentry parked at (-5.7, 3.5), heading +x, AMCL on `clean_map`, head still.
`opponent_0` drives the open top lane (y 3.35) at range r ahead;
`opponent_1` the middle lane (y 2.45, 0.4 m from walls and the centre bar)
at range r. Both oscillate +-0.3 m along range and spin at 2 rad/s. Three
trackers (margins 0.15, 0.25, 0.40 m) run on the same scans; 12 s per case.
A scan is eligible for an opponent when its head is outside the self-filter
blind sector, has map line of sight and is not shadowed by the other
opponent. A detection is a track refreshed by that scan within 0.6 m of gz
truth; error is to the opponent's yaw axis. Unmatched tracks within 1 m of
an opponent count as duplicates, others as false tracks.

## Parked (margin 0.25 m)

| Range | `opponent_0`, open lane | error mean / p95 | `opponent_1`, 0.4 m from walls | error mean / p95 |
| --- | --- | --- | --- | --- |
| 2 m | 66/66, 53/53 (100%) | 0.08 / 0.14 m | 135/135 (100%) | 0.09 / 0.14 m |
| 4 m | 135/135 (100%) | 0.09 / 0.15 m | 135/135 (100%) | 0.09 / 0.15 m |
| 6 m | 135/135, 128/135 (95-100%) | 0.10 / 0.17 m | 135/135 (100%) | 0.09 / 0.16 m |
| 8 m | 132/135 (98%) | 0.10 / 0.16 m | 114/134 (85%) | 0.08 / 0.15 m |

Two counts are one-opponent and two-opponent cases. Velocity error mean
0.08-0.14 m/s. No false or duplicate tracks in any parked case at 0.15 or
0.25 m. Error is mostly the visible-surface centroid bias toward the sensor.

At 2 m, `opponent_0`, nearly straight ahead of the gun, was eligible on only
53-66 of 135 scans: the lidar sits 0.22 m off the yaw axis, so a target in
front of the gun at short range overlaps the blind sector's 5.2 deg edge.

## Margin

- 0.15 m: parked detections equal or better (`opponent_0` at 6 m: 135/135
  against 127-128); most false tracks while driving.
- 0.40 m: robots near mapped obstacles disappear. `opponent_0` at 6 m (head
  0.2-0.4 m from the centre bar) fell to 20-25/135, with 11-26 false and 9-17
  duplicate observations from the remaining fragments; `opponent_1` at 8 m
  fell to 78/134 (58%).

## Driving

The sentry drove forward and back along the lane by `/cmd_vel` (peak
0.4 m/s, 1.2 m travel), which moves the gz chassis directly. Localization
followed poorly: `map->root` p95 error 0.85-0.91 m, max 0.97 m, against
0.01-0.04 m parked, with or without opponents. Results are split by that
error (`scenario-drive2/`, all ranges and counts):

| `map->root` error | Scans | Detected, 0.15 / 0.25 / 0.40 m | False per scan, 0.15 / 0.25 / 0.40 m |
| --- | --- | --- | --- |
| < 0.1 m | 852 | 69% / 69% / 52% | 0.75 / 0.42 / 0.31 |
| 0.1-0.3 m | 47 | 0% / 0% / 0% | 4.7 / 3.4 / 0.8 |
| > 0.3 m | 314 | 0% / 0% / 0% | 6.3 / 5.2 / 1.3 |

With good localization at 0.25 m: 74% at 2 m, 73% at 4 m, 67% at 6 m, 63% at
8 m; fresh-match error 0.09-0.15 m mean. Of the misses there, 253 of 297 had
no return within 0.6 m of the head at all: the plane passed the head,
probably from chassis pitch while accelerating (not measured). False tracks
sit 0.25-0.35 m off walls, as the design predicts when localization error
exceeds the margin. The real drive goes through firmware; `mcb_drive` below
is the realistic localization check.

## Regression suites

Gates unchanged, `backend:=hosted` as in the
[T39 runs](t39-parked-drift-2026-10-25.md) (Renode ran about 15x slower here;
its first `mcb_parked` cell passed before it was stopped). Lockstep reported
0 timeouts.

- `mcb_parked`: 12/12, checker ok. Per-cell `map->root` p95 0.008-0.077 m;
  three T39 runs with opponents hidden and default `reference_scans` off
  spanned 0.011-0.090 m.
- `mcb_drive`: 1/1, checker ok. Localization p95 approach 0.167, drive
  0.031, spin 0.015 m; spin hit rate 0.97. 2026-10-22 promotion runs:
  0.04-0.29, 0.008-0.02, 0.035-0.07 m.
- AMCL `drift`: first run 9/10, `noise_correction` failed (map correction
  1.16 m; 0.08-0.15 m in 14 T39 runs). Three isolated reruns passed
  (0.107-0.127 m) and a full rerun passed 10/10, checker ok. The suite
  spawns no opponents.

Visible opponents produced no AMCL or rf2o change outside run-to-run
spread. In the parked bench, `map->root` stayed at 0.01-0.04 m with one or
two opponents moving at 2-8 m.

## Not done

- No hardware run; other teams' heads may differ from ours.
- Head turns during a sweep are covered by unit tests only; no head-turn
  scenario ran.
- Camera labels (enemy, checked-empty) are unit-tested only; the bench ran
  without the CV stack.
- The bench is not a registered suite: it needs `thornbots_pkg` messages,
  which `sim` does not build-depend on.
