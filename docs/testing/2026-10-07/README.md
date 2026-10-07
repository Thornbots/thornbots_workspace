# E1–E4 nightly validation, 2026-10-07

All changes were committed and pushed on `nightly`, with package commits
pushed before workspace gitlink bumps. Archlinux used an isolated checkout
under `e2e-validation`; its original `rep-105` checkout was left alone.

| Test | Result |
| --- | --- |
| Mac E1, stationary and speed-2, three paths | 6/6 passed, 65.88 s |
| Mac E2, stationary lateral, 10 sim seconds | 20/20 native MCB shots hit, 22.81 s |
| Archlinux E1, same six cells | 6/6 passed, 137.44 s; moving hit rates 20–27% |
| Archlinux E2, stationary lateral, 10 sim seconds | Failed: 0/20 MCB shots hit, 50.44 s |
| Mac E3, spawn-to-center | Diagnostic pass, 37.93 s; 0/33 shots hit |
| Mac E4, latest 2v2 match | Diagnostic pass, 59.44 s; 0/36 MCB shots hit, zero ally intersections |
| Archlinux E4, 2v2 match | Diagnostic pass, 86.04 s; 0/35 MCB shots hit, zero ally intersections |
| Mac sim unit tests | 69 Python cases and 8 gtest cases passed, 9.47 s |
| Archlinux sim unit tests, after correction | Passed, 32.1 s; colcon reports 80 tests, zero failures |

E3/E4 diagnostic passes mean routes completed with stamped localization
data and a measured explanation for low hit rates. They are **not combat
accuracy passes**. Latest E4 route p95 was at most 0.100 m, with 604 referee
UART frames. Each ghost fired 37 times; one red robot lost 20 HP. The test
checks our HP and team return through the compiled MCB's real UART path.
Archlinux's E4 route p95 stayed below 0.096 m and received 360 referee frames.

An earlier E4 run failed the strict zero-ally-intersection assertion: one
parked-segment shot hit the ally hull. It caused no damage, but still counts
as a friendly intersection. Its barrel was 10.27 degrees off the aim, head
TF error was 4.54 degrees, and localization error was 0.514 m. Both that
report and the offending shot are archived; the assertion remains strict.

The ROS convention defect was world-frame linear twist in `Odometry` whose
child frame was the body. Publishers now send child-frame twist, and parent
frame consumers rotate it. Startup localization now initializes AMCL/EKF at
the field spawn, preventing a false firmware relocalization to the origin.

Remaining work: moving localization/head-TF/tracking accuracy, intermittent
friendly intersections, Archlinux's E2 accuracy failure, repeated-run floors,
standalone-versus-sequence equivalence, and hit-angle referee verification.
See `sim/README.md` for model limits and runnable container commands.

Archlinux's first unit run found D213 errors in two final docstring edits.
The correction is in sim `33645a9`; both full unit suites pass after it.
