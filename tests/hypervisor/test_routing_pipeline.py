from __future__ import annotations

from pathlib import Path
from typing import Any

from hypervisor.routing import call_uri, resolve_hypervisor_route
from hypervisor.uri.client import Uri3Client
from uri3.results import service_result


def test_hypervisor_resolves_canonical_route_to_operator_runtime(repo_root: Path):
    resolution = resolve_hypervisor_route(
        "browser://chrome/page/open",
        payload={"url": "https://example.com", "environment": "mock"},
        root=repo_root,
        approved=True,
    )

    assert resolution.route.canonical_uri == "tellmesh://operators/browser/command/open"
    assert resolution.agent_uri == "agent://browser-operator"
    assert resolution.deployment_id == "browser-operator.local"
    assert resolution.environment_uri == "environment://mock"
    assert resolution.policy_uri == "policy://operators/browser/open"
    assert resolution.runtime["type"] == "uri2ops"
    assert resolution.runtime["scheme"] == "browser"
    assert resolution.runtime["operation"] == "open"


def test_hypervisor_treats_playwright_as_adapter_not_environment(repo_root: Path):
    resolution = resolve_hypervisor_route(
        "browser://chrome/page/open",
        payload={"url": "https://example.com", "environment": "playwright"},
        root=repo_root,
        approved=True,
    )

    assert resolution.environment_uri == "environment://local"
    assert resolution.runtime["environment"] == "local"
    assert resolution.runtime["adapter"] == "playwright"
    assert resolution.context["adapter"] == "playwright"


def test_hypervisor_blocks_side_effecting_route_without_approval(repo_root: Path):
    result = call_uri(
        "browser://chrome/page/open",
        payload={"url": "https://example.com", "environment": "mock"},
        root=repo_root,
        approved=False,
    ).to_dict()

    assert result["ok"] is False
    assert result["result_type"] == "policy_decision"
    assert result["data"]["canonical_uri"] == "tellmesh://operators/browser/command/open"
    assert result["errors"][0]["code"] == "ROUTE_REQUIRES_APPROVAL"


def test_hypervisor_dispatches_approved_route_through_uri2run(monkeypatch, repo_root: Path):
    captured: dict[str, Any] = {}

    def fake_run_backend(backend, payload, context):
        captured["backend"] = backend
        captured["payload"] = payload
        captured["context"] = context
        return service_result(ok=True, result_type="fake", data={"executed": True})

    monkeypatch.setattr("uri2run.run_backend", fake_run_backend)

    result = call_uri(
        "browser://chrome/page/open",
        payload={"url": "https://example.com", "environment": "mock"},
        root=repo_root,
        approved=True,
    ).to_dict()

    assert result["ok"] is True
    assert captured["backend"]["type"] == "uri2ops"
    assert captured["backend"]["environment"] == "mock"
    assert captured["context"]["canonical_uri"] == "tellmesh://operators/browser/command/open"


def test_uri3_client_operator_call_uses_hypervisor_routing(monkeypatch):
    captured: dict[str, Any] = {}

    def fake_run_backend(backend, payload, context):
        captured["backend"] = backend
        captured["payload"] = payload
        captured["context"] = context
        return service_result(ok=True, result_type="fake", data={"executed": True})

    monkeypatch.setattr("uri2run.run_backend", fake_run_backend)

    result = Uri3Client().call(
        "browser://chrome/page/open",
        {"url": "https://example.com", "environment": "mock"},
        approved=True,
    )

    assert result["ok"] is True
    assert captured["backend"]["type"] == "uri2ops"
    assert captured["backend"]["canonical_uri"] == "tellmesh://operators/browser/command/open"
