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

Each package dir is its own git repo. Commit and push to `main` from inside the
package dir. Pushing from `src/` hits a different repo, the one holding the
top-level docs and `.claude/`.

Every package has an `AGENTS.md`. Read it before working there.

## Comments

Keep in-code comments and docstrings under 10 lines, holding the interface facts
a reader needs now: topics, params, key invariants, current tuned value.

`# see README.md for design rationale` when the trimmed comment would otherwise
hide context a future reader needs to know exists.
