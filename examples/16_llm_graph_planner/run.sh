#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
source "$ROOT/../resource-agent-hypervisor/scripts/examples/cli_fallback.sh"
PROMPT="$(cat "$ROOT/examples/16_llm_graph_planner/prompt.txt")"
BRIDGE="$ROOT/../uri2ops/examples/16_nl2uri_operator_bridge/workflow.health.yaml"
TASK="/tmp/llm-operator-task.yaml"

echo "== rule-based graph (uri3 dry-run) =="
run_cli nl2uri graph -p "$PROMPT" --validate --dry-run

echo
echo "== import-graph -> uri2ops mock run =="
if [[ -f "$BRIDGE" ]]; then
  run_cli uri2ops import-graph "$BRIDGE" --validate --out "$TASK"
  run_cli uri2ops run "$TASK" --adapter mock --approve
else
  echo "Skipping uri2ops bridge: missing $BRIDGE"
fi

if [[ -n "${OPENROUTER_API_KEY:-}" ]]; then
  echo
  echo "== LLM graph (--llm) =="
  run_cli nl2uri graph -p "$PROMPT" --llm --validate --dry-run
  run_cli nl2uri graph -p "$PROMPT" --llm --validate > /tmp/nl2uri-llm-workflow.yaml
  run_cli uri2ops import-graph /tmp/nl2uri-llm-workflow.yaml --validate --out /tmp/nl2uri-llm-task.yaml
  run_cli uri2ops run /tmp/nl2uri-llm-task.yaml --adapter mock --approve
else
  echo
  echo "Skipping LLM demo: OPENROUTER_API_KEY is not set"
fi
