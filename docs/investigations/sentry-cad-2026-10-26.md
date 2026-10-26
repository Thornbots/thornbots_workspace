# Sentry CAD integration — 2026-10-26

Input: the team's `sentry_low_res_model` Onshape URDF export, supplied as
`sentry_low_res_model.zip`, SHA256
`0841b0ca27e54125ad8d962edf78dad97ce76198bb9d3b7c69036974ba32adff`.
Only XML and STL data were read; no supplied code was executed.

## Frame derivation

URDF rotations compose as `Rz(yaw) Ry(pitch) Rx(roll)`. The yaw bearing is
`revolute_3_2`: `base -> lpr_yaw`, translation `(0, 0, 0.171275)`,
yaw `1.72033`, axis `-z`. The export's `root` is at this bearing;
`fixed_node_to_root_joint` puts `base` 0.171275 m below it.

The gun's `fastened_7` rotation is approximately `Rz(pi) Rx(110 degrees)`.
The barrel extends along gun-local **-z**, so it points along `lpr_yaw` **-y**
in plan, elevated 20 degrees in the exported pitch pose. Therefore
`p_head = Rz(pi/2) p_lpr_yaw`: `(x_head, y_head) = (-y_CAD, x_CAD)`.
The export's yaw angle is reversed, rather than copied into the ROS joint:
`heading = 1.72033 - pi/2 - q_CAD`. ROS `headlink` retains axis `+z` and
the heading-fixed `root` convention.

`pitch_revolute` is 0.136 m above the yaw bearing, axis CAD `-x`.
Pitch assets use `Ry(20 degrees) Rz(90 degrees)` so zero ROS pitch is a
horizontal gun and positive ROS `+y` pitch points down. The CAD-pose conversion
is `q_ROS = -q_CAD - 20 degrees`. Existing ±0.6 rad simulation limits remain
an explicit approximation; the export's limits convert to approximately
`[-0.349066, +0.366519]` rad, not a new command policy.

The four wheel-mesh minima in export-root z are -0.236906, -0.234981,
-0.267504 and -0.241994 m. Their 32.523 mm spread means this export is an
uneven suspension pose. The lowest wheel defines the imported clearance
datum: yaw bearing z = 0.267503694 m. It is **not a measured settled ground
plane**. Wheel/suspension dynamics retain their existing simulation values.

## Lidar comparison

Distances are metres from the yaw axis in `head`; bearings are CCW from
the horizontal gun direction. Radius means XY radius.

| Source | x | y | z | Radius | Bearing |
| --- | ---: | ---: | ---: | ---: | ---: |
| Previous `lidarlink` | -0.119391 | -0.185010 | 0.0968001 | 0.220188 | -122.835° |
| New CAD FOV reference | -0.105000 | -0.193326 | 0.101293 | 0.220000 | -118.507° |
| Oct 25 fit | ≈-0.190 | ≈-0.130 | unknown | ≈0.230217 | ≈-145.620° |

Previous → CAD: `(0.014391, -0.008316, 0.0044929)` m: 16.621 mm in XY,
17.218 mm in 3D. CAD → fit: approximately `(-0.085, +0.063326, unknown)` m,
**105.996 mm in XY**, substantially over the requested 3 cm warning threshold.
The user chose the CAD despite this disagreement. This does not establish
that CAD alone fixes the Oct 25 head-turn SLAM displacement.

`lidar_revolute` locates the part at CAD yaw-frame
`(-0.193326, +0.105, +0.107168)` m, which maps to
`(-0.105, -0.193326, +0.107168)` in `head`. `fastened_6` places the
`lidar_fov__1_` reference 5.875 mm lower and rotates it by -1.72033 rad.
The imported `lidar` uses that FOV reference, giving scan-zero yaw
`pi/2 - 1.72033 = -0.149533673` rad (**-8.567648°**) relative to the gun,
instead of the former zero yaw. The FOV link has no mesh: this is an authored
CAD reference, **not proof of the physical scan plane or driver scan zero**.
Validate both against `/scan_raw` on the robot before trusting localization.

## Optical and armor references

The IR FOV mesh has its apex at the `ir_fov` link origin. That apex, rather
than the sensor housing centre or the separate RGB apex, defines the camera
translation. `camera` keeps REP 103 body axes (+x forward, +y left, +z up).
The gun muzzle uses the front bore cross-section centre, not its bounding-box
extremum. Numerical export rotation noise is rounded away.

Joint translations below are parent-relative, in metres. Camera/muzzle
translations use the rebased `head_pitch` frame, so their parent-relative
deltas include the change of pitch reference, not just physical displacement.

