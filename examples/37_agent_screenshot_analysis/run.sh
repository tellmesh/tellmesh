#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
source "$ROOT/../resource-agent-hypervisor/scripts/examples/cli_fallback.sh"
if [[ -x "$ROOT/.venv/bin/python3" ]]; then
  export PY="$ROOT/.venv/bin/python3"
elif [[ -x "$ROOT/.venv/bin/python" ]]; then
  export PY="$ROOT/.venv/bin/python"
fi

echo "== 37_agent_screenshot_analysis =="
ADAPTER="${ADAPTER:-mock}"

run_cli hypervisor run-agent browser-operator.local --detach --wait-healthy --if-running restart
run_cli hypervisor run-agent screenshot-analysis-agent.local --detach --wait-healthy --if-running reuse

echo "== schema discovery =="
run_cli uri call schema://agent/browser-operator.local --json >/tmp/taskinity-browser-schema.json
run_cli uri call schema://agent/screenshot-analysis-agent.local --json >/tmp/taskinity-screenshot-analysis-schema.json
python3 - <<'PY'
import json
from pathlib import Path

for name in ("browser", "screenshot-analysis"):
    path = Path(f"/tmp/taskinity-{name}-schema.json")
    data = json.loads(path.read_text())
    payload = data.get("data") if isinstance(data.get("data"), dict) else data
    print(name, payload.get("agent_id"), [c.get("name") for c in payload.get("capabilities", [])][:6])
PY

BROWSER_URL="$(python3 - <<'PY'
import json
data = json.load(open("/tmp/taskinity-browser-schema.json"))
payload = data.get("data") if isinstance(data.get("data"), dict) else data
print(str(payload["card_uri"]).rsplit("/.well-known/", 1)[0])
PY
)"
ANALYZER_URL="$(python3 - <<'PY'
import json
data = json.load(open("/tmp/taskinity-screenshot-analysis-schema.json"))
payload = data.get("data") if isinstance(data.get("data"), dict) else data
print(str(payload["card_uri"]).rsplit("/.well-known/", 1)[0])
PY
)"
echo "browser_url=$BROWSER_URL"
echo "analyzer_url=$ANALYZER_URL"
echo "adapter=$ADAPTER"

echo "== capture/analyze tick 1 =="
curl -s -X POST "$ANALYZER_URL/skills/capture_and_analyze" \
  -H 'Content-Type: application/json' \
  -d "{\"operator_url\":\"$BROWSER_URL\",\"target_url\":\"http://localhost:8788/www/\",\"adapter\":\"$ADAPTER\",\"approve\":true,\"run_label\":\"example37\"}" \
  >/tmp/taskinity-screenshot-analysis-1.json

echo "== capture/analyze tick 2 =="
curl -s -X POST "$ANALYZER_URL/skills/capture_and_analyze" \
  -H 'Content-Type: application/json' \
  -d "{\"operator_url\":\"$BROWSER_URL\",\"target_url\":\"http://localhost:8788/www/\",\"adapter\":\"$ADAPTER\",\"approve\":true,\"run_label\":\"example37\"}" \
  >/tmp/taskinity-screenshot-analysis-2.json

python3 - <<'PY'
import json
from pathlib import Path

for idx in (1, 2):
    data = json.loads(Path(f"/tmp/taskinity-screenshot-analysis-{idx}.json").read_text())
    if not data.get("ok"):
        raise SystemExit(json.dumps(data, indent=2, ensure_ascii=False))
    analysis = data["analysis"]
    print(
        f"tick {idx}: ok={data['ok']} artifact={data['artifact_uri']} "
        f"media={analysis['media_type']} changed={analysis['changed_from_previous']}"
    )

jsonl = Path("output/analysis/screenshots/screenshot-analysis.jsonl")
md = Path("output/analysis/screenshots/screenshot-analysis.md")
assert jsonl.exists(), jsonl
assert md.exists(), md
print(f"analysis_jsonl={jsonl}")
print(f"analysis_markdown={md}")
PY

echo "schedule_uri=cron://screenshots/capture-analysis/every-5-min"
echo "PASS examples/37_agent_screenshot_analysis"
