#!/usr/bin/env bash
# System automations: TUI (shell://, apt) + GUI browser (browser://) + desktop (kvm://, him://, ocr://, llm://).
# Mock smoke: uri2flow validate/expand + uri3 validate + dry-run.
# Real (optional): URISYS_RUN_REAL=1 — calls urisys HTTP endpoints when Docker stacks are up.
# Voice (optional): URISYS_RUN_VOICE=1 — stt:// → voice:// → uri2flow (example 21 pattern).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
EX="$ROOT/examples/39_system_automations"
OUT="$ROOT/output/39_system_automations"
VOICE_REG="$ROOT/examples/21_touri_voice"
VOICE_OUT="$ROOT/output/artifacts/voice/system_automations"

mkdir -p "$OUT" "$VOICE_OUT"

if [[ -f "$ROOT/../resource-agent-hypervisor/scripts/examples/cli_fallback.sh" ]]; then
  # shellcheck source=/dev/null
  source "$ROOT/../resource-agent-hypervisor/scripts/examples/cli_fallback.sh"
fi

PY_BIN="${PY:-}"
if [[ -z "$PY_BIN" ]]; then
  if command -v python >/dev/null 2>&1; then
    PY_BIN="python"
  else
    PY_BIN="python3"
  fi
fi

invoke_cli() {
  if declare -F run_cli >/dev/null 2>&1; then
    run_cli "$@"
    return
  fi
  case "$1" in
    uri2flow) "$PY_BIN" -m uri2flow.cli "${@:2}" ;;
    uri3) "$PY_BIN" -m uri3.cli "${@:2}" ;;
    touri) "$PY_BIN" -m touri.cli "${@:2}" ;;
    *) "$@" ;;
  esac
}

FLOWS=(
  "$EX/01-check-env.uri.flow.yaml"
  "$EX/02-apt-update.uri.flow.yaml"
  "$EX/03-install-browser.uri.flow.yaml"
  "$EX/04-docker-stack.uri.flow.yaml"
  "$EX/05-browser-health.uri.flow.yaml"
  "$EX/06-browser-capture.uri.flow.yaml"
  "$EX/07-gui-software-center.uri.flow.yaml"
  "$EX/08-llm-guided-click.uri.flow.yaml"
  "$EX/09-rdp-session-smoke.uri.flow.yaml"
  "$EX/10-full-system-browser.uri.flow.yaml"
)

# uri3 validate/run: env + browser + http schemes. kvm/him/ocr/llm/rdp run via urisys (see README).
URI3_FLOWS=(
  "$EX/01-check-env.uri.flow.yaml"
  "$EX/05-browser-health.uri.flow.yaml"
  "$EX/06-browser-capture.uri.flow.yaml"
)

echo "== 39_system_automations: uri2flow expand (all flows) =="
for flow in "${FLOWS[@]}"; do
  base="$(basename "$flow" .uri.flow.yaml)"
  graph="$OUT/${base}.uri.graph.yaml"
  echo
  echo "=== validate: $flow ==="
  invoke_cli uri2flow validate "$flow"
  echo "=== expand: $flow ==="
  invoke_cli uri2flow expand "$flow" --out "$graph"
  echo "OK expand $base"
done

echo
echo "== uri3 validate + dry-run (browser/kvm/env/http flows) =="
for flow in "${URI3_FLOWS[@]}"; do
  base="$(basename "$flow" .uri.flow.yaml)"
  graph="$OUT/${base}.uri.graph.yaml"
  echo
  echo "=== uri3 validate: $graph ==="
  invoke_cli uri3 validate-workflow "$graph"
  echo "=== uri3 dry-run: $graph ==="
  invoke_cli uri3 run-workflow "$graph" --dry-run > "$OUT/${base}.dry_run.json"
  echo "OK uri3 $base"
done

