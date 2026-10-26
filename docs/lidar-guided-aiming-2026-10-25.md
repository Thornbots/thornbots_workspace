# Lidar-guided aiming (design draft, 2026-10-25)

Stage 1 is built (no Jetson patrol, idle looks, fire age limit); stages 2-4
are open. Replaces the Jetson head patrol with lidar-guided looking. Evidence: the
[2026-10-25 robot session](#evidence). Game rules:
[ARCC context](ARCC_2026_SENTRY_CONTEXT.md).

## Why

- The RPLIDAR is on the head, 0.22 m off the yaw axis
  ([lidar_self_filter](../thornbots_pkg/README.md#lidar_self_filter)). Jetson
  patrol turns the head at -2 rad/s, about 0.19 rad per 93 ms sweep. rf2o's
  per-scan step grew from 0.7 mm (head still) to about 23 mm (patrol), and the
  parked reference check failed under patrol (82.9 mm steps, 0.81 m drift).
- The lidar sees about 285 deg whatever way the head faces (blind only 6-79.5 deg
  CCW of the gun), so it does not need head motion to cover the field. Only the
  camera does.

## Current chain

| Stage | Behaviour | Timeouts |
| --- | --- | --- |
| YOLO -> `target_selector` -> `target_tracker` | `/cv/target_state`, capture-stamped, published per detection only | track resets after a 0.5 s gap (`track_max_gap_s`) |
| `point_to_cv_target` | 40 Hz `/cv/target`, `now()`-stamped; aims and fires on a held state; patrol point after 0.2 s without target | `target_timeout_s` 0.5 s |
| `mcb_relay` -> bridge | republish; bridge drops frames >= 200 ms old since decision | decision age only, not detection age |
| Firmware `AutoAimAndFireCommand` | aims/fires per frame; after expiry: hit turn (if `turn_to_hit`), else firmware patrol (if `type_c_based_patrol`), else hold | `TARGET_VALID_TIME` 200 ms; `HIT_TURN_DURATION` 500 ms |

Firmware keeps the **last frame's flags**. If the Jetson goes silent after a
target frame (which clears `turn_to_hit`), firmware hit turns stop working, so
any no-patrol design must keep sending non-firing frames.

Hits: firmware turns the head toward the hit armor's side
(`util/HitOrientation.hpp`) and reports the hit on REF_SYS.

## Decided

- No Jetson patrol.
- Fire on a prediction only while the newest detection is at most 0.15 s old
  (`fire_max_state_age_s`). Keep aiming, without firing, until
  `target_timeout_s` (0.5 s).
- The `room_check` stale-CV mode is a diagnostic, not a requirement. YOLO
  outages need not be designed for beyond the stack restarting.
- Shooting with no referee engages every robot (already true:
  `team_from_ref_sys` returns no team for `robot_id` 0).
- Firmware hit handling is unchanged; hold 2 s after a hit.
- Obstacles come from the saved field map.

## Design

### Where the head looks with no camera target

Non-firing frames, `turn_to_hit` set, `patrol` bit set (meaning: not a target
point). In order:

1. **Last enemy**, 3 s after losing it: keep following the prediction until 0.5 s,
   then hold its last position.
2. **Hit**, 2 s: follow the gun so the head stays where firmware's hit turn left
   it. The newer of 1 and 2 wins.
3. **Lidar track worth checking** (stage 2 below).
4. **Enemy starting zone.** Raw odometry is field-centred: firmware boots red at
   (-`START_X`, `START_Y`) facing +x, blue at (+`START_X`, `START_Y`) facing -x
   (`OdometrySubsystemConstants.hpp`; `START_X` 4.625 m, not yet measured on
   the field). The enemy zone is our start with x negated. Team comes from the
   REF_SYS blue flag exactly as firmware uses it, so with no referee both sides
   assume red and the head looks down the field from the boot spot.

Aim height is armor height (~0.15 m; Standard-class panels sit 60-150 mm up),
not lidar height. Turns are rate capped to limit lidar smear.

### Lidar tracker (new `lidar_tracker` node, thornbots_pkg)

- `/scan`, skipping scans taken while the head turns fast.
- Opponents taller than the 0.355 m scan plane mostly show their **head**:
  small clusters, but the head is on the robot's yaw axis, so the cluster
  centre is steady even while the chassis spins.
- Size from our own head as a stand-in (`sentry_v2` CAD sliced at z 0.275-0.425 m,
  within 0.13 m of the yaw axis, excluding our lidar arm): 0.15-0.25 m wide
  depending on view angle, median 0.23 m, nearly constant over that 15 cm of
  height. Accept clusters of roughly 0.10-0.40 m.
- Obstacles come from the saved field map (`/map`, published in
  `localization_mode` `amcl` and `slam`). Scan points within a margin
  (~0.25 m, to absorb localization and URDF mount error) of an occupied cell
  are obstacles; the rest can be robots. A robot that close to a wall is missed.
- No map frame (`none`) or a live map (`mapping`, which can map robots): no lidar
  looks; the enemy-zone look still works.
- Tracks: position and velocity, kept a few seconds through dropouts (tilt on
  the Bumpy Road or ramps moves the plane ~7 cm per degree at 4 m).
- Each track is unchecked, enemy (camera confirmed) or checked-empty
  (teammate or false cluster; ignored for a while).
- Ranking for a look: enemy > unchecked, then moving/approaching, then closer,
  Look ~0.6 s; no enemy found -> mark
  checked, move on.
- Tracks live in `map`. A look only has to land the robot in the camera's view
  (~1 m at 2-3 m), but obstacle removal needs localization within the margin:
  a misaligned map turns walls into candidates.

### Hits

Firmware's hit turn stays as it is; no firmware change. The Jetson only keeps
it permitted (`turn_to_hit` on every non-target frame) and, for 2 s after REF_SYS
reports a hit, follows the gun instead of pulling the head back.

## Stages

| # | Change | Before Oct 31 |
| --- | --- | --- |
| 1 | No patrol; idle looks 1, 2, 4; fire age limit | yes |
| 2 | `sim`: our lidar sees other robots (today every robot model is hidden from it, [sim README](../sim/README.md#both-robot-models-the-lidar-does-not-scan-its-own-model)) | yes |
| 3 | `lidar_tracker` publishing only (rviz), no head effect | likely |
| 4 | Head looks at tracks | draft; needs a robot test before enabling |

## Risks

- Detection range is unmeasured. A 0.23 m head spans about 6-7 of the 0.5 deg
  bins at 4 m and about 3 at 8 m, before missing returns (~408 of 720 bins
  return per scan); other teams' heads may differ from ours.
- Head-sized clutter (posts, corners, ramp edges); robots on the High Ground
  or with heads off the plane; teammates cost one look each.
- Turning toward targets still smears scans; rf2o/AMCL should skip
  fast-turn scans (localization side). The URDF lidar offset (~10 cm) shifts
  localization when the head turns until the new CAD lands.
- Staring at the zone covers less than patrol did until stage 4; compare
  time-to-first-detection in the sim match stages before promoting.

## Acceptance before `main`

- Sim match stages no worse than with patrol.
- Robot, head idle: rf2o per-scan steps near the still-head 0.7 mm.
- A hit turn observed on the robot (needs referee hardware).

## Match-day settings

`auto.launch.py` arguments, set through `AUTO_LAUNCH_ARGS` in
`/etc/thornbots/launch.env`; a change needs a `thornbots` restart. Patrol is
not an option.

| Argument | Default | Effect |
| --- | --- | --- |
| `lidar_looks` | `true` | `false`: lidar tracks never steer the head; last-enemy, hit-hold and idle looks remain. Also off by itself with no saved map |
| `idle_direction` | `zone` | `hold`: with nothing else to look at, the head stays where it is (still sending non-firing frames, so hit turns keep working) instead of facing the enemy starting zone |
| `lidar_obstacle_margin_m` | `0.25` | distance from a mapped obstacle within which scan points count as obstacle |

`fire_max_state_age_s` stays a node parameter, not a launch argument.

| At the venue | Set |
| --- | --- |
| Head chases walls or empty spots | `lidar_obstacle_margin_m:=0.4`, or `lidar_looks:=false` |
| No saved map for this field | `lidar_looks:=false` (automatic) |
| Idle head faces a wrong direction | `idle_direction:=hold` |
| Localization degrades whenever the head moves | `lidar_looks:=false idle_direction:=hold` |

## Open questions

None at this revision.

## Evidence

`~/ros2_ws/robot-session-20261025/REPORT.md` on the Mac mini (steps 3-4,
`step4/patrol-lidar.txt`); partial deskew work in
`~/ros2_ws/scan-deskew-20261025/`.
