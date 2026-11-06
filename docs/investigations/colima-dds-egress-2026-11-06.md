# Colima hangs from agent-container DDS egress (2026-11-06)

Status: fixed by a VM guard plus off-by-default remote DDS and Foxglove. Not yet
validated across `colima stop/start` (other agent containers were running), nor
on a robot.

## Symptom

Colima on the Mac mini hung twice (about 02:00 and 09:10). The VM journal shows
`virtio_net eth0: NETDEV WATCHDOG ... transmit queue 0 timed out` for minutes,
with no OOM; Docker and SSH, forwarded over that link, then died. VM egress goes
through Lima's userspace NAT (`limactl usernet`): 151% CPU and 1.5 GB RSS during
the first hang, 2.1 GB 32 minutes after a restart.

## Cause

Bridged agent containers run the image's default Fast DDS profile
(`isaac_ros_common/docker/fastdds_cable.xml`), whose `initialPeersList` holds the
robots' Tailscale IPs with `maxInitialPeersRange` 32. Each participant sends
SPDP unicast to every peer address and port in range. tcpdump on the VM eth0 saw
731k packets / 388 MB to 100.93.23.77 in about 30 minutes; the NAT keeps state for
each flow.

## Measurements (2026-11-06, one agent container, Jazzy, Fast DDS 2.14.6)

Packets leaving the container for `100.64.0.0/10`, captured on `docker0`, one
`ros2 topic pub`, 15 s (the cable and `udp_only` rows are the old behavior):

| Fast DDS profile | `ROS_AUTOMATIC_DISCOVERY_RANGE` | to Tailscale | other off-box |
|---|---|---|---|
| cable (peers) | unset | 1056 | 1071 |
| cable (peers) | `LOCALHOST` | 1920 | 1930 |
| `udp_only` (peers) | `LOCALHOST` | 1920 | 1930 |
| none | `LOCALHOST` | 0 | 0 |
| none | unset | 0 | 14 (multicast) |
| peers-free XML (SHM+UDP) | unset / `LOCALHOST` | 0 | 14 / 0 |
| peers-free UDP-only XML | unset / `LOCALHOST` | 0 | 14 / 0 |
| loopback-only UDP-only XML | unset | 0 | 0 |

- **`LOCALHOST` does not suppress initial peers.** An XML profile's
  `initialPeersList` wins. Remote DDS off therefore means no peers profile and the
  range, together.
- **`LOCALHOST` adds the SHM transport back** to a UDP-only XML: 8 `fastrtps_*`
  segments with it, 0 without. The pinned UDP-only nodes exist to avoid SHM
  (stale-segment hangs, visibility from a robot shell), so they use loopback-only
  twins (interface whitelist and peer `127.0.0.1`) and
  `ROS_AUTOMATIC_DISCOVERY_RANGE=SYSTEM_DEFAULT`. 0 off-box packets, 0 SHM files.
- Discovery still works locally: 14 `LOCALHOST` participants with no profile found
  each other at the default peer range; a loopback-only pinned node and a
  `LOCALHOST` default node saw each other's topics in both directions, 6 of 6.

## Stack measurements

Stack: `sim.launch.py gui:=false rviz:=false` plus `auto.launch.py real_hardware:=false
localization_mode:=none use_rf2o:=false`, about 21 nodes. An `mcb_parked` lateral
cell could not run: the `firmware/MCBV3` submodule is not available in this
checkout. Capture on `docker0`, source = the container, destination
`100.64.0.0/10` / anything outside `172.16.0.0/12`.

| Case | Window | To Tailscale | Other off-box | Foxglove |
|---|---|---|---|---|
| defaults | 60 s | 0 | 0 | none |
| `foxglove:=true` | 30 s | 0 | 0 | 1 process |
| `remote_dds:=true` (guard on) | 40 s | 52,327 (~1,300/s) | 53,167 | none |

- The `remote_dds:=true` row is the old behavior; the VM guard dropped all of it, so
  the VM eth0 transmit delta (44 KB in 40 s) stayed at the idle level. Idle eth0
  transmit is 30 to 60 KB per 30 s; `limactl usernet` stays 47 to 82 MB RSS, 0%
  CPU, bouncing with other traffic.
- Pinned nodes in the defaults run (`pose_translator` etc.): profile
  `fastdds_udp_only_local.xml`, range `SYSTEM_DEFAULT`; with remote on:
  `fastdds_udp_only.xml`.
- The first defaults run showed 8,064 packets: `sim`'s `gz_bridge`
  (`sim/clock_bridge.py`) still pinned the peers profile. All pinned sites now go
  through `sim/dds_switch.py`'s `udp_env()`.

## Guard (VM)

`scripts/agent_container.sh` installs `/usr/local/sbin/thornbots-agent-guard` and a
`thornbots-agent-guard.service` unit in the Colima VM (`WantedBy`/`PartOf`
`docker.service`). It creates chain `THORNBOTS-AGENT` (`-d 100.64.0.0/10 -j DROP`)
and jumps to it from `DOCKER-USER` for `docker0` and `br+`. Every check uses
`iptables -C` first, so a rerun adds nothing. Persistence: the unit and script live
on the VM disk, which survives `colima stop/start`, and the unit reruns after every
Docker start, when Docker recreates `DOCKER-USER`; `up` also re-applies it. That is
why it is a unit and not Colima's provision list, which would also need the VM
restarted to take effect.

- Opt-out: `up -T` creates a dedicated bridge named `ta<cksum>` that `br+` does not
  match, and sets `THORNBOTS_REMOTE_DDS=true`. Measured: 1440 packets to
  `100.64.0.0/10` on the VM eth0 in 25 s from one `ros2 topic pub`, `limactl usernet`
  RSS 47 to about 99 MB within 6 s. Removed with the container.
- Host-network container: UDP to `100.93.23.77:9998` from `--network host` reached
  the VM eth0 (5 of 5); from a bridged container (`:9999`) 0 of 5. Host-network
  traffic takes `OUTPUT`, not `DOCKER-USER`.
- Since it was installed, the guard has dropped 5.77M packets / 2.99 GB. At the end
  of this work `isaac-agent-t17rl` (172.17.0.2), started before the switch existed,
  was still sending about 1,150 packets/s to Tailscale and the guard was dropping
  all of it. Its launches pick up the defaults when restarted.
- IPv6 (`fd7a:115c:a1e0::/48`) is not guarded: the peers list is IPv4 only.
- **Not tested:** a real `colima stop/start` (two other agent containers' work was
  running), and a robot.

## Changes

`isaac_ros_common` (guard follow-up, `THORNBOTS_*` container env, `up -F/-T`,
`dexec.sh`, bashrc), `thornbots_pkg` (`remote_dds`, `fastdds_udp_only_local.xml`,
`operator_workflow`), `sentry_localization` (`fastdds_no_shm_local.xml`), `sim`
(`dds_switch.py`, `foxglove:=`, `remote_dds:=`), `isaac-ros-startup`
(`THORNBOTS_REMOTE_DDS`, `THORNBOTS_FOXGLOVE`). Robot defaults: remote DDS off,
Foxglove on; sim, tests and agent containers: both off. The image's bashrc part
takes effect on the next image build; `dexec.sh` covers agent containers now.
