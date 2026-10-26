# Sentry CAD integration — 2026-10-26

Round 2 below supersedes the round-1 muzzle choice and acceptance summary.
The frame derivation and initial measurements remain here as provenance.

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

## Round 2: pitch-axis contract and independent CAD checks

The `muzzle` contract is an aiming origin on the pitch axis between the
flywheels, directed along `head_pitch` +x. Round 1 incorrectly replaced it
with the bore-front reference. Round 2 restores `(0, 0.00190269, 0)` in
`head_pitch`, preserving only the CAD lateral offset. The bore front remains
172.9764 mm ahead of this origin. No aiming algorithm changed. The independent
FK fixture's literal origin and pitch-invariant z expectation were updated;
the three failing ray/round-trip/elevation test assertions and tolerances
were not changed. All aiming tests now pass.

### Armor lower-edge rule

The 100 mm bound is S126, a physical constraint on lower edges, not a
historical model tolerance. Independently composing the original joint and
visual transforms confirms an actual CAD violation; flattening the import
or relaxing the assertion would hide it. The four panels attach directly to
`base` through fixed joints. Low/high mount z values are 47.8454/151.7300 mm,
already 103.8846 mm apart before importing. The importer selected the matching
135 × 125 mm outward faces; vertex-average and area-weighted face centres
agree within 0.000002 mm.

| Reference | Low lower edges | High lower edges | Maximum spread |
| --- | ---: | ---: | ---: |
| Actual 19 mm-deep CAD modules | 83.7035–83.7037 mm | 187.5882–187.5883 mm | 103.884783 mm |
| Outward CAD faces | — | — | 103.884837 mm |
| Imported scoring rectangle, current test | — | — | 103.884705 mm |

The scoring box thickness contributes about 0.388 mm to absolute lower-edge
height but does not resolve the stagger. Neither changing the wheel datum
nor suspension motion changes fixed panel-to-base separation. Tilting improves
one comparison while worsening the opposite: an all-azimuth 1° sweep gives
107.223–110.233 mm spread, and 5° gives 120.238–135.269 mm. A numerical tilt
minimization also finds the minimum near level; this is not a formal global
proof. The simplified export establishes a modeled violation, not measured
noncompliance of the physical robot.

S126 and the imported coordinates are retained. A mechanically confirmed
CAD correction needs at least 3.885 mm less high/low separation (for example,
1.943 mm per pair toward the other). This decision is outside a faithful
import and remains unresolved. Registered tests therefore report one failing
GTest case plus its CTest wrapper, rather than zero failures.

### Oct 25 head-turn displacement: offline evidence

The session is `~/ros2_ws/robot-session-20261025/`. The CSV producer
`scripts/yaw_watch.py` records `map->root` translation/yaw and `root->lidar`
yaw, despite naming the latter `head_yaw`. The deployed lidar fixed yaw was
zero, so this also represented head-joint yaw. The first recorded TF yaw was
about +0.1036 rad (+5.94°), whereas the settled baseline immediately before
the deliberate turns was essentially zero (median -0.0009 rad in the
reproduction window). Held turns were approximately +1.5919/-1.5513 rad.
Consequently the deliberate-test baseline has effectively aligned map, root
and head axes. Rotating the rounded historical `(-0.19, -0.13)` fit from the
first CSV orientation changes it by about 24 mm, insufficient to explain
the disagreement with CAD. The original fit implementation is unavailable;
its exact convention cannot be certified from the rounded session report.

Refitting five settled CSV windows, subtracting recorded odometry translation,
gives apparent head-frame translation `(-0.2007, -0.1169)` m if map yaw is
ignored, and `(-0.1844, -0.1261)` m if reported SLAM yaw and the deployed TF
chain are included. SLAM yaw ratchets from zero to 0.0942 rad after the positive
turn and finishes near 0.1082 rad. Positive/negative-turn estimates disagree
by centimetres; these are diagnostic fits, not calibrated extrinsics. A
position-only fit cannot explain the yaw ratchet itself.

Raw scans do exist in `step4/bag/bag_0.mcap`, together with TF and odometry.
An independent reproduction registers six individual settled scans (three
near zero and three near +0.65 rad): all nine pairs, each with three initial
yaw guesses, using trimmed point-to-point ICP. It retains the closest 80%
of correspondences under 0.3 m, using finite driver-valid ranges up to 8 m.
The 27 fits have retained-point RMS 25.9–32.1 mm. Recorded pod displacement
between these headings is approximately 1 mm. Scene changes, partial overlap,
limited heading separation and nearest-neighbour fitting remain limitations.
These recordings are from later on Oct 25, not the deliberate ±90° CSV run.

