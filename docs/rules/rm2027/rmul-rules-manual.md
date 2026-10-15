# RoboMaster 2027 RMUL Rules Manual V1.0.0 (2026-10-15)

Unofficial English translation of the Chinese original. The Chinese PDF governs;
see the [translation index](README.md) for source, checksums and conventions.
`<!-- p.N -->` markers give the physical PDF page.

<!-- p.1 -->
### RoboMaster 2027 RMUL Rules Manual

- V1.0.0
- The 26th National University Student Robotics Competition, RoboMaster 2027
- RoboMaster University League (RMUL)
- Rules Manual
- Compiled by the RoboMaster Organizing Committee
- Released October 2026

<!-- p.2 -->
### Intellectual Property Statement

The RoboMaster Organizing Committee (RMOC, RoboMaster Organizing Committee) encourages and advocates technical innovation and open-sourcing of technology, and respects the intellectual property of participating teams. All intellectual property developed by participating teams during the competition belongs to the teams themselves. The Organizing Committee does not take part in handling intellectual property disputes among members within a team. Participating teams must properly handle the ownership of intellectual property among their own school members, company members and members of other affiliations.

When using the Referee System and competition support materials provided by the Organizing Committee, participating teams must respect the owners of all intellectual property in the original products, and must not reverse engineer, copy, translate or otherwise act in any way that harms the intellectual property of the owners.

Any act that harms the intellectual property of the competition education products provided by the Organizing Committee and host organizations will be pursued by the intellectual property owners in accordance with the law.

For suggestions on open-source materials, see: https://bbs.robomaster.com/article/4820

### Reading Notes

The RoboMaster competition is a robot competition whose purpose is to cultivate young engineering talent. Related documents may involve sensitive terms, names, operations, technologies and other content. Such content does not reflect any technology or action existing in reality, and is not intended to refer to any specific country, organization or individual. This manual is intended to explain the robot competition rules and must not be used for any purpose other than the RoboMaster competition. It should not be regarded as being associated with any real events or entities.

### Field Drawing Legend

| Symbol | Meaning |
| --- | --- |
| Green grid pattern | shared Buff Point |
| Green horizontal-line pattern | one-side Buff Point |
| Yellow crosshatch pattern | shared Restricted Zone |
| Yellow diagonal-line pattern | one-side Restricted Zone |
| Triangle marker above a box labeled "G" | The horizontal plane of the Battlefield ground, which is the lowest plane of the Battlefield |
| Dimension "(100)" | Dimensions are for reference only |

<!-- p.3 -->
### Revision Log

| Date | Version | Revision Record |
| --- | --- | --- |
| 2026.10.15 | V1.0.0 | First release |

<!-- p.4 -->

## Contents

Page numbers in these lists are the printed Chinese manual page numbers;
physical PDF page numbers in the markers are one higher.

