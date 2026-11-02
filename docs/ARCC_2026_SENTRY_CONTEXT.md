# ARCC rules: Sentry-relevant context

CV detection/tracking comes first. This is the workspace's rules context;
[ROADMAP](ROADMAP.md) owns priorities and package READMEs own implementation.
Values below are rules, except the explicitly labelled team assumptions.
The file name predates Season 2; it is kept so incoming links stay valid.

## Which rules govern?

Checked **2026-11-01** against ARC's [2027 manuals page][arc-2027]:

- **ARCC Season 2 (2026–2027), event 2027-06-13 to 06-20** ([P27][p27]
  Table 2-1): Events Manual **V1.0** ([E27][e27]), Robot Building
  Specifications **V1.0** ([BS27][bs27]) and Participant Manual **V1.0**
  ([P27][p27]), all **2026-11-01**. The **Site Manual** (match formats,
  venue) is not yet published.
- **Self-contained:** E27 §1.1 says only Season 2 manuals and Season 2 Q&A
  apply, “even where a rule appears unchanged”; RoboMaster Q&A from any
  season does not apply (§1.2). BS27 is a full ARC document, not an
  RMUS-plus-overrides diff like A26. Conflict order: captain's meeting/ARC
  announcements > Q&A > Site > Events > Participant > Building Specs.
- **Superseded:** ARCC 2026 Events Manual V1.6 ([E26][events]) and Building
  Specifications V1.3.1 ([A26][arc-build]) over Chinese RMUS 2026 V1.3.0
  ([B26][build26-zh]). The “2026” columns below cite them only to show what
  changed; the English-basis gap noted against B26 no longer matters.
- **Sentry events:** the Sentry plays in the **3v3 Tournament** (Hero,
  Engineer, Sentry) and in a new standalone **Sentry Tournament** (Sentry
  1v1, below). Infantry plays only the 1v1 Tournament.

## Sentry limits, autonomy and combat (3v3)

| Rule / code constraint | ARCC Season 2 basis | Change from ARCC 2026 |
| --- | --- | --- |
| Autonomy / communication | E27 §3.1.3, Table 3-4: fully autonomous, no pilot, no inter-robot communication; at most one debug remote | Same (E26 Table 3-4) |
| Debug remote removal | E27 R24, §9.4: after Setup, place it in the designated area; no commissioning from start of 5-second countdown. R25: no operating remotes from outside after the countdown | Same; was E26 R23 |
| Launcher / speed | E27 Table 3-4: one 17 mm launcher, ≤25 m/s | Same |
| HP / chassis / heat | E27 Table 3-4: 400 HP, **80 W**, heat limit 260, cooling 30/s | **Chassis 100 W → 80 W** |
| Ammo / duration | E27 Table 3-4, §3: 750 initial allowance, cannot increase; Gold buys only 42 mm (§3.3.3); 3-minute Setup, 5-minute Battle (Table 9-2) | Same |
| Heat accounting | E27 §3.3.1.3, Fig 3-14: +10 per 17 mm shot, cooling at 10 Hz (−3/tick); Q1>260 locks until Q1=0; Q1>Q2=360 locks for the game | **Prose and flowchart now both use `>Q2`**, so 360 itself is not a game lock (E26 prose/flowchart disagreed) |
| Overspeed locks | E27 §3.3.1.2, Table 3-9: excess (0,5) m/s →15 s; [5,10) →20 s; ≥10 →rest of game | Same |
| Armor hit registration | E27 §3.3.1.1, Table 3-7: 17 mm normal component **>12 m/s**, minimum detection interval 50 ms | Same |
| Damage | E27 Table 3-8: 17 mm 20 HP, 42 mm 200 HP, collision 2 HP; collision damage is forbidden (R45) | Same 17 mm / collision values |
| Chassis overlimit | E27 §3.3.1.4, Fig 3-15: 60 J buffer, 10 Hz accounting; exhausted while over →5 s chassis power cut | Same |
| Main controller offline | E27 §3.3.1.5.1, Table 3-10: launcher/gimbal/chassis off; −5% max HP/s; RFID off; no damage detected; respawn stops. Mini PC keeps power when defeated (§2) | Same core effects |
| Armor / supercap module offline | E27 §3.3.1.5.2, Fig 3-16: −4×N HP each 500 ms | Same |
| Speed monitor offline | E27 §3.3.1.5.3: launcher loses power until it reconnects | Same |
| Healing / revival | E27 §3.3.2: own Resupply Zone heals 25% max HP/s; revival 5 s, +5 s per later defeat; heat 0 and buffer full on defeat; revive at 20% HP, **10 s** Invincible, Weakened (launcher locked) until own Resupply Zone, which clears both | **Invincibility 30 s → 10 s**; no capture restriction (no Capture Point) |
| Yellow Card on Sentry | E27 §10.1.2, Table 10-2: chassis off 2 s, −15% max HP (others −5%); a repeat within 30 s doubles the loss; three Yellow Cards = Red Card | Same baseline; was E26 Table 8-2 |
| Penalty Zones | E27 R48, §10.2.3.2: opponent Resupply Zone and **both** Scoring Areas; any part on or above the zone; >3 s →Yellow Card, then one per 10 s | **Scoring Areas are new** |
| Other robot rules | E27 R42 no self-obstructed armor; R46 entanglement >10 s →Yellow; R47 no contact interrupting enemy healing; R38 stay in Starting Zone until Battle | Self-obstruction was E26 R41 |

