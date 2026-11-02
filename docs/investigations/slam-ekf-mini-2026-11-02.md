# SLAM/EKF recovery on the Mini, 2026-11-02

Track H and SIM-wall/SIM-returns remain open. This investigation reconstructs
the previously reported harness changes locally; historical laptop measurements
and unpushed work are not evidence for the rebuilt candidates.

## Environment and provenance

- Host: `Blaises-Mini.tail2b35ba.ts.net`; no other machine accessed.
- Child worktree: `/Users/blaise/.t3/worktrees/src/t3-e5b66d7e`.
- Workspace base: `a522d7a` (`origin/nightly`, fetched November 2).
- Container: `isaac-agent-track-h-mini`, domain 142, private partition,
  2 CPUs, 4 GiB memory; sequential build, one compiler job.
- Evidence: `.track-h-evidence/` in this worktree; initial build log is
  `track-h-build.log`. Evidence is local and is not shipped with the repository.
- Initial host swap usage: 1193.81 MiB; unchanged during compilation.
- No matching pushed H candidate or dangling local package commit was found.
  Package branch heads were fetched from GitHub before reconstructing changes.

## Candidate behavior

The drift suite previously compared AMCL correction magnitude/change with
blank-map SLAM truth error. Noise and cornering cases now use the same planar
root truth error, looking up TF at the captured truth stamp. Missing stamped TF
does not fall back to latest TF. Historical correction metrics cannot establish
the required 0.05 m parity.