| Joint | Previous xyz | Imported xyz | Delta xyz |
| --- | --- | --- | --- |
| `headlink` | (-0.000171, 0.000095, 0.248293) | (0, 0, 0.267504) | (+0.000171, -0.000095, +0.019211) |
| `headpitch` | (-0.007605, -0.100122, 0.142350) | (0, 0, 0.136) | (+0.007605, +0.100122, -0.006350) |
| `cameralink` | (0.092038, 0.094867, 0.056659) | (0.095700, -0.011500, 0.055000) | (+0.003662, -0.106367, -0.001659) |
| `muzzlelink` | (0, 0.112800, 0) | (0.172976, 0.001903, 0) | (+0.172976, -0.110897, 0) |
| `armor_0link` | (0.178162, 0.178426, 0.230361) | (0.204140, 0.150683, 0.148603) | (+0.025978, -0.027743, -0.081758) |
| `armor_1link` | (-0.177935, 0.177863, 0.135661) | (-0.148299, 0.200911, 0.252488) | (+0.029636, +0.023048, +0.116827) |
| `armor_2link` | (-0.178505, -0.178235, 0.230361) | (-0.204140, -0.150683, 0.148603) | (-0.025635, +0.027552, -0.081758) |
| `armor_3link` | (0.177593, -0.177673, 0.135661) | (0.148299, -0.200911, 0.252488) | (-0.029294, -0.023238, +0.116827) |

At yaw/pitch zero, camera displacement expressed in the common `head`
axes is (+0.011267, -0.006245, -0.008009) m; muzzle displacement is
(+0.180582, -0.010775, -0.006350) m. The imported armor bearings are
36.432°, 126.432°, -143.568° and -53.568°; radii are 0.253729 m for
the low pair and 0.249716 m for the high pair.

Low-resolution meshes aggregate `base` into `root`; `lpr_yaw` and `lpr_lidar`
into `head`; and `lpr_pitch`, gun, camera housing and `part_2` into
`head_pitch`. FOV cones and dummy loop links are excluded. Head collision
meshes are convex hulls; chassis collision, masses, inertias, wheels,
suspension, plugins and topics remain the previous simulation approximation.
The new export's gram-scale masses are not credible dynamic parameters.

Each armor frame uses the centre of the largest outward panel face, with
the 3 mm scoring box centred 1.5 mm behind it. Normals remain 15 degrees up;
the Small Armor Module scoring rectangle remains 135 × 125 mm. Frame indices
are sorted by CCW bearing from +x. The new vertical stagger is approximately
103.885 mm, exceeding the existing 100 mm rule assertion; this is reported,
not silently flattened to make that assertion pass.

## Integration boundaries

