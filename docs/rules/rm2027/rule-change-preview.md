# RoboMaster 2027 University Series Rule-Change Preview (2026-09-09)

Unofficial English translation of the Chinese original. The Chinese PDF governs;
see the [translation index](README.md) for source, checksums and conventions.
`<!-- p.N -->` markers give the physical PDF page.

<!-- p.1 -->
### The 26th National University Student Robot Competition
### RoboMaster 2027
### RoboMaster University Series
### Rule-Change Preview Manual

Compiled by the RoboMaster Organizing Committee (RMOC)

Published September 2026

<!-- p.2 -->
### Intellectual Property Statement

The RoboMaster Organizing Committee (RMOC) encourages and advocates technical innovation and open-source technology, and respects the intellectual property of participating teams. All intellectual property developed by a team during the competition belongs to that team. RMOC does not handle intellectual property disputes among members within a team; teams must properly handle the intellectual property ownership relationships among their own school members, corporate members and members of other affiliations.

When using the Referee System and competition support materials provided by RMOC, teams must respect the intellectual property rights of the original product owners, and must not reverse engineer, copy, translate or otherwise act in any way that harms the owners' intellectual property rights.

For any act that harms the intellectual property of the competition education products provided by RMOC and the organizing entities, the intellectual property owner will pursue legal liability in accordance with the law.

For suggestions on open-source materials, see: https://bbs.robomaster.com/article/4820

### Reading Notice

The RoboMaster competition is a robot competition whose purpose is to cultivate young engineering talent. The related documents may involve sensitive wording, names, operations, technologies and other content. Such content does not reflect any technology or action that exists in reality, and is not intended to refer to any specific country, organization or individual. This manual is intended to explain the robot competition rules. It must not be used for any purpose other than the RoboMaster competition, and should not be considered to be associated with any real events or entities.

<!-- p.3: contents list omitted -->

<!-- p.4: contents list omitted -->

<!-- p.5: contents list omitted -->

<!-- p.6 -->
## 1 Overview of Main Changes in the New Season

This chapter briefly describes the main rule adjustments for the RM2027 season. Compared with the RM2026 season, the main revisions are as follows:

Robot systems:

- Redesigned the deployment method, usage method and functions of the Aerial Robot.
- The former Hero Robot and Engineer Robot are merged into the Heavy Robot.
- The former Custom Controller and Custom Client are merged into the Custom Terminal.

Battlefield:

- The former Launch Ramp is replaced by the Tunnel.
- Adjusted the overall layout of the Operator Room.
- Added the High Point, the Hangar Placement Zone and the Workbench.
- Removed the Flight Zone and the Wireless Charging Device Placement Zone.

> Note: This manual publishes only some key rule changes. For complete rule details and the final enforcement standards, refer to the official Rules Manual to be released later.

<!-- p.7 -->
## 2 Robot System Mechanics and Building Specifications

### 2.1 Robots and Operators

The robot lineup is as follows:

**Table 2-1 Robot Lineup**

| Type | Full lineup quantity (units) | Competition stage |
| --- | --- | --- |
| Heavy Robot | 1 | Throughout RMUC 2027 |
| Infantry Robot | 2 | Throughout RMUC 2027 |
| Aerial Robot and Hangar | 1 | Throughout RMUC 2027 |
| Sentry Robot | 1 | Throughout RMUC 2027 |
| Dart System | 1 | Throughout RMUC 2027 |
| Radar | 1 | Throughout RMUC 2027 |

The Operator lineup is as follows:

**Table 2-2 Operator Lineup**

| Type | Robots operated | Full lineup headcount |
| --- | --- | --- |
| Ground Robot Operator | Heavy Robot | 1 |
| Ground Robot Operator | Infantry Robot | 2 |
| Ground Robot Operator | Sentry Robot | 0 |
| Commander | Aerial Robot and Hangar (optional), Dart System (optional) | 1 |

> Note: Minimum lineup for the first round of each match: at least 3 robots, excluding the Radar and the Dart System.

<!-- p.8 -->
#### 2.1.1 Heavy Robot

The Heavy Robot can obtain diverse team Buffs by acquiring and assembling Energy Units; once certain conditions are met, it can also launch 42mm projectiles.

**Table 2-3 Heavy Robot Key Features**

| Key feature | Description |
| --- | --- |
| Initial zone | Starting Zone |
| Operation mode | Unrestricted; at most 1 Remote Controller and 1 Custom Terminal may be configured |
| Multi-robot communication | Allowed |
| Launching mechanism | 1 installable modular 42mm launching mechanism |
| Projectile loading and resupply | - During the three-minute Setup Period, 42mm and 17mm projectiles can be preloaded in both the robot and the modular 42mm launching mechanism; the initial Projectile Allowance is 0. - During the seven-minute Round, Projectile Allowance can be exchanged at permitted Buff Points or exchanged remotely. |
| Experience and Performance System | Not applicable<br>Note: The attributes of the Heavy Robot change as the match progresses. |