## Sentry Tournament (new)

Sentry vs Sentry, following 1v1 rules (E27 §5, §4):

- **Battlefield:** 5×5 m with two Bunkers and corner Starting Zones
  (§4.2, Figs 4-1–4-4); same tolerances/environment caveats as 3v3.
- **Sentry changes** (Table 5-2): **120 W** chassis; **250** ammo, cannot
  increase; other performance unchanged (400 HP, 260 heat, 30/s).
- **2-minute Battle**, 2-minute Setup, 1 Team Timeout per event (Table 9-2).
- **No respawn, no Resupply healing:** dealing projectile damage heals 50%
  of the damage dealt (§4.3.2).
- **Winner** (§4.4): defeat the opponent; else more HP; else the side that
  did **not** take the first damage; if both at full HP, more shots fired,
  then first to fire, then the lighter robot (Inspection weight).

## Battlefield geometry and objectives (3v3)

| Rule / nav constraint | ARCC Season 2 basis | Change from ARCC 2026 |
| --- | --- | --- |
| Arena | E27 §3.2.1, Figs 3-1–3-3: 12×8 m, mirrored about the central line; ±10% (±5 mm under 100 mm), ±3° structure / ±1° components; magnetic fields, wind, lighting possible | Same size; **new layout**, do not reuse E26 geometry |
| Start / resupply | E27 §3.2.2, Fig 3-4: Starting Zone = Resupply Zone, **1500×2000 mm** in the team's corner, RFID cards; RFID dead zones possible | Same role |
| High Ground | E27 §3.2.3: Central 3000×2000 mm, 210 mm, 15° ramps 784 mm long, against the far wall; Side High Ground beside each Resupply Zone, tiers 210/410 mm | Changed layout |
| Limbo Bars | E27 §3.2.6, Table 3-5: Central **420 mm** clearance / 600 mm wide; Side **300 mm** / 1000 mm. Referee modules may be briefly blocked passing under (BS27 §3.1) | **New**; a taller Sentry must plan around them |
| Bumpy Road | E27 §3.2.5: 400×400 mm PVC tiles, 2.5 mm thick, four 1.2 mm bumps | Similar |
| Objectives | E27 §3.2.4: cube (Central High Ground), bucket of 10 pipes, 2 donuts; scored on a 300×300×50 mm Scoring Area or through a 52.5 mm Pipe Chute. **Only Engineers may Control Objectives** (§3.2.4.5, R51) | **New**; replaces the Capture Point |
| Score / victory | E27 §§3.3.4–3.3.5, Table 3-13: start at 0 VP; cube 1/s, pipe 30, donut 5/s each, **20 VP to the opponent per robot defeated**; first to **300** wins; else more VP, then Attack Damage, then remaining HP | Was 200 points counting down, −20 per own defeat, occupation drain |
| Comeback | E27 §3.3.3: first VP gaps of 100/200 give the trailing team 80 Gold each (Hero ammo only) | Was 70/140 gaps, 200 Gold each |

For the Sentry, the 3v3 job is defending/denying and killing (20 VP each)
while avoiding Penalty Zones; it cannot score Objectives. RFID activation is
a sensor condition, not an XY containment test; exact geometry comes from
the cited drawings.

## Match phases (Season 2)

