"""Tests for deployment registry port sync and run dependency checks."""

from __future__ import annotations

from pathlib import Path

import pytest

from hypervisor.deployment_registry.loader import load_deployment_registry
from hypervisor.deployment_registry.registry_sync import sync_deployment_port
import sys

from hypervisor.deployment_registry.run_executor import validate_run_dependencies


def test_validate_run_dependencies_detects_missing_uvicorn():
    plan = {
        "command": [
            sys.executable,
            "-m",
            "uvicorn",
            "agents.generated.invoices_agent.main:app",
            "--port",
            "8110",
        ]
    }
    message = validate_run_dependencies(plan)
    if message is None:
        pytest.skip("uvicorn is installed in this environment")
    assert "uvicorn" in message.lower()


def test_sync_deployment_port_updates_registry(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    registry_path = tmp_path / "deployments" / "agent_deployments.yaml"
    registry_path.parent.mkdir(parents=True)
    registry_path.write_text(
        """
deployments:
  - id: invoices-agent.local
    agent_ref: agent://invoices-agent
    target_uri: local://agents/generated/invoices_agent
    status: generated
    declared:
      target_uri: local://agents/generated/invoices_agent
      preferred_port: 8103
      health_uri: http://localhost:8103/health
      card_uri: http://localhost:8103/.well-known/agent-card.json
    health_uri: http://localhost:8103/health
    card_uri: http://localhost:8103/.well-known/agent-card.json
""".strip(),
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "hypervisor.deployment_registry.registry_sync.load_deployment_registry",
        lambda root, path=None: load_deployment_registry(tmp_path, path=registry_path),
    )
    monkeypatch.setattr(
        "hypervisor.deployment_registry.registry_sync.save_deployment_registry",
        lambda registry: registry.path.write_text(
            __import__("yaml").safe_dump(
                {"deployments": [item.to_dict() for item in registry.deployments]},
                sort_keys=False,
            ),
            encoding="utf-8",
        )
        or registry.path,
    )

    result = sync_deployment_port("invoices-agent.local", 8110, root=tmp_path)
    assert result["ok"] is True
    assert result["health_uri"] == "http://localhost:8110/health"

    updated = load_deployment_registry(tmp_path, path=registry_path).by_id("invoices-agent.local")
    assert updated is not None
    assert updated.health_uri == "http://localhost:8110/health"
    assert updated.declared and updated.declared.preferred_port == 8110