For translation `l` in `head` and scan-zero yaw `delta`, parked registration
constrains `u = Rz(-delta) l`, rather than `l` and `delta` separately. If scan B
registers into scan A by `p_A = R(theta) p_B + t`, then
`t = (R(theta)-I) u`; the yaw-axis coordinate in the scan frame is `-u`.
The implementation checks this equation, its gauge freedom and ICP recovery
against independent synthetic points before fitting the recording.

| Quantity | Independent raw-scan reproduction |
| --- | --- |
| Median effective `u` | (-0.202956, -0.104684) m |
| Fit x range | -0.209429…-0.195434 m |
| Fit y range | -0.115644…-0.098976 m |
| CAD `u`, using CAD translation and -8.568° yaw | (-0.075027, -0.206811) m |
| CAD-to-fit distance in `u` | 163.7 mm |
| CAD translation held fixed: best direction-only yaw | +34.21°, with 8.36 mm radius residual |
| CAD yaw held fixed: implied translation | (-0.216287, -0.073280) m |

An earlier independent selection returned `u≈(-0.2051,-0.1111)` m, retained
RMS 26–34 mm and a 161 mm CAD discrepancy. The reproduction does not certify
those exact earlier windows/settings; both fits support the discrepancy at
centimetre precision. The parent reran the saved reproduction and obtained
identical numerical outputs. A 108-fit sensitivity sweep over retained fractions
0.6/0.7/0.8/0.9 moves median `u` from about (-0.199,-0.111) to
(-0.210,-0.101) m; the large CAD discrepancy persists. These dependent fits
provide sensitivity ranges, not statistical confidence intervals.
The combined CAD translation/yaw is inconsistent
with these fits; neither conditional extrinsic above is a hardware calibration.

Established: CAD-to-head `Rz(+90°)` maps `(x,y)` to `(-y,x)` and is a proper
rotation; converting the CAD `-z` yaw joint to ROS `+z` reverses its coordinate.
Raw scans register at the recorded positive head rotation with small residual
yaw, so a wholesale reversed head-yaw sign is poorly supported. Swapping old
negative x/y values gives a vector near the fits, but a swap alone is a
reflection, and numerical proximity does not establish that failure. A wrong
physical yaw-axis location could alter the lever arm; a fixed root-position
offset cancels from the parked comparison. The old head-joint XY offset is
only 0.196 mm and cannot explain this discrepancy. Absolute scan-zero yaw is
not separately observable from these parked rotations without an external
heading/geometry constraint. The authored FOV yaw remains unverified.

The shortest settling check is to immobilize the chassis, disable patrol and
hold `0 -> +90° -> 0 -> -90° -> 0`, approximately three settled seconds at
each pose. Record `/scan_raw`, `/tf`, `/tf_static`, `/odom` and head joint/MCB
pose; fit only settled scans and inspect turning scans separately. Check return
repeatability and include one surveyed target bearing relative to the gun and
actual scan centre. That external bearing separates scan yaw from lever-arm
direction. No physical robot run was performed in round 2.

Reproduction scripts, exact scan timestamps, CSV windows, input hashes,
dependency versions and outputs are retained in
`~/ros2_ws/sentry-cad-20261026/round2/offline/`; the parent's independent rerun
is `round2/offline-parent-final/` (CSV, ICP, selection and provenance JSON are
byte-identical). Armor derivation artifacts are
`/tmp/cad-armor-round2-20261026/` and copied into the round-2 evidence directory.

### Localization geometry audit and map controls

The generated Gazebo SDF places the lidar sensor relative to `head` at
`(-0.105,-0.193326,0.101293)`, yaw -0.149534 rad as printed by sdformat.
This matches the real URDF's -0.149533673 rad within the conversion's printed
precision (0.327 microradian), rather than omitting or doubling that yaw.
Sim's body-relative head yaw becomes world head yaw in `pose_emulator`,
matching the heading-fixed `root->head` chain. RF2O composes previous/current
live extrinsics into its prior; `fixed_heading` clamps root rotation and
rebuilds laser pose through the live extrinsic. The audit found no supported
mounting-yaw/sign mismatch in these consumers.

Map regeneration at z=0.3335931 m (old nominal plane), 0.338085694 m
(old head height plus CAD lidar offset), and 0.357296694 m (new nominal plane)
produces the same PGM byte-for-byte as the checked-in map: SHA256
`f802d689183e715bd13fa06f426b0d0643ec010d7709a118cd6dd17fd98fe9ca`.
The explicit actual-field map fixture also passes 2/2. A stale map slice is
therefore unsupported as the regression explanation for this field geometry.

