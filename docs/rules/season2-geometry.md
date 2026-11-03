# Season 2 figure geometry and chassis power evidence

This is the maintained transcription of E27 event-map figures, subordinate to
[the rules context](../ARCC_2026_SENTRY_CONTEXT.md#which-rules-govern).
It describes source evidence, not an accepted simulator/map implementation.
Open acceptance lives only in [DOC14g](../ROADMAP.md#issues-found) and
[RULES-S2](../ROADMAP.md#additional-mini-work).

## Coverage and authority

Fetched 2026-11-03 UTC from the [2027 manuals page][manuals]. E27 and BS27
are V1.0, dated 2026-11-01. PDF page numbers below are **1-based physical PDF
pages**, which equal the printed page numbers for the cited figures.
All dimensions are **mm**, angles degrees, power W unless specified.
Text extraction was checked against rendered E27 pp.16–24, 37–38, including
arrow endpoints; coordinates below never come from measuring image pixels.

| Canonical commitment | Evidence completed here | Acceptance boundary |
| --- | --- | --- |
| DOC14g event geometry | Every figure 3-3–3-13 (pp.16–24), 4-3–4-4 (pp.37–38), including printed placement chains below | Nominal transcription; ambiguities remain explicit, no package acceptance |
| RULES-S2 Tournament geometry | Corner starts, marked bunker corners, dimensions and derived placement below | Implementation/acceptance stays with package owners |
| RULES-S2 chassis audit | E27 Table 3-4 p.13: 80; Table 5-2 p.40: 120; read-only implementation audit below | No firmware/default changes or electrical compliance proof |
| DOC14g publication checks | Manuals page lists only Season 2 Participant, Building and Events V1.0; BS27 mounting instructions extracted below | Site Manual, dot-matrix appearance/dimension authority and detailed zig-zag shape have no newly published authority in these sources |

Reproducible source fingerprints (SHA-256 of downloaded bytes):

- [E27][e27]: `9499085844981cffabfe50442e12858c716b28a78f2341364405f9ffc8bfb21b`.
- [BS27][bs27]: `d0b6ecbb1b1011a94e5146e34b271731bbbe10aefcd1613f4a79755f38a42c29`.

E27 §3.2 p.13: component dimension tolerance ±10%, except dimensions under
100 mm use ±5 mm; structure angles ±3°, component angles ±1°, unless stated
otherwise. §4.2 p.35 applies the same battlefield caveats to 1v1; §5 p.40
inherits 1v1 for Sentry Tournament. These are nominal drawings, not surveyed
clearances or independent tolerances on each derived coordinate.

## Coordinate convention

For transcription, origin is the **inside lower-left floor corner** of each
plan as printed. `u` points right, `v` up the page, `h` vertically up.
3v3 central line is `u=6000`, lower edge is the resupply wall; mirror red to
blue with `(u,v,h) -> (12000-u,v,h)` (E27 p.15 and Fig 3-3 p.16).
This is a reflection, not a heading-preserving rigid transform.
A field-centred ROS frame with +x right, +y up the plan and +z up is
`(x,y,z)=((u-6000)/1000,(v-4000)/1000,h/1000)` for 3v3;
use 2500 offsets for Tournament. These are **derived choices**, not E27 axes.

BS27 §3.6.1 p.43 defines a robot-body construction frame at centre of mass,
+X along a maximum-efficiency chassis direction, +Z toward Earth.
With the same physical +X and origin, converting this right-handed frame to
ROS +Z up requires `(x,y,z)=(X,-Y,-Z)`; merely negating Z is a reflection.
The plan frame is not that body frame; body pose/origin must be supplied.

## 3v3 placement chains — E27 Fig 3-3, p.16

The following intervals/points are **derived from labelled arrows** in this
figure and component dimensions cited below. Red half only; mirror as above.
No dimension is inferred from how many pixels a feature occupies.

| Feature | Printed chain / derived nominal placement | Qualification |
| --- | --- | --- |
| Inside arena | 12000 × 8000; half-width 6000 | Perimeter height 500 in front elevation; perimeter thickness not explicitly dimensioned |
| Central High Ground | Left ramp starts `u=3716`; total 4568 (Fig 3-5); `v=6000..8000` | Derives ramp/plateau intervals `3716..4500`, `4500..7500`, `7500..8284`; cube centre `(6000,7000)` from 1000 arrow and §3.2.4.2 |
| Resupply / start | `u=0..1500`, `v=0..2000` | §3.2.2 p.16 / Fig 3-4 p.17: measured to **outer tape edges** |
| Side High Ground | Left edge 2000 from left wall; near edge 1000 from lower wall; far edge 3000 from lower wall | Fig 3-6 p.19 gives 1000 width, two 1000 tiers; upper `v=1000..2000`, lower `2000..3000`; pole centre `(2800,2800)` derives from 200 inset arrows |
| Side Limbo Bar | Left edge `u=2430`, from lower wall toward Side High Ground; 1000 clear opening | Fig 3-13 p.24 gives 140-wide bar, hence nominal `u=2430..2570`; spacer positions not dimensioned |
| Side Wall | Length 2000 from left wall, thickness 170; lower/near (resupply-facing) face `v=3915` | Derived `u=0..2000`, `v=3915..4085`; thickness extends toward +v; height 422 |
| Side L-shaped Bumpy Road | Left edge `u=1100`, right edge `u=2700`; top `v=6800` from 1200 setback; total depth 1600 | Vertices `(1100,5200),(2700,5200),(2700,6800),(1900,6800),(1900,6000),(1100,6000)`; upper arm 800 wide, notch 800 deep |
| Central Bumpy Road | Lower edge `v=3000`; depth 1600; printed red width 3200 runs from the L-road right-edge extension `u=1100+1600=2700` to the central-wall base left face | Centred 170-wide base gives face `u=5915`, hence span 3215: **15 mm nominal conflict**, detailed below; no unique exact interval |
| Central Wall | Base length 3000, thickness 170, height 422; upright panel length 2559, total height 1406 | `u=5915..6085` for base. Limbo opening 600 is face-to-face (Fig 3-12); absolute v position depends on post face convention, not simply `6000-600`. Panel end offsets/thickness not separately dimensioned |
| Bucket / Objective B | Centre `(6000,1000)` | On central line; 1000 arrow to centre, not bucket edge |
| Scoring Area | 800 arrow from left wall to outer tape left edge; 850 from upper inside wall to outer tape top edge | Fig 3-7 shows 300 platform and tape 50.8 outside. Derived platform `u=850.8..1150.8`, `v=6799.2..7099.2`; outer tape `u=800..1201.6`, `v=6748.4..7150` |
| Pipe Chute | 850 arrow from left wall to plate left edge; plate 200 wide (Fig 3-7) | Derived centre `u=950`, height 600; **not** Scoring Area centre `u=1000.8`. §3.2.4.1 says “directly behind”, without resolving this 50.8 difference |

The side-view Fig 3-7 p.20 also labels 850 **between the near edge of the
Scoring Area and the wall**. That agrees with Fig 3-3's outer tape setback
only if the side-view edge is the outer tape edge; it must not silently be
reinterpreted as an additional centre offset. Preserve this endpoint
qualification when generating penalty-zone geometry.

## Component drawings — E27

| Figure / PDF page | Full printed dimension inventory and meaning |
| --- | --- |
| 3-4 / 17 | Starting Zone 1500 × 2000, tape width 50.8; outer-edge convention above |
| 3-5 / 18; §3.2.3 p.17 | Central High Ground plateau 3000 × 2000, top 210; two 784 **horizontal** runs at 15°; total footprint length 4568 |
| 3-6 / 19 | Side High Ground 1000 wide, two 1000-long tiers; tops 210 / 410 above floor, not a 410 rise above lower tier; pole centre 200 from each indicated lower-tier edge |
| 3-7 / 20; §3.2.4.1 p.19 | Scoring platform 300 × 300 × 50; tape 50.8 outside platform; chute plate 200 × 200, hole Ø52.5, centre height 600; side-view gap 850 |
| 3-8 / 21; §3.2.4.2 p.20 | Cube 100 × 100 × 100; chamfer pictured but not dimensioned |
| 3-9 / 21 | Bucket Ø200 × 250 high; ten pipes (5 each colour), length 500, Ø26.7, nominal 3/4-inch Schedule 40 PVC; no bucket wall thickness or pipe arrangement dimensions |
| 3-10 / 22 | Donut Ø100 outside / Ø50 inside, thickness 25; depicted overall height 456 from base underside to pole top, base drawn 250 wide; bend shape, diameter and base thickness not dimensioned |
| 3-11 / 23; §3.2.5 p.22 | Tile 400 × 400 × 2.5, four ribs raised 1.2; rib length 350, side margins 25, width 53.8, gaps 45, first top margin 25; rounded rib end profile pictured |
| 3-12 / 24; Table 3-5 p.23 | Central Limbo clear height 420, face-to-face opening 600; bar cross-section 88.9 horizontal × 38.1 vertical; post shown without its own dimension chain |
| 3-13 / 24; Table 3-5 p.23 | Side Limbo clear height 300, opening 1000; bar cross-section 140 horizontal × 38.1 vertical; upper bar and spacers pictured without independent mounting dimensions |

### Cross-figure reconciliation

- Fig 3-3 p.16: the 3200 arrow shares its left extension with the
  L-road's 1600 right-edge extension, fixing that endpoint at `u=2700`.
  The centred wall-base chain fixes the right endpoint at `6000-170/2=5915`.
  Thus `5915-2700=3215`, conflicting with the printed 3200 by 15.
  Keeping the L-road endpoint and printed width instead gives `2700..5900`;
  keeping the centred wall face and printed width gives `2715..5915`,
  shifting the shared endpoint 15. Mirroring gives respectively
  `6100..9300` or `6085..9285`; keeping both endpoint chains gives
  `6085..9300` (span 3215). These are alternative implementation choices,
  not equally exact transcriptions. This audit selects none; an owner must
  record which constraint it relaxes. General tolerance does not resolve
  the conflicting nominal chains, and averaging would invent new endpoints.
- Fig 3-3 p.16: Side Wall `3915+170=4085`; its near face, not far face,
  terminates the 3915 arrow. Reflection keeps the same v interval.

- `784 + 3000 + 784 = 4568`, and `3716 + 4568/2 = 6000`:
  Central High Ground agrees with the field centreline.
- `atan(210/784) = 14.995°`: the rounded rise/run agrees with 15°;
  the sloping surface length is derived ≈811.64, **not** the 784 run.
- `25 + 4*53.8 + 3*45 + 25 = 400.2`: rib chain differs from tile size
  by 0.2. Retain printed values; do not rewrite width or spacing to force
  exact closure (well within the stated component tolerance).
- Side High Ground tier lengths `1000+1000=2000`; pole insets place it
  inside the lower tier. Central wall panel length leaves `3000-2559=441`
  total base overhang; equal 220.5 end overhangs are an implementation
  symmetry assumption, not independently printed dimensions.

## Sentry Tournament — E27 Figs 4-3–4-4, pp.37–38

Fig 4-3: inside square 5000 × 5000; red start `u=0..1000,v=4000..5000`,
blue start `u=4000..5000,v=0..1000`. These are derived intervals from the
corner rectangles and four 1000 labels. No tape width is specified here.

The black marked points locate **corners of the bunker footprint**, not
centres or centreline endpoints. Derived coordinates in this document's
plan frame:

| Marked corner | Printed horizontal / vertical chains | Derived `(u,v)` |
| --- | --- | --- |
| Left bunker lower-left | 1400 from left, 2150 from bottom | (1400,2150) |
| Left bunker upper-left | 2000 from left, 2050 from top | (2000,2950) |
| Right bunker lower-right | 2000 from right, 2050 from bottom | (3000,2050) |
| Right bunker upper-right | 1400 from right, 2150 from top | (3600,2850) |

Fig 4-4 gives each bunker **1000 length × 170 thickness × 422 height**.
The marked long edge vector is `(600,800)`, length exactly 1000,
orientation derived `atan2(800,600)=53.130102°`. The drawn thickness extends
toward +u/−v for the left bunker, −u/+v for the right bunker. The following
footprints are derived by adding the perpendicular vector of length 170:

- Left: `(1400,2150),(2000,2950),(2136,2848),(1536,2048)`;
  centre `(1768,2499)`.
- Right: `(3000,2050),(3600,2850),(3464,2952),(2864,2152)`;
  centre `(3232,2501)`.

A 180° rotation about `(2500,2500)` maps one footprint onto the other.
Treating the marked points as bunker centres would shift the collision box
85 mm perpendicular to its length. This derivation uses Fig 4-4 thickness;
it is not an independently specified centre/yaw or a surveyed tolerance.

## Publication evidence — BS27 and manuals page

BS27 §2.1.4 p.10 explicitly defers the dot-matrix display's “specific style”.
BS27 §3.6.2 pp.46–47 **does publish mounting procedure**: four equal hole
sets, official frames secured with at least two M4 screws each, module slots
engage lower/upper catches, one M4 fastening screw per frame, supplied 6-pin
series cable. S103/S104 and the frame introduction are on p.42; S105 is on p.43.
They allow rear/bottom mounting face and forbid modifying the official frame.
Page 48 separately says detailed mounting steps are subject to later update;
the published pp.46–47 procedure is not a guarantee of final completeness.
Those published facts must not be called unpublished.
The illustrations supply no dimensioned panel outline or mounting-hole
pitch; the old 135 × 125 team CAD prior is not verified dot-matrix geometry.

E27 §3.2.4.4 p.22 explicitly defers additional zig-zag pole details despite
publishing height/base width. The 2027 manuals page currently lists three
V1.0 manuals, no Season 2 Site Manual. Its embedded older 2026 Site Manual
entry is not Season 2 authority. Absence from this page is a publication
check, not proof that no captain announcement/Q&A exists. Conflict precedence
and remaining external acceptance are maintained in the linked context and
canonical roadmap.

## Chassis power audit — read-only, 2026-11-03

Inspected workspace nightly `9bfd4edc06be5585bd26a5b75a8bfece47c2fdb3`,
MCBV3 pinned `a16c9aae5650b038441527b3bb8972d5d15ac775`, sim pinned
`7079a7d0160db5c2ceb8ab1b8c81d25b2d379439`. Also read foundation heads
sim #63 `03ade7d170d8a4a496734bfe455327f63ab20b5a`, MCB #131
`8125d4677e12e02397c5c90098796990fb11a565`; the drivetrain files below
are unchanged between those MCB refs. These are observations at exact refs,
not a claim about later foundation edits.

| Source path (relative to package) | Observation / implication for owner |
| --- | --- |
| MCBV3 `MCB-project/src/subsystems/drivetrain/DrivetrainSubsystemConstants.hpp:26` | SENTRY `INITIAL_POWER_LIMIT_3V3=100`, unlike E27's 80; shared `DEFAULT_POWER_LIMIT=45` is initial object state, not a verified event cap |
| MCBV3 `MCB-project/src/subsystems/drivetrain/DrivetrainSubsystem.cpp:56–62` | `minLimit=240`; only receiving RMUL_3V3 in INITIALIZATION/COUNTDOWN selects startup constant; effective base is `min(minLimit, referee powerConsumptionLimit)`. Live 80/120 referee values can constrain it; this does not validate stale/missing/wrong data or establish an explicit Season 2 Tournament mode |
| Same file `:87–102` | Translation may add 20 with buffer >30, subtract 10 at ≤15; position mode subtracts 10 at ≤10. Buffer-assisted transient power is distinct from nominal cap; requires owner's energy/limiter acceptance, not a blind 80 clamp |
| MCBV3 `MCB-project/src/subsystems/drivetrain/ChassisController.cpp:151–178` | Model-based current/torque limiting uses requested power; source inspection cannot prove measured electrical compliance |
| Sim `include/sim/mcb_firmware.hpp:168–180` | 0x0201 synthetic robot status sends fixed **240** power limit; 0x0202 sends zero measured draw and 60 buffer. No 80/120 event selection here; cannot establish buffer-exhaustion/overlimit acceptance |
| Sim `include/sim/mcb_firmware.hpp:123–150`, `src/mcb_firmware_system.cpp:63` | `chassis_power` is a boolean referee output flag, not a numeric watt setting |

E27 §3.3.1.4 pp.27–28 specifies the 60 J buffer, 10 Hz accounting and
5-second cut when exhausted while overlimit; Sentry's nominal limit is
80 (Table 3-4 p.13), overridden to 120 for Tournament (Table 5-2 p.40).
The commented chassis-power gate in `DrivetrainSubsystem.cpp:52–53` is also
nonstandard unfinished safety code; this audit does not certify BS27 S101
hardware cutoff. Route changes to the foundation/firmware owners.

### Foundation geometry comparison evidence

Read-only comparison against sim #63's `world/arcc_s2_3v3/cad/NOTES.md`
and `arcc_3v3_field.py` reuses its figure authority. It already identifies
scoring/chute offset, post-face placement and placeholder pole. Its
perimeter 170 thickness, central panel 25 thickness, 400 green pad, bucket
wall and pipe arrangement are implementation estimates, not newly verified
E27 dimensions. Central panel equal end overhang and the post thickness
used to place the wall also require that distinction. No shared generator,
mesh, fixture, route, controller, localization file or test is changed here.

[manuals]: https://www.arc-robotics.org/participants/2027-manuals
[e27]: https://www.arc-robotics.org/_files/ugd/6f41a3_caec30f4845b4904a45ddeb6338510ca.pdf
[bs27]: https://www.arc-robotics.org/_files/ugd/6f41a3_dbe73f66c9cf4630bad6046b379736e5.pdf
