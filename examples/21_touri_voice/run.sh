#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
REGISTRY="$ROOT/examples/21_touri_voice"
OUT_DIR="$ROOT/output/artifacts/voice"
PROMPT="${1:-wygeneruj agenta pogodowego, uruchom go lokalnie i sprawdz health w Chrome}"

export PYTHONPATH="$REGISTRY${PYTHONPATH:+:$PYTHONPATH}"
mkdir -p "$OUT_DIR"

json_payload() {
  PAYLOAD_TEXT="$1" python - <<'PY'
import json
import os

print(json.dumps({"text": os.environ["PAYLOAD_TEXT"]}, ensure_ascii=False))
PY
}

echo "1. Mock STT"
touri call stt://mock/transcribe \
  --registry "$REGISTRY" \
  --payload "$(json_payload "$PROMPT")" \
  > "$OUT_DIR/stt_result.json"

TRANSCRIPT="$(
  python - "$OUT_DIR/stt_result.json" <<'PY'
import json
import sys

payload = json.loads(open(sys.argv[1], encoding="utf-8").read())
print(payload["data"]["text"])
PY
)"

echo "2. Voice command -> compact URI flow"
touri call voice://command/from-text \
  --registry "$REGISTRY" \
  --payload "$(json_payload "$TRANSCRIPT")" \
  > "$OUT_DIR/voice_command_result.json"

FLOW="$OUT_DIR/voice_command.uri.flow.yaml"
GRAPH="$OUT_DIR/voice_command.uri.graph.yaml"

echo "3. Expand flow -> workflow graph"
uri2flow expand "$FLOW" --out "$GRAPH"

echo "4. Validate workflow graph"
uri3 validate-workflow "$GRAPH"

echo "5. Dry-run workflow"
uri3 run-workflow "$GRAPH" --dry-run > "$OUT_DIR/voice_command.dry_run.json"

echo "6. Mock TTS"
touri call tts://mock/speak \
  --registry "$REGISTRY" \
  --payload "$(json_payload "Workflow zostal przygotowany i przeszedl walidacje.")" \
  > "$OUT_DIR/tts_result.json"

echo "Done:"
echo "  STT result:       $OUT_DIR/stt_result.json"
echo "  Voice result:     $OUT_DIR/voice_command_result.json"
echo "  Flow:             $FLOW"
echo "  Graph:            $GRAPH"
echo "  Workflow dry-run: $OUT_DIR/voice_command.dry_run.json"
echo "  TTS result:       $OUT_DIR/tts_result.json"
