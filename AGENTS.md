# isaac_ros-dev workspace

Call out code that doesn't follow standard practice.

## Repository checks

Use a host Python 3.12 venv with `.github/quality/requirements.txt`. Run
`python .github/quality/check.py` in each repo and `actionlint -shellcheck=""`.
Checker tests: `python -m unittest discover -s .github/quality -v`.
Branch protection is opt-in: the script prints policy unless `--apply` is
passed. MCBV3 policy targets only `main`. Coverage: [docs/CI.md](docs/CI.md).

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

`nightly` integrates Jazzy changes; `main` is the promoted release
(`isaac_ros_jazzy_container`). Humble is frozen: no work on
`humble` branches or in `isaac_ros_dev-x86_64-container`.

## Packages

Each package dir is a submodule. Every package change needs a gitlink bump
here, or everyone else builds old code. One logical change per bump, even if
it moves several gitlinks or just one line.

Commit and push each logical change once it's tested, without being asked.
Push the submodule before the superproject.

Stage superproject files by explicit path; never use `git commit -a`.
Inspect `git diff --cached --stat` before committing. Include only gitlink
changes you deliberately intend; stale submodule checkouts must not revert
other people's gitlink updates (the user, 2026-10-04).

Author and commit changes as `Blaise Baptist <blaise.baptist@gmail.com>`.
Sign every commit with Blaise's configured Git signing key; never disable
signing or substitute an agent identity. Do not add Claude or other AI
co-author trailers or generated-by attribution to commit messages.
Claude attribution is disabled in `.claude/settings.json`; keep it disabled.

`nightly` keeps `.gitmodules` on package `nightly` branches. For coordinated
package integration, follow [CI guidance](docs/CI.md#coordinated-package-integration).
`.gitmodules` records each package's branch. After a clone, run the one-liner
in `README.md` to get off detached HEAD.

Instructions go in `AGENTS.md`, since more than Claude works here. Every
`CLAUDE.md`, root and package, is just `@AGENTS.md`.

Read a package's `AGENTS.md` before working there. Keep it short: current
state, open questions, rules. Test runs and measurements go in commit messages.

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

## Wire compatibility

Use the current UART/wire format only
([UART_PROTOCOL](ros2_dji_serial_bridge/UART_PROTOCOL.md)). Do not add an
old-format fallback, including the former 40-byte `CVData` payload. When
firmware and protocol disagree, update the MCB firmware and `sim` MCB
emulator rather than downgrading the bridge (the user, 2026-10-02).

## Responses

Use terse bullet lists for checklists, status, and to-do summaries: one
action or fact per item. Give rationale when asked (the user, 2026-10-03).

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
