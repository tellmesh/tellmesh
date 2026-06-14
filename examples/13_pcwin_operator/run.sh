#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
TASK="examples/13_pcwin_operator/task.pcwin.yaml"
python -m uri2ops.cli validate "$TASK"
python -m uri2ops.cli plan "$TASK"
python -m uri2ops.cli run "$TASK" --adapter mock --approve
