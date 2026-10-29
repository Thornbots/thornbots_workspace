# Sentry CAD integration — 2026-10-26

The robot measurement update below supersedes the round-1/2 lidar yaw,
self-filter and outstanding scan-zero validation. Round 2 supersedes the
round-1 muzzle choice. All CAD measurements and earlier runs remain below
as historical provenance; their results do not validate the updated pins.

**Accepted deviation (2026-10-26):** the 103.8847 mm armor lower-edge spread
exceeds the 2027 manual V1.0.0 §3.6.1.3 S124 100 mm limit (older notes below
use S126), but is accepted as a mechanical issue with no material CV impact
and is no longer a merge blocker. The test uses a temporary 0.104 m bound;
restore 0.100 m after the mechanical team fixes the plates. The ARCC 2026
base spec V1.3.0 wording remains unconfirmed; see the
[sim rule reference](../../sim/README.md#urdfsentry_v2-the-teams-low-resolution-cad).

Acceptance validation: all 29 `test_cv_bench.cpp` cases pass in the task-owned
Jazzy container, compiled directly with C++17, `cv_head_aim_core.cpp`, Eigen,
nlohmann JSON, TinyXML2 and GTest. The fresh container lacked the workspace
package installs needed for colcon. Host Python 3.12 quality and actionlint
pass for sim and the workspace; no quality baseline changed.

Input: the team's `sentry_low_res_model` Onshape URDF export, supplied as
`sentry_low_res_model.zip`, SHA256
`0841b0ca27e54125ad8d962edf78dad97ce76198bb9d3b7c69036974ba32adff`.
Only XML and STL data were read; no supplied code was executed.

The [E2E fixture diagnosis](#e2e-idle-zone-regression) below records the
restored hosted acceptance and matched nightly controls.

## Robot measurement update

The Oct 26 five-pose robot head-turn fit replaces the authored FOV-marker
yaw -0.149533673 rad with **0.5907 rad** (33.84 degrees) CCW of the gun.
The CAD lidar translation remains (-0.105, -0.193326, 0.101293) m in `head`;
its 0.220 m radius agrees with the fitted 0.2225 m radius. The scan-frame
self-filter is **-0.5585..1.0123 rad** (-32..58 degrees), verified on both
Oct 25 bags and live with zero head-return leakage. The
[measurement note](lidar-mount-2026-10-26.md) records the evidence files,
leave-one-out uncertainty, independent fits and head-turn SLAM A/B.

Only the FOV marker's orientation is superseded; every other CAD transform,
mesh, nominal height and dimension remains. The imported lidar yaw relative
to `root` is now 0.5907, 2.161496327 and -0.980096327 rad at head yaw
0, +90 and -90 degrees respectively. The old rotations below describe the
earlier CAD proposal.

thornbots_pkg #30 merges measured-mount #32, preserving its launch overrides,
xacro defaults and shared filter. Sim #48 merges the matching sim mount
update. Shared ancestry and identical lidar values keep either package merge
order from reverting the measurement. The armor-spread decision above
supersedes the earlier hold and failing-test reports below.

### Measured-mount validation

The updated combined pins are thornbots_pkg #30 `c40ca88`, sim #48
`1dc2dc2`, and sentry_localization #20 `9607e2a`. The map package merges
current nightly while retaining its CAD slice height, so integration does
not revert newer operator documentation or quality tooling.

In the task-owned Jazzy container, thornbots_pkg passes 142 tests and
sentry_localization passes 135 tests, with zero errors/failures/skips.
Sim reports 224 tests, 87 skips and the same two failure reports for the
unchanged `UrdfConstants.ArmorRules` case and its CTest wrapper:
0.103884704 m exceeds 0.100 m. The lidar TF/sensor consistency checks pass.
Host Python 3.12 quality and actionlint pass in all four changed repositories.

One AMCL/rf2o `scenario:=baseline` integration passes in 7.93 s; the native
checker accepts the console, sim and robot logs. Post-run process checks
find no remaining stack or installed nodes. This check does not replace
repeated localization-accuracy acceptance. The container and its private
volumes were removed; Colima remains running because other containers are
active. None of those containers was touched. No physical robot was run.

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

## Odometry pods

Encoder **2 = Pico Y = start-forward**; encoder **1 = Pico X = start-right**.
These are axes of the heading at power-on, not chassis-fixed axes. The
field-x (encoder 2) wheel is the **start-forward-rolling** one. In the
export's near-start-aligned interpretation it is the **rear, slightly left**
wheel (`part_18_1`); that physical part assignment is conditional on the
motor-to-CAD angular datum, which the available sources do not establish.
Geometry, firmware and recorded motion establish the mapping to start-frame
axes; the remaining CAD angular ambiguity is stated below.

Positions are axle centres in metres in imported `root` at the exported pod
pose and zero chassis/head reference yaw: +x forward, +y left, +z up.
Compose the original URDF origins at zero joint coordinates, then apply
`p_root = Rz(pi/2 - 1.72033) p_export_root + (0, 0, 0.267503694)`.
Rolling vectors below are `axle_axis cross +z`, the direction of positive
CAD wheel-joint rotation at ground contact, not the quadrature count sign.

| Export wheel / arm | Axle centre (x, y, z) | CAD positive rolling direction (x, y) | Encoder / start axis if near-start-aligned | Positive Pico displacement in field axes (red / blue) |
| --- | --- | --- | --- | --- |
| Rear, slightly left: `part_18_1` / `part_17_1`, `ode_wheel_1` | (-0.083262, +0.007841, +0.060929) | (+0.995595, -0.093757) | Y / 2 / forward | +x / -x |
| Right, slightly rear: `part_18` / `part_17`, `ode_wheel_1_1` | (-0.007321, -0.077746, +0.052861) | (+0.093752, +0.995596) | X / 1 / right | -y / +y |

The table's geometry is unconditional; its part-to-encoder column assumes
the exported pair is about 5.380° clockwise from its held start orientation.
The rolling lines are perpendicular but slightly diagonal in this pose, so
**both roll during reference-forward motion**. For 1 m along reference +x,
the CAD-positive projections are +0.995595 m (`part_18_1`) and +0.093752 m
(`part_18`). Under the table's channel assignment and measured forward/right
sign convention these become Y +0.995595 m, X -0.093752 m. A common
`ode_yaw` rotation of about +5.380° aligns these to pure forward/right axes;
a quarter-turn alternative could exchange which source part is Y or X.
These pose projections do not claim the powered robot holds the exported angle.

The mount `part_16` (`ode_yaw`, base parent) is at (0, 0, 0.087104).
Arm joints `revolute_6` / `revolute_6_1` are at
(-0.041317, +0.003891, +0.083929) / (-0.003891, -0.041317, +0.083929).
Subtract 0.267504 from z for positions relative to the yaw bearing. Rotate
wheel/arm XY positions and rolling axes about the motor-driven pod mount
when its heading changes; head yaw and chassis yaw do not define pod axes.

### Firmware and recorded-motion evidence

At MCBV3 `8d46da5`, [`pico-encoder.ino`](../../firmware/MCBV3/pico-encoder.ino)
sends `[enc1_position, enc2_position, enc1_speed, enc2_speed]`, each scaled by
`-0.024 * 2*pi / (64*4096)`. Encoder 1 uses GPIO 12/13, encoder 2 GPIO 14/15.
[`LocalizationPico.hpp`](../../firmware/MCBV3/MCB-project/src/communication/LocalizationPico.hpp)
exposes them as `getX()` / `getY()`.
[`OdometrySubsystem.cpp`](../../firmware/MCBV3/MCB-project/src/subsystems/odometry/OdometrySubsystem.cpp)
uses `fromStart(rawY, -rawX)`: red field displacement is `(Y, -X)`;
blue is `(-Y, X)`, since `getStartYaw()` returns 0 / pi. Raw `odom` and
heading-fixed `root` have these field-aligned axes. Pico's X/Y labels must
not be read as field x/y. Positive hardware counts give negative Pico
metres for both channels; firmware plus forward motion establishes the
output sign, while CAD alone cannot establish quadrature phase.

`getOdoEncoderValue()` is `fmod(motor_position + encoderOffsetOdo, 2*pi)`,
with `encoderOffsetOdo = -0.25 + pi/2` (about 1.320795 rad, firmware pi).
[`OdometryPointForwardsCommand`](../../firmware/MCBV3/MCB-project/src/subsystems/odometry/OdometryPointForwardsCommand.hpp)
controls `head_world_yaw - head_encoder_yaw + odo_encoder_yaw` toward
`-chassis_angular_velocity/200`; at rest its target is zero. Thus the pod
motor counteracts chassis yaw and holds the start heading. At rest,
`motor_position ≈ head_encoder_yaw - head_world_yaw - 1.320795` modulo 2*pi.
`getStartYaw()` rotates the resulting displacement into field axes; it is not an additional
CAD motor angle. The source provides no motor-position-to-`ode_yaw` zero
relation. Its calibrated 1.320795 rad offset cannot simply be substituted
as a CAD joint angle, so the held-start CAD pose and unique part-to-channel
assignment cannot be recovered from these constants alone.

Oct 25 recorded-motion evidence: `~/ros2_ws/odom-x-deeper-20261025/REPORT.md`
and `csv-step-analysis.json`, independently checked against
`~/ros2_ws/robot-session-20261025/step2-attempt3/step2c-yaw.csv` and
`step2-attempt4/odomtest.csv`. The CSVs reproduce 1,780 / 3,834 finite rows
and x ranges [-4.6251, -3.7368] / [-4.6251, -2.2243] m. On the reported red
forward legs x increases: attempt 3 at wall time 1792955106.639–5106.839 has
(dx, dy) = (+0.1435, -0.0006) m; attempt 4 at 1792955628.463–5628.663 has
(+0.1594, +0.0054) m. A strafe sample at 1792955110.639–5110.840 has
(0, -0.1892) m. The documented straight return also counts negative x;
subsequent selective x loss after strafes does not change the channel mapping.
Invalid/nonfinite rows are excluded, not repaired; these are sampled `/odom`
positions, not direct encoder traces or a measured calibration of CAD yaw.

Confidence is **high for geometry and for encoder/start-axis/field-sign
mapping**, supported by geometry + firmware + recorded motion. The missing
motor-to-CAD datum limits confidence in assigning `part_18` versus
`part_18_1` to those channels; the near-aligned assignment in the table is
an explicit inference, not a wiring observation. No new robot run was made.

Neither pod mount, arm nor wheel survived round 1 as a separate link, joint
or mesh in `thornbots_pkg/urdf/sentry.urdf.xacro` or sim's active
`sentry_v2.urdf.xacro` / included `sentry_v2/sentry_v2.urdf`. The imported
root mesh contains only `base`; `wheel_0` through `wheel_3` are retained
drive wheels. Nothing is renamed or added to the models. If pods are later
imported with their angular datum established, use `odom_pod_yaw_mount`,
`odom_pod_y_enc2_arm` / `odom_wheel_y_enc2` and
`odom_pod_x_enc1_arm` / `odom_wheel_x_enc1`, preserving the start-frame meaning.

### Pod documentation validation

Validated in task-owned `isaac-agent-odom-pods-20261026`, domain 127, after
merging the measured-lidar work (`thornbots_pkg c40ca88`, `sim 1dc2dc2`) and
the separately accepted armor-deviation check (`sim 2719de8`). The final
build and both xacro/`check_urdf` renders pass. Registered package results:
thornbots_pkg **142**, sim **224** tests, zero failures/errors/skips. The
first sim run lacked the hosted-firmware environment and skipped 87 cases;
the final run sets `MCB_FIRMWARE_BINARY` and supersedes it. Earlier armor
failures are superseded by the separately authored acceptance, not a pod edit.

Hosted E2E stages **did not pass**: parked failed setup waiting 60 s for a
valid `/cv/target_state` (all 12 cells unscored); drive at
`real_time_factor:=1` failed to reach center and fired no shots (0/1), with
zero lockstep timeouts. Both native log checks reject the runs. The merged
idle aiming now faces the enemy zone instead of sweeping; a parked-fixture
acquisition mismatch is a candidate, not an established diagnosis. These
results do not establish integration acceptance. Pod edits affect only docs;
no motion, aiming, fixture, geometry, plugin or topic changes were made here.

Host Python 3.12 quality and `actionlint -shellcheck=""` pass in both packages
and the workspace; added local links/anchors resolve. The initial two-job
cold build was OOM-killed; a serial build succeeds after the repository's sim
dependency installer supplies missing development packages. Evidence,
geometry derivation, independent CSV summary/input hashes and logs are at
`~/ros2_ws/sentry-cad-20261026/odom-pods/`. The hosted ELF is the unchanged
round-2 MCBV3 `8d46da5` fixture (SHA256 `2800ac7cf9835a5dd3b8049da29dec9450dce5f4da146026c4e27dbc75987c99`).
No robot was run. Final process checks are clean; the task container and its
volumes were removed. Colima remains for other active containers, untouched.

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

**Superseded 2026-10-29:** `camera` is the RGB FOV apex, (0.095700, 0.032500,
0.055000) in `head_pitch`, 44 mm left of the IR apex below.
`/cv/panel_detections` are deprojected with the colour intrinsics, so the
IR apex put real-robot aim points to the right of the panels.

The IR FOV mesh has its apex at the `ir_fov` link origin. That apex, rather
than the sensor housing centre or the separate RGB apex, defined the camera
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

## E2E idle-zone regression

The parked acquisition failure is a shared fixture-frame mismatch after
thornbots_pkg #28 removed patrol sweeps, rather than a CAD visibility limit.
Hosted parked paths lie toward world -y, but the blue team's default idle
goal is (-4.625, 0, 0.15), along -x. The detector stand-in applies the camera
FOV even without rendering a camera; those directions differ by 90 degrees,
outside its 87-degree horizontal FOV. Its capture-time TF frame names remain
unchanged. Treating the generic sim spawn heading as the strategy frame was
an invalid fixture assumption.

Using freshly built firmware, workspace `52489c0` produces 5,701 empty panel
arrays and no TargetState during parked bring-up. Both the initial nightly
control `c3ae0e8` and updated nightly `8963533` fail the same acquisition wait.
All three original configurations pass drive, including center arrival and
shots; the reported drive failure was not reproduced. In particular, the
original CAD drive records 31 shots and 29 hits, with zero lockstep timeouts.

The fix forwards the existing `zone_start_x_m` and `zone_start_y_m` node
parameters through `auto.launch.py`. Only hosted parked selects the idle
zone in its existing -y scene. Board parked, driving stages and robot defaults
retain the field-frame goal. Paths, spawn, movement, firmware, CAD geometry,
measured lidar mount/filter and all scoring gates are unchanged.

A diagnostic A/B that instead rotated the paths restored acquisition, but
was rejected: the lateral footprint at (-1.3, 1.9) comes within 0.104 m of
field geometry, failing the existing 0.40 m clearance test. No rotated path
or relaxed clearance bound is committed. Its logs remain as rejected
experiments, not acceptance evidence.

Evidence is retained on the mini under
`~/ros2_ws/sentry-cad-e2e-fix-20261026/`. The earlier attempt used
`isaac-agent-cad-e2e-fix`, domain 155, partition `agent-cad-e2e-fix-155`.
Runs use the documented `sim/tools/run_suite.sh` with `backend:=hosted`,
full default cells/durations and native log checks. The fresh hosted build
from pinned MCBV3 `8d46da5` has SHA256
`2800ac7cf9835a5dd3b8049da29dec9450dce5f4da146026c4e27dbc75987c99`,
identical to round 2. Earlier auxiliary runs used a different existing ELF
(`9b0a1df835553b000b1575b1bf7734e86d1ba931ad9f242c76c28964fc03e511`)
and are labelled separately. These hosted runs do not establish board or
physical-robot acceptance.

### Resumed validation

Resumed from the pushed package fix, without recreating its commits:
thornbots_pkg #30 `6a30764e6d7fb631f0bc76a64b02602b570977f2` and sim #48
`6dc64ae12fc9a9094dd558c85bef63f9bb461ad6`. Both already merge current
package nightly. sentry_localization #20 remains
`9607e2a717658094063335133beda67818d8271c`, which also contains its current
nightly. Workspace #103 had not yet pinned the fix; its starting head was
`e4d512da7a28e17570b24f9dfd5cc2cb15f28773`. The earlier original-CAD run
at `52489c0` remains applicable: the intervening sim pin changes documentation,
comments and the armor-rule assertion, with no E2E runtime change.

Fresh runs use task-owned `isaac-agent-cad-e2e-resume`, domain 122, partition
`agent-cad-e2e-resume-122`. Evidence on the mini is
`~/ros2_ws/sentry-cad-e2e-resume-20261026/`; each stage directory contains
`console.log` with the native checker verdict, `status`, and `details/`
with stack, pose, shot and score logs. `results.json`, manifests and saved
patches identify each configuration. Every run selects the same pinned hosted
ELF SHA256 recorded above. No board or physical robot acceptance is claimed.

- Exact current workspace nightly `8963533`, using its pinned package heads:
  `nightly-original-mcb_parked` fails acquisition in 71.81 s, all 12 cells
  unscored. Its observer sees 5,655 panel arrays, only four briefly nonempty,
  and zero valid target states. `nightly-original-mcb_drive` passes in 30.64 s
  with 34 shots and 94.12% hits. Thus current nightly is not a passing parked
  control after patrol removal.
- Nightly plus only the idle-zone launch wiring, with identical compiled
  nodes, geometry, paths and map: `nightly-idle-mcb_parked` passes 12/12 in
  234.26 s, 420 shots, minimum cell hit rate 70.97%, worst localization p95
  3.224 cm and maximum chassis displacement 1.389 mm.
  `nightly-idle-mcb_drive` passes in 34.35 s, 34 shots and 91.18% hits.
  Saved patches contain only eight added sim launch lines and twelve added
  robot launch lines; this is the minimal one-factor A/B.
- Pushed CAD fix: `cad-fixed-mcb_parked` passes 12/12 in 255.44 s, 413 shots,
  minimum cell hit rate 50%, worst localization p95 5.489 cm and maximum
  chassis displacement 2.378 mm. `cad-fixed-mcb_drive` passes in 35.86 s,
  35 shots and 91.43% hits. All native checkers accept these fixed/control
  runs, with zero lockstep timeouts and unchanged acceptance gates.
- Matching the earlier failing drive timing, `real_time_factor:=1` also
  passes on exact nightly (`nightly-original-rtf1-mcb_drive`, 38.19 s,
  37 shots, 94.59% hits) and CAD (`cad-fixed-rtf1-mcb_drive`, 39.82 s,
  11 shots, 100% hits). Both reach center, pass the native checker and have
  zero lockstep timeouts. The reported drive failure remains unreproduced;
  these results do not establish its original cause or repeated combat accuracy.

The detector stand-in explicitly applies the camera intrinsics/FOV to truth
panels; a rendered camera or mesh width is not needed for this failure.
The frame names and pitch convention remain unchanged. Correcting only the
idle direction restores target state with both geometries, so reverting CAD
head height, camera apex, pitch, muzzle or armor poses is unsupported.
Independent review on archlinux checked both exact package heads and all six
stage/backend branches: only hosted parked selects the scene override.

The drive completion verdict is diagnostic, not a localization-accuracy gate.
The fresh CAD default-speed run retains an approach localization p95 outlier
of **33.03 cm**, then 3.775 cm during drive and 1.787 cm during spin. At RTF 1
these are 7.101, 2.950 and 0.811 cm. Exact nightly's approach p95 is 3.849 cm
(default speed) and 3.288 cm (RTF 1). This remains consistent with the earlier
startup/localization variability; the idle-zone correction does not resolve
that separate sensitivity. No localization tuning or movement change was made.

After restoring the exact pushed CAD heads, the final serial build and all
**501 registered tests pass**, with zero errors, failures or skips. Logs are
`restored-cad-build.log`, `final-package-tests.log` and
`final-package-results.log` in the resumed evidence directory. The initial
cold parallel build was OOM-killed; the serial retry succeeds. No quality
baseline or acceptance threshold changed. The final process check found only
init, sleep and this domain's ROS CLI daemon; the task container and its
private volumes were removed. Pre-existing containers were untouched, so
Colima remains running for them.

Host Python 3.12 quality and `actionlint -shellcheck=""` pass in the workspace,
sim, thornbots_pkg and sentry_localization; changed local links/anchors resolve.
