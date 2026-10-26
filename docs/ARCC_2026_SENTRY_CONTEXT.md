# ARCC 2026 rules: Sentry-relevant context

CV detection/tracking comes first. This is the workspace's rules context;
[ROADMAP](ROADMAP.md) owns priorities and package READMEs own implementation.
Values below are rules, except the explicitly labelled team assumptions.

## Which rules govern?

Checked **2026-10-26** against ARC's [2026 manuals index][arc-index],
[2027 manuals page][arc-2027] and [announcements][arc-news]:

- **ARCC 2026:** Events Manual **V1.6, 2026-06-08** ([E26][events]);
  Building Specifications **V1.3.1, 2026-05-04** ([A26][arc-build]).
  A26's introduction adopts the **English RMUS 2026 Building Specifications
  V1.3.0**, interpreted as RMUL, with A1–A12 overrides.
- **Base-spec gap:** the [RoboMaster index linked by ARC][rm26-index] offers
  **Chinese V1.3.0, 2026-02-09** ([B26][build26-zh]), but only
  **English V1.2.0, 2026-01-07** ([B26-en][build26-en]). B26 citations below
  are to the Chinese V1.3.0; they verify its values, but do not establish
  that an unavailable English V1.3.0 has identical wording/numbering.
  Do not substitute the 2024 V2.0 numbering or RMUC match rules.
- **October 31 mini competition:** no ruleset adoption or local exceptions
  were found in repository docs or the ARC pages checked. Its governing
  rules remain **unconfirmed**; neither the date nor this document adopts
  RMUL 2027 for that event.
- **ARCC 2027 is not RMUL 2027 by default.** ARC's
  [Season 2 preview, 2026-09-24][arc-preview] announces Hero/Sentry/Engineer
  for 3v3, Infantry for 1v1, small armor on all mobile ground robots, and
  Aerial/Dart side events. It promises manuals by **2026-11-01**. The 2027
  manuals page still serves the 2026 files and says “TODO: FIX ALL LINKS”.
