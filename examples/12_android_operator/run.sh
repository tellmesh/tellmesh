#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
TASK="examples/12_android_operator/task.android.yaml"
python -m uri2ops.cli validate "$TASK"
python -m uri2ops.cli plan "$TASK"
python -m uri2ops.cli run "$TASK" --adapter mock --approve
