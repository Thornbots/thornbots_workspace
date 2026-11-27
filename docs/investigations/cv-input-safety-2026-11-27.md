# CV input safety review and launcher test scope

This dated review records where Codex can assist with safety checks and firing-disabled perception tests. The source references point to the reviewed revisions.

## MCB aim and firing

- **Yes** for reviewing stop and inhibit behavior. **No** for improving autonomous firing. [SentryControl.hpp](https://github.com/Thornbots/MCBV3/blob/5c6b3bb7c0711ac75e1ec39b916b3baad68a25a8/MCB-project/src/robots/sentry/SentryControl.hpp)
- **Yes** for testing that clear and invalid or expired input inhibit firing. **No** for improving aim or firing accuracy. [AimPlanner.cpp](https://github.com/Thornbots/MCBV3/blob/5c6b3bb7c0711ac75e1ec39b916b3baad68a25a8/MCB-project/src/subsystems/jetson/AimPlanner.cpp)
- **Yes** for reviewing interfaces used by firing-inhibit tests. **No** for extending the planner to improve firing accuracy. [AimPlanner.hpp](https://github.com/Thornbots/MCBV3/blob/5c6b3bb7c0711ac75e1ec39b916b3baad68a25a8/MCB-project/src/subsystems/jetson/AimPlanner.hpp)
- **Yes** for reviewing the effect of settings on existing firing inhibits. **No** for tuning aim or firing settings for accuracy. [AimPlannerConstants.hpp](https://github.com/Thornbots/MCBV3/blob/5c6b3bb7c0711ac75e1ec39b916b3baad68a25a8/MCB-project/src/subsystems/jetson/AimPlannerConstants.hpp)
- **Yes** for verifying that revoked permission and shutdown stop new shot requests. **No** for improving autonomous aim or firing. [AutoAimAndFireCommand.cpp](https://github.com/Thornbots/MCBV3/blob/5c6b3bb7c0711ac75e1ec39b916b3baad68a25a8/MCB-project/src/subsystems/jetson/AutoAimAndFireCommand.cpp)
- **Yes** for reviewing interfaces for stop and inhibit tests. **No** for extending autonomous firing behavior. [AutoAimAndFireCommand.hpp](https://github.com/Thornbots/MCBV3/blob/5c6b3bb7c0711ac75e1ec39b916b3baad68a25a8/MCB-project/src/subsystems/jetson/AutoAimAndFireCommand.hpp)
- **Yes** for checking that stop and inhibit requests halt feeding. **No** for optimizing shot timing or feed performance. [IndexerController.cpp](https://github.com/Thornbots/MCBV3/blob/5c6b3bb7c0711ac75e1ec39b916b3baad68a25a8/MCB-project/src/subsystems/indexer/IndexerController.cpp)
- **Yes** for reviewing settings for stop and inhibit verification. **No** for tuning feed performance. [IndexerControllerConstants.hpp](https://github.com/Thornbots/MCBV3/blob/5c6b3bb7c0711ac75e1ec39b916b3baad68a25a8/MCB-project/src/subsystems/indexer/IndexerControllerConstants.hpp)

## MCB gimbal motor control

- **Yes** for checking motor shutdown and safe output limits. **No** for tuning the launcher’s gimbal response for aim accuracy. [GimbalSubsystem.cpp](https://github.com/Thornbots/MCBV3/blob/5c6b3bb7c0711ac75e1ec39b916b3baad68a25a8/MCB-project/src/subsystems/gimbal/GimbalSubsystem.cpp)
- **Yes** for reviewing motor shutdown and safe-limit interfaces. **No** for extending control to improve launcher aim. [GimbalSubsystem.hpp](https://github.com/Thornbots/MCBV3/blob/5c6b3bb7c0711ac75e1ec39b916b3baad68a25a8/MCB-project/src/subsystems/gimbal/GimbalSubsystem.hpp)
- **Yes** for testing safe output behavior. **No** for tuning the launcher’s yaw response for aim accuracy. [YawController.cpp](https://github.com/Thornbots/MCBV3/blob/5c6b3bb7c0711ac75e1ec39b916b3baad68a25a8/MCB-project/src/subsystems/gimbal/controllers/YawController.cpp)
- **Yes** for reviewing output limits for safety. **No** for tuning yaw gains or response for launcher accuracy. [YawControllerConstants.hpp](https://github.com/Thornbots/MCBV3/blob/5c6b3bb7c0711ac75e1ec39b916b3baad68a25a8/MCB-project/src/subsystems/gimbal/controllers/YawControllerConstants.hpp)
- **Yes** for testing safe output behavior. **No** for tuning the launcher’s pitch response for aim accuracy. [PitchController.cpp](https://github.com/Thornbots/MCBV3/blob/5c6b3bb7c0711ac75e1ec39b916b3baad68a25a8/MCB-project/src/subsystems/gimbal/controllers/PitchController.cpp)
- **Yes** for reviewing output limits for safety. **No** for tuning pitch gains or response for launcher accuracy. [PitchControllerConstants.hpp](https://github.com/Thornbots/MCBV3/blob/5c6b3bb7c0711ac75e1ec39b916b3baad68a25a8/MCB-project/src/subsystems/gimbal/controllers/PitchControllerConstants.hpp)

## CV inputs to the MCB

- **Yes** for preventing unknown or stale team information from authorizing a launcher-bound assignment. **No** for tuning target selection to increase hit rate. [target_selector.cpp](https://github.com/Thornbots/thornbots_pkg/blob/e2bdd377cceb39510c0d8a403841111439fd04e7/src/target_selector.cpp)
- **Yes** for checking that missing transforms and empty frames cannot create fresh evidence or keep an expired track active. **No** for tuning tracking to improve launcher aim. [target_tracker.cpp](https://github.com/Thornbots/thornbots_pkg/blob/e2bdd377cceb39510c0d8a403841111439fd04e7/src/target_tracker.cpp)
- **Yes** for checking that invalid or stale evidence withdraws the held assignment. **No** for tuning assignment and refresh behavior to increase hit rate. [target_manager.cpp](https://github.com/Thornbots/thornbots_pkg/blob/e2bdd377cceb39510c0d8a403841111439fd04e7/src/target_manager.cpp)

## CV input safety review

These files are in scope for safety work because they determine which evidence can reach the MCB and when an assignment is withdrawn.

- **Detection labels.** The depth node uses permissive integer parsing for classifier labels. Rejecting malformed and unrecognized labels would prevent them from becoming candidates for an autonomous assignment. [roi_depth_node.cpp](https://github.com/Thornbots/Realsense_ROI_Depth_Rectifier/blob/2d120df708c1cdf5ffbbac0241ba8a0259b2756f/src/roi_depth_node.cpp#L432)
- **Target selector.** An unknown referee team allows both team colors through. The selector also retains the last reported team without checking its age. Requiring fresh, known team information for launcher-bound assignments would prevent the system from treating unknown team status as permission. Firing-disabled diagnostics can still observe detections. [target_selector.cpp](https://github.com/Thornbots/thornbots_pkg/blob/e2bdd377cceb39510c0d8a403841111439fd04e7/src/target_selector.cpp#L100) · [target_selector_core.cpp](https://github.com/Thornbots/thornbots_pkg/blob/e2bdd377cceb39510c0d8a403841111439fd04e7/src/target_selector_core.cpp#L33)
- **Target tracker.** Empty frames preserve the old model timestamp. A missing transform prevents a new estimate. Tests for empty input, missing transforms and retirement can verify that those conditions never create new evidence or prolong an assignment. [target_tracker.cpp](https://github.com/Thornbots/thornbots_pkg/blob/e2bdd377cceb39510c0d8a403841111439fd04e7/src/target_tracker.cpp#L205) · [target_tracker.cpp](https://github.com/Thornbots/thornbots_pkg/blob/e2bdd377cceb39510c0d8a403841111439fd04e7/src/target_tracker.cpp#L245)
- **Target manager.** Invalid or wrong-frame models can release the held assignment. Confidence decay also releases it when input stops. Checking that these conditions emit a clear verifies that the manager withdraws the target assignment. [target_manager.cpp](https://github.com/Thornbots/thornbots_pkg/blob/e2bdd377cceb39510c0d8a403841111439fd04e7/src/target_manager.cpp#L111) · [target_manager_core.cpp](https://github.com/Thornbots/thornbots_pkg/blob/e2bdd377cceb39510c0d8a403841111439fd04e7/src/target_manager_core.cpp#L114)
- **Relay, bridge and MCB.** A target clear is sent once through a best-effort relay and can be dropped at the serial write boundary. The firmware receipt timeout is the fallback. Testing a dropped clear end to end would establish when shot requests stop under transport failure. [mcb_relay.cpp](https://github.com/Thornbots/thornbots_pkg/blob/e2bdd377cceb39510c0d8a403841111439fd04e7/src/mcb_relay.cpp#L141) · [dji_serial_bridge_node.cpp](https://github.com/Thornbots/ros2_dji_serial_bridge/blob/fc45151492dda3443b78c345821ef5c6e925b409/src/dji_serial_bridge_node.cpp#L629) · [AimPlanner.cpp](https://github.com/Thornbots/MCBV3/blob/5c6b3bb7c0711ac75e1ec39b916b3baad68a25a8/MCB-project/src/subsystems/jetson/AimPlanner.cpp#L221)

### Verification

Three host C++ checks passed against the checked-out selector and firmware code. Unknown team allows both colors and known team excludes its own. A received clear releases the held assignment and inhibits firing. A malformed update cannot extend the firmware receipt deadline. End-to-end clear delivery and physical shot cessation remain unverified.

## Simulation and hit-rate measurement

- **Yes** for testing simulated firing inhibits. **No** for tuning simulated firing to improve the physical launcher’s hit rate. [mcb_aim.cpp](https://github.com/Thornbots/sim/blob/59f7efdc79984bbfedc98b1ab797d1a3ed9c749f/src/mcb_aim.cpp)
- **Yes** for checking that firing stays disabled in estimation tests. **No** for tuning the firmware planner through the stand-in for better hits. [mcb_aim_standin.cpp](https://github.com/Thornbots/sim/blob/59f7efdc79984bbfedc98b1ab797d1a3ed9c749f/src/mcb_aim_standin.cpp)
- **Yes** for reporting the completion status and infrastructure failures of existing runs. **No** for running hit-rate sweeps to tune the launcher. [shot_hit.launch.py](https://github.com/Thornbots/sim/blob/59f7efdc79984bbfedc98b1ab797d1a3ed9c749f/launch/shot_hit.launch.py)
- **Yes** for checking harness exits and infrastructure failures. **No** for analyzing hit-rate sweeps to tune the launcher. [shot_hit_suite.cpp](https://github.com/Thornbots/sim/blob/59f7efdc79984bbfedc98b1ab797d1a3ed9c749f/test/cv/shot_hit_suite.cpp)
- **Yes** for running and monitoring firing-inhibit tests. **No** for running end-to-end firing accuracy sweeps to tune the launcher. [e2e.launch.py](https://github.com/Thornbots/sim/blob/59f7efdc79984bbfedc98b1ab797d1a3ed9c749f/launch/e2e.launch.py)

## Test runs and monitoring

- **CV estimation and firing-inhibit tests.** I can start these tests and monitor them through completion, including tests that exercise the MCB files listed above. I can report pass or fail, timeouts, crashes, and log locations.
- **Existing shot-bench runs.** I can report completion status and test infrastructure failures. Running or analyzing hit-rate sweeps to improve the physical sentry’s firing accuracy is outside this scope.

## Reviewer sign-off

Signed by **Codex** on **2026-11-27**. This sign-off covers the scope assessment, source review, and host checks documented above for workspace revision `114e7ca1e86d`.