The initial yaw toggle holds scan-frame mask 0.32–1.62 rad fixed. At CAD yaw
this covers head bearings 0.170466327–1.470466327; at zero yaw it covers
0.32–1.62. It tests the complete yaw change, not scan-grid sampling alone.
Matched-mask controls preserve the physical sector to distinguish these effects.
All temporary URDF/launch overrides are restored after each experiment group.

The audit also identified pre-existing nonstandard RF2O pyramid sampling:
decimation centres at previous index `2*u`, but reduced-level angles span the
entire original FOV. At the 45-column level, the final centre derives from
original index 704 while its assigned angle corresponds to index 719, a
7.51° discrepancy for 720 inclusive beams. Filtering affects effective centres,
so this is a candidate orientation-sensitivity issue, not an established cause
of these results. RF2O is outside this CAD fix and was not changed.

### Opponent-visibility compatibility

Reran sim #46's seven static visibility/section tests against a scratch copy
of the new assets with #46's opponent render-mask expression. The scratch copy
changes only that expression; the active CAD branches do not incorporate #46.
The self/opponent mask checks pass. Overall result: 6/7 pass; the old
`test_head_section[0.425]` bounds fail because that upper slice is narrower
in the new CAD. These old-model empirical bounds are separate from S126's
physical armor rule and were not relaxed on the CAD branch.

| Root-relative slice z | Central silhouette min / median / max width |
| --- | --- |
| 0.275 m | 0.1400 / 0.2255 / 0.2441 m |
| 0.325 m | 0.1400 / 0.2255 / 0.2441 m |
| 0.355 m | 0.1415 / 0.2321 / 0.2520 m |
| 0.375 m | 0.1400 / 0.2317 / 0.2520 m |
| 0.425 m | 0.0980 / 0.1783 / 0.2041 m |

The scan-height neighbourhood remains within #46's historical width bounds;
the 0.425 m upper slice does not. Expanded-model tests establish masks and
mesh sections, not live renderer returns or tracker detection rates. No
combined #27/#46 tracker deployment or robot run was performed; their live
return/detection acceptance must still be repeated when those branches are
integrated. The #27 hardcoded 0.355 m output/plane remains outside this change.
Scratch fixtures and raw pytest output are in `round2/visibility/` and
`round2/visibility-tests.log` in the retained evidence directory.

### Round-2 registered tests and environment

Built with two compiler jobs in `isaac-agent-cad-r2`, Colima, domain 160,
partition `agent-cad-r2-160`. `smoke.sh` was rerun after the build to verify
the locally built packages resolve through the expected entry point. The
hosted firmware fixture is the same checked-out `8d46da5` source used in
round 1, SHA256
`2800ac7cf9835a5dd3b8049da29dec9450dce5f4da146026c4e27dbc75987c99`.
It was copied into the evidence mount and selected explicitly through
`MCB_FIRMWARE_BINARY`; firmware source was not modified. No image was built.

| Registered package results | Tests | Reported failures |
| --- | ---: | ---: |
| thornbots_pkg | 140 | 0 |
| sentry_localization | 135 | 0 |
| sim | 224 | 2: S126 case and its CTest wrapper |
| Total | 499 | 2 |

Both xacro renders pass `check_urdf`. Repository quality and
`actionlint -shellcheck=""` pass in the packages and workspace using the host
Python 3.12 venv and pinned requirements. Package repositories share the
workspace checker (`python ../.github/quality/check.py` from each package).
No quality baseline or acceptance threshold was expanded.

The initial A/B invocation encountered the registered launch-exit test's
temporary clock bridge; the suite preflight refused all experiments before
starting a stack. Those results were discarded. The recorded A/B runs began
after registered tests ended and the live-process check was clean. No foreign
container or process was stopped.

### Controlled sim A/B

All values below are localization p95 in **cm**. Three slash-separated values
are the three runs in order; parked reports the worst of each run’s 12 cells.
Round-1 rows are the earlier single runs, not new matched baseline reruns.
The drive stage has completion/diagnostic gates, not a localization-accuracy gate.

