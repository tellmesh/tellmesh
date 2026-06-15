#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

for task in \
  examples/36_physical_ops/task.robot.yaml \
  examples/36_physical_ops/task.device.yaml
do
  python -m uri2ops.cli validate "$task"
  python -m uri2ops.cli plan "$task"
  python -m uri2ops.cli run "$task" --adapter mock --approve
done
