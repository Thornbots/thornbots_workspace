#!/usr/bin/env bash
# Run host helpers without ROS, CUDA hardware, or a service/container launch.
set -euo pipefail
cd "$1"
case "$2" in
  startup)
    cmake -S . -B build/host-tests -DBUILD_TESTING=ON -DCMAKE_BUILD_TYPE=Release
    cmake --build build/host-tests --parallel 2
    ctest --test-dir build/host-tests --output-on-failure --no-tests=error \
      --output-junit results.xml
    ;;
  common)
    mkdir -p build/host-tests
    PYTHONPATH=isaac_common_py python -m pytest isaac_common_py/tests tests -q \
      --junitxml=build/host-tests/results.xml
    ;;
  *) echo "Unknown host test suite: $2" >&2; exit 1 ;;
esac
