# RoboMaster 2027 RMUC Rules Manual V1.0.0 (2026-10-15)

Unofficial English translation of the Chinese original. The Chinese PDF governs;
see the [translation index](README.md) for source, checksums and conventions.
`<!-- p.N -->` markers give the physical PDF page.

<!-- p.1 -->
V1.0.0

The 26th National University Student Robot Competition

RoboMaster 2027

RoboMaster University Championship

**Rules Manual**

Compiled by the RoboMaster RMOC

Released October 2026

<!-- p.2 -->
### Intellectual Property Statement

The RoboMaster Organizing Committee (RMOC, RoboMaster Organizing Committee) encourages and advocates technical innovation and open-source technology, and respects the intellectual property of participating teams. All intellectual property developed by a team during the competition belongs to that team. The RMOC does not handle intellectual property disputes between members within a team. Teams must properly handle the ownership of intellectual property among their internal school members, corporate members and members of other affiliations.

When using the Referee System and competition support materials provided by the RMOC, teams must respect the intellectual property ownership of the original products. Teams must not reverse engineer, copy, translate, or otherwise take any action that harms the intellectual property of the rights holder.

Any act that infringes the intellectual property of the competition education products provided by the RMOC and host organizations will be pursued legally by the rights holder.

For recommendations on open-source materials, see: https://bbs.robomaster.com/article/4820

### Reading Notice

The RoboMaster competition is a robot competition whose aim is to cultivate young engineering talent. The related documents may contain sensitive wording, names, operations, technologies and other content. Such content does not reflect any technology or action that exists in reality, and is not intended to refer to any specific country, organization or individual. This manual is intended to explain the robot competition rules. It must not be used for any purpose other than the RoboMaster competition, and should not be considered to be associated with any real events or entities.

### Version Number Description

The version numbers of competition rules documents use the semantic versioning format X.Y.Z, with the following meanings:

- X: Update for a different competition stage (fixed at 1 for Regional Competitions and fixed at 2 for the Final Tournament; the specific year is reflected in the file name and cover).
- Y: Update of important content such as mechanisms and the field, for example: a change of competition mechanisms or a change of robot attributes.
- Z: Correction of errors without changing the original mechanisms or field, for example: correcting a typo, adjusting an ambiguous sentence, or replacing an incorrect drawing.

> Examples:
>
> - The first version of the manual for a season (for Regional Competitions) has the version number V1.0.0.
> - On the basis of the first version (for Regional Competitions), some competition mechanisms were adjusted; the version number is V1.1.0.
> - On the basis of the second version (for Regional Competitions), 3 typos were corrected; the version number is V1.1.1.
> - On the basis of the third version (for the Final Tournament), some competition mechanisms were adjusted; the version number is V2.0.0.

<!-- p.3 -->
### Field Drawing Legend

| Symbol | Meaning |
| --- | --- |
| Green grid pattern | shared Buff Point |
| Green horizontal-line pattern | one-side Buff Point |
| Yellow crosshatch pattern | shared Restricted Zone |
| Yellow diagonal-line pattern | one-side Restricted Zone |
| Triangle marker above a box labelled "G" | The horizontal plane on which the battlefield ground lies is the lowest plane of the battlefield |
| Dimension arrow labelled "(100)" | Dimensions are for reference only |

### Revision Log

| Date | Version | Revision record |
| --- | --- | --- |
| 2026.10.15 | V1.0.0 | First release |

<!-- p.4: contents list omitted -->

<!-- p.5: contents list omitted -->

<!-- p.6: contents list omitted -->

<!-- p.7: contents list omitted -->

<!-- p.8: contents list omitted -->

<!-- p.9: contents list omitted -->

<!-- p.10: contents list omitted -->

<!-- p.11: contents list omitted -->

<!-- p.12: contents list omitted -->

<!-- p.13 -->
## 1 Preface

### 1.1 About the Competition

The National University Robot Competition RoboMaster University Championship (RMUC, RoboMaster University Championship) was initiated by DJI. Its core format is tactical confrontation between robots. Participating teams must design, develop and build multiple robots that comply with the specifications, and form a robot team to compete. In a seven-minute timed match, the two sides engage in tactical confrontation by operating their robots, and the side that destroys the opponent's Base wins the match.

RMUC is committed to cultivating outstanding young engineers and encourages team members to combine what they have learned with practical application, so that they continue to grow through participation.

*Figure 1-1 Talent Cultivation Philosophy*

- Pyramid, top to bottom: Core Values; (Sublimation); Essential Character; (Shaping); Key Abilities; (Cultivated in real-world scenarios); Scientific Knowledge | Engineering Experience
- Core Values: Investigating things to extend knowledge, striving for excellence, reflecting on oneself
  - Develop the habit of deep thinking and the ability to locate the root causes of problems
  - Pursue excellence driven by high goals and maintain a positive mindset
  - Face oneself honestly and be aware of one's own limits
- Essential Character: Proactive, positive, seeking truth from facts, upholding fairness
- Key Abilities: Thinking, communication and expression, problem solving, self-directed learning, forward design

<!-- p.14 -->
### 1.2 Major Changes in the New Season

Compared with RMUC 2026, RMUC 2027 mainly makes the following adjustments:

**Robots and Operators**

- The former Hero Robot and Engineer Robot are merged into the Heavy Robot.
- The former Aerial Robot is adjusted into the Aerial System (including the Aerial Robot and the Hangar).
- The former Custom Controller and Custom Client are merged into the Custom Terminal.
- Commander and Safety Officer are added.
- Gimbal Operator and Drone Pilot are removed.

**Battlefield**

- The former Launch Ramp is changed to the Tunnel.
- The overall layout of the Operator Room is adjusted.
- High Point, Hangar platform and Workbench are added.
- The flight zone, wireless charging device placement zone and landing pad are removed.

**Competition Mechanisms**

- The HP deduction and exceeding-the-limit penalty mechanisms are adjusted.
- The Economy System is adjusted.
- The Dart System special mechanisms are adjusted.
- The Radar System special mechanisms are adjusted.
- The Adaptive Armor mechanism is added.
- The Heavy Robot special mechanisms are added.
- The Hero Robot special mechanisms, Engineer Robot special mechanisms and Aerial Robot special mechanisms are removed.

**Competition Procedure**

The number of backup robots is adjusted.

**Violations and Penalties**

Some penalty provisions are adjusted to fit the rules.

<!-- p.15 -->
### 1.3 About the Competition Rules Documents

The competition rules documents include the Rules Manual, the Participant Manual, the Robot Building Specifications Manual, the communication protocol, and supplements to the above documents. The competition rules documents apply to all participating teams, referees, event staff and other partners.

- During the preparation period, the RMOC will update the competition rules documents from time to time according to actual circumstances.
- During the competition, so that teams can fully demonstrate their technical achievements, the RMOC may adjust the competition rules at the following points, but will not involve direct structural changes to robots.
  - During a Regional Competition: after the matches of a single competition region end.
  - During the Final Tournament: after a stage of the schedule (for example: group stage, Round of 16 to 8) has been fully completed.

The RMOC has the final right of interpretation of the competition rules documents. During the competition, only the Chief Referee answers questions about the competition rules documents on behalf of the RMOC; any question about the competition rules documents may only be directed to the Chief Referee.

> Note: For more reference materials on RMU, see the "Rules/Resource Center". This site is built and maintained by the RoboMaster RMOC and provides, in one place, the official materials needed for participation, intended to help teams obtain information efficiently. Coverage:
>
> - Competition rules: Rules Manual, Robot Building Specifications Manual, Participant Manual, communication protocol.
> - Competition products: Referee System (including onboard modules and the competition engine), robot kits and accessories, RM Assistant product details, downloads, purchase and after-sales policies.
> - Technical Assessment: Technical Assessment detailed rules, notes for each stage.
> - Brand promotion: brand promotion material pack.
> - Sponsorship guidance: sponsorship brochure, sponsorship guide.
> - Training system: participation guides, course salons, open-source materials.

### 1.4 About Q&A

When participating teams and other related personnel have questions about the competition rules documents, they can raise questions through official channels, and the RMOC will answer them. The procedure is as follows:

1. The asker fills in the questionnaire and submits the question:
   https://qingflow.com/f/fpckalpss002?exWsld=1SdM5_PB-NwUtnyPn2b8NA
2. The RMOC will post feedback updates at:
   https://qingflow.com/appView/fpckalpss002/shareView/fpckam8gs001

<!-- p.16 -->
Timeliness:

- For questions submitted during the competition period, the RMOC will respond within 1 calendar day.
- For questions submitted during the preparation period, the RMOC will respond within 5 working days.

> - Competition period: from the check-in day of the event to the end of its last competition day.
> - Preparation period: any period other than the competition period.
>
> Note: The competition period and preparation period of different events and event stages are calculated separately.

Q&A answers have the same effect as the competition rules documents. When a Q&A answer differs from the competition rules documents, the most recently published Q&A answer or competition rules document prevails. Each season's Q&A answers apply only to that season.

<!-- p.17 -->
## 2 Important Concepts

This chapter briefly explains common important concepts related to the competition rules. For details of these concepts, look up the relevant chapters by keyword.

**Table 2-1 Overview of Important Concepts**

| Concept | Definition |
| --- | --- |
| **Robots** | |
| Robot | Collective term for the Ground Robots, Combined Systems and Auxiliary Equipment that a participating team brings and uses to take part in the competition. |
| Ground Robot | A robot that operates independently within the competition field, including the Heavy Robot, Infantry Robot and Sentry Robot. |
| Combined Systems | A robot composed of two or more system units and competing as a whole, including the Dart System, Radar System and Aerial System. The permitted constituent units of a Combined System and their connection, separation or launching methods are as specified in the special rules of each system. |
| System unit | The basic unit that makes up a Combined System, with an independent physical form and function. Except as specified by special rules, a system unit must not be further decomposed into multiple independently moving parts. |
| Auxiliary Equipment | Equipment that assists the operation of Ground Robots and Combined Systems and does not directly take part in competitive confrontation, including: the Custom Terminal. |
| Main robot states | - **Alive**: the state in which the robot's Referee System Main Controller Module is normally connected to the Referee System server and HP is not 0.<br>  - **Disengaged**: the state in which an alive robot has gone 6 s consecutively without launching a projectile and without HP deduction. At the start of the match, robots are in the disengaged state by default.<br>- **Defeated**: the state in which the robot's HP is 0 (causes include: Armor Module attacked or hit by a collision, Referee System module offline, Ejection, HP deduction caused by a dart).<br>  - **Ejection**: the state in which the robot has received a Red Card warning.<br>  - **Temporarily activated**: the state in which, after the robot is Defeated, its chassis and gimbal are temporarily powered on. At this time the robot's launching mechanism is powered off.<br>- **Abnormal offline**: the state in which, during the match, the Referee System Main Controller Module cannot connect to the Referee System server because the robot lost power or for other reasons. |

<!-- p.18 -->
| Concept | Definition |
| --- | --- |
|  | Note: After a robot is Defeated, the Referee System cuts the power output to the robot (except the Mini PC). |
| Referee System | The Referee System is an electronic penalty system for robot competitions that integrates computing, communication and control. It includes the onboard modules and the competition engine installed on PC hosts (server, referee client, player client), and has functions such as monitoring robot power, projectile launching and damage, and automatically determining the winner according to the competition rules. |
| Multi-robot communication | The interaction method in which robots communicate with each other through the Referee System serial port. |
| Chassis | The mechanism that carries the power system of a Ground Robot and its auxiliary components, and supports the body of the Ground Robot. |
| Chassis Power | The power consumption of the mechanism that, based on rotary motion and relying on ground friction, does work for the robot's planar horizontal movement or rotation. For the definition of Chassis Power, see the "Referee System Installation Specifications" chapter of the "RoboMaster 2027 RoboMaster University Series Robot Building Specifications Manual". |
| Launching mechanism | A mechanism that lets a projectile leave the robot along a fixed path and with a certain initial speed. |
| Launching mechanism locked | If the launching mechanism is locked, it is powered off. |
| Launching mechanism unlocked | If the launching mechanism is unlocked, it is powered on or off depending on its Projectile Allowance. |
| Launch | The act of a robot sending out a projectile or dart. "Launch" mentioned in the later "Competition Mechanisms" chapter is based on the launching act detected by the Referee System. |
| Initial Launch Speed | The speed value detected by the relevant Referee System module after the projectile or dart has finished accelerating. |
| Barrel Heat | Barrel Heat increases as the robot fires projectiles and is used to limit continuous firing by the robot. |
| Projectile Allowance | The number of projectiles the robot can currently launch. |
| Initial HP | The HP value set for the robot by the Referee System at the start of the match.<br>Note: the Referee System rounds to an integer when settling HP. |
| Current HP | The robot's real-time HP value. |
| Max HP | The highest value to which the robot's HP can be recovered. |
| Experience | The value a robot must accumulate to level up, which can be obtained in multiple ways. |
| Invincible | The state in which the robot takes no damage from projectiles, darts or collisions. |

<!-- p.19 -->
| Concept | Definition |
| --- | --- |
| Attack | The act of a robot launching projectiles, darts, or of an Aerial Robot making impact. |
| Destroy | One side's robot attacks the Armor Module of an opposing robot, Base or Outpost, reducing its HP to 0. |
| Activate | A surviving robot reaches a Buff Point and its Field Interaction Module detects a Field Interaction Module card in that zone, or other conditions are met. |
| Rigid connection | During a match, a mechanical connection formed between robots such that when one robot moves in any direction, it remains mechanically connected to the other robot. |
| Ramming | An active collision by one side's robot during a match. |
| **Field** | **Field** |
| Buff Point | A zone that produces certain special effects after one side's robot activates it during a match. |
| Restricted Zone | A zone that robots are forbidden to enter. |
| Field props | Components of the Battlefield, including but not limited to: Base, Outpost, Power Rune. |
| **Personnel** | **Personnel** |
| Arbitration Committee | Composed of the Chief Referee and other relevant RMOC personnel; responsible for handling Appeals and related matters. |
| Referee | Personnel who maintain order at the venue and enforce the Rules. |
| Chief Referee | The person with final authority to interpret the rules documents during the competition. |
| Head Referee | The primary referee who maintains order at the venue and enforces the Rules. |
| Chief Inspector | The referee responsible for leading and assigning Pre-Match Inspection work, with final authority to interpret Pre-Match Inspection standards. |
| Participating team | A team that has registered for this season and been entered into the registration system. |
| Participant | A person who has registered for this season and been entered into the registration system. |
| On-site personnel | Official team members, team advisors and supervising teachers who have registered for this season, been entered into the registration system, and may enter the waiting area and the competition area. |

<!-- p.20 -->
| Concept | Definition |
| --- | --- |
| Operator | On-site personnel responsible for controlling robots during a match, including Ground Robot Operators, the Commander and the safety officer. |
| Violating party | A participating team that has committed a violation. |
| Violating person | A participant who has committed a violation. |
| **Match Procedure** | **Match Procedure** |
| Match timing notes | Throughout this document, "X minutes Y seconds" means the countdown reads (6-X):(59-Y); "the period from X minutes Y seconds to M minutes N seconds" means the countdown runs from (6-X):(59-Y) to (7-M):(60-N).<br>**Example:**<br>**- 5 minutes after the start of the match means the countdown reads 1:59.**<br>**- The period from 2 to 5 minutes after the start of the match means the countdown runs from 4:59 to 2:00.** |
| Round | A complete game including the Setup Period, the Referee System Self-Check Period, the Five-Second Countdown and the Round (match phase). |
| Match | Depending on the Competition Format, a match may contain several rounds. |
| Official technical pause | A technical pause initiated by the Head Referee during the Setup Period or the Referee System Self-Check Period. |
| Team technical pause | A technical pause requested by a participating team during the Setup Period. |
| Normal battle damage | A failure of Referee System onboard modules during the three-minute Setup Period between rounds of a match or during the seven-minute Round. |
| **Determining Victory** | **Determining Victory** |
| Attack Damage | HP deduction suffered by one side's robot, Base or Outpost from hits by projectiles or darts and impacts by Aerial Robots.<br>Note: HP deducted from one side's robot, Base or Outpost because of a violation penalty counts as Attack Damage of the opposing side. |
| Non-Attack Damage | HP deduction suffered by one side's robot due to Armor Module collisions, Referee System module going offline, and similar causes. |
| Total Remaining HP | The total remaining HP of all of a side's surviving robots at the end of each round. |
| Control Degree | A measure of one side's overall control of the Battlefield through occupying positions, taken at the end of each round. |

<!-- p.21 -->
## 3 Robots and Operators

RoboMaster emphasizes robots competing as teams and requires balanced cooperation among robots. For robot building specifications, see the *RoboMaster 2027 Robot Building Specifications Manual for the University Series*.

For each match, the participating team must bring the number of each type of robot strictly according to the robot lineup table below.

**Table 3-1 Robot lineup**

| Category | Name | No. | Main lineup quantity | Max reserve quantity | Max Custom Terminals that can be equipped | Max backup Custom Terminals | Event stage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Ground Robot | Heavy Robot | 1 | 1 | 1 | 1 | 1 | RMUC 2027 (entire event) |
| Ground Robot | Infantry Robot | 3/4 | 2 | 2 | 1 per robot | 1 per robot | RMUC 2027 (entire event) |
| Ground Robot | Sentry Robot | 7 | 1 | 2 | 0 | 0 | RMUC 2027 (entire event) |
| Combined Systems | Aerial System | 6 | Hangar: 1<br>Aerial Robot: 4 | Hangar: 0<br>Aerial Robot:<br>BO2/3: 4<br>BO5: 8 | 1 | 1 | RMUC 2027 (entire event) |
| Combined Systems | Dart System | 8 | Dart launcher: 1<br>Dart body: 4 | Dart launcher: 0<br>Dart body:<br>BO2/3: 4<br>BO5: 8 | 1 | 1 | RMUC 2027 (entire event) |
| Combined Systems | Radar System | 9 | Computing platform end: 1<br>Sensor end: 1 | Computing platform end: 0<br>Sensor end: 0 | 0 | 0 | RMUC 2027 (entire event) |

<!-- p.22 -->
The total number of robots a team may register in a standalone event stage is 9 (reserve Dart bodies and reserve Aerial Robots do not count toward the total).

Minimum lineup for the first round of each match: at least 3 Ground Robots.

The Operator lineup is as follows:

**Table 3-2 Operator lineup**

| Type | Robot operated | Number at full lineup |
| --- | --- | --- |
| Ground Robot Operator | Heavy Robot | 1 |
| Ground Robot Operator | Infantry Robot | 2 |
| Ground Robot Operator | Sentry Robot | 0 |
| Commander | Aerial System (optional), Dart System (optional) | 1 |
| Safety officer | Aerial Robot (restricted) | 1 |

> Note:
> - Operators may only be on-site personnel of the participating team for this season other than supervising teachers.
> - After each round, Operators may be replaced by on-site personnel of that match other than supervising teachers.
> - Whether or not the Aerial System and Dart System take part, the Commander may operate the Referee System client for the Aerial System and Dart System, configure a Custom Terminal and wear the corresponding headset, and may not change position after the three-minute Setup Period ends.

<!-- p.23 -->
### 3.1 Robots

#### 3.1.1 Heavy Robot

A Heavy Robot can obtain diverse team Buffs by acquiring and assembling Energy Units; once certain conditions are met, it can also launch 42mm projectiles.

**Table 3-3 Key characteristics of the Heavy Robot**

| Key characteristic | Description |
| --- | --- |
| Initial zone | Starting Zone |
| Operating mode | Unrestricted; at most 1 Remote Controller and 1 Custom Terminal may be configured |
| Multi-robot communication | Allowed |
| Launching mechanism | 1 installable modular 42mm launching mechanism |
| Initial Launch Speed limit (m/s) | 16.5 after the modular 42mm launching mechanism is successfully installed |
| HP deduction and exceeding-the-limit penalty mechanisms | - Initial Launch Speed exceeding the limit: applies<br>- Barrel Heat exceeding the limit and cooling: applies<br>- Chassis Power exceeding the limit: applies<br>- Attack Damage or collision: applies<br>- Referee System module going offline: applies<br>- Penalty Damage: applies<br>See "5.1 HP deduction and exceeding-the-limit penalty mechanisms" |
| HP Recovery and Revival mechanisms | - HP Recovery: through permitted Buff Points or remote exchange of HP.<br>- Revival: progress-bar Revival or exchange for immediate Revival.<br>See "5.3 HP Recovery and Revival mechanisms" |
| Projectile loading and resupply | - During the three-minute Setup Period, the robot may be preloaded with 42mm and 17mm projectiles; the initial Projectile Allowance is 0.<br>- During the seven-minute Round, Projectile Allowance can be exchanged through permitted Buff Points or by remote exchange. |

<!-- p.24 -->
| Key characteristic | Description |
| --- | --- |
| Experience and Performance System | Not applicable<br>Note: The attributes of the Heavy Robot change as the match progresses. |
| Activatable Buff Points | - Base Buff Point<br>- Central Highland Buff Point<br>- Terrain-crossing Buff Points (Road, Highland, Tunnel)<br>- High Point Buff Point<br>- Outpost Buff Point<br>- Assembly Zone Buff Point<br>- Supply Zone Buff Point<br>- Fortress Buff Point<br>See "5.6.4 Field Buff mechanisms" |

**Table 3-4 Key characteristics of the modular 42mm launching mechanism**

| Key characteristic | Description |
| --- | --- |
| Initial zone | Workbench |
| Projectile loading and resupply | - During the three-minute Setup Period, 42mm and 17mm projectiles may be preloaded; the initial Projectile Allowance is 0.<br>- During the seven-minute Round, Projectile Allowance can be exchanged through permitted Buff Points or by remote exchange. |

#### 3.1.2 Infantry Robot

An Infantry Robot can launch 17mm projectiles.

**Table 3-5 Key characteristics of the Infantry Robot**

| Key characteristic | Description |
| --- | --- |
| Initial zone | Starting Zone |
| Operating mode | Unrestricted; at most 1 Remote Controller and 1 Custom Terminal may be configured |
| Multi-robot communication | Allowed |

<!-- p.25 -->
| Key characteristic | Description |
| --- | --- |
| Launching mechanism | 1 17mm launching mechanism |
| Initial Launch Speed limit (m/s) | 25 |
| HP deduction and exceeding-the-limit penalty mechanisms | - Initial Launch Speed exceeding the limit: applies<br>- Barrel Heat exceeding the limit and cooling: applies<br>- Chassis Power exceeding the limit: applies<br>- Attack Damage or collision: applies<br>- Referee System module going offline: applies<br>- Penalty Damage: applies<br>See "5.1 HP deduction and exceeding-the-limit penalty mechanisms" |
| HP Recovery and Revival mechanisms | - HP Recovery: through permitted Buff Points or remote exchange of HP.<br>- Revival: progress-bar Revival or exchange for immediate Revival.<br>See "5.3 HP Recovery and Revival mechanisms" |
| Projectile loading and resupply | - During the three-minute Setup Period, the robot may be preloaded with 42mm and 17mm projectiles; the initial Projectile Allowance is 0.<br>- During the seven-minute Round, Projectile Allowance can be exchanged through permitted Buff Points or by remote exchange.<br>See "5.4 Economy System" |
| Experience and Performance System | Applicable<br>Note: Parameters such as Chassis Power limit, initial HP, Max HP, Barrel Heat Limit and Barrel Cooling Rate depend on Level and chassis type; see "5.5 Experience and Performance System". |
| Activatable Buff Points | - Base Buff Point<br>- Central Highland Buff Point<br>- Terrain-crossing Buff Points (Road, Highland, Tunnel)<br>- High Point Buff Point<br>- Outpost Buff Point<br>- Supply Zone Buff Point |

<!-- p.26 -->
| Key characteristic | Description |
| --- | --- |
| Activatable Buff Points | - Fortress Buff Point<br>See "5.6.4 Field Buff mechanisms" |

#### 3.1.3 Sentry Robot

A Sentry Robot can run fully automatically or semi-automatically and can launch 17mm projectiles.

**Table 3-6 Key characteristics of the Sentry Robot**