##### 2.1.1.1 Special Mechanics

The relationship between the Heavy Robot's attributes and its highest completed Assembly Level is shown in the table below:

**Table 2-4 Heavy Robot Assembly Level Attributes**

| Highest completed Assembly Level | Max HP | Barrel Heat Limit | Barrel Cooling Rate | Initial Launch Speed limit |
| --- | --- | --- | --- | --- |
| Start of match | 400 | - | - | - |
| Level 3 | 600 | 300 | 100 | 16.5m/s |
| Level 4 | 600 | 300 | 100 | 16.5m/s |

<!-- p.9 -->
Modular 42mm launching mechanism and unlock method:

The Heavy Robot's modular 42mm launching mechanism is stored on the Workbench in the Resource Zone at the start of the match and is not installed on the robot. After any one of the following conditions is met, the Heavy Robot unlocks the permission to use the modular 42mm launching mechanism, can install it on the robot, and can launch 42mm projectiles.

The modular launching mechanism is unlocked when any of the following conditions is met:

- Condition 1: Complete Level 3 assembly.
- Condition 2: The match has been in progress for 5 minutes.
- Condition 3: For each certain degree that a team falls behind, the unlock time in Condition 2 is moved earlier.

> Note: In RMUL, the Heavy Robot has no assembly tasks and unlocks permission to use the modular 42mm launching mechanism from the start of the match, but it must still install it on the robot by itself during the match before it has the ability to launch 42mm projectiles. The specific mechanics and values are subject to the official release.

##### 2.1.1.2 Building Specifications

The Heavy Robot must meet the following building requirements:

- The Heavy Robot must be able to move horizontally and to grab Energy Units in the Resource Zone.

  > Note: In RMUL, the Heavy Robot does not need the ability to grab Energy Units.

- Heavy Robot building parameter requirements:

**Table 2-5 Heavy Robot Building Parameters**

| Item | Limit | Remarks |
| --- | --- | --- |
| Operation mode | Unrestricted; at most 1 Remote Controller and 1 Custom Terminal may be configured | - |
| Max total power supply capacity (Wh) | 300 | - |
| Max operating voltage (V) | 30 | The voltage at any point inside the robot at any time relative to the battery negative terminal must not exceed 30V |
| Launching mechanism | Modular 42mm launching mechanism | Can only be installed during the seven-minute Round |
| Max weight (kg) | - 36: includes the weight of the battery and Referee System, but not the modular 42mm launching mechanism weight.<br>- 41: includes the weight of the battery, Referee System and modular 42mm launching mechanism. | - |

<!-- p.10 -->
| Item | Limit | Remarks |
| --- | --- | --- |
| Max stowed dimensions (mm, L*W*H) | The robot has a state in which its length, width and height are each no greater than 600*600*600 | - |
| Max extended dimensions (mm, L*W*H) | One of the following requirements must be met:<br>- Requirement 1: Under all circumstances, the robot's length, width and height must not exceed 1200*1200*1100.<br>- Requirement 2: Subject to the official Rules Manual release. | - |
| Referee System | - Small Armor Module<br>- Camera Video Transmitter Module (transmitter)<br>- Field Interaction Module<br>- Positioning Module (not applicable in RMUL)<br>- Main Controller Module<br>- Power Management Module<br>- Light Indicator Module | - |

The modular 42mm launching mechanism must meet the following building requirements:

- The Heavy Robot main body must be electrically isolated from the modular 42mm launching mechanism. The operating voltage inside the Heavy Robot main body must not exceed 30V and must not interfere with the normal operation of the Referee System.
- The modular 42mm launching mechanism must be able to launch 42mm projectiles.

Modular 42mm launching mechanism building parameter requirements:

**Table 2-6 Modular 42mm Launching Mechanism Building Parameters**

| Item | Limit | Remarks |
| --- | --- | --- |
| Max total power supply capacity (Wh) | - | No battery may be installed; powered by the robot directly |

<!-- p.11 -->
| Item | Limit | Remarks |
| --- | --- | --- |
| Max operating voltage (V) | 140 | The voltage at any point inside the module at any time relative to the battery negative terminal must not exceed 140V |
| Max weight (kg) | 6 | Includes the weight of the Referee System |
| Max stowed dimensions (mm, L*W*H) | The modular 42mm launching mechanism has a state in which its length, width and height are each no greater than 400*400*400 | - |
| Referee System | 42mm Speed Monitor Module |  |

The Heavy Robot can perform the following operations, but only at the Workbench:

Split into sub-robots or multiple subsystems connected by flexible cables, or merge from such a state.

Install or remove the modular 42mm launching mechanism.