`slam_input_frame:=odom` replaces SLAM's scan-prior helper while retaining the
EKF and the public `map->nav_odom` correction. The fused-input default stays
unchanged. This depends on a protected slam_toolbox Jazzy API; see the
[owning rationale](../../sentry_localization/README.md#slam---use-rf2o-worse).

Saved-graph mapping now waits for the referee team and uses its configured
spawn, like saved-graph localization. The harness accepts saved graph basenames
for localization/refinement. This does not register a local MMM graph into
field coordinates or prove rasterization latency.

The new wall diagnostic separates approach, sustained pressure and retreat;
its contact gates are independent of localization error. It uses the existing
velocity-driven sim model, not a physical robot or firmware drivetrain.

## Validation

- Seed/launch tests: 25 passed on host Python 3.12.
- Package quality checks: zero new diagnostics for localization, bringup and sim;
  `actionlint -shellcheck=""` passed for each.
- Initial build stopped at sim because the existing image lacked
  `nlohmann_json`; declared sim dependencies were installed in this container.
- Runtime campaigns and final build results are pending.

## Remaining acceptance

- H-ekf: repeated, comparable truth-error trials; retune only from valid data.
- H-map: surveyed graph registration, save/load and rasterization timing.
- T3: five-minute games with spinning occluders/high ground, crossed-cell map
  inspection, and three games on a carried map. Short moving-box loops do not
  satisfy this requirement.
- H-anomalies: reproduce on the same truth metric before deciding to bisect.
- SIM-returns: no recorded robot bag was found in this child worktree. Driver
  source alone cannot distinguish missing physical returns from angular-bin
  gaps, range/material effects or motion; no arbitrary dropout model is added.
- SIM-wall: runtime results pending.

## Recovery after quota reset, 21:15 UTC

The new implementation checkout is `/Users/blaise/.t3/worktrees/src/t3-d2b524ec`,
updated to workspace nightly `53ccdb2d93598d9ca3187222d833a2d55b779dec`.
The old checkout and evidence remain unchanged. Recovered package candidates:
localization `e5a54d4`, sim `ab166d4`, bringup `46bd515`; sim was reapplied on
nightly including the merged suite naming change. The old registered result was
607 tests, zero failures/errors, **92 firmware-dependent skips**. It is neither
an integrated acceptance result nor evidence for the new changes.

Host-only work adds an AMCL `amcl_sigma_hit` trial override through bringup and
the localization harness. The default stays 0.08. The
[batch driver](../../sim/tools/run_localization_campaign.sh) plans 46 native
runs: three repeats of three scenarios for AMCL at 0.08/0.15/0.20, fused SLAM,
and raw-odom SLAM with EKF retained, plus wall impact. It stops on the first
failed native gate and preserves logs; short cases do not replace carried games.
Only plan mode has run. No new container was created while Season2 held capacity.

### Recorded returns available on the Mini

Read-only inventory found local, filtered replay copies in
`/Users/blaise/ros2_ws/robot-session-20261026/rf2o-replay/inputs/`.
The adjacent `filter_bags.py` describes copying selected topics without changing
payloads; `inventory.md` records the historical October 26 robot capture paths.
Those historical remote paths were not accessed during recovery. Local MCAP
summary counts and decoded payloads were checked afresh. The following three
files contain both raw and filtered scans; the room-04 and drive-v4 named files
contain no scans and cannot support returns analysis.

- `sentry-20261026__1__headturn-yaw.mcap`: SHA-256
  `107884fbb8e4d5e1d8ec5a390f5f45b8f1ec7b4f15d54206011966622b88cb0f`;
  1,645 raw scans over 154.751 s, median missing fraction 0.41528.
- `sentry-20261026__1c__1c-old.mcap`: SHA-256
  `a4d879f665f1a5e07dac0436bfa663cc00e36b9b0891553a76e23a116195c9fa`;
  1,119 raw scans over 103.120 s, median missing fraction 0.41667.
- `sentry-20261026__1d__1d-new.mcap`: SHA-256
  `d8e571f9f52b65488ba9b3fc23f3cdb0fa4a62ca183d643752bcdf62e1331363`;
  1,105 raw scans over 101.383 s, median missing fraction 0.41944.

All 3,869 raw scans have 720 bins. Across the three captures, 130/134/135 bins
respectively are absent in over 95% of scans; only 3.65/3.75/3.78% of missing
bins have finite immediate neighbours on both sides. Adjacent finite ranges are
exactly equal in 53.05/53.96/54.09% of finite pairs. Every missing bin has zero
intensity; no finite bin has zero intensity. Missing fractions by sensor-angle
sector are strongly nonuniform; the 0–30 degree sector is entirely missing in
all three captures. These are raw-topic measurements before the software
self-filter, not a count of newly masked beams.

The [driver compensation loop](../../sllidar_ros2/src/sllidar_node.cpp) starts
with zero-filled output bins, ignores zero-distance input samples and replicates
each accepted sample into consecutive bins. Publishing converts zero distances
to infinity. This explains why output infinity alone cannot distinguish an
unfilled angular bin from a missing physical return. Sample duplication is
consistent with the observed equal adjacent ranges. The bags do not record
pre-compensation samples, calibrated material labels or a surveyed trajectory.
No conclusion about material/range/motion causation, and no independent 40%
random-dropout model, is justified by these aggregate measurements.

The maintained [analysis script](../../sim/tools/analyze_lidar_returns.py) reproduces
these summaries. Local analysis artifacts are `.track-h-evidence/analyze_returns.py`,
`returns-summary.jsonl` and `returns-additional.jsonl` in the new checkout.
They used isolated host Python 3.12 with mcap 1.6.0,
mcap-ros2-support 0.6.0 and numpy 2.5.4. The physical-cause investigation,
angle-compensation model comparison and sim validation remain open.

### Outstanding recovery validation

Host seed tests pass 25/25; package quality/actionlint pass before the final
batch-driver addition. After the batch driver was staged, package quality/actionlint were rerun.
Updated container build, native suites, wall impact,
accuracy campaigns, sigma selection and graph deserialize/rasterization tests
remain unrun. Season2 owns scan liveness, backend readiness, moving-obstacle
clearance and foundational fixtures; merge accepted exact foundation SHAs
before campaigns. No acceptance threshold or baseline was changed.

The headturn capture's filtered `/scan` median missing fraction is 0.47500
(raw 0.41528), and 199 bins are absent in over 95% of filtered scans (raw 130).
The current self-filter sector differs from the October capture; these data
therefore cannot validate today's mount/blind-sector calibration.

### Published recovery candidates

These draft implementation heads are pushed and await runtime gates and fresh
independent review; no review or merge is claimed:

- [localization #37](https://github.com/Thornbots/sentry_localization/pull/37):
  `670a0da77a8aa09d818c397195c90734a67827db`.
- [sim #69](https://github.com/Thornbots/sim/pull/69):
  `67803b5c4fd31b8beed8ca7f464cbe07f82f0862`.
- [bringup #56](https://github.com/Thornbots/thornbots_pkg/pull/56):
  `dd4e0f5d424a440ec0870e603cab59b3a45f19a2`.

Full H/J scope remains on the roadmap. In particular, the five-minute Battle
fixture, carried-map metrics, MMM graph registration, graph round-trip and
physical-cause returns model are unfinished software/sim work.

### Head-angle control in the recorded data

The headturn file has `/joint_states`; nearest-stamp matching within 50 ms
matches all 1,645 raw scans. Recorded `headlink` spans 0.44–358.45 degrees.
The 0–30 degree **sensor** sector is missing in every matched scan across all
four head-yaw quadrants (877/261/201/306 scans respectively). Their median total
missing fractions are 0.41389/0.37222/0.43194/0.42083. This supports a
sensor/mount-fixed component rather than attributing all misses to one room
surface or head motion. It does not isolate physical blockage from acquisition
or driver behavior. Neither 1c nor 1d records joint states; no equivalent joint
matching is claimed for those files. Supporting local code/results:
`.track-h-evidence/head_returns.py`, `head-returns-summary.jsonl`.

The 1c capture's local `1/1c/mapping.log` reports Express mode, 4 kHz samples,
12 m range and configured 10 Hz frequency. The driver derives the compensation
multiplier from configured rate/frequency, not the observed header cadence.
The headturn file's scan-time p05/median/p95 is 0.08746/0.09547/0.09556 s.
A simulator that merely matches 720 output bins does not reproduce the
acquisition rate, duplicate-bin correlations or missing angular sectors.

The scored noise/cornering/degraded-scan cases now reject every missing or
nonfinite stamped-truth sample instead of omitting it from the error maximum.
This strengthens validity without changing any numerical acceptance threshold.
Compilation/runtime validation of this follow-up remains pending capacity.

A bounded local inventory also found a saved graph basename at
`/Users/blaise/ros2_ws/robot-session-20261026/next/robot/maps/room-1026-04/snapshot/map`.
The `.posegraph` is 9,761,718 bytes (SHA-256
`a0e29ef3b05349cd67cef583923684dc1929cb75072e9d5178beda708a71d2f6`);
the `.data` is 1,258,126 bytes (SHA-256
`3db636d4b42fa3ae97dc982e4ab563e76cada5c39e03058e4bccc6c83f7358d8`).
These are historical room artifacts, not a surveyed event-map acceptance
fixture. No deserialize compatibility or timing result is claimed yet.