| Key characteristic | Description |
| --- | --- |
| Initial zone | Starting Zone |
| Operating mode | At most 1 Remote Controller, used for debugging |
| Multi-robot communication | Can send data to all friendly robots, but can only receive data from the Radar |
| Launching mechanism | 1 17mm launching mechanism |
| Initial Launch Speed limit (m/s) | 25 |
| HP deduction and exceeding-the-limit penalty mechanisms | - Initial Launch Speed exceeding the limit: applies<br>- Barrel Heat exceeding the limit and cooling: applies<br>- Chassis Power exceeding the limit: applies<br>- Attack Damage or collision: applies<br>- Referee System module going offline: applies<br>- Penalty Damage: applies<br>See "5.1 HP deduction and exceeding-the-limit penalty mechanisms" |
| HP Recovery and Revival mechanisms | - HP Recovery: through permitted Buff Points or remote exchange of HP.<br>- Revival: progress-bar Revival or exchange for immediate Revival.<br>See "5.3 HP Recovery and Revival mechanisms" |
| Projectile loading and resupply | - During the three-minute Setup Period, the robot may be preloaded with 17mm and 42mm projectiles; the initial Projectile Allowance is 300.<br>- During the seven-minute Round, Projectile Allowance can be exchanged through permitted Buff Points, obtained directly, or remote exchange of Projectile |

<!-- p.27 -->
| Key characteristic | Description |
| --- | --- |
| (continuation) | Allowance.<br>See "5.4 Economy System" |
| Experience and Performance System | The Experience and Performance System does not apply; performance depends on how the robot is operated, as follows:<br>**Fully automatic Sentry Robot**<br>- Initial HP / Max HP is 400<br>- Barrel Heat Limit is 260<br>- Barrel Cooling Rate is 30/s<br>- Chassis Power limit is 100W<br>**Semi-automatic Sentry Robot**<br>- Initial HP / Max HP is 200<br>- Barrel Heat Limit is 100<br>- Barrel Cooling Rate is 10/s<br>- Chassis Power limit is 60W<br>See "5.7.2 Special Sentry Robot mechanisms" |
| Activatable Buff Points | - Base Buff Point<br>- Central Highland Buff Point<br>- Terrain-crossing Buff Points (Road, Highland, Tunnel)<br>- High Point Buff Point<br>- Outpost Buff Point<br>- Supply Zone Buff Point<br>- Fortress Buff Point<br>See "5.6.4 Field Buff mechanisms" |

<!-- p.28 -->
### 3.2 Combined Systems

#### 3.2.1 Aerial System

The Aerial System can perform diverse attack and reconnaissance tasks on the Battlefield.

**Table 3-7 Key characteristics of the Aerial Robot**

| Key characteristic | Description |
| --- | --- |
| Initial zone | Hangar |
| Operating mode | Fully automatic, but must be equipped with one Remote Controller for emergency stop |
| Multi-robot communication | Only indirect communication through the Hangar is allowed |

**Table 3-8 Key characteristics of the Hangar**

| Key characteristic | Description |
| --- | --- |
| Initial zone | Hangar platform |
| Operating mode | Unrestricted; at most 1 Remote Controller may be configured |
| Multi-robot communication | Allowed |
| Launching mechanism | Not applicable |
| Projectile loading and resupply | Not allowed |

#### 3.2.2 Dart System

The Dart System can attack the opposing Outpost and Base by launching darts.

**Table 3-9 Key characteristics of the Dart System**

| Key characteristic | Description |
| --- | --- |
| Initial zone | Dart Launching Station |
| Operating mode | Unrestricted; at most 1 Remote Controller may be configured |
| Multi-robot communication | Allowed |

<!-- p.29 -->
#### 3.2.3 Radar System

The Radar can autonomously obtain Battlefield information, send information to friendly robots or the Referee System client through multi-robot communication, and can also intercept the opposing side's information.

**Table 3-10 Key characteristics of the Radar System**

| Key characteristic | Description |
| --- | --- |
| Initial zone | Radar Base |
| Operating mode | Runs automatically; at most 1 Remote Controller, used for debugging |
| Multi-robot communication | Can send data to all friendly robots, but can only receive data from the Sentry Robot |

### 3.3 Auxiliary Equipment

#### 3.3.1 Custom Terminal

The Custom Terminal (formerly the custom controller and custom client) is a multi-purpose device built by participating teams. It is used to monitor robot motion and status, control robot actions, receive match-related information and robot video transmission feeds sent by the Referee System match engine server, and send match-specific interaction commands to the match engine server, extending the possibilities of human-robot interaction.

A typical Custom Terminal may consist of a display device, a computing platform (including memory, a controller and a processor) and a set of input devices; it may also take an integrated form, for example: a handheld tablet with a network port.

> **Example: A team builds a Custom Terminal that receives the robot video transmission and presents it on a self-made display, overlays a self-made UI shown through an unofficial link, and controls the robot through a matching controller. The team can thus complete a match without using the official Referee System client or Remote Controller.**

All Custom Terminals in the Operator Room may be wired to one another and communicate, and a Custom Terminal may connect by wire to the match engine server through the RJ45 port provided in the Operator Room to send and receive related content.

A Custom Terminal can receive the match information that is shown on the Referee System client and available to its own side, for example: both sides' HP, its own side's economy, remaining match time and key match events.

A Custom Terminal can send to the Referee System the match commands supported by the client, for example: active commands such as selecting the Performance System before the match, exchanging Projectile Allowance during the match, and intervening in Sentry Robot actions.

<!-- p.30 -->
## 4 Battlefield

### 4.1 Battlefield overview

> Note:
> - Unless otherwise marked, all dimensions described in this document carry certain tolerances. Structural error for dimensions under 100mm is within ±5mm; error for dimensions of 100mm or more is within ±5%; angular error of Battlefield structures is within ±3°; angular error of field props is within ±1°. Dimension parameters in the field drawings are in mm. To ensure field stability and safety, detailed dimensions and processes may be adjusted during actual construction; for Battlefield elements/dimensions not detailed in the drawings, the actual field prevails.
> - The Battlefield has a centrally symmetric layout. Some descriptions and illustrations of field modules in this document use the red side as an example; the blue side is the same. The field environment is complex, and there may be asymmetric environmental factors such as uneven magnetic fields and venue air-conditioning airflow.
> - Renderings are for illustration only; specific dimensional details follow the corresponding drawings. Matters not covered follow the actual situation at adaptive training.
> - The Battlefield contains multiple Buff Points and Restricted Zones. To keep the document concise and clear, this chapter does not describe them one by one; their specific definitions are given together in "5.6.4.1 Field Buff Point overview" and "7.2.3.2 Robot interaction with field props".

The core competition field of RMUC is called the "Battlefield". The Battlefield is an area 28m long and 15m wide, with a wooden internal structure covered with 2mm thick PVC floor covering or PVC wire-embedded floor covering, and some structures have a metal protective layer. It mainly contains the Base Zone, Highland Zone, Road Zone and so on. Around the Battlefield is a black steel barrier whose upper edge is 2.4m above the Battlefield floor.

*Figure 4-1 Top-view rendering of the Battlefield*

<!-- p.31 -->
*Figure 4-2 Oblique-view rendering of the Battlefield*

*Figure 4-3 Axonometric rendering of the Battlefield*

<!-- p.32 -->
- [1] Supply Zone
- [2] Road Zone
- [3] Road Tunnel
- [4] Outpost
- [5] Far Highland Tunnel
- [6] Near Highland Tunnel
- [7] Red Hangar platform
- [8] Blue Assembly Zone
- [9] Fortress
- [10] High Point
- [11] Dart Launching Station
- [12] Radar Base
- [13] Workbench
- [14] Resource station
- [15] Base
- [16] Central Highland
- [17] Blue Hangar platform
- [18] Power Rune
- [19] Tech Core
- [20] Red Assembly Zone
- [21] Trapezoidal Highland
- [22] Fan

*Figure 4-4 Battlefield module diagram*

<!-- p.33 -->
- Dimension labels (mm): horizontal 28000, 25589, 17024, 9180, 6571, 2075; vertical 15000, 7500, 3600, 826; also 2600, 1480, 2186, 1838; angles 10.5°, 15.8°.
- [1] Parallel to the long side of the Battlefield and in the facing direction of the Dart Launching Station

*Figure 4-5 Battlefield module positioning dimension drawing*

<!-- p.34 -->
All dimensions in this document are marked relative to the left-right sloped surfaces. The actual Battlefield is not level: it slopes 1° to 2° toward both long sides about the Battlefield centre axis, as shown in the figure below. The Battlefield slope causes projectiles to flow toward both long sides.

> Note: To allow projectiles to be recovered smoothly, grooves about 50mm high may exist along the lines where some wooden Battlefield structures meet the floor, and ducted fans inside the wooden Battlefield structure will be briefly switched on after the match ends.

- [1] Higher side
- [2] Lower side
- [3] Base pedestal
- [4] Fortress pedestal
- [5] Assembly Zone pedestal

*Figure 4-6 Battlefield slope diagram*

<!-- p.35 -->
- Dimension labels (mm, in parentheses in the figure): 353, 94, 219.
- [1] Air inlet
- [2] Air outlet

*Figure 4-7 Fan diagram*

> Note: The fans are embedded into the wooden structure according to the shape of the wooden structure on the field.

<!-- p.36 -->
### 4.2 Base Zone

The Base Zone contains the Starting Zone, Base, Dart Launching Station, High Point, Radar Base, Supply Zone and Fortress.

- [1] Dart Launching Station
- [2] High Point
- [3] Fan
- [4] Starting Zone
- [5] Radar Base
- [6] Fortress
- [7] Workbench
- [8] Supply Zone
- [9] Resource station

*Figure 4-8 Base Zone diagram*

<!-- p.37 -->
#### 4.2.1 Starting Zone

The Starting Zone is the hexagonal area around the Base, where Ground Robots are placed before the match starts.

*Figure 4-9 Schematic of the robot Starting Zone*

- [1] Starting Zone
- Dimensions (mm): horizontal 4245, 2208, 1651, 770; vertical 2385, 1692, 4045

<!-- p.38 -->
#### 4.2.2 Base

The Base is the core of attack and defense for both sides. It is placed on the Base mount at the center of each side's Starting Zone.

The Base consists of the Base body, 6 Base Armor Modules, a Dart detection module, Base armor plating, etc. The Base armor plating has two states: armor closed and armor open.

*Figure 4-10 Schematic of the Base mount*

- Dimensions (mm): 1873, 1094, 772, 665, 1609, 200 (height)

*Figure 4-11 Dimensions of the Base with armor closed*

- [1] Base Armor Module
- [2] Dart detection module
- Dimensions (mm): width 980; heights 860, 905, 1043, 1093, 1150, 1181; side view angle 27.5°

<!-- p.39 -->
*Figure 4-12 Dimensions of the Base with armor open*

- Dimensions (mm): heights 312, 860, 905, 1043, 1093, 1150, 1181; angles 27.5°, 27.5°, 90°

The Dart detection module is located on the upper part of the Base and the Outpost, and consists of a Dart armor module, a Dart detection sensor and a Dart guidance light.

The Dart armor module of the Dart detection module can detect Dart hits; the Dart detection sensor can detect the infrared beam emitted by the Dart trigger device. When the projection of the Dart trigger device onto the Dart detection module falls entirely within the Dart armor module, and the Dart detection module detects both the infrared beam and a hit at the same time, the system considers the module to have been hit by a Dart; if only a hit is detected, the system considers the module to have been hit by a projectile. The Dart guidance light emits green visible light in the 520nm band. When approximated as a point light source, its luminous intensity is about 10cd, and the diameter of the light-emitting part is about 55mm. It is used to guide the Dart to hit the target.

> Note: When the projection of the Dart trigger device onto the Dart detection module does not fall entirely within the Dart armor module, the Dart detection module may still recognize it successfully with a certain probability.

<!-- p.40 -->
*Figure 4-13 Schematic of the Dart detection module*

- Base Dart detection module (dimensions, mm: 242, 140, 239, 81, 25; section A-A angle 228°)
- Outpost Dart detection module (dimensions, mm: 140, 141, 23)
- [1] Dart armor module
- [2] Dart detection sensor
- [3] Dart guidance light

<!-- p.41 -->
#### 4.2.3 Dart Launching Station

The Dart Launching Station is the only placement area for the Dart System, and consists of a station body, a sliding platform and a gate. The Dart Launching Station contains a lighting device that cannot be turned off. During the Referee System self-check period, the Dart Launching Station gate opens briefly (about 5 s); while it is open, the Dart detection module remains stationary at the position corresponding to the Base fixed target. During the three-minute Setup Period and the 15-Second Referee System Initialization Period, the Dart guidance lights of both the Outpost and the Base are lit.

*Figure 4-14 Schematic of the Dart Launching Station*

- [1] Gate
- [2] Status indicator light
- [3] Dart System placement space
- [4] Sliding platform
- [5] Station body
- Dimensions (mm): 1870, 1322±10, 1000 (horizontal); 1214±10, 1147±10, 1000, 205 (vertical)

*Figure 4-15 Schematic of the sliding platform extended*

- Dimensions (mm): 600, 700

<!-- p.42 -->
*Figure 4-16 Dimensions of the sliding platform*

- [1] Dart System placement plane
- [2] Support wheel
- Dimensions (mm): 1000, 600; 45, 20, 205

#### 4.2.4 High Point

The High Point is located in the Base Zone. The junction between the Trapezoidal Highland and the High Point is a three-level step, which robots can climb to enter the High Point.

*Figure 4-17 Schematic of the High Point*

- Dimensions (mm): 2400, 1394, 1200 (both directions)
- Section A-A: 300, 300, 100; 200, 200, 200; (600)
- Section B-B: 300, 300, 300, 100; (800), 200, 200, 200, 200; 100, 300

<!-- p.43 -->
#### 4.2.5 Radar Base

The Radar Base is used to place the Radar System. Its top is a platform with an area of 3.4m*1.16m. The center of the platform plane is aligned with the central axis of the battlefield, at a height of about 2.4m above the battlefield floor, and is surrounded by a 1.1m-high railing. Next to the platform there is a sensor data cable slot. Use it during the match according to the actual field conditions.

The Radar computing end is powered by 220V mains, and its placement platform is provided with:

- 1 official display device that supports only HDMI signal input, with a display resolution of 1920*1080. Teams can use it to confirm the operating status of the Radar System.
- 1 HDMI male signal cable, used to connect the Radar System to the official display device.
- 1 new-national-standard 5-hole socket, in which the single-phase two-pole and single-phase three-pole sockets can be used at the same time to power the Radar System. This socket cannot be moved.

*Figure 4-18 Schematic of the Radar Base*

- [1] Radar information wave
- [2] Sensor data cable slot
- [3] Radar information wave emitting surface
- [4] Radar sensor placement platform
- [5] Radar computing end placement platform
- Dimensions (mm): 3400, 1210, 1160, 235, Ø150, (230), (509), (426), 190, 2400, 900, 1100, 2450, 2700, 3800, 900

<!-- p.44 -->
*Figure 4-19 Schematic of the relative position of the Radar Base*

- [1] Battlefield entrance/exit
- [2] Entrance/exit steps
- [3] Radar Base
- Dimensions (mm): 40, 200, 425, 2710

<!-- p.45 -->
#### 4.2.6 Supply Zone

The Supply Zone includes the resource station, the Supply Zone Buff Point and the Workbench. It is an important area where robots recover HP, replenish Projectile Allowance, obtain Energy Units, and install the modular 42mm launching mechanism.

*Figure 4-20 Schematic of the Supply Zone*

- [1] Fan
- [2] Supply Zone

<!-- p.46 -->
The resource station is the area where Heavy Robots obtain Energy Units. It contains 6 Energy Units, all held in the Energy Unit placement area by magnetic attraction. A Heavy Robot must remove an Energy Unit along the direction of the Energy Unit's rotational symmetry axis. In addition to overcoming gravity, this process requires applying an extra force of up to 10N to overcome the magnetic attraction.

*Figure 4-21 Schematic of the resource station*

- [1] Energy Unit placement area
- [2] Baffle
- Dimensions (mm): 700, 50, 150

> Note: The actual installed position of an Energy Unit may have an angular deviation about its symmetry axis relative to the figure. The figure is for illustration only; refer to the actual placement.

<!-- p.47 -->
*Figure 4-22 Schematic of the Energy Unit placement area*

- Dimensions: Ø454, 60°, 102, 38, 77 (mm)

The Workbench is located in the Supply Zone. Robots can pick up and install the modular 42mm launching mechanism.

*Figure 4-23 Schematic of the Workbench*

- Dimensions (mm): 400, 450, 350, 650, 750

<!-- p.48 -->
The wall of the Road Zone facing the Supply Zone is fitted with metal vision tags, which the camera Video Transmitter Module uses to determine whether a robot is in the Supply Zone, as shown below.

*Figure 4-24 Schematic of the vision tags*

- [1] Vision tag
- Wall dimensions (mm): (2970), (400)
- Red side vision tag: outer 340 x 340, inner 280 x 280 (mm)
- Blue side vision tag: outer 340 x 340, inner 280 x 280 (mm)

<!-- p.49 -->
#### 4.2.7 Fortress

The Fortress is a key defensive area of the Base Zone.

*Figure 4-25 Schematic of the Fortress*

- [1] 20° slope
- Dimensions (mm): 2107, 1131, 1216, 653, 150

<!-- p.50 -->
### 4.3 Highland Zone

A highland is a part of the battlefield that is higher than the battlefield floor. There is 1 Trapezoidal Highland on each of the red and blue halves, plus the Central Highland in the middle of the battlefield. They divide the battlefield into multiple areas and form a three-dimensional battlefield in space.

#### 4.3.1 Trapezoidal Highland

The Trapezoidal Highland is located near the High Point, and its height above the battlefield floor is 200mm.

*Figure 4-26 Schematic of the Trapezoidal Highland*

- [1] 23° slope
- Dimensions (mm): 6682, 2717, 4131, 1140, 4586, 200 (height)

<!-- p.51 -->
#### 4.3.2 Central Highland

The Central Highland is located in the middle of the battlefield, and its two ends connect to the Road Zone through ramps.

*Figure 4-27 Schematic of the Central Highland*

- [1] Red Assembly Zone
- [2] Blue Assembly Zone
- [3] 12° slope
- [4] Fan
- [5] Metal plate
- Dimensions (mm): 10820, 7740, 2988, 800, 190, 1090, 150; section A-A: 200, 350, 400, 300, 360

<!-- p.52 -->
##### 4.3.2.1 Assembly Zone

The Assembly Zone is located at the center of the battlefield, directly below the Power Rune. It is divided into red and blue sides. A Tech Core is installed below the Power Rune, and Heavy Robots can assemble Energy Units onto the Tech Core, as shown in the figure below.

*Figure 4-28 Isometric view of the Assembly Zone*

- [1] Power Rune
- [2] Tech Core
- [3] Red Assembly Zone
- [4] 14° slope
- [5] Blue Assembly Zone
- [6] 12° slope
- [7] 46° slope
- [8] 12° slope
- Dimensions (mm): 300, 100

<!-- p.53 -->
*Figure 4-29 Dimensions of the Assembly Zone*

- Dimensions: 2199, 1230, 1411, 927, 383 (mm); angles 61°, 95°

<!-- p.54 -->
##### 4.3.2.2 Hangar Platform

The Hangar platform is located at the center of the battlefield and is divided into red and blue sides. Each side can install its Aerial system only on the Hangar platform.

*Figure 4-30 Schematic of the Hangar platform*

- [1] Red Hangar platform
- [2] Blue Hangar platform
- Dimensions (mm): 400, 320, 320, 400 (landing pad), 40 (detail B), 1200

<!-- p.55 -->
##### 4.3.2.3 Power Rune

The Power Rune is located directly above the assembly zone. The Power Rune is driven by motors and rotates synchronously according to a fixed pattern. The Power Rune is divided into red and blue sides: one side is the red Power Rune and the other side is the blue Power Rune.

> Note:
> - Because of the heavy weight of the middle part of the Power Rune, it may sag slightly. The sag range is 0~50mm.
> - Because of the viewing angle and transmission backlash, part of the opposing Power Rune may be visible when observing one side's Power Rune.

The Power Rune has 5 evenly distributed light arms. Their positions and dimensions are shown below:

*Figure 4-31 Power Rune diagram*

- Dimensions: 72°; Ø1400; 2300; 300

*Figure 4-32 Power Rune light arm dimensions diagram*

- Dimensions: 372; 320; 29; 382; 36; 24; 60; 136; 330; 203; 20; 215; Ø300; Ø308; 121°; 120°

<!-- p.56 -->
> Note: The maximum diameter of the circular target on an actual light arm is 308mm, and the actual effective detection diameter is 300mm.

*Figure 4-33 Power Rune center marking dimensions diagram*

- Dimensions: Ø106

<!-- p.57 -->
##### 4.3.2.4 Outpost

The Outpost is placed on the Outpost base and consists of the Outpost main body, 3 Outpost Armor Modules, and a dart detection module. For the dart detection module diagram, see "Figure 4-13 Dart detection module diagram". The Outpost Buff Points are located around the Outpost; their specific positions are shown in the figure below.

*Figure 4-34 Outpost diagram*

- Dimensions: 120°; Ø550; 1216; 1114; 1318; 571; 1110; 1446; 1496; 1554; 1578; 75°; 27.5°; 75°; 650; 300; 400; 1878

[1] Outpost base  [2] Outpost  [3] Middle armor

<!-- p.58 -->
### 4.4 Road Zone

The Road Zone includes the road, Tunnels, and Bumpy Roads.

*Figure 4-35 Road Zone diagram*

- Dimensions (top view): 3902; 3125; 2634; 1858; 1500; 1148; 350; 3801; 1561; 2090; 690; 764; 350; 400
- Section A: 800; (358); 260; 200
- Section B: 800; 250; (417)

[1] 11° slope  [2] 15° slope

<!-- p.59 -->
#### 4.4.1 Bumpy Road

The Bumpy Road is located in the Road Zone. Its surface has bumps arranged at fixed spacing and in the direction shown, as follows:

*Figure 4-36 Bumpy Road diagram*

[1] Bumpy Road

*Figure 4-37 Bump diagram*

- Dimensions: 70; 240

[1] Bump

<!-- p.60 -->
#### 4.4.2 Tunnel

Tunnels are located in the Road Zone. Robots can pass through or cross over a Tunnel to quickly reach the opponent's half of the field.

*Figure 4-38 Far Highland Tunnel diagram*

- Dimensions: 350; 800; 1350; 2900; 200; 250; 270

[1] Metal plate

### 4.5 Other

#### 4.5.1 Movable Props

The Energy Unit is a Movable Prop that can be grasped and carried by robots. The Energy Unit is a hollow cylinder weighing approximately 400±50g, with asymmetric ends.

> Note: As the competition proceeds, the surface of Movable Props may show slight damage or dust accumulation. Participating teams must adapt to this themselves, but severely worn or soiled Movable Props will not be used in official matches.

<!-- p.61 -->
*Figure 4-39 Energy Unit diagram*

- Dimensions: Ø95±1; Ø85±1; Ø60±1; Ø65±1; Ø40±1; 30±1; 40±1; 150±1; 75±1; 100±1; 25±1; Ø80±1

[1] Iron plate

<!-- p.62 -->
#### 4.5.2 Projectiles

Robots can launch projectiles to attack Armor Modules and thereby cause damage. The projectile parameters and arrangements used in matches are as follows:

**Table 4-1 Projectile parameters and usage arrangements**

| Type | Appearance | Color | Size | Mass | Shore hardness | Material | Usage arrangement | Rated quantity |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 42mm luminous projectile | Similar in shape to a golf ball | Translucent | 42.5mm ±0.5mm | 44.5g ±0.5g | 90±5A | Plastic TPE | Whole season | 100 per round |
| 17mm fluorescent projectile | Spherical | Yellow-green | 16.8mm ±0.2mm | 3.2g±0.1g | 90±5A | Plastic TPU | Whole season | Limited, but not less than 3000 per round |

#### 4.5.3 Operator Room

The Operator Room is located near the outside of the Battlefield and is the area where Operators work during the match. Each Operator's desk in the Operator Room is 120cm long and 75cm wide, and is equipped with a corresponding number of computers. Each computer is equipped with official equipment including a corresponding monitor, mouse, keyboard, camera Video Transmitter Module (receiver) and its bracket, one 1GbE (RJ45) network port, and a wired headset.

Heavy Robot Operators and Commanders are additionally provided with 1 official display device that supports only HDMI signal input, with a display resolution of 1920*1080, and 1 HDMI male signal cable for connecting the Custom Terminal to the official display device. Participating teams may use it to display the Custom Terminal's picture.

Physical partitions will exist in the Operator Room, separating Ground Robot Operators from Commanders.

The desktop layout of the Operator Room is shown below. The Operator Room desktop has a monitor, a broadcast camera, a camera Video Transmitter Module (receiver) and its bracket, a keyboard, a mouse, and a device placement area. The positions of the monitor, broadcast camera, and ports are fixed and cannot be moved. The camera Video Transmitter Module (receiver) bracket is fixed on the desktop, and the Operator may operate the camera Video Transmitter Module (receiver) within the bracket's range of movement. The keyboard and mouse can be moved freely, and the Operator may place the Custom Terminal on the placement area. The specific layout is shown in the figure below:

<!-- p.63 -->
Infantry Robot Operator layout diagram

Heavy Robot Operator and Commander layout diagram

*Figure 4-40 Operator Room layout diagram*

- Dimensions (both layouts): 1200; 500; 750

[1] Port position  [2] Monitor  [3] Keyboard and mouse  [4] Placeable area
[5] Broadcast camera  [6] Camera Video Transmitter Module (receiver) and its bracket  [7] Storage shelf

<!-- p.64 -->
> Note:
> - It is forbidden to remove the camera Video Transmitter Module (receiver) from its bracket. Teams bear the consequences of doing so themselves.
> - Robots entering the Battlefield automatically connect to the camera Video Transmitter Module (receiver) in the Operator Room. A camera Video Transmitter Module (receiver) brought by the participating team will not work. The default state of the joystick on the Operator Room's camera Video Transmitter Module (receiver) is: centered. The default state of the toggle switch is: position C.

<!-- p.65 -->
## 5 Match Mechanics

### 5.1 HP Deduction and Limit-Exceeding Penalty Mechanisms

#### 5.1.1 Attack Damage or Collision

When the Armor Modules of Ground Robots, the Base, and the Outpost are attacked or collided with, HP may be deducted. The specific mechanism is as follows:

The dart detection module detects dart attacks through the combination of an Armor Module and photoelectric sensors.

Armor Modules can detect projectile attacks and Aerial Robot impacts. The minimum detection interval is 50ms for 17mm projectiles and 200ms for 42mm projectiles.

When a projectile or Aerial Robot contacts the attacked surface of an Armor Module, certain requirements must be met for it to be validly detected. The detection requirements of Armor Modules for different types of attack are shown in the table below:

**Table 5-1 Effective detection speed of Armor Modules for different types of projectiles**

| Armor Module | 17mm projectile | 42mm projectile | Aerial Robot impact |
| --- | --- | --- | --- |
| Small Armor Module | Greater than 12m/s | Greater than 8m/s | Contact time ∈ [TBD]<br>Surface cumulative impulse during contact ∈ [TBD]<br>Explanation:<br>The detection principle of an Armor Module for impacts: when the Armor Module's detection surface recognizes a contact force higher than αN at any position, an "impact event" starts; the "impact event" ends once the contact force at all positions is lower than αN.<br>Contact time is the duration of one "impact event".<br>Impact area S is the sum of the areas of all regions whose instantaneous contact force is greater than αN during the entire "impact event" (the regions may be non-contiguous). Surface cumulative impulse is ∬FdtdS, that is, the double integral of the contact force over the impact area with respect to the contact time and the impact area during the "impact event". |
| Base Armor Module | Greater than 12m/s | Greater than 8m/s | Same as Small Armor Module (merged cell) |
| Outpost Armor Module | Greater than 12m/s | Greater than 8m/s | Same as Small Armor Module (merged cell) |
| Power Rune Armor Module | Greater than 12m/s | - | - |

<!-- p.66 -->
> Note:
> - In actual matches, because of projectile speed decay and because the incidence angle is not along the normal of the Armor Module's attacked surface, the normal velocity of a projectile contacting the attacked surface differs from its Initial Launch Speed. Damage detection is based on the normal component of the projectile's velocity when it contacts the Armor Module's attacked surface.
> - Participating teams must not use 42mm projectiles, darts, or Aerial Robots to hit the Power Rune.
> - When a side's Heavy Robot has not launched a 42mm projectile for 4 consecutive seconds, all armor of the opponent's robots, Outpost, and Base will block 42mm projectile damage until a Heavy Robot launches a 42mm projectile.
> - To ensure detection accuracy and reduce false detections, in some cases the Referee System must wait for the 42mm projectile launch information to match. Therefore, after an Armor Module detects a 42mm projectile hit, damage settlement may be slightly delayed.

When the Armor Modules of Ground Robots, the Base, and the Outpost are collided with, there is a probability that the collision is judged as projectile damage. Except for Aerial Robot impacts, it is not allowed to cause damage to the opponent by collision (including colliding with robots, throwing objects, etc.).

With no Buffs, the base damage values are shown in the table below:

**Table 5-2 HP deduction mechanism for attack damage or collision**

| Target \ Damage type | 42mm projectile | 17mm projectile | Aerial Robot impact | Dart | Collision |
| --- | --- | --- | --- | --- | --- |
| Robot Armor Module | 200 | 20 | - | - | 2 |
| Base Armor Module | 200 | 20 | 200 | - | - |
| Base dart detection module | - | - | - | - Fixed target: 200<br>- Random fixed target: 300<br>- Random moving target: 800<br>- End moving target: 1250 | - |
| Outpost middle Armor Module | 200 | 20 | 200 | - | - |
| Outpost dart detection module | - | - | - | 1000 | - |

<!-- p.67 -->
#### 5.1.2 Initial Launch Speed Exceeding the Limit

When a Ground Robot's Initial Launch Speed exceeds the limit, the robot's launching mechanism will be locked and unlocked after a certain time; times do not accumulate.

Locking and unlocking caused by exceeding the Initial Launch Speed limit are independent of locking and unlocking caused by other conditions. Let the robot's Initial Launch Speed limit be V0 (m/s), and let the actual Initial Launch Speed of a projectile detected by the Referee System be V1 (m/s). The specific lock times are shown in the table below:

**Table 5-3 Penalty mechanism for Initial Launch Speed exceeding the limit**

| 17mm projectile | 42mm projectile | Lock time |
| --- | --- | --- |
| 0 < V1 - V0 < 5 | V0 < V1 ≤ 18 | 15 s |
| 5 ≤ V1 - V0 < 10 | - | 20 s |
| 10 ≤ V1 - V0 | 18 < V1 | Remainder of the round, no unlocking |

#### 5.1.3 Barrel Heat Exceeding the Limit and Cooling

When a Ground Robot's Barrel Heat exceeds the limit, the robot's launching mechanism will be locked. Locking and unlocking caused by Barrel Heat exceeding the limit are independent of locking and unlocking caused by other conditions. The specific mechanism is as follows:

