# RoboMaster 2027 University Series Robot Building Specifications Manual V1.0.0 (2026-10-15)

Unofficial English translation of the Chinese original. The Chinese PDF governs;
see the [translation index](README.md) for source, checksums and conventions.
`<!-- p.N -->` markers give the physical PDF page.

<!-- p.1 -->
### The 26th National University Student Robot Competition (RoboMaster 2027)
### RoboMaster University Series
### Robot Building Specifications Manual
V1.0.0

Compiled by the RoboMaster Organizing Committee

Published October 2026

<!-- p.2 -->
### Intellectual Property Statement
The RoboMaster Organizing Committee (RMOC) encourages and advocates technical innovation and open-source technology, and respects the intellectual property of participating teams. All intellectual property developed by a team during the competition belongs to that team. RMOC does not take part in resolving intellectual property disputes among members of a team. Participating teams must properly handle ownership relations among their own school members, company members and members of other affiliations.

When using the Referee System and competition support materials provided by RMOC, teams must respect the intellectual property of the original product owners, and must not reverse engineer, copy, translate or otherwise act against the owners' intellectual property rights.

Any act that infringes the intellectual property of the competition education products provided by RMOC and the host organizations will be pursued by the rights holders through legal means.

For suggestions on open-source materials, see: https://bbs.robomaster.com/article/4820

### Reading Notice
The RoboMaster competition is a robot competition whose purpose is to cultivate young engineering talent. The related documents may involve sensitive wording, names, operations and technologies. These do not reflect any technology or action existing in reality, and are not intended to refer to any specific country, organization or individual. This manual is intended to describe the robot competition rules. It must not be used for any purpose other than the RoboMaster competition, and should not be regarded as related to any real events or entities.

### Revision Log
| Date | Version | Revision Record |
| --- | --- | --- |
| 2026.10.15 | V1.0.0 | First release |

<!-- p.3 -->

## Contents

