#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
source "$ROOT/../resource-agent-hypervisor/scripts/examples/cli_fallback.sh"
run_cli hypervisor deployments | grep -q weather-map-agent
run_cli hypervisor run-agent weather-map-agent.local --dry-run | grep -q uvicorn
