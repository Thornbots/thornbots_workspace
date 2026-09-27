# isaac_ros-dev workspace

Use standard practices, and call out code that doesn't follow them.

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

`src/` is the `thornbots_workspace` repo and each package dir is a submodule.
A package change takes two commits: one in the package, one here bumping the
gitlink. Skip the bump and everyone else builds old code, and your next
`git submodule update` rewinds your work.

One logical change, one bump. A bump may move several gitlinks if they are one
change; a one-line submodule commit still gets its own. `git bisect` can't read
a bump that batches unrelated work.

Commit and push each logical change once it's tested, without being asked
(the user, 2026-09-27).

Push the submodule first. A gitlink to an unpushed commit breaks
`git submodule update --init` for everyone (`fatal: reference is not a tree`).

`.gitmodules` records each package's branch. After a clone, run the one-liner
in `README.md` or you're on a detached HEAD and commits land on no branch.

Read a package's `AGENTS.md` before working there. Keep it short: current
state, open questions, rules. Test runs and measurements go in commit messages.

Write `README.md` for a human in a container terminal: plain `colcon` and
`ros2`, no `dexec.sh`, `kill_launch.sh` or skills. Host-side equivalents go in
`AGENTS.md`.

## Timestamps

Every internal ROS message carries a `std_msgs/Header` stamped with when the
data was true (sensor capture, or the input's stamp carried through), not when
it was published. Use `now()` only for data created on the spot, like a fire
decision. Document the stamp's meaning in the `.msg` comment. Use `*Stamped`
over bare `Point`/`Twist` unless a standard interface requires the bare type.

## Comments

Keep comments and docstrings under 10 lines: topics, params, key invariants,
current tuned value. Add `# see README.md for design rationale` when trimming
would hide context a reader should know exists.
