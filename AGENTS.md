# isaac_ros-dev workspace

Call out code that doesn't follow standard practice. CV detection/tracking
comes first; [game context](ARCC_2026_SENTRY_CONTEXT.md) defines the field.
Use terse bullets for status/checklists; give rationale when asked.
Memory is disabled: do not read or write agent memory.

## Delegation

Delegate well-specified, high-volume repetitive edits to lower-cost agents
(Haiku/Luna). The delegating agent defines scope and acceptance checks,
resolves ambiguity, then reviews the diff and runs the checks itself.

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

- Ask before starting, restarting or stopping any laptop container or VM,
  including through scripts/services or Colima. On `ts-nano-*`, carry out
  requested container/image lifecycle work without separate confirmation.
  “dev” means `ts-nano-dev`.
- Ask before every sim integration test or bench run, even an obvious rerun.
- Check for running stacks before launching; ask before stopping anything you
  did not start, and clean up what you started.

## Branches

`nightly` integrates Jazzy; `main` is the promoted release
(`isaac_ros_jazzy_container`). Humble branches and
`isaac_ros_dev-x86_64-container` are frozen; do not work there.

## Packages

- Read the package's `AGENTS.md` before editing. `CLAUDE.md` stays `@AGENTS.md`.
- Commit with the existing Git identity and signing key tied to your GitHub
  account. Do not rewrite identity config, disable signing, bypass hooks, or
  add AI author, co-author, generated-by or session attribution; keep
  `.claude/settings.json` attribution disabled.
- Commit and push each tested logical change without being asked: package
  first, then one workspace gitlink bump per logical change. Never point at an
  unpushed commit.
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
| Hardware/migration status | [JAZZY_FLASH](JAZZY_FLASH.md#hardware-status) |
| Open work | [ROADMAP](ROADMAP.md) |
| Wire/timestamp contract | [UART_PROTOCOL](ros2_dji_serial_bridge/UART_PROTOCOL.md) |
| Defaults/message fields | Source declarations |

## Frames

Follow [REP 103](https://github.com/ros-infrastructure/rep/blob/master/rep-0103.rst)
units/axes and [REP 105](https://github.com/ros-infrastructure/rep/blob/master/rep-0105.rst)
frame roles. Document only choices and deviations at their owner: the
heading-fixed `root` base ([pose_translator](thornbots_pkg/README.md#pose_translator))
and the field-centred [wire frame](ros2_dji_serial_bridge/UART_PROTOCOL.md#message-types).

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
