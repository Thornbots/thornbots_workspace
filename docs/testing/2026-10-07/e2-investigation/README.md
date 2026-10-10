# E2 investigation

The Archlinux failure is intermittent, not a consistent UART encoding or
native-build failure. A 20-second stationary repeat hit 40/40 on each
machine. Earlier Archlinux runs hit 0/20 or lost the track and fired no shots.
Those failures remain valid; a passing repeat does not resolve them.

The original failing Archlinux run's median aim error was 0.669 m and barrel
error was 2.695 degrees. The Mac baseline's median aim error was 0.004 m.
On a later passing Archlinux run the aim error was 0.005 m, with head-TF
error 0.132 degrees and localization error 0.221 m (medians). The tracker
repeatedly rejected stationary measurements during the failing run.

Changes on nightly:

- Test-owned stacks start the opponent parked before requesting a cell.
  This removes machine-dependent unscored motion, but did not eliminate
  acquisition failures; one parked-start confirmation still fired no shots.
- Bring-up requires a fresh aim, rather than an aim received at any earlier time.
- The requested real-time factor now reaches the test-owned stack. Previously
  the launch argument was ignored when the suite created its child stack.
- The E2E watchdog detects five wall seconds without clock progress, backward
  clock motion and a total budget. The old three-times-duration cap falsely
  labeled a progressing RTF-0.3 run stalled. Three regression tests cover it.
- `states.jsonl`, `poses.jsonl` and shot records expose stamped tracker,
  head-TF and localization errors, including periods without shots. Missing
  stamped TF is unavailable; a latest transform is never substituted.

Validation: Mac unthrottled 40/40 in 20 sim seconds; Archlinux unthrottled
40/40 in 20 sim seconds; Mac RTF-1 control passes. The repaired Archlinux
RTF-0.3 control completes its entire 10-second window and passes. Mac's
full sim unit suite passes: 72 Python cases and 8 gtest cases, 9.47 s.
Archlinux's full unit suite passes in 31.8 s; colcon reports 83 tests,
zero errors and zero failures. Package commit: sim `bdda911`.

A live discovery check found no Mac ROS nodes on idle Archlinux while the
Mac stack ran, so cross-machine ROS interference was not established.
The slow Archlinux control used ROS domain 87 and `GZ_IP=127.0.0.1`.
No firmware changes, score floors, skips or xfail were used to obtain passes.
Remaining work is acquisition/tracking repeatability and moving E2 accuracy.
