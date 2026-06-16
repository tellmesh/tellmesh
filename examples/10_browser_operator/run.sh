#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
source "$ROOT/../resource-agent-hypervisor/scripts/examples/cli_fallback.sh"

TASK="examples/10_browser_operator/task.health.yaml"
run_cli uri2ops validate "$TASK"
run_cli uri2ops plan "$TASK"
run_cli uri2ops run "$TASK" --adapter mock --approve
