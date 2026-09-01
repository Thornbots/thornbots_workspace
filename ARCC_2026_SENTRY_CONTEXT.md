# ARCC 2026 rules: Sentry-relevant context

Distilled from the ARCC 2026 rulebook (76 pages, RoboMaster-style 3v3 combat
competition), fetched from:
https://e0398dbe-f5cb-43f1-8df9-3f2f243ba559.filesusr.com/ugd/df0c37_304dcbb3e08c422b987a1b627110d767.pdf

This is a starting-context doc for `sentry_pkg` / `sim` work. It pulls out only
what's relevant to building an autonomous Sentry, not the full rulebook (pit
crew procedures, other robot types, appeals process, etc. are omitted). Read
the source PDF directly if you need something not covered here.

Dev status, priorities, and open work are not tracked here: each package's
`AGENTS.md` has an `## Open` section with its live TODO list, and its
`README.md` has the detail. This doc holds only the rules and opponent facts.

## Sentry robot spec (§3.1.3)

- **Must operate fully autonomous during the match: no pilot, no teleop.**
  A debug remote controller is allowed only before the match; it must be
  physically removed from the Battlefield entrance once the match starts and
  cannot be used after the Five-Second Countdown (R23).
- **No inter-robot communication**: unlike Hero/Infantry, the Sentry cannot
  talk to teammates. All perception/decision-making must be self-contained.
- Launcher: 17mm only, muzzle speed capped at 25 m/s.
- Initial/Max HP: 400 (highest of the three robot types).
- Chassis power limit: 100W.
- Max barrel heat: 260, cooling rate: 30/s (best cooling of the three robot
  types).
- Projectile allowance: 750, preloaded during the 3-minute Setup Period,
  **fixed for the whole match**. Sentry cannot buy more via the Economy
  System mid-match the way Hero/Infantry can (that requires occupying the
  Resupply Zone with a live Pilot exchange, which a fully autonomous Sentry
  doesn't do here).
- Can occupy the Capture Point and the Resupply Zone (25% max-HP/sec
  recovery while inside).

## Our Sentry's drivetrain (not from the rulebook, our hardware choice)

- **Holonomic chassis** (e.g. mecanum/omni wheels): can translate in any
  direction without changing heading.
- **Does not turn/rotate its chassis heading during matches.** Heading stays
  fixed; all repositioning is pure translation. Deliberate design choice,
  likely so the gimbal/turret aims independently of chassis facing and
  armor-panel orientation stays predictable toward expected threat
  directions.
- **Implication for SLAM/nav**: no need to plan or reason about heading
  changes. The planner can treat orientation as constant and optimize
  purely over (x, y) translation. Costmaps/footprints should still account
  for the fixed heading's asymmetric footprint (if any) since it never
  rotates to present a different profile.
- **Implication for firing-timing (later)**: since chassis heading is fixed,
  gimbal/turret aim is fully decoupled from chassis motion. There's no need to
  coordinate "stop translating before firing" the way a differential-drive
  robot might need to stop turning to stabilize aim.

## Battlefield geometry (§3.2): relevant to SLAM/nav

- Battlefield: **12m × 8m**, mirrored layout about the centerline (Red/Blue
  symmetric).
- Each team has a **Starting Zone == Resupply Zone**, inlaid with RFID
  Interaction Module Cards (used for HP recovery and Capture Point
  detection: robots must physically sense the RFID card, not just be in
  the right XY region).
- One shared **Capture Point** at the center, also RFID-carded. **RFID
  dead zones exist**, and the rulebook explicitly says teams must handle this
  (don't assume 100% detection reliability inside the zone; a robot that
  loses RFID contact loses occupation after 2 seconds).
- **Bumpy Road**: PVC flooring with evenly spaced bumps around the Capture
  Point. Expect wheel odometry noise/slip here; may want extra localization
  weight from other sensors when crossing it.
- **High Ground** exists as a terrain feature (elevation change).
- Environment is explicitly **not fully symmetrical in practice**: non-uniform
  magnetic fields, wind, venue lighting are called out as real conditions
  (relevant if using a magnetometer or vision-based localization that assumes
  uniform lighting).
- An extra flooring layer sits over the RFID zones (minor height change to
  model if doing precise wheel/lidar odometry calibration).

## Combat mechanics: relevant to firing-timing phase (later)

- **Barrel heat**: each 17mm shot fired adds +10 heat; cools at rate/10 per
  100ms tick (30/s cooling rate → -3 per 100ms). Exceeding the limit (260)
  locks the launcher until heat drains to 0; exceeding limit+100 (360) locks
  the launcher for the rest of the round. **Firing-rate logic needs a heat
  budget model**, not just "fire when target acquired."
- **Projectile speed limit** (25 m/s): overspeed locks the launcher 15–20s
  depending on margin, or for the rest of the round if >10 m/s over. Muzzle
  velocity calibration/control matters as much as aim.
- **Damage**: 17mm hit = 20 HP to target's armor module (detection requires
  >12 m/s normal-component impact speed on the armor panel).