Let the robot's Barrel Heat Limit be Q0 and the current Barrel Heat be Q1. For each 17mm projectile the Referee System detects, the current Barrel Heat Q1 increases by 10 (regardless of the 17mm projectile's Initial Launch Speed). For each 42mm projectile detected, Q1 increases by 100 (regardless of the 42mm projectile's Initial Launch Speed). Barrel Heat cooling is settled at a frequency of 10Hz; the cooling value per detection cycle = cooling value per second / 10.

When Q2>Q1>Q0, the first-person operation interface video feed of the corresponding Operator of that robot is disconnected and the launching mechanism is locked. The first-person operation interface returns to normal and the launching mechanism is unlocked only when Q1=0.

When Q1>Q2, the robot's launching mechanism is locked for the remainder of the round and is not unlocked again.

For a 17mm launching mechanism, Q2=Q0+100;

For a 42mm launching mechanism, Q2=Q0+200.

<!-- p.68 -->
*Figure 5-1 Barrel Heat exceeding the limit and cooling mechanism*

- Start, then two parallel loops:
- Loop 1: "Detect one projectile" -> "Projectile type is 17mm projectile?" YES: "Q1 = Q1 + 10"; NO: "Q1 = Q1 + 100". Both lead to "Q1 ≥ Q2?" YES: "The robot's launching mechanism is locked for the remainder of the round and is not unlocked again" (returns to start of loop 1); NO: "Q1 > Q0?" YES: "Robot launching mechanism locked, video feed disconnected" (returns to start of loop 1); NO: returns to start of loop 1.
- Loop 2: "100ms detection cycle reached" NO: returns to start of loop 2; YES: "Q1 = Q1 - cooling value per second / 10" -> "Q1 ≤ 0?" YES: "Q1=0, robot launching mechanism unlocked, video feed returns to normal" (returns to start of loop 2); NO: returns to start of loop 2.

> Note: When the video feed is disconnected because of excess heat, the mini-map and custom UI can still be used normally.

#### 5.1.4 Chassis Power Exceeding the Limit

The Referee System continuously monitors the robot's Chassis Power; the robot chassis must operate within the power limit. When a Ground Robot's Chassis Power exceeds the limit, the robot will have Buffer Energy deducted. When the Buffer Energy is exhausted and the Chassis Power still exceeds the limit, the chassis will be powered off for 5 seconds. The Referee System settles the Chassis Power detection at a frequency of 10Hz.

Let Z be the Buffer Energy, Q be the Buffer Energy upper limit (Q=60J), Pr be the instantaneous chassis output power, and Pl be the power limit.

<!-- p.69 -->
*Figure 5-2 Robot Chassis Power detection and limit-exceeding penalty mechanism*

- Start -> "Buffer Energy Z = Q" -> "100ms detection cycle reached?" NO: returns to this check; YES: "Calculate work consumed: Z = Z - (Pr-Pl) × 0.1" -> "Z ≤ 0?" YES: "Z = 0, chassis powered off for 5 s" (then returns to the 100ms check); NO: "Z > Q?" YES: "Z = Q" (then returns to "Buffer Energy Z = Q" step); NO: returns to the 100ms check.

#### 5.1.5 Referee System Module Offline

Participating teams must install the robot's corresponding Referee System modules as required by the "RoboMaster 2027 RoboMaster University Series Robot Building Specifications Manual" and must keep each Referee System module's connection to the server stable during the match. The Referee System server checks the connection status of each module at a frequency of 2Hz.

<!-- p.70 -->
##### 5.1.5.1 Abnormal Offline

During a match, if a robot's Main Controller Module goes offline, it enters the "abnormal offline" state and can reconnect to the match. Experience and Level continue to be settled during the offline period.

**Table 5-4 Penalty mechanism for robot abnormal offline**

| Robot type | Handling during offline period |
| --- | --- |
| Ground Robot | Launching mechanism (if any), gimbal, and chassis are powered off; 5% of Max HP is deducted per second until HP reaches 0 |
| Ground Robot | Field Interaction Module becomes ineffective |
| Ground Robot | The robot no longer detects damage caused by collisions and projectile hits, or HP deduction for module offline |
| Ground Robot | Revival progress no longer increases |
| Ground Robot | Multi-robot communication is disconnected |
| Hangar | Actuators are powered off |
| Hangar | Multi-robot communication is disconnected |
| Radar System | Multi-robot communication is disconnected |
| Dart System | If offline while the Dart Launching Station gate is closed: the Dart Launching Station gate cannot be opened |
| Dart System | If offline while the Dart Launching Station gate is open: the Dart Launching Station gate closes immediately and cannot be opened |

<!-- p.71 -->
##### 5.1.5.2 Armor Module or Supercapacitor Management Module Offline

If a Ground Robot's Armor Module or Supercapacitor Management Module goes offline because of the robot's own design, structure, or similar problems, the robot will have HP deducted.

*Figure 5-3 HP deduction mechanism for Armor Module and Supercapacitor Management Module offline*

- Start -> "500ms detection cycle reached?" NO: returns to this check; YES: "Is an Armor Module or Supercapacitor Management Module offline?" NO: returns to the 500ms check; YES: "Count the number N of offline Armor Modules and Supercapacitor Management Modules" -> "Calculate HP deduction value: Value = 4*N" -> "Deduct the robot's HP" -> returns to the 500ms check.

<!-- p.72 -->
##### 5.1.5.3 Speed Monitor Module Offline

If a 17mm Speed Monitor Module or 42mm Speed Monitor Module loaded on a Ground Robot goes offline, that robot's 17mm or 42mm launching mechanism is locked immediately. Locking and unlocking caused by Speed Monitor Module offline are independent of locking and unlocking caused by other conditions.

*Figure 5-4 Power-off mechanism for Speed Monitor Module offline*

- Start -> "500ms detection cycle reached?" NO: returns to this check; YES: "Speed Monitor Module offline?" NO: "No additional handling" (returns to the 500ms check); YES: "Corresponding 17/42mm launching mechanism locked" -> "Speed Monitor Module reconnected to the server?" NO: returns to this check; YES: "Corresponding 17/42mm launching mechanism unlocked" -> returns to the 500ms check.

##### 5.1.5.4 Positioning Module Offline

If the Positioning Module loaded on a Ground Robot goes offline, the opponent's Radar marking of that robot is always treated as "accurate", and the friendly Radar marking of that robot is always treated as "wrong".

#### 5.1.6 Penalty Damage

When a Ground Robot receives a penalty such as a Yellow Card or Red Card Warning, HP may be deducted; see "7.1 Penalty System".

<!-- p.73 -->
### 5.2 Adaptive Armor Mechanism

During a match, a team may independently choose to reinforce one specific region of all of its own Armor Modules. Projectile damage taken in the reinforced region is reduced, and projectile damage taken in the unreinforced region is increased. The area of the reinforceable region of an Armor Module is jointly determined by the projectile hit accuracy of both sides: the higher a side's relative accuracy, the larger its reinforceable region. The specific mechanism is as follows:

At the start of the match, all armor plates are in the "default" state. After the match starts, each side gains 1 accumulable reinforcement opportunity every 1 min. After a side's cumulative number of projectiles hit in the current round is >= 10, that side's Radar may at any time send a command to the Referee System server to spend 1 reinforcement opportunity to select or change 1 center point. Until the center point is next changed, on all of that side's robots, Outpost and Base Armor Modules, the circular region with the selected center point as its center and area A is regarded as "reinforced", and the remaining region is regarded as "unreinforced".

The damage multipliers for projectiles hitting unreinforced, reinforced and default-state regions are as follows:

**Table 5-5 Damage multipliers for each region of the Armor Module**

| Region type | Damage multiplier |
| --- | --- |
| Hit on unreinforced region | *1.5 |
| Hit on reinforced region | *0.5 |
| Hit on default-state region | *1 |

> Note: This damage multiplier acts on the original damage of the projectile, i.e. it is multiplicative with attack and defense Buffs.

> Note: The hit position of each projectile (x, y, hit region type) is sent to the hit side through the Referee System's regular link, and is also sent to the attacking side over the Radar wireless link.

The reinforceable region area is calculated as follows:

- Hit rate eta: eta = (number of own projectiles that hit the opponent) / (number of all projectiles fired by own side)

- Scatter circle radius sigma: all armor plates use a unified Armor Module coordinate system. Each projectile hit produces a set of hit coordinates (x, y). Take the median x0 of the x coordinates and the median y0 of the y coordinates of all hit projectiles; then sigma = the median of the distances from each hit point to the point (x0, y0).

> Note: Armor Module coordinate system: a planar Cartesian coordinate system with the lower-left corner of the Armor Module's detection surface as the origin O, the horizontal rightward direction along the detection surface as the positive x axis, and the vertical upward direction as the positive y axis.

<!-- p.74 -->
- Relative accuracy rho: rho = Lambda_own / Lambda_opponent, where Lambda is the accuracy, Lambda = eta / sigma

- Reinforceable region area A: A = armor plate area * rho^2 / (2 + rho^2)

### 5.3 HP Recovery and Revival Mechanism

Except when abnormally offline or Ejected, Ground Robots can use HP Recovery and Revival.

Apart from the descriptions below, the specific HP Recovery and Revival parameters are additionally affected by Base HP; see "5.6.1 Base and Outpost Mechanism".

#### 5.3.1 HP Recovery Mechanism

**Supply Zone HP Recovery**

A Ground Robot can activate its own Supply Zone Buff Point; activating its own Supply Zone Buff Point grants an HP Recovery Buff of 10% of Max HP per second. 4 minutes after the match starts, when the robot is in the out-of-combat state, activating its own Supply Zone Buff Point grants an HP Recovery Buff of 25% of Max HP per second; when the robot is not in the out-of-combat state, the 25% of Max HP per second HP Recovery Buff immediately becomes invalid.

**Outpost HP Recovery**

When a Ground Robot activates the Outpost Buff Point corresponding to an Outpost position that its own side fully controls, it gains an HP Recovery Buff equal to 50% of its HP Recovery rate in the Supply Zone at that time.

**Remote HP Exchange**

In a round, when a Ground Robot is in the out-of-combat state, it can spend Gold to remotely exchange for HP. 6 seconds after the remote HP exchange is confirmed, the robot gains 60% of its Max HP at that time, but not exceeding Max HP.

> Note:
> - If the robot is Defeated within the 6 seconds after the remote HP exchange is confirmed, the remote HP exchange is void and the Gold is not refunded.
> - How to judge whether a robot is in the Supply Zone: a robot is regarded as being in the Supply Zone when its Field Interaction Module detects a Supply Zone Field Interaction Module card, or, when the robot is within the Supply Zone as set by the rules, the robot's camera Video Transmitter Module recognizes a Supply Zone visual tag. A surviving robot in its own Supply Zone is regarded as activating the Supply Zone Buff Point.
> - The Video Transmitter Module can recognize a visual tag only when the visual tag is in the central region of the Video Transmitter Module image and the Video Transmitter Module has no obvious roll angle.

<!-- p.75 -->
*Figure 5-5 Schematic of the relative position of the robot Video Transmitter Module and the visual tag*

- [1] Visual tag
- [2] Robot Video Transmitter Module range
- [3] Recognizable zone

#### 5.3.2 Revival Mechanism

When a robot is Defeated, its Barrel Heat is reset to 0 and its Buffer Energy is reset to the Buffer Energy limit. A Defeated robot can revive by completing the Revival progress bar, or by immediately reviving through a Gold exchange while the Revival progress bar is in progress.

When reviving by completing the Revival progress bar, the required Revival progress bar depends on the remaining match time when the robot was Defeated and the number of times the robot has cumulatively exchanged for immediate Revival. The formula is as follows:

Required Revival progress bar = 10 + (420 - remaining match time) / 10 + 20 * cumulative number of immediate Revival exchanges

> Note: The remaining match time is in seconds. The fractional part is rounded to the nearest integer.

Example: A robot is Defeated with 120 seconds of match time remaining, and has previously exchanged for immediate Revival 2 times. Its Revival progress bar length this time is 10 + (420 - 120) / 10 + 20 * 2 = 80.

After a robot is Defeated, the Revival progress bar starts immediately. Starting from the moment the robot is Defeated, the progress increases by 1 per second; when the robot is at the Supply Zone Buff Point or its side's Base HP is below 4000, the progress increases by 4 per second.

<!-- p.76 -->
When reviving by completing the Revival progress bar:

- The robot keeps its Level and Experience from before it was Defeated, and is temporarily Invincible for 30 seconds.
- HP is restored to 10% of Max HP.
- The robot enters the "Weakened" state.

Thereafter, after it detects a Field Interaction Module card of an activatable Outpost, Base Buff Point or Supply Zone Buff Point, its "Weakened" state is removed. If the Invincible state it gained from this Revival has accumulated more than 10 seconds, the Invincible state is removed; if the Invincible state it gained from this Revival has not yet accumulated 10 seconds, the Invincible state is removed once it reaches 10 seconds.

When reviving immediately by exchanging Gold:

- The robot keeps its Level and Experience from before it was Defeated, and is temporarily Weakened and Invincible for 3 seconds, after which the Weakened and Invincible states are removed.
- HP is restored to 100% of Max HP.
- The Chassis Power limit is increased by 1x (but not exceeding 200W) for 4 seconds.

Thereafter, after it detects a Field Interaction Module card of an activatable Outpost, Base Buff Point or Supply Zone Buff Point, its "Weakened" state is removed.

A robot in the "Weakened" state:

- Its launching mechanism is locked.
- Activating Buff Points has no effect.

### 5.4 Economy System

#### 5.4.1 Economy System Overview

During the three-minute Setup Period, Ground Robots can all be preloaded with 42mm and 17mm projectiles.

At the start of the match, each side receives a certain amount of initial Gold. As the match progresses, both sides periodically receive Gold; the specific increments are shown in the table below. During the match, additional Gold can also be obtained by assembling Energy Units. Gold can be used to exchange for 17mm/42mm Projectile Allowance, remote HP Recovery and immediate Revival.

**Table 5-6 Overview of periodic Gold increments for robots**

| Match countdown | Red side | Blue side |
| --- | --- | --- |
| 06:59 | 800 (initial) | 800 (initial) |
| 05:59 | 100 | 100 |

<!-- p.77 -->
| Match countdown | Red side | Blue side |
| --- | --- | --- |
| 04:59 | 100 | 100 |
| 03:59 | 100 | 100 |
| 02:59 | 100 | 100 |
| 01:59 | 100 | 100 |
| 00:59 | 300 | 300 |

**Table 5-7 Exchange rules**

| Exchange item | Exchange rate | Exchange limit |
| --- | --- | --- |
| 17mm Projectile Allowance | Remote exchange: 150 Gold / 100 projectiles; non-remote exchange: 10 Gold / 10 projectiles | 1000 projectiles/team |
| 42mm Projectile Allowance | Remote exchange: 150 Gold / 10 projectiles; non-remote exchange: 10 Gold / 1 projectile | 100 projectiles/team |
| HP (remote exchange) | 50 + ROUNDUP((420 - remaining match time) / 60 * 20) Gold / 1 time | Unlimited |
| Immediate Revival | ROUNDUP((420 - remaining match time) / 60) * 80 + robot Level * 20 Gold / 1 robot | Unlimited |

> Note:
> - Durations are in seconds.
> - ROUNDUP means rounding up, to the units digit.
> - The exchange limit for 17mm Projectile Allowance refers to the upper limit of Projectile Allowance obtained through Gold exchange.

#### 5.4.2 Projectile Allowance Mechanism

For every projectile a robot fires, the Projectile Allowance of the corresponding projectile type decreases by 1.

In the following special cases, all armor of the opponent's robots, Outpost and Base will block 42mm projectile damage, until the Heavy Robot returns to the surviving state and its Projectile Allowance is greater than 0:

- 3 seconds after a Heavy Robot changes from surviving to Defeated or abnormally offline.
- A Heavy Robot fires a 42mm projectile when its Projectile Allowance is 0 (overfiring occurs).

<!-- p.78 -->
- After a Defeated Heavy Robot fires its 3rd 42mm projectile.
- The communication packet loss rate between the modular 42mm launching mechanism and the Referee System Main Controller Module is greater than or equal to 5%.

> Note: 17mm projectile damage is not blocked.

**Buff Point Exchange**

When a Ground Robot activates a specific Buff Point (see "5.6.4 Field Buff Mechanism"), the Operator can exchange for Projectile Allowance through the Referee System client; the Sentry Robot can also exchange for Projectile Allowance on its own through the Referee System serial port. The exchangeable types and minimum exchange units are shown in the table below:

**Table 5-8 Minimum exchange unit of Projectile Allowance for different projectile types (for Buff Point exchange)**

| 17mm Projectile Allowance | 42mm Projectile Allowance |
| --- | --- |
| 10 projectiles | 1 projectile |

**Remote Exchange**

If the robot is in the out-of-combat state, the Operator can remotely exchange for Projectile Allowance through the Referee System client, and the Sentry Robot can remotely exchange for Projectile Allowance on its own through the Referee System serial port. The exchangeable types and minimum exchange units are shown in the table below:

**Table 5-9 Minimum exchange unit of Projectile Allowance for different projectile types (for remote exchange)**

| 17mm Projectile Allowance | 42mm Projectile Allowance |
| --- | --- |
| 100 projectiles | 10 projectiles |

After a successful remote exchange, the Projectile Allowance takes effect 6 seconds later.

**Supply Zone Acquisition**

After the match starts, every 1 minute the Sentry Robot can activate its own Supply Zone Buff Point to obtain 100 Projectile Allowance; Projectile Allowance not obtained this way can accumulate.

Example: If a Sentry Robot has never activated its own Supply Zone Buff Point, and activates its own Supply Zone Buff Point with 30 seconds of match time remaining, the Sentry Robot's Projectile Allowance will increase by 600.

#### 5.4.3 Tech Core - Energy Unit Mechanism

During the match, a Heavy Robot assembles the Energy Unit it carries into the Tech Core in exchange for Gold and team Buffs.

For each Tech Core, take the midpoint of the line segment where the front of the base meets the Battlefield ground as the origin O, the direction in which the normal of the base front points toward the Tech Core as the negative X axis, and vertically upward as the positive Z axis, to establish a right-handed Cartesian coordinate system named the assembly coordinate system OXYZ. Take the geometric center of the front surface of the Energy Unit assembly post as the origin E to establish a right-handed Cartesian coordinate system EX'Y'Z', whose X', Y' and Z' axes are all parallel to the X, Y and Z axes with the same positive directions. The unit normal vector of the front surface of the Energy Unit assembly post is e. Based on the Tech Core coordinate system, a spherical coordinate system (r, theta, phi) is established, where theta is the angle between the projection of e on the X'Y' plane and the positive X' axis, theta in [-90, 90]; phi is the angle between e and the positive Z' axis, phi in [0, 90]. Also define alpha as the rotation angle of the Tech Core about the direction of e, with counterclockwise rotation being positive alpha, alpha in [-45, 45].

<!-- p.79 -->
The combination (x, y, z, theta, phi, alpha) of the coordinates (x, y, z) of the center point E of the front surface of the Energy Unit assembly post in the OXYZ coordinate system, the azimuth coordinates (theta, phi) of the unit normal vector e in the Tech Core spherical coordinate system, and the rotation angle alpha of the Tech Core about the direction of e is called the pose of the Tech Core.

*Figure 5-6 Schematic of the Tech Core*

- [1] Tech Core
- [2] Assembly post
- [3] Base

<!-- p.80 -->
(Uncaptioned figures continuing Figure 5-6: assembly coordinate system and Tech Core views.)

- Axis labels shown: O, X, Y, Z (assembly coordinate system); E, X', Y', Z' (Energy Unit coordinate system); P, Q (rotation axes)
- Dimensions (mm): 208, 169, 100, 108, Ø36
- Callouts: [1], [2] (not explained in the page text)

<!-- p.81 -->
*Figure 5-7 Schematic of Tech Core coordinates*

- [1] Q axis
- [2] P axis
- Dimensions (mm): 54, 15

*Figure 5-8 Schematic of Tech Core MARK light dimensions*

- Views labeled A and B
- Dimensions (mm): 80, 20 (front view, both directions); view A: 30, 22, 14, 8; view B: 30, 22

<!-- p.82 -->
*Figure 5-9 Schematic of Tech Core dimensions*

- Dimensions (mm): 259, 307, 98, 74, 55, 155, 30, 55, 162, 97

*Figure 5-10 Schematic of the spherical coordinate system*

- Labels: E, X', Y', Z', e (vector), theta, phi, alpha (rotation about e)

The initial pose of the Tech Core is x=-200, y=200, z=800, theta=0, phi=90, alpha=0. All lengths mentioned above are in mm, and all angles are in degrees.

The Tech Core pose range satisfies the following conditions:

- No part of the Tech Core structure may extend beyond the plane of the base front;
- The Tech Core pose is related to the difficulty level, as follows:

<!-- p.83 -->
**Table 5-10 Relationship between Tech Core pose and difficulty level**

| Difficulty | x | y | z | theta | phi | alpha | Translation requirement | Rotation requirement |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Level 1 | [-100,0] | [100,300] | [500,700] | 0 | 90 | 0 | No translation requirement | No rotation requirement |
| Level 2 | [-100,0] | [100,300] | [500,700] | [-90,90] | [0,90] | [-45,45] | Translate 100mm after insertion | No rotation requirement |
| Level 3 | [-100,0] | [100,300] | [500,700] | [-90,90] | [0,90] | [-45,45] | Translate 100mm after insertion | After the translation is completed, using the Q axis as the rotation axis (see "Figure 5-7 Schematic of Tech Core coordinates"), rotate it to the specified angle with 5° accuracy within a range of at most 90° clockwise and counterclockwise about the Q axis |
| Level 4 | [-100,0] | [100,300] | [500,700] | [-90,90] | [0,90] | [-45,45] | Translate 100mm after insertion | After the translation is completed, using the Q axis as the rotation axis (see "Figure 5-7 Schematic of Tech Core coordinates"), rotate it to the specified angle with 5° accuracy within a range of at most 90° clockwise and counterclockwise about the Q axis |

In each round, the Tech Core pose changes of the red and blue sides are the same at the same difficulty level. The pose value ranges and the translation and rotation requirements of Level 3 and Level 4 are the same, but in Level 4, the other side's Tech Core will temporarily move to this side's position. At this time, the positional relationship between the other side's Tech Core coordinates x'y'z' and this side's Tech Core xyz is: x'=x, y - y' <= 400, z'=z, with a random rotation requirement; the assembling side must complete the assembly of both sides' Tech Cores. After selecting Level 4, the Heavy Robot must complete the assembly within 45 seconds after the Tech Core is in place.

**Level 4 assembly priority**

- If one side is not attempting assembly and the other side selects Level 4, the Tech Core immediately moves to the specified position.
- If one side is attempting assembly at Level 1, 2 or 3, the other side cannot select Level 4.
- If one side is attempting assembly at Level 4, the other side cannot enter the assembly process.

The Heavy Robot can choose the difficulty level on its own, but must complete the assembly of the previous difficulty level before selecting the next one. The selectable difficulty levels are subject to certain conditions, as shown in the table:

**Table 5-11 Heavy Robot assembly difficulty level unlock schedule**

| Match time | Selectable difficulty levels |
| --- | --- |
| At match start | Both sides can select Level 1 only |

<!-- p.84 -->
| Match time | Selectable difficulty levels |
| --- | --- |
| 1 minute after match start | Both sides can select Level 1 and 2 |
| 2 minutes after match start | Both sides can select Level 1, 2 and 3 |
| 3 minutes after match start | Both sides can select Level 1, 2, 3 and 4 |

After a successful assembly, depending on whether this assembly is the first completion, the team gains different rewards, as shown in the table below:

**Table 5-12 Heavy Robot assembly difficulty rewards**

| Completed difficulty | First-completion reward | Non-first-completion reward |
| --- | --- | --- |
| Level 1 | The Heavy Robot is raised to Level 5. Thereafter, this side gains 40 Gold every 10 seconds. | Thereafter, this side gains an additional 4 Gold every 10 seconds. |
| Level 2 | The Heavy Robot is raised to Level 7. Unlock the robot Level cap: before completing this difficulty's assembly task, this side's robot Level cap is Level 5; after completion, the Level cap is raised to Level 7. Thereafter, this side gains an additional 20 Gold every 10 seconds. | Thereafter, this side gains an additional 8 Gold every 10 seconds. |
| Level 3 | The Heavy Robot is raised to Level 10. This side's Ground Robots, Outpost and Base gain a 25% defense Buff, lasting until the end of the match. This side's Heavy Robot unlocks use of the modular 42mm launching mechanism. This side's robot Level cap is raised to Level 10. Thereafter, this side gains an additional 20 Gold every 10 seconds. | Thereafter, this side gains an additional 12 Gold every 10 seconds. |
| Level 4 | This side's Ground Robots, Outpost and Base gain a 50% defense Buff, lasting until the end of the match. Thereafter, this side gains an additional 40 Gold every 10 seconds. | Can only be completed once |

<!-- p.85 -->
> Note: After a robot reaches its Level cap, it no longer gains Experience.

Example: A side successfully completes five assembly tasks in a round, with difficulty levels Level 1, Level 2, Level 3, Level 2, Level 1 in order. The amount of Gold it gains every 10 seconds is 40+20+20+8+4=92.

*Figure 5-11 Schematic of Tech Core light effects*

- [1] First group of lights
- [2] Second group of lights
- [3] Third group of lights

**Table 5-13 Summary of Tech Core light effects**

| State | Light effect |
| --- | --- |
| Match in progress, assembly process not entered | First group of lights all off; second and third groups of lights steady on, showing the team color (red or blue) |
| Match in progress, assembly difficulty selected, robotic arm not yet in position | First group of lights shows a flowing-light effect; second and third groups of lights steady on, showing the team color (red or blue) |
| Match in progress, assembly difficulty selected, robotic arm in position | First group of lights flashes white at 1Hz; second and third groups of lights flash at 1Hz, showing the team color (red or blue) |
| Step 2 completed | First group of lights flashes white at 1Hz; second group of lights flashes at 1Hz, showing the team color (red or blue) |

<!-- p.86 -->
| State | Light effect |
| --- | --- |
| | Third group of lights flashes at 3Hz, showing the team color (red or blue) |
| Step 3 completed | First group of lights flashes white at 1Hz; second and third groups of lights flash at 3Hz, showing the team color (red or blue) |
| Step 4 completed | First group of lights flashes white at 1Hz; second and third groups of lights steady on, showing the team color (red or blue) |
| Step 5 in progress | First group of lights effect as follows: the specified angle position lights up in the team color (red or blue), not flashing; other angle positions light up white matching the Energy Unit's current rotation angle, not flashing. Second and third groups of lights steady on, showing the team color (red or blue) |
| Step 5 completed | In the first group of lights, the specified angle position lights up green, not flashing; second and third groups of lights steady on, showing the team color (red or blue) |
| Assembly confirmed, Energy Unit being retrieved | First group of lights flashes white at 3Hz; second and third groups of lights flash at 3Hz, showing the team color (red or blue) |

To fully carry out Energy Unit assembly, the following steps must be completed:

1. After the Heavy Robot activates the assembly zone Buff Point, the Operator selects the assembly difficulty on the Referee System client.
2. After the Tech Core moves to the corresponding pose (assemblable state), the corresponding light effect appears as a prompt. The Heavy Robot aligns the opening at the bottom of the Energy Unit with the Energy Unit assembly post and inserts it 100mm along the negative x direction. When it reaches the bottom, the corresponding light effect appears as a prompt, and Step 2 is complete, as shown in the figure below.

> Note: The Energy Unit can be inserted only after the Tech Core has moved to the corresponding pose; inserting the Energy Unit early prevents the subsequent assembly process from proceeding normally.

<!-- p.87 -->
*Figure 5-12 Schematic of Step 2*

- [1] 3Hz flashing

3. The Heavy Robot moves the Energy Unit, already fixed on the Energy Unit assembly post, 100mm along the positive z axis. When it reaches 100mm, the corresponding light effect appears as a prompt, and Step 3 is complete, as shown in the figure below.

> Note:
> - The Energy Unit is actually opaque; it is shown here only to illustrate the light effects.
> - In this step, apart from the force necessary to overcome the weight of the Energy Unit, the resistance to movement along the positive z axis is at most 10N.

*Figure 5-13 Schematic of Step 3*

- [1] 3Hz flashing

<!-- p.88 -->
4. The Heavy Robot, using the P axis as the rotation axis, rotates the Energy Unit upward by 90°. When it reaches 90°, the corresponding light effect appears as a prompt, and Step 4 is complete, as shown in the figure below.

*Figure 5-14 Schematic of Step 4*

5. The Heavy Robot, using the Q axis as the rotation axis, rotates the Energy Unit to the specified angle, until the corresponding prompt appears on the client (it appears after staying at the correct position for at least 0.3s and at most 0.5s), and Step 5 is complete, as shown in the figure below.

*Figure 5-15 Schematic of Step 5 Tech Core light effects*

> Note:
> - If, after the Operator presses the "Confirm Assembly" button, the Tech Core does not detect that the Energy Unit has been correctly assembled as required, it will not accept further "Confirm Assembly" command input within the following 1 second.
> - In this step, the Energy Unit assembly post has a torque that naturally returns it to 0°, with a maximum value of 0.3N·m.

<!-- p.89 -->
> Note:
> - For safety reasons, in this step, after staying at the correct position for more than 2s, the rotation mechanism actively holds its position with a torque of about 0.5N·m, at which point the Heavy Robot mechanism can disengage from the Energy Unit without changing its position.

6. The Operator presses the corresponding button to confirm that assembly is complete. If the Tech Core detects that the Energy Unit has been fully inserted and correctly assembled according to the corresponding translation and rotation requirements, the Energy Unit is retrieved and the corresponding reward is given to that side.

- For Level 1, completing steps 1, 2 and 6 is regarded as a successful assembly;
- For Level 2, completing steps 1, 2, 3 and 6 is regarded as a successful assembly;
- For Level 3, completing steps 1, 2, 3, 4, 5 and 6 is regarded as a successful assembly.
- For Level 4, to achieve Energy Unit assembly, the Heavy Robot must not only complete steps 1, 2, 3, 4, 5 and 6, but must also, within 5 seconds after each assembly step other than step 1 and step 4 is completed, also complete that step at the other Tech Core. After both Tech Cores have completed step 6, if the Tech Cores detect that both Energy Units have been fully inserted and correctly assembled according to the corresponding translation and rotation requirements, and the time requirements are met, the Energy Units are retrieved and the corresponding reward is given to that side; otherwise the assembly is regarded as failed.

In addition, the Operator must note the following during assembly:

- After the Operator selects the assembly difficulty, if there is already an Energy Unit in the Tech Core, the assembly difficulty may not be changed, and until the Energy Unit is successfully assembled, the Tech Core pose at the same assembly difficulty remains the same.
- After the Heavy Robot Operator confirms the Energy Unit assembly, the Operator must not perform any further operation on or intervention with the Energy Unit, otherwise the assembly may fail.
- During assembly, the Heavy Robot may remove the Energy Unit. Besides overcoming gravity, removal requires applying an additional force of at most 10N outward along the Energy Unit's rotational symmetry axis. When the Tech Core sensor detects that the Energy Unit has been removed, the assembly process fails immediately.
- During assembly, if the Heavy Robot does not detect the assembly zone interaction module card for 15 consecutive seconds, the current assembly is judged as failed and exited automatically; the Tech Core then immediately performs the Energy Unit retrieval operation.
- The Tech Core has no obstacle detection or active obstacle avoidance while operating. If it is blocked in its motion path, the system will trigger an overload alarm and hover briefly, then attempt to resume motion. If the Heavy Robot's mechanism is damaged by contact or collision with the Tech Core, all losses arising are borne by the participating team itself.
- If the Heavy Robot is Defeated after grasping the Energy Unit, the current assembly is immediately regarded as failed. After the Operator manually cancels the assembly, the Tech Core will perform the Energy Unit retrieval operation.
- If a side's Heavy Robot is Defeated during assembly, only the Defeated robot's 42mm launching mechanism is powered off; the gimbal and chassis remain powered. The Operator must control the Defeated robot to disengage from the Tech Core within 15 seconds. After 15 seconds, the Tech Core will perform the Energy Unit retrieval operation.

<!-- p.90 -->
- When assembling, the Heavy Robot must operate the Energy Unit, not the movable structures or other body structures of the Tech Core.
- Facing the Tech Core, during assembly the Energy Unit can rotate 90° clockwise or counterclockwise about the Q axis.

### 5.5 Experience and Performance System

#### 5.5.1 Experience System

At the start of the match, the Infantry Robot's Level is Level 1 and can be raised by gaining Experience; the experience system does not apply to the other robots. The Heavy Robot's Level is Level 1; for the specific upgrade method, see "Table 5-12 Heavy Robot assembly difficulty rewards".

During a match, a robot can gain Experience in multiple ways, as shown in the table below:

**Table 5-14 Experience gain and settlement mechanism**

| Behavior type | Experience gained |
| --- | --- |
| Firing projectiles | Infantry Robot: gains 1 point of Experience for every projectile fired. |
| Dealing attack damage | Dealing attack damage to a robot: the attacker gains 4 points of Experience for every 1 point of damage dealt. |
| Dealing attack damage | Dealing attack damage to an Outpost Armor Module: the attacker gains 2 points of Experience for every 1 point of damage dealt. |
| Dealing attack damage | Dealing attack damage to a Base Armor Module: the attacker gains 1 point of Experience for every 2 points of damage dealt; when the damage is odd, round up. |
| Dealing attack damage | When a side's robot, Base or Outpost takes attack damage but the Referee System does not detect the specific source of the damage, the damage source cannot gain Experience, or the damage source is a penalty or a friendly robot: if it is projectile damage, the Experience is split equally among all surviving robots of the other side that can normally deal that type of projectile damage and can gain Experience; if it is non-projectile damage, the Experience is split equally among all surviving Infantry Robots of the other side at that time. The average is rounded to the nearest, to one decimal place. Example: A blue Infantry Robot takes 120 points of 17mm projectile damage, but the system does not detect the damage source. At this time the red side has 2 surviving Infantry Robots, so the Experience gained by each Infantry Robot is 4*120/2 = 240. |
| Robot Defeated | In the calculations below, the Sentry Robot is regarded as Level 1. If a killer exists and the killer can gain Experience: when the Level of the destroyed robot is greater than or equal to the Level of the killer, Experience is calculated as follows: Experience gained by the killer = 50 * destroyed robot's Level * (1 + 0.2 * Level difference between the destroyed robot and the killer). |

<!-- p.91 -->
| Behavior Type | Experience Gained |
| --- | --- |
|  | - When the Level of the destroyed robot is lower than the Level of the destroyer, the Level difference between them is treated as 0. Experience is calculated as follows:<br>  Experience gained by the destroyer = 50 * Level of the destroyed robot<br>- If the Referee System does not detect the destroyer, or the destroyer cannot gain Experience:<br>  - For projectile damage, the destroyer's Level is treated as the Level corresponding to the average Experience of all surviving robots on the other side that can normally deal that type of projectile damage, and the Experience is split equally among those robots.<br>  - For non-projectile damage, the Experience is split equally among all surviving Infantry Robots on the other side at that time. The average is rounded to one decimal place.<br>If a robot becomes Defeated for a reason other than its Armor Module being attacked, goes abnormally offline, or the Referee System cannot detect the destroyer, the destroyer is considered not found.<br>Example 1: A Level 2 Infantry Robot destroys an opposing Level 6 Infantry Robot. The Experience gained by the destroyer is 50*6*(1+(6-2)*0.2)=540.<br>Example 2: A Level 9 Infantry Robot of the Red side is Defeated and no destroyer is detected. At this time the Blue side has 2 surviving Infantry Robots with total Experience of 1250 and 4000. The average Experience is 2625, corresponding to Level 5. Each of the 2 Blue Infantry Robots gains Experience of 50 * 9 * (1+(9-5)*0.2)/2 = 405. |
| Activate Small Power Rune | See "5.6.3 Power Rune Mechanism". |
| Activate Large Power Rune | See "5.6.3 Power Rune Mechanism". |
| Terrain Crossing | When a robot obtains the Terrain Crossing Buff (Road), Terrain Crossing Buff (Highland), Terrain Crossing Buff (Tunnel), or the High Point Buff Point for the first time, it gains 300 Experience each time. |
| Dart hits Outpost/Base | See the Dart hit rewards part of "5.7.3 Dart System Special Mechanisms". |

<!-- p.92 -->
**Table 5-15 Infantry Robot Levels and Experience**

| Level | Total Experience Required to Level Up |
| --- | --- |
| 1 | 0 |
| 2 | 550 |
| 3 | 1100 |
| 4 | 1650 |
| 5 | 2200 |
| 6 | 2750 |
| 7 | 3300 |
| 8 | 3850 |
| 9 | 4400 |
| 10 | 5000 |

#### 5.5.2 Performance System

After the three-minute Setup Period begins, the Operator of an Infantry Robot may select the robot's chassis and launching mechanism types. No other robots are subject to the Performance System.

Once the seven-minute Round begins and the chassis and launching mechanism types have been selected, they cannot be changed for the rest of the round. If no chassis or launching mechanism type is selected, then after the seven-minute Round begins the chassis type defaults to "HP Priority" and the launching mechanism type defaults to "Cooling Priority". When a robot levels up, the increase in Max HP is immediately added to the robot's current HP.

**Table 5-16 Heavy Robot Overall Attributes**

| Match Stage | Max HP | Chassis Power Limit | Barrel Heat Limit | Barrel Cooling Rate | Initial Launch Speed Limit (m/s) |
| --- | --- | --- | --- | --- | --- |
| Default at start | 400 | 50 | - | - | - |

<!-- p.93 -->
**Table 5-16 Heavy Robot Overall Attributes (continued)**

| Match Stage | Max HP | Chassis Power Limit | Barrel Heat Limit | Barrel Cooling Rate | Initial Launch Speed Limit (m/s) |
| --- | --- | --- | --- | --- | --- |
| After completing Assembly Level 1 | 450 | 50 | - | - | - |
| After completing Assembly Level 2 | 500 | 50 | - | - | - |
| After completing Assembly Level 3, or after successfully installing the modular 42mm launching mechanism | 600 | 50 | 300 | 100 | 16.5 |

**Table 5-17 Infantry Robot Chassis Attributes**

| Chassis Type | Level | Max HP | Chassis Power Limit (W) |
| --- | --- | --- | --- |
| Power Priority | 1 | 150 | 60 |
| Power Priority | 2 | 175 | 65 |
| Power Priority | 3 | 200 | 70 |
| Power Priority | 4 | 225 | 75 |
| Power Priority | 5 | 250 | 80 |
| Power Priority | 6 | 275 | 85 |
| Power Priority | 7 | 300 | 90 |
| Power Priority | 8 | 325 | 95 |
| Power Priority | 9 | 350 | 100 |
| Power Priority | 10 | 400 | 100 |
| HP Priority | 1 | 200 | 45 |
| HP Priority | 2 | 225 | 50 |

<!-- p.94 -->
**Table 5-17 Infantry Robot Chassis Attributes (continued)**

| Chassis Type | Level | Max HP | Chassis Power Limit (W) |
| --- | --- | --- | --- |
| HP Priority | 3 | 250 | 55 |
| HP Priority | 4 | 275 | 60 |
| HP Priority | 5 | 300 | 65 |
| HP Priority | 6 | 325 | 70 |
| HP Priority | 7 | 350 | 75 |
| HP Priority | 8 | 375 | 80 |
| HP Priority | 9 | 400 | 90 |
| HP Priority | 10 | 400 | 100 |

**Table 5-18 Infantry Robot 17mm Launching Mechanism Attributes**

| Launching Mechanism Type | Level | Barrel Heat Limit | Barrel Cooling Rate (per second) |
| --- | --- | --- | --- |
| Burst Priority | 1 | 170 | 5 |
| Burst Priority | 2 | 180 | 7 |
| Burst Priority | 3 | 190 | 9 |
| Burst Priority | 4 | 200 | 11 |
| Burst Priority | 5 | 210 | 12 |
| Burst Priority | 6 | 220 | 13 |
| Burst Priority | 7 | 230 | 14 |
| Burst Priority | 8 | 240 | 16 |
| Burst Priority | 9 | 250 | 18 |
| Burst Priority | 10 | 260 | 20 |

<!-- p.95 -->
**Table 5-18 Infantry Robot 17mm Launching Mechanism Attributes (continued)**

| Launching Mechanism Type | Level | Barrel Heat Limit | Barrel Cooling Rate (per second) |
| --- | --- | --- | --- |
| Cooling Priority | 1 | 40 | 12 |
| Cooling Priority | 2 | 48 | 14 |
| Cooling Priority | 3 | 56 | 16 |
| Cooling Priority | 4 | 64 | 18 |
| Cooling Priority | 5 | 72 | 20 |
| Cooling Priority | 6 | 80 | 22 |
| Cooling Priority | 7 | 88 | 24 |
| Cooling Priority | 8 | 96 | 26 |
| Cooling Priority | 9 | 104 | 28 |
| Cooling Priority | 10 | 120 | 30 |

### 5.6 Field-Related Mechanisms

#### 5.6.1 Base and Outpost Mechanisms

The Base has 10000 HP and the Outpost has 1000 HP.

When a side's Outpost Position is fully controlled by that side (likewise for the Blue side), that side's Base gains a 100% defense Buff; otherwise the Base loses this 100% defense Buff.

When an Outpost Position changes from full control by one side to full control by the other side through the Outpost being destroyed, the Outpost is "rebuilt" as an Outpost owned by the other side, returns to the alive state, and has 500 HP.

> Note: For the definitions and detailed mechanisms of full control and temporary control, see "5.6.2 Battlefield Control Mechanism". After a side fully controls an Outpost Position, it can activate the Outpost Buff Point corresponding to that Outpost Position; see "5.6.4.6 Outpost Buff Point Mechanism".

As a side's Base HP decreases, that side's logistics capabilities are reduced to a certain extent, as follows:

Define ∆ = the Base HP lost by the side's own Base, and the logistics coefficient λ = 1 − ∆/20000. The original parameter of each item in the table below is denoted by x:

<!-- p.96 -->
**Table 5-19 Logistics Capability Parameter Calculation Logic**

| Logistics Capability Item | Relationship Between the Item's Parameter and the Logistics Coefficient |
| --- | --- |
| Progress bar required for Revival | x/λ |
| Supply Zone HP Recovery rate | x * λ |
| HP Recovery ratio of remote exchange for HP | x * λ |
| Robot interaction data bandwidth | x * λ |
| Video transmission resolution | x * λ^2 (x is 1920*1080, the original video transmission resolution. After Base HP decreases, the video transmission picture reduces its clarity by area-average downsampling followed by bilinear upscaling. The clarity of the original Operator-side UI is not affected.) |

> Note: For the definition of robot interaction data in multi-robot communication, see the communication protocol.

> Note: The video transmission resolution includes the video transmission pictures of both the official Operator-side client and the Custom Terminal.

*Figure 5-16 Illustration of video transmission clarity at λ=1, 0.75, 0.5*

- Row labels: 6 px, 3 px, 1 px (cell side length)
- Axis label: "Cell side length / logistics coefficient"; columns: λ=1, λ=0.75, λ=0.5

The Outpost's middle armor can rotate; for its initial position, refer to "Figure 4-34 Outpost Illustration". After the Round begins, the middle armor starts rotating, reaches a speed of 0.8π rad/s within 5 s of rotation, and then keeps rotating at a constant speed in a random direction. In each round, the rotation direction of the Outposts of the Red and Blue sides is the same and stays fixed.

A side's Outpost armor stops rotating when any of the following conditions is met:

- That side's Outpost is destroyed for the first time.
- The opposing Base armor is deployed.

<!-- p.97 -->
- 3 minutes after the Round begins.

An Outpost armor that has stopped rotating will not rotate again in that round.

> Note: When both Outposts stop rotating at the same time, the time at which their middle armors reach the initial position may differ slightly.

The Dart guide lights of the Outpost and Base stay constantly on during the seven-minute Round.

#### 5.6.2 Battlefield Control Mechanism

During the match, the two sides must contest Positions to demonstrate and improve their control of the Battlefield, thereby raising their control degree. Each side has two Positions: the Outpost Position and the Base Position. The control state of a Position is divided into temporary control and full control. The relationship between Positions and control is as follows:

**Table 5-20 Relationship Between Positions and Control**

| Position | Composition | Supports Temporary Control | Supports Full Control |
| --- | --- | --- | --- |
| Outpost Position | Outpost Buff Point + Central Highland Buff Point | Yes | Yes |
| Base Position | Base Buff Point + Fortress Buff Point | Yes | Only the initial owner |

At the start of the match, both sides fully control their own Base Position and Outpost Position. After the match begins, the control relationship of Positions can be changed in the following ways:

**Table 5-21 Position Control State Transition Mechanisms**

| Transition Result | Transition Method | Additional Mechanisms |
| --- | --- | --- |
| Convert a Position fully controlled by the opponent into a Position temporarily controlled by the own side | The own side continuously activates any Buff Point composing that Position for 5s | If continuous activation stops before reaching 5s, the occupation progress regresses evenly (at the same rate as it increased) instead of resetting to zero.<br>When both sides activate Buff Points in the same Position, the occupation progress is paused until only one side's robots still have activated Buff Points in that Position. |
| Convert a Position temporarily controlled by the opponent into a Position fully controlled by the own side | The opposing robots do not activate any Buff Point composing the Position for 5s continuously | If continuous activation stops before reaching 5s, the occupation progress regresses evenly (at the same rate as it increased) instead of resetting to zero.<br>When both sides activate Buff Points in the same Position, the occupation progress is paused until only one side's robots still have activated Buff Points in that Position. |
| Convert an Outpost Position fully controlled by the opponent into an Outpost Position temporarily controlled by the opponent | Destroy the Outpost on the Position | If continuous activation stops before reaching 5s, the occupation progress regresses evenly (at the same rate as it increased) instead of resetting to zero.<br>When both sides activate Buff Points in the same Position, the occupation progress is paused until only one side's robots still have activated Buff Points in that Position. |
| Convert an Outpost Position temporarily controlled by the own side into an Outpost Position fully controlled by the own side | Destroy the Outpost on the Position | If continuous activation stops before reaching 5s, the occupation progress regresses evenly (at the same rate as it increased) instead of resetting to zero.<br>When both sides activate Buff Points in the same Position, the occupation progress is paused until only one side's robots still have activated Buff Points in that Position. |

<!-- p.98 -->
When a side controls all 2 Outpost Positions, that side's control degree increases by 1 per second.

When a side controls all 2 Base Positions, that side's control degree increases by 3 per second.

#### 5.6.3 Power Rune Mechanism

Robots can activate the Power Rune by hitting it with projectiles. Both sides can hit the Power Rune at the same time. After the Red side's Power Rune is activated, it provides Buffs only to the Red side; the same applies to the Blue side.

The Power Rune rotates continuously during the match, but the rotation strategy changes with its state:

The Power Runes of the Red and Blue sides rotate coaxially: when the Red side's Power Rune rotates clockwise, the Blue side's Power Rune rotates counterclockwise accordingly (the rotation direction is determined as seen when facing that side's Power Rune). Before each round starts, the Power Rune rotation direction is random. During that round, the Power Rune rotation direction stays the same.

- The rotation speed of the Small Power Rune is fixed at 1/3 π rad/s.
- The rotation speed of a Large Power Rune that is not in the activating state is fixed at 1/3 π rad/s.
- The rotation speed of a Large Power Rune in the activating state varies periodically as a trigonometric function. The target speed function is: spd = a * sin(ω * t) + b, where spd is in rad/s and t is in s, a ranges from 0.780 to 1.045, ω ranges from 1.884 to 2.000, and b always satisfies b = 2.090 - a. Each time the Large Power Rune enters the activatable state, all parameters are reset: t is reset to 0, and a and ω are reset to arbitrary values within their ranges. The time error between the actual rotation speed of the Power Rune and the target speed function is within 500ms.

After a side activates the Power Rune, until its duration ends, all surviving robots of that side gain certain Buffs, and that side's Power Rune enters the activated state. After the Power Rune Buff effect ends, the Power Rune enters the inactive state. Both sides can hold Power Rune Buffs at the same time.

By time, the Power Rune is divided into two stages: the Small Power Rune and the Large Power Rune. From the start of the match to 3 minutes into the match is the Small Power Rune stage; after 3 minutes into the match is the Large Power Rune stage.

- **Small Power Rune:** The Small Power Rune states of the two sides are independent of each other. At the start of the match and at 1 minute 30 seconds into the match, each side gets 1 chance to activate the Small Power Rune, and these chances can accumulate. An Infantry Robot Operator (through the Referee System Operator-side client) or a Sentry Robot (through the Referee System serial port) can trigger an inactive Small Power Rune to enter the activating state. If the Small Power Rune has still not been activated 20 seconds after entering the activating state, it returns to the inactive state. After a side's robot successfully activates the Small Power Rune, all robots, the Outpost and the Base of that side gain a 25% defense Buff lasting 45 seconds. During the Small Power Rune Buff, all Infantry Robots gain an additional 100% of the original Experience whenever they gain Experience; a side can gain at most 1200 additional Experience in this way during one Small Power Rune Buff.
- **Large Power Rune:** The Large Power Rune states of the two sides are independent of each other. At 3 minutes, 4 minutes 15 seconds, and 5 minutes 30 seconds into the match, each side gets 1 chance to activate the Large Power Rune, and these chances can accumulate. An Infantry Robot Operator (through the Referee System Operator-side client) or a Sentry Robot (through the Referee System serial port) can trigger an inactive Large Power Rune to enter the activating state. If the Large Power Rune has still not been activated 20 seconds after entering the activating state, it returns to the inactive state. Each Armor Module of the Large Power Rune is divided into rings 1 to 10. Once a side's Large Power Rune is activated,

<!-- p.99 -->
the system provides all robots of that side with attack, defense and barrel cooling Buffs of differing duration and effect according to the average ring number hit and the number of activated light arms, and provides the corresponding defense Buff to that side's Outpost and Base; see "Table 5-22 Average Ring Number and Corresponding Buffs". At the same time, when the Large Power Rune is activated, 750 Experience is split equally among all surviving Infantry Robots of the activating side.

*Figure 5-17 Illustration of Power Rune hit zones*

- Ring numbers labeled: 2, 4, 6, 8, 10 (from outside in)
- Ring diameters: Ø300, Ø270, Ø240, Ø210, Ø180, Ø150, Ø120, Ø90, Ø60, Ø30

> Note: The detection accuracy of the Power Rune Armor Module for the projectile hit position is 1mm in the radial direction.

**Table 5-22 Average Ring Number and Corresponding Buffs**

| Average Ring Number Range | Attack Buff | Defense Buff | Barrel Cooling Buff |
| --- | --- | --- | --- |
| [1,3] | 150% | 25% | None |
| (3,7] | 150% | 25% | 2x |
| (7,8] | 200% | 25% | 2x |
| (8,9] | 200% | 25% | 3x |
| (9,10] | 300% | 50% | 5x |

**Table 5-23 Number of Activated Light Arms and Corresponding Buff Duration**

| Number of Activated Light Arms | Buff Duration (s) |
| --- | --- |
| 5 | 30 |

<!-- p.100 -->
**Table 5-23 Number of Activated Light Arms and Corresponding Buff Duration (continued)**

| Number of Activated Light Arms | Buff Duration (s) |
| --- | --- |
| 6 | 35 |
| 7 | 40 |
| 8 | 45 |
| 9 | 50 |
| 10 | 60 |

Each time a side successfully activates its own Large Power Rune, the effective hit zone of that side's Power Rune shrinks, and only Armor Modules with some of the ring numbers can continue to detect projectile hits. The relationship is shown in the table below:

**Table 5-24 Relationship Between Large Power Rune Activation Count and Effective Detected Rings**

| Cumulative Activation Count of the Side's Large Power Rune | Rings That Can Still Be Detected |
| --- | --- |
| 1 time | Rings 4, 5, 6, 7, 8, 9, 10 |
| 2 times | Rings 7, 8, 9, 10 |

##### 5.6.3.1 Power Rune States

The Power Rune has 4 states: inactive, activating, activated and activation failed.

**1. Inactive state**

When the Power Rune enters the inactive state, its appearance is as shown below:

*Figure 5-18 Illustration of the Power Rune inactive state*

<!-- p.101 -->
**2. Activating state**

**Small Power Rune**

When the Small Power Rune enters the activating state, the Power Rune randomly lights any 1 of the 5 Armor Modules. The lit Armor Module shows a special light effect, and the center axis of the light arm corresponding to that Armor Module shows an arrow-shaped flowing light effect. At this time, if a projectile hits any lit Armor Module within 2.5 seconds, that light arm is fully lit and shows the corresponding light effect; at the same time, the Power Rune randomly lights any one of the remaining 4 Armor Modules, and so on.

*Figure 5-19 Illustration of the Small Power Rune activating state*

**Large Power Rune**

When the Large Power Rune enters the activating state, the Power Rune randomly lights any 2 of the 5 Armor Modules. The lit Armor Modules show a special light effect, and the center axis of the light arm corresponding to each Armor Module shows an arrow-shaped flowing light effect. At this time, if a projectile hits the detectable zone of any lit Armor Module within 2.5 seconds, the corresponding light arm changes its light effect; within the following 1 second, the robot can hit the other lit Armor Module. Whether or not it succeeds, the Power Rune re-randomly lights any 2 of the 5 Armor Modules, and so on. The light effect in the middle of the Large Power Rune's light arms indicates the activation progress. For example, if the first group has been activated and the second group is being activated, the middle light arm lights up about 1/5; afterwards, if the second group is successfully activated (hitting the first lit Armor of the second group counts as successfully activating the second group, whether or not the second Armor of the second group is hit; the light effect changes when activation of the third group begins), the middle light arm lights up about 2/5.

The specific light effects are shown in the figure below:

*Figure 5-20 Illustration of the Large Power Rune activating state*

<!-- p.102 -->
*Figure 5-21 Illustration of the Power Rune activatable indicator*

- Dimensions: 35, 7°, 100, 90°, 20; Ø70, Ø150, Ø270, Ø300

> Note: To ensure timing alignment, during the activation process, the light arms and Armor Module light effects go dark for up to 200ms before the Power Rune re-randomly lights the next group of Armor Modules.

**3. Activated state**

If all 5 groups of light arms are activated, the Power Rune is in the activated state, as shown below:

*Figure 5-22 Illustration of the Power Rune activated state*

**4. Activation failed**

During activation, if any of the following occurs, this activation fails and the Power Rune resets to the activating state:

- Failing to hit the lit Armor Module within 2.5 seconds.
- Hitting an Armor Module that was not randomly lit.

<!-- p.103 -->
#### 5.6.4 Field Buff Mechanisms

##### 5.6.4.1 Field Buff Point Overview

The distribution of all Buff Points on the field is shown in the figure below. Field Interaction Module cards are laid at the Battlefield Buff Points. The Field Interaction Module cards may have dead zones, and participating teams must adjust and adapt on their own. Field Interaction Module detection may be delayed; the deactivation of a robot's activated state has a 2-second delay in all cases.

*Figure 5-23 Illustration of Battlefield Buff Point distribution*

- [1] Supply Zone Buff Point
- [2] Terrain Crossing Buff Point (Road)
- [3] Terrain Crossing Buff Point (Tunnel)
- [4] Terrain Crossing Buff Point (Tunnel)
- [5] High Point Buff Point
- [6] Base Buff Point
- [7] Fortress Buff Point
- [8] Terrain Crossing Buff Point (Highland)
- [9] Outpost Buff Point
- [10] Terrain Crossing Buff Point (Tunnel)
- [11] Assembly Zone Buff Point
- [12] Central Highland Buff Point and Terrain Crossing Buff Point (Highland)

<!-- p.104 -->
*Figure 5-24 Illustration of Field Interaction Module card installation*

- [1] Field Interaction Module card mounting position
- Detail A dimensions: 92, 28, 28, 112, 70

Buffs can be divided into different types according to their effects; see the table below:

**Table 5-25 Buff Effect Types**

| Type | Description |
| --- | --- |
| Attack Buff | Increases the damage dealt by projectile attacks or Aerial Robot impacts; the damage becomes: original damage * attack Buff |
| Defense Buff | Changes the damage taken from projectile attacks, collisions and Aerial Robot impacts, so that the attack damage taken by robots, the Base and the Outpost becomes: original damage * (1 - defense Buff). A negative defense Buff is called "vulnerability". Note: Defense Buffs do not apply to HP deductions caused by rule-violation penalties, Referee System module offline, Darts, etc. |
| Barrel Cooling Buff | Increases the Barrel Cooling Rate. |
| Buffer Energy Buff | Gains extra Chassis Power Buffer Energy. |
| HP Recovery Buff | The robot recovers a certain amount of HP per second until reaching Max HP. |
| Chassis Power Buff | Increases the robot's Chassis Power limit. |

> Note: For original damage, see "Table 5-2 HP Deduction Mechanism for Attack Damage or Collisions" and "5.2 Adaptive Armor Mechanism".

By Buff source, Buffs can be divided into three types: field persistent Buffs, field temporary Buffs and non-field temporary Buffs. Different Buffs behave differently when the robot state changes; see the table below:

<!-- p.105 -->
**Table 5-26 Buff Source Types and Behavior**

| Type | Buff Characteristics | Included Buff Sources | Behavior | Notes |
| --- | --- | --- | --- | --- |
| Field persistent Buff | A Buff type that requires the robot to continuously activate the Buff Point and has no concept of duration | - Supply Zone Buff<br>- High Point Buff<br>- Base Buff<br>- Fortress Buff<br>- Outpost Buff<br>- Assembly Zone Buff<br>- Central Highland Buff | Removed immediately once the robot no longer activates the corresponding Buff Point | - |
| Field temporary Buff | A Buff type that does not require the robot to continuously activate a Buff Point and can be triggered once certain conditions are met; it has a concept of duration | Terrain Crossing Buff | Removed when the robot is Defeated or the duration ends | - |
| Non-field temporary Buff | A Buff type not obtained through Field Interaction Module cards | - Power Rune Buff<br>- Buffs from special robot mechanisms (Sentry posture Buff, Heavy Robot defense Buff, Radar vulnerability)<br>- Defense Buff from Assembly Level | Not removed when the robot is Defeated | As long as the Buff source exists, all robots/field props to which the Buff applies have the Buff. For example, an Outpost rebuilt due to a control change immediately gains the owner's current Power Rune Buff |

Example 1: If a Red robot has a 200% attack Buff, a Blue robot has a 25% defense Buff, and the Blue robot's marking progress by the opposing Radar robot is greater than 100, then when the Red side fires one 42mm projectile that hits the Blue robot, the damage taken by the Blue robot is: 200*200%*(1-25%+15%)=360.

<!-- p.106 -->
Example 2: If a Red robot has a 200% attack Buff, and the Blue Heavy Robot's marking progress by the opposing Radar is greater than 100, then when the Red side fires one 42mm projectile that hits the Blue Heavy Robot, the damage taken by the Blue Heavy Robot is: 200*200%*(1+15%)=460.

When a robot obtains more than one Buff of the same type, the maximum Buff effect is taken. This includes attack, defense, vulnerability, HP Recovery and Barrel Cooling Buffs.

Example 1: A Red Infantry Robot obtains a 25% defense Buff by activating the Large Power Rune. If it then also activates its own Base Buff Point, it has a 50% defense Buff. If it afterwards obtains 15% vulnerability, it has a 35% defense Buff.

Example 2: A Blue Infantry Robot obtains a 25% defense Buff by activating the Large Power Rune. If it then activates the opposing Fortress Buff Point, it has 75% vulnerability. If it afterwards obtains another 15% vulnerability, it still has 75% vulnerability.

If the final damage value or HP Recovery value after Buff calculation is not an integer, it is rounded to the nearest integer.

##### 5.6.4.2 Base Buff Point Mechanism

The Base Buff Point can be activated by Ground Robots of both sides. Multiple robots of the same side can activate the Base Buff Point at the same time.

During the seven-minute Round, a robot that activates its own Base Buff Point gains a 50% defense Buff, can exchange for Projectile Allowance, and has the "Weakened" state removed. For the "Weakened" state, see "5.3.2 Revival Mechanism".

##### 5.6.4.3 High Point Buff Point Mechanism

All robots of a side can activate that side's High Point Buff Point. Multiple robots of the same side can activate the High Point Buff Point at the same time.

If a side's High Point Buff Point is activated by that side's robot, the robot that activated the High Point gains a 50% defense Buff and can exchange for Projectile Allowance non-remotely.

##### 5.6.4.4 Central Highland Buff Point Mechanism

Heavy Robots, Infantry Robots and Sentry Robots can all activate the Central Highland Buff Point. Activation of unconnected Central Highland Buff Points is independent of each other, and the laying range of their Field Interaction Module cards is consistent with the higher part of the two Terrain Crossing Buff Points (Highland). Multiple robots of the same side can activate the Central Highland Buff Point at the same time. If a robot of one side activates the Central Highland Buff Point, a robot of the other side cannot activate it at the same time.

A robot that activates the Central Highland Buff Point gains a 25% defense Buff.

##### 5.6.4.5 Terrain Crossing Buff Point Mechanism

The Central Highland has 2 Terrain Crossing Buff Points (Highland) each, and each side's Road Zone has 2 Terrain Crossing Buff Points (Road) and 9 Terrain Crossing Buff Points (Tunnel).

Ground Robots can all activate Terrain Crossing Buff Points. Multiple robots of the same side, and robots of both sides, can activate Terrain Crossing Buff Points at the same time.

The same robot must, within X seconds, detect the Field Interaction Module cards of every Terrain Crossing Buff Point of the same type on one side's field, and must not detect any other Field Interaction Module card along the way. For the Terrain Crossing Buff (Road/Highland), the lower Buff Point must be detected first and then the higher Buff Point, in order to trigger the Terrain Crossing Buff.

<!-- p.107 -->
The Terrain Crossing Buff Point (Tunnel) has two mutually independent Buff forms, which differ according to the type and order of Field Interaction Module cards detected when passing through the tunnel. X is 3 for the Terrain Crossing Buff Point (Road) and the Terrain Crossing Buff Point (Tunnel), and X is 5 for the Terrain Crossing Buff Point (Highland). The specific Buffs are as follows:

**Terrain Crossing Buff (Highland)**

- 25% defense Buff, lasting 30 seconds.

**Terrain Crossing Buff (Road)**

- 25% defense Buff, lasting 5 seconds.
- The same robot cannot obtain the Terrain Crossing Buff (Road) again within 15 seconds after obtaining it.

**The two types of Terrain Crossing Buff (Tunnel):**

**Table 5-27 Tunnel Buff Trigger Logic and Effects**

| Buff Type | Field Interaction Module Card Detection Type and Order | Buff Effect |
| --- | --- | --- |
| Terrain Crossing Buff (Tunnel Crossover) | Only the Field Interaction Module cards at one end and then the other end of the tunnel are detected, in order | 25% defense Buff, lasting 30 seconds |
| Terrain Crossing Buff (Tunnel Passthrough) | The Field Interaction Module cards at one end, the inside, and then the other end of the tunnel are detected, in order | 1.5x Barrel Cooling Buff, lasting 120 seconds |

When a robot holding a Terrain Crossing Buff (Tunnel Crossover, Tunnel Passthrough, Highland or Road) obtains a different Terrain Crossing Buff, the robot gains a 50% defense Buff. At the same time, the remaining duration of that defense Buff is updated to the larger of the remaining time of the Buff already held and the initial duration of the newly obtained Buff.

After a robot is Defeated, the Terrain Crossing Buffs it has obtained are cleared.

##### 5.6.4.6 Outpost Buff Point Mechanism

All Ground Robots can activate the Outpost Buff Point, and multiple robots of both sides can activate the Outpost Buff Point at the same time.

In an Outpost Position fully controlled by the own side, own-side robots that activate the Outpost Buff Point can exchange for Projectile Allowance, HP Recovery, and removal of "Weakened" and the corresponding Invincible state. See "5.3 HP Recovery and Revival Mechanisms".

##### 5.6.4.7 Assembly Zone Buff Point Mechanism

The Assembly Zone Buff Point can only be activated by the own side's Heavy Robot.

A Heavy Robot that activates the Assembly Zone Buff Point and is in the Assembly process is Invincible and has its launching mechanism powered off. Invincibility lasts at most 45 seconds cumulatively (if the Buff Point is activated again after leaving the Buff zone, the time is not reset). Each time the highest successfully completed Assembly Level increases, this cumulative timer is refreshed to 0 seconds.

<!-- p.108 -->
##### 5.6.4.8 Supply Zone Buff Point Mechanism

Ground Robots can all activate their own side's Supply Zone Buff Point. Multiple robots of the same side can activate the Supply Zone Buff Point at the same time.

A robot that activates its own Supply Zone Buff Point can exchange for Projectile Allowance non-remotely, and also gains faster Revival progress or an HP Recovery Buff; for the specific implementation and values, see "5.3 HP Recovery and Revival Mechanisms".

After the Supply Zone Buff Point is activated, the Heavy Robot is Invincible.

##### 5.6.4.9 Fortress Buff Point Mechanism

The Fortress Buff Point can be activated by Heavy Robots, Infantry Robots and Sentry Robots. Both sides can activate it at the same time. At any one time it can be activated by only one own-side robot, and only the robot that activated it first gains the Buff, but it can be activated by multiple opposing robots at the same time.

The Fortress Buff Point takes effect when the own side's Outpost Position is not controlled by the own side.

**Own-side activation effect**

Define ∆ as the difference between the own Base's Max HP and the lowest HP value reached in this round.

An own-side robot that activates the Fortress Buff Point gains a 50% defense Buff and a Barrel Cooling Buff of value w, where w is related to ∆ as w = ∆/80 (rounded down), with an upper limit of 75 for w. This Barrel Cooling Buff takes the highest effect when combined with Barrel Cooling Buffs from other sources.

**Example:**

A robot with a Barrel Cooling Rate of 40/s simultaneously obtains a Barrel Cooling Buff of value 75 from the Fortress Buff Point and a 5x Barrel Cooling Buff. Since 40*5 > 40+75, the robot's actual Barrel Cooling Rate is 200/s.

After a robot activates the Fortress, the Fortress Buff zone provides the robot with a "Reserve Projectile Allowance" (independent of the Projectile Allowance the robot itself has), with an upper limit of N. When a robot that has activated the Fortress Buff zone fires projectiles, it consumes the "Reserve Projectile Allowance" first, and consumes its own Projectile Allowance only after the "Reserve Projectile Allowance" is exhausted. Each 17mm projectile fired by an Infantry Robot or Sentry Robot consumes 1 Reserve Projectile Allowance; each 42mm projectile fired by a Heavy Robot consumes 10 Reserve Projectile Allowance.

N = 100 + ∆/15 (rounded down), with N at most 500.

**Opposing activation effect**

After 3 minutes of the match have elapsed and the opposing Outpost Position is controlled by the own side, Ground Robots can activate the opposing Fortress Buff Point.

A robot that is activating the opposing Fortress Buff Point gains 100% vulnerability. When a single activation by a robot accumulates 10 seconds, the opposing Base armor is deployed. The timer for activating the opposing Fortress Buff Point can be retained for 3 seconds after the robot dies or the activation state lapses, and the timer is paused during the retention period. After the opposing Base armor is deployed, the robot activating the opposing Fortress Buff Point no longer gains vulnerability.

<!-- p.109 -->
### 5.7 Robot Special Mechanisms

#### 5.7.1 Heavy Robot Special Mechanisms

During the first 3 minutes of the match, and before the modular 42mm launching mechanism has been successfully installed, the Heavy Robot has a 50% defense Buff.

**Installing the modular 42mm launching mechanism**

After meeting either of the following conditions, the Heavy Robot unlocks the right to use the launching mechanism. It may go to the Workbench in the Supply Zone to install the modular 42mm launching mechanism. After it successfully fires one 42mm projectile that is detected by the Referee System, the Heavy Robot is considered to have "successfully installed the modular 42mm launching mechanism".

The Heavy Robot can perform the following operations, but only at the Workbench:

Split into sub-robots or multiple subsystems connected by flexible cables, or merge back from such a state.

Install or remove the modular 42mm launching mechanism.

> Note:
> - This 42mm projectile does not count toward Barrel Heat, Initial Launch Speed, or damage.
> - Before the right to use the modular 42mm launching mechanism is unlocked, the Heavy Robot's launching mechanism is not powered on.

Unlock paths for the right to use the modular 42mm launching mechanism:

- Complete Assembly Level 3.
- After (300 − M/50 − 2N/3) seconds of the match have elapsed, where M is the highest value, within the round, of the difference between the opponent's Base HP and one's own Base HP, and N is the highest value, within the round, of the difference between the opponent's control degree and one's own control degree.

The attributes of the Heavy Robot differ by match stage; see "Table 5-16 Heavy Robot Complete Machine Attributes".

#### 5.7.2 Sentry Robot Special Mechanisms

After the three-minute Setup Period begins and before the 15-Second Referee System Initialization Period, the Commander may choose the control mode of the corresponding Sentry Robot: automatic control or semi-automatic control. If no control mode is chosen within the specified time, the Sentry Robot defaults to automatic control after the seven-minute Round begins. The Sentry Robot can autonomously exchange for Projectile Allowance, remotely exchange for Projectile Allowance, remotely exchange for HP, confirm Revival, exchange for immediate Revival, and switch posture, by sending messages to the Referee System server.

In addition, the Commander can intervene in the Sentry Robot's actions through the relevant commands of the Referee System Client. The specific commands are:

- Forward mini-map markers
- Purchase Projectile Allowance at the Supply Zone, the Base Buff Point, and the Outpost Buff Point
- Confirm Revival
- Remotely exchange for Projectile Allowance

<!-- p.110 -->
- Remotely exchange for HP
- Remotely exchange for immediate Revival
- Switch posture

For a semi-automatic Sentry, the above operations do not consume Gold; for an automatic Sentry, each time the Commander performs one of the above operations, it costs 50 Gold.

The Sentry Robot has a "posture" system, which strengthens some abilities at the expense of others. The Sentry Robot is in the movement posture by default at the start of a round. Posture switching has a 5-second cooldown. In each round, if the Sentry Robot spends more than 3 minutes cumulatively in one posture, the effect of that posture degrades. The Sentry can enter an enhanced posture, in which its abilities are further strengthened, but each enhanced posture can be entered for at most 15s cumulatively. The timers of the different enhanced postures are independent of each other, and once the time is exceeded that enhanced posture can no longer be entered. Details are given in the table below:

**Table 5-28 Sentry Robot Posture Effects**

| Posture | Enhanced posture effect | Default effect | Degraded effect |
| --- | --- | --- | --- |
| Attack posture | Current heat is always 0, firing projectiles does not add heat, the Chassis Power upper limit is reduced to 1/2 of the original, and gains 25% vulnerability | Gains a 3x heat cooling Buff, the Chassis Power upper limit is reduced to 1/2 of the original, and gains 25% vulnerability | Gains a 2x heat cooling Buff, the Chassis Power upper limit is reduced to 1/2 of the original, and gains 25% vulnerability |
| Defense posture | Gains a 99% defense Buff, the Chassis Power upper limit is reduced to 1/2 of the original, and the heat cooling rate is reduced to 1/3 of the original | Gains a 50% defense Buff, the Chassis Power upper limit is reduced to 1/2 of the original, and the heat cooling rate is reduced to 1/3 of the original | Gains a 25% defense Buff, the Chassis Power upper limit is reduced to 1/2 of the original, and the heat cooling rate is reduced to 1/3 of the original |
| Movement posture | The Chassis Power upper limit is raised to 200W, gains 25% vulnerability, and the heat cooling rate is reduced to 1/3 of the original | Gains a 1.5x Chassis Power Buff, gains 25% vulnerability, and the heat cooling rate is reduced to 1/3 of the original | Gains a 1.2x Chassis Power Buff, gains 25% vulnerability, and the heat cooling rate is reduced to 1/3 of the original |

> Note:
> - All the above calculations take integer values.
> - When the effect is a reduction of heat cooling or Chassis Power, it is applied multiplicatively on top of the values for which the Sentry Robot has already completed the heat cooling Buff and Chassis Power Buff calculations.
>
> Example 1: An automatic Sentry in the default defense posture has a base heat cooling rate of 30 per second. It then obtains a 3x Barrel Heat cooling Buff by activating the large Power Rune, and a Barrel Heat cooling Buff of 75 per second by activating the Fortress Buff Point. The larger of the two is taken first (that is, +75 per second), so the automatic Sentry's heat cooling rate is 30+75=105,

<!-- p.111 -->
> then the cooling rate attenuation coefficient corresponding to the defense posture (1/3) is applied multiplicatively, giving the automatic Sentry's actual heat cooling rate of 105 * 1/3 = 35.
>
> Example 2: A Sentry Robot has already spent a cumulative 2 minutes 50 seconds in the movement posture in the current round and has never entered another posture. If it then switches to the enhanced movement posture, after 15 seconds it automatically switches back to the movement posture, and the degraded movement posture effect applies.

#### 5.7.3 Dart System Special Mechanisms

In each round, the Dart System can load 4 darts. The Dart Launching Station gate has 2 opportunities to open: 1 at 30 seconds after the match starts and 1 at 4 minutes after the match starts. The Commander may choose suitable times to use them, and unused opportunities accumulate.

**Dart Launching Station gate opening and closing**

During the match, the Commander can use the keyboard and mouse on the Referee System Client to open the launching station gate. While the gate is opening or closing, the Commander cannot control dart launching. The Referee System Client displays the opening and closing status of the gate.

> Note: The gate takes about 7 seconds to open fully.

After the launching station gate is fully open, the Commander can launch darts by controlling the Dart System, for a duration of 30 seconds. At the same time, the dart detection module of the opponent's Outpost or Base refreshes its detection window, which lasts 40 seconds. A launched dart must hit the dart detection module within the detection window, otherwise the attack is invalid.

After the launching station closes its gate for the first time, the Dart Launching Station enters a 15-second cooldown. Only after the cooldown ends can the gate be opened a second time. During the cooldown, the Dart Launching Station gate cannot be opened.

**Dart target selection**

Before controlling the Dart Launching Station gate to open, the Commander can use the Referee System Client to change the target for this round of dart attacks to "Outpost", "Base fixed target", "Base random fixed target", "Base random moving target", or "Base terminal moving target". If the target is selected as "Outpost", then during the same gate opening, after one dart hits, the target can be switched, only once, from "Outpost" to one of the several Base targets.

- If "fixed target" is selected, the dart detection module stays at its initial position.
- If "random fixed target" is selected, then when the Dart Launching Station gate opens, the Base's dart detection module starts moving, and before the gate is fully open it moves to another random position relative to the initial position. After the dart detection window ends it returns to the initial position. During the detection window, if a dart hits, the dart detection module moves to a new position.
- If "random moving target" is selected, then when the Dart Launching Station gate opens, the Base's dart detection module starts moving. After detecting that any dart has been launched, it moves to a new position different from the position at the time of launch, completing the move and coming to rest within 600ms. During the detection window, after a dart hits, or 10 seconds after the first dart launch is detected, the dart detection module starts moving again, until the next dart launch is detected.

<!-- p.112 -->
- If "terminal moving target" is selected, then when the Dart Launching Station gate opens, the Base's dart detection module starts moving. 1.2 seconds after detecting that any dart has been launched, it starts moving to a new position different from the position at the time of launch, completing the move and coming to rest within 600ms. During the detection window, after a dart hits, or 10 seconds after the first dart launch is detected, the dart detection module starts moving again, until the next dart launch is detected.

The dart detection module and the dart guide light keep the same relative position while moving, and always move in the same plane relative to the initial position. The movement range is [-280mm,280mm] relative to the initial position, in the direction parallel to the wide side of the field.

When the target is selected as "random fixed target", "random moving target", or "terminal moving target", a dart hit is valid only after the dart detection module has finished moving and come to rest. Information that the dart detection module has finished moving is displayed on the Referee System Client.

**Dart hit rewards**

The following are the rewards obtained after a dart hits its target, in addition to the damage it causes to the target itself:

- When a dart hits the opponent's Outpost or the Base "fixed target" or "random fixed target" for the first, second, third, and fourth time, all of the opponent's operator interfaces, robot positions on the mini-map, and custom UI are blocked for 10 seconds (first), 5 seconds (second), 3 seconds (third), and 2 seconds (fourth) respectively. When a dart hits the opponent's Base, one's own surviving Infantry Robots equally split 200 (fixed target) or 600 (random fixed target) points of Experience.
- When a dart hits the opponent's Base "random fixed target", the opponent's currently held terrain-crossing and Power Rune Buffs are temporarily disabled, that is, they keep timing normally but have no Buff effect. The disabled duration is the same as the corresponding blocked duration above.
- When a dart hits the opponent's Base "random moving target" or "terminal moving target", all of the opponent's operator interfaces, robot positions on the mini-map, and custom UI are blocked for 10 seconds, one's own surviving Infantry Robots equally split 2500 points of Experience, and the opponent's currently held terrain-crossing and Power Rune Buffs are disabled.
- If the Base dart detection module is hit after "random moving target" or "terminal moving target" was selected, all of the opponent's surviving Ground Robots immediately lose HP equal to 20% (random moving target) or 50% (terminal moving target) of their respective current Max HP (counted toward the opponent's total team damage, but this HP deduction itself and any resulting robot Defeat do not generate Experience). If hits are consecutive, the blocked durations are added together.
- If all 4 darts hit the Base after "fixed target" or "random fixed target" was selected, or any one dart hits the Base after "random moving target" or "terminal moving target" was selected, the opponent's Base armor is deployed immediately.
- If a dart hits the Base or the Outpost, the corresponding Buff Point is temporarily disabled for 30 seconds; if hits are consecutive, the disabled time is refreshed. After each dart hit, the detection window of the corresponding target is closed for 2 seconds.

> Note:
> - While the operator interface, robot positions on the mini-map, and custom UI are blocked, the operator may actively choose to control the robot by semi-automatic control. Specifically, the Referee System Client displays a large map interface similar to the one the Commander has, and the operator can control the robot by clicking on the large map interface to send commands to the robot. The interval between two sends must not be shorter than 3 seconds.
> - The Custom Terminal can still receive data such as the video transmission feed as normal.

<!-- p.113 -->
#### 5.7.4 Radar System Special Mechanisms

The functions of the Radar System include radar recognition and radar decoding of information waves, as follows:

**Radar recognition**

The Radar can recognize the positions of both sides' Ground Robots and send the robots' coordinates to the Referee System server. Each Ground Robot has a "marked progress" P, with a value range from 0 (initial and minimum value) to 150 (maximum value). The Referee System updates P in real time according to the accuracy of the Radar's recognition: consecutive accurate marking makes P rise at an accelerating rate; conversely, consecutive erroneous marking or data interruption makes P decay at an accelerating rate. When P reaches certain thresholds, the corresponding target receives certain effects. In addition, by continuously marking to maintain the opponent's vulnerable state, the Radar can also unlock the "double vulnerability" effect.

> Note: Affected by the wireless environment at the match venue, or when the Positioning Module is covered over a large area, the coordinates detected by a robot's Positioning Module may, with small probability, exhibit intermittent or persistent drift.

Parameter settings:

- d: recognition error, that is, the straight-line distance between the "coordinates sent by the Radar" and the "robot's actual planar coordinates", divided into three levels:
  - Accurate: d<0.8m
  - Semi-accurate: 0.8m≤d<1.6m
  - Erroneous: d≥1.6m
- x: the influence value of the current marking (that is, the progress change amount), with an initial value of 0.
- Judgment frequency: determined by the Radar's sending frequency.

Calculation logic of progress P:

Each time the Referee System receives Radar data, or the data is interrupted, x is updated first, then P is updated.

**Table 5-29 Calculation Logic of "Marked Progress" P**

| Marking state | Update logic of x | Update logic of P |
| --- | --- | --- |
| Accurate | If the previous marking was accurate or semi-accurate, x=x+1.0; otherwise x=1.0 | P=P+x. If the result is P<0, P is set to 0; if the result is P>150, P is set to 150. |
| Semi-accurate | If the previous marking was accurate or semi-accurate, x=x+0.5; otherwise x=0.5 | P=P+x. If the result is P<0, P is set to 0; if the result is P>150, P is set to 150. |
| Erroneous | If the previous marking was erroneous/interrupted, x=x−0.8; otherwise x=−0.8 | P=P+x. If the result is P<0, P is set to 0; if the result is P>150, P is set to 150. |
| Data interruption | Each time the Referee System accumulates 0.5 seconds without receiving data, it is treated as triggering one "erroneous" judgment | P=P+x. If the result is P<0, P is set to 0; if the result is P>150, P is set to 150. |

<!-- p.114 -->
> Example: If one side's Radar continuously sends the coordinates of the opponent's Heavy Robot to the Referee System server at a frequency of 5Hz with 100% accuracy, then within 0 to 1 seconds, at 0.2-second intervals, the opponent Heavy Robot's marked progress is 1, 3, 6, 10, 15 respectively, and at second 3.0 the robot's marked progress reaches 120. After that, if the Radar sends the robot's coordinates to the Referee System server at a frequency of 5Hz with 0% accuracy, then within 3.0 to 4.0 seconds, at 0.2-second intervals, the robot's marked progress is 119.2, 117.6, 115.2, 112, 108 respectively. After that, if the Radar does not send the Heavy Robot's coordinates for 1.0 consecutive seconds, then within 4.0 to 5.0 seconds the robot's marked progress will be 103.2, 97.6 (judged as two additional consecutive errors on top of the previous errors). After that, if the Radar sends the Heavy Robot's correct coordinates twice consecutively, the robot's marked progress will be 98.6, 100.6.

> Note: After a robot is destroyed and Revived, its P value is retained, but its current x value is reset to 0.

Thresholds of P and corresponding effects:

**Table 5-30 Thresholds of P and Effects Obtained by the Corresponding Target**

| Target type | Value range of P | Mini-map display effect | Buff (Ground Robots only) |
| --- | --- | --- | --- |
| Opponent robot | [0,100) | The position corresponding to the robot coordinates sent by one's own Radar | No additional effect |
| Opponent robot | [100,120) | - The actual position detected by the robot's Positioning Module<br>- Special marker | 15% vulnerability |
| Opponent robot | [120,150] | - The actual position detected by the robot's Positioning Module<br>- Special marker | 20% vulnerability |
| Own robot | [0,50) | The position corresponding to the robot coordinates sent by one's own Radar | No additional effect |
| Own robot | [50,150] | - The actual position detected by the robot's Positioning Module<br>- Special marker | No additional effect |

Double vulnerability mechanism: Each time the Radar accumulates 1 minute of making opponent robots vulnerable (when multiple robots are vulnerable at the same time, the time is not added up), it gains 1 opportunity to trigger "double vulnerability". The Radar can consume the opportunity by actively sending a command through the Referee System, which doubles all current vulnerability values originating from the Radar for 30 seconds. In each round, the Radar can trigger "double vulnerability" at most 2 times.

**Radar decoding of electromagnetic waves**

During the match, an official transmitting source will be placed on each side's Radar Base. This source transmits electromagnetic waves, including an information wave carrying the opposing team's information and an interference wave of a similar frequency band. The red side's broadcast source/interference source is placed on the red side's Radar Base and contains information about the blue team, and vice versa. Participating teams can build and install an antenna and a demodulation circuit on the Radar to decode and recognize the information wave and the interference wave, and to provide their own side with information and advantages.

<!-- p.115 -->
The interference wave has three difficulty levels. Decoding difficulty rises with the difficulty level. Specific parameters will be released later.

The information wave will contain the following information about the opponent:

- Positions of each robot
- HP of each robot
- Remaining projectile allowance of each robot
- Buffs currently held by each robot
- Team's remaining Economy
- Team's total Economy
- Activation status of each of the opponent's Buff Points
- Armor hit information

> Note: For the specific communication protocol structure, see: "RoboMaster 2027 RoboMaster University Series Communication Protocol".

The interference wave contains no specific information, but contains a 6-character (alphanumeric combination) key customized by the opponent. The key is reset to a random value at the start of the round and whenever the difficulty of the corresponding side's interference wave changes.

At the start of a round, both sides' interference waves default to difficulty level 1.

The Radar can decode this key and send it to the event engine server. If decoding succeeds, the opponent's interference wave decoding difficulty subsequently rises by 1 level, that is, the difficulty of the interference source placed on one's own Radar Base rises by 1 level. When the opponent's interference wave difficulty is higher than one's own, the opponent's Radar will not produce vulnerability or accumulate "double vulnerability" progress against one's own robots, even if it marks them accurately.

### 5.8 Competition Format and Victory Conditions

The official matches of RMUC 2027 are divided into two stages: the group stage and the knockout stage. The group stage format is BO2 or BO3, and the knockout stage format is BO3 or BO5.

The outcome of a single round is determined item by item in the priority order of the following numbered list, until a final result is obtained:

1. When one side's Base is destroyed, the side with the higher remaining Base HP wins.
2. When the round time runs out, if neither side's Base is destroyed, the side with the higher cumulative control degree wins.
3. When the round time runs out, if neither side's Base is destroyed and the cumulative control degrees are equal, the side with the higher team attack damage wins.
4. When the round time runs out, if neither side's Base is destroyed, the cumulative control degrees are equal, and the team attack damage is equal, the side with the higher total team remaining HP wins.

<!-- p.116 -->
5. If the winner cannot be determined by the above conditions, the round is considered a draw. In BO3 and BO5 matches, if a draw occurs, an extra round is played immediately until a winner is determined.

<!-- p.117 -->
## 6 Match Procedure

*Figure 6-1 Single Match Flowchart*

Flowchart boxes (left) with their annotations (right):

- Teams wait in the staging area for inspection. Annotation: (1) Teams correctly install the Referee System; (2) Check whether the robots comply with the requirements of the competition rules documents.
- Decision: Is the Pre-Match Inspection passed? NO: return to the staging-area step above. YES: continue. Annotation: (1) Arrive at the inspection area for inspection at the specified time before the match; (2) The team captain signs to confirm the inspection result.
- Arrive at the waiting zone. Annotation: (1) Arrive at the waiting zone at the specified time before the match; (2) Follow the order of the waiting zone; (3) Teams wait to enter the field for the match.
- Arrive at the field waiting area.
- Setup Period begins. Annotation: (1) Power on the robots and check that the robots are normal; (2) Connect to the Referee System server; (3) Obtain the initial projectiles; (4) Operators enter the Operator Room; (5) All robots must be powered on for the last 30 seconds; team members must leave the Battlefield; (6) Special situations, technical pause.
- 15-Second Referee System Initialization Period and Five-Second Countdown. Annotation: (1) Referee System self-check; (2) After the Referee System self-check ends, enter the match countdown.
- Match start to end. Annotation: (1) Robots from both sides engage in shooting combat within the Battlefield; (2) The winner is determined according to the match rules.
- Decision: Is there a next round? YES: return to the "Setup Period begins" step. NO: continue.
- One match ends. Annotation: (1) Robots are powered off and leave the Battlefield; (2) Within 5 minutes, the team captain signs to confirm the result or initiates an Appeal.
- The team leaves the field and arrives at the projectile return area. Annotation: Recover projectiles, PASS cards, etc.
- Return to the staging area. Annotation: Return to the staging area.

<!-- p.118 -->
### 6.1 Pre-Match Inspection

> Note:
> - The inspection results of the pre-inspection and adaptive training are for reference only and are not the basis for passing the Pre-Match Inspection of official matches.
> - The inspection result of an official match is valid only for that match.
> - Passing the inspection only proves that the robot met the inspection pass criteria at the time of inspection. Teams must themselves ensure that their robots always meet the requirements of the Robot Building Specifications Manual. During inspection, all functions of the robot must be proactively demonstrated to the inspectors.

To ensure that the robots built by teams comply with the requirements of the "RoboMaster 2027 RoboMaster University Series Robot Building Specifications Manual", teams are advised to arrive at the inspection area 60 minutes before the start of each match. If a team has not started inspection 55 minutes before the start of each match, the team's eligibility to field spare robots is cancelled. If a team has not started inspection 50 minutes before the start of each match, the eligibility of 1 Ground Robot to take the field is cancelled. Robots that have not arrived at the inspection area 45 minutes before the start of the match are stopped from entering the inspection area. The inspection procedure is as follows:

*Figure 6-2 Pre-Match Inspection Flowchart*

Flowchart boxes (left) with their annotations (right):

- Team members bring the robots into the inspection area (inspection begins). Annotation: Each robot may be brought into the inspection area by at most 2 team members; another 1 team member or advisor is responsible for organizing and coordinating the Pre-Match Inspection. Without the approval of the Chief Inspector, other team members may not enter the inspection area. If the participating robots have not arrived at the inspection area, no member of the team may enter the inspection area.
- The robots are inspected. Annotation: Staff mark the robots that need inspection (Ground Robots, all system units contained in Combined Systems, and Auxiliary Equipment). Forms of marking include but are not limited to a PASS card, writing a timestamp to the Referee System on-board end, and Qingliu lineup registration. The marking is modified according to which inspection items are passed, and only robots with a complete mark are eligible to enter the waiting zone and the field area. Teams must modify robots that fail inspection until they meet the inspection requirements and pass. Teams must also check and confirm that the structure, functions, etc. of the Referee System on-board end are normal.
- The team captain signs to confirm the inspection result. Annotation: After the captain signs, no objection to the inspection result may be raised.

Spare robot regulations are as follows:

- At pre-inspection, each team must bring all participating equipment (including spares) for registration and pre-inspection. In subsequent matches within the same event stage, both the team's robots and spare robots must be on the registration list, and no replacement may be made within the same event stage. Registered robots are marked on the main body structure with a unique special identifier (marking methods include but are not limited to: tamper-evident labels, laser marking; the specific form is subject to the on-site arrangement), and the identifier is checked in subsequent match inspections. If maintenance of a robot during the competition affects its unique special identifier, the relevant change information must be submitted through the designated channel.
> Note: After the Revival Tournament ends, the robot list may be re-registered. The specific schedule is subject to the latest notice from the RMOC.

<!-- p.119 -->
- For each match, each team may bring a specified number of main robots and spare robots.
- Each team may borrow the Referee System of at most 2 spare robots.

### 6.2 Waiting Zone

Teams must arrive at the waiting zone at least 10 minutes before the start of each match. The staff in the waiting zone will check the participating robots' PASS cards and the on-site personnel information.

The limits on on-site personnel for each team are as follows:

- 1 advisor.
- 2 team mentors.
- 20 official team members.

One of the on-site personnel must wear the captain-designated mark and perform the captain's duties. After a team enters the waiting zone, if a robot needs repair, it needs the Referee's permission before the robot can leave the waiting zone for repair. After repair is completed, the robot must return to the inspection area for inspection and pass the Pre-Match Inspection again before returning to the waiting zone. If the resulting delay causes the team to fail to arrive at the waiting zone on time, the robot cannot take part in the match, and the team bears the consequences.

> Note: Captain-designated mark: any on-site person wearing the captain-designated mark performs the captain's duties during the match. The captain must oversee the team's match procedure, confirm results, file Appeals, etc.

After the team is sent from the waiting zone to the field, it enters the field's waiting area and places its robots. After the Referee's approval, the team brings its robots to the Battlefield entrance and stands by. According to the match procedure, the Referee opens the door and guides the team members in. The countdown of the three-minute Setup Period starts at the same time the door opens.

### 6.3 Three-Minute Setup Period

> Note:
> - After the second and fourth rounds of a BO5 match end, both teams have 10 minutes to debug their robots. Immediately after the 10 minutes end, the three-minute Setup Period of the next round begins.
> - When a team arrives at the field, it may collect at the designated location all the 42mm light-emitting projectiles needed for that match. For the limit on the quantity of projectiles collected, see "4.5.2 Projectiles"; for example, in a BO3 match, 300 42mm light-emitting projectiles can be collected at one time.
> - After the previous match ends and the Radar has been withdrawn from the Radar Base, the team may deploy the Radar on the Radar Base in advance.

<!-- p.120 -->
During the three-minute Setup Period, on-site personnel must place the robots in their respective starting areas, check that the robots' Referee Systems operate normally, pre-load projectiles into the robots, debug the modular 42mm launching mechanism, load darts into the Dart System, deploy the Radar on the Radar Base, and install the aerial system on the Hangar platform. On-site personnel may repair robots or replace their equivalent parts, but must meet the requirements of the specification documents. On-site personnel must debug the robots near their own robots' starting areas. Each team is allowed only 2 on-site personnel to leave the Base and the vicinity of its starting area to assist with debugging, and they may not cross the Central Highland. The starting areas are shown in the figure below:

*Figure 6-3 Setup Period Debugging Area Diagram*

- [1] Red Base and the vicinity of its starting area
- [2] Red Hangar platform and the vicinity of its starting area
- [3] Blue Hangar platform and the vicinity of its starting area
- [4] Blue Base and the vicinity of its starting area

> Note:
> - Equivalent parts: standard modules or parts of the same material, form, and function, such as motors of the same model, or self-made friction wheel modules. The main structures carrying the robot body cannot be replaced as equivalent parts, such as a robot's chassis or an Aerial Robot's airframe.
> - If an "equivalent part" contains a Referee System module, the team must itself ensure that the Referee System on-board end module can be used normally (including version number, sensor calibration, installation standards, etc.). When the Referee System on-board end module in an "equivalent part" is abnormal, the team bears the consequences, and no official technical pause will be triggered.

When 1 minute 30 seconds remain in the three-minute Setup Period, operators are advised to enter the Operator Room to debug the keyboard and mouse. Check and confirm that robot control and the official equipment operate normally. If the official equipment cannot operate normally, on-site personnel must raise it before 15 seconds remain in the three-minute Setup Period, other

<!-- p.121 -->
wise the Referee will not grant a technical pause. During the three-minute Setup Period, in the Operator Room, besides the operators and Commander corresponding to the robots taking the field, at most 1 additional person is allowed to enter for pre-match tactical deployment. Before the three-minute Setup Period ends, anyone other than the operators and Commander corresponding to the robots taking the field must leave the Operator Room.

When 30 seconds remain in the three-minute Setup Period, all robots in the Battlefield must be powered on, and personnel in the Battlefield leave in an orderly manner. Robots that are still not powered on when 15 seconds remain in the three-minute Setup Period must be moved out of the Battlefield. After the three-minute Setup Period ends, on-site personnel must place the Sentry Robot's and the Radar's Remote Controllers in the designated area at the Battlefield entrance or the Operator Room entrance.

#### 6.3.1 Official Technical Pause

During the three-minute Setup Period, when the Referee System or official equipment malfunctions, or a robot needs temporary inspection (the malfunction situations are shown in the table below), the Head Referee may initiate an official technical pause and pause the countdown. The time at which the pause is initiated is decided by the Head Referee according to the situation.

During an official technical pause, on-site personnel must cooperate with the Referee's requirements to eliminate faults related to the Referee System or official equipment, and may not repair other faults. If the Referee System malfunctions and needs replacement, the time limits for replacing the Referee System on-board end in the "RoboMaster 2027 RoboMaster University Series Robot Building Specifications Manual" must be followed. After the faults related to the Referee System or official equipment are eliminated and the Head Referee resumes the countdown, on-site personnel must follow the standards of the three-minute Setup Period and leave the Battlefield at the specified time points.

**Table 6-1 Malfunction Situations**

| Item | Description |
| --- | --- |
| 1 | Official equipment in the Operator Room malfunctions, or key match props in the Battlefield suffer structural damage or functional abnormality. |
| 2 | During the three-minute Setup Period of the first round, a Referee System on-board end module malfunctions, for example: an Armor Module is damaged, or a Speed Monitor Module is offline. |
| 3 | During the three-minute Setup Period, the Referee System main controller cannot connect to the server, or the robot cannot transmit images back to the Operator Room normally. |
| 4 | Other situations that the Head Referee judges to require an official technical pause. |

Because it cannot be determined whether a malfunction is due to a fault in the Referee System module itself, a defect in the participating robot's circuit or structural design, or a result of robot combat in earlier matches, except for the situation in item 3 above, ordinary battle damage does not trigger an official technical pause, and the Referee will provide a spare Referee System module. The team may apply for a "team technical pause" to repair the robot.

If, after investigation by the Referee, the malfunction situations described in items 2 and 3 above are caused by the team, the Referee will explain the situation and end the official technical pause.

#### 6.3.2 Team Technical Pause

If a robot's mechanical structure, software system, or the Custom Terminal and other equipment brought into the Operator Room malfunctions, the team may apply for a "team technical pause" only before the 15-second countdown of the three-minute Setup Period, with on-site personnel applying to the Referee in the Battlefield or Operator Room and stating the reason for the application.

<!-- p.122 -->
Once a team technical pause application has been initiated and conveyed to the Head Referee, this technical pause cannot be withdrawn or modified.

After the Head Referee confirms a team technical pause, regardless of which side initiated it, the Referee will notify both teams at the same time. During the team technical pause, both teams may continue to debug and repair robots as normal.

After the Head Referee confirms that both teams are ready, the technical pause may be ended early. Even if a team did not enter the Battlefield or the technical pause was ended early, the opportunity consumed is still the one corresponding to the time declared when the team applied.

To ensure that the subsequent schedule proceeds on time, in the same three-minute Setup Period the two sides together may initiate only 1 team technical pause, on a first-come, first-served basis. The post-match result confirmation form records whether a technical pause opportunity was consumed during the match.

The team technical pause arrangements for different schedule stages within the same event stage are shown below:

**Table 6-2 Team Technical Pause Arrangements**

| Event stage | Schedule stage | Arrangement |
| --- | --- | --- |
| Regional Competition | Group stage | 2 two-minute technical pauses. |
| Regional Competition | Knockout stage | 1 three-minute technical pause. If the technical pause opportunities in the group stage are not used up, they can carry over to the knockout stage. |

### 6.4 15-Second Referee System Initialization Period

After the three-minute Setup Period ends, the match enters the 15-Second Referee System Initialization Period. During the self-check, the Referee System server automatically checks the connection status of the Referee System Clients, the status of the robots' Referee System modules, and the status of the field props, and resets all robots' HP, ensuring that all robots are at full HP when the match starts.

### 6.5 Five-Second Referee System Self-Check Period

After the 15-Second Referee System Initialization Period ends, the match enters the Five-Second Countdown. During this time, the Referee System Client does not respond to robot control commands (including the Custom Terminal). After the countdown ends, the Referee System Client resumes responding to robot control commands, and the match starts immediately.

### 6.6 Seven-Minute Round

In the seven-minute Round, the robots of the two teams engage in shooting combat in the core competition venue (the Battlefield).

### 6.7 Match End

A round ends when the round time runs out or one team triggers the Victory Conditions early. For the Victory Conditions, see "5.8 Competition Format and Victory Conditions". A match ends when the winner of the match is determined or all rounds are finished.

<!-- p.123 -->
### 6.8 Result Confirmation

In a match, the Referee records on the result confirmation form the main penalty situations of each round, key settlement information at the end of the match, win/loss results, and the use of the team technical pause opportunity.

The team captain must sign to confirm the match result within 5 minutes after a match ends. If the captain neither signs to confirm the result nor files an Appeal within 5 minutes, the match result is deemed confirmed.

### 6.9 Leaving the Field

After a match ends, the team must power off its robots and move them out of the Battlefield, and go to the projectile return area to return projectiles. In the projectile return area, the team must follow the staff's guidance, proactively return the relevant materials, empty the projectiles loaded in the robots, and proactively return all projectiles used in the match.

<!-- p.124 -->
## 7 Violations and Penalties

To ensure the fairness of the competition and strict discipline, teams, participants, and robots must strictly follow the match rules. In case of violations, the Referee will impose corresponding penalties. Some violation penalties issued before the official start of the match will be executed after the official start. Major penalties during the match and all Appeals will be publicly announced.

The penalties corresponding to all violation provisions in this chapter are determined by the Head Referee according to the actual situation of the match. If a situation arises during the match that affects the fairness of the match but is not covered by the detailed penalty rules and serious violations, it is determined by the Head Referee according to the actual situation.

> Note: If one side's behavior directly causes the other side to commit a violation, the other side is not considered to have violated the rules, but must terminate the violating behavior promptly.

### 7.1 Penalty System

#### 7.1.1 Penalty Methods

During the event, the Referee System or Referees will impose penalties on participants and robots that do not comply with the event rules. The penalty methods are as follows:

**Table 7-1 Penalty Methods**

| Penalty method | Description |
| --- | --- |
| Referee System automatic penalty | Everything in "5.1 HP Deduction and Exceeding-the-Limit Penalty Mechanism" other than attack damage or collision and Penalty Damage belongs to Referee System automatic penalties. |
| Referee System manual penalty | A penalty issued by a Referee operating the server against a robot's violation. |
| Referee manual penalty | Applies to scenarios where the Referee System cannot be used to impose a penalty, such as verbal warnings and disqualification from the match. |

#### 7.1.2 Penalty Types

The types of manual penalties during the match are shown in the table below:

**Table 7-2 Penalty Types**

| Penalty type | Description |
| --- | --- |
| Verbal warning | Verbal caution |
| Yellow Card Warning | - One-side Yellow Card: |

<!-- p.125 -->
| Penalty type | Description |
| --- | --- |
| Yellow Card Warning | &nbsp;&nbsp;- If the violating robot is a Sentry Robot, its chassis is powered off for 2 seconds, and other robots' operation interfaces are blocked for 2 seconds.<br>&nbsp;&nbsp;- If the violating robot is not a Sentry Robot, its operation interface is blocked for 5 seconds, and other robots' operation interfaces are blocked for 2 seconds.<br>&nbsp;&nbsp;- The Referee System automatically deducts 15% of the violating robot's current Max HP, and the other surviving robots are deducted 5% of their current Max HP. If a robot receives another Yellow Card Warning within 30 seconds of each Yellow Card Warning, the percentage of current Max HP deducted is 2 times the previous one, and the other surviving robots are deducted 5% of their current Max HP.<br>&nbsp;&nbsp;- In each round, when all robots have cumulatively received 3 Yellow Card Warnings, a Red Card Warning is received at the same time.<br>- Both-side Yellow Card: All operators' operation interfaces are blocked for 2 seconds, and all robots are deducted 5% of Max HP, which does not count toward a single robot's cumulative Yellow Card count.<br>> Note: (1) If Yellow Card Warnings are received consecutively, the interface blocking times are added together, and the 30-second timer is reset. (2) If a robot's remaining HP is less than or equal to the HP to be deducted by the penalty, the robot's HP is reduced to 1. (3) The durations of chassis power-off, interface blocking, etc. caused by violation penalties are independent of match mechanisms and do not stack with them. (4) When the interface is blocked due to a Yellow Card Warning, the video transmission feed, mini-map, and custom UI are all unavailable. |
| Red Card Warning (Ejection) | - Ejected robot:<br>&nbsp;&nbsp;- If a robot is ejected before the 15-Second Referee System Initialization Period, the violating robot is not allowed to take the field and must be moved out of the Battlefield, and no other robot may substitute for it in all rounds of that match.<br>&nbsp;&nbsp;- If a robot is ejected during the 15-Second Referee System Initialization Period, the Red Card Warning is issued after the match starts.<br>&nbsp;&nbsp;- If the aerial system is ejected during the match, the Hangar is powered off. If the Aerial Robot is in flight, the safety officer must immediately take control of the Remote Controller and stop the propellers, and the Aerial Robot may not fly again. If the Dart System is ejected during the match, the dart launch button is immediately disabled and the Dart Launching Station gate cannot be opened; |

<!-- p.126 -->
| Penalty type | Description |
| --- | --- |
| Red Card Warning (Ejection) | &nbsp;&nbsp;if the gate is already open, it is closed immediately.<br>&nbsp;&nbsp;- If the Radar is ejected during the match, the Radar's multi-machine communication is disconnected (it can only receive one-way and can no longer send).<br>&nbsp;&nbsp;- If a Ground Robot is ejected during the match, the robot's HP immediately becomes 0, its video transmission feed is disconnected, its multi-machine communication is disconnected, and it cannot be Revived.<br>- Ejected Auxiliary Equipment: the corresponding equipment is not allowed to take the field.<br>- Ejected on-site personnel: the Referee requires the ejected on-site personnel to leave the competition area immediately, and no other on-site personnel may substitute for them in all rounds of that match. If an operator is ejected, the robot they operate is ejected for that round and is not allowed to take the field in all rounds of that match, and no robot may substitute for it; if the Commander is ejected, both the aerial system and the Dart System are ejected and are not allowed to take the field in all rounds of that match, and no robot may substitute for them. |
| Loss by forfeit | - If a Loss by forfeit penalty is issued for a round (hereinafter "round forfeit"), the details are as follows:<br>&nbsp;&nbsp;- If the forfeit penalty is issued before the seven-minute Round (including the three-minute Setup Period and the 15-Second Referee System Initialization Period), the violating side's Base HP is 0 and control degree is 0, and its other robots have full HP. The other side's Base and robots have full HP, and its control degree is 1680. Both teams' total team damage is considered 0. The round time is considered 420s.<br>&nbsp;&nbsp;- If the forfeit penalty is issued during the seven-minute Round, the round ends immediately. The violating side's Base HP is 0, its other robots' HP is as of the end of the match, and its control degree is the value at the end of the match. The other side's Base and robots' HP is as of the end of the match, and its control degree is the value at the end of the match. The round time is the actual match time elapsed when the forfeit was issued.<br>&nbsp;&nbsp;- If the forfeit penalty is issued after the seven-minute Round ends, the violating side's Base HP is 0, its other robots' HP is as of the end of the match, and its control degree is the value at the end of the match. The other side's Base and robots' HP is as of the end of the match, and its control degree is the value at the end of the match. The round time is the actual match time elapsed when the forfeit was issued.<br>- If a forfeit penalty is issued for a match (hereinafter "match forfeit"), that is, a forfeit penalty is issued for all rounds of that match, the HP settlement of each round follows the description above. |
| Disqualification from awards | - Participants are disqualified from awards.<br>- Teams are disqualified from awards. |

<!-- p.127 -->
| Penalty Type | Description |
| --- | --- |
| Disqualification | - Participants are disqualified from the competition and from awards.<br>- Teams are disqualified from the competition and from awards. The team's results for this season are retained as a reference for the advancement of other teams. |

### 7.2 Penalty Details

This section describes the detailed violation penalties. Items numbered R# are rules that explicitly state what participating teams, participants and robots must follow.

#### 7.2.1 Personnel

##### 7.2.1.1 General Requirements

**R1** Participating teams must meet the requirements of the *RoboMaster 2027 RoboMaster University Championship Participant Manual*.
Violation penalty: up to disqualification of the violating party.

**R2** Participants and their actions must not interfere with the normal operation of official equipment or competition procedures, or the normal work of RMOC staff.
Violation penalty: up to disqualification of the violating party.

**R3** Participating teams must not set up their own wireless devices or use walkie-talkies in competition-related areas (including but not limited to the preparation area, the Pre-Match Inspection area, the waiting area and the competition area).
Violation penalty: up to disqualification of the violating party.

**R4** Participating teams must not damage official equipment (including but not limited to equipment located in the competition area, waiting area, preparation area and Pre-Match Inspection area).
Violation penalty: up to disqualification of the violating party, and the violating party must pay compensation at the equipment's price.

**R5** Except for field personnel who enter the waiting area and competition area for the needs of the match, other participants must not enter the waiting area and competition area without special reason.
Violation penalty: up to disqualification of the violating personnel.

**R6** Field personnel who have entered the waiting area or competition area for the needs of the match must not leave the waiting area or competition area, or change field personnel, without the Referee's consent.
Violation penalty: the violating personnel may not enter the waiting area and competition area for this match, up to disqualification of the violating personnel.

**R7** Except for projectiles preloaded in the Pre-Match Inspection area, participating teams must not bring their own projectiles for use in the match into the waiting area or competition area.
Violation penalty: the projectiles are confiscated, up to disqualification of the violating personnel.

<!-- p.128 -->
**R8** After a match ends, field personnel must immediately power off the robots and move them out of the competition area, and empty the projectiles inside the robots in the projectile return area.
Violation penalty: the violating robot is held in the projectile return area until its projectiles are emptied.

**R9** After a match ends, field personnel must return all projectiles used in the match in the projectile return area.
Violation penalty: the projectiles are confiscated and the violating personnel lose the right to enter the competition area in subsequent matches in the current regional competition. Up to disqualification of the violating personnel.

**R10** Except in emergencies, participating teams must arrive at the Pre-Match Inspection area for Pre-Match Inspection at least 55 minutes before the start of each match, and must arrive at the waiting area and be ready at least 10 minutes before the start of each match.
Violation penalty: up to Loss by forfeit for the match.

**R11** Without the Referee's permission, after a robot passes inspection and before the match ends, the robot must not be powered on for debugging or repaired outside the Battlefield.
Violation penalty: up to Loss by forfeit for the match.

**R12** The identity and number of personnel each team sends into designated areas such as the preparation area, Pre-Match Inspection area, waiting area and competition area must meet the requirements.
Violation penalty: up to disqualification of the violating party.

**R13** Field personnel must wear the corresponding badges, and the badges must not be covered. One person must wear the badge designated for the team captain.
Violation penalty: up to disqualification of the violating personnel.

**R14** Without the Referee's permission, field personnel who have entered the competition area must not communicate with the outside in any way.
Violation penalty: up to disqualification of the violating personnel.

**R15** Except for the Radar, field personnel must not use official equipment power supplies to power their own equipment in the competition area, but may bring their own power supplies.
Violation penalty: up to disqualification of the violating personnel.

**R16** Except in special circumstances, field personnel are prohibited from entering the competition area wearing slippers.
Violation penalty: up to a Red Card Warning for the violating personnel.

**R17** During an Appeal, the appealing party must provide valid evidence or the relevant provisions of the normative documents relied upon.
Violation penalty: up to disqualification of the violating personnel.

**R18** The team captain has management responsibilities and must ensure the following during preparation and the competition:
- Participating robots must pass the review of complete finished robots and the open-source robot usage specifications.
- Team advisors, reserve-squad members and other persons not eligible for awards must not commit violations during the competition.
- Other violations must be stopped promptly.

Violation penalty: the captain's management responsibility is determined according to the violation, up to disqualification of the violating personnel.

<!-- p.129 -->
##### 7.2.1.2 Battlefield Requirements

**R19** Field personnel must wear safety goggles when entering the Battlefield.
Violation penalty: verbal warning, and the violating personnel are ejected from the Battlefield. If the warning is ineffective, a Red Card Warning is issued to the violating personnel.

**R20** During an official technical pause, field personnel must not repair faults other than those of Referee System related modules.
Violation penalty: verbal warning. If the warning is ineffective, a Red Card Warning is issued to the violating personnel.

**R21** After the three-minute Setup Period ends, field personnel must return to the designated area outside the Battlefield. During the match, field personnel must not leave this area without the Referee's permission.
Violation penalty: verbal warning. If the warning is ineffective, a Red Card Warning is issued to the violating personnel.

**R22** After 30 s remain in the three-minute Setup Period, team members are prohibited from continuing to debug robots inside the competition area.
Violation penalty: verbal warning. If the warning is ineffective, a Red Card Warning is issued to the violating robot after the match starts.

**R23** After the three-minute Setup Period ends, the Remote Controllers of the Sentry Robot and the Radar must be placed in the designated area at the Battlefield entrance or Operator Room entrance, and the Remote Controllers of the other robots must be placed inside the Operator Room or at the designated position at the Battlefield entrance.
Violation penalty: if before the seven-minute Round, a verbal warning; if the warning is ineffective, a Red Card Warning is issued to the violating robot. If during the seven-minute Round, a Red Card Warning is issued to the violating robot.

**R24** After the Five-Second Countdown begins, field personnel must not operate the Remote Controllers corresponding to the robots on the field that are located outside the Operator Room.
Violation penalty: a Red Card Warning is issued to the violating robot, up to Loss by forfeit for the round.

**R25** Field personnel must ensure that their own robots operate safely and do not cause harm to any personnel or equipment in the competition area.
Violation penalty: the violating party bears the corresponding responsibility.

##### 7.2.1.3 Operator Room Requirements

**R26** During the three-minute Setup Period, in addition to the Operators and Commander corresponding to the robots on the field, at most 1 additional person is allowed in the Operator Room, and persons other than the Operators and Commander corresponding to the robots on the field must leave the Operator Room before the three-minute Setup Period ends.
Violation penalty: verbal warning. If the warning is ineffective, a Red Card Warning is issued to the violating personnel.

**R27** Without the Referee's permission, during the 15-Second Referee System Initialization Period and the seven-minute Round, Operators must be in the corresponding Operator Room, operate the control devices of the corresponding robot, wear the corresponding headset, and must not change position after the three-minute Setup Period ends.
Violation penalty: verbal warning. If the warning is ineffective, a Red Card Warning is issued to the violating personnel.

**R28** An Operator has not arrived at the Operator Room before the Five-Second Countdown, or leaves the Operator Room during the seven-minute Round.
Violation penalty: a Red Card Warning is issued to the violating personnel.

<!-- p.130 -->
**R29** During the seven-minute Round, the Commander may be configured with the Hangar Remote Controller, the Dart System Remote Controller and a Custom Terminal at the same time. Apart from this, each Operator must configure control devices and a Custom Terminal according to the control method requirements of the corresponding robot.
Violation penalty: verbal warning. If the warning is ineffective, a Red Card Warning is issued to the violating personnel.

**R30** During the match, the safety officer must watch the flight of the Aerial Robot and may operate the Remote Controller used for emergency propeller stop only when an urgent safety problem occurs (for example, the robot is about to fly out of the Battlefield).
Violation penalty: if the safety officer operates the emergency propeller stop Remote Controller, a Red Card Warning is issued to the Aerial System.

**R31** Using your own headsets or computers (other than the Custom Terminal) in the Operator Room is prohibited.
Violation penalty: verbal warning. If the warning is ineffective, Loss by forfeit for the round.

**R32** Each operating device in the Operator Room provides at most 1 RJ45 network port, and this port may only be connected to the Custom Terminal.
Violation penalty: verbal warning, and use of the violating device is prohibited. If the device is affected, up to disqualification of the violating party.

**R33** During the match, communication with the outside of the Operator Room is not allowed.
Violation penalty: verbal warning. If the warning is ineffective, Loss by forfeit for the round.

#### 7.2.2 Robots

##### 7.2.2.1 General Requirements

**R34** Robots and related equipment used in the match must pass Pre-Match Inspection.
Violation penalty: Loss by forfeit for the round.

**R35** In the first round of a match, the robots must meet the minimum lineup for taking the field.
Violation penalty: Loss by forfeit for the match.

**R36** Robots must meet the requirements of the *RoboMaster 2027 RoboMaster University Series Robot Building Specifications Manual*.
Violation penalty: up to disqualification of the violating party.

> Note:
> - The RMOC will conduct spot checks on robots from time to time.
> - If a robot is reported as not complying with the Robot Building Specifications, the reporter must provide corresponding evidence.
> - During the match, if the Positioning Module or Speed Monitor Module is not installed as required, the corresponding module is regarded as offline for that round.

**R37** In case of a dispute, participating teams are responsible for showing the RMOC the robot's mechanical and circuit design drawings and related code files, and for answering related technical inquiries.
Violation penalty: up to disqualification of the violating party.

<!-- p.131 -->
**R38** While waiting in the waiting area, participants must not take robots out of the waiting area without permission.
Violation penalty: verbal warning. If the warning is ineffective, a Red Card Warning is issued to the violating personnel and robot, up to disqualification of the violating personnel.

**R39** Robots must not have or develop safety hazards including but not limited to short circuits, crashes, smoke, open flames, parts falling to the ground and gas cylinder explosions; if a safety hazard exists or occurs, participants must cooperate with the Referee in carrying out the corresponding operations.
Violation penalty: before the Battlefield is cleared, field personnel must resolve the safety problem as the Referee requires, otherwise the violating robot may not take the field. If during the match, a verbal warning; if the warning is ineffective, a Red Card Warning is issued to the violating personnel or the violating robot. If the safety hazard is serious, the Head Referee handles it according to "8 Abnormal Situations".

**R40** No robot may continuously launch projectiles out of the Battlefield.
Violation penalty: verbal warning. If the warning is ineffective, a Red Card Warning is issued to the violating robot.

**R41** The Dart System must not launch darts out of the Battlefield.
Violation penalty: a Red Card Warning is issued to the violating robot.

**R42** From the three-minute Setup Period until the Battlefield is cleared, robots inside the Battlefield must not leave their corresponding debugging area. After the Battlefield is cleared, through the 15-Second Referee System Initialization Period and the Five-Second Countdown, robots inside the Battlefield must not leave their corresponding starting area.
Violation penalty: up to a Red Card Warning for the violating robot.

**R43** During the three-minute Setup Period, if projectiles need to be launched, they must be launched into the projectile clearing bag.
Violation penalty: up to a Red Card Warning for the violating robot.

**R44** During the three-minute Setup Period, modules or parts replaced on a robot must meet the "equivalent part" requirements.
Violation penalty: up to a Red Card Warning for the violating robot.

##### 7.2.2.2 Ground Robots

**R45** During the match, no surviving robot may use its own structure to block any of its own Armor Modules, and no robot may block more than 1 Armor Module of other surviving robots on its own side. When a Heavy Robot grasps or carries Movable Props, the carried Movable Props and the related parts of its own structure are allowed to block 1 of its own Armor Modules, and the blocked Armor Module may be a different one each time, but blocking multiple Armor Modules at the same time is not allowed.

> Note:
> - Infantry Robots and Sentry Robots must not block their own Armor Modules while carrying Movable Props.
> - If a blocked Armor Module goes offline, it is not considered a violation.

Violation penalty: if 1 Armor Module is blocked, a warning is issued to the violating party according to subjective intent: if the blocking is active, a Yellow Card Warning and a verbal warning are issued when the violation occurs, and if the warning is ineffective, a Red Card Warning is issued; if the blocking is passive, 1 Yellow Card Warning is issued when the violation occurs.

<!-- p.132 -->
If the number of blocked Armor Modules is greater than 1, a Yellow Card Warning and a verbal warning are issued when the violation occurs, and if the warning is ineffective, a Red Card Warning is issued.

**R46** The subsystems or individual units into which a Heavy Robot is separated must not leave the Workbench.
Violation penalty: up to a Red Card Warning for the violating robot.

##### 7.2.2.3 Combined Systems

**R47** During the three-minute Setup Period, field personnel may debug the Aerial System near the Hangar platform and its starting area, but must not start the propellers.
Violation penalty: up to a Red Card Warning for the violating personnel and the violating robot.

**R48** During the match, the Aerial Robot must not fly out of the Battlefield.
Violation penalty: a Red Card Warning is issued to the violating robot. This Aerial System may not take the field in the other rounds of the same match.

**R49** During the match, if the Aerial System develops a fault, or suffers battle damage because of an unreasonable design of the power system and power supply system, the system may continue to take the field only after passing the Referee's inspection and after the Head Referee confirms there are no safety hazards.
Violation penalty: a Red Card Warning is issued to the violating robot. The violating robot may not take the field in the other rounds of the same match.

> Note: For safety reasons, if the Aerial Robot flies unstably during the match, the Head Referee will eject the Aerial System. The safety officer should land the Aerial Robot and stop the propellers as soon as possible, and must not operate that Aerial Robot again.

**R50** Except during the seven-minute Round, the Dart System must not be in the ready-to-launch state.

> Note: Ready-to-launch state: the energy storage element used to give the dart its initial kinetic energy is tensioned, inflated or rotating. Energy storage elements include but are not limited to rubber bands, cylinders and friction wheels.

Violation penalty: verbal warning. If the warning is ineffective, a Red Card Warning is issued to the violating robot.

#### 7.2.3 Interaction

##### 7.2.3.1 Robot Interaction

**R51** A robot of one side must not use any of its own structure to collide with a robot of the other side. If a Defeated robot blocks a key movement path, it may be pushed away slowly.
Violation penalty: a warning is issued to the violating robot according to subjective intent and the severity of the collision.

<!-- p.133 -->
**Table 7-3 Collision Violation Penalty Standards**

| Violation Level | Description |
| --- | --- |
| Yellow Card Warning | - Actively causing a head-on, fast collision<br>- Actively pushing so that the other side's robot moves noticeably<br>- Actively pushing the other side's robot so that its normal movement is obstructed |
| Red Card Warning | - Actively causing a head-on, fast, repeated or violent collision<br>- Actively pushing so that the other side's robot moves a considerable distance<br>- Actively pushing the other side's robot so that its normal movement is severely obstructed |

If the collision has serious consequences for the other side's robot or affects the fairness of the match, in the next round of the same competition stage the violating robot (by robot number only) may not take the field, and no other robot may substitute for it.

**R52** A robot of one side must not, through active interference, blocking, collision or similar behavior, cause any of its own structure to become fixedly attached to a robot of the other side (except robots that cannot be revived).
Violation penalty: timing starts from the moment the attachment can be determined, and warnings are issued to the violating robot according to the violation duration: the first Yellow Card Warning is issued when the violation exceeds 10 s, and then 1 Yellow Card Warning every 20 s until the violating robot is ejected. Whether or not the violating robot is alive, when the violation time exceeds 90 s, up to Loss by forfeit for the round is issued according to the subjective intent of the violating party's behavior.

**R53** A robot of one side must not actively attack the other side's Dart launcher or Radar.
Violation penalty: up to disqualification of the violating party.

**R54** A robot of one side, and its actions, must not block a robot of the other side from entering its Supply Zone.
Violation penalty: a Yellow Card Warning is issued to the violating robot. If the warning is ineffective, a Red Card Warning is issued to the violating robot.

**R55** Robots must not actively carry the other side's darts or the other side's Aerial Robot.
Violation penalty: verbal warning. If the warning is ineffective, a Red Card Warning is issued to the violating robot.

<!-- p.134 -->
##### 7.2.3.2 Robot Interaction with Field Props

Multiple Restricted Zones are set up in the Battlefield. A Restricted Zone covers the ground and the vertical airspace above it. If a robot body or anything it carries (such as Movable Props) touches or enters this space, it is judged to have entered the Restricted Zone. The extent of the Restricted Zones is shown in the figure below.

*Figure 7-1 Battlefield Restricted Zones*

- [1] Supply Restricted Zone
- [2] Base Restricted Zone
- [3] Assembly Restricted Zone
- [4] Dart Launching Station Restricted Zone

Robot interaction with Restricted Zones must follow the rules below, otherwise it is regarded as a violating entry into the Restricted Zone.

- One-side Restricted Zone: only robots of the owning side may enter; all robots of the other side are prohibited from entering.
- Shared Restricted Zone: all robots of both sides are prohibited from entering.

**Table 7-4 Battlefield Restricted Zone Access Rules**

| Restricted Zone | Restricted Zone Attribute |
| --- | --- |
| Supply Restricted Zone | One-side Restricted Zone |
| Assembly Restricted Zone | One-side Restricted Zone |
| Base Restricted Zone | Shared Restricted Zone |
| Dart Launching Station Restricted Zone | Shared Restricted Zone |

<!-- p.135 -->
**R56** Ground Robots must not enter the Base Restricted Zone in violation of the rules.
Violation penalty: warnings are issued to the violating robot according to the duration of stay and the impact of the violating behavior. The first Yellow Card Warning is issued when the violation exceeds 3 s, and then 1 Yellow Card Warning every 10 s until the violating robot is ejected.

**R57** Ground Robots must not enter the Supply Restricted Zone or Assembly Restricted Zone in violation of the rules.

> Note: If a robot is Defeated or ejected inside any Restricted Zone, the Referee may, depending on the situation on site, set the robot to a temporarily activated state and guide its Operator to operate the robot out of the Restricted Zone.

Violation penalty: warnings are issued to the violating robot according to the duration of stay and the impact of the violating behavior. The first Yellow Card Warning is issued when the violation duration exceeds 3 s, and then 1 Yellow Card Warning every 5 s until the violating robot is ejected. If a robot that is Defeated or abnormally offline stays in a Restricted Zone for more than 20 s, up to Loss by forfeit for the round.

**R58** Robots must not place Movable Props into their own Supply Restricted Zone, the Shared Base Restricted Zones, or the other side's Dart Launching Station.
Violation penalty: a Yellow Card Warning is issued to the violating robot. If the Movable Props subsequently have a decisive effect on projectile resupply, dart launching or dart hits, or affect the normal operation of any core prop, a Red Card Warning is issued to the violating robot.

**R59** Wireless debuggers and Movable Props used in the match must not be brought into the competition area. During the match, robots may only use the official dedicated projectiles and Movable Props provided in the competition area by the RMOC.
Violation penalty: items brought into the competition area are confiscated; if the match is affected, up to disqualification of the violating party.

**R60** Robots must not obtain, or carry or use in any way, an Energy Unit that has already been successfully assembled.
Violation penalty: Loss by forfeit for the round.

**R61** During the match, robots must not damage the Battlefield, field props or projectiles, nor affect the normal function of field props.
Violation penalty: up to disqualification of the violating party.

**R62** 42mm projectiles, darts and Aerial Robots must not be used to hit the Power Rune and the Hangar.
Violation penalty: up to a Red Card Warning for the violating robot.

**R63** During assembly, robots must not operate the movable structures of the Tech Core (other than the Energy Unit) or other body structures.
Violation penalty: Loss by forfeit for the round.

**R64** Robots and the Aerial System must not enter the Dart Launching Station Restricted Zone in violation of the rules.
Violation penalty: a Red Card Warning is issued to the violating robot.

### 7.3 Serious Violations

If any of the behaviors listed below occurs during the competition, it is judged a serious violation. For serious violations, the RMOC will disqualify the violating party at most from the competition.

<!-- p.136 -->
If the behavior violates local laws and regulations, the RMOC will cooperate with the relevant authorities in pursuing the legal liability of the offender.

**Table 7-5 Types of Serious Violations**

| No. | Type |
| --- | --- |
| 1 | Maliciously damaging official equipment such as the venue and props, or other teams' robots, equipment, etc. |
| 2 | Cheating, impersonation or other dishonest participation. |
| 3 | Modifying or damaging the Referee System, or using technical means to interfere with any detection function of the Referee System. |
| 4 | Failing to comply with the normative documents and being judged a serious violation by the Chief Referee. |
| 5 | Disobeying penalties, not cooperating with inspections, deliberate delay, disrupting order, withdrawing or boycotting without reason, and other behavior that hinders the match. |
| 6 | Passive play, match manipulation and similar behavior. |
| 7 | Giving property to others, or unlawfully soliciting or accepting property from others, in order to obtain improper competition results or improper benefits. |
| 8 | Uncivil or immoral words and actions such as slandering, abusing, making improper gestures, malicious heckling and maliciously throwing objects. |
| 9 | Publishing, spreading or disseminating to the media false or irresponsible statements. |
| 10 | Deliberately attacking or colliding with others, or acting in a way that endangers one's own or others' safety. |
| 11 | Carrying dangerous or prohibited items. |
| 12 | Other behavior that violates the spirit of the competition and is judged a serious violation. |
| 13 | Other words and actions that run counter to the core socialist values, violate sportsmanship, violate public order and good morals, violate competition conduct and discipline, cause adverse social impact, or violate laws and regulations. |

<!-- p.137 -->
## 8 Abnormal Situations

> Note: There may be some delay in the Referee's manual penalties and handling of abnormal situations. If this has a major impact on the match result, the Chief Referee will determine the final handling according to the actual situation.

If any of the following abnormal situations occurs, it will be handled in the corresponding way, and neither team may object. The handling is as follows:

- When a serious safety hazard or abnormal condition occurs, for example battery combustion or explosion, venue power outage, high-pressure gas cylinder explosion or conflict among personnel on the field, after the Head Referee finds and confirms it, the Head Referee will notify both Operators and eject all robots through the Referee System, the result of that round is void, and the round is restarted after the hazard or abnormal condition is cleared. The RMOC will handle safety problems first and protect the robots as far as possible, but cannot guarantee that robots will not be affected at all; any loss or impact caused by safety handling is borne by the participating team.
- During the match, if non-critical props in the Battlefield are damaged, for example damaged floor mat, damaged field Light Indicators or damaged Base lighting effects, which do not affect the fairness of the match, the match proceeds normally.
- During the match, if abnormal robot Armor Module lighting effects or Light Indicator effects, damaged Armor Modules or similar situations occur, the match proceeds normally.
- During the match, if critical official equipment or props malfunction or are structurally damaged in a way that affects the fairness of the match, for example the on-site network is abnormal and causes robots to go offline, the Buff is not triggered after hitting the Power Rune, or the field prop mechanisms cannot operate normally, the Referee will handle such faults manually through the Referee System. If the fault cannot be handled manually, the Referee will notify both Operators and eject all robots, the round ends immediately and its result is void. After the problem is resolved, the round is restarted.
- During the match, if critical official equipment or props malfunction or are structurally damaged in a way that affects the fairness of the match, and the Head Referee does not confirm and end the round in time, so that a round that should have ended continues and produces a win/loss result, then within 5 minutes after the match ends, once verified by the Chief Referee, the result of that round is void and the round must be replayed.
- If a serious violation that clearly triggers a Loss by forfeit penalty occurs but the Head Referee does not confirm and enforce it in time, then within 5 minutes after the match ends, once verified by the Chief Referee, the result of that round is void and an additional Loss by forfeit penalty is imposed on the violating party.
- During the match, if a situation that may affect the fairness of the match occurs, within 5 minutes after the match ends the Chief Referee will inform both team captains and suspend the result confirmation process, and within the following 60 minutes will verify the situation and inform both team captains of the final handling. Neither team may object to the handling result.

<!-- p.138 -->
## 9 Appeals

Each participating team has 1 Appeal opportunity each in the Regional Competition, the Revival Tournament and the Final Tournament; they cannot be combined. If the Appeal succeeds, the Appeal opportunity is retained; otherwise 1 Appeal opportunity is consumed. When no Appeal opportunity remains, the arbitration committee will no longer accept any Appeal from that team. After an Appeal is accepted, the arbitration committee arbitrates on the Appeal materials and related evidence, and the Chief Referee informs both parties of the Appeal result on behalf of the arbitration committee; the arbitration committee has the final right of interpretation of the Appeal result.

The following cannot be used as grounds for an Appeal:
- Verbal warnings, Yellow Card Warnings and Red Card Warnings in violation penalties.
- The type and procedure of initiating a technical pause.
- "Normal battle damage" occurring on the Referee System onboard unit.

An Appeal cannot be initiated after signing the result confirmation form or more than 5 minutes after a match ends.

<!-- p.139 -->
### 9.1 Appeal Procedure

A participating team that needs to make an Appeal should follow this procedure:

1. **Team submits Appeal.** Within 5 minutes after the match ends (as recorded on the result confirmation form), in the group stage a team may appeal all rounds in the match, and in the knockout stage the team that did not win may appeal the rounds of the match that it did not win. The Appeal is raised by the team captain at the result confirmation desk; confirming the submission starts the Appeal procedure and consumes the Appeal opportunity. After the result confirmation form has been signed, or 5 minutes after the match ends, the arbitration committee no longer accepts Appeals. Appeals are not allowed before or during the match.

   > Note: If the Appeal reason involves the robots of both sides, the arbitration committee has the right to isolate the relevant robots; robots isolated for inspection will be returned no later than together with the Appeal result.

2. **Team fills in the Appeal form and signs to confirm.** After the Appeal form is provided, the appealing team captain must fill in the Appeal form in detail at the result confirmation desk and sign and submit it within 10 minutes. While filling in the Appeal form, in addition to the captain, at most 2 field personnel are allowed to assist. The arbitration committee arbitrates only on the "Appeal reason" part of the Appeal form, which the appealing party may not modify or supplement afterwards. If the form is not signed and submitted within 10 minutes, it is regarded as having no "Appeal reason", the subsequent procedure is skipped, and the Appeal result is regarded as "original match result upheld".

3. **Team collects evidence or defense materials.** If either party needs to collect Appeal materials, it must submit them to the Chief Referee within 30 minutes after the Appeal is accepted, with the time and place of submission agreed in advance, and the Appeal materials must be explained in detail at submission. After the Appeal material submission period expires, the arbitration committee does not accept new materials. If neither party needs to collect Appeal materials, the arbitration committee has already established sufficient evidence, or the Appeal reason filled in by the appealing party cannot be used as grounds for an Appeal, the procedure may proceed directly to the next step.

4. **Appeal result is announced to both parties.** After the arbitration committee reaches a ruling based on the relevant evidence, it notifies both team captains to come to the arbitration room, and the basis of the ruling is shown and the Appeal result announced in this step. Both parties must arrive at the arbitration room within 10 minutes after the arbitration committee's notice. This step allows in-person participation only. Each party may have no more than 3 members present, and the members present may only be official team members or advisors. If either party is absent, the absent party is regarded as having automatically waived participation. If the appealing party's Appeal reason is clearly inconsistent with the facts or is a reason that cannot be used as grounds for an Appeal, the arbitration committee may explain the situation only to the appealing party and uphold the original match result. When the representatives of both parties accept the Appeal result, or the arbitration committee considers that the necessary communication has been completed, the procedure moves to the next step.

5. **Appeal result is confirmed.** The arbitration committee gives the Appeal result on the Appeal form, and 1 of the members of each party in the arbitration room must sign the Appeal form as representative; signing means acknowledging the Appeal result, and neither party may object to the Appeal result afterwards. If the form is not signed within 5 minutes after the Appeal result is given, the arbitration result is regarded as acknowledged. If the appealing party's Appeal reason is clearly inconsistent with the facts or is a reason that cannot be used as grounds for an Appeal, the arbitration committee explains the situation to the appealing party and upholds the original match result; the appealed party does not need to sign and is regarded as having acknowledged the Appeal result.

6. **Continued Appeal.** If a round is replayed because the Appeal arbitration result was "both sides replay", then after the replayed round ends, teams that still have an Appeal opportunity may appeal the replayed round. In this case, if the original appealing party appeals again (called a "Continued Appeal"), because it seriously affects the schedule, the original appealing party's Appeal opportunity is consumed whether or not the Appeal succeeds.

*Figure 9-1 Appeal Flowchart*

### 9.2 Appeal Materials

Each file in the Appeal materials submitted by a participating team must not exceed 500MB, and there must be no more than 10 files.

<!-- p.140 -->
### 9.3 Appeal Results

Appeal results include: original match result upheld, appealed party Loss by forfeit, and both sides replay. After the arbitration committee confirms the Appeal result, neither party may object to it.

> Note:
> - Appeal succeeds: appealed party Loss by forfeit, or both sides replay.
> - Appeal fails: original match result upheld.

If the result announced in the arbitration communication step is both sides replay, but neither side accepts the replay, the Appeal is regarded as failed and the original match result is upheld.

> Note:
> - Where it does not affect the overall schedule, replays are in principle scheduled after all matches of the day end, subject to actual circumstances.
> - The replay procedure is the same as the regular schedule procedure, and both sides must play at the time specified by the RMOC and comply with the relevant regulations.

If the Appealed round affects the win/loss outcome of the match, the match outcome must be re-determined.

**Example: A BO3 match ends 1:2, with Red winning the first round and Blue winning the second and third rounds. After the match, Red appeals the second round and the Appeal result is both sides replay. If Red wins the replayed round, the final match result is 2:0; if Blue wins the replayed round, the final match result is 1:2.**

<!-- p.141 -->
## Appendix 1 Pre-Match Procedure Description

> Note: This season there will be no separate Sentry mapping session.

### Pre-Inspection

Pre-Inspection is an inspection session set before the formal Pre-Match Inspection, intended to help participating teams find and resolve problems with their robots in advance. During Pre-Inspection and adaptive training, the RMOC will do its best to help teams troubleshoot and handle robot faults, but the Pre-Inspection result is not equivalent to the formal match Pre-Match Inspection result; if a robot is found at the formal Pre-Match Inspection not to meet the passing criteria, it still may not take the field.

Unique identifier registration can only be done during Pre-Inspection; after Pre-Inspection ends, only replacement re-registration of robots whose unique identifiers have already been registered is allowed. If a team needs to repair or replace a part that carries a unique identifier, it must apply to the RMOC to report it and re-register and re-mark it. Each team may initiate at most 6 such reports in the same competition region; replacing a part that carries a unique identifier without reporting it causes the robot to lose its eligibility to take the field.

- Non-emergency reporting method: if the team's next match is more than 2 hours away, or it is outside the RMOC's working hours, the team may replace the relevant parts itself and, in [Robot Unique Identifier Re-registration], submit detailed photos of the robot before and after the replacement or a full video of the replacement process, book an inspection time through the same link, and arrive at the second Pre-Match Inspection area at the agreed time, where dedicated RMOC staff will review it. Robots that pass the review will receive their unique identifiers again.
- Emergency reporting method: if the team's next match is less than 2 hours away and it is within the RMOC's working hours, the team should contact the Referee at the second Pre-Match Inspection area to report an emergency repair. After confirmation, RMOC staff will accompany the team to the team preparation area and supervise the whole repair process. In this case, the robot may pass Pre-Match Inspection and take part in this match without all unique identifiers being completed, but after the team's next match ends, the robot must be moved to the second Pre-Match Inspection area for a second review and have all unique identifiers completed.

### Field Prop Training

Prop training provides field props and wooden structures similar to those used in the formal match for participating teams to test with. Passing Pre-Match Inspection is not required before training; teams must make sure their robots' Referee System works properly, and if the on-site Referee System fails, the related time counts toward that team's training time.

**Time and booking:**

Each team must wait in the waiting area 20 minutes in advance; for teams that do not arrive on time, training time is still counted as normal and is not extended. Each team has two training sessions in total, each 30 minutes (including entering and leaving the field). The first session is arranged by the RMOC and the second is booked by the team itself; enter and leave strictly according to the time slots, and do not occupy other teams' training time.

**Personnel and equipment:**

Each team may send at most 12 people into the training area, and entrants must wear safety goggles. The RMOC provides only 2 Operator computers for the video transmission channel; if more robot player-side devices need to be connected, teams may bring their own computers, but these must not be connected to the competition network.

<!-- p.142 -->
**Props, projectiles and safety:**

The RMOC provides only Movable Props for testing and does not provide 17mm or 42mm projectiles; teams must bring their own if testing requires them. When testing with 42mm projectiles, take care to avoid actively hitting the Power Rune. Because of venue limitations, the training area may be affected by ambient light, and teams must adapt on their own. If a team does not obey the on-site Referee or commits other violations, its prop training eligibility will be revoked and it will be asked to leave immediately; in serious cases its adaptive training eligibility is also revoked.

### Adaptive Training

Adaptive training is a debugging and acclimatization opportunity for participating teams before the formal matches. Its main purposes include:
- Becoming familiar with the competition environment and procedures.
- Testing and adjusting robot status and strategy.

Rules for adaptive training:
- The training schedule is tight and mainly for debugging; absent a major official equipment failure, training is not paused by default.
- If the Referee System (onboard unit) is abnormal, the RMOC may grant an official technical pause of at most 2 minutes to handle the fault; the pause duration counts toward the total adaptive training time.
- No team technical pause opportunity is provided during adaptive training.

Rules for the free debugging stage:
- When testing projectile launching, a team may apply to the Referee to borrow a projectile clearing bag and may launch only into the clearing bag.
- During the free debugging stage the match stage status is "Not Started"; teams must adapt to and become familiar with the switching and requirements of the match stages themselves.

Eligibility and stage division:
- Robots that did not pass Pre-Match Inspection on time or that have safety hazards may not take part in adaptive training.
- Robots that failed Pre-Match Inspection because they seriously do not meet the inspection standards are allowed to take part only in the free debugging stage of adaptive training.
- The number of robots taking part in adaptive training must not exceed the maximum robot lineup limit specified for each event.

<!-- p.143 -->
## Appendix 2 Future Rules Planning

To be updated

<!-- p.144 -->
Email: robomaster@dji.com
Forum: https://bbs.robomaster.com
Website: https://www.robomaster.com
Phone: +86 0755-84357613 (Monday to Friday 10:30-19:30)
Address: 13F, Building D1, Chuangzhi Yuncheng, Nanshan District, Shenzhen, Guangdong Province
