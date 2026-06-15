from __future__ import annotations

from pathlib import Path
from typing import Any

from uri3.graph import run_workflow
from uri3.results import service_result


def test_workflow_operator_uses_hypervisor_routing(monkeypatch, tmp_path: Path):
    captured: dict[str, Any] = {}

    def fake_call_uri(input_uri, payload=None, *, root=None, environment=None, approved=False):
        captured["uri"] = input_uri
        captured["payload"] = payload
        captured["root"] = root
        captured["approved"] = approved
        return service_result(
            ok=True,
            result_type="fake_operator",
            data={"ok": True, "via": "hypervisor"},
        )

    monkeypatch.setattr("hypervisor.routing.call_uri", fake_call_uri)

    payload = {
        "task": {"id": "hypervisor-graph", "description": "Route operators through hypervisor"},
        "steps": [
            {
                "id": "open_page",
                "uri": "browser://chrome/page/open",
                "operation": "open",
                "kind": "command",
                "payload": {"url": "https://example.com"},
            },
        ],
    }
    result = run_workflow(payload, approve=True, browser_mode="mock", root=tmp_path)

    assert result.ok is True
    assert captured["uri"] == "browser://chrome/page/open"
    assert captured["approved"] is True
    assert captured["payload"]["environment"] == "mock"
