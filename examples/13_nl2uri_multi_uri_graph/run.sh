#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

PROMPT="$(cat examples/13_nl2uri_multi_uri_graph/prompt.txt)"

echo "=== classify ==="
nl2uri classify -p "$PROMPT"

echo
echo "=== single ==="
nl2uri single -p "pokaż status agenta pogodowego"

echo
echo "=== list ==="
nl2uri list -p "sprawdź health agenta pogodowego i pokaż jego agent card"

echo
echo "=== tree ==="
nl2uri tree -p "wygeneruj domenę weather map z agentem" --json | head -n 20

echo
echo "=== task ==="
nl2uri task -p "otwórz Chrome i sprawdź localhost:8101/health" --validate --dry-run > examples/13_nl2uri_multi_uri_graph/task_plan.yaml

echo
echo "=== graph ==="
nl2uri graph -p "$PROMPT" --validate > examples/13_nl2uri_multi_uri_graph/workflow_graph.yaml

echo
echo "=== uri3 validate-workflow ==="
uri3 validate-workflow examples/13_nl2uri_multi_uri_graph/workflow_graph.yaml

echo
echo "=== uri3 plan-workflow ==="
uri3 plan-workflow examples/13_nl2uri_multi_uri_graph/workflow_graph.yaml | head -n 30

echo
echo "Done."