- **RMUL 2027 comparison only:** Rules Manual **V1.0.0** ([R27][rmul27]) and
  shared Building Specifications **V1.0.0** ([B27][build27]), both
  **2026-10-15**. [Translations and Chinese originals](rules/rm2027/README.md)
  are already on `nightly` via [merged PR #54][rules-pr]; no dependency on an
  unmerged branch and no duplicate rule files. Chinese originals govern
  those translations; they do not override ARC event rules.

## Sentry limits, autonomy and combat

Each source label resolves to the version/date above. **Same** means the
listed Sentry value matches E26/B26, not that the entire manuals match.

| Rule / code constraint | ARCC 2026 basis | RMUL / RMUS 2027 comparison |
| --- | --- | --- |
| Autonomy / communication | E26 §3.1.3, Table 3-4: fully autonomous, no pilot, no inter-robot communication; at most one debug remote | **Same**, R27 §3.1.3, Table 3-5 |
| Debug remote removal | E26 §8.2.1.2 R23: leave at Battlefield entrance after Setup; no commissioning from start of five-second countdown | **Same**, R27 §6.2.1.2 R22 |
| Launcher / speed | E26 §3.1.3: one 17 mm launcher, ≤25 m/s | **Same**, R27 §3.1.3 |
| HP / chassis / heat | E26 §3.1.3: 400 HP, 100 W, heat limit 260, cooling 30/s | **Same**, R27 §3.1.3 |
| Ammo / duration | E26 §3.1.3, §3 and §7.4: 750 initial allowance, cannot increase; three-minute Setup, five-minute Battle | **Same**, R27 §3.1.3, §5.3, §5.6. This is an explicit allowance restriction, not an inference about pilot purchases. |
| Heat accounting | E26 §3.3.1.3, Figs 3-11–3-12: +10 per 17 mm shot, cooling at 10 Hz (−3/tick at nominal rate); above 260 locks until heat reaches 0; Q2=360 is round-lock threshold | R27 §3.3.1.3, Fig 3-12: **same values**. Both prose descriptions use `>Q2`; both flowcharts use `≥Q2`. Exact equality needs referee clarification; budget below the limit. |
| Overspeed locks | E26 §3.3.1.2, Table 3-8: excess speed (0,5) m/s →15 s; [5,10) →20 s; **≥10** →rest of round | **Same**, R27 §3.3.1.2, Table 3-9; old “>10” summary was wrong at equality |
| Armor hit registration | E26 §3.3.1.1, Table 3-6: 17 mm normal impact component **>12 m/s**, minimum detection interval 50 ms | **Same**, R27 §3.3.1.1, Table 3-7. Spinning-panel facing affects registration. |
| Unbuffed damage | E26 §3.3.1.1, Table 3-7: 17 mm hit 20 HP, collision 2 HP | **Same**, R27 §3.3.1.1, Table 3-8; deliberate collision damage is forbidden in both |
| Chassis overlimit | E26 §3.3.1.4: 60 J buffer, 10 Hz accounting; exhausted buffer while over limit →5 s chassis power cut | **Same**, R27 §3.3.1.4, Fig 3-13 |
| Referee main controller offline | E26 §3.3.1.5.1, Table 3-9: launcher/gimbal/chassis off; −5% max HP/s; RFID invalid and respawn stops | **Same**, R27 §3.3.1.5.1, Table 3-10; Mini PC is exempt from defeated-state power cut (both §2) |
| Armor / supercapacitor module offline | E26 §3.3.1.5.2, Fig 3-14: −4×N HP each 500 ms for N disconnected modules | **Same**, R27 §3.3.1.5.2, Fig 3-14 |
| Speed monitor offline | E26 §3.3.1.5.3: corresponding launcher immediately loses power | **Same**, R27 §3.3.1.5.3 |
| Healing / revival | E26 §3.3.2: own Resupply Zone heals 25% max HP/s; first revival 5 s, +5 s each later defeat; heat resets; revive at 20% HP, 30 s invincibility, Weakened (no firing/capture) until own Resupply RFID; that also removes invincibility | **Same baseline**, R27 §3.3.2; new point-gap bonuses below can change revival/healing |
| Yellow Card on Sentry | E26 §8.1.2, Table 8-2: chassis off 2 s, −15% max HP on first one-side Yellow Card | **Same baseline**, R27 §6.1.2, Table 6-2; consult full tables for repeat/team penalties |

## Battlefield geometry and objectives

| Rule / nav constraint | ARCC 2026 basis | RMUL 2027 comparison |
| --- | --- | --- |
| Arena | E26 §3.2.1, Figs 3-1–3-3: 12×8 m, mirrored layout; drawings in mm, dimensions ±10%; nonuniform magnetic fields, wind and lighting explicitly possible | **Same size/environment caveats**, R27 §3.2.1; changed layout, use its Figs 3-1–3-3 |
| Start / supply | E26 §3.2.2: Starting Zone = Resupply Zone, RFID cards; opponent's resupply is a penalty zone | R27 §3.2.2: Starting Zone = Supply Zone, 2500×2000 mm; **Workbench added** |
| Terrain / interaction | E26 §§3.2.3–3.2.5: High Ground, PVC Bumpy Road around central Capture Point; RFID dead zones and extra flooring over RFID zones | R27 §§3.2.3–3.2.4: **Highland/Tunnel layout**; dead zones and extra flooring retained. Do not reuse E26 terrain geometry. |
| Occupation | E26 §3.3.4: **one** shared Capture Point, first arrival wins a contest; occupation expires 2 s after lost RFID | R27 §§3.3.4.1, 3.3.5.3: **three** Control Zones; 0–5 progress counters at 1/s, contest pauses, unattended control decays; activation expires after 2 s without RFID |
| Score / victory | E26 §§3.3.4–3.3.5: **200 Victory Points**, −1/s while opponent holds point, **−20 per own defeat**; zero ends round, otherwise higher points wins | R27 §§3.3.4.2, 3.3.7: **600 Control Points**, −1/s **per enemy-held zone**, **−10 per own defeat**; same zero/higher-points principle. E26 already uses points, not base HP. |
| Comeback / buffs | E26 §3.3.3: first point gaps of 70 and 140 award 200 Gold Coins each (max 400) | R27 §§3.3.4.2–3.3.5: **gaps ≥200/400 reduce revival bar by 33%/50%, raise healing to 33%/50% per second**; Highland gives 25% defense; both own Tunnel cards within 3 s with no intervening card give 1.5× cooling for 60 s |

RFID activation is a sensor condition, not an XY containment test. Exact
zone geometry comes from the cited drawings, not this summary.

## Armor geometry and building limits

**B26 rule IDs below are Chinese V1.3.0 IDs**, subject to the English-basis
gap above. The old 2024 V2.0 IDs (cant S122, stagger S126, height S127)
are not current citations. B26-en V1.2.0 already says ≤400 mm / no ground
contact (§3.6.1.3 S153), so removing “60–400 mm” corrects stale context;
it is **not a newly introduced 2027 relaxation**.

| Rule / CV prior | 2026 basis (B26 unless A26 noted) | 2027 comparison (B27) |
| --- | --- | --- |
| Armor type | §2.4.5 S114, Table 2-10: Sentry uses Small Armor Modules; Infantry §2.4.3 likewise. All-ARCC small armor was also a team report (2026-09-27), not established for every class here. | §2.4.3 S74, Table 2-8: Small Armor Module; ARC's separate 2027 preview explicitly says all mobile ground robots use small armor |
| Cant / yaw | §3.6.1.1 **S150**: normal 75° from −Z (15° off vertical); four direction vectors align ±X/±Y within 5°; non-light-bearing edges <5° from XY | **Same**, §3.6.1.1 **S120** |
| Center offset | §3.6.1.1 **S151**: perpendicular opposing-center lines; transverse offset ≤50 mm (Y panel's X offset, and conversely) | **Same**, §3.6.1.1 **S121**; not a 50 mm radial-distance limit |
| Rigidity | §3.6.1.2 **S152**: 60 N upward at lower-edge midpoint changes angle ≤2.5° | **Same**, §3.6.1.2 **S122** |
| Panel motion | §3.6.1.3 **S153**: no active motion relative to overall center of mass in principle; deformable designs must not move panels continuously/reciprocally at >0.5 m/s relative to chassis | **Same**, §3.6.1.3 **S123** |
| Lower-edge stagger | §3.6.1.3 **S154**: ≤100 mm between any two panels | §3.6.1.3 **S124**: **same 100 mm, explicit brief terrain-crossing exception added** |
| Lower-edge height | §3.6.1.3 **S155**: **≤400 mm, never directly touching ground**, before/during/after transformation; measure from highest support surface, exempt if unsupported | **Same**, §3.6.1.3 **S125**; no 60 mm minimum in either verified version |
| Bumpers / wall clearance | §3.6.1.4 **S156–S158**: bumpers required, armor must not touch a vertical wall when robot side is against it; only support bracket may contact module | **Same**, §3.6.1.4 **S126–S128**. **S126 is the bumper rule, not stagger.** |
| Exposure | §3.6.3 **S159**: Sentry/Infantry/Hero clear within **105° lower / 120° upper / 145° left and right** edges | **Same Sentry/Infantry**, §3.6.3 **S129**; Heavy exceptions are separate S130. This is not a single 145° cone. |
| Envelope / energy | §2.4.5 **S114**, Table 2-10: 600 mm cube stowed, 800 mm cube extended, 300 Wh, 30 V | **Same**, §2.4.3 **S74**, Table 2-8; A26 A10 requires initial-size measurement powered on |
| Weight accounting | §2.4.5 **S114**: **25 kg including battery, excluding referee system** (listed referee mass 3.25 kg) | §2.4.3 **S74**: **28 kg including battery and referee system**; compare accounting, not just 25→28 |
| Required modules | §3.2: RMUL exempts Positioning Module; §3.12 **S187** requires Supercapacitor Management Module even without capacitor bank | **Same**, §3.2 and §3.12 **S158** |
| Fluorescent charger | **A26 A7**, overriding B26 §2.1.11: every 17 mm robot **must install**, custom/alternate part allowed | B27 §2.1.8: **RMUL exempt**; future ARC override unconfirmed |
| Wireless / lasers | **A26 A1/A2**: nonremovable wireless hardware must not transmit; **no visible lasers** | B27 §2.1.2 **S22** still restricts wireless equipment; §2.1.3 **S28** now explicitly bans visible lasers and permits only Class I invisible lasers. **Same visible-laser ban** as A26 A2; A26 A1's nonremovable-hardware exception is not established for 2027. |
| Chassis power cutoff | **A26 A11**, elaborating B26 §3.4.2 **S145**: all chassis motor controllers immediately lose power; no supercapacitor backfeed; software disable insufficient | B27 §3.4.2 **S113–S115**: immediate interface power-off and separate chassis supply; retain A26 hardware requirement for ARCC 2026 |

The build-spec body frame has **+Z down** (§3.6.1), with X the chassis's
maximum-efficiency motion direction, not its firing direction. This is a
rulebook construction convention; ROS frames still follow
[REP 103](https://www.ros.org/reps/rep-0103.html).

### Visual status and stickers

- **E26 §8.2.2 R34** requires armor stickers before the 15-second referee
  initialization; **R41** forbids an alive robot obscuring its own armor.
  The old R37/R45 citations came from RMUC and were wrong for ARCC.
  R27 §6.2.1.4 **R40** retains self-obstruction prohibition; do not carry
  E26 R34's number into R27 (its R34 is safety hazards).
- **E26 §9** explicitly continues matches despite armor/indicator-light
  anomalies or damaged stickers. Dark LEDs alone do not establish defeat.
  Treat the two side light strips (B26 S150 / B27 S120) and sticker as cues;
  neither guarantees visibility through another robot or terrain.
- Team CV assumptions, **not rule limits**: near full-size opponents,
  translation up to 4 m/s, chassis spin roughly 1–2 Hz. Expect repeated
  panel occlusion and changing normal direction. The team's 135×125 mm
  small-panel CAD measurement is an asset assumption, not a rule-specified
  universal face size. The old class-height clusters and 2018 LED-color
  claims are not verified current rules and must not constrain detection.

## Our Sentry's drivetrain (not from the rulebook, our hardware choice)

Holonomic translation and chassis spin require per-panel tracking and
world-frame aim. Firmware route rates and their provenance belong in
[sim firmware behaviour](../sim/README.md#firmware-behaviour-and-historical-results-then-stage-e2-now-mcb_parked);
ROS frame/odometry choices belong in
[pose_translator](../thornbots_pkg/README.md#pose_translator).

## RoboMaster 2027 RMUL base rules

The comparison tables above describe **RMUL**, not adopted ARCC 2027 rules.
R27 §3.1 replaces Hero with Heavy, uses Infantry/Sentry, and adds a modular
42 mm launcher/Workbench mechanism (§3.3.6); Custom Terminal replaces the
Custom Controller/Client split (§3.1.4). **ARC's September preview instead
keeps Hero and adds Engineer to 3v3.** Do not port the RMUL lineup or field
into ARCC defaults without the final ARC manuals.

## Not yet extracted / worth pulling in later

- Confirm the **October 31 mini competition's** event manual, version and
  local exceptions; no adoption notice was found in the sources checked.
- Obtain ARC's named **English 2026 V1.3.0** building spec or an organizer
  clarification reconciling it with Chinese V1.3.0 / English V1.2.0.
- Recheck ARC's promised **November 1** manuals before adopting 2027 rules;
  the preview does not specify Sentry limits, field geometry or armor IDs.
- Confirm the **heat equality boundary Q1=360** against referee behavior.
- Extract exact field geometry from E26 Figs 3-1–3-9 for event-specific maps.
  UART/message semantics have their maintained home in the
  [wire protocol](../ros2_dji_serial_bridge/UART_PROTOCOL.md); match-phase
  timing comes from E26 §§7.4–7.8, or R27 §§5.3–5.7 for RMUL only.

[arc-index]: https://www.arc-robotics.org/participants/2026-manuals
[arc-2027]: https://www.arc-robotics.org/participants/2027-manuals
[arc-news]: https://www.arc-robotics.org/announcements
[arc-preview]: https://www.arc-robotics.org/announcements/2027-season-preview
[events]: https://www.arc-robotics.org/_files/ugd/df0c37_304dcbb3e08c422b987a1b627110d767.pdf
[arc-build]: https://www.arc-robotics.org/_files/ugd/df0c37_85f8332e4e464f12ad4f5f4cb74a758d.pdf
[rm26-index]: https://bbs.robomaster.com/wiki/20204847/809872
[rmul27]: rules/rm2027/rmul-rules-manual.md
[build27]: rules/rm2027/robot-building-specifications.md
[rules-pr]: https://github.com/Thornbots/thornbots_workspace/pull/54
[build26-zh]: https://hz-rm-bbs-web-prod.oss-cn-hangzhou.aliyuncs.com/0af874e7e10a4f9eb7c3c4872e47f03b1770636018010/RoboMaster%202026%20%E6%9C%BA%E7%94%B2%E5%A4%A7%E5%B8%88%E9%AB%98%E6%A0%A1%E7%B3%BB%E5%88%97%E8%B5%9B%E6%9C%BA%E5%99%A8%E4%BA%BA%E5%88%B6%E4%BD%9C%E8%A7%84%E8%8C%83%E6%89%8B%E5%86%8CV1.3.0%EF%BC%8820260209%EF%BC%89.pdf
[build26-en]: https://hz-rm-bbs-web-prod.oss-cn-hangzhou.aliyuncs.com/270e4d3f297a414ba809f701dda8a28f1767780578641/RoboMaster%202026%20University%20Series%20Robot%20Specification%20Manual%20V1.2.0%EF%BC%8820260107%EF%BC%89.pdf