- sim draft [#46](https://github.com/Thornbots/sim/pull/46), head `2dc107d`,
  changes opponent visibility and `sentry_v2.urdf.xacro`. Keep its visibility
  and opponent-driver changes when rebasing; rerun its visibility test against
  the replacement head/gun meshes and the new scan height/sector.
- thornbots_pkg draft [#27](https://github.com/Thornbots/thornbots_pkg/pull/27)
  is outside this change. Its `lidar_tracker.cpp` hardcodes output z = 0.355 m;
  that should become a carried scan-frame transform, or use the new scan
  height explicitly. Its map filtering must use the matching map slice.
- Firmware, movement/routes, odometry constants, wire format and patrol/aiming
  algorithms are outside this integration. Geometry constants in simulation
  consumers must agree with the imported transforms; any solver assumption
  exposed by the new geometry needs a separate aiming change.

## Validation

Ran on the Mac mini in `isaac-agent-cad-20261026`, Colima, domain 164,
partition `agent-cad-20261026-164`, using the checked-out hosted firmware
fixture (`backend:=hosted`) for E2E and AMCL/rf2o for drift. No physical
robot runs. All suite commands used `headless:=true foxglove:=false`.
Measurements are single runs, not a controlled accuracy improvement claim.

Baseline: parked 12/12 and drive 1/1 passed the native log checker. Drift
was 9/10: `parked_push` missed by 0.0161 m against 0.015 m; its isolated
rerun passed. `noise_correction` passed. Baseline package tests reported
499 tests, zero failures. An initial mistaken `backend:=hosted` drift
invocation failed argument validation and is excluded from measurements.

Changed model: parked 12/12 and drive 1/1 passed the native log checker.
The first drift run passed 10/10, but review found that `scan_degraded`
restored the old mask during recovery. The test now captures and restores
the actual parameters, including exception cleanup; the final rerun is
recorded below. No baseline or acceptance threshold was expanded.

The final full drift rerun passed **10/10**, including `noise_correction`,
`scan_degraded` recovery and `parked_push`, and passed the native log checker.
Final build passes. Final package result: **499 tests, six reported failures**:
four failed GTest cases plus their two failed CTest wrapper results.
The failures are `UrdfConstants.ArmorRules` (103.885 mm exceeds 100 mm),
`CvHeadAim.RandomAnglesRoundTrip`, `CvHeadAim.SolvedRayPassesThroughTargetPoint`
and `CvHeadAim.TargetLevelWithRootIsAimedDownward`. The unchanged aiming
algorithm assumes the muzzle is on the pitch axis; with the actual forward
muzzle, the fixed-target ray tests miss by approximately 7–53 mm. This is a
real integration limitation, not a tolerance to relax. The updated lateral
offset test checks the new, smaller nonzero yaw displacement. All registered
thornbots_pkg and sentry_localization tests pass. The explicit actual-field
map fixture passes 2/2. Draft PRs must remain unmerged until these failures
are resolved by the owning workstreams or their acceptance is decided.

| Localization p95 | Baseline | Imported CAD |
| --- | ---: | ---: |
| Parked: range across 12 cases | 0.014456–0.075829 m | 0.008254–0.112258 m |
| Drive: approach segment | 0.039312 m | 0.084792 m |
| Drive: drive segment | 0.035643 m | 0.038770 m |
| Drive: spin segment | 0.009432 m | 0.017085 m |

These passing runs show worse worst-case p95 values after the import;
they do not validate the CAD against the Oct 25 physical displacement.
The drive suite still reports diagnostic aiming/TF errors even when its
completion gates pass; it is not a combat-accuracy acceptance test.

The drift harness does not publish a high-rate p95. The following are p95
values of its **sparse printed truth-error samples**, including deliberate
fault injection, not additional acceptance gates or uniformly sampled data:

| Drift scenario | Baseline p95 (samples) | Imported CAD p95 (samples) |
| --- | ---: | ---: |
| drift_correction | 0.215515 m (14) | 0.062720 m (15) |
| drift_correction_obstacle | 0.065545 m (14) | 0.072490 m (15) |
| moving_obstacles | 0.068300 m (15) | 0.083200 m (15) |
| real_accel | 0.063275 m (8) | 0.055520 m (8) |
| odom_stuck | 2.395500 m (27) | 4.138460 m (27) |
| scan_degraded | 0.248375 m (14) | 0.232930 m (14) |

`odom_stuck` intentionally checks liveness rather than accurate recovery;
its large error is not a localization-accuracy pass. Noise and parked-push
cases use their own correction/recovery metrics rather than this sample set.

Both real/sim xacro renders pass `check_urdf`. Regenerating the canonical
field map at nominal sim scan height 0.357296694 m reproduces the existing
PGM byte-for-byte. Quality checks use a host Python 3.12 venv with the
workspace's pinned requirements; actionlint uses `-shellcheck=""`.
Both checks pass in all three changed packages and the workspace.
An initial unrestricted compiler run was killed for memory pressure; the
successful rebuild used two compiler jobs. The first container creation
requested eight CPUs on a six-CPU Colima VM; its helper cleaned up, and the
successful container used six CPUs. No image was rebuilt.

Source validation began at workspace `d0fd482`. The workspace PR is based on
current nightly `fe4849d6f49a5ae0e229535d8829df2f7a123a14`, preserving its unrelated
gitlink advances. Diff review of those advances found only documentation,
host setup/installer and image-build changes; runtime code used by these
suites is unchanged. Exactly thornbots_pkg, sim and sentry_localization are
bumped. Full evidence and the import/slicing calculations are retained at
`~/ros2_ws/sentry-cad-20261026/validation-20261026/` on the Mac mini.

TF sanity at zero pitch, positions in metres (root at its clearance datum):

| Frame | In head, all yaws | In root, yaw 0 | In root, yaw +90° | In root, yaw -90° |
| --- | --- | --- | --- | --- |
| lidar | (-0.105, -0.193326, 0.101293) | (-0.105, -0.193326, 0.368797) | (0.193326, -0.105, 0.368797) | (-0.193326, 0.105, 0.368797) |
| camera | (0.095700, -0.011500, 0.191000) | (0.095700, -0.011500, 0.458504) | (0.011500, 0.095700, 0.458504) | (-0.011500, -0.095700, 0.458504) |
| muzzle | (0.172976, 0.001903, 0.136000) | (0.172976, 0.001903, 0.403504) | (-0.001903, 0.172976, 0.403504) | (0.001903, -0.172976, 0.403504) |

Lidar yaws relative to root are -0.149533673, +1.421262654 and -1.720330000
rad respectively; camera/muzzle yaws equal head yaw. Roll/pitch are zero.
Independent review verified transformed visual vertices, sensor positions,
armor radii and head collision-hull containment to approximately 2 µm.

Package drafts and signed heads:

- [thornbots_pkg #30](https://github.com/Thornbots/thornbots_pkg/pull/30):
  `ec913d14b8b108fad9599f44e475a7d70b74efdb`
- [sim #48](https://github.com/Thornbots/sim/pull/48):
  `293eb5e50a792f3e08925e4077314411f128e2b9`
- [sentry_localization #20](https://github.com/Thornbots/sentry_localization/pull/20):
  `d4207c6a1031d9ee6075134d294e6430ca3e24ee`

The task container and its volumes were removed, and Colima stopped when
no containers remained. No other container was stopped or removed.
