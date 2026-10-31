# Flipped lidar mount — 2026-10-31

The team flipped sentry's lidar upside down to lower the scan plane and
exported a new `sentry_low_res_model` (SHA256
`0ae239a37fae038f98be52ae93456841a9f8abeb85ad94700af4ad0f2784391d`). This
supersedes the [Oct 26 upright mount](lidar-mount-2026-10-26.md). Maintained
values live in the [filter owner](../../thornbots_pkg/README.md#lidar_self_filter).

## CAD comparison

Forward kinematics of both exports, in the gun-aligned `head` frame:

| | Oct 26 | Oct 31 |
| --- | --- | --- |
| Scan-plane reference (m) | (-0.105, -0.193326, 0.101293) | (-0.0056, -0.193326, 0.063707) |
| Radius / bearing from gun | 0.220 m / -118.5° | 0.1934 m / -91.7° |
| Lidar body z | up | down |

Chassis, armor, wheels and pitch-group parts (gun, RealSense, FOV apexes)
agree within 0.5 mm; the export only changed the head yaw/pitch pose and
replaced `lpr_yaw` with one `head` part. Scan height above the CAD root datum
drops 37.6 mm, to 0.3312 m. Only XML and STL data were read.

## Robot measurement

Parked in a room on `ts-nano-sentry`, stack on the old values, read-only
probes, one head pose (yaw 179.7° in `root`), level pitch:

- RealSense depth points at lidar height vs `/scan_raw`, fraction within
  5 cm: current old-CAD TF 0.052; unmirrored best 0.238; **mirrored with the
  new CAD translation 0.751 at 147.75° CCW of the gun**; mirrored with the old
  translation 0.596. The scan is mirrored, so the driver's `inverted`
  (exactly `a -> -a`, `sllidar_node.cpp`) is needed; yaw is then 2.579 rad.
- Self-occlusion in `/scan_raw`: no return or <0.2 m hits at 14.8..105.4°.
  Under the fit this is 43..133° from the gun; the new CAD head wall slices
  at 51..124°, centres agreeing within 0.25°. In the inverted frame the
  filter is -110.4..-9.8° (5° margin), i.e. -1.927..-0.171 rad.
- AMCL was unusable (yaw sd 14°) and the old filter passed head hits at
  61..66° and 73..75°.

Not yet measured: nose-up/down sectors, a head-turn yaw fit (single pose,
≈±1° here), and the floor-to-scan height that sets the
[map slice](../../sentry_localization/README.md) (still 0.357296694 m).
The sim head mesh still shows the upright lidar; sim's sensor ignores it.
