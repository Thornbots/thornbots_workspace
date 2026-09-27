# isaac_ros-dev workspace

Call out code that doesn't follow standard practice.

## Skills

- [`isaac-ros-docker`](.claude/skills/isaac-ros-docker/): every docker command,
  and anything run inside the container.
- `writing:deslop`: all writing.
- `t3-fleet:serve-plan`: every plan or report.

## Priority

CV (target detection/tracking) comes first. Game rules and field geometry:
[`ARCC_2026_SENTRY_CONTEXT.md`](ARCC_2026_SENTRY_CONTEXT.md).

## Branches

`main` is Jazzy (`isaac_ros_jazzy_container`). Humble is frozen: no work on
`humble` branches or in `isaac_ros_dev-x86_64-container`.

## Packages

Each package dir is a submodule. Every package change needs a gitlink bump
here, or everyone else builds old code. One logical change per bump, even if
it moves several gitlinks or just one line.

Commit and push each logical change once it's tested, without being asked.
Push the submodule before the superproject.

`.gitmodules` records each package's branch. After a clone, run the one-liner
in `README.md` to get off detached HEAD.

Read a package's `AGENTS.md` before working there. Keep it short: current
state, open questions, rules. Test runs and measurements go in commit messages.

Write `README.md` for a human in a container terminal: plain `colcon` and
`ros2`, no `dexec.sh`, `kill_launch.sh` or skills. Host-side equivalents go in
`AGENTS.md`.

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
