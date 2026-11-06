# Colima DDS egress, 2026-11-06

Two Mini hangs around 02:00 and 09:10 followed `virtio_net` transmit queue
watchdogs. The preceding boot had sent 731,000 packets / 388 MB on eth0;
Lima usernet reached 1.5 GB RSS and 151% CPU in the first hang and 2.1 GB
within 32 minutes of a restart. The agent DDS profiles list three robot
Tailscale addresses with 32 participant ports each, so the many participants
in a sim stack generate sustained unicast discovery through usernet.

The agent container guard installs a Docker-ordered systemd unit in the VM.
It adds `DOCKER-USER` jumps for Docker's default and `br-*` bridges to a
CGNAT drop chain; the host-network robot container does not traverse it.
`-T` creates a separately named task-owned bridge outside these jumps for
cross-machine DDS tests. The unit runs after Docker starts on the next VM
boot; restart survival was not exercised while other agents were running.

An isolated ROS 2 Jazzy participant using the current XML still emitted
robot-directed UDP with `ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST`: tcpdump
captured a packet and reported 474 matching packets received by its filter.
After removing the explicit peers and restricting UDP to loopback, the same
probe produced zero matching packets in an eight-second capture; two local
participants discovered one another. Thus the environment variable alone
is not sufficient with the existing profiles.

The parked test harness also starts an inner stack without forwarding the
outer `foxglove:=false`; a Foxglove process was observed despite that argument.
The remote-DDS and Foxglove source switches require coordinated changes to
startup, robot/localization profiles, sim launch and the test harness.

A 92-second `mcb_parked` stationary-lateral hosted attempt on a two-CPU agent
container failed during bring-up: Gazebo requested an unbuilt firmware ELF
and the lockstep coordinator timed out. It did start the ROS stack, but did
not score a cell. VM-wide eth0 TX rose by 247,440 bytes / 420 packets; the
guard dropped 253,632 packets / 131,496,576 bytes. Other agents were running,
so neither measurement is attributable solely to this stack. Usernet RSS was
96,048 KiB before and 95,824 KiB after; instantaneous CPU was 0.0% and 0.2%.
These are not a controlled before/after benchmark.

With `-T`, a single test participant again produced robot-directed UDP on
VM eth0: tcpdump captured five packets and reported 444 received by the
filter. Repeated setup left one copy of each rule; the task container and its
exception network were removed afterward. The other two agent containers and
Colima remained running.
