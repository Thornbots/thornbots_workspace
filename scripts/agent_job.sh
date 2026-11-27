#!/usr/bin/env bash
# agent_job.sh -- run a long host job detached; wait for it with one blocking call.
#
#   agent_job.sh start NAME [-C DIR] -- CMD...   # detach; log, pid, then rc on exit
#   agent_job.sh wait  NAME [-t SECS] [-p SECS] [-n LINES] [-m ERE [-c N]]
#   agent_job.sh wait  -f FILE -m ERE [-c N] [-t SECS] [-p SECS]   # a log you did not start
#   agent_job.sh status [NAME]
#   agent_job.sh stop  NAME                       # SIGTERM the job's process group
#
# Jobs live in $AGENT_JOB_ROOT (default ~/.local/state/agent-jobs)/NAME: cmd, log,
# pid, rc (written atomically when the command ends, even on SIGTERM/SIGINT/SIGHUP).
# `wait` returns as soon as rc exists (exit = the job's rc) or -m matches N times
# (exit 0), prints progress every -p seconds (default 60), and gives up after -t
# (default 540, under the 10-minute tool ceiling) with exit 124: re-run it.
# 125: the runner died without writing rc (SIGKILL); 1: the job ended before -m matched.
# Usage notes: the isaac-ros-docker skill, "Long jobs". bash 3.2 compatible.
set -uo pipefail

ROOT="${AGENT_JOB_ROOT:-$HOME/.local/state/agent-jobs}"
SELF="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)/$(basename "${BASH_SOURCE[0]}")"

die() { echo "agent_job.sh: $*" >&2; exit 2; }
usage() { sed -n '3,7p' "$SELF" | sed 's/^# \{0,1\}//' >&2; exit 2; }

valid_name() { [[ "${1:-}" =~ ^[A-Za-z0-9][A-Za-z0-9._-]*$ ]]; }
alive() { [ -n "${1:-}" ] && kill -0 "$1" 2>/dev/null; }
elapsed() { printf '%dm%02ds' $(($1 / 60)) $(($1 % 60)); }

# Internal: the detached runner. It is its own session/process-group leader.
cmd_run() {
    local dir="$1"; shift
    echo "$$" > "$dir/pid.tmp" && mv "$dir/pid.tmp" "$dir/pid"
    local child rc
    "$@" < /dev/null >> "$dir/log" 2>&1 &
    child=$!
    trap 'kill -TERM "$child" 2>/dev/null' TERM
    trap 'kill -INT "$child" 2>/dev/null' INT
    trap 'kill -HUP "$child" 2>/dev/null' HUP
    while :; do  # a trapped signal ends `wait` early with status > 128
        wait "$child"; rc=$?
        alive "$child" || break
    done
    date +%s > "$dir/ended"
    echo "$rc" > "$dir/rc.tmp" && mv "$dir/rc.tmp" "$dir/rc"
}

cmd_start() {
    local name="${1:-}"; valid_name "$name" || die "start: NAME must match [A-Za-z0-9][A-Za-z0-9._-]*"
    shift
    local cwd="$PWD"
    while [ "$#" -gt 0 ] && [ "$1" != "--" ]; do
        case "$1" in
            -C) cwd="${2:?-C needs a directory}"; shift 2 ;;
            *) die "start: unknown option $1" ;;
        esac
    done
    [ "${1:-}" = "--" ] && shift
    [ "$#" -gt 0 ] || die "start: no command (start NAME -- CMD...)"
    local dir="$ROOT/$name"
    if [ -e "$dir" ]; then
        if [ -f "$dir/rc" ]; then
            die "start: job '$name' already ran (rc=$(cat "$dir/rc")); pick a new name or remove $dir"
        fi
        die "start: job '$name' exists and has not finished; wait for it or pick a new name"
    fi
    { mkdir -p "$ROOT" && mkdir "$dir"; } || die "start: cannot create $dir"
    printf '%q ' "$@" > "$dir/cmd"; echo >> "$dir/cmd"
    echo "$cwd" > "$dir/cwd"
    date +%s > "$dir/started"
    : > "$dir/log"
    # A new session keeps the job alive when the calling tool's shell is killed.
    (
        cd "$cwd" || exit 1
        if command -v setsid >/dev/null; then
            exec setsid "$SELF" _run "$dir" "$@"
        fi
        exec python3 -c 'import os, sys; os.setsid(); os.execv(sys.argv[1], sys.argv[1:])' \
            "$SELF" _run "$dir" "$@"
    ) < /dev/null > /dev/null 2>&1 &
    local _
    for _ in $(seq 1 50); do [ -f "$dir/pid" ] && break; sleep 0.1; done
    [ -f "$dir/pid" ] || die "start: runner did not start; see $dir"
    echo "started $name (pid $(cat "$dir/pid"), log $dir/log)"
    echo "  wait:  $SELF wait $name"
}