#### 2.1.2 Aerial Robot and Hangar

The Aerial Robot can depart from the Hangar and perform diverse attack and reconnaissance missions on the Battlefield.

**Table 2-7 Aerial Robot and Hangar Key Features**

| Key feature | Description |
| --- | --- |
| Initial zone | Hangar Placement Zone |
| Multi-robot communication | Allowed |
| Launching mechanism | Not applicable |
| HP Recovery and Revival mechanics | Not applicable |
| Experience and Performance System | Not applicable |

<!-- p.12 -->
Typical functions of the Aerial Robot:

- Cause projectile damage to the opponent's Outpost and Base Armor Modules through direct impact.
- Change the trajectories of opposing Darts and projectiles by actively intercepting them, achieving interception.
- Hover and obtain information; after returning to the Hangar, transmit the information to the Hangar, which further provides it to systems such as the Radar.

##### 2.1.2.1 Building Specifications

The Aerial Robot must meet the following building requirements:

- The Aerial Robot must be able to hover continuously for at least 10 s.
- The Aerial Robot must have a fully enclosed propeller guard outside its body; the propellers and body must not be exposed. When the Aerial Robot strikes an Armor Module at any angle and at a certain horizontal speed, the propeller guard must effectively keep the propellers from touching the Armor Module.
- The Aerial Robot's propellers must be made of flexible material.
- The Aerial Robot must be equipped with a remote controller/receiver for emergency propeller stop, and a safety officer must be assigned.

Aerial Robot building parameter requirements:

**Table 2-8 Aerial Robot Building Parameters**

| Item | Limit | Remarks |
| --- | --- | --- |
| Operation mode | Fully automatic | Can communicate with the Hangar while inside the Hangar |
| Max total power supply capacity (Wh) | TBD | - |
| Max operating voltage (V) | TBD | - |
| Launching mechanism | Installation of a launching mechanism is not allowed | - |
| Max weight (kg) | y | Size and weight limits are linearly related: y=−0.001225x+0.3225, y∈[0.15,0.249] |
| Max extended dimensions (mm) | When the Aerial Robot's weight is y, under all circumstances the robot's length, width and height must not exceed x*x*x | Size and weight limits are linearly related: y=−0.001225x+0.3225, y∈[0.15,0.249] |

The Hangar must meet the following building requirements:

- The Hangar must be able to store Aerial Robots.

<!-- p.13 -->
Hangar building parameter requirements:

**Table 2-9 Hangar Building Parameters**

| Item | Limit | Remarks |
| --- | --- | --- |
| Operation mode | Unrestricted; at most 1 Remote Controller may be configured for debugging | - |
| Max total power supply capacity (Wh) | 300 | - |
| Max operating voltage (V) | 30 | The voltage at any point inside the Hangar at any time relative to the battery negative terminal must not exceed 30V |
| Aerial Robot load limit | 4 | - |
| Max weight (kg) | TBD | - |
| Max stowed dimensions (mm, L*W*H) | 300*300*200 | - |
| Max extended dimensions (mm, L*W*H) | TBD | - |
| Referee System | TBD | - |

The Hangar can provide initial thrust to the Aerial Robot, but the direction is limited to within a 15° cone angle of the Hangar's vertical normal.

### 2.2 Custom Terminal

The Custom Terminal (the former Custom Controller and Custom Client) is a multi-purpose device built by participating teams. It is used to monitor robot motion and status, control robot actions, receive match-related information and robot video feeds sent by the Referee System's match engine server, and send match-specific interaction commands to the match engine server, expanding the possibilities of human-robot interaction.

A typical Custom Terminal can consist of one display device, one computing platform (including memory, controller and processor) and a set of input devices; it can also take an integrated form, for example a handheld tablet device with a network port.

> Example: A team builds a Custom Terminal that can receive the robot video feed and present it on a self-made display, overlay a self-made UI shown over an unofficial link, and control the robot through a matching controller. As a result, the team can complete the match without using the official Referee System Operator-side client and Remote Controller.

<!-- p.14 -->
All Custom Terminals in the Operator Room can be connected to one another by wire and communicate, and a Custom Terminal can connect by wire to the match engine server through the RJ45 port provided in the Operator Room to send and receive related content.

A Custom Terminal can receive match information that is shown on the Referee System Operator-side client and is obtainable by its own team, for example: both teams' HP, own team's Economy, remaining match time, and announcements of key match events.

A Custom Terminal can send to the Referee System the match commands supported by the Operator-side client, for example active commands such as selecting the Performance System before the match, exchanging Projectile Allowance during the match, and intervening in Sentry Robot actions.

#### 2.2.1 Building Specifications

The Custom Terminal's building parameters must meet the following requirements:

**Table 2-10 Custom Terminal Building Parameters**

