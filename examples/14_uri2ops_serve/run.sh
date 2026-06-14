#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
python -m uri2ops.cli registry validate
python - <<'PY'
from pathlib import Path

import yaml
from fastapi.testclient import TestClient

from uri2ops.server.app import create_app

task = yaml.safe_load(Path("examples/10_browser_operator/task.health.yaml").read_text(encoding="utf-8"))
client = TestClient(create_app(root=Path.cwd(), base_url="http://testserver"))
print(client.get("/health").json())
print("tools", len(client.get("/mcp/tools").json()["tools"]))
result = client.post("/a2a/tasks", json={"task": task, "approve": True, "adapter": "mock"})
print("a2a ok", result.json()["workflow_result"]["ok"])
PY