| Configuration | Parked worst-cell | Drive approach | Drive | Spin |
| --- | ---: | ---: | ---: | ---: |
| Round-1 full baseline, one run | 7.58 | 3.93 | 3.56 | 0.94 |
| Round-1 CAD, one run | 11.23 | 8.48 | 3.88 | 1.71 |
| CAD yaw -8.568°, CAD mask | 7.23 / 6.02 / 8.53 | 9.58 / 11.38 / 71.31 | 2.69 / 2.13 / 2.80 | 0.98 / 1.51 / 1.32 |
| Yaw 0°, same scan-frame mask | 6.42 / 10.08 / 7.73 | 21.78 / 23.50 / 21.47 | 6.89 / 8.01 / 9.11 | 2.65 / 3.78 / 3.54 |
| Yaw 0°, matched CAD physical sector | — | 21.75 / 20.60 / 22.17 | 8.46 / 7.64 / 6.44 | 4.37 / 3.62 / 4.13 |
| CAD yaw, old physical sector | — | 4.36 / 2.98 / 4.70 | 4.72 / 3.30 / 2.20 | 0.73 / 2.63 / 1.98 |
| CAD yaw/mask, old nominal scan height | — | 3.90 / 38.81 / 4.18 | 2.53 / 3.21 / 2.33 | 1.23 / 1.79 / 1.06 |
| Old sensor configuration, current CAD model | — | 22.10 / 21.35 / 22.96 | 8.20 / 9.12 / 10.07 | 6.51 / 6.24 / 6.84 |

The controls change only these fields from the current CAD model:

- `zero_mask`: both real/sim lidar yaw 0 and scan mask 0.170466327–1.470466327 rad, preserving the CAD mask’s head-relative sector.
- `old_mask`: CAD yaw and scan mask 0.239533673–1.559533673 rad, restoring old head-relative bearings 0.09–1.41 rad.
- `old_height`: both lidar z offsets 0.077589406 m with the CAD head height retained, restoring the old nominal world scan plane 0.3335931 m.
- `baseline_sensors`: old lidar x/y (-0.119391,-0.185010), old nominal plane, yaw 0 and old scan mask 0.09–1.41. This retains the current CAD model/head dynamics and is not a full baseline replay; the old 0.196 mm head-axis XY offset is not restored.

All 72 parked cells (six complete runs), six main drive runs and 12 control drive runs passed the native log checker, with zero lockstep timeouts. All overrides were restored, and both package worktrees are clean at their pushed heads.

The parked “roughly doubled” worst p95 is not reproducible as a stable effect: the three CAD-yaw runs span 6.02–8.53 cm, overlapping the prior 7.58 cm baseline. The drive approach remains sensitive and includes a 71.31 cm CAD outlier, which is retained.

The strongest controlled contributor is the new physical blind sector: retaining CAD yaw/height/assets while restoring the old physical sector reduces approach p95 to 4.36/2.98/4.70 cm. Zero yaw remains about 21–23 cm even with the CAD physical sector preserved, supporting scan-grid/estimator orientation sensitivity as another contributor. Restoring height has a 38.81 cm outlier, so its two small results do not establish a height fix. The old-sensor combination also fails to reproduce the full old-model baseline, leaving dynamics/startup/estimator interactions unresolved.

The matched sensor/TF poses, identical maps and controls do not support a stale-map or omitted-yaw integration bug. They also do not prove that geometry alone explains every outlier. During approach, recorded navigation error and AMCL correction are both large for the yaw-zero runs; aggregate map->root p95 cannot fully separate RF2O/EKF error from AMCL recovery. The old and new ideal field sections each contain 111 segments; endpoint/midpoint-to-opposite-section distances are at most 1.577 mm, below map raster resolution.

No mask/yaw/height rollback was committed. The CAD-derived mask encodes a proposed physical occlusion sector; unmasking that sector on hardware without checking returns could admit self returns. The remaining decision is physical mount/scan-zero/sector validation and estimator robustness work, alongside the independent armor correction. Retain the draft state.

Final full AMCL/rf2o drift rerun passes **10/10** in 138.22 s and passes the
native checker, including noise, degraded-scan recovery and parked-push cases.
The post-run process check finds no remaining stack. As in round 1,
`odom_stuck` establishes liveness rather than accurate recovery. All final
quality/actionlint checks pass, and changed local links/anchors resolve.

Signed package heads after round 2: thornbots_pkg #30
`4a9e481cee2abf2220a3807a1d21cd72317d8c87`, sim #48
`0e60c632980b756731def50dcae3a22e9cb1703d`; sentry_localization #20
remains `d4207c6a1031d9ee6075134d294e6430ca3e24ee`. All remain draft.
The round-2 container and its build/install/log volumes were removed, and
Colima stopped after no running containers remained. No foreign container
was stopped or removed. No physical robot was contacted or run.