| Item | Limit | Remarks |
| --- | --- | --- |
| Max operating voltage (V) | 30 | The voltage at any point inside the module at any time relative to the battery negative terminal must not exceed 30V |
| Max stowed dimensions (mm, L*W*H) | 600*600*600 | - |
| Max extended dimensions (mm, L*W*H) | Unlimited | Consequences caused by size, such as inconvenient use or inability to compete normally, are borne by the participating team |
| Data transmission | Video feed information: UDP<br>Match-related data: MQTT+ProtoBuf |  |
| Protocol | See the Communication Protocol | - |

**Usage specification:**

The Custom Terminal must not use wireless transmitting/receiving devices.

<!-- p.15 -->
## 3 Battlefield and Related Mechanics

### 3.1 High Point

The High Point is located in the Base Zone. The connection between the Trapezoidal Highland and the High Point is a three-level step, and robots can climb the step to enter the High Point.

[1] High Point

*Figure 3-1 High Point Diagram*

- [1] High Point
- Plan view dimension labels: 2400, 1394, 1200 (horizontal); 2400, 1394, 1200 (vertical); section lines A and B
- Section A-A: 300, 300, 100; 200, 200, 200, (600)
- Section B-B: 300, 300, 300, 100; (800), 200, 200, 200, 200; 100, 300
- G: ground datum

#### 3.1.1 Buff Point Mechanics

All own-team robots can occupy their own team's High Point Buff Point.

If a team's High Point Buff Point is occupied by a robot of that team, the robot occupying the High Point gains a 50% defense Buff and can exchange Projectile Allowance non-remotely.

### 3.2 Tunnel

The former Launch Ramp is changed to the Tunnel. The Tunnel is located in the Road Zone, and robots can pass through or leap over the Tunnel to quickly reach the opponent's half of the field.

<!-- p.16 -->
*Figure 3-2 Tunnel Diagram*

- Top view: 350 (central bridge width), 800 (tunnel width)
- View A: 200, 250, 270
- G: ground datum

#### 3.2.1 Buff Point Mechanics

The terrain-crossing Buff Point (Tunnel) has two Buff forms, depending on the type and order of Field Interaction Module cards detected when passing through the Tunnel:

**Table 3-1 Tunnel Buff Trigger Logic and Effects**

| Buff type | Field Interaction Module card types and order detected | Buff effect |
| --- | --- | --- |
| Leap over the Tunnel | Only the Field Interaction Module cards at the Tunnel entrance and exit are detected, in order | 25% defense Buff, lasting 30 s |
| Pass through the Tunnel | The Field Interaction Module cards at the Tunnel entrance, interior and exit are detected, in order | 1.5x Barrel Cooling Rate Buff, lasting 120 s |

The same robot must have each Field Interaction Module card of the Tunnel detected in order within 3 s, and no other type of Field Interaction Module card may be detected along the way, to obtain the above Buffs.

### 3.3 Supply Zone

The Supply Zone includes the Resource Station, the Supply Zone Buff Point and the Workbench. It is an important area where robots recover HP, replenish Projectile Allowance, obtain Energy Units and assemble the modular 42mm launching mechanism.

<!-- p.17 -->
#### 3.3.1 Workbench

The Workbench is located in the Supply Zone. Robots can pick up the modular 42mm launching mechanism and assemble it.

[1] Workbench

*Figure 3-3 Workbench Diagram*

- [1] Workbench
- Side view: 400
- Top view: 450, 350; 650, 750
- G: ground datum

<!-- p.18 -->
### 3.4 Hangar Placement Zone

The Hangar Placement Zone is located in the center of the Battlefield and is divided into red and blue sides. Each side can install its Hangar only in the Hangar Placement Zone.

[1] Red side Hangar Placement Zone  [2] Blue side Hangar Placement Zone

*Figure 3-4 Hangar Placement Zone Diagram*

- [1] Red side Hangar Placement Zone
- [2] Blue side Hangar Placement Zone
- Top view: 400, 320 (at each of the two "H" markers)
- Section A-A: 40, (1140), 100, 300
- G: ground datum

### 3.5 Operator Room

The Operator Room is located near the outer edge of the Battlefield and is the activity area for Operators during matches. Each Operator desk in the Operator Room is 120cm long and 75cm wide and is provided with a corresponding number of computers. Each computer is equipped with official equipment including a corresponding monitor, mouse, keyboard, Camera Video Transmitter Module (receiver) and its bracket, one 1GbE (RJ45) network port, and a wired headset.

<!-- p.19 -->
Email: robomaster@dji.com
Forum: https://bbs.robomaster.com
Website: https://www.robomaster.com
Tel: +86 0755-84357613 (Monday to Friday 10:30-19:30)
Address: 13F, Building D1, Chuangzhi Yuncheng, Nanshan District, Shenzhen, Guangdong Province
