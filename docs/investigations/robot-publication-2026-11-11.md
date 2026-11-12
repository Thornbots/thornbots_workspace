# Robot publication validation — 2026-11-11

Live commitment: [T29](../ROADMAP.md#short-todos). No physical robot was used.

- [Nightly publication run 43133577047](https://github.com/Thornbots/thornbots_workspace/actions/runs/43133577047), source `2c48a8237d42403370b95a6d334a53a6bcb256d6`, failed after 9 min 9 s. Cache pull succeeded; native image compilation failed because `colcon` discovered the workspace `robot_localization` fork but the image selected neither that package nor the apt underlay. The offline overlay gate and image publication were skipped; no digest was produced.
- `thornbots_pkg` also depends at runtime on `thornbots_nav`, which the image, overlay and startup package lists omitted. The coordinated draft changes add it and exclude the simulation-only `robot_localization` fork from the robot build context, allowing rosdep to install the apt package.
- The first Mini emergency build was interrupted after 598.96 s when the hosted failure exposed the same build inputs; it did not reach image export or shipping. A second build with the proposed fixes passed in 1,243.31 s (42 layers); its local image ID was `sha256:7041876b84a8c455ecd4979672f72847fe43f7ec3e1e1d61a7d9547c7e85b8fc`. The shipping destination must be a nonrobot; laptop shipping additionally requires external nonrobot capacity and remains unvalidated.
- Host quality checks passed for the workspace, common and startup using Python 3.12 and actionlint. Common robot contract tests passed 11/11; startup Linux build and tests passed 13/13 in a task-owned container. A native macOS startup build could not compile Linux `CLOCK_BOOTTIME`.

## Corrected publication run

[Run 43135391848](https://github.com/Thornbots/thornbots_workspace/actions/runs/43135391848)
passed on draft source `146d8dd68f2478b6d84a2a19f78e7a0904fab3b9` in 20 min 22 s.
The image build took 7 min 11 s; baked package tests reported 615 tests, zero
errors or failures and 22 skipped. The offline gate took 3 min 47 s and printed
`Robot image dependency contract matches checkout.`, then built all eight packages
and reported `Offline overlay ready for sha256:54a79c5d6cb66b7ea74797d646806c5a74c761eff921a971c5d1fede1e6da9e6.`
That ID is the runner's local image ID, not the registry manifest digest.

The immutable `ghcr.io/thornbots/isaac-ros:sha-146d8dd68f2478b6d84a2a19f78e7a0904fab3b9-arm64-jetpack`
and `t3-t29-publication-validation-arm64-jetpack` tags were published with
manifest digest `sha256:d2a640eb5b655835bc8f80fda1cb32a2d59422362e2c3efd6fcf8d0b49ad30ea`;
the push took 5 min 32 s. This validates the draft's exact gitlinks, not an
integrated nightly publication. The task-owned Mini container and volumes were
removed; Colima remained running for another agent container.
