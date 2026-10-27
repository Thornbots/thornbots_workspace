# thornbots_workspace

The `src/` root of the Thornbots Sentry's Isaac ROS dev workspace.

`main` is on ROS 2 Jazzy and Isaac ROS 4.6. The `humble` branch here and in
every package holds the Humble tree, **frozen since 2026-09-27**: it takes no
more work; every robot now runs JetPack 7.2.1, so it is history only.
A GitHub ruleset makes it read-only (no pushes or deletion, admins
included); the repos still unlocked are listed in
[ROADMAP T36](docs/ROADMAP.md#short-todos).

`nightly` integrates changes across the workspace and all eleven package repos.
On this branch, `.gitmodules` tracks each package's `nightly` branch while
keeping exact commit pins. [CHANGELOG.md](CHANGELOG.md) records unreleased
changes to carry into `main`; update it when adding work to nightly.

## Map a new field

This is a deliberate copy of the
[Notion mapping doc](https://app.notion.com/p/fff357611caa4131b216742bb7c6e048);
keep both in sync. Technical reference:
[field-day and room workflow](https://github.com/Thornbots/sentry_localization/blob/nightly/README.md#field-day-and-room-workflow).
Boot/image reference:
[startup](https://github.com/Thornbots/isaac-ros-startup/blob/nightly/README.md#use),
[release images](https://github.com/Thornbots/isaac_ros_common/blob/nightly/docker/README.md#pulling-from-github-container-registry).

1. **Place on the taped start before power-on; verify the release image — robot host.**
   Keep the robot still while the IMU settles; moving it then caused heading drift.
   Clear the route, check battery/pod contact, disable firing. Controller ON: left
   switch MID, right switch MID (manual no-spin); centre the head with the right
   stick, then leave that stick neutral. Keep these settings through acceptance.
   With `thornbots` initially running, enter the team's approved release SHA:

   ```bash
   read -r -p 'Approved release workspace SHA: ' RELEASE_SHA
   export RELEASE_IMAGE="ghcr.io/thornbots/isaac-ros:sha-${RELEASE_SHA}-arm64-jetpack"
   docker image inspect "$RELEASE_IMAGE" --format '{{.Id}}'
   docker inspect thornbots-runtime --format '{{.Config.Image}} {{.Image}}'
   journalctl -b -u thornbots --no-pager
   ```

   Turning the controller off invalidates the session. After any SWD flash,
   power-cycle the MCB before trusting odometry (warm reset leaves Pico I2C dead).
   MCB power-cycling reboots the Jetson via shared power: re-sync the clock,
   restart the container and begin a new session (steps 2–4).

   PASS: runtime image ID matches the installed approved release image; head stays
   still, chassis is at red `(-4.625, 0)` facing +x or blue `(4.625, 0)` facing -x.

2. **Give the manual session sole ownership; synchronize UTC — host.**

   ```bash
   sudo cp -p /etc/thornbots/launch.env /etc/thornbots/launch.env.before-field-map
   sudo systemctl stop thornbots
   systemctl is-active thornbots
   docker ps --format '{{.Names}}'
   sudo systemctl start systemd-timesyncd
   timedatectl status
   date -u
   # Only after correct UTC and synchronization:
   sudo systemctl stop systemd-timesyncd
   ```

   PASS: service is `inactive` (nonzero exit is expected), runtime and old manual
   stacks are gone, UTC is correct and `System clock synchronized: yes` before ROS.

3. **Open container shells A and B using the release image — host, then container.**
   Set `ISAAC_ROS_WS` to the host directory recorded by `ISAAC_ROS_WS_HOST` in
   `/etc/thornbots/launch.env`; use that same workspace in both host terminals:

   ```bash
   isaac-ros activate --start-only
   ```

   From another host terminal compare the development container with step 1:

   ```bash
   docker inspect isaac_ros_jazzy_container --format '{{.Config.Image}} {{.Image}}'
   ```

   In **both container shells**, source only the image install; choose a new,
   identical session name (`oct31-blue-01` for blue):
   `$SESSION` is one attempt's folder; use a new name for every attempt.
   `operator_workflow` runs the mapping, save, registration and AMCL acceptance steps.

   ```bash
   source /opt/ros/jazzy/setup.bash
   source /workspaces/ros2_ws/install/setup.bash
   export ROS_DOMAIN_ID=1 RMW_IMPLEMENTATION=rmw_fastrtps_cpp
   export FASTRTPS_DEFAULT_PROFILES_FILE=/etc/fastdds/profile.xml
   export SESSION=/workspaces/isaac_ros-dev/maps/oct31-red-01
   export HEAD_OFF='enable_cv_target_bridge:=false enable_target_selector:=false enable_target_tracker:=false'
   ros2 pkg prefix thornbots_pkg
   ros2 pkg prefix sentry_localization
   ros2 run sentry_localization operator_workflow --help
   test ! -e "$SESSION"
   df -h /workspaces/isaac_ros-dev
   ```

   PASS: same release image ID as step 1, both prefixes under
   `/workspaces/ros2_ws/install/`, workflow available, new session and enough space.

4. **Start SLAM in A; capture boot in B before moving either chassis or head.**
   Verify `/dev/ttyUSB0` is the lidar; substitute its actual device if different.

   ```bash
   # A: leave running
   ls -l /dev/ttyUSB0
   ros2 run sentry_localization operator_workflow mapping "$SESSION" $HEAD_OFF lidar_serial_port:=/dev/ttyUSB0
   # B: after A asks for boot-pose, before ANY movement
   ros2 run tf2_ros tf2_echo root head
   # Check yaw ≈ 0, then Ctrl-C before capture:
   ros2 run sentry_localization operator_workflow boot-pose "$SESSION"
   cat "$SESSION/boot.json"
   ```

   PASS: `PREFLIGHT OK`, `BOOT CAPTURE OK`, recorded team/raw start agrees with the
   mark, head still and RViz scans form consistent walls.

5. **Drive ≤0.2 m/s with the head still; watch raw odometry and RViz — B.**
   First a straight out-and-back, then a short strafe and fore/aft check. Cover
   lanes, centre, ends and obstacle backs with overlapping views and level stops.

   ```bash
   ros2 topic echo /odom --field pose.pose.position
   # Ctrl-C stops this observer only. Before a rough transfer:
   ros2 run sentry_localization operator_workflow pause "$SESSION"
   # Drive across, stop level, let chassis settle, then:
   ros2 run sentry_localization operator_workflow resume "$SESSION"
   ```

   PASS: x/y follow travel even after strafing; `/map` and `/scan` overlap with
   single walls; rough transfers report `SCAN INSERTION PAUSED` then `RESUMED`.

6. **Return exactly to the boot mark/heading; park, inspect and save — B.**
   Resume insertion, wait for loop closure/fresh map, inspect coverage and walls.
   Keep A running and the head still. Boot anchors registration and the AMCL
   start; save requires SLAM `map->root` within 0.15 m/0.15 rad of boot, not raw
   odometry ([gate rationale](sentry_localization/README.md#preparation-and-rationale)).

   ```bash
   ros2 run sentry_localization operator_workflow save "$SESSION"
   ls -lh "$SESSION/snapshot/"
   ```

   PASS: `SAVE OK`; nonempty `map.pgm`, `map.yaml`, `map.posegraph`, `map.data`,
   `boot.json`. Never relax the gate, substitute autosaves or recapture after a lap.

7. **Register the captured chassis heading in radians; check deployment — B.**

   ```bash
   # Red facing +x:
   ros2 run sentry_localization operator_workflow align "$SESSION" --yaw 0
   # Blue facing -x: use this INSTEAD of the red command:
   # ros2 run sentry_localization operator_workflow align "$SESSION" --yaw 3.141592653589793
   ros2 run sentry_localization operator_workflow check "$SESSION"
   ```

   PASS: check exits successfully; `deployment/field.pgm`, `field.yaml` and
   `registration.json` exist and the registered raster looks correct.

8. **Stop A with Ctrl-C, wait for exit, then start AMCL in A; check in B.**
   Stay at the live team's contract start with head still.

   ```bash
   # A: leave running after LOCALIZE PASS
   ros2 run sentry_localization operator_workflow localize "$SESSION" $HEAD_OFF lidar_serial_port:=/dev/ttyUSB0
   # B: after LOCALIZE PASS
   ros2 run sentry_localization operator_workflow convergence "$SESSION" --hold 30 --samples 20
   ```

   PASS: `LOCALIZE PASS`, `CONVERGED` and scan/wall overlap; make a slow controlled
   away-and-back, return to the mark, then repeat the parked convergence command.

9. **Set match boot — stop A, exit B then original activation shell A; host.**
   Confirm the development container has exited. Edit the existing environment;
   preserve unrelated keys/arguments, remove any `USE_WS_OVERLAY` assignment.

   ```bash
   docker ps --format '{{.Names}}'
   sudoedit /etc/thornbots/launch.env
   ```

   Set these values for red (use the actual session and step 1's immutable image
   tag; replace the image placeholder with that literal tag):

   ```bash
   THORNBOTS_IMAGE=ghcr.io/thornbots/isaac-ros:sha-RELEASE_SHA-arm64-jetpack
   ROS_DOMAIN_ID=1
   LOCALIZATION_MODE=amcl
   LIDAR_SERIAL_DEVICE=/host-dev/rplidar
   AUTO_LAUNCH_ARGS="real_hardware:=true use_rf2o:=false autosave_map:=false map_file:=/workspaces/isaac_ros-dev/maps/oct31-red-01/deployment/field amcl_initial_x:=-4.625 amcl_initial_y:=0.0 amcl_initial_yaw:=0.0"
   ```

   For blue use its session and `amcl_initial_x:=4.625`; **root yaw stays 0 for
   both teams**, unlike blue chassis yaw in step 7. `map_file` has no extension.
   Keep `use_rf2o:=false`: rf2o replay showed false motion during head sweeps.

   ```bash
   sudo systemctl start systemd-timesyncd
   timedatectl status
   date -u
   # Only after correct UTC and synchronization:
   sudo systemctl enable thornbots
   sudo systemctl start thornbots
   systemctl status thornbots --no-pager
   docker inspect thornbots-runtime --format '{{.Config.Image}} {{.Image}}'
   ```

   PASS: sole stack owner, active service without restart loops, same approved
   image ID; controller still in manual mode, head still. Retain the whole session.

10. **Reboot on the start mark, then verify the running boot stack.** Keep firing
    disabled and controller in manual mode throughout. Host:

    ```bash
    sudo reboot
    # Reconnect after boot:
    systemctl status thornbots --no-pager
    journalctl -b -u thornbots --no-pager
    docker inspect thornbots-runtime --format '{{.Config.Image}} {{.Image}}'
    docker exec -it -u admin thornbots-runtime bash
    ```

    In that runtime shell repeat step 3's image-only sourcing/environment/session
    exports (skip activation and the new-session test), then:

    ```bash
    ros2 pkg prefix sentry_localization
    ros2 lifecycle get /map_server
    ros2 lifecycle get /amcl
    ros2 param get /map_server yaml_filename
    ros2 param get /amcl use_sim_time
    ros2 run sentry_localization operator_workflow convergence "$SESSION" --hold 30 --samples 20
    ```

    PASS: approved image ID, baked package prefix, both lifecycle nodes `active`,
    intended `deployment/field.yaml`, `use_sim_time` false, `CONVERGED`, correct
    live team/raw start and wall overlap; no clock-step/backend/restart failures.

Notes:

- **Head control on nightly:** both workflow modes launch `auto.launch.py`, not
  just localization/serial; CV selector/tracker/aim default on.
  `$HEAD_OFF` suppresses them during manual mapping/localization. There is no
  Jetson patrol: with no camera target the head makes idle looks (last enemy,
  hit hold, enemy start zone). The boot service also launches YOLO, so match
  boot tracks targets. At firmware `8d46da5`, left switch UP schedules
  automatic aim/fire; leaving UP selects joystick gimbal control. Select left
  MID/right MID, centre using the right stick and leave it neutral. This holds
  the commanded yaw; verify it physically throughout. No ROS workflow command
  locks the head. Do not use autonomous/keyboard modes during acceptance.
- The image **must contain the release workflow and launch arguments**. No host
  overlay/build is required: the Dockerfile installs these packages in
  `/workspaces/ros2_ws`. `activate --start-only` uses the local CLI image tag;
  ID equality is the gate that it is the same release. CLI tags hash Dockerfiles,
  not package sources; the journal's `WS host` commit describes the host checkout,
  not proof of baked code. If IDs/prefixes/help differ, stop and deploy the approved
  image using the release-image reference before continuing. Do not set
  `USE_WS_OVERLAY`.
- Field starts must match the physical field/referee contract. Mapping does not
  change firmware routes or CV coordinates. If pods moved while powered off,
  power-cycle on the mark before starting. Keep controller on: Oct 25 controller-off
  IMU recalibration interrupted POSE. Head/mount and raw-x failures remain unresolved.
- Mapping uses raw wheel passthrough, not rf2o. Boot capture checks 20 fresh scans
  and at least 2 stationary seconds within 3 cm/0.03 rad; save requires the same
  live session and the
  [SLAM return gate](sentry_localization/README.md#preparation-and-rationale).
  Convergence requires fresh pose,
  scans/TF, xy std ≤0.25 m, yaw std ≤0.15 rad, start distance ≤0.4 m and yaw
  difference ≤0.25 rad over 30 s/20 samples. Covariance alone is not accuracy.
- Practice without referee: add `--no-referee --team red` (or blue) to both
  mapping/localize. `--room` rehearses without a referee, keeping boot coordinates
  instead of field registration. Add it to mapping, then run
  `ros2 run sentry_localization operator_workflow prepare-room "$SESSION"`
  instead of `align`; localize infers room mode. Sim: add `--sim-time` to mapping,
  boot-pose, pause/resume, save, localize and convergence, plus
  `real_hardware:=false rviz:=false` to mapping/localize; omit lidar-port override.
- Boot's full stack does not run the workflow's start/convergence gates. Keep
  manual control until acceptance; do not launch mapping/localize beside it.
  Systemd, reboot, image delivery and physical controls need robot-side acceptance.

| Symptom | Action |
| --- | --- |
| Existing stack, serial busy, doubled topics | Stop service/previous manual launch and wait for exit. Keep one UART/lidar owner. |
| Wrong UTC, stale/future scans, TF extrapolation | Stop ROS, synchronize UTC, stop NTP for manual ROS and start a new session. Never step time under ROS. |
| No nodes in attached shell | Check domain/profile and baked prefixes; attached-shell DDS discovery remains open. Inspect logs too. |
| Head moves, walls double or matching invents sideways travel | Check manual switches/right stick and `$HEAD_OFF`; stop, revisit known level geometry, remap if distorted. No mount fix is claimed. |
| Raw x freezes after strafe | Stop; inspect pod contact/raw odometry. Retain evidence; new attempt after resolving/resetting on mark. SLAM cannot repair firmware odometry. |
| Boot capture/save rejected | Check fresh fixed-geometry scans, stationary head/chassis, return and boot provenance; remap with a new session. Never bypass checks. |
| Team/heading or AMCL rejection | Check referee, contract start, radians and deployed map; stay parked, correct cause and repeat acceptance. |
| Need rollback | Host: stop `thornbots`, restore `/etc/thornbots/launch.env.before-field-map` to `/etc/thornbots/launch.env`, start service. This restores its previous mode, possibly blank-map SLAM. Retain all evidence. If leaving ROS stopped, restart timesyncd. |

## Working with submodules

Each package is a submodule:

```sh
git clone --recurse-submodules https://github.com/Thornbots/thornbots_workspace.git src
```

That checks out the exact commits this repo pins, each on a detached HEAD.
Build from that state to reproduce the workspace. To change a package, start a
branch where it stands, then rebase onto the package's `nightly` only when you
mean to take newer work:

```sh
cd thornbots_pkg
git switch -c my-change
git fetch origin && git rebase origin/nightly   # optional: move to the branch tip
```

Do not run `git checkout nightly` in every submodule: it jumps each package to
its branch tip, which can differ from the pinned commit, and nested
submodules have no configured branch.

A package change takes two commits: one in the package, one here to bump the gitlink. `Dockerfile.thornbots` builds from this directory, so your image picks up the change without the bump. Skip it and everyone else builds the old code, and your next `git submodule update` rewinds the package.

[CI and validation](docs/CI.md) covers repository checks, lint debt, and
robot images. Only `main` runs CI and builds images (`nightly` is covered by
[local checks](docs/CI.md#local-checks-for-prs-into-nightly) and the
[nightly tests](docs/CI.md#nightly-tests)); pushes to `main`
publish tested images to `ghcr.io/thornbots/isaac-ros`, using exact gitlinks.

One logical change, one bump: a bump may move several gitlinks when they belong
to the same change, and a one-line package commit still earns its own. Push the
package before you push here — a gitlink pointing at an unpushed commit fails
everyone else's `git submodule update --init`.

A change across packages can live on a branch of the same name in each, with
this repo's branch bumping the gitlinks. Follow the
[coordinated package integration procedure](docs/CI.md#coordinated-package-integration).

| Path | Branch | Role |
| --- | --- | --- |
| `thornbots_pkg` | `nightly` | Hardware interface, URDF, CV target selection, `auto.launch.py` |
| `sentry_localization` | `nightly` | SLAM / AMCL / EKF backends |
| `sim` | `nightly` | gz-sim worlds and the localization test suite |
| `realsense-yolov8-nitros-bridge` | `nightly` | YOLOv8 detection on the RealSense stream |
| `Realsense_ROI_Depth_Rectifier` | `nightly` | Depth rectification for detection ROIs |
| `ros2_dji_serial_bridge` | `nightly` | Serial link to the DJI Type-C board |
| `sllidar_ros2` | `nightly` | RPLIDAR driver (fork) |
| `rf2o_laser_odometry` | `nightly` | Scan-matched odometry (fork) |
| `isaac_ros_common` | `nightly` | Isaac ROS base, our Dockerfiles and container scripts |
| `isaac-ros-startup` | `nightly` | systemd service that starts the robot stack at boot |
| `firmware/MCBV3` | `nightly` | MCB firmware, opt-in: not cloned by default, see below |

Start with [ROADMAP.md](docs/ROADMAP.md) for open work, robot checks and links to its plans.
[ARCC_2026_SENTRY_CONTEXT.md](docs/ARCC_2026_SENTRY_CONTEXT.md) covers competition
rules and hardware context. The [documentation ownership map](AGENTS.md#documentation)
identifies where shared information belongs; link there instead of copying it.

### MCB firmware

`firmware/MCBV3` is the MCB team's repo, so a wire change and its firmware half can be checked together. It's `update = none` in `.gitmodules`: `clone --recurse-submodules` and `submodule update --init` skip it, so the robots never fetch it. `firmware/COLCON_IGNORE` and `.dockerignore` keep it out of colcon and the image. To get it, with its own taproot submodules:

```sh
git submodule update --init --checkout firmware/MCBV3
git -C firmware/MCBV3 submodule update --init --recursive
```