echo
echo "== shell:// flows (uri2flow only; execute via uri2run / urish call) =="
for flow in "$EX/02-apt-update.uri.flow.yaml" "$EX/03-install-browser.uri.flow.yaml" "$EX/04-docker-stack.uri.flow.yaml" "$EX/10-full-system-browser.uri.flow.yaml"; do
  echo "  - $(basename "$flow")"
done

if [[ "${URISYS_RUN_VOICE:-0}" == "1" ]]; then
  echo
  echo "== voice pipeline (stt:// → voice:// → uri2flow) =="
  PROMPT="${URISYS_VOICE_PROMPT:-zaktualizuj system, zainstaluj Chromium i sprawdz health w Chrome}"
  json_payload() {
    PAYLOAD_TEXT="$1" "$PY_BIN" - <<'PY'
import json
import os

print(json.dumps({"text": os.environ["PAYLOAD_TEXT"]}, ensure_ascii=False))
PY
  }
  export PYTHONPATH="$VOICE_REG${PYTHONPATH:+:$PYTHONPATH}"
  invoke_cli touri call stt://mock/transcribe \
    --registry "$VOICE_REG" \
    --payload "$(json_payload "$PROMPT")" \
    > "$VOICE_OUT/stt_result.json"
  TRANSCRIPT="$(
    "$PY_BIN" - "$VOICE_OUT/stt_result.json" <<'PY'
import json
import sys

payload = json.loads(open(sys.argv[1], encoding="utf-8").read())
print(payload["data"]["text"])
PY
  )"
  invoke_cli touri call voice://command/from-text \
    --registry "$VOICE_REG" \
    --payload "$(json_payload "$TRANSCRIPT")" \
    > "$VOICE_OUT/voice_command_result.json"
  VOICE_FLOW="$VOICE_OUT/voice_command.uri.flow.yaml"
  VOICE_GRAPH="$VOICE_OUT/voice_command.uri.graph.yaml"
  invoke_cli uri2flow expand "$VOICE_FLOW" --out "$VOICE_GRAPH"
  invoke_cli uri3 validate-workflow "$VOICE_GRAPH"
  invoke_cli uri3 run-workflow "$VOICE_GRAPH" --dry-run > "$VOICE_OUT/voice_command.dry_run.json"
  echo "Voice artifacts: $VOICE_OUT"
fi

if [[ "${URISYS_RUN_REAL:-0}" == "1" ]]; then
  echo
  echo "== real urisys HTTP probes (requires Docker stacks) =="
  curl_json() {
    local uri="$1"
    local payload="${2:-{}}"
    curl -sfS -X POST "http://127.0.0.1:${3:-8792}/uri/call" \
      -H 'Content-Type: application/json' \
      -d "{\"uri\":\"${uri}\",\"payload\":${payload},\"context\":{\"allow_real\":true,\"approved\":true}}"
  }
  echo "--- urisys-rdp flow dry-run (07/08/09 patterns) ---"
  if command -v urisys-rdp >/dev/null 2>&1; then
    urisys-rdp flow "$EX/09-rdp-session-smoke.uri.flow.yaml" --dry-run --approve | head -c 600
    echo
  else
    echo "urisys-rdp not installed; skip local flow dry-run"
  fi
  echo "--- uribrowser :8792 ---"
  curl_json "browser://chrome/page/open" '{"url":"http://localhost:8101/health"}' 8792 | head -c 400
  echo
  echo "--- urikvm :8793 ---"
  curl_json "kvm://local/monitor/primary/query/screenshot" '{}' 8793 | head -c 400
  echo
  echo "--- urirdp :8795 ---"
  curl_json "kvm://local/monitor/primary/query/screenshot" '{}' 8795 | head -c 400
  echo
  echo "--- urienv :8790 ---"
  curl_json "env://runtime/var/LLM_MODEL/query/value" '{}' 8790 | head -c 400
  echo
fi

echo
echo "PASS examples/39_system_automations"
echo "Artifacts: $OUT"
