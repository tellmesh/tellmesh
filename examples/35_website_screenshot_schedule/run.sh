#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
source "$ROOT/scripts/examples/cli_fallback.sh"
GRAPH="examples/35_website_screenshot_schedule/task_graph.yaml"
REGISTRY="examples/20_touri_capabilities"

echo "=== validate graph (relative) ==="
run_cli uri3 validate-workflow "$GRAPH"

echo
echo "=== validate graph via file:// (demonstrates native file:// URI support) ==="
FILE_GRAPH="file://$(pwd)/$GRAPH"
run_cli uri3 validate-workflow "$FILE_GRAPH"

echo
echo "Tip: In another terminal, watch logs live with log:// while running the workflow:"
echo '  urish watch '\''log://hypervisor?grep=website-screenshot-schedule|browser|screen'\'' --interval 1'
echo '  # or for file log: urish watch '\''log://file/output/logs/hypervisor.log?grep=screenshot'\'' --interval 2'

echo
echo "=== touri dry-run ==="
run_cli touri call workflow://graph/website-screenshot-schedule/dry-run --registry "$REGISTRY"

echo
echo "=== uri run dry-run ==="
run_cli uri run workflow://graph/website-screenshot-schedule/dry-run --dry-run

echo
echo "=== uri run approve (mock) ==="
run_cli uri run workflow://graph/website-screenshot-schedule --approve --adapter mock

echo
echo "Done."