| Entry | Printed page |
| --- | --- |
| [Intellectual Property Statement](#intellectual-property-statement) | 1 |
| [Reading Notice](#reading-notice) | 1 |
| [Revision Log](#revision-log) | 1 |
| [1 Foreword](#1-foreword) | 9 |
| [2 Technical Specifications](#2-technical-specifications) | 10 |
| [2.1 General Technical Specifications](#21-general-technical-specifications) | 10 |
| [2.1.1 Energy](#211-energy) | 10 |
| [2.1.2 Communication Equipment](#212-communication-equipment) | 12 |
| [2.1.3 Optical Means](#213-optical-means) | 14 |
| [2.1.4 Visual Features](#214-visual-features) | 15 |
| [2.1.5 Appearance Design](#215-appearance-design) | 15 |
| [2.1.6 Launching Mechanism](#216-launching-mechanism) | 17 |
| [2.1.7 Custom Terminal](#217-custom-terminal) | 17 |
| [2.1.8 17mm Fluorescent Projectile Charging Device](#218-17mm-fluorescent-projectile-charging-device) | 18 |
| [2.1.9 Others](#219-others) | 20 |
| [2.2 Specifications for Complete Finished Robots and Open-Source Robots](#22-specifications-for-complete-finished-robots-and-open-source-robots) | 20 |
| [2.2.1 Sufficient Redesign](#221-sufficient-redesign) | 21 |
| [2.2.2 Non-Sufficient Redesign](#222-non-sufficient-redesign) | 22 |
| [2.2.3 Invalid Redesign](#223-invalid-redesign) | 23 |
| [2.3 Definition and Scope of Third-Party Finished Modules and Finished Systems](#23-definition-and-scope-of-third-party-finished-modules-and-finished-systems) | 23 |
| [2.4 Robot Technical Specifications](#24-robot-technical-specifications) | 26 |
| [2.4.1 Heavy Robot](#241-heavy-robot) | 26 |
| [2.4.2 Infantry Robot](#242-infantry-robot) | 29 |
| [2.4.3 Sentry Robot](#243-sentry-robot) | 30 |
| [2.4.4 Aerial System](#244-aerial-system) | 31 |

<!-- p.4 -->

| Entry | Printed page |
| --- | --- |
| [2.4.5 Dart System](#245-dart-system) | 35 |
| [2.4.6 Radar System](#246-radar-system) | 41 |
| [3 Referee System Installation Specifications](#3-referee-system-installation-specifications) | 44 |
| [3.1 Referee System Overview](#31-referee-system-overview) | 45 |
| [3.2 Robot Referee System Onboard End Configuration](#32-robot-referee-system-onboard-end-configuration) | 46 |
| [3.3 Main Controller Module Installation Specifications](#33-main-controller-module-installation-specifications) | 48 |
| [3.3.1 Installation Steps](#331-installation-steps) | 48 |
| [3.3.2 Installation Requirements](#332-installation-requirements) | 49 |
| [3.4 Power Management Module Installation Specifications](#34-power-management-module-installation-specifications) | 53 |
| [3.4.1 Installation Steps](#341-installation-steps) | 54 |
| [3.4.2 Installation Requirements](#342-installation-requirements) | 56 |
| [3.5 Light Indicator Module Installation Specifications](#35-light-indicator-module-installation-specifications) | 58 |
| [3.5.1 Installation Steps](#351-installation-steps) | 59 |
| [3.5.2 Installation Requirements](#352-installation-requirements) | 60 |
| [3.6 Armor Module Installation Specifications](#36-armor-module-installation-specifications) | 60 |
| [3.6.1 General Specifications](#361-general-specifications) | 61 |
| [3.6.2 Installation Steps](#362-installation-steps) | 63 |
| [3.6.3 Installation Requirements](#363-installation-requirements) | 66 |
| [3.7 Speed Monitor Module Installation Specifications](#37-speed-monitor-module-installation-specifications) | 68 |
| [3.7.1 Installation Steps](#371-installation-steps) | 70 |
| [3.7.2 Installation Requirements](#372-installation-requirements) | 74 |
| [3.8 Field Interaction Module Installation Specifications](#38-field-interaction-module-installation-specifications) | 77 |
| [3.8.1 Installation Steps](#381-installation-steps) | 77 |
| [3.8.2 Installation Requirements](#382-installation-requirements) | 78 |
| [3.9 Camera Video Transmitter Module (Transmitter) Installation Specifications](#39-camera-video-transmitter-module-transmitter-installation-specifications) | 79 |
| [3.9.1 Installation Steps](#391-installation-steps) | 80 |
| [3.9.2 Installation Requirements](#392-installation-requirements) | 80 |

<!-- p.5 -->

| Entry | Printed page |
| --- | --- |
| [3.10 Camera Video Transmitter Module (Receiver) Usage Specifications](#310-camera-video-transmitter-module-receiver-usage-specifications) | 81 |
| [3.10.1 Installation Requirements](#3101-installation-requirements) | 82 |
| [3.11 Positioning Module Installation Specifications](#311-positioning-module-installation-specifications) | 82 |
| [3.11.1 Installation Steps](#3111-installation-steps) | 82 |
| [3.11.2 Installation Requirements](#3112-installation-requirements) | 83 |
| [3.12 Supercapacitor Management Module Installation Specifications](#312-supercapacitor-management-module-installation-specifications) | 84 |
| [3.12.1 Installation Steps](#3121-installation-steps) | 84 |
| [3.12.2 Installation Requirements](#3122-installation-requirements) | 85 |
| [Appendix 1 17mm Speed Monitor Module Adapter Part Engineering Drawing](#appendix-1-17mm-speed-monitor-module-adapter-part-engineering-drawing) | 87 |
| [Appendix 2 Reference Drawings](#appendix-2-reference-drawings) | 88 |

<!-- p.6 -->

## List of Tables

| Entry | Printed page |
| --- | --- |
| Table 2-1 Summary of Battery Types | 10 |
| Table 2-2 Summary of Control Methods | 12 |
| Table 2-3 Summary of Remote Controllers | 13 |
| Table 2-4 Custom Terminal Build Parameters | 17 |
| Table 2-5 Heavy Robot build parameter description | 26 |
| Table 2-6 Modular 42mm launching mechanism build parameter description | 29 |
| Table 2-7 Infantry Robot build parameter description | 29 |
| Table 2-8 Sentry Robot build parameter description | 30 |
| Table 2-9 Aerial Robot build parameter description | 32 |
| Table 2-10 Hangar build parameter description | 34 |
| Table 2-11 Dart build parameter description | 35 |
| Table 2-12 Dart launcher build parameter description | 36 |
| Table 2-13 Radar computing platform end manufacturing parameters | 41 |
| Table 2-14 Radar sensor end parameters | 41 |
| Table 3-1 Maximum replacement time for each Referee System onboard end module | 44 |
| Table 3-2 Referee System modules | 45 |
| Table 3-3 Robot Referee System onboard end module configuration | 46 |
| Table 3-4 Power Management Module interface description | 57 |

<!-- p.7 -->

## List of Figures

| Entry | Printed page |
| --- | --- |
| Figure 2-1 Installation Diagram of the 17mm Fluorescent Projectile Charging Device | 18 |
| Figure 2-2 Aerial Robot Pre-Match Inspection diagram | 32 |
| Figure 2-3 Aerial Robot propeller guard diagram | 33 |
| Figure 2-4 Light group diagram | 34 |
| Figure 2-5 Dart flight direction diagram | 36 |
| Figure 2-6 Dart System size limit diagram | 37 |
| Figure 2-7 Dart trigger device diagram | 39 |
| Figure 2-8 Dart trigger device no-obstruction zone diagram | 40 |
| Figure 2-9 Dart trigger device internal cavity diagram | 40 |
| Figure 3-1 Main Controller Module diagram | 48 |
| Figure 3-2 Main Controller Module wiring diagram | 49 |
| Figure 3-3 Main Controller Module no-obstruction zone | 49 |
| Figure 3-4 Main Controller Module installation position diagram | 50 |
| Figure 3-5 Hangar Main Controller Module installation diagram | 51 |
| Figure 3-6 Dart Launching Station Referee System aviation cable position diagram | 52 |
| Figure 3-7 Power Management Module diagram | 53 |
| Figure 3-8 Power Management Module installation diagram | 54 |
| Figure 3-9 Power Management Module interface diagram | 55 |
| Figure 3-10 Power Management Module wiring diagram | 56 |
| Figure 3-11 Light Indicator module diagram | 58 |
| Figure 3-12 Light Indicator module screw installation positions | 59 |
| Figure 3-13 Light Indicator module bottom view | 59 |
| Figure 3-14 Light Indicator module wiring diagram | 59 |
| Figure 3-15 Designated armor support bracket diagram | 60 |
| Figure 3-16 Robot coordinate system diagram | 61 |

<!-- p.8 -->

| Entry | Printed page |
| --- | --- |
| Figure 3-17 X axis diagram for different robot chassis configurations | 61 |
| Figure 3-18 Armor Module force diagram | 62 |
| Figure 3-19 Robot protection diagram | 63 |
| Figure 3-20 Armor support bracket installation diagram | 64 |
| Figure 3-21 Armor Module installation diagram | 64 |
| Figure 3-22 Armor Module wiring diagram | 65 |
| Figure 3-23 Armor Module installation specification diagram | 66 |
| Figure 3-24 No-obstruction zone of Infantry Robot and Sentry Robot Armor Modules | 66 |
| Figure 3-25 No-obstruction zone of Heavy Robot Armor Modules | 67 |
| Figure 3-26 17mm Speed Monitor Module diagram | 68 |
| Figure 3-27 42mm Speed Monitor Module diagram | 69 |
| Figure 3-28 17mm launch tube diagram | 70 |
| Figure 3-29 Speed Monitor Module installation diagram | 71 |
| Figure 3-30 17mm adapter part diagram | 71 |
| Figure 3-31 17mm adapter part fixing method diagram | 72 |
| Figure 3-32 17mm short launch tube installation diagram | 73 |
| Figure 3-33 42mm launch tube diagram | 74 |
| Figure 3-34 Speed Monitor Module installation diagram | 75 |
| Figure 3-35 Speed Monitor Module installation specification diagram | 76 |
| Figure 3-36 Referee System wire sequence diagram | 76 |
| Figure 3-37 Field Interaction Module diagram | 77 |
| Figure 3-38 Field Interaction Module wiring diagram | 77 |
| Figure 3-39 Field Interaction Module installation diagram | 78 |
| Figure 3-40 Camera Video Transmitter Module (transmitter) diagram | 79 |
| Figure 3-41 Camera Video Transmitter Module (transmitter) installation diagram | 80 |
| Figure 3-42 No-obstruction zone of the Camera Video Transmitter Module (transmitter) | 81 |
| Figure 3-43 Camera Video Transmitter Module (receiver) diagram | 81 |

<!-- p.9 -->

| Entry | Printed page |
| --- | --- |
| Figure 3-44 Positioning Module diagram | 82 |
| Figure 3-45 Positioning Module installation diagram | 82 |
| Figure 3-46 Positioning Module wiring diagram | 83 |
| Figure 3-47 Positioning Module installation diagram | 83 |
| Figure 3-48 Supercapacitor Management Module wiring diagram | 85 |

<!-- p.10 -->
## 1 Foreword
RoboMaster teams must develop and build their robots themselves. Participating robots must satisfy all specifications described in this document, and Pre-Match Inspection staff will spot-check robots according to the provisions of this document. In addition, participating robots must comply with relevant laws and regulations and must not pose safety hazards. If a safety accident is caused by a violation, RMOC will pursue the legal liability of the violating party in accordance with the law. If there is any dispute over these specifications, the interpretation of the Chief Referee or the Chief Inspector shall prevail.

To help teams understand and comply with the provisions of this manual, the binding force of the provisions and their possible consequences are explained as follows:

- Provisions marked "S#" before the item (for example, S10) throughout the document are mandatory provisions. Mandatory provisions focus on key requirements such as safety, size/weight, electromagnetic compatibility and field rules, and must be strictly observed. If a mandatory provision is violated, RMOC has the right to refuse the robot's participation, require rectification within a time limit, or directly declare disqualification, depending on the nature of the violation.
- Provisions not marked "S#" are advisory provisions. Advisory provisions are used to optimize performance, improve stability or reduce failure risk, but are not a hard condition for passing Pre-Match Inspection. Not following an advisory provision does not directly affect passing the inspection, but may lead to module malfunction, limited performance in matches, additional repair/damage assessment costs or safety hazards. All losses and consequences arising from this are borne by the team itself.
- Unless otherwise stated in a provision, all mandatory provisions in this manual apply to both RMUC and RMUL robots. If a provision involves robot types, field props or competition rules that are not relevant to RMUL, RMUL robots may be exempted from that specific requirement.

<!-- p.11 -->
## 2 Technical Specifications
### 2.1 General Technical Specifications
#### 2.1.1 Energy
**S1** The only forms of energy a robot may use are electric power and gas supply.

**S2** For robots subject to the Chassis Power limit, the power source for horizontal movement of the chassis is limited to electric power.

> Note:
> - Fuel-driven engines, explosives and hazardous chemical materials are prohibited.
> - Mains power is prohibited within the competition area (except for the Radar computing platform end).
> - Hydraulic or other power methods that may cause pollution are prohibited.

##### 2.1.1.1 Power Supply
**S3** Batteries must be stably mounted on a battery rack.

> Note: The battlefield terrain is complex; it is recommended to provide cushioning protection for the battery.

**S4** The only battery types a robot may use are listed in the table below:

> Note: For the definition of a regular manufacturer, see "2.3 Definition and Scope of Application of Third-Party Finished Modules and Finished Systems".

**Table 2-1 Summary of Battery Types**

| Robot/Module \ Battery type | Batteries produced by Shenzhen DJI Innovation Technology Co., Ltd. | Dry batteries produced by other regular manufacturers | Lithium batteries produced by other regular manufacturers |
| --- | --- | --- | --- |
| Heavy Robot | Allowed | Allowed | Not allowed |
| Infantry Robot | Allowed | Allowed | Not allowed |
| Aerial Robot | Allowed | Allowed | Allowed |
| Hangar | Allowed | Allowed | Not allowed |
| Sentry Robot | Allowed | Allowed | Not allowed |

<!-- p.12 -->
| Robot/Module \ Battery type | Batteries produced by Shenzhen DJI Innovation Technology Co., Ltd. | Dry batteries produced by other regular manufacturers | Lithium batteries produced by other regular manufacturers |
| --- | --- | --- | --- |
| Dart Launcher | Allowed | Allowed | Not allowed |
| Dart | Allowed | Allowed | Allowed |
| Radar sensor end | Allowed | Allowed | Allowed |
| Radar computing platform end | Allowed | Allowed | Allowed |
| Custom Terminal | Allowed | Allowed | Allowed |

> Note: The following provisions in this subsection that involve Supercapacitor module requirements apply only to Supercapacitor modules that participate in Chassis Power.

**S5** Only Ground Robots may install Supercapacitor modules; each robot may install at most 1 Supercapacitor module.

**S6** For a Ground Robot, the total nominal energy of a single Supercapacitor module must not exceed 2000 J, and the total measured energy must not exceed 2200 J. The nominal energy of a single capacitor module is calculated as E = 1/2 * C * U^2 (U is the rated withstand voltage of the capacitor, C is the capacitance).

**S7** For the chassis power energy source of robots subject to the power limit, the sum of the nominal capacitance of capacitors connected to the Chassis interface but not participating in Chassis Power must not exceed 10 mF.

> Note: If the capacitor bank used in a Supercapacitor module does not participate in Chassis Power, the corresponding schematic must be brought to Pre-Match Inspection as supporting evidence.

**S8** In a modular 42mm launching mechanism, the sum of the nominal capacitance of the capacitors must not exceed 80 mF.

##### 2.1.1.2 Gas Supply
**S9** The pressure of compressed gas stored in a gas cylinder must not exceed 20 MPa, the nominal withstand pressure of the cylinder must not be less than 30 MPa, and a dual-gauge constant-pressure valve must be installed directly at the cylinder outlet, with a working pressure not exceeding 0.8 MPa.

**S10** The working gas must be non-combustible, non-toxic and non-polluting, such as air, nitrogen or carbon dioxide.

**S11** Any mechanism that uses or stores gas (gas cylinders, air cylinders, air springs, etc.) must have a certificate of conformity or a stamped nameplate, and the certificate or nameplate stamp must be easy to view during Pre-Match Inspection.

**S12** If a gas cylinder is still within its service life, it must be returned to the factory for maintenance within the period specified in the manual or on the nameplate, and proof of maintenance must be provided.

**S13** Gas cylinders must have a certification certificate issued by a certification body officially recognized by the country of origin.

<!-- p.13 -->
**S14** Gas cylinders must be mounted on the robot body safely and firmly. The cylinder body must have at least 2 fixing points spaced more than 1/5 of the cylinder length apart, or must have a fixing surface longer than 1/5 of the cylinder length. Cylinders and gas lines must be protected to prevent damage caused by robot rollover, collision, rotation, failure of moving parts, etc. The cylinder mouth must not be exposed, to prevent damage from projectile impact. For safety, the cylinder mouth must remain horizontal or face upward.

**S15** When a gas cylinder is installed, it must be considered that if the robot rolls over at any angle, neither the cylinder nor the gas lines will touch the ground.

**S16** Gas lines and fittings must be rated for the maximum possible working pressure of the system.

> Note:
> - It is recommended to install a safety relief valve in the low-pressure gas circuit.
> - It is recommended to avoid any flammable material within 50 mm of the gas cylinder.

#### 2.1.2 Communication Equipment
The competition venue and its surroundings are complex, and RMOC cannot guarantee that the wireless environment in the competition area will not interfere with participating equipment. Teams must adapt to the wireless environment at the venue themselves.

**S17** The control methods designated for this season are shown in the table below:

**Table 2-2 Summary of Control Methods**

| Data link | Information transmitted |
| --- | --- |
| Remote Controller | Remote Controller stick information |
| Camera Video Transmitter Module (receiver end) | Keyboard and mouse commands, Remote Controller stick information |
| Video transmission link | Custom Terminal information |
| Referee System serial port | Multi-robot communication |

> Note:
> - RMOC recommends that teams control robots using the video transmission link or the Camera Video Transmitter Module (receiver end).
> - The Camera Video Transmitter Module (receiver end) itself has Remote Controller data sending capability (together with the player end, it can send keyboard and mouse data at the same time). For protocols related to the Camera Video Transmitter Module (receiver end), see the "Camera Video Transmitter Module User Manual".
> - The video transmission link refers to the link that uses the Camera Video Transmitter Module for data transmission. For protocols related to the video transmission link, see the "RoboMaster 2027 University Series Communication Protocol".

**S18** At Pre-Match Inspection, a robot must be equipped with a compliant Remote Controller for debugging, so that functions such as projectile launching, chassis movement and gimbal movement can be demonstrated during inspection.

<!-- p.14 -->
**S19** The Remote Controllers designated for this season are shown in the table below. Other models of the same style must not be used. Only Remote Controllers using the 2.4G band are allowed, and RMOC does not guarantee their stability.

> Note: The Camera Video Transmitter Module (receiver end) has Remote Controller functions but is not regarded as a Remote Controller. During a match, RMOC only guarantees the stability of the Camera Video Transmitter Module (receiver end) located in the Operator Room.

**Table 2-3 Summary of Remote Controllers**

| Name | Picture (for reference only) |
| --- | --- |
| DT7 | (picture) |
| FlySky i6X | (picture) |
| Radiolink ET08, ET08A | (picture) |

<!-- p.15 -->
| Name | Picture (for reference only) |
| --- | --- |
| Radiolink ET16S, Radiolink ET16 | (picture) |

> Note:
> - Given the complex wireless environment at the venue, the above Remote Controllers may also be subject to interference. It is recommended to carry multiple redundant control methods to avoid loss of control.
> - Robots entering the battlefield automatically connect to the Camera Video Transmitter Module (receiver end) in the Operator Room; Camera Video Transmitter Modules (receiver end) brought by teams cannot be used. The default state of the sticks of the Camera Video Transmitter Module (receiver end) in the Operator Room is centered, and the default state of the switches is position C.

**S20** Except for Aerial Robots, each Remote Controller must be paired one-to-one with a receiver.

**S21** Modification of the wireless RF part of the Remote Controller is not allowed. Adjusting the antenna mounting, antenna damage, or repairing the antenna through official after-sales channels is not regarded as modification.

**S22** Except for visible light communication, a robot must not carry wireless communication equipment other than the Remote Controller, the Referee System and radar information receiving devices. Visible light communication is limited to between participating robots.

**S23** Equipment carried by a robot must not generate wireless signal interference in the bands 0.428-0.438 GHz, 2.3-2.55 GHz, 3.75-4.75 GHz and 5-7.5 GHz.

> Note: It is recommended to enable all functions of the robot and use a spectrum analyzer placed close to equipment that may generate wireless interference to measure.

#### 2.1.3 Optical Means
**S24** Except for the Custom Terminal, a robot may install a display of no more than 7 inches. The illuminance measured within 40 mm of the display must not exceed 300 Lux, and the light-emitting surface of the display must be more than 100 mm from the Armor Module.

**S25** Except for devices required to be installed by this manual, a robot must not install obvious visible-light or invisible-light emitting devices.

> Note: Light sources such as robot status indicators and infrared sensors are not regarded as obvious light-emitting devices.

<!-- p.16 -->
**S26** Laser products must not be modified. The laser safety rating of a laser product is determined by the following data, taking the highest value:

- The value on the laser product's own safety nameplate, or relevant proof issued by the manufacturer/distributor.
- The power measured by inspection staff with a laser power meter placed close against the laser product.

**S27** No optical means used by a robot may cause physical harm to anyone.

**S28** All robots may only install invisible laser products with laser safety class Class I; visible laser products must not be installed.

#### 2.1.4 Visual Features
The competition field and its surroundings are complex, and RMOC cannot guarantee that visual features at the venue will not cause visual interference. Vision algorithms must adapt to changes in field lighting and other possible surrounding interference.

The following specifications must be followed when designing robots:

**S29** Visual features must not be simulated.

**S30** The robot's visual features must not be altered by any means.

> Note:
> - In the 2027 season, the hit surface of the Referee System Armor Module is a dot-matrix screen. The hit surface can display the corresponding robot number or a pattern (specific styles to be updated later).
> - Robot visual features: the content displayed by the Armor Module and its appearance.
> - Field visual features: the Dart Launching Station, visual tags, Power Rune lighting effects, Tech Core lighting effects, dart guidance lights, etc.

#### 2.1.5 Appearance Design
To prevent robot appearance design from affecting shooting engagements on the field and the viewing experience, the following specifications must be followed when designing and building robot appearance:

**Basic requirements:**

**S31** Robot wiring must be neat, with no exposed metal cores. Unavoidably exposed wires must be protected with drag chains, cable organizers or similar materials.

**S32** The robot's appearance must not contain materials that obviously harm its appearance, such as washbasins, plastic bottles, corrugated cardboard, bed sheets, white foam boards, bubble wrap, etc.

**S33** Fishing nets must not be used as appearance design material, but may be used to make protective covers for Aerial Robots.

**S34** Sharp structures must not be designed or used, to prevent damage to the field and injury to people.

**S35** For Ground Robots, within the height range of 0 to 400 mm above the ground, all exposed mechanism structure edges that may come into direct contact with the detection surface of other robots' Armor Modules must be rounded, with a fillet radius of not less than 10 mm.

<!-- p.17 -->
> Note: Flexible protective material will be provided in the Pre-Match Inspection area for collection on site. However, flexible material covered on site may not fit the robot's structure, moving mechanisms or functional components. It is recommended that teams install protective covers before the match, or wrap the relevant structures with flexible material.

**Glossiness:**

**S36** The glossiness of any area of the robot's appearance larger than 10mm*20mm must not exceed 30 Gs. Items that cannot be used after glossiness is reduced, such as optical axes and camera lenses, are excluded, but the shortest straight-line distance between such items and the left and right edges of the Armor Module must be greater than 100 mm.

**Paint color:**

> Note:
> - It is recommended that the appearance style of all robots in a team be coordinated.
> - It is recommended that each robot have two of its own school emblems or team emblems on its exterior, attached facing different directions. The area of a single school emblem or team emblem must not exceed 100mm*100mm. The emblem must be in a prominent position on the robot and at least 30 mm from the Light Indicators on both sides of the Armor Module. If the appearance does not meet the specifications, Pre-Match Inspection staff will require the placement or size of the school emblem or team emblem to be corrected.

**S37** The protective shell of Red-side robots may use red tones, and that of Blue-side robots may use blue tones. A robot may have at most 4 areas in the opposing team's color, and the area of each single region must not exceed 60mm*60mm.

> Note: When designing a robot, it is recommended to avoid red or blue accessories as much as possible.

**S38** Paint or stickers of school emblems and team emblems must not affect the robot's visual features and must not emit light.

**Protective shell installation:**

> Note: It is recommended that teams make protective shells from tough materials that are not easily damaged, and perform reliability tests on the shells, to avoid shell damage from engagements on the field that results in violations.

**Decoration requirements:**

**S39** Advertising spaces must be placed on the left and right sides of the robot, at least 30 mm from the edge of the Armor Module.

**S40** Paint or stickers on advertising spaces must not affect the robot's visual features and must not emit light.

**S41** The area of a single advertising space on a robot must not exceed 100mm*100mm, and each robot may have at most 2 advertising spaces for sponsor exposure. If the appearance does not meet the specifications, Pre-Match Inspection staff will require the placement or size of the advertising space to be corrected.

**S42** Auxiliary Equipment (Custom Terminal) and its components, in either hardware or software (including the user interface UI), must not display sponsor brand names, logos, slogans or other related elements in any form.

<!-- p.18 -->
> Note: School emblems, team emblems and advertising spaces may be rendered in monochrome white or may keep their original colors.

#### 2.1.6 Launching Mechanism
> Note: Launching mechanism: a mechanism that enables a projectile to leave the robot along a fixed path with a certain Initial Launch Speed.

**S43** For launching mechanisms that use compressed gas as the projectile launch power, the acceleration stroke must not exceed 200 mm (acceleration must be completed before entering the Speed Monitor Module).

**S44** A robot's launching mechanism must be able to stably launch 10 17mm projectiles or 5 42mm projectiles.

**S45** Each launching mechanism must have the corresponding Speed Monitor Module installed according to the specifications.

#### 2.1.7 Custom Terminal
The Custom Terminal is a multi-purpose set of equipment made by the team. It is a controller used to control robot actions or monitor robot movement, status, etc. It receives competition-related information and robot video transmission images sent by the Referee System match engine server, and sends competition-specific interaction commands to the match engine server.

**S46** The build parameters of the Custom Terminal must meet the following requirements:

**Table 2-4 Custom Terminal Build Parameters**

| Item | Limit | Remarks |
| --- | --- | --- |
| Maximum working voltage (V) | 30 | The voltage at any point inside the module at any time must not exceed 30 V relative to the battery negative terminal |
| Maximum stowed size (mm, L*W*H) | 600*600*600 | - |
| Maximum extended size (mm, L*W*H) | Unlimited | Consequences such as inconvenient use or inability to participate normally due to size are borne by the team itself |
| Data transmission | Video transmission image information: UDP | - |
| Data transmission | Competition-related data: MQTT+ProtoBuf | - |
| Protocol | See "Communication Protocol" | - |

**Installation requirements:**

**S47** Adhesive or sharp objects such as double-sided tape and screws must not be in contact with the Operator Room desktop.

<!-- p.19 -->
**S48** The Custom Terminal must not have live wires directly exposed.

**Usage specifications:**

> Note: The Operator Room provides an RJ45 network port that can be used to connect the Custom Terminal signal. Operators may connect it themselves.

**S49** Before use, the Custom Terminal must be connected to the data interface provided by the Operator Room to test whether it works normally.

**S50** The Custom Terminal must not use wireless transmitting/receiving devices.

#### 2.1.8 17mm Fluorescent Projectile Charging Device
Reserve mounting holes at specific positions on the robot with reference to the dimensions of the 17mm fluorescent projectile charging device.

*Figure 2-1 Installation Diagram of the 17mm Fluorescent Projectile Charging Device*
- [1] Projectile in launching state
- [2] 17mm fluorescent projectile charging device
- [3] Projectile in preset state
- Device dimension drawings (mm): heat sink width 10, 11 (hole spacing 7.30, 2-diameter 1.60 holes, counterbore diameter 3 depth 0.5, heights 17.14 and 7.14); board side view thicknesses 2, 1.83, 1; board width 9 (7.30, 3.30), height 19.60 (15.00), lead length 300, notch 2-R0.75; assembled board width 14, height 30, lead length 160, with + and - polarity marks.
- Installation views: dimension labels < 30 and < 20 (mm); two views each marked 120 degrees.

<!-- p.20 -->
> Note: The projectile in the launch state is the projectile at the position shown in the figure above, at the instant it contacts the friction wheels or other launching structure. The projectile in the preset state is the projectile immediately before the launch-state projectile in the feed path.

**Installation steps:**

> Note: In RMUL, robots do not need to install the fluorescent charging device.

1. Install the UV light board at the specified position on the robot. The installed boards must be placed parallel to and symmetric about the center plane of the projectile channel. The distance between the upper surfaces of the LED beads of the two boards must be less than 20 mm, and the front end face of the board must be less than 30 mm from the front end of the launch-state projectile. Every LED bead must provide a 120° illumination FOV. The installation position is shown in the figure above.
2. If the feed tube is metal, maximize the contact area between the feed tube and the light board and tighten the screws to aid heat conduction. A non-metal feed tube must have a heat sink installed.
3. After wiring the UV light board, the XT30 port may be connected to 12V or 24V power.

**Installation requirements:**

> Note:
> - It is recommended that the LED bead side of the UV light board be mounted tightly against the metal parts of the launcher, and the back of the LED beads be tightly against the heat sink. Leave at least 20 mm of clearance outside the heat sink so that flowing air can directly contact it.
> - It is recommended to keep conductive materials clear of the solder pads of the light board power wires to prevent short circuits.
> - It is recommended to avoid covering the back of the UV light board or the heat sink surface with tape, plastic or other parts that impair heat dissipation.
> - During use, check whether dirt blocks the LED beads or whether any bead is damaged. If so, replace promptly to avoid affecting Pre-Match Inspection.

**S51** The UV light board must be installed so that there is no obvious light leakage, to prevent UV radiation from injuring people.

**S52** The LED beads of the UV light board must be arranged along the direction in which projectiles travel in the feed path, and no structure may block the beads from illuminating the projectile, to ensure the projectile charging effect.

**S53** The maximum fire rate of the 17mm launching mechanism must be greater than or equal to 10Hz, and the Initial Launch Speed of the projectile must be greater than 20m/s. In self-testing, fire at the actual match-condition fire rate or the maximum fire rate of the launching mechanism, and the brightness must meet the self-test requirement. This requirement will be provided in a later update.

**S54** During Pre-Match Inspection of the 17mm fluorescent charging device, the robot must fire projectiles at the match-condition fire rate or the maximum fire rate of the launching mechanism.

**S55** If the official fluorescent charging device is used, the matching heat sink and its matching components must be used.

**S56** A self-made UV light board must use UV LED beads with a wavelength of 390-410nm.

**Suggestions for self-made UV light boards:**

- It is recommended that the LED bead emission angle be 120°.

<!-- p.21 -->
- It is recommended that the total luminous power of a single light board be 3W (6W for two boards).
- It is recommended that the circuit board material be aluminum-based or copper-based.
- For heat sink specifications, LED bead spacing, total light board length, etc., it is recommended to follow the fluorescent charging device.

#### 2.1.9 Others

**S57** In the design and manufacture of the robot, materials that are fragile, easily shed, or hard to clean, such as feathers and cotton wadding, must not be used. Any glue or adhesive material is prohibited for connecting the robot to the field or field props.

> Note: If the fragile or easily shed nature of a material is ambiguously defined on the market, a team may use such material in a match only after ensuring its strength and obtaining permission from the Pre-Match Inspection referee.
>
> To avoid potential risks caused by ambiguously defined material properties, for example the robot possibly being unable to enter the field, teams are advised not to use materials with such ambiguously defined properties.

**S58** When acquiring and assembling Energy Units, the robot must not leave obvious marks on or damage the Energy Unit.

> Note: A robot grasping the on-board Referee System modules may seriously affect the module functions. The consequences are borne by the team.

**S59** Except for the Dart launcher launching darts in the Dart System and the Aerial Robot taking off from the Hangar, a robot must not be separated into sub-robots or multiple subsystems connected by flexible cables, and must not actively throw or launch its own parts.

**S60** If the computing platform on any robot uses an operating system, it must be an open-source operating system, for example Linux and its derivatives, or RTOS. Closed-source operating systems such as Windows and macOS must not be used.

### 2.2 Specifications for Complete Finished Robots and Open-Source Robots

> Note:
> - Only teams that did not successfully take part in an offline competition of the 2026 University Series may field at most 1 unmodified RoboMaster Competition Robot Self-Assembled Version A, or at most 1 RoboMaster AI Robot 2020 Standard Version modified to meet the new-configuration conditions.
> - Other teams building their own robots may not merely modify the above robot products into new-configuration robots, and may not directly use their frame profiles or other important structural parts during construction. Only the motor couplings, launching mechanisms, feeding mechanisms and similar parts of the above robot products may be used.

In the RoboMaster University Series, the RMOC will define the ownership of robot intellectual property: only the students who took part in the design and manufacture, and the universities they represent, own the intellectual property of the relevant robot configuration. Only teams representing a university that owns the intellectual property of a robot configuration, with the relevant students as team members, are allowed to compete with that configuration. If another team chooses to reference that robot configuration, it must redesign the robot

<!-- p.22 -->
so that it meets at least 1 sufficient redesign condition or 3 non-sufficient redesign conditions. The motion mechanism of the robot (Ground Robot chassis, etc.) and the functional mechanism (Infantry Robot launching mechanism, Heavy Robot robotic arm, etc.) are each judged independently for redesign conditions, and the sum of the number of redesign conditions met by the two must reach the above standard. Once the conditions are met, the design is regarded as a new configuration, and the team may compete with the new-configuration robot. The types of redesign include but are not limited to the examples given in this text.

In addition, during the competition the RMOC will spot-check robots from time to time. Teams are obliged to show the RMOC the mechanical and circuit design drawings and related code files of their robots, and to answer related technical inquiries. The RMOC has the right to photograph/record the robot configuration and related information of teams.

**S61** Before robot Pre-Match Inspection, the team must submit photos of the robot to the designated channel. The photos must clearly show the main structure of the robot. If there is a protective shell, remove it before photographing the main body.

**S62** When a team uses a complete finished robot or an open-source robot and redesigns it, the team must submit a document describing the changes to the designated channel.

**S63** When robots fail to meet the redesign conditions relative to each other and no open-source robot is cited, the owner of the intellectual property is defined as the team that first used that robot in an official match. That is, as long as that team is still taking part in the RoboMaster University Series, all robots fielded later by other teams must meet the redesign conditions relative to the robot that was fielded earlier.

**S64** When a team uses a complete finished robot, references another team's configuration, or redesigns from an open-source solution, the Dart launcher, the dart body, the Hangar and the Aerial Robot are each treated as an independent judging unit. Each unit that needs redesign must meet at least 1 sufficient redesign condition or 3 non-sufficient redesign conditions. Redesign conditions of different units are not combined.

#### 2.2.1 Sufficient Redesign

Sufficient redesign refers to improvements to the core mechanisms of the robot, involving a wide range of related systems.

1. Chassis
   - Change of the wheel set scheme. For example: a change among Mecanum wheels, steering wheels, omnidirectional wheels, Ackermann steering wheels, tracks, etc.
   - Change of the wheel set transmission scheme. For example: a change between power below the suspension and power above the suspension.
   - Change of the suspension scheme. For example: a change among double wishbone suspension, torsion beam suspension, double trailing arm suspension, lifting suspension, etc.
   - Change of chassis power. For example: DC or AC, brushed or brushless, geared or direct drive.
   - Change of chassis form. For example: a change among frame type, laminated plate type, monocoque type, etc.
2. Gimbal
   - Change of the gimbal transmission stack. For example: a change in the nesting relationship or number of Yaw, Pitch and Roll axes.
   - Change of the feeding principle. For example: the robot feed path changing from simple direct feeding to feeding to the launching mechanism through the Yaw axis joint.
   - Change of magazine position. For example: a change among the magazine being fixed to the chassis, fixed to the Yaw axis, fixed to the Pitch axis, etc.
   - Change of the gimbal motor transmission method. For example: a change among direct drive, belt pulley, linkage, gears, etc. (excluding interchange among belt pulleys, gears and sprockets).

<!-- p.23 -->
3. Actuator
   - Change of topology of mechanisms other than the end effector. For example: a change in the order, number or type of combination of revolute joints, prismatic joints, etc.
   - Improvement of the power efficiency of the actuator. For example: fewer power units with unchanged function, an unchanged number of power units with added effective functions, or more power units with added effective functions.
4. Dart System
   - Dart body: change of the overall aerodynamic configuration or of the way control force is generated. For example: changing from a conventional main wing-tail wing layout to a flying wing layout; or overall restructuring of the function allocation of the front and rear aerodynamic control surfaces, with the aerodynamic layout, actuators and control coordination redesigned accordingly.
   - Dart launcher: change of the working principle of the launch power or of the core transmission topology; change of the kinematic chain topology of the dart feeding and loading core mechanism. For example: changing from elastic energy storage ejection to friction wheel acceleration; redesigning the drive kinematic chain so that the way power is input, transmitted and applied to the dart body changes in principle.
5. Aerial System
   - Hangar: change of the principle or kinematic chain topology of the core mechanism for entering/leaving the Hangar, transfer or docking. For example: changing from each bay parking and taking off/landing independently to a shared take-off/landing platform with an active transfer mechanism; or changing from fixed passive guided docking to active multi-axis alignment docking, with sensing, actuation and control coordination restructured accordingly.
   - Aerial Robot: change of the overall layout of the lift units or of the principle of the attitude control mechanism; change of the main load-bearing system of the airframe. For example: changing from rotors distributed in a plane to a coaxial arrangement, or from fixed-axis rotors to actively tilting rotors, actually changing the load transfer relationship among the power units, on-board equipment and landing structure.

#### 2.2.2 Non-Sufficient Redesign

Non-sufficient redesign refers to improvements with less involvement of related systems.

- A change of more than 10% in key parameters (for example: suspension hardpoint positions, track width, wheelbase, effective acceleration stroke of the Dart launcher, the dart body, local aerodynamic geometric parameters of the Aerial Robot, etc.).
- A change in the number of effective powered wheel sets.
- A change of the reduction ratio of the power motors of the chassis, gimbal, Dart launcher or Hangar, or of the local transmission path or transmission method of an actuator.
- A change in the placement of at least 3 on-board Referee System modules, each of which causes a change in the topology of the robot system.
- Addition of a new functional module related to the original function of the robot. For example: an independent rescue device, a small turntable for the Video Transmitter Module, Energy Unit steering, the addition of a vision module; modules related to Dart launcher loading and launching; sensing, feedback and actuation modules of the Aerial System and dart body.
- A change between longitudinal and transverse mounting of the friction wheels.

<!-- p.24 -->
- A change of power source. For example: pneumatic or electric.
- A change of the type or scheme of the end effector. For example: rotary gripping changed to translational gripping.
- A change of the layout of core electronic devices (main controller, power supply, computing platform, sensing modules). For example: moving the position from the gimbal to the chassis.
- A change of gimbal rotation range from limited to unlimited.
- Adjustment of the size, number or mounting angle of local aerodynamic components of the dart, for example a change in tail wing area, tail wing mounting angle, or airfoil camber.
- Replacement of the dart material, together with adjustment of the mass distribution or surface characteristics.
- Adjustment of the layout or structural form of the feeding mechanism of the Dart launcher, such as a change in the shape of the feeding track or optimization of the shape of the pusher mechanism.
- Revision of the transmission ratio or transmission path between components of the launcher.

#### 2.2.3 Invalid Redesign

Invalid redesign refers to changes with little effect on core functions.

Invalid redesign includes but is not limited to the following changes:

- Changes to non-primary load-bearing structures and shield/guard structures. For example: a change in cutouts or in shape.
- A change in the model or quantity of standard parts.
- Interchanging cylinders and electric push rods.
- Routine counterweight leveling, replacing only the servo or battery model, or modifying only the mounting interface to the launcher.
- Substitution of materials with the same characteristics. For example: interchanging fiberglass board and carbon fiber board.
- Changes with no change in principle. For example: changing the upper feed hard tube to a soft tube or other hardness changes.
- A Hangar changing only the outer box or hatch cover shape, or duplicating identical parking bays.
- An Aerial Robot replacing only the propeller blades, motors, battery or flight controller model, modifying only PID or off-the-shelf firmware configuration, or adding only non-primary load-bearing propeller guards.
- A Dart launcher replacing only the motor, spring or rubber band specifications, or changing only the housing or the way darts are mounted.

### 2.3 Definition and Scope of Third-Party Finished Modules and Finished Systems

**S65** Unless otherwise specified, teams are prohibited from using third-party finished modules and finished systems when building robots.

- Third party: any party other than the RMOC and the participating team itself.
- Finished module: a functional component with a specific function made up of several basic functional components, which can be used to form a system with complete functions. For example:

<!-- p.25 -->
  a robotic arm, a chassis, a supercapacitor control board and its matching code, a gimbal, a dart, a wheel set with suspension, a feeding mechanism, a launching mechanism, a mainboard, a CPU, a GPU, memory, a hard disk.
- Finished system: a system with complete functions formed from a combination of several finished modules or self-made modules (including at least one finished module). For example: a laptop, an all-in-one desktop computer.

> Note: The computing platforms used on the Radar computing platform side and the Custom Terminal may be finished modules and finished systems, and are not subject to this rule.

**Exemption for commercially available general-purpose products**

To encourage teams to use general-purpose products that have long-term value in scientific research and engineering practice, commercially available general-purpose products are allowed and not regarded as violations, provided the following conditions are met.

A commercially available general-purpose product must meet all of the following conditions:

- Public sale requirement
  - It is produced or sold by a legally registered enterprise or institution.
  - Before the registration deadline, it has been publicly sold to society through channels such as the company's official website, e-commerce platforms and distributors, and not only through RoboMaster teams or channels related to a specific competition.
- General-purpose use requirement
  - The product is mainly intended for the general industrial, scientific research, education or consumer market.
  - Its promotional materials must not present RoboMaster or any other single competition as the sole or primary usage scenario.
  - A product whose functions or specifications are clearly customized for RoboMaster or another specific competition, or which is sold only through competition channels, is not regarded as a commercially available general-purpose product.

**Price limit**

- Finished module: the unit price of the product must not exceed RMB 5000.
- Finished system: the unit price of the product must not exceed RMB 8000.
- The price is based on the official list price or the tax-inclusive transaction price on mainstream sales channels. The RMOC reserves the right of final interpretation.

**Exemption conditions for computing platforms**

A computing platform that meets the public sale requirement and the general-purpose use requirement needs to meet only one of the price condition and the peak computing power condition:

- Price condition: the same as for finished systems.
- Peak computing power condition:
  - Accelerated computing power not higher than 160 TOPS (based on the AI TOPS INT8 sparse value);

<!-- p.26 -->
  - General computing power not higher than 25GHz. General computing power is calculated by summing the nominal base frequency of all processor cores core by core (that is, Σ(frequency * number of cores) ≤ 25GHz).

**Compliance certification**

In addition, if a product meets the following compliance certification conditions, this can help support the judgment that it is a commercially available general-purpose product.

- Electronic and electrical products should meet the basic safety and electromagnetic compatibility standards usually required by their target market.
- If the product is sold in the Chinese market and holds any of the following certifications, this can be regarded as strong supporting evidence that it was designed and produced for the general market:
  - China CCC certification (for products within the mandatory certification catalog);
  - IECEE CB Scheme certification;
  - International or regional safety certifications such as UL / ETL / TUV / CSA;
  - Electromagnetic compatibility or radio certifications such as FCC / IC / CE / RCM / KC.

**Prohibited situations and discretion**

If a product falls under any of the following situations, the RMOC may still determine it to be a prohibited finished module even if it meets some of the above conditions:

- It is clearly developed or customized specifically for RoboMaster or other competitions and is sold only to participating teams in related groups, internal channels or a small circle.
- Although it has an online display page, its main slogan, product name or packaging uses "RoboMaster only", "for use in a certain competition only" or the like as the core selling point.
- Its market launch time is clearly tied to the competition season cycle, appearing only briefly around the season, with no continuous sales record toward a broad market.
- It attempts to disguise a product with a clear competition orientation as a general-purpose product through simple renaming or minor revisions.
- The RMOC determines that the product's degree of integration seriously replaces the core technical difficulties of the competition, so that the competition loses its proper technical challenge and fairness.

The RMOC has the right to require teams to provide the following materials to determine the nature of a product:

- Product purchase invoice or order record;
- Product manual, datasheet, advertisement or promotional materials;
- Links to the product's official website and e-commerce pages, and historical version information;
- Relevant certification certificates or test reports;
- Other materials that can prove the product's launch time, sales scope and purpose.

The RMOC reserves the right of final interpretation and ruling on whether a product is a "commercially available general-purpose product".

<!-- p.27 -->
### 2.4 Robot Technical Specifications

> Note:
> - Maximum stowed size: the robot must have one state that meets the maximum stowed size limit, including the Referee System and its brackets.
> - Maximum extended size: the limit on the maximum size of the robot at any moment, based on the limit posture to which the robot's mechanical structure may possibly extend, including the Referee System and its brackets. When a Combined System is physically connected to system units, all connected system units count toward the maximum extended size of the Combined System. During Pre-Match Inspection, teams must proactively demonstrate all deformations of the mechanical structure, and in any form before, during and after deformation the robot must not exceed the maximum extended size requirement.
> - In this section, the length, width and height of a robot correspond to its lengths along the X axis, Y axis and Z axis of the body coordinate system. For the Aerial Robot and the Radar, the X axis and Y axis directions may be chosen freely, and the Z axis is perpendicular to the plane on which it is placed. Coordinate-system-related specifications do not apply to the Dart System.

**S66** Except for the Radar System, the Custom Terminal and the modular 42mm launching mechanism, a robot must not be split into independent individual units when its size changes. In addition, the connection structure must meet the following requirements:

- Mechanical hinged or ball connections (for example: hinges, rotating shafts, ball bearings, linear guides) and other movable connections interlocked through solid body structure are allowed.
- Flexible traction connections (for example: cables, ropes, chains, belts) and connections that rely on suction or friction to be maintained (for example: suction cups, magnetic attachment, connections held by friction alone) are prohibited.

> Note: Loosening or tightening parts such as screws and cable ties without removing them is not regarded as splitting into independent individual units.

#### 2.4.1 Heavy Robot

**S67** The Heavy Robot must be able to move horizontally and to grab Energy Units in the Resource Zone.

> Note: In RMUL, the Heavy Robot does not need the function of grabbing Energy Units.

**S68** The Heavy Robot build parameters must meet the following requirements:

**Table 2-5 Heavy Robot build parameter description**

| Item | Limit | Remarks |
| --- | --- | --- |
| Operation mode | Unrestricted; at most 1 Remote Controller and 1 Custom Terminal configured | - |
| Maximum total power supply capacity | 300 | - |

<!-- p.28 -->
| Item | Limit | Remarks |
| --- | --- | --- |
| (Wh) | | |
| Maximum operating voltage (V) | 30 | The voltage at any point inside the robot at any moment must not exceed 30V relative to the battery negative terminal |
| Launching mechanism | Modular 42mm launching mechanism | Can only be installed during the seven-minute Round |
| Maximum weight (kg) | - 36: includes battery and Referee System weight, but excludes the modular 42mm launching mechanism weight.<br>- 41: includes battery, Referee System and modular 42mm launching mechanism weight. | - |
| Maximum stowed size (mm, L*W*H) | The robot has a state with length, width and height not greater than 600*600*600 | The maximum stowed size does not include the modular 42mm launching mechanism |
| Maximum extended size (mm, L*W*H) | One of the following requirements must be met:<br>- Requirement 1: In any situation, the length, width and height of the robot must not exceed 1200*1200*1100.<br>- Requirement 2 (both must be met at the same time):<br>(1) Take the outer edge of the body on the positive X axis direction of the robot body coordinate system as the Y' axis, choose any point on the Y' axis as the origin O to establish an X'Y'Z' coordinate system. With the robot chassis locked, other movable structures extending in the negative X axis, positive Y axis and negative Y axis directions must not go beyond x'∈[-900,0], y'∈[-900,900], z'∈[0,1250]<br>(2) Take the outer edge of the body on the negative X axis direction of the robot body coordinate system as the Y' axis, choose any point on the Y' axis as the origin O to establish an X'Y'Z' coordinate system. With the robot chassis locked, other movable structures extending in the positive X axis, positive Y axis and negative Y axis directions must not go beyond | - The modular 42mm launching mechanism must be installed during Pre-Match Inspection.<br>- The actual Pre-Match Inspection method for Requirement 2: place the robot on level ground with the robot against the limit surface and the positive X axis direction of the robot perpendicular to the limit surface. The robot may be translated along the limit surface to select its initial position. After the initial position is determined, the chassis must not translate or rotate, and with the robot's mechanisms in any reachable combination of states, no part of the robot may go beyond the cuboid space with the floor as the ground, the rear side as the limit surface, a forward depth of 900mm, a lateral width of 1800mm (900mm on each side of the lateral centerline) and a vertical height of 1250mm.<br>Example:<br>As shown in the left figure below, the robot in this posture meets the maximum extended size requirement. Afterwards, without any deformation, |

<!-- p.29 -->
| Item | Limit | Remarks |
| --- | --- | --- |
| (Maximum extended size, continued) | x'∈[0,900], y'∈[-900,900], z'∈[0,1250] (figure: three views of a robot inside the bounding box, labeled 1250, 900, 1800) | exceeding the specified range due to interaction with the outside (as shown in the right figure below, crossing terrain) is not regarded as failing the maximum extended size requirement. (figure: two views, labeled 1250 and 900)<br>As shown in the left figure below, if the robot does not exceed the specified range when interacting with the outside, but exceeds the specified range when not interacting with the outside (as shown in the right figure below), it is regarded as failing the maximum extended size requirement. (figure: two views, labeled 1250 and 900) |
| Referee System | - Small Armor Module<br>- Video Transmitter Module with camera (transmitter end)<br>- Field Interaction Module<br>- Positioning Module (not applicable in RMUL)<br>- Main Controller Module<br>- Power Management Module<br>- Light Indicator Module | - |

**S69** The modular 42mm launching mechanism must be able to launch 42mm projectiles.

<!-- p.30 -->
**S70** The build parameters of the modular 42mm launching mechanism must meet the following requirements:

**Table 2-6 Modular 42mm launching mechanism build parameter description**

| Item | Limit | Remarks |
| --- | --- | --- |
| Maximum total power supply capacity (Wh) | - | No battery may be installed; it is powered directly by the robot |
| Maximum operating voltage (V) | 140 | The voltage at any point inside the module at any moment must not exceed 140V relative to the battery negative terminal |
| Maximum weight (kg) | 6 | Includes Referee System weight |
| Maximum stowed size (mm, L*W*H) | The modular 42mm launching mechanism has a state with length, width and height not greater than 400*400*400 | - |
| Referee System | 42mm Speed Monitor Module | - |

> Note: During Pre-Match Inspection, the modular 42mm launching mechanism will be installed and removed multiple times. It is recommended to keep each installation or removal within 1 minute. Any consequences for the Pre-Match Inspection progress are borne by the team.

#### 2.4.2 Infantry Robot

**S71** The Infantry Robot must be able to move horizontally and to launch 17mm projectiles.

**S72** The Infantry Robot build parameters must meet the following requirements:

**Table 2-7 Infantry Robot build parameter description**

| Item | Limit | Remarks |
| --- | --- | --- |
| Operation mode | Unrestricted; at most 1 Remote Controller and 1 Custom Terminal configured | - |
| Maximum total power supply capacity (Wh) | 300 | - |
| Maximum operating voltage (V) | 30 | The voltage at any point inside the robot at any moment must not exceed 30V relative to the battery negative terminal |

<!-- p.31 -->
| Item | Limit | Remarks |
| --- | --- | --- |
| Launching mechanism | 1 17mm launching mechanism | - |
| Maximum weight (kg) | 28 | Includes battery weight and Referee System weight |
| Maximum stowed size (mm) | The robot has a state with length, width and height not greater than 600*600*600 | - |
| Maximum extended size (mm) | In any situation, the length, width and height of the robot must not exceed 800*800*800 | - |
| Referee System | - Small Armor Module<br>- 17mm Speed Monitor Module<br>- Video Transmitter Module with camera (transmitter end)<br>- Field Interaction Module<br>- Positioning Module (not applicable in RMUL)<br>- Main Controller Module<br>- Power Management Module<br>- Light Indicator Module<br>- 17mm fluorescent projectile charging device<br>- Supercapacitor Management Module | The weight is 3.25kg |

#### 2.4.3 Sentry Robot

**S73** The Sentry Robot must be able to move horizontally and to launch 17mm projectiles.

**S74** The Sentry Robot build parameters must meet the following requirements:

**Table 2-8 Sentry Robot build parameter description**

| Item | Limit | Remarks |
| --- | --- | --- |
| Operation mode | Unrestricted; at most 1 Remote Controller used for debugging | - |
| Maximum total power supply capacity (Wh) | 300 | - |

<!-- p.32 -->
| Item | Limit | Remarks |
| --- | --- | --- |
| Maximum operating voltage (V) | 30 | The voltage at any point inside the robot at any moment must not exceed 30V relative to the battery negative terminal |
| Launching mechanism | 1 17mm launching mechanism | - |
| Maximum weight (kg) | 28 | Includes battery weight and Referee System weight |
| Maximum stowed size (mm) | The robot has a state with length, width and height not greater than 600*600*600 | - |
| Maximum extended size (mm) | In any situation, the length, width and height of the robot must not exceed 800*800*800 | - |
| Referee System | - Small Armor Module<br>- 17mm Speed Monitor Module<br>- Field Interaction Module<br>- Positioning Module (not applicable in RMUL)<br>- Main Controller Module<br>- Power Management Module<br>- Light Indicator Module<br>- 17mm fluorescent projectile charging device<br>- Supercapacitor Management Module<br>- Video Transmitter Module with camera (transmitter end) | The weight is 3.25kg |

#### 2.4.4 Aerial System

The Aerial System consists of the Aerial Robot and the Hangar.

**S75** The Aerial Robot must be able to hover continuously for at least 10 s.

**S76** The Aerial Robot build parameters must meet the following requirements:

<!-- p.33 -->
**Table 2-9 Aerial Robot build parameter description**

| Item | Limit | Remarks |
| --- | --- | --- |
| Operation mode | Fully automatic; equipped with a Remote Controller for emergency propeller stop | Can communicate with the Hangar while inside the Hangar |
| Maximum total power supply capacity (Wh) | 4 | - |
| Maximum operating voltage (V) | 30 | The voltage at any point inside the robot at any moment must not exceed 30V relative to the battery negative terminal |
| Launching mechanism | Installing a launching mechanism is not allowed | - |
| Maximum weight (kg) | x | Size and weight limits are linearly related: y = (0.3225 - x) / 0.001225, where x∈[0.15,0.249]; the result is rounded to an integer; when x < 0.15, y = 141 |
| Maximum extended size (mm) | When the weight of the Aerial Robot is x, in any situation the length, width and height of the robot must not exceed y*y*y | Size and weight limits are linearly related: y = (0.3225 - x) / 0.001225, where x∈[0.15,0.249]; the result is rounded to an integer; when x < 0.15, y = 141 |

**S77** Teams must provide their own rigid open-top container (such as a lidless box) matching the size of each Aerial Robot. During Pre-Match Inspection, the maximum allowed extended size corresponding to the measured weight of the robot is calculated, and the robot is placed in the container. The inner length, width and height of the container must not exceed the allowed size limit for that weight, and the robot must not exceed the interior space of the container in any extended state, as shown in "Figure 2-2 Aerial Robot Pre-Match Inspection diagram".

*Figure 2-2 Aerial Robot Pre-Match Inspection diagram*

- Labels: L, W, H (length, width, height of the container interior)

<!-- p.34 -->
**S78** All propeller blades of the Aerial Robot must be equipped with an omnidirectional guard structure. The structure must fully cover the swept space of each blade's rotation, that is, form a continuous closed boundary above, below and around the blade. The aperture of the guard structure must be smaller than 17mm. During operation, the guard structure must not intrude into the swept space of the blades due to breakage, detachment or deformation.

During Pre-Match Inspection, the following two tests must be passed:

1. A 17mm projectile placed at any position on the guard structure must not be able to pass through.
2. The Aerial Robot is placed at a height of 500mm and allowed to fall freely onto a floor covered with field rubber mat from three orientations: bottom, side and top. The guard structure and the blades must show no obvious deformation or damage.

> Note: Flexible materials are recommended for Aerial Robot propeller blades.

*Figure 2-3 Aerial Robot propeller guard diagram*

**S79** The Aerial Robot must be paired with a Remote Controller for emergency propeller stop and may be paired only with that Remote Controller. At any moment, this Remote Controller must be able to emergency-stop the propellers of all Aerial Robots on the field at the same time. In addition, the Aerial Robot must automatically stop its propellers whenever it loses Remote Controller signal control at any moment.

> Note:
> - During Pre-Match Inspection, the Remote Controller must be turned off to demonstrate the automatic propeller stop function of the Aerial Robot.
> - After taking off and stopping its propellers, the Aerial Robot lands within the field and may be hit or run over by other robots. In addition, the Aerial Robot also suffers large impacts when it strikes targets. Teams are advised to design for strength and cushioning to avoid damage to the Aerial Robot.

**S80** Teams must design and install, on their own, navigation appearance lights to improve the recognizability of the robot. The navigation appearance lights must ensure that the projection of the Aerial Robot's top side can be effectively observed. The specific requirements are as follows:

- The light group must be a circular light group, installed at the center of the top surface of the Aerial Robot, firmly connected to the airframe and naturally fitted to it, with no obvious tilt, offset, partial obstruction, overhang, bulging or wrinkling. The angle between the normal of the light group mounting surface and the positive Z axis of the body coordinate

<!-- p.35 -->
  system must not exceed 10°, and the mounting surface must be on the highest surface of the airframe (excluding motors, motor mounts and propeller blades).
- The light group must use XL-3528SURUBC LED beads (red-blue dual-color LED, SMD3528 package, no built-in control IC, front emitting), 7 in number. The beads must be evenly distributed with one bead at the center, and the diameter of the enveloping circle of the outermost edge of the beads must not exceed 24mm.
- The light group must be DC driven and continuously lit at rated voltage and current; periodic PWM or scanning drive of the LEDs must not be used. Within the specified exposure range of the designated camera, there must be no light/dark stripes or frame-to-frame brightness fluctuation that affect recognition. There must be no obvious brightness or color differences among the beads, the emitted color must be stable, and there must be no obvious color cast or localized whitening.
- The light group must be able to switch between red and blue to match the team's color in the match. The red side's light group must display red (target RGB value #FF0000), and the blue side's light group must display blue (target RGB value #0000FF). The red side must turn the red LEDs on and the blue LEDs off; the blue side must turn the blue LEDs on and the red LEDs off.

*Figure 2-4 Light group diagram*

> Note: The self-test requirements for the navigation appearance lights will be provided in a later update.

**S81** Teams may install indicator lights on the Aerial Robot for communication. The specific requirement is: the color of the indicator lights must match the team's color in the match. The red side's indicator lights must display red, and the blue side's indicator lights must display blue.

**S82** The Hangar must be able to store Aerial Robots.

**S83** The Hangar build parameters must meet the following requirements:

**Table 2-10 Hangar build parameter description**

| Item | Limit | Remarks |
| --- | --- | --- |
| Operation mode | Unrestricted; at most 1 Remote Controller used for debugging | - |
| Maximum total power supply capacity (Wh) | 300 | - |

<!-- p.36 -->
| Item | Limit | Remarks |
| --- | --- | --- |
| Maximum operating voltage (V) | 30 | The voltage at any point inside the robot at any moment must not exceed 30V relative to the battery negative terminal |
| Aerial Robot loading capacity limit | 4 | - |
| Maximum weight (kg) | Unlimited | - |
| Maximum stowed size (mm, L*W*H) | 300*300*200 | - |
| Maximum extended size (mm, L*W*H) | 600*300*400 | Refer to the Hangar platform in the "RoboMaster 2027 University Championship Rules Manual"; the Hangar platform is adjacent to the Power Rune pillar, so pay attention to the extension direction |
| Referee System | - Main Controller Module<br>- Power Management Module<br>- Video Transmitter Module with camera (transmitter end) | - |

#### 2.4.5 Dart System

The Dart System consists of the dart and the Dart launcher. The Dart launcher serves as the carrier of the dart and provides the initial power for the dart.

**S84** The dart build parameters must meet the following requirements:

**Table 2-11 Dart build parameter description**

| Item | Limit | Remarks |
| --- | --- | --- |
| Maximum total power supply capacity (Wh) | 4 | - |
| Maximum operating voltage (V) | 8.4 | The voltage at any point inside the robot at any moment must not exceed 8.4V relative to the battery negative terminal |
| Maximum weight (kg) | 0.3915 | Includes the dart trigger device |

<!-- p.37 -->
| Item | Limit | Remarks |
| --- | --- | --- |
| Maximum extended size (mm, L*W*H) | 250*250*150 | - The length along the dart flight direction must not exceed 250<br>- The dart wingspan must not exceed 250 |

*Figure 2-5 Dart flight direction diagram*

- Axis labels: x, y, z

> Note: Take the forward direction of the dart trigger device as the dart flight direction; the y and z directions in the figure are the wingspan and height of the dart.

**S85** The Dart launcher build parameters must meet the following requirements:

**Table 2-12 Dart launcher build parameter description**

| Item | Limit | Remarks |
| --- | --- | --- |
| Operation mode | Unrestricted; at most 1 Remote Controller configured | Adapting to the Referee System serial port is recommended |
| Rotation angle (°) | - Yaw axis angle: unlimited<br>- Pitch axis angle: 25-45 | - |
| Maximum total power supply capacity (Wh) | 300 | - |
| Maximum operating voltage (V) | 30 | The voltage at any point inside the robot at any moment must not exceed 30V relative to the battery negative terminal |
| Maximum operating power (W) | Unlimited | - |
| Dart loading capacity limit | 4 | - |
| Dart Initial Launch Speed | Unlimited | When the dart Initial Launch Speed exceeds 25m/s, the Referee System |

<!-- p.38 -->
| Item | Limit | Remarks |
| --- | --- | --- |
| | | may be unable to detect the dart |
| Maximum weight (kg) | 25 | Includes battery and Referee System weight; no dart needs to be loaded when measuring the maximum weight |
| Maximum extended size (mm, L*W*H) | 1000*600*1000 | - The maximum extended size is the size with the Dart launcher loaded with 4 darts<br>- In any situation, the orthographic projection of the Dart System on the ground must not go beyond a 1000*600 rectangular area, and the highest point of the Dart System must be no more than 1000 above the ground<br>- The orthographic projections on the ground of the Dart launcher and the dart to be launched must at no time go beyond the outermost edge of the Dart System bottom frame. The part of the outermost edge of the Dart System bottom frame that contacts the ground must be a closed rectangle of size 950*550, with an assembly tolerance of ±50mm allowed, as shown in "Figure 2-6 Dart System size limit diagram". |
| Referee System | - Main Controller Module<br>- Power Management Module | The weight is 0.22kg |

*Figure 2-6 Dart System size limit diagram*

- [1] Dart launcher
- [2] Dart System bottom
- [3] Dart body
- [4] Outermost edge of the contact plane

<!-- p.39 -->
**S86** The Dart launcher must be able to load and launch Darts over 5 m, and the Dart must be fitted with a Dart trigger device. During Pre-Match Inspection, the team must provide a video of the Dart launching system launching a Dart over 5 m.

**S87** The Dart must locate the Dart detection module and control its flight direction by propeller (at most 1 allowed), control surfaces, jets, etc., finally striking the Dart detection module to achieve the hit effect. The Dart thrust-to-weight ratio must be less than 1.

**S88** The Dart trigger device must light up when the Dart is launched, and viewed from above, the Dart System must have no exposed light sources other than the Referee System and the Dart trigger device.

> Note: If the Dart trigger device does not light up when the Dart is launched, the Referee System will be unable to detect the Dart launch normally.

**S89** The Dart trigger device contains built-in red and blue dual-color LED beads, set to the corresponding color according to the team's red or blue side in the match.

> Note:
> - After launch, the Dart lands in the field and may be hit or run over by other robots. In addition, the Dart also suffers a large impact when it hits the target. Teams are advised to design for strength and cushioning to avoid damage to the Dart.
> - When the Dart trigger device shows an alternating red and blue flashing light effect, damaged beads or other abnormal conditions, the trigger device is damaged, and the Base and Outpost may be unable to detect Dart hits. Replace it with a spare Dart trigger device yourself; otherwise all resulting losses are borne by the team.

**S90** Schemes that use compressed air to directly propel the Dart for launch are prohibited.

**S91** The Dart System is only allowed to be in the ready-to-launch state during the seven-minute Round.

> Note: Ready-to-launch state: the energy storage element that provides initial kinetic energy to the Dart is in a tensioned, inflated or rotating state. Energy storage elements include but are not limited to rubber bands, cylinders and friction wheels.

##### 2.4.5.1 Installation Specifications

**S92** The Dart must be fitted with the officially designated Dart trigger device.

> Note: The officially designated Dart trigger device this season is "Dart Trigger Device 2".

The mass of the Dart trigger device is about 39.5 g ± 2 g. Its shape and dimensions are shown in the figure below. Refer to the Dart trigger device dimensions and reserve mounting holes at the head of the Dart.

<!-- p.40 -->
*Figure 2-7 Dart trigger device diagram*

- [1] Power supply negative
- [2] Power supply positive
- [3] Serial cable
- [4] Logo
- [5] Dart trigger device
- [6] Mounting ear
- [7] 3P 2.54 mm ribbon cable
- Dimension labels in the drawing (mm): 150; 28; 11.60; 8.00; 13.00; 9.50; 3.50; 0.00; hole callout 4-Ø2.50 THRU, countersink Ø5.1 x 90°; 43.50; 38.40; 25.34; 45.10; 42.10; Ø16.60; 14.08; 8.70; 19.75; 4-Ø3.00 depth 2; section view labelled A-A

###### 2.4.5.1.1 Installation Steps

1. Fix the Dart trigger device at the head of the Dart using 8 M2.5 countersunk screws and 4 locating pins.
2. Connect the power supply port of the Dart trigger device to a 5 V supply.

###### 2.4.5.1.2 Installation Requirements

**S93** The Dart trigger device becomes dim when the battery voltage is low. Teams must ensure that the battery voltage used by the Dart during the match is at least 4 V. If the actual operating voltage of the Dart trigger device is below 4 V, the Base and Outpost may be unable to detect Dart hits.

**S94** After the Dart trigger device is installed, ensure that its top, bottom, left and right sides are not blocked by the Dart structure. The upper hemisphere with a radius of 125 mm centered on the center of the bottom face of the Dart trigger device must be free of any obstruction, as shown in the figure below.

<!-- p.41 -->
*Figure 2-8 Dart trigger device no-obstruction zone diagram*

- [1] Left
- [2] Top
- [3] Right
- [4] Bottom
- [5] No-obstruction zone
- [6] Unrestricted area inside the Dart trigger device

**S95** A Dart camera or other devices may be installed in the internal cavity of the Dart trigger device; the installation area must not exceed the shaded area shown in the figure below.

*Figure 2-9 Dart trigger device internal cavity diagram*

- [1] Shaded area
- Dimension label: Ø16.60; section view B-B

##### 2.4.5.2 Visual Features

The visual feature used to assist Dart System aiming is the green integrated LED bead installed on the Dart detection module. For specific dimensions, see the descriptions of the Outpost and Base in the

<!-- p.42 -->
"RoboMaster 2027 University Championship Rules Manual".

#### 2.4.6 Radar System

**S96** The Radar System consists of a computing platform end and a sensor end, which must be connected by a cable and be able to display a debugging screen.

**S97** The manufacturing parameters of the Radar computing platform end must meet the following requirements:

**Table 2-13 Radar computing platform end manufacturing parameters**

| Item | Limit | Remarks |
| --- | --- | --- |
| Operating mode | Fully automatic; at most 1 Remote Controller configured for debugging | - |
| Max power (W) | 750 | If the total power generated during Radar System use exceeds the max power, mains power to the Radar computing platform end will be cut off for that round, and all resulting consequences are borne by the team |
| Supply voltage (V) | 220 | This is the mainland China mains standard; other countries and regions may refer to the local mains standard, or use another power supply that meets general power supply standards |
| Supply frequency (Hz) | 50 | This is the mainland China mains standard; other countries and regions may refer to the local mains standard |
| Max extended size (mm) | Under any circumstances, the length, width and height of the Radar computing platform must not exceed 600*350*600 | - |
| Referee System | - Main Controller Module<br>- Power Management Module | Weight 0.22 kg |

**S98** The parameters of the Radar sensor end are as follows:

**Table 2-14 Radar sensor end parameters**

| Item | Limit | Remarks |
| --- | --- | --- |
| Max extended size (mm) | The length and width of the Radar sensor end must not exceed | - The Radar sensor bracket height is recommended to be 1.2 m |

<!-- p.43 -->
| Item | Limit | Remarks |
| --- | --- | --- |
|  | the placement platform of the Radar sensor end; its height must not exceed 1500 under any circumstances | or above<br>- Cables used for connection are not counted in the size<br>- The radio receiving device included in the Radar sensor end may be separated from the main body of the Radar sensor end, but its length and width must not exceed the placement platform of the Radar sensor end |
| Max operating voltage (V) | 60 | The voltage at any point inside the robot must not exceed 60 V relative to the battery negative at any time |

##### 2.4.6.1 Installation Specifications

The Radar sensor end and the Radar computing platform end are installed far apart; teams are advised to reserve an effective cable length of at least 5 m for the connecting cable.

##### 2.4.6.2 Computing Platform End

During the three-minute Setup Period, the team must place the computing platform end on the designated table near the Radar Base. The Radar System's Referee System may only be installed on the computing platform end.

**S99** No wireless devices may be installed or used on the computing platform end. If a wireless device cannot be removed, it must be disabled in the operating system.

**S100** The Main Controller Module and Power Management Module must meet the module installation specifications and be firmly installed on the Radar computing platform end. The Referee System power may share the computing platform end's power supply or use the battery designated for this season.

> Note:
> - The official AC supply is 220 V 50 Hz, with 1 new-national-standard 5-hole socket, into which single-phase two-pole and single-phase three-pole plugs can be inserted at the same time. Teams must prepare power converters according to their own situation.
> - The RMOC only guarantees that the official monitor at the Radar Base and the HDMI signal cable provided by the RMOC work normally; teams must resolve connection issues themselves.

##### 2.4.6.3 Sensor End

> Note: Teams must fit protective covers to their equipment to prevent damage from projectile hits during the match.

**S101** The sensor end must be fixed on the Radar sensor bracket and placed on the Radar Base.

**S102** The radio receiving device must be installed on the Radar sensor end.

**S103** Teams must design the Radar sensor bracket themselves to raise the sensor installation height.

<!-- p.44 -->
**S104** The dimensions of the Radar sensor bracket must allow it to be placed on the installation plane of the Radar Base. For Radar Base specifications, see the descriptions of the Radar Base in the "RoboMaster 2027 University Championship Rules Manual". Signal transmission and power supply for the sensor end must be resolved by the team.

<!-- p.45 -->
## 3 Referee System Installation Specifications

Users are advised to first read the manual of each Referee System module to understand its function and installation method. After correctly installing the Referee System modules, read the "Referee System User Manual" to understand the functions of the whole Referee System.

File download address: https://bbs.robomaster.com/wiki/20204847/804050?source=7

When installing and using the Referee System, refer to the following suggestions:

- While the robot is running, no Referee System module should collide with, rub against, or otherwise interact with the ground, walls or other objects in a way that may cause damage.
- Referee System modules should be connected in the manner specified in the instruction manual, with appropriate protection to ensure stable connections.

**S105** Except for the installation methods mentioned in this manual, any disassembly or modification of the Referee System onboard end is prohibited.

**S106** Robots may only be fitted with the Referee System borrowed for the current season.

**S107** When replacing Referee System onboard end modules during the match and Pre-Match Inspection, the following time requirements apply (firmware upgrade time not included):

**Table 3-1 Maximum replacement time for each Referee System onboard end module**

| Module | Max replacement time (minutes) |
| --- | --- |
| Main Controller Module | 5 |
| Power Management Module | 10 |
| Light Indicator Module | 5 |
| Small Armor Module | 2 |
| Armor support frame | 7 |
| Camera Video Transmitter Module (transmitter end) | 5 |
| Field Interaction Module | 7 |
| 17mm Speed Monitor Module | 7 |
| 42mm Speed Monitor Module | 7 |
| Positioning Module | 4 |

<!-- p.46 -->
| Module | Max replacement time (minutes) |
| --- | --- |
| Supercapacitor Management Module | 3 |

**S108** While a robot is tipped over, if it does not meet the building specifications, the referee may waive penalties depending on the actual situation, but any state the robot actively enters is not regarded as an abnormal working condition.

### 3.1 Referee System Overview

The robot designed by the team must reserve mechanical and electrical interfaces and comply with the specifications in this chapter to correctly install each Referee System module.

> Note:
> - The RoboMaster RMOC provides the Referee System on loan. Teams can obtain Referee System loan permission through the Technical Assessment of each competition. For details, see the "Season Schedule" in each competition's Participant Manual.
> - Chassis Power: the power consumed by mechanisms that rely on rotational motion and ground friction to do work moving or rotating the robot horizontally on a plane. For example, the steering motors of a swerve drive, the joint motors of a legged robot, and track mechanisms used only for climbing steps or crossing obstacles are not counted in Chassis Power.
> - No device used by a team may interfere with the normal operation of the Referee System. If interference exists, the team must cooperate with the RMOC in adjusting the source of interference until it no longer interferes.
> - When a robot passes through the Tunnel, the Speed Monitor Module and Positioning Module may be briefly blocked. The Main Controller Module, Camera Video Transmitter Module (transmitter end) and Light Indicator Module may also be briefly blocked, but any resulting functional abnormality or interference is borne by the team. The remaining modules must still meet their respective installation requirements.

The modules of the Referee System are as follows:

**Table 3-2 Referee System modules**

| Module | Description |
| --- | --- |
| Main Controller Module | The Main Controller Module is the core control unit of the Referee System. It can monitor the running status of the whole system and integrates functions such as human-machine interaction, wireless communication and status display. |
| Power Management Module | The Power Management Module controls power to the robot's chassis, gimbal and launching mechanism, forwards data, detects Chassis Power, and so on. |
| Light Indicator Module | The Light Indicator Module uses LED light bars to indicate the robot's red/blue side, HP, Buffs, module offline status and so on. |
| Armor Module | The Armor Module detects projectile hits and collisions on the robot. |

<!-- p.47 -->
| Module | Description |
| --- | --- |
| Speed Monitor Module | The Speed Monitor Module detects the robot's projectile Initial Launch Speed and Barrel Heat. It is divided into the 17mm Speed Monitor Module and the 42mm Speed Monitor Module. |
| Field Interaction Module | The Field Interaction Module can exchange information with the field or with the Field Interaction Module cards of robots to implement the corresponding functions. |
| Camera Video Transmitter Module | The Camera Video Transmitter Module is divided into a transmitter end and a receiver end. The transmitter end is installed on the robot, and the receiver end is installed on the client in the Operator Room. It captures the view in front of the robot in real time through the camera and sends the first-person view back to the display in the Operator Room. It also provides remote control of the robot. |
| Positioning Module | The Positioning Module obtains the robot's position on the Battlefield. |
| Supercapacitor Management Module | The Supercapacitor Management Module detects the energy input to and output from the supercapacitor module. |

### 3.2 Robot Referee System Onboard End Configuration

The Referee System onboard end module configuration of each robot is as follows:

**Table 3-3 Robot Referee System onboard end module configuration**

| Quantity \ Type | Heavy Robot | Infantry Robot | Aerial System | Sentry Robot | Dart System | Radar System |
| --- | --- | --- | --- | --- | --- | --- |
| Main Controller Module | 1 | 1 | 1 | 1 | 1 | 1 |
| Power Management Module | 1 | 1 | 1 | 1 | 1 | 1 |
| Light Indicator Module | 1 | 1 | 0 | 1 | 0 | 0 |
| Small Armor Module | 4 | 4 | 0 | 4 | 0 | 0 |
| Camera Video Transmitter Module (transmitter end) | 1 | 1 | 1 | 1 | 0 | 0 |
| Field Interaction Module | 1 | 1 | 0 | 1 | 0 | 0 |
| 17mm Speed Monitor Module | 0 | 1 | 0 | 1 | 0 | 0 |

<!-- p.48 -->
| Quantity \ Type | Heavy Robot | Infantry Robot | Aerial System | Sentry Robot | Dart System | Radar System |
| --- | --- | --- | --- | --- | --- | --- |
| 42mm Speed Monitor Module | 1 | 0 | 0 | 0 | 0 | 0 |
| Positioning Module | 1 | 1 | 0 | 1 | 0 | 0 |
| Supercapacitor Management Module | 1 | 1 | 0 | 1 | 0 | 0 |

> Note: In RMUL, robots do not need to install the Positioning Module.

<!-- p.49 -->
### 3.3 Main Controller Module Installation Specifications

Refer to the Main Controller Module dimensions and reserve mounting holes at a specific position on the robot.

*Figure 3-1 Main Controller Module diagram*

- [1] Infrared receiver
- [2] Button
- [3] Power indicator
- [4] Aviation connector interface with black metal ring
- [5] Metal lower shell
- [6] Upgrade interface
- [7] Plastic upper shell
- [8] Screen
- Dimension labels in the drawing (mm): 76; 67.50; 4.20; 63; 56; 44; 14; 4-Φ2.6

#### 3.3.1 Installation Steps

1. Fix the Main Controller Module at a specific position on the robot using 4 M2.5 screws.

> Note: Installation reference: you may design your own parts, with non-metal baffles on all sides for protection against projectile hits.

<!-- p.50 -->
2. Use the aviation adapter cable in the package to connect the Main Controller Module to the black-metal-ring aviation connector interface of the Power Management Module.

> Note: When the Main Controller Module is connected to the Power Management Module, no other Referee System onboard end module may be connected in series between them.

*Figure 3-2 Main Controller Module wiring diagram*

- [1] Aviation adapter cable

#### 3.3.2 Installation Requirements

The Main Controller Module must be installed to meet the following requirements; otherwise the connection to the competition server may fail or be unstable.

- With the robot in working state, the top surface of the Main Controller Module must face horizontally upward. Taking each antenna center as the apex, there must be at least one cone with a cone angle of 60° (solid angle π(2-√3) sr) extending without limit and free of obstruction by conductive material, or an equivalent space that does not interfere with wireless signal transmission (it must be the same cone, and the generatrices of the complete cone of the adjusted shape must lie within the upper hemisphere), as shown in the figure below.

*Figure 3-3 Main Controller Module no-obstruction zone*

- [1] No-obstruction zone
- Cone angle labels in the drawing: 60°

<!-- p.51 -->
- The Main Controller Module should be installed in a location with good heat dissipation; otherwise, heat dissipation problems of the Main Controller Module are very likely to cause abnormal operation during the match.

- The area above the Main Controller Module screen, buttons, interfaces, infrared receiver, etc. must not be blocked. When designing protective devices, use transparent material that is easy to open; if it cannot be opened, the screen, buttons, interfaces and infrared receiver must be fully exposed. Blocking them may make it impossible to connect to the competition server at all, or to troubleshoot abnormalities.

- Within the upper hemisphere of radius 70 mm centered 8.5 mm directly below the center point of the Logo, avoid conductive materials, electromagnetic absorbing materials, or other components that may cause WiFi signal interference.

> Note: If electromagnetic shielding material or electromagnetic interference equipment carried by mechanisms such as the gimbal or robotic arm passes through this area while moving, WiFi signals may be interfered with.

*Figure 3-4 Main Controller Module installation position diagram*

- [1] Antenna center
- Dimension labels in the drawing (mm): 65; 35; SR70; 8.5

**S109** The Power Rune pillar has an infrared emitting area 150 mm long and 150 mm high. This area is centered along the width of the pillar, with its lower edge flush with the bottom surface of the Hangar platform. Teams must design the installation position and orientation of the Hangar Main Controller Module according to the position of this area, ensuring that the Main Controller Module's infrared receiver faces this area and is within effective receiving range, so that it can connect to the server.

<!-- p.52 -->
*Figure 3-5 Hangar Main Controller Module installation diagram*

- [1] Infrared emitting area
- [2] Main Controller Module

> Note: If the connection to the server is not successfully made within a certain time after power-on in the Setup Period, the Main Controller Module position may be adjusted appropriately within the infrared range.

**S110** In official matches, the Dart System and Radar System must connect the Power Management Module and Main Controller Module in the manner specified by the RMOC.

For the Radar System:

The Battlefield provides a wired connection so that the Radar System can join the Battlefield network and server. The Radar computing platform end platform provides a wired access point: a single-ended female aviation cable. Field staff must connect the main controller interface of the Power Management Module on the Radar computing platform end to the wired access point using the official aviation docking cable.

To let the Radar System connect quickly and successfully, follow these requirements:

- During the match the Radar System does not need to carry its own Main Controller; remove the Main Controller used for debugging on the robot before Pre-Match Inspection.
- The Power Management Module of the Radar System must be exposed and placed where staff can easily operate it.
- The main controller interface on the Radar System's Power Management Module must not be connected to any device. This aviation cable must be neatly arranged, not tangled with others, and easy to pull out and connect to the wired access point.

For the Dart System:

The Battlefield provides a wired connection so that the Dart System can join the Battlefield network and server. The Dart Launching Station provides a single-ended female aviation cable 800 mm long. Field staff must connect the Dart System to the wired access point using the official aviation docking cable.

To let the Dart System connect quickly and successfully, follow these requirements:

- During the match the Dart System does not need to carry its own Main Controller; remove the Main Controller used for debugging on the robot before Pre-Match Inspection.

<!-- p.53 -->
- The aviation cable connecting the Power Management Module and the Main Controller can be plugged and unplugged easily without tools.
- The Power Management Module of the Dart System must be exposed and placed where staff can easily operate it.
- The Dart System's Power Management Module must be installed as close as possible to the wired access point of the Dart Launching Station, and its other end must not be connected to any device. This aviation cable must be neatly arranged, not tangled with others, and easy to pull out and connect to the wired access point.

*Figure 3-6 Dart Launching Station Referee System aviation cable position diagram*

- [1] 0.8 m female Referee System connecting cable
- [2] Dart System placement plane

<!-- p.54 -->
### 3.4 Power Management Module Installation Specifications

Refer to the Power Management Module dimensions and reserve mounting holes at a specific position on the robot.

*Figure 3-7 Power Management Module diagram*

- [1] Connection status indicator
- [2] System status indicator
- [3] Launching mechanism power output indicator
- [4] Gimbal power output indicator
- [5] Chassis power output indicator
- [6] Bottom mounting surface
- Dimension labels in the drawing (mm): 70; 69; 63; 60; 48; 42; 5; 22.50; 15.50; 4-Ø2.70 with Ø4.50 depth 3

<!-- p.55 -->
#### 3.4.1 Installation Steps

> Note: The aviation connector interfaces of the Light Indicator Module, Camera Video Transmitter Module (transmitter end), Speed Monitor Module and Positioning Module are equivalent interfaces and can be connected in series with each other.

Fix the Power Management Module to the robot using 4 M2.5 screws.

*Figure 3-8 Power Management Module installation diagram*

- [1] Power Management Module

<!-- p.56 -->
*Figure 3-9 Power Management Module interface diagram*

- [1] Armor Module SM06B-GHS-TB interface
- [2] Field Interaction Module SM04B-GHS-TB interface
- [3] Supercapacitor Management Module SM04B-GHS-TB interface
- [4] Main Controller Module interface (the metal ring of this aviation connector interface is black)
- [5] Interfaces for other Referee System onboard end modules (Speed Monitor, Positioning, Video Transmitter, Light Indicator; the metal ring of this aviation connector interface is silver-white)
- [6] Referee System serial port SM03B-GHS-TB interface
- [7] System upgrade SM03B-GHS-TB interface
- [8] Referee System power XT60 interface (input)
- [9] Mini PC power XT30 interface (output)
- [10] Referee System power XT30 interface (output), connected to the chassis
- [11] Referee System power XT30 interface (output), connected to the gimbal
- [12] Referee System power XT30 interface (output), connected to the launching mechanism

<!-- p.57 -->
*Figure 3-10 Power Management Module wiring diagram*

- [1] Aviation adapter cable

#### 3.4.2 Installation Requirements

The Power Management Module must be installed to meet the following requirements:

> Note: The Power Management Module must be firmly fixed on heat-resistant material in a location with good heat dissipation, with each interface protected. The Power Management Module generates heat during use; if it is fixed with adhesive such as double-sided tape, it is very likely to fall off, creating a safety hazard. The team bears the consequences of improper fixing or poor heat dissipation of the Power Management Module.

**S111** For robots with a Chassis Power limit, the electrical energy used by mechanisms counted in Chassis Power must not bypass the monitoring of the Power Management Module.

**S112** The Dart System and Radar System must use the Main Controller Module installed on the field by the RMOC. Therefore, when designing robots, teams must meet the following requirements:

- When designing the Dart System and Radar System structures, the Main Controller Module interface of the Power Management Module must be exposed.
- When designing the Dart System structure, the Power Management Module must be installed close to the entrance of the Dart Launching Station.

**S113** Carefully distinguish the interfaces of the Power Management Module and ensure correct wiring. For the power supply of robot mechanisms, refer to "Table 3-4 Power Management Module interface description".

> Note: Except for the Ground Robot chassis power, to keep the other power supply interfaces of the robot (such as gimbal power and 42mm launching mechanism power) stable, these interfaces may be powered by a battery and controlled through relays or other means,

<!-- p.58 -->
> but must be switched on and off through the corresponding Power Management Module interface (a relay or other means must be powered through the corresponding interface, ensuring that the robot's Referee System can switch on and off the power of all devices connected to the "Referee System power interface (output)"; otherwise it is regarded as cheating).
>
> - Electrical devices connected to a Power Management Module power supply interface must power off immediately when that interface is powered off.
> - If the Radar System or the Dart launching rack requires a 24V power supply interface, it can be powered directly from the "Mini PC" interface of the Power Management Module or from the battery.

**Table 3-4 Power Management Module interface description**

| Robot type | Chassis | Gimbal | Ammo-Booster | Mini PC |
| --- | --- | --- | --- | --- |
| Heavy Robot | Chassis power | Gimbal power | 42mm launching mechanism power | Mini PC power |
| Infantry Robot | Chassis power | Gimbal power | 17mm launching mechanism power | Mini PC power |
| Hangar | No power supply | Actuator power | No power supply | Mini PC power |
| Sentry Robot | Chassis power | Gimbal power | 17mm launching mechanism power | Mini PC power |
| Dart launching rack | No power supply | No power supply | No power supply | Mini PC power |
| Radar computing platform | No power supply | No power supply | No power supply | Mini PC power |

**S114** For a robot with a launching mechanism, when the Power Management Module "Ammo-Booster" interface is powered off, the launching mechanism (friction wheel motors, feeder motor, solenoid valves, etc.) must also be powered off at the same time.

**S115** For a robot with a Chassis Power limit, its circuit boards and wiring must meet the following requirements:

- Circuit boards related to the chassis power supply must be independent of the gimbal and launching mechanism power supplies. A circuit board powered by the Power Management Module "Chassis" interface must not be connected to any other power supply interface of the Power Management Module.
- All wiring related to the robot chassis must be clear. Referees will spot-check the robot after the match, and the team must cooperate by disassembling the relevant robot parts and showing the relevant wiring. It is recommended to consider the needs of referee spot checks when designing and laying out the wiring. Preparation time lost to disassembling and reassembling the robot for wiring inspection is borne by the team.
- Between circuit boards connected to the robot's Power Management Module "Chassis" interface (that is, circuit boards related to the chassis power supply) and circuit boards connected to the other power supply ports of the Power Management Module, use only cables with a wire gauge of 24AWG or smaller, used for communication only, with a total current flow of 50mA or less.

<!-- p.59 -->
> Note:
>
> - Power Management Module input voltage requirement: 22V-26V. Power output interfaces No. 10, 11 and 12 in "Figure 3-9 Power Management Module interface diagram" can be switched on and off by the Referee System.
> - For the load thresholds of each interface of the Power Management Module, refer to the Power Management Module User Manual.
> - When the system load fluctuates greatly, the voltage of power output interfaces 9-12 will fluctuate. Teams are advised to provide voltage stabilization for voltage-sensitive loads (such as the Mini PC).

### 3.5 Light Indicator Module Installation Specifications

- [1] Auxiliary Light Indicator
- [2] Main Light Indicator
- [3] Fixing bracket
- [4] Aviation connector interface

*Figure 3-11 Light Indicator module diagram*

- Dimensions: 285, 85

<!-- p.60 -->
#### 3.5.1 Installation Steps

1. Optional: the Light Indicator module can be fixed with the screw holes at the bottom of the fixing bracket and installed at a suitable position on the robot.

*Figure 3-12 Light Indicator module screw installation positions*

- Dimensions: 50.00, 2-Ø3.00 (two holes), 5.30, 12.00, 20.00, 4.00, 12.00

*Figure 3-13 Light Indicator module bottom view*

- Dimensions: 4-M3.00, depth 6; 105.00, 5.00, 100.00, 7.00, 10.00, 20.00

2. Using the aviation adapter cable in the package, connect the Light Indicator module to the aviation connector interface with the silver metal ring on the Power Management Module.

- [1] Aviation adapter cable

*Figure 3-14 Light Indicator module wiring diagram*

<!-- p.61 -->
#### 3.5.2 Installation Requirements

The Light Indicator module installation must meet the following requirements:

**S116** The connecting line between the left and right auxiliary Light Indicators must be parallel to the ground.

> Note: When installing the Light Indicator module, the following specification is recommended: when looking straight at the robot from at least one horizontal direction, tilted up or down by 45 degrees, the status of the main Light Indicator and auxiliary Light Indicators must be fully visible. Otherwise, the information conveyed by the Light Indicator effects may be lost during the match, and detection and handling of abnormal situations may be delayed.

### 3.6 Armor Module Installation Specifications

Armor Modules must be installed on the robot through the designated armor support bracket.

**S117** The armor support bracket may be installed on the robot chassis using only its rear mounting surface or only its bottom mounting surface.

**S118** Only the officially provided armor support bracket may be used to install Armor Modules. Modifying or damaging the armor support bracket is prohibited.

The outline of the designated armor support bracket is shown below:

*Figure 3-15 Designated armor support bracket diagram*

- Scale 1:2
- Dimensions: (70.9), (133), (141), (125), (112°), (40), 30, 18, 15, 7.5, 86, (33.5), 9, 18
- Labels: 4-M4 threaded holes; 2-M4 threaded holes; 2-M4 threaded holes, depth 10

<!-- p.62 -->
**S119** Do not make any modification to or decoration of the Armor Module.

#### 3.6.1 General Specifications

> Note: Robot chassis: the mechanism that carries the robot's power system and its accessory parts; the mechanism that supports the robot body.

The robot body coordinate system is a standard X, Y, Z Cartesian coordinate system whose origin is the robot's center of mass. According to the Armor Module installation requirements for Ground Robots, the robot coordinate system is established with the theoretical maximum-efficiency direction of the robot's chassis configuration as the X axis and the direction pointing to the center of the earth as the positive Z axis. If a special chassis configuration (e.g. steering-wheel chassis) has multiple maximum-efficiency directions, any one of them may be chosen as the X axis. For the X axis definition of various chassis configurations, refer to the figures below:

*Figure 3-16 Robot coordinate system diagram*

- Axis labels: X+, Y+, Z+

*Figure 3-17 X axis diagram for different robot chassis configurations*

<!-- p.63 -->
##### 3.6.1.1 Armor Module Installation

**S120** When installing Armor Modules on the robot, the Armor Module and the armor support bracket must be firmly connected. The bottom connecting surface of the armor support bracket of the Armor Module must be parallel to the XY plane, so that the acute angle between the line of the normal vector of the plane containing the Armor Module's impact-receiving surface and the line of the negative Z axis is 75 degrees. The angle between the two sides of the Armor Module that do not carry side lights and the XY plane must be less than 5 degrees. Define the projection onto the XY plane of the normal vector of the installed Armor Module's impact-receiving surface (the one forming an acute angle with the negative Z axis) as the direction vector of that Armor Module. The direction vectors of the 4 Armor Modules must correspond one-to-one to the positive X axis, negative X axis, positive Y axis and negative Y axis of the robot body coordinate system, and the angular error between each direction vector and its corresponding coordinate axis must not exceed 5 degrees.

**S121** The robot's own kinematic equations must also be established in the above body coordinate system. The installation of the Armor Modules must share the same reference coordinate system with the robot's own structural or kinematic characteristics. The line connecting the geometric centers of the Armor Modules installed on the X axis and the line connecting the geometric centers of the Armor Modules installed on the Y axis must be perpendicular to each other. After a single Armor Module installed on the Y axis is offset, the component along the X axis of the offset of its geometric center relative to the robot's geometric center must not exceed 50mm; the same applies to Armor Modules installed on the X axis.

##### 3.6.1.2 Rigid Connection

**S122** The installed Armor Module and armor support bracket must be rigidly connected to the chassis. During the match, no relative movement may occur between the Armor Module and the chassis. The rigid connection is defined as shown in the figure below: when a vertically upward force of 60N is applied to the midpoint of the lower edge of the Armor Module, the change in the angle α of the Armor Module's impact-receiving surface must not exceed 2.5 degrees.

*Figure 3-18 Armor Module force diagram*

- Labels: α <= 2.5°, F=60N

##### 3.6.1.3 Robot Deformation

**S123** In principle, after the match starts, no Armor Module may actively move relative to the robot's overall center of mass. If

<!-- p.64 -->
a participating robot has deformable characteristics due to its structural design, its Armor Modules must meet the following: at any time, no Armor Module may make continuous, reciprocating rapid movement relative to the robot chassis. Rapid movement is defined as movement at a speed exceeding 0.5m/s.

**S124** For a Ground Robot, the height difference between the lower edges of any two Armor Modules must not exceed 100mm. This requirement may be briefly not met while the robot crosses terrain.

**S125** For a Ground Robot, before, during and after deformation, the height of the lower edge of the Armor Module above the ground must not exceed 400mm, and the lower edge of the Armor Module must not directly touch the ground.

> Note:
>
> - When the surface supporting the robot body is not the ground, the Armor Module installation height is measured from the highest surface supporting the robot body.
> - If the robot has no supporting surface at all, this requirement does not apply.

##### 3.6.1.4 Armor Module Protection

**S126** Teams must design bumpers for Ground Robots to reduce damage caused by Armor Module impacts.

**S127** When any side of the robot on level ground is pressed against a vertical rigid plane, the Armor Module must not directly touch that rigid plane, as shown in the figure below:

- [1] Wall

*Figure 3-19 Robot protection diagram*

**S128** Except for the armor support bracket, no structure may make any contact with the Armor Module.

#### 3.6.2 Installation Steps

The Armor Module installation steps are the same for all Ground Robots. The Infantry Robot Armor Module is used below as an example. The following installation steps

<!-- p.65 -->
use installation with only the bottom mounting surface of the armor support bracket as an example.

1. Reserve 4 groups of mounting holes on the chassis, one group for each Armor Module. The 4 mounting holes in each group must have the same size and relative positions.
2. Each armor support bracket must be fixed to the chassis with 2 M4 screws. The result after installation is shown in the figure below:

*Figure 3-20 Armor support bracket installation diagram*

3. Install the Armor Module onto the armor support bracket and fix it with M4 screws. The specific installation steps are as follows:

*Figure 3-21 Armor Module installation diagram*

   1) Insert the slot at the bottom of the Armor Module into the clip at the bottom of the armor support bracket.
   2) Insert the top end face of the Armor Module into the clip at the top of the armor support bracket.

<!-- p.66 -->
   3) Insert the fastening screws.

4. Using the 6-pin cables provided in the package, connect the Armor Modules in series to the Armor Module interfaces of the Power Management Module. The 2 6-pin interfaces of the armor support bracket are equivalent.

> Note:
>
> - Route the cables reasonably according to the robot's own situation, ensuring a secure connection and avoiding cable damage.
> - When connecting, it is recommended to divide the number of Armor Modules in series on the two 6-pin interfaces of the Power Management Module evenly, so as to share the current of these interfaces equally.

- [1] Power Management Module

*Figure 3-22 Armor Module wiring diagram*

> Note: The specific installation steps are subject to later updates.

<!-- p.67 -->
#### 3.6.3 Installation Requirements

**S129** For Infantry Robots and Sentry Robots, the area within 105 degrees of the lower edge, within 120 degrees of the upper edge, and within 145 degrees of the left and right edges of the Armor Module's impact-receiving surface must not be obstructed.

- [1] Top fixed with M4 screws

*Figure 3-23 Armor Module installation specification diagram*

- [1] Extends infinitely

*Figure 3-24 No-obstruction zone of Infantry Robot and Sentry Robot Armor Modules*

- Angle labels: 120°, 105°, 145°, 145°

**S130** For Heavy Robots, the area within 105 degrees of the lower edge of the impact-receiving surface of all Armor Modules must not be obstructed. At least 3 of the 4 Armor Modules must satisfy the requirement that the area within 120 degrees of the upper edge and within 145 degrees of the left and right edges is not obstructed. At most 1 Armor Module may be conditionally obstructed within 120 degrees of the upper edge and 145 degrees of the left and right edges of its impact-receiving surface. The condition for obstruction is:

<!-- p.68 -->
on the plane containing the Armor Module's impact-receiving surface, obstruction is allowed at a distance greater than 150mm from the upper edge of the Armor Module, or greater than 170mm from the left and right edges; that is, the shaded part in the figure below must not be obstructed.

> Note: The no-obstruction zones in this section extend infinitely within the robot's maximum extended size.

- [1] Extends infinitely

*Figure 3-25 No-obstruction zone of Heavy Robot Armor Modules*

- Labels: 150, 170, 135°, 120°, 105°, 145°, 145°

<!-- p.69 -->
### 3.7 Speed Monitor Module Installation Specifications

There are two types of Speed Monitor Module: the 17mm Speed Monitor Module and the 42mm Speed Monitor Module.

17mm Speed Monitor Module:

- [1] Photoelectric sensor
- [2] Speed Monitor Module clamping screw hole
- [3] M2.5 mounting screw hole
- [4] LED Light Indicator
- [5] Aiming sight

*Figure 3-26 17mm Speed Monitor Module diagram*

- Dimensions: 51.00, 23.25, 42.40, 2 x Ø5.00, 14.30, 25.00, Ø21.10, 2.00, 30.00, 6.40, 16.00; 4 x M2.5, depth 4; Section A-A

<!-- p.70 -->
42mm Speed Monitor Module:

- [1] Photoelectric sensor
- [2] Speed Monitor Module clamping screw hole
- [3] M2.5 mounting screw hole
- [4] LED Light Indicator
- [5] Aiming sight

*Figure 3-27 42mm Speed Monitor Module diagram*

- Dimensions: 51.00, 21.00, 74.00, 2 x Ø6.00, 28.00, 27.00, Ø48.50, 4.00, 30.00, 8.30, 16.00; 4 x M2.5, depth 4; Section A-A

**S131** Removing the aiming sight of the Speed Monitor Module is prohibited.

<!-- p.71 -->
#### 3.7.1 Installation Steps

Currently there are 3 mounting schemes for the 17mm Speed Monitor Module. All 3 schemes comply with the Referee System installation specifications for the 17mm Speed Monitor Module, and teams choose one of them.

##### 3.7.1.1 17mm Speed Monitor Module Mounting Scheme 1

17mm launch tube size limits:

- [1] Facing the launch port
- [2] Wall thickness is recommended to be no less than 1mm

*Figure 3-28 17mm launch tube diagram*

- Dimensions: 21.00±0.03, 2 x Ø8.00, MAX 97.00, 23.25±0.20, 74.25±0.20; Section A-A

Requirements for making the 17mm launch tube:

**S132** Ensure the photoelectric sensor is not obstructed.

**S133** Transparent materials and light-emitting materials are prohibited, and infrared sensors are prohibited near the launch tube.

**S134** Ensure there is no strongly reflective material on the inner wall of the launch tube, to avoid interfering with normal operation of the Speed Monitor Module.

> Note: It is recommended to frost or matte-finish the inner wall of the launch tube.

Mounting Scheme 1 installation steps:

1. Fit the Speed Monitor Module over the launch tube.
2. Pass M3 screws through the Speed Monitor Module clamping screw holes to clamp the launch tube.

<!-- p.72 -->
3. Using the aviation adapter cable, connect the aviation connector interface of the Speed Monitor Module to the aviation connector interface of the Power Management Module.

> Note: After installation, prevent the launch tube from rotating or shifting so as to obstruct the photoelectric sensor.

The result after installation is shown below:

*Figure 3-29 Speed Monitor Module installation diagram*

##### 3.7.1.2 17mm Speed Monitor Module Mounting Scheme 2

Team members design and machine their own adapter parts to connect the 17mm Speed Monitor Module to the launching mechanism.

For detailed engineering drawings of the adapter parts, see "Appendix 1 Engineering drawings of the 17mm Speed Monitor Module adapter parts". The 3D model can be downloaded from the Speed Monitor Module product page on the RoboMaster official website, for reference only.

A reference adapter part is shown below:

- [1] Front boss
- [2] Rear boss

*Figure 3-30 17mm adapter part diagram*

<!-- p.73 -->
- [1] LED Light Indicator fixing screw M2.5
- [2] Screw M3
- [3] Self-made part 1
- [4] Side fixing hole
- [5] Rear boss
- [6] Self-made part 2
- [7] Screw M2.5
- [8] Screw M3

*Figure 3-31 17mm adapter part fixing method diagram*

Mounting Scheme 2 installation steps:

1. Remove the one M2.5 screw fixing the LED Light Indicator on each of the left and right sides of the Speed Monitor Module (the position of one side is shown as [1] in the figure). Removing any other LED Light Indicator fixing screws of the Speed Monitor Module is prohibited.
2. Through the side fixing holes on the left and right sides (the position of one side is shown as [4] in the figure), fix the adapter part to the Speed Monitor Module with 2 M2.5x14 screws.
3. Use 2 M3 screws to fix the robot's existing plate part 1 to the upper end of the Speed Monitor Module.
4. Use 2 M3 screws and four M2.5 screws to fix the robot's existing plate part 2 to the lower end of the Speed Monitor Module.
5. Using the aviation adapter cable, connect the aviation connector interface of the Speed Monitor Module to the aviation connector interface of the Power Management Module.

> Note: Apart from the two screws in step 1, which may be removed, no other screw on the Speed Monitor Module may be removed or reinstalled without authorization. Violators are regarded as damaging the Referee System.

<!-- p.74 -->
##### 3.7.1.3 17mm Speed Monitor Module Mounting Scheme 3

Team members design and machine their own launch tube parts to connect the 17mm Speed Monitor Module to the launching mechanism.

- [1] Launch tube
- [2] Self-made part 1
- [3] M2.5 screw

*Figure 3-32 17mm short launch tube installation diagram*

Mounting Scheme 3 installation steps:

1. Insert the Speed Monitor Module into the short launch tube.
2. Use 4 M2.5 screws to fix the robot's existing plate part 1 to the lower end of the Speed Monitor Module.
3. Using the aviation adapter cable, connect the aviation connector interface of the Speed Monitor Module to the aviation connector interface of the Power Management Module.

> Note:
>
> - The length of the launch tube inserted into the Speed Monitor Module must be no more than 23mm, to avoid obstructing the Speed Monitor Module's speed-measuring photoelectric sensor.
> - The outer diameter of the launch tube is recommended to be kept within 21mm + 0.05. A launch tube diameter that is too small leaves a large gap between the outer wall of the launch tube and the inner wall of the Speed Monitor Module, which enlarges the projectile dispersion area.
> - In this scheme, because the Speed Monitor Module and the launching mechanism parts are not positioned relative to each other, the axis of the Speed Monitor Module may not coincide with the projectile launch axis, so that some projectiles touch the inner wall of the Speed Monitor Module. In this case, team members may add shims between the robot's existing plate part 1 and the Speed Monitor Module as needed to adjust the installation angle of the Speed Monitor Module and the robot's existing plate part 1.

##### 3.7.1.4 42mm Speed Monitor Module Mounting Scheme

> Note: The 42mm Speed Monitor Module mounting scheme may follow the 3 mounting schemes of the 17mm Speed Monitor Module.

<!-- p.75 -->
42mm launch tube size limits:

- [1] Facing the launch port
- [2] Wall thickness must be no less than 1mm

*Figure 3-33 42mm launch tube diagram*

- Dimensions: 48.50±0.03, 2 x Ø10.00, MAX 103.00, 21.00±0.20, 72.00±0.20; Section A-A

Requirements for making the 42mm launch tube:

**S135** Ensure the photoelectric sensor is not obstructed.

**S136** Transparent materials and light-emitting materials are prohibited, and infrared sensors are prohibited near the launch tube.

**S137** Ensure there is no strongly reflective material on the inner wall of the launch tube, to avoid interfering with normal operation of the Speed Monitor Module.

> Note: It is recommended to frost or matte-finish the inner wall of the launch tube.

Mounting scheme installation steps:

1. Fit the Speed Monitor Module over the launch tube.
2. Pass M3 screws through the Speed Monitor Module clamping screw holes to clamp the launch tube.
3. Using the aviation adapter cable, connect the aviation connector interface of the Speed Monitor Module to the aviation connector interface of the Power Management Module.

#### 3.7.2 Installation Requirements

The Speed Monitor Module installation must meet the following requirements:

> Note: It is recommended that, for each Speed Monitor Module, the normal of at least one light-emitting face of its Light Indicator lies within the hemisphere above the horizontal plane, and that an inspector standing 1m or more from the Speed Monitor Module, looking straight at the Light Indicator perpendicular to its light-emitting face, can see 80% of the Light Indicator area. Otherwise, the information conveyed by the Light Indicator effects may be lost during the match, and detection and handling of abnormal situations may be delayed.

<!-- p.76 -->
**S138** The Speed Monitor Module must be installed at the end of the launching mechanism, ensuring that projectiles enter the Speed Monitor Module after being fully accelerated.

**S139** The Speed Monitor Module must be installed such that the line of intersection of the plane perpendicular to the projectile launch direction with the Logo face is level with the ground, as shown in the figure below. This requirement must be maintained at all times while projectiles are being launched; an angle of up to 5 degrees to the ground is allowed.

- [1] Projectile direction
- [2] Plane perpendicular to the projectile direction
- [3] Line of intersection of the Logo face with [2]

*Figure 3-34 Speed Monitor Module installation diagram*

**S140** When the Speed Monitor Module is calibrated for level, the Logo face must face up.

**S141** The Speed Monitor Module must be fixed securely and must not move by itself relative to the preloaded projectiles adjacent to the projectile being launched in the launching mechanism.

**S142** The launch tube installed inside the Speed Monitor Module must not use iron or other easily magnetized materials.

**S143** For strongly magnetic materials, or devices that produce strong magnetism when working, the effect on the Speed Monitor Module's magnetic angle, whether static or in operation, must be within 2 degrees (RMUL does not need to follow this requirement).

> Note: After calibrating the Speed Monitor Module, briefly press the confirm key of the Main Controller Module and then briefly press the page-down key to observe the changes in the robot's real-time coordinates on the Main Controller Module as follows (for details, see the onboard-end chapter of the Referee System User Manual):
>
> - After rotating the gimbal by 90 degrees, 180 degrees and 240 degrees respectively, the error between the displayed angle and the true rotation angle must be less than 15 degrees.
> - For strongly magnetic materials, after installing them in compliance with the above requirements, observe whether the angle value of the Speed Monitor Module fluctuates within 2 degrees.
> - For devices that produce strong magnetism when working, power the device on and observe the angle value of the Speed Monitor Module with the device at rest and in operation (for example: a friction wheel motor at rest and rotating after power-on) to see whether it fluctuates within 2 degrees.

**S144** As shown in the Speed Monitor Module installation specification diagram, within a sphere of 50mm diameter centered on the Logo position, easily magnetized substances (products made of iron, cobalt or nickel, the Video Transmitter Module transmitter's cooling fan, industrial camera bodies, etc.) are not allowed; within a sphere of 100mm diameter, magnetic substances other than the camera Video Transmitter Module and the industrial camera body (friction wheel motors, gimbal motors, etc.) are not allowed, to avoid interference with the magnetometer inside the Speed Monitor Module.

<!-- p.77 -->
- [1] Sphere center position
- Dimension: sphere diameter 50.00

*Figure 3-35 Speed Monitor Module installation specification diagram*

> Note:
> - Four M2.5 threaded holes are provided.
> - Do not block the photoelectric sensor holes, otherwise the Speed Monitor Module self-check will fail.
> - The aviation cable of the Speed Monitor Module is close to the friction wheels. Take care during use to keep the cable from being worn.

**S145** Teams must ensure electrical isolation between the modular 42mm launching mechanism and the Heavy Robot. Specifically:

- For the Referee System four-core aviation cable connection terminals led out from the Heavy Robot, with no external power supply connected, shorting any two of them together must not prevent the Heavy Robot's Referee System from working normally.
- For the Referee System four-core aviation cable connection terminals led out from the modular 42mm launching mechanism, with an external power supply of no more than 30V connected, connecting the positive and negative terminals of the external supply to the header pins in any pairwise combination may at most take the modular 42mm launching mechanism's Referee System offline, but must not damage it.

- [1] Brown - GND
- [2] Orange - CAN_L
- [3] Red - 12V power supply
- [4] Yellow - CAN_H
- Pin diagram labels: (1) brown, (2) orange, (3) red, (4) yellow

*Figure 3-36 Referee System wire sequence diagram*

> Note: Teams must carry out the above operations themselves during the actual Pre-Match Inspection.

<!-- p.78 -->
### 3.8 Field Interaction Module Installation Specifications

Refer to the Field Interaction Module structural dimensions and mounting interface, and reserve mounting holes on the robot chassis.

- [1] Back
- [2] LED Light Indicator
- [3] Front
- Dimensions (mm): 121.67 (overall width); 62 +/-0.02 (hole spacing); 105.67 (overall height); 50 +/-0.02 (hole spacing); 4xM3, depth 4; thickness 17.80

*Figure 3-37 Field Interaction Module diagram*

#### 3.8.1 Installation Steps

1. Use the 4-pin connection cable provided in the package to connect the Field Interaction Module to the RFID port on the Power Management Module.

*Figure 3-38 Field Interaction Module wiring diagram*

<!-- p.79 -->
2. Use M3 screws to secure the Field Interaction Module to the chassis. Do not pinch the connection cable during installation, and keep an appropriate distance between the Field Interaction Module and the ground.

*Figure 3-39 Field Interaction Module installation diagram*

#### 3.8.2 Installation Requirements

The Field Interaction Module must be installed in accordance with the following specifications, otherwise module detection quality may degrade. Teams bear sole responsibility for consequences caused by non-compliant installation.

- Avoid installing large areas of conductive material near the Field Interaction Module, and avoid large-current or high-frequency signal interference (such as motor wires, the RoboMaster center board, CAN cables, and supercapacitors).
- The front and back of the Field Interaction Module must not be covered by conductive material. Keep at least 30mm between the back and conductive materials such as metal plates and carbon plates.

**S146** The Field Interaction Module must not extend beyond the outermost edge of the rectangular area formed by the Armor Modules. In addition, while the robot transforms, the module may move relative to the chassis only along the Z axis and must not be displaced relative to the chassis in any other direction.

> Note:
> - The effective detection distance of the Field Interaction Module is 100mm (+/-5%). The actual detection distance after installation is subject to testing. If the effective detection distance is shortened or the module does not work normally, check whether the installation is appropriate. For the specific effective detection distance, refer to the *Field Interaction Module Manual* and the *Power Management Module Manual*.
> - Because the electromagnetic environment inside the robot is complex, the effective detection distance of the Field Interaction Module must be tested while all robot modules are working normally (for example, the supercapacitor, drive motors and wireless charging coil all operating). If the robot has multiple operating conditions (such as capacitor charging and discharging, or motors changing speed and running at constant speed), the effective detection distance must also be tested under the different conditions.

<!-- p.80 -->
### 3.9 Camera Video Transmitter Module (Transmitter) Installation Specifications

> Note:
> - Video transmission link data is output from the UART serial port of the Camera Video Transmitter Module (transmitter).
> - The UART serial port of the Camera Video Transmitter Module (transmitter) supports 3.3V TTL level. The UART pins are RX, TX and GND. Do not connect the positive power supply terminal to the UART serial port.

Refer to the transmitter's structural dimensions and mounting interface, and reserve mounting holes at the specified positions.

- [1] Air inlet
- [2] Indicator light
- [3] Sphere center position
- [4] Antenna
- [5] Camera
- [6] Air outlet
- [7] Mounting through hole
- [8] Mounting threaded hole
- Dimensions (mm): SR70 (70mm radius hemisphere zone); 28.8 (diameter); 14.3; 45.4; 14; 2; 9; 15 (diameter); 37.55; 8.5; 32; 26; 9.2; 60.42; 54.5; 32; 50; 25.5; 35; 78.5; 50.5; 4-diameter 3.2 (mounting through holes); 4-M3 thread, depth 4

*Figure 3-40 Camera Video Transmitter Module (transmitter) diagram*

> Note: The figure above is authoritative for the Camera Video Transmitter Module (transmitter). The Camera Video Transmitter Module (transmitter) shown in any other drawings is for reference only.

<!-- p.81 -->
#### 3.9.1 Installation Steps

1. Use four M3 screws to secure the transmitter at a suitable position on the robot.

- [1] Camera Video Transmitter Module (transmitter)

*Figure 3-41 Camera Video Transmitter Module (transmitter) installation diagram*

2. Use an aviation adapter cable to connect the aviation cable port of the Camera Video Transmitter Module (transmitter) to the aviation cable port for the video transmitter on the Power Management Module.

#### 3.9.2 Installation Requirements

The Camera Video Transmitter Module (transmitter) must be installed to meet the following requirements, otherwise image quality may degrade, the video transmission link may be unstable, and the robot may go offline abnormally.

- Avoid blocking the indicator light of the Camera Video Transmitter Module (transmitter).
- Taking the center of the bottom face of the Camera Video Transmitter Module (transmitter) as the vertex, there must be a cone whose generatrix is parallel to the bottom face of the module and located directly in front of the camera, with a cone angle of 60 degrees (solid angle of pi(2-sqrt(3)) sr) and unlimited extension, free of any obstruction by conductive material, as shown in the figure below.

**S147** The air inlet and air outlet of the Camera Video Transmitter Module (transmitter) must not be blocked.

> Note: It is recommended to keep the area within 150mm of each air inlet and air outlet unobstructed.

<!-- p.82 -->
- [1] No-obstruction zone
- [2] Zone axis
- Cone angle 60 degrees; 39 (mm, offset dimension shown on the transmitter)

*Figure 3-42 No-obstruction zone of the Camera Video Transmitter Module (transmitter)*

- Within the upper hemisphere of 70mm radius centered on the midpoint of the line connecting the bottoms of the antennas of the Camera Video Transmitter Module (transmitter), there must be no conductive material, electromagnetic absorbing material, or other components that may cause wireless signal interference, as shown in "Figure 3-40 Camera Video Transmitter Module (transmitter) diagram".
- If the video transmission link is used, the UART serial port section of the Camera Video Transmitter Module (transmitter) must be protected, for example with foam or a non-metallic baffle.
- The ports and indicator light of the Camera Video Transmitter Module (transmitter) must be unobstructed.

### 3.10 Camera Video Transmitter Module (Receiver) Usage Specifications

- [1] Heat dissipation holes
- Dimensions (mm): 150; 103; 65; (203)

*Figure 3-43 Camera Video Transmitter Module (receiver) diagram*

<!-- p.83 -->
#### 3.10.1 Installation Requirements

The Camera Video Transmitter Module (receiver) must be used in accordance with the following requirements, otherwise its image quality may degrade, remote control data transmission may stutter, or it may even malfunction.

**S148** Avoid metal obstruction near the Camera Video Transmitter Module (receiver).

**S149** The heat dissipation vents must not be blocked.

### 3.11 Positioning Module Installation Specifications

Refer to the Positioning Module dimensions and reserve mounting holes at the specified position on the robot.

- [1] Referee System connection cable
- [2] Top
- [3] Front
- Labels: USB, SYS, LINK
- Dimensions (mm): 45 x 45 mounting plate; 38 (hole spacing); 2xM3, depth 5

*Figure 3-44 Positioning Module diagram*

#### 3.11.1 Installation Steps

1. Use two M3 screws to secure the Positioning Module at the specified position on the robot, as shown in the figure below:

*Figure 3-45 Positioning Module installation diagram*

<!-- p.84 -->
2. Use the aviation adapter cable included in the package to connect the Positioning Module to the aviation cable port with a silver-white metal ring on the Power Management Module.

*Figure 3-46 Positioning Module wiring diagram*

#### 3.11.2 Installation Requirements

The Positioning Module must be installed to meet the following requirements. If not installed as required, the Positioning Module may produce abnormal positioning.

**S150** The Positioning Module mounting bracket must be rigidly connected to the robot: when a force of 40N perpendicular to the bracket is applied at any point on it, the plane of the Positioning Module's bottom must deviate by no more than 10 degrees from the horizontal plane.

**S151** The Positioning Module must be mounted horizontally with its top facing up. Within 145 degrees above the Positioning Module, there must be no obstruction by conductors, as shown in the figure below. If the Positioning Module is installed on a mechanism that can actively transform or participates in mechanical linkage, the requirements on Positioning Module obstruction must be met before, during and after the robot's transformation.

- [1] Unlimited extension
- Angle: 145 degrees

*Figure 3-47 Positioning Module installation diagram*

**S152** The Positioning Module must be installed at least 150mm from the Camera Video Transmitter Module. Distance is the shortest straight-line distance between the outermost edges of the modules.

<!-- p.85 -->
**S153** No magnets, magnetically permeable objects, or objects or components that are easily magnetized, which could produce a strong magnetic field, may be present within 100mm around the Positioning Module, to avoid interfering with it.

> Note: Common components that may cause magnetic interference include motors, magnetized metal, and magnets.

**S154** Magnets, magnetically permeable materials, and adhesive materials must not be used to secure the Positioning Module.

> Note:
> - Mounting screws are included in the Positioning Module package, and using them for installation is recommended (if the screws are lost, they can be obtained on site).
> - If other screws are chosen, they must comply with the relevant specifications.

### 3.12 Supercapacitor Management Module Installation Specifications

The Supercapacitor Management Module detects the capacitance of the supercapacitor pack and the supercapacitor pack's energy during a match. The dimensions of the Supercapacitor Management Module are expected to be 60*30*7.5mm (L*W*H), with heat-shrink tubing as the module's outer protection.

The hardware interfaces include one XT30 male connector, two XT30 female connectors, and one Supercapacitor Management Module communication interface.

> Note:
> - The XT30 female connector model is XT30PW-F.
> - The XT30 male connector model is XT30PW-M.

#### 3.12.1 Installation Steps

> Note: The power control board is the module that regulates the output power of the Chassis port of the Power Management Module and the input and output power of the supercapacitor pack to meet the power limits in the rules. This module is built by the teams themselves.

1. Install the Supercapacitor Management Module between the output port of the supercapacitor pack and the input port of the power control board.
2. Use cables with XT30 connectors to connect the supercapacitor pack to the Supercapacitor Management Module.
3. Use cables with XT30 connectors to connect the power control board to the Supercapacitor Management Module.
4. Use a 4-pin connection cable to connect the communication port of the Supercapacitor Management Module to the CAN1 port of the Power Management Module.

<!-- p.86 -->
The Supercapacitor Management Module wiring is shown in the figure below:

- [1] Robot chassis power supply port
- [2] Power control board
- [3] Supercapacitor pack
- [4] Supercapacitor Management Module
- [5] Supercapacitor Management Module port (output, XT30 female) - connects to the power control board
- [6] Supercapacitor Management Module inspection port (output, XT30 female) - used only for Pre-Match Inspection
- [7] Supercapacitor Management Module communication port (CAN, SM04B-GHS-TB connector) - connects to the Power Management Module
- [8] Supercapacitor Management Module port (input, XT30 male) - connects to the supercapacitor pack
- [9] Chassis output port of the Power Management Module
- [10] Power Management Module

*Figure 3-48 Supercapacitor Management Module wiring diagram*

#### 3.12.2 Installation Requirements

> Note:
> - The communication port of the Supercapacitor Management Module must be connected to the CAN1 port of the Power Management Module, otherwise it cannot work normally.
> - During Pre-Match Inspection, staff will check whether the team's supercapacitor pack installation meets the requirements according to the Supercapacitor Management Module wiring diagram, and after the check is completed will attach a pass mark to the module and the capacitor pack. Teams are advised to design a structure that makes the marks easy to see, to avoid frequent disassembly and reassembly of the robot structure during Pre-Match Inspection.

<!-- p.87 -->
**S155** Neither the peak current nor the maximum continuous current of the XT30 ports of the Supercapacitor Management Module may exceed 15A.

**S156** The capacitor voltage must be discharged from full charge to below 1V. A robot whose voltage drops abnormally fast or shows similar anomalies will not pass Pre-Match Inspection.

**S157** The inspection port of the Supercapacitor Management Module must be led out with at least 100mm of cable ending in an XT30 female connector.

**S158** Heavy Robots, Infantry Robots and Sentry Robots must all install a Supercapacitor Management Module. If the robot has no supercapacitor pack, it only needs to connect the Supercapacitor Management Module to the Power Management Module with a 4-pin cable.

**S159** The Supercapacitor Management Module must be installed in a location that is easy to access, so that it can be operated during Pre-Match Inspection.

**S160** The supercapacitor pack may use only one power supply port, which must be connected as shown in "Figure 3-48 Supercapacitor Management Module wiring diagram" and must not be connected to any other circuit on the robot.

<!-- p.88 -->
### Appendix 1 17mm Speed Monitor Module Adapter Part Engineering Drawing

- Dimensions (mm): 60.00; 40.20; 30.20; 17.20; 13.50; 3.30; 13.40; 2-diameter 2.50 with diameter 4.5 counterbore, depth 3; diameter 19.00; diameter 21.00 (+0.05/0); 53.00; 4-M3 thread, depth 6; 12.00; 6.00; 2.50; diameter 22.00 (+0.05/0)

<!-- p.89 -->
### Appendix 2 Reference Drawings

*Appendix Figure 1 Outpost Armor Sticker*

*Appendix Figure 2 Outpost Dart Detection Module Sticker*

<!-- p.90 -->
*Appendix Figure 3 Base Small Armor Sticker*

*Appendix Figure 4 Base Dart Detection Module Sticker*

<!-- p.91 -->
- Email: robomaster@dji.com
- Forum: https://bbs.robomaster.com
- Website: https://www.robomaster.com
- Phone: +86 0755-84357613 (Monday to Friday 10:30-19:30)
- Address: 13F, Building D1, Chuangzhi Yuncheng, Nanshan District, Shenzhen, Guangdong Province