| Entry | Printed page |
| --- | --- |
| [Intellectual Property Statement](#intellectual-property-statement) | 1 |
| [Reading Notes](#reading-notes) | 1 |
| [Field Drawing Legend](#field-drawing-legend) | 1 |
| [Revision Log](#revision-log) | 2 |
| [1 Introduction](#1-introduction) | 9 |
| [1.1 About the Competition](#11-about-the-competition) | 9 |
| [1.2 Main Changes in the New Season](#12-main-changes-in-the-new-season) | 10 |
| [1.3 About the Competition Rules Documents](#13-about-the-competition-rules-documents) | 10 |
| [1.4 About Q&A](#14-about-qa) | 11 |
| [2 Important Concepts](#2-important-concepts) | 12 |
| [3 3V3 Match](#3-3v3-match) | 16 |
| [3.1 Robots and Operators](#31-robots-and-operators) | 16 |
| [3.1.1 Heavy Robot](#311-heavy-robot) | 16 |
| [3.1.2 Infantry Robot](#312-infantry-robot) | 18 |
| [3.1.3 Sentry Robot](#313-sentry-robot) | 20 |
| [3.1.4 Custom Terminal](#314-custom-terminal) | 21 |
| [3.2 Competition Field](#32-competition-field) | 21 |
| [3.2.1 Battlefield Overview](#321-battlefield-overview) | 21 |
| [3.2.2 Starting Zone and Supply Zone](#322-starting-zone-and-supply-zone) | 24 |
| [3.2.3 Highland and Tunnel](#323-highland-and-tunnel) | 25 |
| [3.2.4 Control Zone](#324-control-zone) | 27 |
| [3.2.5 Other](#325-other) | 28 |
| [3.3 Match Mechanisms](#33-match-mechanisms) | 29 |
| [3.3.1 HP Deduction and Exceeding-the-Limit Penalty Mechanisms](#331-hp-deduction-and-exceeding-the-limit-penalty-mechanisms) | 29 |
| [3.3.2 HP Recovery and Revival Mechanism](#332-hp-recovery-and-revival-mechanism) | 34 |

<!-- p.5 -->

| Entry | Printed page |
| --- | --- |
| [3.3.3 Economy System](#333-economy-system) | 35 |
| [3.3.4 Control Zones and Control Points Mechanism](#334-control-zones-and-control-points-mechanism) | 36 |
| [3.3.5 Field Buffs Mechanism](#335-field-buffs-mechanism) | 37 |
| [3.3.6 Heavy Robot Special Mechanism](#336-heavy-robot-special-mechanism) | 37 |
| [3.3.7 Competition Format and Victory Conditions](#337-competition-format-and-victory-conditions) | 38 |
| [4 Infantry Match](#4-infantry-match) | 39 |
| [4.1 Robots and Operators](#41-robots-and-operators) | 39 |
| [4.1.1 Infantry Robot](#411-infantry-robot) | 39 |
| [4.1.2 Custom Terminal](#412-custom-terminal) | 40 |
| [4.2 Competition Area](#42-competition-area) | 41 |
| [4.3 Match Mechanisms](#43-match-mechanisms) | 44 |
| [4.3.1 HP Recovery Mechanism](#431-hp-recovery-mechanism) | 44 |
| [4.4 Competition Format and Victory Conditions](#44-competition-format-and-victory-conditions) | 44 |
| [4.4.1 Special Cases in the Infantry Match](#441-special-cases-in-the-infantry-match) | 44 |
| [5 Match Procedure](#5-match-procedure) | 45 |
| [5.1 Pre-Match Inspection](#51-pre-match-inspection) | 46 |
| [5.2 Waiting Area](#52-waiting-area) | 46 |
| [5.3 Setup Period](#53-setup-period) | 47 |
| [5.3.1 Official Technical Timeout](#531-official-technical-timeout) | 48 |
| [5.3.2 Team Technical Timeout](#532-team-technical-timeout) | 49 |
| [5.4 15-Second Referee System Self-Check Period](#54-15-second-referee-system-self-check-period) | 49 |
| [5.5 Five-Second Referee System Self-Check Period](#55-five-second-referee-system-self-check-period) | 49 |
| [5.6 Round Stage](#56-round-stage) | 49 |
| [5.7 End of Match](#57-end-of-match) | 49 |
| [5.8 Result Confirmation](#58-result-confirmation) | 49 |
| [5.9 Exit](#59-exit) | 50 |
| [6 Violations and Penalties](#6-violations-and-penalties) | 51 |

<!-- p.6 -->

| Entry | Printed page |
| --- | --- |
| [6.1 Penalty System](#61-penalty-system) | 51 |
| [6.1.1 Penalty Methods](#611-penalty-methods) | 51 |
| [6.1.2 Penalty Types](#612-penalty-types) | 51 |
| [6.2 Detailed Penalty Rules](#62-detailed-penalty-rules) | 54 |
| [6.2.1 Personnel](#621-personnel) | 54 |
| [6.2.2 Interaction](#622-interaction) | 58 |
| [6.3 Serious Violations](#63-serious-violations) | 60 |
| [7 Abnormal Situations](#7-abnormal-situations) | 61 |
| [8 Appeals](#8-appeals) | 62 |
| [8.1 Appeal Process](#81-appeal-process) | 63 |
| [8.2 Appeal Materials](#82-appeal-materials) | 63 |
| [8.3 Appeal Results](#83-appeal-results) | 64 |
| [Appendix Pre-Match Procedure Description](#appendix-pre-match-procedure-description) | 65 |
| [Pre-Inspection](#pre-inspection) | 65 |
| [Adaptation Training](#adaptation-training) | 65 |

<!-- p.7 -->

## List of Tables

| Entry | Printed page |
| --- | --- |
| Table 2-1 Overview of Important Concepts | 12 |
| Table 3-1 3V3 Match Robot and Operator Lineup | 16 |
| Table 3-2 Key Features of the Heavy Robot | 16 |
| Table 3-3 Key characteristics of the modular 42mm launching mechanism | 18 |
| Table 3-4 Key characteristics of the Infantry Robot | 18 |
| Table 3-5 Key characteristics of the Sentry Robot | 20 |
| Table 3-6 Projectile parameters and usage arrangements | 28 |
| Table 3-7 Effective detection speeds of Armor Modules for different projectile types | 29 |
| Table 3-8 Attack damage HP deduction mechanism | 29 |
| Table 3-9 Penalty mechanism for Initial Launch Speed exceeding the limit | 30 |
| Table 3-10 Penalty mechanism for robot abnormal offline | 33 |
| Table 3-11 Periodic Gold increments for robots | 35 |
| Table 3-12 Exchange rules | 36 |
| Table 4-1 Infantry Match robot and Operator lineup | 39 |
| Table 4-2 Key characteristics of the Infantry Robot | 39 |
| Table 5-1 Failure situations | 48 |
| Table 6-1 Penalty Methods | 51 |
| Table 6-2 Penalty Types | 51 |
| Table 6-3 Collision Violation Penalty Standards | 58 |
| Table 6-4 Types of Serious Violations | 60 |

<!-- p.8 -->

## List of Figures

| Entry | Printed page |
| --- | --- |
| Figure 1-1 Talent Development Philosophy | 9 |
| Figure 3-1 Top-view rendering of the 3V3 Match field | 22 |
| Figure 3-2 Oblique-view rendering of the 3V3 Match field | 22 |
| Figure 3-3 Isometric rendering of the 3V3 Match field | 23 |
| Figure 3-4 Schematic of the 3V3 Match field modules | 23 |
| Figure 3-5 Schematic of the 3V3 Match field dimensions | 24 |
| Figure 3-6 Schematic of the Starting Zone and Supply Zone | 24 |
| Figure 3-7 Schematic of the Starting Zone and Supply Zone Restricted Zone | 25 |
| Figure 3-8 Schematic of the Highland | 25 |
| Figure 3-9 Schematic of the Tunnel | 26 |
| Figure 3-10 Schematic of the Control Zones | 27 |
| Figure 3-11 Field Interaction Module card laying grid | 27 |
| Figure 3-12 Barrel Heat exceeding the limit and cooling mechanism | 31 |
| Figure 3-13 Robot chassis detection and Chassis Power exceeding-the-limit penalty mechanism | 32 |
| Figure 3-14 HP deduction mechanism for Armor Module and Supercapacitor Management Module offline | 33 |
| Figure 3-15 Power-off mechanism for Speed Monitor Module offline | 34 |
| Figure 4-1 Top-view render of the Infantry Match field | 41 |
| Figure 4-2 Oblique-view render of the Infantry Match field | 41 |
| Figure 4-3 Isometric render of the Infantry Match field | 42 |
| Figure 4-4 Top view of the Infantry Match field | 42 |
| Figure 4-5 Dimension diagram of the Infantry Match field | 43 |
| Figure 4-6 Cover diagram | 43 |
| Figure 5-1 Single-match flowchart | 45 |
| Figure 5-2 Pre-Match Inspection flowchart | 46 |
| Figure 5-3 Diagram of the two sides' designated debugging zones | 47 |

<!-- p.9 -->

| Entry | Printed page |
| --- | --- |
| Figure 6-1 Schematic of Battlefield Restricted Zones | 59 |
| Figure 8-1 Appeal Flowchart | 63 |

<!-- p.10 -->
## 1 Introduction

### 1.1 About the Competition

The National University Student Robotics Competition RoboMaster University League (RMUL, RoboMaster University League) is initiated by DJI and hosted by local academic institutions and universities, drawing in surrounding universities to participate. It aims to promote regional exchange of university robotics technology, foster a strong academic atmosphere, and support regional scientific and technological innovation.

RMUL is dedicated to cultivating outstanding young engineers and encourages participating team members to combine what they have learned with practical application and achieve continuous growth through participation.

*Figure 1-1 Talent Development Philosophy*

- Core Values (top of pyramid)
- Sublimate (between Core Values and Essential Qualities)
- Essential Qualities
- Shape (between Essential Qualities and Key Abilities)
- Key Abilities
- Cultivated in real-world scenarios (between Key Abilities and the base)
- Scientific Knowledge | Engineering Experience (base)
- Core Values: Investigate things to extend knowledge, strive for excellence, reflect and examine oneself
  - Develop the habit of deep thinking and cultivate the ability to identify the root cause of problems
  - Pursue excellence driven by high goals and maintain an active, positive mindset
  - Face oneself honestly and reflect on the limits of one's own abilities
- Essential Qualities: Proactive, positive, seeking truth from facts, keeping an open mind
- Key Abilities: Thinking, communication and expression, problem solving, autonomous learning, forward design

The RMUL 2027 season has two challenge events: the 3V3 Match and the Infantry Match.

<!-- p.11 -->
- In the 3V3 Match, each side must independently develop a Heavy Robot, Infantry Robots and a Sentry Robot, and control the robots to launch projectiles to attack the opposing robots within the designated competition field, engaging in tactical confrontation. When the match ends, the side that controls the Battlefield wins.
- In the Infantry Match, each side must independently develop an Infantry Robot, and control the robot to launch projectiles within the designated competition field in a 1V1 confrontation. When the match ends, the side whose Infantry Robot has more remaining HP wins.

### 1.2 Main Changes in the New Season

Compared with RMUL 2026, the main adjustments in RMUL 2027 are as follows:

**3V3 Match**

- Added the Heavy Robot and removed the Hero Robot; the former custom controller and custom client are merged into the Custom Terminal;
- Added the Tunnel and the Workbench, and adjusted the overall layout of the Operator Room;
- Added the Heavy Robot special mechanism and the Field Buffs mechanism, and adjusted the control zone and Control Points mechanism.

**Infantry Match**

Added the HP Recovery mechanism

Removed the Engineer Challenge

### 1.3 About the Competition Rules Documents

The competition rules documents include the Rules Manual, the Participant Manual, the Robot Building Specifications Manual, the communication protocol, and supplements to the above documents. The competition rules documents apply to all participating teams, referees, event staff and other partners.

Outside of competition periods, the Organizing Committee will update the competition rules documents from time to time according to actual circumstances.

The Organizing Committee holds the final right of interpretation of the competition rules documents. During the competition period, only the Chief Referee, on behalf of the Organizing Committee, answers questions about the competition rules documents; any questions about the competition rules documents may only be directed to the Chief Referee.

> Note: For more reference materials on RMU, see the "Rules/Resource Center". This site is built and maintained by the RoboMaster Organizing Committee and centrally provides the official materials needed for participation, aiming to help teams obtain information efficiently. Content coverage:
>
> - Competition rules: Rules Manual, Robot Building Specifications Manual, Participant Manual, communication protocol.
> - Competition products: Referee System (including onboard modules and the competition engine), robot kits & accessories, RM Assistant product details, downloads, purchase & after-sales policies.
> - Technical Assessment: Technical Assessment rules, notes for each stage.
> - Brand promotion: brand promotion asset pack.

<!-- p.12 -->
> - Sponsorship guidance: sponsorship manual, sponsorship guide.
> - Training system: participation guides, course salons, open-source materials.

### 1.4 About Q&A

When participating teams and other related personnel have questions about the competition rules documents, they can raise questions through official channels, and the Organizing Committee will answer them. The specific process is as follows:

1. The questioner fills in the questionnaire and submits the question:

   https://qingflow.com/f/fpckalpss002?exWsld=1SdM5_PB-NwUtnyPn2b8NA

2. The Organizing Committee will post feedback updates at:

   https://qingflow.com/appView/fpckalpss002/shareView/fpckam8gs001

Timeliness notes:

- For questions submitted during the competition period, the Organizing Committee will respond within 1 calendar day;
- For questions submitted during the preparation period, the Organizing Committee will respond within 5 working days.

> Note:
>
> - Competition period: from the registration day of the event to the end of the last competition day of the event.
> - Preparation period: the period outside the competition period.
>
> Note: The competition period and preparation period are calculated separately for different events and event stages.

Q&A answers have the same effect as the competition rules documents. When a Q&A answer differs from the competition rules documents, the most recently released Q&A answer or competition rules document prevails. Each season's Q&A answers apply only to that season.

<!-- p.13 -->
## 2 Important Concepts

This section briefly explains common important concepts related to the competition rules. For details of these concepts, look up the relevant sections by keyword.

**Table 2-1 Overview of Important Concepts**

| Concept | Definition |
| --- | --- |
| **Robots** | |
| Robot | Collective term for the Ground Robots and Auxiliary Equipment that participating teams bring and use in the competition. |
| Ground Robot | A robot that operates independently within the competition field, including the Heavy Robot, Infantry Robot and Sentry Robot. |
| Auxiliary Equipment | Equipment that assists the operation of Ground Robots and does not directly take part in the competition confrontation, including: the Custom Terminal. |
| Robot main states | - **Alive**: the state in which the robot's Referee System Main Controller Module is normally connected to the Referee System server and its HP is not 0.<br>- **Defeated**: the state in which the robot's HP is 0 (causes include: Armor Module being attacked, being hit by collision, Referee System onboard module going offline, Ejection).<br>  - **Ejection**: the state in which the robot has received a Red Card Warning.<br>  - **Temporary activation**: the state in which the robot's chassis and gimbal are temporarily powered on after the robot is Defeated. At this time the robot's launching mechanism is in the power-off state.<br>- **Abnormal offline**: the state in which, during the match, the Referee System Main Controller Module cannot connect to the Referee System server because the robot lost power or for other reasons.<br><br>Note: After a robot is Defeated, the Referee System cuts off the power output to the robot (except the Mini PC). |
| Referee System | The Referee System is an electronic judging system for robot competitions that integrates computing, communication and control. It includes the onboard modules and the competition engine installed on PC hosts (server, referee client, player client), and has functions such as monitoring robot power, projectile launches and damage, and automatically determining the winner according to the competition rules. |
| Multi-robot communication | The mode of interaction in which robots communicate with each other through the Referee System serial port. |
| Chassis | The mechanism that carries the robot's power system and its accessory parts and supports the robot body. |

<!-- p.14 -->
| Concept | Definition |
| --- | --- |
| Chassis Power | The power consumed by the mechanism that, based on rotary motion and relying on ground friction, does work to move or rotate the robot horizontally on a plane. See the definition of Chassis Power in the "Referee System Installation Specifications" section of the "RoboMaster 2027 University Series Robot Building Specifications Manual". |
| Launching mechanism | A mechanism that enables a projectile to leave the robot along a fixed path at a certain initial speed. |
| Launching mechanism locked | If the launching mechanism is locked, it is in the power-off state. |
| Launching mechanism unlocked | If the launching mechanism is unlocked, it is powered on or off depending on its Projectile Allowance. |
| Launch | The act of a robot firing a projectile. "Launch" as mentioned in the later "Competition Mechanisms" section is determined by the launch detected by the Referee System. |
| Initial Launch Speed | The speed value detected by the relevant Referee System module after the projectile has finished accelerating. |
| Barrel Heat | Barrel Heat increases as the robot fires projectiles and is used to limit continuous firing by the robot. |
| Projectile Allowance | The number of projectiles each robot can currently launch. |
| Initial HP | The HP value set for the robot by the Referee System at the start of the match.<br><br>Note: The Referee System rounds to the nearest integer when settling HP. |
| Current HP | The robot's real-time HP value. |
| Max HP | The highest value to which the robot's HP can be recovered. |
| Experience | The value a robot must accumulate to level up, which can be obtained in multiple ways. |
| Invincible | The state in which a robot takes no damage from projectile attacks or collisions. |
| Attack | The act of a robot launching a projectile. |
| Destroy | One side's robot attacks the opposing robot's Armor Module, causing its HP to reach 0. |
| Activation | An Alive robot reaches a Buff Point, and its Field Interaction Module detects a Field Interaction Module card within that zone or other conditions are met. |

<!-- p.15 -->
| Concept | Definition |
| --- | --- |
| Rigid connection | During the match, a mechanical connection formed between robots such that, when one robot moves in any direction, it remains mechanically connected to the other robot. |
| Ramming | An active collision by one side's robot during the match. |
| **Field** | |
| Buff Point | A zone that produces certain special effects after being activated by one side's robot during the match. |
| Restricted Zone | A zone that robots are prohibited from entering. |
| Field props | Component elements of the Battlefield. |
| **Personnel** | |
| Arbitration Committee | Composed of the Chief Referee and other relevant RMOC personnel, responsible for handling matters such as Appeals. |
| Referee | Personnel who maintain order on the field and enforce the competition rules. |
| Chief Referee | The person who holds the final right of interpretation of the competition rules documents during the competition period. |
| Head Referee | The primary referee who maintains order on the field and enforces the competition rules. |
| Chief Inspector | The referee responsible for leading and assigning Pre-Match Inspection work, who holds the final right of interpretation of the Pre-Match Inspection standards. |
| Participating team | A team registered for this season and entered in the registration system. |
| Participant | A person registered for this season and entered in the registration system. |
| Field personnel | Official team members, team advisors and supervising teachers who are registered for this season, entered in the registration system, and permitted to enter the waiting area and the field area.<br><br>Note: Member role divisions differ between events; refer to the "RoboMaster 2027 University League Participant Manual" for specifics. |
| Operator | Field personnel responsible for controlling a robot during the match. |
| Violating party | A participating team that has committed a violation. |
| Violating personnel | A participant who has committed a violation. |

<!-- p.16 -->
| Concept | Definition |
| --- | --- |
| **Match procedure** | |
| Round | A complete match comprising the Setup Period, the Referee System Self-Check Period, the Five-Second Countdown and the Round period. |
| Match | Depending on the Competition Format, a match may include several rounds. |
| Official technical pause | A technical pause initiated by the Head Referee during the Setup Period or the Referee System Self-Check Period. |
| Team technical pause | A technical pause requested by a participating team during the Setup Period. |
| Routine battle damage | A failure of the Referee System onboard module during the inter-round Setup Period or the Round period of a match. |
| **Determination of victory or defeat** | |
| Attack damage | HP deduction caused by projectile attacks on one side's robot.<br><br>Note: HP deduction on one side's robot caused by penalties for violations is counted as attack damage of the opposing side. |
| Non-attack damage | HP deduction caused by impacts on Armor Modules, Referee System modules going offline, and similar causes. |
| Total remaining HP | The total remaining HP of all of a side's Alive robots at the end of each round. |
| Net remaining HP | At the end of each round, the remaining HP of a side's robots minus the remaining HP of the opposing robots. |
| Control Points | A measure of one side's overall control of the Battlefield through occupied positions at the end of each round. |

<!-- p.17 -->
## 3 3V3 Match

In the five-minute time-limited Round, the two sides engage in tactical confrontation by controlling robots within the core competition field, the "Battlefield". The side with the higher Battlefield Control Points causes the opposing side to lose "Control Points". The side that first reduces the opposing side's "Control Points" to zero wins.

### 3.1 Robots and Operators

RoboMaster emphasizes that robots take part as teams, requiring balanced cooperation among robots. For robot building specifications, see the "RoboMaster 2027 University Series Robot Building Specifications Manual".

The robot and Operator lineup is as follows:

**Table 3-1 3V3 Match Robot and Operator Lineup**

| Type | Number | Main lineup quantity | Max reserve quantity | Max Custom Terminals that can be equipped | Max Custom Terminals that can be held in reserve | Operator lineup |
| --- | --- | --- | --- | --- | --- | --- |
| Heavy Robot | 1 | 1 | 1 | 1 | 1 | 1 person per robot |
| Infantry Robot | 3 | 1 | 1 | 1 | 1 | 1 person per robot |
| Sentry Robot | 7 | 1 | 1 | 1 | 1 | 0 persons per robot |

The total number of robots each team can register in an independent competition stage is: 4.

In each match, the minimum lineup for the first round is 2 robots.

Operators may only be filled by field personnel of the current participating team other than supervising teachers.

After each round ends, Operators may be replaced from the field personnel for the match other than supervising teachers.

#### 3.1.1 Heavy Robot

After successfully installing the modular 42mm launching mechanism, the Heavy Robot is the only robot on the Battlefield that can launch 42mm projectiles.

**Table 3-2 Key Features of the Heavy Robot**

| Key feature | Description |
| --- | --- |
| Initial zone | Starting Zone |
| Mode of operation | Unrestricted; up to 1 Remote Controller and 1 Custom Terminal may be configured |

<!-- p.18 -->
| Key Characteristic | Description |
| --- | --- |
| Multi-robot communication | Allowed |
| Launching mechanism | 1 modular 42mm launching mechanism |
| Performance | See the performance table below |
| HP deduction and exceeding-the-limit penalty mechanisms | - Initial Launch Speed exceeding the limit: applicable<br>- Barrel Heat exceeding the limit and cooling: applicable<br>- Chassis Power exceeding the limit: applicable<br>- Attack damage or collision: applicable<br>- Referee System onboard module offline: applicable<br>- Penalty Damage: applicable<br>See "3.3.1 HP Deduction and Exceeding-the-Limit Penalty Mechanisms". |
| HP Recovery and Revival mechanisms | - HP Recovery method: HP can be recovered by activating the Supply Zone.<br>- Revival method: progress-bar Revival.<br>See "3.3.2 HP Recovery and Revival Mechanisms". |
| Projectile loading and supply | During the three-minute Setup Period, 42mm projectiles can be preloaded; the initial Projectile Allowance is 0 |
| Activatable Buff Points | - Control Zone (see "3.3.4 Control Zones and Control Points Mechanism")<br>- Supply Zone Buff Point (see "3.3.2 HP Recovery and Revival Mechanisms")|

Performance sub-table of the above:

| State | Max HP | Chassis Power Limit (W) | Initial Launch Speed Limit (m/s) | Barrel Heat Limit | Barrel Cooling Rate (/s) |
| --- | --- | --- | --- | --- | --- |
| At start | 100 | 50 | - | - | - |
| After the modular 42mm launching mechanism is successfully installed | 450 | 50 | 16.5 | 250 | 66 |

<!-- p.19 -->
**Table 3-3 Key characteristics of the modular 42mm launching mechanism**

| Key Characteristic | Description |
| --- | --- |
| Initial area | Workbench |
| Projectile loading and supply | During the three-minute Setup Period, 42mm projectiles can be preloaded; the initial Projectile Allowance is 0. |

#### 3.1.2 Infantry Robot

Infantry Robots can launch 17mm projectiles.

**Table 3-4 Key characteristics of the Infantry Robot**

| Key Characteristic | Description |
| --- | --- |
| Initial area | Starting Zone |
| Operating mode | Unrestricted; at most 1 Remote Controller and 1 Custom Terminal may be configured |
| Multi-robot communication | Allowed |
| Launching mechanism | 1 17mm launching mechanism |
| Initial Launch Speed limit (m/s) | 25 |
| Performance | After the Setup Period begins, the Operator of the Infantry Robot can select the robot's chassis type (HP Priority or Power Priority) and launching mechanism type (Burst Priority or Cooling Priority). After the Round begins and the chassis and launching mechanism types have been selected, they cannot be changed for the rest of the round. If no chassis or launching mechanism type is selected, then after the Round begins the chassis type defaults to "HP Priority" and the launching mechanism type defaults to "Cooling Priority".<br>**Chassis type**<br>- Power Priority:<br>  - Initial HP / Max HP: 300<br>  - Chassis Power limit: 90W<br>- HP Priority:<br>  - Initial HP / Max HP: 350<br>  - Chassis Power limit: 75W |

<!-- p.20 -->
| Key Characteristic | Description |
| --- | --- |
| Performance (continued) | **Launching mechanism type**<br>- Burst Priority:<br>  - Barrel Heat Limit: 230<br>  - Barrel Cooling Rate: 14/s<br>- Cooling Priority:<br>  - Barrel Heat Limit: 88<br>  - Barrel Cooling Rate: 24/s |
| HP deduction and exceeding-the-limit penalty mechanisms | - Initial Launch Speed exceeding the limit: applicable<br>- Barrel Heat exceeding the limit and cooling: applicable<br>- Chassis Power exceeding the limit: applicable<br>- Attack damage or collision: applicable<br>- Referee System onboard module offline: applicable<br>- Penalty Damage: applicable<br>See "3.3.1 HP Deduction and Exceeding-the-Limit Penalty Mechanisms". |
| HP Recovery and Revival mechanisms | - HP Recovery method: HP can be recovered by activating the Supply Zone.<br>- Revival method: progress-bar Revival.<br>See "3.3.2 HP Recovery and Revival Mechanisms". |
| Projectile loading and supply | During the three-minute Setup Period, 17mm projectiles can be preloaded; the initial Projectile Allowance is 0. |
| Activatable Buff Points | - Control Zone (see "3.3.4 Control Zones and Control Points Mechanism")<br>- Supply Zone Buff Point (see "3.3.2 HP Recovery and Revival Mechanisms") |

<!-- p.21 -->
#### 3.1.3 Sentry Robot

Sentry Robots must operate fully automatically and can launch 17mm projectiles.

**Table 3-5 Key characteristics of the Sentry Robot**

| Key Characteristic | Description |
| --- | --- |
| Initial area | Starting Zone |
| Operating mode | Automatic operation; at most 1 Remote Controller may be configured for debugging |
| Multi-robot communication | Not allowed |
| Launching mechanism | 1 17mm launching mechanism |
| Initial Launch Speed limit (m/s) | 25 |
| Performance | - Initial HP / Max HP: 400<br>- Chassis Power limit: 100W<br>- Barrel Heat Limit: 260<br>- Barrel Cooling Rate: 30/s |
| HP deduction and exceeding-the-limit penalty mechanisms | - Initial Launch Speed exceeding the limit: applicable<br>- Barrel Heat exceeding the limit and cooling: applicable<br>- Chassis Power exceeding the limit: applicable<br>- Attack damage or collision: applicable<br>- Referee System onboard module offline: applicable<br>- Penalty Damage: applicable<br>See "3.3.1 HP Deduction and Exceeding-the-Limit Penalty Mechanisms". |
| HP Recovery and Revival mechanisms | - HP Recovery method: HP can be recovered by activating the Supply Zone.<br>- Revival method: progress-bar Revival.<br>See "3.3.2 HP Recovery and Revival Mechanisms". |
| Projectile loading and supply | - During the three-minute Setup Period, 17mm projectiles can be preloaded. |

<!-- p.22 -->
| Key Characteristic | Description |
| --- | --- |
| Projectile loading and supply (continued) | - During the five-minute Round, the initial Projectile Allowance is 750 and cannot be increased during the round. |
| Activatable Buff Points | - Control Zone (see "3.3.4 Control Zones and Control Points Mechanism")<br>- Supply Zone Buff Point (see "3.3.2 HP Recovery and Revival Mechanisms") |

#### 3.1.4 Custom Terminal

The Custom Terminal (formerly the Custom Controller and Custom Client) is a multi-purpose set of equipment built by participating teams. It is used to monitor robot motion and status, control robot actions, receive match-related information and robot camera video feeds sent by the Referee System's match engine server, and send match-specific interaction commands to the match engine server, in order to expand the possibilities of human-robot interaction.

A typical Custom Terminal may consist of a display device, a computing platform (including memory, controller and processor) and a set of input devices; it may also take an integrated form, for example a handheld tablet with a network port.

> Example: A team builds a Custom Terminal that receives the robot camera video feed and shows it on a self-made display, overlays a self-made UI displayed via an unofficial link, and controls the robot through a matching controller. This team can therefore complete the match without using the official Referee System Operator client or the Remote Controller.

All Custom Terminals in the Operator Room may be wired to each other and communicate, and Custom Terminals may be wired to the match engine server through the RJ45 port provided in the Operator Room to send and receive related content.

A Custom Terminal may receive match information that is displayed on the Referee System Operator client and available to its own side, for example: both sides' HP, its own side's economy, remaining match time, and key match events.

A Custom Terminal may send to the Referee System the match commands supported by the Operator client, for example active commands such as selecting the Performance System before the match and exchanging Projectile Allowance during the match.

### 3.2 Competition Field

#### 3.2.1 Battlefield Overview

> Note:
> - Unless otherwise specified, all dimensional tolerances described in this document are within +/-10%, the angular tolerance of Battlefield structures is within +/-3 degrees, the angular tolerance of field props is within +/-1 degree, the dimensional tolerance of structures smaller than 100mm is within +/-5mm, and the dimension unit in the field drawings is mm. To ensure field stability and safety, detailed dimensions and workmanship of the field may be adjusted during actual construction. For Battlefield elements/dimensions not detailed in the drawings, the actual field prevails.
> - The Battlefield layout is centrally symmetric. Descriptions and illustrations of field modules in this document use the Red side as an example; the Blue side is the same. The field environment is complex, and environmental factors that are not fully symmetric may exist, such as uneven magnetic fields and venue air-conditioning airflow.

<!-- p.23 -->
The core competition field of the 3V3 Match is called the "Battlefield". The Battlefield is an area 12m long and 8m wide. Its interior is a wooden structure, the surface is covered with 2mm-thick PVC floor covering, and some structures have a metal protective layer. Supply Zones and Control Zones are set up within the area.

*Figure 3-1 Top-view rendering of the 3V3 Match field*

*Figure 3-2 Oblique-view rendering of the 3V3 Match field*

<!-- p.24 -->
*Figure 3-3 Isometric rendering of the 3V3 Match field*

*Figure 3-4 Schematic of the 3V3 Match field modules*

- [1] Supply Zone
- [2] Workbench
- [3] Tunnel
- [4] Highland
- [5] Red Highland Control Zone
- [6] Central Control Zone
- [7] Blue Highland Control Zone

<!-- p.25 -->
*Figure 3-5 Schematic of the 3V3 Match field dimensions*

- Overall field: 12000 (length) x 8000 (width), in mm
- Dimensions measured from the field's bottom-left corner: horizontal 2500 (to the left edge of the Red Highland) and 4500 (to the Highland / Central Control Zone boundary); vertical 2500 (to the bottom edge of the Central Control Zone) and 3000 (to the bottom edge of the Red Highland)

#### 3.2.2 Starting Zone and Supply Zone

The Starting Zone is the area where robots are placed before the match officially begins. The Starting Zone also serves as the Supply Zone and has a Workbench. It is an important area for robots to exchange Projectile Allowance, recover HP and install the modular 42mm launching mechanism, and Field Interaction Module cards are laid in it.

*Figure 3-6 Schematic of the Starting Zone and Supply Zone*

- [1] Workbench
- [2] Supply Zone
- Dimensions (mm): Starting Zone 2500 (width) x 2000 (height); Workbench footprint 750 wide (650 between the chamfered corners) x 450 deep (350 between the chamfered corners); Workbench side-view height 400 (above ground G)

<!-- p.26 -->
One side's Supply Zone is a Restricted Zone for the opposing side's robots.

*Figure 3-7 Schematic of the Starting Zone and Supply Zone Restricted Zone*

#### 3.2.3 Highland and Tunnel

*Figure 3-8 Schematic of the Highland*

- [1] Metal plate
- Dimensions (mm), plan view: Highland width 2000; length 4060; Control Zone left edge 400 from the Highland left edge; Control Zone bottom edge 1200 from the Highland bottom edge; 150-wide raised strip along the right edge, 1800 long, starting 900 from the bottom edge; metal plate [1] 350 wide, 825 from the left edge
- Dimensions (mm), side views: Highland deck 200 high with the raised strip a further 200 (total (400) above ground G); other side view: 250, 270 and 800

<!-- p.27 -->
*Figure 3-9 Schematic of the Tunnel*

- [1] Red Tunnel Buff Point
- [2] Blue Tunnel Buff Point

<!-- p.28 -->
#### 3.2.4 Control Zone

The Control Zones are located at the Highlands and the center of the Battlefield, and Field Interaction Module cards are laid in them.

*Figure 3-10 Schematic of the Control Zones*

- [1] Red Highland Control Zone
- [2] Central Control Zone
- [3] Blue Highland Control Zone
- Dimensions (mm): Highland Control Zones 1200 x 1200; Central Control Zone 3000 x 3000

*Figure 3-11 Field Interaction Module card laying grid*

- [1] Field Interaction Module card mounting position
- Detail A dimensions (mm): 92, 28, 28, 112, 70

<!-- p.29 -->
> Note:
> - Field Interaction Module cards are laid at all Battlefield Buff Points, and Field Interaction Module cards may have dead zones.
> - On top of the Field Interaction Module cards in the Control Zones, Supply Zones and Tunnels, an additional layer of floor covering is laid over the floor covering already present on the field.

#### 3.2.5 Other

##### 3.2.5.1 Projectiles

Robots can attack Armor Modules and thereby cause damage by launching projectiles. The parameters and usage arrangements of the projectiles used in the match are as follows:

**Table 3-6 Projectile parameters and usage arrangements**

| Type | Appearance | Color | Size | Mass | Shore Hardness | Material | Usage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 42mm projectile | Similar in shape to a golf ball | White | 42.5mm±0.5mm | 41g±1g | 90±5A | Plastic, TPE | 3V3 Match |
| 17mm projectile | Spherical | Yellow-green | 16.8mm±0.2mm | 3.2g±0.1g | 90±5A | Plastic, TPU | 3V3 Match, Infantry Match |

##### 3.2.5.2 Operator Room

The Operator Room is equipped with the corresponding number of computers, and each computer is equipped with official devices: a display, mouse, keyboard, camera Video Transmitter Module (receiver) and its bracket, and one 1GbE (RJ45) network port. The camera Video Transmitter Module (receiver) bracket is fixed on the desk, and the Operator can operate the camera Video Transmitter Module (receiver) within the bracket's range of movement.

> Note:
> - It is forbidden to remove the camera Video Transmitter Module (receiver) from its bracket; the teams bear the consequences themselves.
> - Robots entering the Battlefield automatically connect to the Operator Room's camera Video Transmitter Module (receiver); camera Video Transmitter Modules (receivers) brought by teams cannot be used. The default state of the Operator Room camera Video Transmitter Module (receiver) joystick is centered, and the default state of its toggle switch is position C.

<!-- p.30 -->
### 3.3 Match Mechanisms

#### 3.3.1 HP Deduction and Exceeding-the-Limit Penalty Mechanisms

##### 3.3.1.1 Attack Damage or Collision

The Armor Modules of Heavy Robots, Infantry Robots and Sentry Robots may have HP deducted when attacked or collided with. The specific mechanism is as follows:

An Armor Module can detect projectile attacks, with a minimum detection interval of 50ms (when a 42mm projectile hits an Armor Module, the detection interval may be extended to at most 200ms).

A projectile must contact the attacked surface of an Armor Module at a certain speed to be effectively detected. The effective detection speed ranges of an Armor Module for different projectile types are shown in the table below:

**Table 3-7 Effective detection speeds of Armor Modules for different projectile types**

| Armor Module | 17mm projectile | 42mm projectile |
| --- | --- | --- |
| Small Armor Module | Greater than 12m/s | Greater than 8m/s |

> Note:
> - In actual matches, because of projectile speed decay and an incidence angle that is not normal to the attacked surface of the Armor Module, the normal speed of a projectile contacting the attacked surface differs from its Initial Launch Speed. Damage detection is based on the normal component of the speed at which the projectile contacts the attacked surface of the Armor Module.
> - When one side's Heavy Robot has not launched a 42mm projectile for 4 consecutive seconds, all armor of the opposing side's robots will block 42mm projectile damage until the Heavy Robot launches a 42mm projectile.
> - The Referee System rounds to an integer when settling HP.

An Armor Module on a robot that is collided with has a probability of being judged as projectile damage, but causing damage to the opponent by collision (including ramming robots and throwing objects) is not allowed.

With no Buffs of any kind, the original damage values are shown in the table below:

**Table 3-8 Attack damage HP deduction mechanism**

| Target \ Damage type | 42mm projectile | 17mm projectile | Collision |
| --- | --- | --- | --- |
| Robot Armor Module | 200 | 20 | 2 |

<!-- p.31 -->
##### 3.3.1.2 Initial Launch Speed Exceeding the Limit

When the Initial Launch Speed of a Heavy Robot, Infantry Robot or Sentry Robot exceeds the limit, the robot's launching mechanism is locked and unlocked after a certain time; the times do not accumulate.

Locking and unlocking caused by the Initial Launch Speed exceeding the limit are independent of locking and unlocking caused by other conditions. Let the robot's Initial Launch Speed limit be V0 (m/s), and let the Initial Launch Speed of a projectile detected by the Referee System be V1 (m/s). The specific lock times are shown in the table below:

**Table 3-9 Penalty mechanism for Initial Launch Speed exceeding the limit**

| 17mm projectile | 42mm projectile | Lock time |
| --- | --- | --- |
| 0 < V1 - V0 < 5 | V0 < V1 ≤ 1.1 * V0 | 15 s |
| 5 ≤ V1 - V0 < 10 | 1.1 * V0 < V1 ≤ 1.2 * V0 | 20 s |
| 10 ≤ V1 - V0 | 1.2 * V0 < V1 | The rest of the round, with no further unlocking |

##### 3.3.1.3 Barrel Heat Exceeding the Limit and Cooling

When the Barrel Heat of a Heavy Robot, Infantry Robot or Sentry Robot exceeds the limit, the robot's launching mechanism is locked. Locking and unlocking caused by Barrel Heat exceeding the limit are independent of locking and unlocking caused by other conditions. The specific mechanism is as follows:

Let the robot's Barrel Heat Limit be Q0 and its current Barrel Heat be Q1. For each 17mm projectile the Referee System detects, the current Barrel Heat Q1 increases by 10 (regardless of the Initial Launch Speed of the 17mm projectile). For each 42mm projectile detected, the current Barrel Heat Q1 increases by 100 (regardless of the Initial Launch Speed of the 42mm projectile). Barrel Heat cooling is settled at a frequency of 10Hz; the cooling value per detection cycle = cooling value per second / 10.

When Q2 > Q1 > Q0, the first-person operation interface video feed of the robot's Operator is disconnected and the launching mechanism is locked; the first-person operation interface returns to normal and the launching mechanism is unlocked only when Q1 = 0.

When Q1 > Q2, the robot's launching mechanism is locked for the rest of the round with no further unlocking.

For a 17mm launching mechanism, Q2 = Q0 + 100;

For a 42mm launching mechanism, Q2 = Q0 + 200.

<!-- p.32 -->
*Figure 3-12 Barrel Heat exceeding the limit and cooling mechanism*

- Start
- Detect one projectile; if the projectile type is 17mm: Q1 = Q1 + 10; otherwise: Q1 = Q1 + 100
- If Q1 ≥ Q2: the robot's launching mechanism is locked for the rest of the round with no further unlocking
- If Q1 > Q0: the robot's launching mechanism is locked, video feed disconnected
- When the 100ms detection cycle arrives: Q1 = Q1 - cooling value per second / 10
- If Q1 ≤ 0: Q1 = 0, the robot's launching mechanism is unlocked, video feed returns to normal

<!-- p.33 -->
##### 3.3.1.4 Chassis Power Exceeding the Limit

The Referee System continuously monitors robot Chassis Power; the robot chassis must operate within the power limit. When the Chassis Power of a Heavy Robot, Infantry Robot or Sentry Robot exceeds the limit, the robot has Buffer Energy deducted. When the Buffer Energy is exhausted and Chassis Power still exceeds the limit, the chassis is powered off for 5 seconds. The settlement frequency of the Referee System's Chassis Power detection is 10Hz.

Let Z be the Buffer Energy, Q be the Buffer Energy limit, which is 60J, Pr be the instantaneous chassis output power, and Pl be the limit power.

*Figure 3-13 Robot chassis detection and Chassis Power exceeding-the-limit penalty mechanism*

- Start: Buffer Energy Z = Q
- When the 100ms detection cycle arrives: calculate work consumption, Z = Z - (Pr - Pl) x 0.1
- If Z ≤ 0: Z = 0, chassis powered off for 5 s
- Otherwise, if Z > Q: Z = Q

##### 3.3.1.5 Referee System Onboard Module Offline

Teams install the Referee System modules corresponding to the robot as required by the *RoboMaster 2027 University Series Robot Building Specifications Manual*, and must keep each Referee System module stably connected to the server during the match. The Referee System server checks the connection status of each module at a frequency of 2Hz.

###### 3.3.1.5.1 Abnormal Offline

During the match, if the robot's Main Controller Module goes offline, it enters the "abnormal offline" state and can reconnect to the match.

<!-- p.34 -->
**Table 3-10 Penalty mechanism for robot abnormal offline**

| Robot type | Handling during offline |
| --- | --- |
| Heavy Robot, Infantry Robot, Sentry Robot | - Launching mechanism, gimbal and chassis are powered off, and 5% of Max HP is deducted per second until HP reaches 0 |
| Heavy Robot, Infantry Robot, Sentry Robot | - Field Interaction Module becomes invalid |
| Heavy Robot, Infantry Robot, Sentry Robot | - The robot no longer detects damage caused by collisions and projectile hits, or HP deduction from module offline |
| Heavy Robot, Infantry Robot, Sentry Robot | - Revival progress bar no longer increases |
| Heavy Robot, Infantry Robot, Sentry Robot | - Multi-robot communication is disconnected |

###### 3.3.1.5.2 Armor Module or Supercapacitor Management Module Offline

If a Heavy Robot, Infantry Robot or Sentry Robot has an Armor Module or Supercapacitor Management Module go offline because of its own design, structure or similar problems, the robot will have HP deducted.

*Figure 3-14 HP deduction mechanism for Armor Module and Supercapacitor Management Module offline*

- Start
- When the 500ms detection cycle arrives: check whether any Armor Module or Supercapacitor Management Module is offline
- If yes: count the number N of offline Armor Modules and Supercapacitor Management Modules
- Calculate the HP deduction value: Value = 4*N
- Deduct robot HP

<!-- p.35 -->
###### 3.3.1.5.3 Speed Monitor Module Offline

If the 17mm Speed Monitor Module or 42mm Speed Monitor Module installed on a Heavy Robot, Infantry Robot or Sentry Robot goes offline, the 17mm or 42mm launching mechanism of that robot is powered off immediately.

*Figure 3-15 Power-off mechanism for Speed Monitor Module offline*

- Start
- Decision: 500ms detection period elapsed? NO: return to this check. YES: continue.
- Decision: Speed Monitor Module offline? NO: no additional handling, return to the 500ms check. YES: the corresponding 17/42mm launching mechanism is locked.
- Decision: Speed Monitor Module reconnected to the server? NO: keep waiting. YES: the corresponding 17/42mm launching mechanism is unlocked, then return to the 500ms check.

##### 3.3.1.6 Penalty Damage

When a Heavy Robot, Infantry Robot or Sentry Robot receives a Yellow Card or Red Card Warning or other penalties, HP may be deducted from that robot. See "6.1 Penalty System".

#### 3.3.2 HP Recovery and Revival Mechanism

Except when abnormally offline or Ejected, Ground Robots can recover HP and revive.

<!-- p.36 -->
##### 3.3.2.1 HP Recovery Mechanism

Heavy Robots, Infantry Robots and Sentry Robots can activate their own Supply Zone. Activating their own Supply Zone recovers HP at a rate of 25% of Max HP per second.

##### 3.3.2.2 Revival Mechanism

When a robot is Defeated, its Barrel Heat is reset to 0 and its Buffer Energy is reset to the Buffer Energy limit. A Defeated robot can revive automatically, and must complete a revival progress bar to do so. During automatic revival, the progress increases by 1 point per second. The revival progress bar length required for a robot's first Defeat is 5, and the length required increases by 5 after each subsequent Defeat of the same robot.

After a robot revives, its HP is restored to 20% of Max HP, it is temporarily Invincible for 30 seconds, and it enters the "Weakened" state. A robot in the "Weakened" state has the following characteristics:

- The launching mechanism is locked.
- It cannot activate Control Zones.

After that, when it detects the Field Interaction Module card of its own Supply Zone, the "Weakened" and Invincible states are removed.

#### 3.3.3 Economy System

At the start of the match, each side receives a certain amount of initial Gold. As the match progresses, both sides periodically receive Gold. Gold can only be used to exchange for Projectile Allowance. The specific Gold increments are shown in the table below:

**Table 3-11 Periodic Gold increments for robots**

| Match countdown | Red Side | Blue Side |
| --- | --- | --- |
| 04:59 | 200 (initial) | 200 (initial) |
| 03:59 | 200 | 200 |
| 02:59 | 200 | 200 |
| 01:59 | 300 | 300 |
| 00:59 | 300 | 300 |

The first time the difference in Control Points between the two sides reaches 200 or 400, the side with fewer Control Points receives 200 Gold. In each round, a side can obtain at most 400 Gold through this mechanism. For the Control Points mechanism, see "3.3.4 Control Zones and Control Points Mechanism".

<!-- p.37 -->
**Table 3-12 Exchange rules**

| Exchange item | Exchange rate |
| --- | --- |
| 17mm projectile | 10 Gold/10 projectiles |
| 42mm projectile | 10 Gold/1 projectile |

For each projectile a robot fires, the Projectile Allowance of the corresponding projectile type is reduced by 1.

In the following special cases, all armor of the opposing side's robots will block 42mm projectile damage, until the Heavy Robot is alive again and its Projectile Allowance is greater than 0:

1. 3 seconds after the Heavy Robot changes from alive to Defeated or abnormally offline.
2. The Heavy Robot fires a 42mm projectile when its Projectile Allowance is 0 (overfiring).
3. After the Heavy Robot fires its 3rd 42mm projectile after being Defeated.
4. The communication packet loss rate between the modular 42mm launching mechanism and the Referee System Main Controller Module is greater than or equal to 5%.

> Note: 17mm projectile damage is not blocked.

When a Heavy Robot or Infantry Robot activates the Supply Zone, its Operator can exchange 42mm and 17mm Projectile Allowance separately through the Referee System Client.

#### 3.3.4 Control Zones and Control Points Mechanism

There are 3 Control Zones on the field: the Red Highland Control Zone, the Blue Highland Control Zone and the Central Control Zone. The Control Zone mechanism takes effect after the match starts.

##### 3.3.4.1 Control Zone Mechanism

At the start of the match, all three Control Zones are neutral.

Each side has its own independent "occupation progress" counter for each Control Zone. The counter has a maximum of 5 and a minimum of 0. When a side's "occupation progress" for a Control Zone reaches 5, that side "controls" the Control Zone; when a side's "occupation progress" for a Control Zone drops to 0, that side loses control of it. When neither side controls a Control Zone, the Control Zone is neutral.

When a Control Zone is activated by robots of only one side and the other side's occupation progress is 0, that side's occupation progress for the Control Zone increases by 1 per second. When a Control Zone is activated by robots of only one side and the other side's occupation progress is not 0, the other side's occupation progress for the Control Zone decreases by 1 per second.

When both sides activate the same Control Zone, changes in occupation progress are paused until only one side's robots remain activating the Control Zone.

When neither side activates a non-neutral Control Zone, both sides' occupation progress for that Control Zone decreases by 1 per second.

<!-- p.38 -->
##### 3.3.4.2 Control Points Mechanism

At the start of the match, each side has 600 Control Points:

- For each Control Zone a side controls, the opposing side loses 1 Control Point per second.
- Each time a robot of a side is Defeated, that side loses 10 Control Points.

When the difference in Control Points between the two sides is greater than or equal to 200, the revival progress bar required by the side with fewer Control Points is reduced by 33%, and its HP Recovery rate at the Supply Zone increases to 33%/s;

When the difference in Control Points between the two sides is greater than or equal to 400, the revival progress bar required by the side with fewer Control Points is reduced by 50%, and its HP Recovery rate at the Supply Zone increases to 50%/s.

#### 3.3.5 Field Buffs Mechanism

##### 3.3.5.1 Highland Buff Point and Highland Control Zone Mechanism

Robots of both sides can activate the Highland Buff Points of both sides, and multiple robots of the same side can activate a Highland Buff Point at the same time.

A robot that activates a Highland Buff Point gains a 25% defense Buff.

The Highland Buff Point is also a Highland Control Zone. For the Control Zone mechanism, see "3.3.4 Control Zones and Control Points Mechanism".

##### 3.3.5.2 Tunnel Buff Point Mechanism

Robots can activate their own Tunnel Buff Points. Multiple robots of the same side can activate a Tunnel Buff Point at the same time.

When the same robot detects the Field Interaction Module cards of both Tunnel Buff Points on one side's half of the field within 3 seconds, and detects no other Field Interaction Module card in between, it gains a 1.5x Barrel Cooling Rate Buff, lasting 60s.

##### 3.3.5.3 Control Zone Buff Point Mechanism

Robots of both sides can activate Control Zones, and multiple robots of the same side can activate a Control Zone at the same time. For the specific effects of activation, see "3.3.4 Control Zones and Control Points Mechanism".

> Note: After a robot no longer detects the Field Interaction Module card of a Buff Point, the activated state expires after 2 seconds.

#### 3.3.6 Heavy Robot Special Mechanism

At the start of the match, the Heavy Robot's performance attributes are low. It must install the modular 42mm launching mechanism and fire one 42mm projectile that is correctly recognized by the Referee System before it gains improved performance attributes. For performance attributes, see "3.1.1 Heavy Robot".

A Heavy Robot can perform the following operations, but only at the Workbench:

<!-- p.39 -->
Separate into sub-robots or multiple subsystems connected by flexible cables, or merge from the above states.

Install or remove the modular 42mm launching mechanism.

A Heavy Robot that has not successfully completed installation of the modular 42mm launching mechanism is Invincible when it activates its own Supply Zone.

#### 3.3.7 Competition Format and Victory Conditions

The 3V3 Match consists of a group round-robin stage and a knockout stage. The group round-robin uses a BO2 Competition Format, and the knockout stage uses a BO3 Competition Format.

The Victory Conditions for a single round are as follows:

1. When one side's Control Points reach 0, the round ends immediately, and the side whose Control Points are not 0 wins.
2. When the round time runs out and neither side's Control Points are 0, the side with higher Control Points wins.
3. When the round time runs out, both sides' Control Points are equal and not 0, the side whose whole team has dealt higher attack damage wins.
4. When the round time runs out, both sides' Control Points are equal and not 0, and the whole teams' attack damage is the same, the side whose robots have higher total remaining HP wins.
5. If the above conditions cannot determine a winner, the round is declared a draw. If a draw occurs in the knockout stage, an additional round is played immediately until a winner is decided.

<!-- p.40 -->
## 4 Infantry Match

During the two-minute Round, the robots of the two teams will engage in shooting combat in the core competition area, the "Battlefield". Destroying the opposing robot wins the match.

### 4.1 Robots and Operators

The robot and Operator lineup is as follows:

**Table 4-1 Infantry Match robot and Operator lineup**

| Type | Number | Main lineup quantity | Max reserve quantity | Max Custom Terminals that can be equipped | Max Custom Terminals that can be kept in reserve | Operator lineup |
| --- | --- | --- | --- | --- | --- | --- |
| Infantry Robot | 3 | 1 | 0 | 1 | 0 | 1 person/robot |

> Note:
> - Operators can only be filled by on-site team members of the current participating team other than the advisor.
> - After each round ends, the Operator can be replaced by an on-site team member other than the advisor from this match's on-site team members.

#### 4.1.1 Infantry Robot

The Infantry Robot can fire 17mm projectiles.

**Table 4-2 Key characteristics of the Infantry Robot**

| Key characteristic | Description |
| --- | --- |
| Initial zone | Starting Zone |
| Operating mode | Unlimited, with at most 1 Remote Controller and 1 Custom Terminal configured |
| Multi-robot communication | Allowed |
| Launching mechanism | 1 17mm launching mechanism |
| Initial Launch Speed limit (m/s) | 25 |
| Performance | - Initial HP/Max HP is 200<br>- Barrel Heat Limit is 80 |

<!-- p.41 -->
| Key characteristic | Description |
| --- | --- |
| Performance (continued) | - Barrel Cooling Rate is 12/s<br>- Chassis Power limit is 120W |
| HP deduction and limit-exceeding penalty mechanism | - Initial Launch Speed exceeding the limit: applies<br>- Barrel Heat exceeding the limit and cooling: applies<br>- Chassis Power exceeding the limit: applies<br>- Attack damage or collision: applies<br>- Referee System onboard module offline: applies<br>- Penalty Damage: applies<br>See "3.3.1 HP Deduction and Limit-Exceeding Penalty Mechanism". |
| HP Recovery and Revival mechanism | Not applicable |
| Projectile loading and resupply | - During the two-minute Setup Period, 17mm projectiles can be preloaded.<br>- During the two-minute Round, the initial Projectile Allowance is 200 projectiles and cannot be increased during the round. |

#### 4.1.2 Custom Terminal

The Custom Terminal (formerly the Custom Controller and Custom Client) is a multi-purpose set of equipment built by the participating team, used to monitor robot motion and status, control robot actions, receive match-related information and robot camera video feeds sent by the Referee System match engine server, and send match-specific interaction commands to the match engine server, in order to expand the possibilities of human-robot interaction.

A typical Custom Terminal can consist of a display device, a computing platform (including memory, controller and processor) and a set of input devices; it can also take an integrated form, for example a handheld tablet device with a network port.

**Example: A team built a Custom Terminal that can receive the robot's camera video feed and present it on a self-made display, overlay a self-made UI shown through an unofficial link, and control the robot through a matching controller. As a result, the team can complete the match without using the official Referee System Client and Remote Controller.**

All Custom Terminals in the Operator Room can be connected to each other by wire and communicate, and Custom Terminals can connect by wire to the match engine server through the RJ45 port provided in the Operator Room and send and receive related content.

A Custom Terminal can receive match information that is displayed on the Referee System Client and available to its own side, for example: both sides' HP, own-side economy, remaining match time and key match events.

A Custom Terminal can send to the Referee System the match commands supported by the Client, for example active commands such as selecting a Performance System before the match and exchanging Projectile Allowance during the match

<!-- p.42 -->
and so on.

### 4.2 Competition Area

The core competition area of the Infantry Match is called the "Battlefield". The Battlefield is an area 5m long and 5m wide, containing each side's Starting Zone and the covers (obstacles). For projectiles and the Operator Room, see "3.2.5.1 Projectiles" and "3.2.5.2 Operator Room".

*Figure 4-1 Top-view render of the Infantry Match field*

*Figure 4-2 Oblique-view render of the Infantry Match field*

<!-- p.43 -->
*Figure 4-3 Isometric render of the Infantry Match field*

*Figure 4-4 Top view of the Infantry Match field*

- [1] Red Starting Zone
- [2] Cover
- [3] Blue Starting Zone

<!-- p.44 -->
*Figure 4-5 Dimension diagram of the Infantry Match field*

- Field: 5000 x 5000
- Starting Zone: 1000 x 1000
- Cover position: 2066 horizontal and 2050 vertical, measured from the field corner of the Red Starting Zone; covers angled at 45 degrees; 1200 perpendicular distance between the two covers

*Figure 4-6 Cover diagram*

- Top view: 1200 x 420; datum G
- Side profile: 400 overall; 125 (offset between the top edge and the step); 800 (length of the straight bottom edge)

<!-- p.45 -->
### 4.3 Match Mechanisms

See the content related to Infantry Robots in "3.3.1 HP Deduction and Limit-Exceeding Penalty Mechanism".

#### 4.3.1 HP Recovery Mechanism

In the Infantry Match, each time a robot deals projectile damage to the opponent, it recovers HP equal to 50% of the damage dealt.

### 4.4 Competition Format and Victory Conditions

The Infantry Match is divided into two parts: a group round-robin stage and a knockout stage. The group round-robin uses a BO2 Competition Format, and the knockout stage uses a BO3 Competition Format.

The Victory Conditions for a single round are as follows:

1. When one side's robot HP drops to 0, the round ends immediately and the opposing side wins.
2. When the round time runs out and neither side's HP is 0, the side whose robot has higher remaining HP wins.
3. When the round time runs out, neither side's HP is 0, and the robots' remaining HP is the same, the side whose HP was first deducted later wins.
4. When the round time runs out, neither side's HP is 0, and both are at full HP, the side with the higher total number of projectiles fired wins.
5. When the round time runs out, neither side's HP is 0, both are at full HP and the total number of projectiles fired is the same, the side that first fired a projectile earlier wins.
6. If the above conditions cannot determine a winner, the round is declared a draw.

#### 4.4.1 Special Cases in the Infantry Match

1. If in the knockout stage the two teams' score is 0:1 or 1:0, the team that won 1 round advances.
2. If in the knockout stage the two teams' score is 0:0 or 1:1, compare the two teams' average per-round net remaining HP advantage over the matches completed so far; the team with the higher average per-round net remaining HP advantage advances.

> Note:
> - If the Regional Competition's Infantry Match schedule contains two group rounds, only the average per-round net remaining HP advantage over the matches completed from the start of the second group round up to now is compared for the two teams.
> - If the two teams' average per-round net remaining HP advantage is the same and a winner cannot be determined, in order to keep the subsequent schedule running smoothly, RMOC will determine the winner by an on-site draw.

<!-- p.46 -->
## 5 Match Procedure

*Figure 5-1 Single-match flowchart*

Flowchart steps (left) and their annotations (right):

- Teams wait for Pre-Match Inspection in the staging area. Annotations: (1) The team correctly installs the Referee System. (2) Check whether the robots comply with the Rules Manual requirements.
- Decision: Passed Pre-Match Inspection? NO: return to waiting in the staging area. YES: continue. Annotations: (1) Arrive at the inspection area at the time designated before the match for Pre-Match Inspection. (2) The team captain signs to confirm the inspection result.
- Arrive at the waiting area. Annotations: (1) Arrive at the waiting area at the time designated before the match. (2) Follow the waiting-area order. (3) The team waits to enter the field for the match.
- Arrive at the match-field waiting zone.
- Setup Period begins. Annotations: (1) Power on the robots and check that the robots are normal. (2) Connect to the Referee System server. (3) Obtain initial projectiles. (4) Operators enter the Operator Room. (5) In the last 30 seconds, all robots must be powered on; team members must leave the Battlefield. (6) Special situations, technical timeout.
- 15-Second Referee System Self-Check Period & Five-Second Countdown. Annotations: (1) Referee System self-check. (2) After the Referee System self-check ends, enter the match countdown.
- Match start to end. Annotations: (1) Robots of both sides engage in shooting combat in the Battlefield. (2) Determine the winner according to the match rules.
- Decision: Is there a next round? YES: return to the start of the Setup Period. NO: continue.
- One match ends. Annotations: (1) Robots are powered off and leave the Battlefield. (2) Within 5 minutes, the team captain signs to confirm the result or files an Appeal.
- The team leaves the field and arrives at the projectile-return area. Annotation: Collect projectiles, PASS cards, etc.
- Return to the staging area. Annotation: Return to the staging area.

<!-- p.47 -->
### 5.1 Pre-Match Inspection

> Note:
> - The inspection results of pre-inspection and adaptive training are for reference only and are not the basis for passing inspection in official matches.
> - The inspection result of an official match is valid only for that match.
> - Passing inspection only proves that the robot met the inspection pass criteria at the time of inspection; the team must itself ensure that the robot always meets the requirements of the Robot Building Specifications Manual. During inspection, all functions of the robot must be proactively demonstrated to the inspectors.

To ensure that robots built by teams meet the requirements of the *RoboMaster 2027 University Series Robot Building Specifications Manual*, teams in the 3V3 Match and the Infantry Match must arrive at the inspection area for Pre-Match Inspection 60 minutes and 40 minutes in advance, respectively. The inspection procedure is as follows:

*Figure 5-2 Pre-Match Inspection flowchart*

- Team members bring the robots into the inspection area (start of inspection). Annotation: At most 2 team members per robot are responsible for bringing it into the inspection area, and another 1 team member or the advisor is responsible for organizing and cooperating with the Pre-Match Inspection. Without approval from the Chief Inspector, other team members may not enter the inspection area. If the participating robots have not arrived at the inspection area, no one from the team may enter the inspection area.
- Robots undergo inspection. Annotation: Staff mark the robots to be inspected (forms of marking include but are not limited to a PASS card, writing a timestamp to the Referee System onboard module, Qingliu lineup registration, etc.) and change the marking according to which inspection items pass; only robots with a complete mark are eligible to enter the waiting area and the field area. The team must modify robots that fail inspection until they meet the inspection requirements to pass. At the same time, the team must also check and confirm that the Referee System onboard module structure, functions, etc. are normal.
- The team captain signs to confirm the inspection result. Annotation: After the team captain signs to confirm, no objection to the inspection result may be raised.

In the RMUL 3V3 Match, each team may borrow the Referee System of at most 1 reserve robot.

### 5.2 Waiting Area

After Pre-Match Inspection is complete, teams must arrive at the waiting area at least 10 minutes before the start of each match. In the 3V3 Match, each team can have at most 10 team members on site; in the Infantry Match, each team can have at most 4 team members on site. One of the team members on site must wear a "Captain" armband and perform the captain's duties. After a team enters the waiting area, if a robot needs repair, approval from a referee is required. A robot can leave the waiting area for repair only after waiting-area staff tear off the PASS card on the robot. After repair, the robot must return to the inspection area for inspection again, and may return to the waiting area only after passing Pre-Match Inspection again. If this causes a delay and the robot does not arrive at the waiting area on time, the robot cannot take part in the match, and the team bears the consequences.

<!-- p.48 -->
> Note: "Captain" armband: Any team member on site wearing a "Captain" armband performs the captain's duties during the match. The captain must manage the team's match procedure, confirm results, submit team technical timeout requests, file Appeals, etc.

After the team is sent from the waiting area to the field, it enters the field's waiting zone and places the robots there. After the referee approves, the team carries the robots to the Battlefield entrance and stands by. According to the match procedure, the referee opens the door and guides team members onto the field. The Setup Period countdown starts at the same time the door is opened.

### 5.3 Setup Period

The Setup Period of the 3V3 Match is 3 minutes, and the Setup Period of the Infantry Match is 2 minutes. During the Setup Period, team members on site must place the robots in their respective initial zones, check whether the robots' Referee System is operating normally, preload projectiles into the robots, and debug the modular 42mm launching mechanism. Team members on site may repair robots or replace their equivalent parts, but must meet the requirements of the specification documents. In the 3V3 Match, team members on site must debug robots in their own side's designated debugging zone (shown in the figure below); in the Infantry Match, team members on site can only debug robots inside the Starting Zone, and each team allows only one team member on site to leave the designated debugging zone to debug.

*Figure 5-3 Diagram of the two sides' designated debugging zones*

- [1] Red designated debugging zone
- [2] Blue designated debugging zone

> Note:
> - Equivalent parts: standard modules or parts of the same material, form and function, such as motors of the same model or self-made friction wheel modules.

<!-- p.49 -->
> Note (continued):
> The main structure that carries the robot body cannot be replaced by an equivalent part, such as the robot chassis.
> - If the "equivalent parts" include a Referee System onboard module, the team must itself ensure that the Referee System onboard module can be used normally (including version number, sensor calibration, installation standards, etc.). When an anomaly occurs in a Referee System onboard module among the "equivalent parts", an official technical timeout will not be triggered.

When 1 minute 30 seconds remain in the Setup Period, Operators are advised to enter the Operator Room to finish debugging the keyboard and mouse and to check and confirm that robot control and the official equipment are operating normally. If the official equipment cannot operate normally, team members on site must raise it before 15 seconds remain in the Setup Period; otherwise the referee will not grant a technical timeout. Except for the Operators corresponding to the robots on the field, other team members on site may not enter the Operator Room.

When 30 seconds remain in the Setup Period, all robots in the Battlefield must be powered on; robots that are not powered on must be moved out of the Battlefield, and personnel in the Battlefield leave in an orderly manner. After the Setup Period ends, team members on site must place the Sentry Robot's Remote Controller in the designated area at the Battlefield entrance.

#### 5.3.1 Official Technical Timeout

During the Setup Period, when the Referee System or Operator Room equipment etc. fails (see the table below for failure situations) or a robot needs a temporary Pre-Match Inspection, the Head Referee can initiate an official technical timeout and pause the countdown. The time at which a pause is initiated is at the Head Referee's discretion.

During an official technical timeout, team members on site must cooperate with the referee's requirements to resolve failures related to the Referee System or official equipment, and may not repair other failures. If the Referee System fails and needs replacement, replacement must follow the time limits for replacing the Referee System onboard module in the *RoboMaster 2027 University Series Robot Building Specifications Manual*. After the failure related to the Referee System or official equipment is resolved and the Head Referee resumes the countdown, team members on site must follow the standards of the three-minute Setup Period and leave the Battlefield at the specified times.

**Table 5-1 Failure situations**

| Item | Description |
| --- | --- |
| 1 | An official device in the Operator Room fails, or key match props in the Battlefield suffer structural damage or functional abnormality. |
| 2 | During the first round's Setup Period, a Referee System onboard module fails, for example: Armor Module damaged, Speed Monitor Module offline, etc. |
| 3 | During the Setup Period, the Referee System Main Controller cannot connect to the server, or the robot cannot properly transmit video back to the Operator Room. |
| 4 | Other situations that the Head Referee determines require an official technical timeout. |

Because it cannot be determined whether a failure is caused by the Referee System onboard module itself, by a defect in the participating robot's circuit or structural design, or by robot combat in earlier matches, apart from the situation in item 3 above, ordinary battle damage does not trigger an official technical timeout, and the referee will provide a spare Referee System onboard module. The team may request a "team technical timeout" to repair the robot.

If, after referee investigation, the failures described in items 2 and 3 above are caused by the team, the referee will explain the situation and end the official technical timeout.

<!-- p.50 -->
#### 5.3.2 Team Technical Timeout

If the robot's mechanical structure, software system, or the keyboard, mouse and other equipment brought into the Operator Room fail, the team may request a "team technical timeout" only before the Setup Period's fifteen-second countdown, with the team captain applying to a referee in the Battlefield or Operator Room and stating the technical timeout duration and reason for the request. Once a team technical timeout request has been initiated and conveyed to the Head Referee, that technical timeout cannot be cancelled or modified.

After a team technical timeout is confirmed by the Head Referee, regardless of which side initiated it, the referee will notify both teams at the same time.

After the Head Referee confirms both teams are ready, the technical timeout may be ended early. Even if the team has not entered the Battlefield or the technical timeout ends early, the opportunity consumed is still the opportunity corresponding to the duration declared by the team when it applied.

To ensure the subsequent schedule runs on time, both sides together can initiate only 1 team technical timeout in the same Setup Period, on a first-come, first-served basis. The post-match result confirmation form will record whether any technical timeout opportunity was consumed during the match.

In the 3V3 Match and the Infantry Match, each team has 2 two-minute technical timeout opportunities.

### 5.4 15-Second Referee System Self-Check Period

After the Setup Period ends, the match enters the 15-Second Referee System Self-Check Period. During the self-check, the Referee System server automatically checks the Referee System Client connection status, the robots' Referee System onboard module status and the field prop status, and resets all robots' HP to ensure all robots are at full HP at the start of the match.

### 5.5 Five-Second Referee System Self-Check Period

After the 15-Second Referee System Self-Check Period ends, the match enters the Five-Second Countdown. At this time, the Referee System Client will not respond to robot control commands (including from Custom Terminals); after the countdown ends, the Referee System Client resumes responding to robot control commands and the match starts immediately.

### 5.6 Round Stage

Robots engage in shooting combat in the core competition area (Battlefield).

### 5.7 End of Match

A round ends when the round time runs out or when one team triggers a Victory Condition early. A match ends when the winner of the match is decided or all rounds are finished.

### 5.8 Result Confirmation

During a match, the referee records on the result confirmation form the main penalties of each round, key settlement information at the end of the round, win/loss results, and team technical timeout opportunity usage, etc.

<!-- p.51 -->
The captain must sign to confirm the match result within 5 minutes after a match ends. If the captain neither signs to confirm the result nor files an Appeal within 5 minutes, the match result is deemed confirmed.

### 5.9 Exit

After a match ends, 3V3 Match teams must power off the robots, move them out of the Battlefield, and go to the projectile-return area to return projectiles. In the projectile-return area, the team must follow staff guidance, proactively return all armbands and PASS cards, empty the projectiles loaded in the robots, and proactively return all projectiles used in the match. Infantry Match teams must carry out the above exit-related operations inside the field.

<!-- p.52 -->
## 6 Violations and Penalties

To ensure fair play and maintain competition discipline, participating teams, participants and robots must strictly follow the competition rules. In case of a violation, the referees will impose the corresponding penalty for the violation. Some penalties issued for violations before the match officially starts will be enforced after the match officially starts. Major penalties during a match and all appeals will be made public.

The penalty for each violation in this chapter is determined by the Head Referee based on the actual situation of the match. If a situation arises during a match that affects fairness but is not covered by the detailed penalty rules or the serious violations, the Head Referee will make a ruling based on the actual situation.

> Note: If one side's action directly causes the other side to commit a violation, it is not regarded as a violation by the other side, but the other side must promptly stop the violation.

### 6.1 Penalty System

#### 6.1.1 Penalty Methods

During the competition, the Referee System or the referees will impose penalties on participants and robots that do not comply with the competition rules. The penalty methods are as follows:

**Table 6-1 Penalty Methods**

| Penalty Method | Description |
| --- | --- |
| Automatic Referee System penalty | In "3.3.1 HP Deduction and Exceeding-the-Limit Penalty Mechanism", all penalties other than attack damage or collisions and Penalty Damage are automatic Referee System penalties. |
| Manual Referee System penalty | Penalties issued by referees operating the Referee System server for robot violations. |
| Manual referee penalty | Applies to scenarios where the Referee System cannot be used to issue penalties, such as verbal warnings and disqualification from the competition. |

#### 6.1.2 Penalty Types

The types of manual penalties during the match are shown in the following table:

**Table 6-2 Penalty Types**

| Penalty Type | Description |
| --- | --- |
| Verbal Warning | Verbal warning |
| Yellow Card Warning | - One-side Yellow Card: |
<!-- p.53 -->
|  | &nbsp;&nbsp;&nbsp;&nbsp;- If the violating robot is a Sentry Robot, its chassis power is cut for 2 s, and the operator interfaces of the other robots are obscured for 2 s.<br>&nbsp;&nbsp;&nbsp;&nbsp;- If the violating robot is not a Sentry Robot, its operator interface is obscured for 5 s, and the operator interfaces of the other robots are obscured for 2 s.<br>&nbsp;&nbsp;&nbsp;&nbsp;- The Referee System automatically deducts 15% of the violating robot's current Max HP, and the other surviving robots each have 5% of their current Max HP deducted. If a robot receives another Yellow Card Warning within 30 s after each Yellow Card Warning, the percentage of current Max HP deducted is 2 times that of the previous one, and the other surviving robots each have 5% of their current Max HP deducted.<br>&nbsp;&nbsp;&nbsp;&nbsp;- In each round, when a robot accumulates 3 Yellow Card Warnings, it will simultaneously receive a Red Card Warning.<br>- Two-side Yellow Card:<br>The operator interfaces of all Operators are obscured for 2 s, and all robots have 5% of their Max HP deducted. This is not counted toward the accumulated Yellow Card count of any single robot.<br><br>> Note:<br>> - If Yellow Card Warnings are received consecutively, the operator interface obscuring times are added together, and the 30 s timer is reset.<br>> - If a robot's remaining HP is less than or equal to the HP to be deducted by the penalty, its HP is reduced to 1.<br>> - The chassis power-cut and operator interface obscuring durations caused by violation penalties are independent of the match mechanisms and are not added to them. |
| Red Card Warning (Ejection) | - Ejecting a robot:<br>&nbsp;&nbsp;&nbsp;&nbsp;- If the robot is ejected before the 15-Second Referee System Self-Check Period, the violating robot is not allowed to take the field and must be removed from the battlefield, and no other robot is allowed to substitute for it in all rounds of that match.<br>&nbsp;&nbsp;&nbsp;&nbsp;- If the robot is ejected during the 15-Second Referee System Self-Check Period, the Red Card Warning will be issued after the match starts.<br>&nbsp;&nbsp;&nbsp;&nbsp;- If a robot is ejected during the match, its HP immediately becomes 0, its video transmission feed is disconnected, multi-robot communication is disconnected, and it cannot be revived.<br>- Ejecting a field team member: The referees require the ejected field team member to leave the match area immediately, and no other field team member is allowed to substitute for them in all rounds of that match. The robot controlled by the ejected Operator is ejected for that round, is not allowed to take the field in all rounds of that match, and no robot may substitute for it. |
<!-- p.54 -->
| Loss by forfeit | - If a Loss by forfeit penalty is issued for one round (hereinafter "round forfeit"), the detailed rules are as follows:<br><br>**3V3 Match:**<br><br>&nbsp;&nbsp;&nbsp;&nbsp;- If the forfeit penalty is issued before the five-minute Round (including the Setup Period and the 15-Second Referee System Self-Check Period), the violating side's control is 0, the violating side's remaining robots have full HP, and the other side's control and robot HP are full. The round time is regarded as 300 s.<br>&nbsp;&nbsp;&nbsp;&nbsp;- If the forfeit penalty is issued during the five-minute Round, the round ends immediately, the violating side's control is 0, the violating side's remaining robots' HP is that at the end of the round, and the other side's control and robot HP are the control and HP at the end of the round. The round time is the actual elapsed match time when the forfeit is issued.<br>&nbsp;&nbsp;&nbsp;&nbsp;- If the forfeit penalty is issued after the five-minute Round, the violating side's control is 0, the violating side's remaining robots' HP is that at the end of the round, and the other side's control and robot HP are the control and HP at the end of the round. The round time is the actual elapsed match time when the forfeit is issued.<br><br>**Infantry Match:**<br><br>&nbsp;&nbsp;&nbsp;&nbsp;- If the forfeit penalty is issued before the two-minute Round (including the Setup Period and the 15-Second Referee System Self-Check Period), the violating side's robot HP is 0 and the other side's robot HP is full. The round time is regarded as 120 s.<br>&nbsp;&nbsp;&nbsp;&nbsp;- If the forfeit penalty is issued during the two-minute Round, the round ends immediately, and both sides' robot HP is that at the end of the round. The round time is the actual elapsed match time when the forfeit is issued.<br>&nbsp;&nbsp;&nbsp;&nbsp;- If the forfeit penalty is issued after the two-minute Round, both sides' robot HP is that at the end of the round. The round time is the actual elapsed match time when the forfeit is issued.<br><br>- If a Loss by forfeit penalty is issued for one match (hereinafter "match forfeit"), the forfeit penalty is issued for all rounds of that match, and the HP settlement for each round follows the descriptions above. |
| Disqualification from awards | - The participant is disqualified from awards.<br>- The participating team is disqualified from awards. |
| Disqualification from the competition | - The participant is disqualified from the competition and from awards.<br>- The participating team is disqualified from the competition and from awards. The team's results this season are retained as a reference for the advancement of other teams. |

<!-- p.55 -->
### 6.2 Detailed Penalty Rules

This section describes the detailed violation penalty rules. Rules numbered R# explicitly state the rules that participating teams, participants and participating robots must follow.

#### 6.2.1 Personnel

##### 6.2.1.1 General Rules

**R1** Participating teams must meet the requirements of the *RoboMaster 2027 University League Participant Manual*.

Violation penalty: Disqualification from the competition for the violating side, at most.

**R2** Participants and their actions must not interfere with the normal operation of official equipment, the normal running of the competition process, or the normal work of RMOC personnel.

Violation penalty: Disqualification from the competition for the violating side, at most.

**R3** Participating teams must not set up their own wireless devices or use walkie-talkies in competition-related areas (including but not limited to the preparation area, inspection area, waiting area and match area).

Violation penalty: Disqualification from the competition for the violating side, at most.

**R4** Participating teams must not damage official equipment (including but not limited to equipment located in the match area, waiting area, preparation area and inspection area).

Violation penalty: Disqualification from the competition for the violating side, at most, and the violating side must compensate at full price.

**R5** Except for field team members who enter the waiting area and match area as required by the match, other participants must not enter the waiting area and match area without special reasons.

Violation penalty: Disqualification from the competition for the violating person, at most.

**R6** Field team members who have entered the waiting area or match area as required by the match must not leave the waiting area or match area, or change field team members, without the referee's approval.

Violation penalty: The violating person is not allowed to enter the waiting area and match area for this match, and is disqualified from the competition at most.

**R7** Except for projectiles preloaded in the inspection area, participating teams must not bring projectiles for the match into the waiting area or match area on their own.

Violation penalty: Projectiles are confiscated and a verbal warning is given. If the warning is ineffective, the violating person is disqualified from the competition, at most.

**R8** After a match ends, field team members must immediately power off the robots and move them off the field, and empty the projectiles inside the robots in the projectile return area.

Violation penalty: The violating robot will be detained in the projectile return area until its projectiles are emptied.

**R9** After a match ends, field team members must return all projectiles used in the match in the projectile return area.

Violation penalty: Projectiles are confiscated, and the violating person's eligibility to enter the field in subsequent matches in the current competition zone is cancelled. The violating person is disqualified from the competition, at most.

<!-- p.56 -->
**R10** Except in emergencies, participating teams must arrive at the inspection area at the time specified before the start of each match (see "5.1 Pre-Match Inspection" for details) for the pre-match inspection, and the team must arrive at the waiting area and be ready 10 minutes before the start of each match.

Violation penalty: Match forfeit, at most.

**R11** Without the referee's permission, after a robot passes inspection and until the end of the match, it must not be powered on for debugging or repaired in areas outside the battlefield.

Violation penalty: Match forfeit, at most.

**R12** The identity and number of personnel of each team entering designated areas such as the preparation area, inspection area, waiting area and match area must meet the requirements.

Violation penalty: Disqualification from the competition for the violating side, at most.

**R13** One field team member must wear a "Captain" armband, and the armband must not be obscured.

Violation penalty: Disqualification from the competition for the violating person, at most.

**R14** Without the referee's permission, field team members who have entered the match area must not communicate with the outside world in any way.

Violation penalty: Verbal Warning. If the warning is ineffective, disqualification of the violating person from the competition, at most.

**R15** Field team members must not use official equipment power supplies in the match area to power their own equipment, but may bring their own power supplies.

Violation penalty: Verbal Warning. If the warning is ineffective, a Red Card Warning is given to the violating person. Disqualification of the violating side from the competition, at most.

**R16** Except in special circumstances, field team members are prohibited from entering the match area wearing slippers.

Violation penalty: A Red Card Warning to the violating person, at most.

**R17** During the appeal process, the appealing side must provide valid evidence or the relevant clauses of the normative documents on which it relies.

Violation penalty: Disqualification from the competition for the violating person, at most.

**R18** The captain has management responsibilities and must ensure the following during preparation and participation:

- Participating robots must pass the review of complete robots and the usage regulations for open-source robots;
- Team advisors, reserve team members and other persons not eligible for awards must not commit violations during participation;
- Other violations are stopped promptly.

Violation penalty: The captain's management responsibility is determined according to the violation, and the violating person is disqualified from the competition, at most.

##### 6.2.1.2 Battlefield Rules

**R19** Field team members must wear protective goggles when entering the battlefield.

Violation penalty: The violating person is ejected from the battlefield.

**R20** During an official technical pause, field team members must not repair faults other than those of Referee System related modules.

Violation penalty: Verbal Warning. If the warning is ineffective, a Red Card Warning is issued to the violating person.

<!-- p.57 -->
**R21** After the Setup Period ends, field team members must return to the designated area outside the battlefield. During the match, field team members must not leave this area without the referee's permission.

Violation penalty: Verbal Warning. If the warning is ineffective, a Red Card Warning is issued to the violating person.

**R22** After the Setup Period ends, field team members must place the debugging Remote Controller of the Sentry Robot at the battlefield entrance, and must not use the Remote Controller to debug the Sentry Robot after the Five-Second Countdown begins.

Violation penalty: If before the five-minute Round, a Verbal Warning, and if the warning is ineffective, a Red Card Warning is issued to the violating robot; if during the five-minute Round, a Red Card Warning is issued to the violating robot.

**R23** After the Five-Second Countdown begins, field team members must not operate the Remote Controllers corresponding to robots on the field that are outside the Operator Room.

Violation penalty: A Red Card Warning is issued to the violating robot, and round forfeit at most.

**R24** Field team members must ensure that their own robots operate safely and do not cause injury to any person or equipment on the field.

Violation penalty: The violating side bears the corresponding responsibility.

##### 6.2.1.3 Operator Room Rules

**R25** Except for the Operators corresponding to the robots on the field, other field team members must not enter the Operator Room.

Violation penalty: Verbal Warning. If the warning is ineffective, a Red Card Warning is issued to the violating person.

**R26** Without the referee's permission, during the 15-Second Referee System Self-Check Period and the Round, Operators must be inside the corresponding Operator Room operating the control devices for the corresponding robots, and must not change positions after the Setup Period ends.

Violation penalty: Verbal Warning. If the warning is ineffective, a Red Card Warning is issued to the violating person.

**R27** During the match, each Operator may be equipped with at most 1 Remote Controller and 1 Custom Terminal.

Violation penalty: Verbal Warning. If the warning is ineffective, a Red Card Warning is issued to the violating person.

**R28** Using personal earphones or computers in the Operator Room is prohibited (except Custom Terminals).

Violation penalty: Verbal Warning. If the warning is ineffective, round forfeit.

**R29** Each operating device in the Operator Room provides at most 1 RJ45 network port, which can only be connected to a Custom Terminal.

Violation penalty: Verbal warning and prohibition of the violating device. If the device is affected, disqualification of the violating side from the competition, at most.

##### 6.2.1.4 Robots

**R30** Robots and related equipment taking the field must pass the pre-match inspection.

Violation penalty: Round forfeit.

**R31** At the start of a match, robots must meet the minimum lineup requirement for taking the field.

<!-- p.58 -->
Violation penalty: Match forfeit.

**R32** Robots must comply with the requirements of the *RoboMaster 2027 University Series Robot Building Specifications Manual*.

Violation penalty: Disqualification from the competition for the violating side, at most.

> Note:
> - RMOC will conduct random spot checks on robots from time to time.
> - If a robot is reported as not complying with the robot building specifications, the reporter must provide corresponding evidence.
> - During the match, if the installation of a Speed Monitor Module does not meet the requirements, the module is regarded as offline.

**R33** While waiting in the waiting area, participants must not take robots out of the waiting area without permission.

Violation penalty: Verbal Warning. If the warning is ineffective, a Red Card Warning is issued to the violating person and robot, and the violating person is disqualified from the competition, at most.

**R34** Robots must not have or exhibit safety hazards, including but not limited to short circuits, crashes, smoking, open flames, parts falling to the ground and gas cylinder explosions; if a safety hazard exists or appears, participants must cooperate with the referees in carrying out the corresponding operations.

Violation penalty: Before the field is cleared, field team members must resolve the safety issue as required by the referees, otherwise the violating robot is not allowed to take the field. If it occurs during the match, a Verbal Warning is given, and if the warning is ineffective, a Red Card Warning is issued to the violating person or the violating robot. If the safety hazard is serious, the Head Referee handles it according to "8 Abnormal Situations".

**R35** No robot may continuously launch projectiles outside the battlefield.

Violation penalty: Verbal Warning. If the warning is ineffective, a Red Card Warning is issued to the violating robot.

**R36** During the Setup Period and the 15-Second Referee System Self-Check Period, robots on the battlefield must not leave their corresponding starting areas.

Violation penalty: A Red Card Warning to the violating robot, at most.

**R37** During the Setup Period, if projectiles need to be launched, they must be launched into the projectile-clearing bag provided by the referees.

Violation penalty: A Red Card Warning to the violating person and the violating robot, at most.

**R38** During the match, a robot must not disassemble into sub-robots or multiple subsystems connected by flexible cables, and must not actively throw or launch its own parts.

Violation penalty: A Red Card Warning is issued to the violating robot.

**R39** Subsystems or individual units into which a Heavy Robot has been disassembled must not leave the Workbench.

Violation penalty: A Red Card Warning to the violating robot, at most.

**R40** During the match, no surviving robot may use its own structures to obscure any of its own Armor Modules, nor deform beyond the maximum extended size.

Violation penalty: A warning is issued to the violating side based on subjective intent. If the obscuring is active, a Yellow Card Warning is issued and a verbal warning is given when the violation occurs; if the verbal warning is ineffective, a Red Card Warning is issued. If the obscuring is passive, one Yellow Card Warning is issued when the violation occurs.

<!-- p.59 -->
**R41** During the Setup Period, replaced modules or parts of a robot must meet the "equivalent parts" requirements; see "5.3 Setup Period" for details.

Violation penalty: A Red Card Warning to the violating robot, at most.

#### 6.2.2 Interaction

##### 6.2.2.1 Robot Interaction

**R42** A robot must not use any of its own structures to ram the opposing robot. If a Defeated robot blocks a critical movement path, it may be pushed slowly out of the way.

> Note: In a collision between Ground Robots, the violating robot is the one the referee judges to be the active party.

Violation penalty: A warning is issued to the violating robot according to subjective intent and the severity of the collision.

**Table 6-3 Collision Violation Penalty Standards**

| Violation Level | Description |
| --- | --- |
| Yellow Card Warning | - Actively causing a head-on, high-speed collision<br>- Actively pushing so that the opposing robot moves noticeably<br>- Actively pushing the opposing robot to hinder its normal movement |
| Red Card Warning | - Actively causing a head-on, high-speed, repeated or violent collision<br>- Actively pushing so that the opposing robot moves a considerable distance<br>- Actively pushing the opposing robot to seriously hinder its normal movement |

If a collision causes serious consequences for the opposing robot or affects the fairness of the match, in the next round of the same competition stage, the violating robot (by robot number only) is not allowed to take the field, and no other robot is allowed to substitute for it.

**R43** A robot must not, through active interference, blocking, ramming or similar actions, cause any of its own structures to become entangled with the opposing robot.

Violation penalty: Starting from when the entanglement can be determined, warnings are issued to the violating robot according to the duration of the violation. A first Yellow Card Warning is issued when the violation exceeds 10 s, followed by one Yellow Card Warning every 20 s until the violating robot is ejected. Regardless of whether the violating robot is surviving, when the violation duration exceeds 90 s, round forfeit at most is imposed according to the subjective intent of the violating side's actions.

**R44** A robot must not use any contact-based means to interfere with the opposing robot's HP Recovery.

Violation penalty: A Yellow Card Warning is issued to the violating robot.

<!-- p.60 -->
##### 6.2.2.2 Robot Interaction with Field Props

To ensure fair competition and that robots on the battlefield can effectively obtain Buffs or supplies, supply restricted zones are set up on the battlefield; that is, one side's Supply Zone is a supply restricted zone for the other side's robots. A Restricted Zone requires that one side's or both sides' robots must not enter, as shown in the figure.

*Figure 6-1 Schematic of Battlefield Restricted Zones*

- [1] Supply restricted zone

**R45** A robot must not enter a supply restricted zone.

Violation penalty: Warnings are issued to the violating side according to the dwell time and the impact of the violation. A first Yellow Card Warning is issued when the violation exceeds 3 s, followed by one Yellow Card Warning every 10 s until the robot is Defeated or abnormally offline. If staying in the Restricted Zone causes serious damage to the opposing robot, a Red Card Warning is issued to the violating robot.

**R46** Wireless debuggers and Movable Props used in the match must not be brought onto the field. During the match, robots may only use the official dedicated projectiles and Movable Props provided by RMOC on the field.

Violation penalty: Disqualification from the competition for the violating side, at most.

**R47** During the match, robots must not damage field props or projectiles, nor affect the normal function of field props.

Violation penalty: Disqualification from the competition for the violating side, at most.

<!-- p.61 -->
### 6.3 Serious Violations

If any of the following behaviors occurs during the competition, it will be judged a serious violation. For serious violations, RMOC will disqualify the violating side from the competition at most. If the behavior violates local laws and regulations, RMOC will cooperate with the relevant authorities in pursuing the legal liability of the offender.

**Table 6-4 Types of Serious Violations**

| Item | Type |
| --- | --- |
| 1 | Maliciously damaging the field, props or other official equipment, or the robots, equipment, etc. of other participating teams. |
| 2 | Falsification, impersonation or other dishonest participation behavior. |
| 3 | Modifying or damaging the Referee System, or using technical means to interfere with any detection function of the Referee System. |
| 4 | Situations that do not comply with the normative documents and are judged by the Chief Referee to be serious violations. |
| 5 | Other behaviors that hinder the competition, such as disobeying penalties, not cooperating with inspections, deliberate delay, disrupting order, abandoning or boycotting the match without cause. |
| 6 | Passive play, manipulating the match, and similar behaviors. |
| 7 | Giving, or illegally soliciting or accepting, property to or from others in order to obtain improper competition results or seek improper benefits. |
| 8 | Uncivilized or immoral words and conduct such as slander, abuse, improper gestures, malicious heckling and maliciously throwing objects. |
| 9 | Publishing, spreading or disseminating to the media untrue or irresponsible statements. |
| 10 | Deliberately attacking or ramming others, or committing acts that endanger one's own or others' safety. |
| 11 | Carrying dangerous or prohibited items. |
| 12 | Other behaviors that violate the spirit of the competition and are judged to be serious violations. |
| 13 | Other words and conduct that go against the core socialist values, violate sports ethics, violate public order and good morals, violate the competition style and discipline, cause adverse social impact, or violate laws and regulations. |

<!-- p.62 -->
## 7 Abnormal Situations

> Note: There is a certain delay in the referees' manual penalties and in the handling of abnormal situations. If there is a significant impact on the match result, the Chief Referee will determine the final handling result based on the actual situation.

If any of the following abnormal situations occurs, it will be handled in the corresponding manner, and neither team may raise an objection. The handling methods are as follows:

- When a serious safety hazard or abnormal situation occurs, for example: battery combustion, venue power outage, high-pressure gas cylinder explosion or a collision of personnel on the field, after the Head Referee discovers and confirms it, the Head Referee will notify both Operators and eject all robots through the Referee System. The result of that round is void, and the round restarts after the hazard or abnormality is cleared. RMOC will prioritize handling the safety issue and will try to protect the robots as far as possible, but cannot guarantee that the robots will not be affected at all. Any loss or impact caused by the safety handling is borne by the participating team itself.
- During the match, if non-critical props on the battlefield are damaged, for example damage to the floor adhesive, in a way that does not affect the fairness of the match, the match proceeds normally.
- During the match, if a robot's Light Indicator effect is abnormal or similar, the match proceeds normally.
- During the match, if a critical prop on the match field has a logic fault or structural fault, for example abnormal on-site network causing robots to go offline or the field prop mechanism being unable to operate normally, the referees will handle such faults manually through the Referee System. If the fault cannot be handled manually, the referees will notify both Operators and eject all robots, that round ends immediately, and the match result is void. After the problem is cleared, the match restarts.
- During the match, if the function abnormality or structural damage of a critical prop on the match field affects the fairness of the match, and the Head Referee fails to confirm and end the match in time, so that a match that should have ended continues and a win/loss result occurs, then within 5 minutes after the end of the match, after verification by the Chief Referee, that round's result is void and the round must be replayed.
- If a serious violation clearly triggers a penalty but the Head Referee fails to confirm and enforce it in time, then within 5 minutes after the end of the match, after verification by the Chief Referee, that round's result is void, and an additional Loss by forfeit penalty is imposed on the violating side.
- During the match, if a situation arises that may affect the fairness of the match, within 5 minutes after the end of the match the Chief Referee will inform both team captains of the situation and suspend the score confirmation process, and within 60 minutes thereafter will verify it and inform both team captains of the final handling method. Neither side may raise an objection to the handling result.

<!-- p.63 -->
## 8 Appeals

Each participating team has 1 appeal opportunity at each stop and in each event of RMUL 2027, which cannot be accumulated. If the appeal succeeds, the appeal opportunity is retained; otherwise 1 appeal opportunity is consumed. When there is no appeal opportunity left, the Arbitration Committee will no longer accept any appeal from that participating team. After accepting an appeal, the Arbitration Committee will arbitrate on the appeal materials and relevant evidence, and the Chief Referee, on behalf of the Arbitration Committee, will inform both sides of the appeal result. The Arbitration Committee has the final right of interpretation of the appeal result.

The following cannot be used as grounds for appeal:

- Verbal Warnings, Yellow Card Warnings and Red Card Warnings in violation penalties.
- The type and process of initiating a technical pause.
- "Normal combat losses" appearing on the Referee System onboard end.

After signing the score confirmation sheet, or more than 5 minutes after a match ends, an appeal cannot be initiated.

<!-- p.64 -->
### 8.1 Appeal Process

A participating team that needs to appeal should follow the process below:

**Figure 8-1 Appeal Flowchart**

- Participating team submits an appeal
  - Within 5 minutes after the end of the match (based on the time recorded on the score confirmation sheet), the participating teams of a group stage may submit appeals for all rounds of that match, and the participating teams of an elimination stage may submit appeals for the rounds of that match that they did not win. When submitting an appeal, the team captain submits it at the score confirmation location, and confirms that the representative initiates the appeal process, that is, consumes the appeal opportunity. After the score confirmation sheet has been signed or 5 minutes after the end of the match, the Arbitration Committee will no longer accept appeals. Appeals are not allowed before or during a match.
  - Note: If the appeal reason involves both sides' robots, the Arbitration Committee has the right to isolate the relevant robots for testing, and the robots isolated for testing will be returned at the latest together with the appeal result.
- Participating team fills in the appeal form and signs to confirm
  - After the appeal is submitted, the appealing team captain must fill in the appeal form in detail at the score confirmation location within 10 minutes and sign to submit it. When filling in the appeal form, at most 2 field team members besides the captain are allowed to assist. The Arbitration Committee will arbitrate only on the "Appeal Reason" section of the appeal form, and the appealing side may not modify or supplement it afterwards. If it is not signed and submitted within 10 minutes, it is regarded as having no "Appeal Reason", the subsequent process is skipped, and the appeal result is regarded as "Original match result maintained".
- Participating team collects evidence or defense materials
  - If either side needs to collect appeal materials, it must submit the materials to the Chief Referee within 30 minutes after the appeal is accepted, and arrange the time and place for submission in advance. When submitting, the appeal materials must be explained in detail. Once the submission period for appeal materials has passed, the Arbitration Committee will not accept new materials. If neither side needs to collect appeal materials, or the Arbitration Committee has verified sufficient evidence, or the appeal reason filled in by the appealing side cannot be used as grounds for appeal, it may proceed directly to the next step.
- Appeal result notified to both sides
  - After the Arbitration Committee arbitrates and makes a ruling based on the relevant evidence, it notifies both team captains to come to the arbitration room, and in this step presents the basis for the ruling and informs them of the appeal result. Within 10 minutes after the Arbitration Committee's notification, both sides must arrive at the arbitration room. Only up to 3 members of each side may be present, and they can only be official team members or advisors. This step is only open to participants. If either side is absent, the absent side is regarded as automatically abandoning participation. If the appeal reason of the appealing side clearly does not match the facts or uses a reason that cannot be used as grounds for appeal, the Arbitration Committee may explain the situation only to the appealing side and then maintain the original match result. When both side representatives have no need to collect appeal materials, or the Arbitration Committee considers the necessary communication complete, proceed to the next step.
- Confirm appeal result
  - The Arbitration Committee will give the appeal result on the appeal form, and one member of each side present in the arbitration room must sign on the appeal form as the representative. Signing means acknowledging the appeal result, and neither side may raise an objection to the appeal result afterwards. If the representative does not sign on the appeal form within 5 minutes after the appeal result is given, it is regarded as acknowledging the arbitration result. If the appeal reason of the appealing side clearly does not match the facts or uses a reason that cannot be used as grounds for appeal, the Arbitration Committee may explain the situation to the appealing side and then maintain the original match result, and the appealed side does not need to sign and is regarded as acknowledging the appeal result.
- Continue appeal
  - If a round is a replay resulting from the appeal arbitration result of "both sides replay", after the replayed round ends, a team that still has an appeal opportunity may appeal again against the replayed round. In this case, if the original appealing side appeals again (called "continued appeal"), since this would seriously affect the schedule, the appeal opportunity of the original appealing side will be consumed regardless of whether the appeal succeeds.

### 8.2 Appeal Materials

Each appeal material file submitted by a participating team must not exceed 500 MB in size, and the number of files must not exceed 10.

<!-- p.65 -->
### 8.3 Appeal Results

Appeal results include: original match result maintained, appealed side forfeits, and both sides replay. After the Arbitration Committee confirms the appeal result, neither side may raise an objection to the appeal result.

> Note:
> - Appeal succeeds: the appealed side forfeits, or both sides replay.
> - Appeal fails: the original match result is maintained.

If the Arbitration Committee's communication step informs both sides of a replay but neither side accepts the replay, the appeal is regarded as failed and the original match result is maintained.

> Note:
> - Provided the overall schedule is not affected, the replay will in principle be scheduled after all matches of that day end, subject to the actual situation.
> - The replay procedure is consistent with that of regular matches, and both sides must play according to the time specified by RMOC and comply with the relevant regulations.

If the appealed round affects the win/loss relationship of the match, the match's win/loss must be re-determined.

**Example: The result of a BO3 match is 1:2, the first round was won by Red, and the second and third rounds were won by Blue. After the match ends, Red appeals the second round and the appeal result is: both sides replay. If Red wins the replayed round, the final match result is 2:0; if Blue wins the replayed round, the final match result is 1:2.**

<!-- p.66 -->
## Appendix Pre-Match Procedure Description

### Pre-Inspection

The pre-inspection is an inspection step set up before the formal inspection, intended to help participating teams find and resolve robot problems in advance. RMOC will do its best to help participating teams troubleshoot and handle robot faults during the pre-inspection and adaptation training, but the pre-inspection result is not equivalent to the formal match inspection result; if a robot is found at the formal inspection not to meet the inspection pass standards, it still cannot take the field to participate.

Robot carrying limits for pre-inspection:

- 3V3 Match: each team may bring at most 4 robots for pre-inspection.
- Infantry Match: in each event, each team may bring at most 2 robots for pre-inspection.

### Adaptation Training

Adaptation training is a debugging and adaptation opportunity for participating teams before the formal match. Its main purposes include:

- Becoming familiar with the match environment and process.
- Testing and adjusting robot status and strategy.

**Adaptation training duration and opportunities:**

- 3V3 Match: total duration 15 minutes, divided into 1 round and free debugging time.
- Infantry Match: total duration 10 minutes, divided into 1 round and free debugging time. Teams participating in both the 3V3 Match and the Infantry Match may only participate in the 3V3 Match adaptation training.

**Adaptation training rules:**

- The training schedule is tight and focused on debugging; by default, training is not paused unless there is a major official equipment fault.
- If the Referee System (onboard end) is abnormal, RMOC may grant an official technical pause of up to 2 minutes to handle the fault; this pause duration counts toward the total adaptation training time.
- No team technical pauses are provided to participating teams during adaptation training.

**Free debugging stage rules:**

- When conducting projectile launch tests, participating teams may apply to the referees to borrow a projectile-clearing bag and may only launch into the projectile-clearing bag.
- The match stage status during the free debugging stage is "Not started"; participating teams must adapt to and become familiar with the switching and requirements of the match stages on their own.

<!-- p.67 -->
**Eligibility and stage division:**

- Robots that did not pass inspection on time or have safety hazards may not participate in adaptation training.
- Robots that failed inspection due to serious non-compliance with inspection standards may only participate in the free debugging stage of adaptation training.
- The number of robots participating in adaptation training must not exceed the maximum robot lineup limit specified for each event.

<!-- p.68 -->
Contact: Email: robomaster@dji.com; Forum: https://bbs.robomaster.com; Official website: https://www.robomaster.com; Phone: +86 0755-84357613 (Monday to Friday 10:30-19:30); Address: 13F, Building D1, Chuangzhi Yun City, Nanshan District, Shenzhen, Guangdong
