#!/bin/bash
# Fast-forward each submodule's .gitmodules branch to the commit this
# workspace's HEAD points it at, so merging a workspace PR moves the
# packages with it.
#
#   advance_submodules.sh --check   # say what would move; fail on a diverged gitlink
#   advance_submodules.sh --push    # push the fast-forwards (needs SUBMODULES_TOKEN)
#
# A gitlink at or behind its branch is left alone. One that has diverged
# from it fails: rebase the package branch onto its base first.
set -euo pipefail

MODE="${1:-}"
case "$MODE" in --check|--push) ;; *) echo "usage: $0 --check|--push" >&2; exit 2 ;; esac
if [[ "$MODE" == --push && -z "${SUBMODULES_TOKEN:-}" ]]; then
    echo "advance_submodules: SUBMODULES_TOKEN is not set" >&2
    exit 2
fi

ROOT="$(git rev-parse --show-toplevel)"
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT
FAILED=0

while read -r key path; do
    name="${key#submodule.}"; name="${name%.path}"
    url="$(git -C "$ROOT" config -f .gitmodules "submodule.$name.url")"
    branch="$(git -C "$ROOT" config -f .gitmodules "submodule.$name.branch" || echo main)"
    sha="$(git -C "$ROOT" ls-tree HEAD "$path" | awk '{print $3}')"
    repo="$WORK/$name"
    git init -q --bare "$repo"
    git -C "$repo" fetch --no-auto-maintenance -q --filter=tree:0 "$url" "refs/heads/$branch:refs/heads/$branch" "$sha"
    tip="$(git -C "$repo" rev-parse "refs/heads/$branch")"
    if [[ "$tip" == "$sha" ]] || git -C "$repo" merge-base --is-ancestor "$sha" "$tip"; then
        echo "$path: $branch already has ${sha:0:7}"
    elif git -C "$repo" merge-base --is-ancestor "$tip" "$sha"; then
        n="$(git -C "$repo" rev-list --count "$tip..$sha")"
        if [[ "$MODE" == --push ]]; then
            push_url="https://x-access-token:${SUBMODULES_TOKEN}@${url#https://}"
            git -C "$repo" push -q "$push_url" "$sha:refs/heads/$branch"
            echo "$path: $branch ${tip:0:7} -> ${sha:0:7} ($n commits)"
        else
            echo "$path: $branch will move ${tip:0:7} -> ${sha:0:7} ($n commits)"
        fi
    else
        echo "$path: ${sha:0:7} has diverged from $branch (${tip:0:7}); rebase it first" >&2
        FAILED=1
    fi
done < <(git -C "$ROOT" config -f .gitmodules --get-regexp '\.path$')

exit "$FAILED"
