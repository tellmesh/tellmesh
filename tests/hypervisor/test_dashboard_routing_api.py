from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient
from hypervisor_dashboard_agent.main import app
from hypervisor_dashboard_agent.uri_client import call_system_uri, explain_system_uri
from uri3.results import service_result


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_explain_system_uri_includes_hypervisor_resolution(repo_root: Path):
    result = explain_system_uri(
        "browser://chrome/page/open",
        root=repo_root,
        payload={"url": "https://example.com", "environment": "mock"},
    )

    assert result["ok"] is True
    assert result["canonical_uri"] == "tellmesh://operators/browser/command/open"
    assert result["explain"]["matched_registry"] == "uri2ops"
    assert result["hypervisor_resolution"]["agent_uri"] == "agent://browser-operator"
    assert result["hypervisor_resolution"]["environment_uri"] == "environment://mock"


def test_api_uri_explain_operator_route(client: TestClient):
    response = client.post(
        "/api/uri/explain",
        json={
            "uri": "browser://chrome/page/open",
            "payload": {"url": "https://example.com", "environment": "mock"},
            "policy": "dev",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["result_type"] == "explain"
    assert payload["canonical_uri"] == "tellmesh://operators/browser/command/open"
    assert payload["preview"]["requires_approval"] is True
    assert payload["hypervisor_resolution"]["runtime"]["type"] == "uri2ops"


def test_call_system_uri_operator_uses_hypervisor_dispatch(monkeypatch, repo_root: Path):
    captured: dict[str, Any] = {}

    def fake_run_backend(backend, payload, context):
        captured["backend"] = backend
        captured["payload"] = payload
        captured["context"] = context
        return service_result(ok=True, result_type="fake_operator", data={"ok": True})

    monkeypatch.setattr("uri2run.run_backend", fake_run_backend)

    result = call_system_uri(
        "browser://chrome/page/open",
        root=repo_root,
        approved=True,
        payload={"url": "https://example.com", "environment": "mock"},
    )

    assert result["ok"] is True
    assert captured["backend"]["type"] == "uri2ops"
    assert captured["backend"]["canonical_uri"] == "tellmesh://operators/browser/command/open"
    assert captured["context"]["agent_uri"] == "agent://browser-operator"