- **Projectile budget is fixed at 750 for the whole match** with no
  resupply path for a fully autonomous Sentry, so firing logic should treat
  ammo as a scarce resource to ration across the 5-minute Battle, not spend
  freely early.
- **Respawn**: on defeat, barrel heat resets to 0, robot respawns with 20%
  HP, 30s invincibility, and a "Weakened" state (launcher locked, can't
  capture points) until it reoccupies its Resupply Zone.
- **Referee System disconnection**: if the Sentry's main control module goes
  offline, launcher/gimbal/chassis power off and HP drains 5%/sec, so the
  autonomy stack's reliability directly costs HP, independent of combat.

## Opponent robot characteristics: relevant to CV

- **Most ARCC robots are near full-size** (RoboMaster Standard-class scale,
  not the smaller reference/toy-scale robots), so targets are large in frame
  at typical engagement ranges, not tiny/distant.
- **Chassis can translate up to 4 m/s**. With the spin below, CV must track
  targets that rotate in place while translating quickly across the frame;
  tracking/prediction can't assume a roughly stationary opponent.
- **Chassis spin at roughly 1–2 Hz** (this is the common "wiggle"/spinning
  defense tactic to make armor panels harder to hit, since panel
  facing keeps rotating rather than staying fixed toward the shooter). CV
  target detection/tracking needs to handle a **continuously rotating
  target**, not a mostly-static one:
  - Panel orientation relative to the camera changes every ~0.5–1s
    (360°/1-2Hz), so a tracker can't assume "last known facing" stays valid.
  - At 1-2 Hz, panel-to-panel occlusion/foreshortening cycles fast, so the
    detection pipeline should expect a given armor panel to swing in/out of
    a good detection angle repeatedly within a second, not just once.
  - This also interacts with the >12 m/s normal-impact-speed detection
    requirement above (Combat mechanics): firing-timing logic (later) will
    need to predict *when* a spinning target's panel will next present
    near-normal to the shot, not just track current position.

### What an armor panel actually looks like (target signature for CV)

From DJI's Referee System install spec (2018 baseline dimensions/behavior;
general form has stayed consistent across RoboMaster years):

- **Shape**: flat rectangular plastic module, screwed onto a bracket bolted
  to a flat chassis face, always **side-mounted** (front/back/left/right),
  never top-mounted. Two sizes: **Large Armor Module** (Hero, Sentry) and
  **Small Armor Module** (Standard, Engineer). Most ARCC opponents will be
  Standard-class, so expect mostly Small Armor Modules.
- **Visual signature**: each panel has **two separate indicator lights**,
  one on each side of the panel body (not a single glowing panel):
  **steady red or blue** = team color / alive, **steady yellow** = that
  module offline/critical. This two-light-segment pattern per rectangular
  panel is the practical thing to detect.
- **Exposure cone**: the front **145° of the panel's exposure surface must
  stay unblocked**, so the two-light pattern is visible/detectable across
  most viewing angles within that cone, not just head-on.
- **Mounting height clusters by robot class**: Standard-class panels'
  lower edge sits ~60–150mm above the ground, Hero-class ~400mm+. Expected
  panel height in frame isn't arbitrary, it's a signal tied to robot type.
- With the spin and translation above, that two-light signature rotates past
  the camera at 1–2Hz while the robot translates up to 4 m/s, so CV needs
  per-panel tracking that tolerates frequent brief occlusion, not a single
  fixed-facing detection.

### Mounting angle (S122, from the 2024 RoboMaster University Series Robot
Building Specifications V2.0; structure unchanged from 2018 baseline.
Confirmed no separate elevated-rail Sentry mount exists in the 2024 spec,
so this general ground-robot rule is what applies, matching our Sentry
being ground/mecanum-based like the others, not the legacy 2018 rail-Sentry
design that used a different, floor-facing angle)

- Robot body coordinate system: **Z-axis points straight down** (toward
  the center of the earth), X-axis is the robot's highest-efficiency
  firing direction, Y-axis completes the right-handed frame at the
  center of mass.
