# isaac_ros-dev workspace

Call out code that doesn't follow standard practice. CV detection/tracking
comes first; [game context](docs/ARCC_2026_SENTRY_CONTEXT.md) defines the field.
Use terse bullets for status/checklists; give rationale when asked.
Memory is disabled: do not read or write agent memory.

## Delegation

Delegate other tasks to a Sol agent (Codex `gpt-6.1-sol` via T3
`delegate_task`, medium reasoning, Standard tier) running on archlinux.
Delegate well-specified, high-volume repetitive edits to lower-cost agents
(Haiku/Luna). The delegating agent defines scope and acceptance checks,
resolves ambiguity, then reviews the diff and runs the checks itself. It
names other user-approved actions in the brief and owns asking the user.
Delegated agents never wait on user input: they skip anything outside the
brief and list it in their report.

## Repository checks

In a host Python 3.12 venv with `.github/quality/requirements.txt`, run
`python .github/quality/check.py` in each changed repo and
`actionlint -shellcheck=""`; checker changes also need
`python -m unittest discover -s .github/quality -v`. Do not grow baselines to
hide regressions. [Repository policy](docs/CI.md#repository-policy) hooks and
CI check commits and message contracts;
[branch protection](docs/CI.md#branch-protection) is opt-in.

## Containers and runs

Load [isaac-ros-docker](.claude/skills/isaac-ros-docker/SKILL.md) for every
Docker command or command inside a container.

- Start laptop containers, VMs (including Colima) and stacks as needed
  without asking, following the skill. Check for running ones first
  and reuse them; ask before restarting or stopping anything you did not
  start, and clean up what you started. On `ts-nano-*`, carry out requested
  container/image lifecycle work without separate confirmation. “dev” means
  `ts-nano-dev`.
- Run tests as you see fit, including sim integration tests, sim benches and
  reruns, without asking. Ask before runs on a physical robot.
- A delegation brief stating the user approved named actions is that approval
  for the delegated agent, only for what it names.

## Branches

`nightly` integrates Jazzy; `main` is the promoted release
(`isaac_ros_jazzy_container`). Humble branches and
`isaac_ros_dev-x86_64-container` are frozen; do not work there.

## Packages

- Read the package's `AGENTS.md` before editing. `CLAUDE.md` stays `@AGENTS.md`.
- Commit with the existing Git identity and signing key tied to your GitHub
  account. Do not rewrite identity config, disable signing or bypass hooks.
- Commit and push each tested logical change without being asked: package
  first, then one workspace gitlink bump per logical change. Never point at an
  unpushed commit.
- Keep [CHANGELOG](CHANGELOG.md) Unreleased current: each workspace change
  that alters behavior, interfaces or contributor workflow adds or updates
  its entry in the same PR.
- Stage explicit superproject paths; never `git commit -a`. Inspect
  `git diff --cached --stat`; only deliberately chosen gitlinks may move.
  Stale checkouts must not revert someone else's gitlink updates.
- `.gitmodules` tracks package `nightly` branches on `nightly`. Use
  [coordinated integration](docs/CI.md#coordinated-package-integration) when
  packages depend on one another; [README](README.md) covers clone setup.

## Documentation

Keep one maintained home per fact; link directly to its section elsewhere.
Search before adding docs, update incoming links when moving sections, and
check changed local links/anchors. Link external standards instead of copying
usage tutorials. READMEs serve humans in container terminals (`colcon`,
`ros2`); agent host commands belong in the Docker skill. Keep AGENTS files to
instructions, open decisions and links. Put test runs/measurements in commits
or dated investigations linked to current status.

| Information | Maintained home |
| --- | --- |
| Usage and design | Owning package's `README.md` |
| Robot launch | [YOLO README](realsense-yolov8-nitros-bridge/README.md#full-robot-pipeline) |
| Node/topic diagram | [thornbots_pkg](thornbots_pkg/README.md#nodes) |
| Hardware/migration status | [JAZZY_FLASH](docs/JAZZY_FLASH.md#hardware-status) |
| Open work | [ROADMAP](docs/ROADMAP.md) |
| Wire/timestamp contract | [UART_PROTOCOL](ros2_dji_serial_bridge/UART_PROTOCOL.md) |
| Defaults/message fields | Source declarations |

## Frames

Follow [REP 103](https://github.com/ros-infrastructure/rep/blob/master/rep-0103.rst)
units/axes and [REP 105](https://github.com/ros-infrastructure/rep/blob/master/rep-0105.rst)
frame roles. Document only choices and deviations at their owner: the
heading-fixed `root` base, the translation-only `nav_odom->odom` correction
([pose_translator and odometry](thornbots_pkg/README.md#pose_translator)), and the
field-centred [wire frame](ros2_dji_serial_bridge/UART_PROTOCOL.md#message-types).

## Wire compatibility

Use only the [current UART format](ros2_dji_serial_bridge/UART_PROTOCOL.md).
No old-format fallback, including the former 40-byte `CVData` payload.
Update firmware and the sim MCB emulator when they disagree with the protocol.

## Timestamps

Internal headers identify when data was true: sensor capture or carried input
stamp. Use `now()` only for freshly created data (e.g. a fire decision).
Prefer `*Stamped` to bare `Point`/`Twist` unless a standard interface requires
otherwise. Policy checks that each internal `.msg` has a `Header` and
documents its stamp; choosing the right meaning is still the author's job.

## Comments

Keep comments/docstrings under 10 lines; use them for interfaces, invariants
and tuned values. Link the README for longer design rationale.