E27 Table 9-2 and §§9.4–9.8 specify 3v3 Setup of 3 minutes and Battle of
5 minutes; Sentry Tournament Setup and Battle are 2 minutes each. At 30 seconds
remaining in Setup robots must be powered up or removed. After Setup, place the
Sentry remote in the designated area. A 15-second referee initialization
follows, then a 5-second countdown, then Battle; the game ends at timeout or
on a winning condition. Timeouts can pause Setup. These are **2027 event rules**;
they do not change the current simulator's 2026 field or behavior. Referee
message semantics are maintained in the [wire protocol](../ros2_dji_serial_bridge/UART_PROTOCOL.md).

The 1v1 field drawing (E27 Fig 4-3) gives 1000 × 1000 mm corner Starting
Zones within the 5000 × 5000 mm arena; Fig 4-4 supplies bunker dimensions. The 3v3 Scoring Areas include their
tape outlines as penalty zones (E27 §3.2.4.1). Exact component placements must
still be transcribed from the drawings before constructing an event map.

## Armor geometry and building limits

BS27 S-IDs are ARC's own and differ from both B26 and the RoboMaster 2027
building spec ([B27][build27]).

| Rule / CV prior | ARCC Season 2 basis (BS27) | Change from ARCC 2026 |
| --- | --- | --- |
| Armor face | §2.1.4: the Armor Module hit face is a **dot-matrix screen** showing the robot number or a pattern (style to be published); its displayed content is the visual feature. S28–S29: no imitating or changing visual features | **New hardware**: do not assume printed number stickers |
| Armor type / count | Table 3-3: four Armor Modules on the Sentry; BS27 does not name a small/large type | Was small armor (B26 S114). ARC's [preview][arc-preview] says small armor on all mobile ground robots; size unconfirmed in BS27 |
| Cant / yaw | S106: normal 75° from −Z (15° off vertical); direction vectors on ±X/±Y within 5°; unlit edges <5° from XY | Same (B26 S150) |
| Center offset | S107: perpendicular opposing-center lines; transverse offset ≤50 mm | Same (S151) |
| Mounting / rigidity | S103–S105: official support frame only, rear or bottom face, no modification; S108: 60 N at lower-edge midpoint changes angle ≤2.5° | Same rigidity (S152) |
| Panel motion | S109: no continuous/reciprocating panel motion >0.5 m/s relative to chassis | Same (S153) |
| Lower-edge stagger | S110: ≤100 mm between panels; brief exception while crossing terrain | **Terrain exception added** (S154) |
| Lower-edge height | S111: ≤400 mm, never touching ground, before/during/after deformation | Same (S155) |
| Bumpers / wall | S112–S114: bumpers required; armor must not touch a wall; only the support frame may touch the module | Same (S156–S158) |
| Exposure | S115: Sentry/Infantry/Hero clear within 105° lower / 120° upper / 145° left and right edges | Same (S159) |
| Light Indicator | S102: light bar long axis parallel to ground; main and auxiliary bars fully visible from at least one horizontal direction at up to 45° tilt; shows side, HP, buffs, offline state (Table 3-2) | Module named explicitly |
| Colours / finish | S35: shell may use own team colour; ≤4 opposing-colour areas, each ≤60×60 mm. S34: gloss ≤30 GU. S37–S38: logos >30 mm from armor light strips, non-luminous | Expect **red/blue shells**, not just lights |
| Envelope / energy | S68, Table 2-8: 600 mm cube powered-on storage, 800 mm expansion (software limits insufficient), 300 Wh, 30 V | Same |
| Weight | S68: **28 kg including battery and referee system** (3.25 kg) | Was 25 kg excluding referee |
| Required modules | Table 3-3: no Positioning Module; S135: Supercapacitor Management Module required | Same |
| Fluorescent charger | S48: every 17 mm robot must install one; custom allowed, power tested | Same as A26 A7 |
| Wireless / light emitters | S21: only remotes, referee system and robot-to-robot visible-light communication; nonremovable radios disabled. S22 bands. S24/S27: no obvious emitters, only Class I invisible lasers; LIDAR allowed | Same as A26 A1/A2, now in the body |
| Chassis power cutoff | S101: disabled Chassis port cuts all chassis motor controllers immediately; no supercap backfeed; software disable insufficient | Same as A26 A11 |
| Third-party parts | S58: no third-party subsystems; generic COTS (Jetson, STM32, LIDAR, 3D cameras) allowed | **New explicit COTS criteria** |

