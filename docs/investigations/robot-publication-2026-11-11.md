# Robot publication validation — 2026-11-11

Live commitment: [T29](../ROADMAP.md#short-todos). No physical robot was used.

- [Nightly publication run 43133577047](https://github.com/Thornbots/thornbots_workspace/actions/runs/43133577047), source `2c48a8237d42403370b95a6d334a53a6bcb256d6`, failed after 9 min 9 s. Cache pull succeeded; native image compilation failed because `colcon` discovered the workspace `robot_localization` fork but the image selected neither that package nor the apt underlay. The offline overlay gate and image publication were skipped; no digest was produced.
- `thornbots_pkg` also depends at runtime on `thornbots_nav`, which the image, overlay and startup package lists omitted. The coordinated draft changes add it and exclude the simulation-only `robot_localization` fork from the robot build context, allowing rosdep to install the apt package.
- The first Mini emergency build was interrupted after 598.96 s when the hosted failure exposed the same build inputs; it did not reach image export or shipping. A second build with the proposed fixes is in progress. The shipping destination must be a nonrobot; laptop shipping additionally requires external nonrobot capacity and remains unvalidated.
- Host quality checks passed for the workspace, common and startup using Python 3.12 and actionlint. Common robot contract tests passed 11/11; startup Linux build and tests passed 13/13 in a task-owned container. A native macOS startup build could not compile Linux `CLOCK_BOOTTIME`.