state_of() {  # prints running|rc=N|died
    local dir="$1"
    if [ -f "$dir/rc" ]; then echo "rc=$(cat "$dir/rc")"; return; fi
    if alive "$(cat "$dir/pid" 2>/dev/null)"; then echo running; return; fi
    if [ -f "$dir/rc" ]; then echo "rc=$(cat "$dir/rc")"; return; fi  # ended between checks
    echo died
}

count_matches() { grep -cE -- "$2" "$1" 2>/dev/null || true; }

cmd_wait() {
    local name="" file="" pattern="" want=1 timeout=540 every=60 lines=20
    if [ "$#" -gt 0 ] && [ "${1#-}" = "$1" ]; then name="$1"; shift; fi
    while [ "$#" -gt 0 ]; do
        case "$1" in
            -f) file="${2:?}"; shift 2 ;;
            -m) pattern="${2:?}"; shift 2 ;;
            -c) want="${2:?}"; shift 2 ;;
            -t) timeout="${2:?}"; shift 2 ;;
            -p) every="${2:?}"; shift 2 ;;
            -n) lines="${2:?}"; shift 2 ;;
            *) die "wait: unknown option $1" ;;
        esac
    done
    local dir=""
    if [ -n "$name" ]; then
        [ -z "$file" ] || die "wait: give NAME or -f FILE, not both"
        valid_name "$name" || die "wait: bad NAME"
        dir="$ROOT/$name"
        [ -d "$dir" ] || die "wait: no job '$name' under $ROOT"
        file="$dir/log"
    else
        [ -n "$file" ] && [ -n "$pattern" ] || die "wait: give NAME, or -f FILE with -m ERE"
    fi
    local label="${name:-$file}" start=$SECONDS next=$every state n waited last
    while :; do
        if [ -n "$pattern" ]; then
            n=$(count_matches "$file" "$pattern")
            if [ "${n:-0}" -ge "$want" ]; then
                echo "agent_job.sh: $label matched /$pattern/ ${n}x after $(elapsed $((SECONDS - start)))"
                grep -E -- "$pattern" "$file" | tail -n 5
                return 0
            fi
        fi
        if [ -n "$dir" ]; then
            state=$(state_of "$dir")
            case "$state" in
                rc=*)
                    echo "agent_job.sh: $name finished, $state, after $(elapsed $((SECONDS - start))) of waiting"
                    tail -n "$lines" "$file"
                    if [ -n "$pattern" ]; then
                        echo "agent_job.sh: $name ended before /$pattern/ matched $want time(s)" >&2
                        return 1
                    fi
                    return "${state#rc=}" ;;
                died)
                    echo "agent_job.sh: $name runner died without writing rc (SIGKILL?)" >&2
                    tail -n "$lines" "$file"
                    return 125 ;;
            esac
        fi
        waited=$((SECONDS - start))
        if [ "$waited" -ge "$timeout" ]; then
            echo "agent_job.sh: $label still running after $(elapsed "$waited"); re-run the same wait" >&2
            tail -n 3 "$file" 2>/dev/null
            return 124
        fi
        if [ "$waited" -ge "$next" ]; then
            last=$(tail -n 1 "$file" 2>/dev/null | cut -c1-160)
            echo "agent_job.sh: $label waiting $(elapsed "$waited"), log $(wc -l < "$file" 2>/dev/null | tr -d ' ') lines: $last"
            next=$((next + every))
        fi
        sleep 1
    done
}

cmd_status() {
    local d name
    [ -d "$ROOT" ] || { echo "no jobs under $ROOT"; return 0; }
    for d in "$ROOT"/${1:-*}; do
        [ -d "$d" ] || continue
        name=$(basename "$d")
        printf '%-32s %-9s %s\n' "$name" "$(state_of "$d")" "$(cut -c1-100 "$d/cmd" 2>/dev/null)"
    done
}

cmd_stop() {
    local name="${1:-}"; valid_name "$name" || die "stop: bad NAME"
    local dir="$ROOT/$name" pid
    pid=$(cat "$dir/pid" 2>/dev/null) || die "stop: no job '$name'"
    [ "$(state_of "$dir")" = running ] || { echo "$name: $(state_of "$dir")"; return 0; }
    kill -TERM -- "-$pid" 2>/dev/null || kill -TERM "$pid"
    echo "sent SIGTERM to $name (process group $pid); container-side processes need kill_launch.sh"
}

case "${1:-}" in
    start) shift; cmd_start "$@" ;;
    wait) shift; cmd_wait "$@" ;;
    status) shift; cmd_status "$@" ;;
    stop) shift; cmd_stop "$@" ;;
    _run) shift; cmd_run "$@" ;;
    *) usage ;;
esac
