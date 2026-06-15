"""urish call routing through hypervisor executive layer for operators."""

from __future__ import annotations

from typing import Any

from urish.backends.call import _is_operator_uri, call_uri
from uri3.results import service_result


def test_operator_uri_uses_hypervisor_routing(monkeypatch, repo_root):
    captured: dict[str, Any] = {}

    def fake_run_backend(backend, payload, context):
        captured["backend"] = backend
        captured["payload"] = payload
        captured["context"] = context
        return service_result(ok=True, result_type="fake_operator", data={"executed": True})

    monkeypatch.setattr("uri2run.run_backend", fake_run_backend)

    from urish.policy import PolicyOptions

    result = call_uri(
        "browser://chrome/page/open",
        {"url": "https://example.com", "environment": "mock"},
        policy_options=PolicyOptions.from_flags(approve=True, policy="dev"),
    )

    assert result["ok"] is True
    assert result["meta"]["transport"] == "hypervisor.routing"
    assert captured["backend"]["type"] == "uri2ops"
    assert captured["backend"]["canonical_uri"] == "tellmesh://operators/browser/command/open"
    assert captured["context"]["agent_uri"] == "agent://browser-operator"


def test_operator_uri_dry_run_returns_plan_with_resolution(repo_root):
    from urish.policy import PolicyOptions

    result = call_uri(
        "browser://chrome/page/open",
        {"url": "https://example.com", "environment": "mock"},
        dry_run=True,
        policy_options=PolicyOptions.from_flags(policy="dev"),
    )

    assert result["ok"] is True
    assert result["result_type"] == "plan"
    assert result["data"]["canonical_uri"] == "tellmesh://operators/browser/command/open"
    assert result["data"]["hypervisor_resolution"]["agent_uri"] == "agent://browser-operator"


def test_operator_schemes_detected():
    assert _is_operator_uri("browser://chrome/page/open")
    assert _is_operator_uri("robot://robot/amr-1/state")
    assert not _is_operator_uri("health://agent/demo.local")
