# Operator workflow package move — 2026-10-27

The maintained interface is [thornbots_pkg's operator workflow](../../thornbots_pkg/README.md#field-day-and-room-workflow).
`ros2 run thornbots_pkg operator_workflow` replaces the localization-package
command. The executable, ROS-free tests and operator reference move together;
localization backends and broad-field coverage remain in `sentry_localization`.
The concurrent Oct 26 mapping notes are retained in the moved reference and
root card. The local Notion mirror was updated without accessing Notion.

## Bridge provenance and lifecycle

`isaac_ros_common/docker/Dockerfile.thornbots` already installs
`ros-jazzy-foxglove-bridge`. The Oct 26 part 2 report and saved
`next/robot/sentry-20261026b/foxglove.log` record a separate bridge, version
3.6.0, listening on 8765 and stopped with the session; the report notes SSH
access was needed from archlinux. The saved evidence does not retain its exact
manual command. The existing read-only invocation in
`isaac-ros-startup/thornbots-launch.sh` supplies the settings reused here:

```bash
ros2 run foxglove_bridge foxglove_bridge --ros-args \
  -p port:=8765 -p address:=0.0.0.0 \
  -p 'capabilities:=[connectionGraph, assets]'
```

Mapping/localize own a separate bridge process group. Signals and final cleanup
stop both owned groups, escalating after the existing shutdown timeout.
Unexpected bridge termination fails the workflow and stops the robot launch.
A requested stop allows the bridge to exit before the launch without reporting
a bridge failure. The capabilities omit client publishing, services and all
parameter access. No Dockerfile or movement behavior changed.

## Checks

- Python 3.12 host quality checker and `actionlint -shellcheck=""` passed in
  workspace, localization, thornbots_pkg and startup; zero diagnostics, no
  baseline changes. Packages use the workspace checker because they have none.
- Both package suites: 281 tests, zero errors/failures/skips. Workflow tests
  include bridge failure, failure cleanup, SIGINT/SIGTERM propagation and both
  clean-stop orderings. Moved tests now satisfy thornbots_pkg's broader lint.
- Root and all 11 subcommand help stdout/stderr and exit codes match the
  original executable exactly. Script diff retains all arguments, gates and
  output except next-command package names and bridge supervision.
- Changed local Markdown links/anchors and exact root-card/local-mirror
  equality checked. No operator workflow entry was listed in ROADMAP.

Evidence is in `~/ros2_ws/move-operator-workflow-20261026/`: `quality-final.log`,
`package-tests-final.log`, `package-test-results-final.log`, `workflow-lint.log`,
`cli-compatibility.log` and `links.log`.

## Isolated room rehearsal

Created `isaac-agent-move-operator-workflow` with `agent_container.sh`, private
ROS domain 189 and partition `agent-move-operator-workflow-189`, six CPUs and
12 GiB. The Mac image already contained bridge 3.5.0; the robot session had
3.6.0. Sim dependencies were installed in the task container only. A parallel
sim compile hit the memory limit; rebuilding with two compilation jobs passed.
`smoke.sh` confirmed this checkout's package resolution and a clean ROS graph.

The full room circuit initially passed boot/pause/resume and its 11.8 m drive,
but save rejected a stale/non-increasing scan stamp. Repeated in a new session
at half simulation speed without changing any workflow gate. Two harness-only
failures were also retained: the probe initially offered the old websocket
subprotocol instead of the image's `foxglove.sdk.v1`, and one retry correctly
refused to overwrite a prior drive-evidence file.

The final session (`card-room-session-r4`) passed:

- New-package mapping, boot capture before movement, pause/resume, centred-head
  11.8267 m mapping circuit and return to boot within 0.0342 m.
- Explicit save, `prepare-room` and `check`, then a clean mapping stop.
- Restart at the original mark, new-package localize with `LOCALIZE PASS`,
  then sustained convergence (`--hold 30 --samples 20`) and clean stop.
- Websocket server-info in both stages advertised exactly `connectionGraph`
  and `assets`; port 8765 released after each workflow stop.

Circuit diagnostics: all 425 truth-stamped transforms available, p95 position
error 0.01165 m and maximum 0.01985 m. These are room-sim diagnostics, not
hardware or full-field acceptance; live scan/wall inspection remains required.
No physical robot, firmware or movement behavior was changed.

Additional evidence: `rehearsal.log`, `room-*.log`,
`room-{mapping,localize}-foxglove-server-info.json`, `card-room-drive-r4.json`,
`package-test-artifacts.tar.gz`, `processes-after.log` and `container-cleanup.log`.
Failed attempts remain under `failed-probe/`, `failed-save/` and
`failed-harness/`. The final process check found no owned ROS/sim/bridge
processes. Removed the task container and all its volumes; Colima remained
running because other containers were up. No other container was touched.