The build-spec body frame has **+Z down** (§3.6.1), with X the chassis's
maximum-efficiency motion direction, not its firing direction. This is a
rulebook construction convention; ROS frames still follow
[REP 103](https://www.ros.org/reps/rep-0103.html).

### Visual status and stickers

- **E27 R42** forbids an alive robot obscuring its own armor; Objectives it
  Controls (Engineers only) may block one panel. E27 has **no armor-sticker
  rule** like E26 R34; the dot-matrix face replaces that role.
- **E27 §11** continues matches despite armor or indicator-light anomalies.
  Dark LEDs alone do not establish defeat. Treat the armor side light
  strips, dot-matrix content and Light Indicator as cues; none guarantees
  visibility through another robot, a Bunker or terrain.
- BS27 §2.1.4 warns venue lighting and surroundings may interfere; vision
  must adapt.
- Team CV assumptions, **not rule limits**: near full-size opponents,
  translation up to 4 m/s, chassis spin roughly 1–2 Hz. Expect repeated
  panel occlusion and changing normal direction. The team's 135×125 mm
  small-panel CAD measurement predates the dot-matrix module; remeasure.

## Our Sentry's drivetrain (not from the rulebook, our hardware choice)

Holonomic translation and chassis spin require per-panel tracking and
world-frame aim. Firmware route rates and their provenance belong in
[sim firmware behaviour](../sim/README.md#firmware-behaviour-and-historical-results-then-stage-e2-now-mcb_parked);
ROS frame/odometry choices belong in
[pose_translator](../thornbots_pkg/README.md#pose_translator).

## RoboMaster 2027 RMUL base rules

RMUL 2027 Rules Manual V1.0.0 ([R27][rmul27]) and Building Specifications
V1.0.0 ([B27][build27]) are background only:
[translations](rules/rm2027/README.md) stay on `nightly` (PR [#54][rules-pr]),
but E27 §1.2 excludes RoboMaster Q&A. BS27 tracks much of B27
(dot-matrix armor, 28 kg with referee, stagger exception, visible-laser
ban), while ARC keeps Hero/Engineer/Sentry 3v3, an 80 W Sentry, its own
field and its own S-IDs. Cite BS27/E27, not B27/R27, for ARCC decisions.

## Not yet extracted / worth pulling in later

- **Site Manual:** match formats (BO2/BO3/BO5, group/elimination) and venue
  details are referred to but unpublished.
- **Dot-matrix armor:** the displayed style is “to be updated later”
  (BS27 §2.1.4), as are detailed mounting steps (§3.6.2); BS27 gives no
  panel dimensions or small/large type. CV training data and armor priors
  need them.
- **Zig-zag pole** for Objective C is still to be announced (E27 §3.2.4.4).
- Extract exact 3v3 and Sentry Tournament geometry from E27 Figs 3-3–3-13
  and 4-3–4-4 for event maps; sim and nav still use the ARCC 2026 field.
  The published dimensions and match timing are summarized above; placement
  coordinates still need careful transcription from the drawings.
- Check firmware/sim chassis power limits against 80 W (3v3) and 120 W
  (Sentry Tournament).

[arc-2027]: https://www.arc-robotics.org/participants/2027-manuals
[arc-preview]: https://www.arc-robotics.org/announcements/2027-season-preview
[e27]: https://www.arc-robotics.org/_files/ugd/6f41a3_caec30f4845b4904a45ddeb6338510ca.pdf
[bs27]: https://www.arc-robotics.org/_files/ugd/6f41a3_dbe73f66c9cf4630bad6046b379736e5.pdf
[p27]: https://www.arc-robotics.org/_files/ugd/6f41a3_9dca2943edd3426db65fcc34fe893dcb.pdf
[events]: https://www.arc-robotics.org/_files/ugd/df0c37_304dcbb3e08c422b987a1b627110d767.pdf
[arc-build]: https://www.arc-robotics.org/_files/ugd/df0c37_85f8332e4e464f12ad4f5f4cb74a758d.pdf
[rmul27]: rules/rm2027/rmul-rules-manual.md
[build27]: rules/rm2027/robot-building-specifications.md
[rules-pr]: https://github.com/Thornbots/thornbots_workspace/pull/54
[build26-zh]: https://hz-rm-bbs-web-prod.oss-cn-hangzhou.aliyuncs.com/0af874e7e10a4f9eb7c3c4872e47f03b1770636018010/RoboMaster%202026%20%E6%9C%BA%E7%94%B2%E5%A4%A7%E5%B8%88%E9%AB%98%E6%A0%A1%E7%B3%BB%E5%88%97%E8%B5%9B%E6%9C%BA%E5%99%A8%E4%BA%BA%E5%88%B6%E4%BD%9C%E8%A7%84%E8%8C%83%E6%89%8B%E5%86%8CV1.3.0%EF%BC%8820260209%EF%BC%89.pdf