- **Panel tilt**: the armor panel's Armor Support Frame bottom surface is
  parallel to the ground (XY plane), and the panel is mounted so the
  **acute angle between the panel's outward-facing normal vector and
  straight-up (negative Z-axis) is 75°**. Since 90° would mean a perfectly
  vertical panel facing purely horizontally, 75° means each panel is
  **canted about 15° off vertical**, angled slightly upward/outward
  rather than dead flat. Panels are deliberately not flush-vertical.
- **Yaw alignment**: projecting each panel's normal onto the ground plane
  gives its "direction vector". The four panels' direction vectors must
  each align with +X, −X, +Y, −Y respectively, within **±5° angular
  error**. So the four panels are roughly a symmetric cross around the
  robot, not just "somewhere on each side."
- **Placement tolerance**: the geometric center of an X-mounted panel and
  a Y-mounted panel form perpendicular lines through the robot's center of
  mass; each panel may be offset up to **50 mm** from center along its axis.
- **Vertical stagger (S126)**: the difference in height between the lower
  edges of any two Armor Modules on the same Ground Robot must not exceed
  **100 mm**. Panels can sit at somewhat different heights (e.g. front/back
  vs. side panels) but not wildly so, a useful prior for where to expect
  a robot's other panels vertically once one is located in-frame. (S127:
  lower-edge height itself must be 60mm–400mm off the ground, except while
  climbing/overcoming obstacles.)
- **Rigidity requirement (S124)**: a 60 N upward force at the midpoint of
  a panel's lower edge must not change its mounting angle by more than
  **2.5°**, i.e. panels must be rigidly fixed, not spring-mounted or
  loose. That reinforces why the 4×N-per-500ms disconnection HP drain (below)
  is a real design risk, not just a wiring edge case.
- **Practical CV takeaway**: opponent armor panels present at a
  consistent, predictable ~15°-off-vertical cant on all 4 sides, useful
  as a geometric prior (e.g. for pose/orientation estimation from a single
  panel's apparent aspect ratio) rather than assuming panels are flush
  vertical rectangles.

### Armor Module rules (from the 2026 RoboMaster University Championship
Rule Manual V1.2.0, which governs ARCC via the Building Specifications diff
above; fetched from
`bbs-web-static.robomaster.com/.../RoboMaster 2026 University Championship
Rule Manual V1.2.0 (20260107).pdf`)

- **Detection speed thresholds confirmed**: Large/Small Armor Module needs
  >12 m/s normal-component impact speed for a 17mm projectile to register
  (matches the Combat mechanics section above); minimum detection interval
  is 50ms for 17mm projectiles (so back-to-back hits within 50ms may not
  both register).
