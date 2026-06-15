from __future__ import annotations

from pathlib import Path

import pytest
from hypervisor.routing.system_dispatch import (
    call_hypervisor_system_uri,
    supports_hypervisor_system_uri,
)
from hypervisor.routing.view_handlers import supports_view_uri
from hypervisor_dashboard_agent.uri_client import call_system_uri


def test_supports_hypervisor_system_uri():
    assert supports_hypervisor_system_uri("health://agent/demo.local")
    assert supports_hypervisor_system_uri("repair://agent/demo.local/diagnose")
    assert not supports_hypervisor_system_uri("view://process/agent/demo.local/latest")
    assert not supports_hypervisor_system_uri("browser://chrome/page/open")


def test_supports_view_uri():
    assert supports_view_uri("view://process/agent/demo.local/latest")
    assert supports_view_uri("resource://dashboard/process/agent/demo.local/latest")
    assert not supports_view_uri("browser://chrome/page/open")


def test_call_hypervisor_system_uri_health_dry_run(repo_root: Path):
    result = call_hypervisor_system_uri(
        "health://agent/user-agent.local",
        root=repo_root,
        dry_run=True,
    )

    assert result["result_type"] == "health"
    assert "agent_id" in result


def test_call_system_uri_delegates_health_to_hypervisor_routing(repo_root: Path):
    result = call_system_uri("health://agent/user-agent.local", root=repo_root, dry_run=True)

    assert result["result_type"] == "health"
    assert result.get("agent_id") == "user-agent.local"


def test_call_system_uri_repair_diagnose_via_hypervisor(repo_root: Path):
    result = call_system_uri("repair://agent/user-agent.local/diagnose", root=repo_root)

    assert result["result_type"] == "diagnosis"


def test_call_system_uri_view_uses_hypervisor_view_handlers(monkeypatch: pytest.MonkeyPatch, repo_root: Path):
    monkeypatch.setattr(
        "hypervisor.routing.view_handlers.resolve_view_envelope",
        lambda view_uri, root=None, renderer=None: type(
            "Envelope",
            (),
            {
                "to_dict": lambda self: {
                    "view_uri": view_uri,
                    "content_type": "text/html",
                    "title": "Demo",
                    "html": "<p>ok</p>",
                }
            },
        )(),
    )

    result = call_system_uri("view://process/agent/demo.local/latest", root=repo_root)

    assert result["ok"] is True
    assert result["content_type"] == "text/html"
