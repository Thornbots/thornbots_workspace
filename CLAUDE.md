# isaac_ros-dev workspace

Call out code that doesn't follow standard practice.

## Skills

- [`isaac-ros-docker`](.claude/skills/isaac-ros-docker/): every docker command,
  and anything run inside the container.

## Containers

Ask before starting, restarting or stopping any container or container VM
on this laptop: `docker run`/`start`, a script or service that starts one,
`colima start`/`stop`. One started wrong can die, or take a running one
with it.

On remote boxes (the robots, `ts-nano-*`), start, stop, build and remove
containers and images when the user asks for it; no separate confirmation
(the user, 2026-10-04). "dev" means `ts-nano-dev`, not this laptop.

## Priority

CV (target detection/tracking) comes first. Game rules and field geometry:
[`ARCC_2026_SENTRY_CONTEXT.md`](ARCC_2026_SENTRY_CONTEXT.md).

## Branches

`main` is Jazzy (`isaac_ros_jazzy_container`). Humble is frozen: no work on
`humble` branches or in `isaac_ros_dev-x86_64-container`.

## Packages

Follow the [submodule workflow](README.md#working-with-submodules) for
package commits, gitlink updates and push order.

Commit and push each logical change once it's tested, without being asked.

Read a package's `AGENTS.md` before working there. Keep it short: agent
instructions and links to current state and open work.

Write `README.md` for a human in a container terminal: plain `colcon` and
`ros2`, no `dexec.sh`, `kill_launch.sh` or skills. Host-side equivalents go in
`AGENTS.md`.

## Documentation

Give each fact, procedure or decision one maintained home. Other documents
link directly to its section instead of copying it. Keep READMEs short:
purpose, quickstart and links to details. AGENTS files add agent instructions
and link to human documentation; they do not repeat it.

| Information | Maintained home |
| --- | --- |
| Package usage and design rationale | The owning package's `README.md` |
| Full robot launch recipe | [YOLO README](realsense-yolov8-nitros-bridge/README.md#full-robot-pipeline) |
| Robot node/topic diagram | [thornbots_pkg README](thornbots_pkg/README.md#nodes) |
| Machine migration and hardware validation status | [JAZZY_FLASH](JAZZY_FLASH.md#hardware-status) |
| Open project work | [ROADMAP](ROADMAP.md); link to plans for implementation detail |
| Wire format and timestamp contract | [UART_PROTOCOL](ros2_dji_serial_bridge/UART_PROTOCOL.md) |
| Parameter defaults and message fields | Their source declarations; link to them from explanatory docs |
| Test runs, tuning history and measurements | Commit messages; longer investigations in dated historical documents |

Before adding documentation, search for an existing home. Update it and
replace overlapping copies with relative Markdown links. Add a row here only
when a topic spans packages and its owner is unclear. When moving a section,
update its incoming links in the same change. Date historical observations
and link to current status so they cannot be mistaken for today's results.
Verify changed local links and anchors before committing.

## Timestamps

Stamp every internal ROS message's `std_msgs/Header` with when the data was
true (sensor capture, or the input's stamp carried through). Use `now()` only
for data created on the spot, like a fire decision. Document the stamp's
meaning in the `.msg` comment. Use `*Stamped` over bare `Point`/`Twist` unless
a standard interface requires the bare type.

## Comments

Keep comments and docstrings under 10 lines: topics, params, key invariants,
current tuned value. Add `# see README.md for design rationale` when trimming
would hide context a reader should know exists.