- **Damage values (Table 5-2, no buffs)**: 17mm hit on a Ground Robot's
  Armor Module = 20 HP (confirmed); collision-detected-as-damage = 2 HP
  (collisions/ramming aren't allowed as a deliberate damage method, but the
  Referee System can still register accidental collisions as small damage,
  relevant if our Sentry's own motion planning brushes an obstacle/robot).
- **Physical armor stickers required (R37)**: every robot must have a
  Referee-provided **Armor Sticker** physically affixed per the Building
  Specifications Manual before the match's 15-Second Referee System
  Initialization Period. This is separate from and in addition to the
  LED indicator lights. A CV pipeline could in principle use sticker
  graphics as an additional visual cue, not just the LEDs.
  Continuation rule: **damage to an Armor Module Sticker, or any anomaly in
  a robot's armor light effects/light indicator effects, does not stop the
  match**, meaning a dead/broken LED or damaged sticker is not reliable
  evidence a robot is disconnected/eliminated. Don't gate "is this robot
  alive" purely on LED state being lit.
- **Self-obstruction is against the rules (R45)**: no alive robot may block
  any of its own Armor Modules with its own body, and can't block more than
  one Armor Module on another allied robot. **Sentry specifically is never
  allowed to obstruct its own Armor Modules** (unlike Engineer, which gets
  a narrow exception while carrying a Mobile Component). Practical
  implication: on a rules-compliant opponent, all 4 side panels should
  stay geometrically unobstructed by the robot's own structure. Any panel
  that looks occluded in-frame is more likely a viewing-angle/lighting
  effect than actual physical blocking, *unless* that panel has disconnected
  (see below), which is itself a valid non-violation reason for it to read
  as blocked/dark.
- **Disconnection penalty is quantified and continuous, not one-shot**:
  every 500ms, the Referee System counts N = number of currently
  disconnected Armor Modules + Supercapacitor Management Modules on a
  robot, and applies **HP loss = 4 × N** for that tick. This runs
  continuously while any module stays disconnected, which reinforces why our
  own armor/panel mounting reliability (screws not just friction-fit, wiring
  strain relief) matters as much as the A11 chassis-power-cutoff exception
  already noted below: a loose panel bleeds HP passively for as long as it
  stays loose, independent of getting shot.

## ARCC 2026 Robot Building Specifications (V1.3.1, 05/04/2026)

Fetched from: https://www.arc-robotics.org/_files/ugd/df0c37_85f8332e4e464f12ad4f5f4cb74a758d.pdf

This is a short (5-page) diff on top of the base
**"2026 RoboMaster University Series Robot Building Specifications V1.3.0"**
(hosted behind RoboMaster's JS-rendered community hub at
`bbs.robomaster.com/wiki/20204847`; no static PDF link found, so open in a
real browser and follow Rulebooks if the base spec's actual construction
limits (size/weight/materials) are needed). ARCC applies all RMUS rules
except where noted here, and interprets RMUC-only rules (e.g. Custom
Clients, Dart/Aerial-specific rules) as not applicable since ARCC is
treated like an RMUL event.

**Sentry-relevant:**
- **A7**: RMUL normally exempts robots from installing the fluorescent
  energy charging device, but ARCC overrides this: **any 17mm-launcher
  robot (including Sentry) must install one**. The installed device doesn't
  need to match the reference part; custom/alternate parts are allowed.
- **A11**: elaborating on S145, when the Power Management Module's chassis
  port is disabled, all chassis motor controllers must **immediately lose
  power**; stored energy in the supercapacitor bank may not backfeed the
  chassis. Software-only motor disable is explicitly not sufficient; this
  needs a hardware cutoff.
- **A2**: no visible lasers allowed on any robot type at ARCC (RMUS allows
  some non-scanning laser types).
- **A1**: any wireless comms hardware that can't be physically removed
  (e.g. an SoC's built-in WiFi antenna) must be disabled so it does not
  transmit. Max penalty for illegal wireless comms during competition is
  disqualification. Relevant since Sentry already can't use inter-robot
  comms per the base rules (§3.1.3 above); this closes the "can't remove
  the antenna" loophole.
- **A12**: COTS devices (e.g. action cameras) fully disconnected from
  chassis/ammo-booster/mini-PC/gimbal may use their own internal battery,
  but must still comply with size, light-emission, and wireless-comms
  rules.

**Other exceptions (not Sentry-specific, kept for completeness):**
- **A3–A6**: advertising-space placement/sizing rules relaxed vs. stock
  RoboMaster (don't need both sides of the robot; no size/count
  restriction, though the Head Inspector can reject designs that obscure
  armor-module visual indicators or are inappropriate).
- **A8**: computational platforms don't need to run open-source OSes
  (RMUS requires this).
- **A9**: robot photographs must be included in the Final Assessment.
- **A10**: "Maximum Storage Size" (§2.4 of the base spec) must be measured
  powered-on; also called "Maximum Initial Size"/"Initial Size."
- The ARC Organizing Group is the ARCC equivalent of RMOC (RoboMaster's
  organizing committee) for rule-interpretation purposes.

## Not yet extracted / worth pulling in later

- Exact Battlefield zone coordinates/drawings (Figures 3-1–3-9 are diagrams,
  not extracted as text, so you need the actual PDF pages if building a precise
  arena map for `sim`).
- Base RMUS "Robot Building Specifications V1.3.0" itself (size/weight
  limits, materials, chassis/armor construction, manufacturing process
  rules). ARCC's building-spec doc above is only a diff against it, and the
  base doc's actual numeric limits aren't extracted yet since it isn't
  reachable as a static PDF (see note above).
- Full Referee System data interface / UART protocol spec.
- **Armor panel face dimensions.** `sim/sim/cv_target_emulator.py`'s
  `PANEL_SIZE = 0.1` (a 0.1m x 0.1m face) is an assumption, explicitly not
  sourced from this document. `sim/test/cv/run_shot_hit_tests.py` derives
  `DEFAULT_HIT_RADIUS` from it, so the shot-hit suite's entire pass/fail line
  rests on that number — treat any hit-rate figure as calibrated on an
  approximation until the real dimension is pulled from the rulebook. The
  145-degree front exposure cone used alongside it *is* sourced from here.
- Round timing/countdown details (§7.5–7.9) if precise match-phase state
  machine timing is needed later.

Re-fetch the PDF and run `pdftotext -layout` on it if deeper detail is needed
later; no extracted plaintext is kept in the repo.
