# isaac_ros-dev workspace

Use standard practices and callout when the current practicies in the code don't
match the standard.

## Skills

- [`isaac-ros-docker`](.claude/skills/isaac-ros-docker/): every docker command,
  and anything run inside the container.
- `writing:deslop`: all writing.
- `t3-fleet:serve-plan`: every plan or report.

## Priority

CV (target detection/tracking) comes first. Read
[`ARCC_2026_SENTRY_CONTEXT.md`](ARCC_2026_SENTRY_CONTEXT.md) for the game rules
and field geometry.

## Packages

`src/` is the `thornbots_workspace` repo; every package dir under it is a
submodule. So a package change takes two commits: one in the package dir, one
here to bump the gitlink. Your own image builds fine either way (the Docker
context is the working tree), but skip the gitlink bump and everyone else builds
the old code, and a later `git submodule update` rewinds your work out of the
working tree.

One logical change, one bump. Group by what changed, not by how much: a bump may
move several gitlinks when they are one change, and a one-line submodule commit
still earns its own. Batching a week of unrelated commits into a single bump
leaves a gitlink diff that `git bisect` can't read.

Push the submodule before the superproject. A gitlink pointing at a commit that
exists only on your machine breaks `git submodule update --init` for everyone
with `fatal: reference is not a tree`, which is worse than a stale gitlink
because a stale one still clones.

Branches differ per package and `.gitmodules` records them. After a clone,
`README.md` has the one-liner that puts each submodule back on its branch —
without it you are on a detached HEAD and commits land on no branch.

Every package has an `AGENTS.md`. Read it before working there.

Write each `README.md` for a human in a container terminal: plain `colcon`
and `ros2` commands, no `dexec.sh`, `kill_launch.sh` or skill references.
The host-side equivalents go in that package's `AGENTS.md`.

## Comments

Keep in-code comments and docstrings under 10 lines, holding the interface facts
a reader needs now: topics, params, key invariants, current tuned value.

`# see README.md for design rationale` when the trimmed comment would otherwise
hide context a future reader needs to know exists.
