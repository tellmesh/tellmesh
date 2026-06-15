"""Tests for evolutionary repair supervisor."""

from __future__ import annotations

from pathlib import Path

import pytest
from hypervisor.repair.classifier import classify_inspection
from hypervisor.deployment_registry.loader import load_deployment_registry
from hypervisor.repair.incident import build_incident_from_inspection, load_incident, write_incident
from hypervisor.repair.registry import find_matching_case
from hypervisor.repair.validator import validate_incident_dict


def test_classify_port_and_health_timeout():
    inspection = {
        "incidents": [
            {"code": "COMMAND_HEALTH_MISMATCH", "detail": "uvicorn port differs"},
            {"code": "PROCESS_RUNNING_BUT_UNHEALTHY", "detail": "health check failed"},
        ],
        "health": {"error": "connection refused"},
    }
    result = classify_inspection(inspection)
    assert "PORT_CONFLICT" in result["family"]
    assert "HEALTH_TIMEOUT" in result["family"]
    assert "sync_health_uri" in result["safe_repairs"]


def test_incident_artifact_has_schema_and_uri(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "schemas").mkdir()
    schema_src = Path(__file__).resolve().parents[2] / "schemas" / "incident.schema.json"
    (tmp_path / "schemas" / "incident.schema.json").write_text(
        schema_src.read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    inspection = {
        "id": "weather-map-agent.local",
        "agent_ref": "agent://weather-map-agent",
        "ok": False,
        "runtime_status": "running",
        "process": {"pid": 1, "running": True},
        "health": {"ok": False, "uri": "http://localhost:40061/health"},
        "readiness": {
            "process": "running",
            "health": "failed",
            "effective_port": 40061,
            "declared_health_uri": "http://localhost:8101/health",
            "effective_health_uri": "http://localhost:40061/health",
        },
        "incidents": [{"code": "PROCESS_RUNNING_BUT_UNHEALTHY", "detail": "health failed"}],
        "log_uri": "log://hypervisor?grep=weather-map-agent.local",
        "log_errors": {"error_count": 0, "entries": []},
        "runtime_state": {
            "command": "uvicorn --port 40061",
            "health_uri": "http://localhost:8101/health",
        },
    }
    incident = build_incident_from_inspection(
        inspection,
        classification={"family": ["PORT_CONFLICT", "HEALTH_TIMEOUT"], "confidence": 0.8},
    )
    path = write_incident(incident, repo_root=tmp_path)
    payload = load_incident(path, repo_root=tmp_path)
    assert payload["kind"] == "Incident"
    assert payload["uri"]["self"].startswith("incident://agent/")
    assert payload["$schema"] == "schemas/incident.schema.json"
    errors = validate_incident_dict(payload, tmp_path)
    assert not errors


def test_find_known_repair_case():
    classification = {"family": ["PORT_CONFLICT", "HEALTH_TIMEOUT"]}
    inspection = {
        "readiness": {"process": "running", "health": "failed", "effective_port": 40061},
    }
    case = find_matching_case(classification, inspection)
    assert case is not None
    assert "sync_health_uri" in case.get("repair_sequence", [])


def test_repair_apply_syncs_registry_when_healthy_but_drifted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    registry_path = tmp_path / "deployments" / "agent_deployments.yaml"
    registry_path.parent.mkdir(parents=True)
    registry_path.write_text(
        """
deployments:
  - id: weather-map-agent.local-dev
    agent_ref: agent://weather-map-agent
    target_uri: local://agents/generated/weather_map_agent
    status: generated
    health_uri: http://localhost:8101/health
    card_uri: http://localhost:8101/.well-known/agent-card.json
""".strip()
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    healthy = {
        "ok": True,
        "id": "weather-map-agent.local-dev",
        "declared_health_uri": "http://localhost:8101/health",
        "effective_health_uri": "http://localhost:8105/health",
    }

    from hypervisor.repair import supervisor as repair_supervisor

    monkeypatch.setattr(repair_supervisor, "diagnose_agent", lambda *args, **kwargs: {"inspection": healthy})
    result = repair_supervisor.repair_apply("weather-map-agent.local-dev", approved=True, root=tmp_path)
    assert result["ok"] is True
    assert result["registry_sync"]["ok"] is True
    assert result["registry_sync"]["port"] == 8105

    registry = load_deployment_registry(tmp_path)
    deployment = registry.by_id("weather-map-agent.local-dev")
    assert deployment is not None
    assert deployment.health_uri == "http://localhost:8105/health"


def test_repair_apply_emits_operation_event_for_healthy_agent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    from hypervisor.repair import supervisor as repair_supervisor

    emitted: list[dict[str, object]] = []
    healthy = {
        "ok": True,
        "id": "demo-agent.local",
        "declared_health_uri": "http://localhost:8123/health",
        "effective_health_uri": "http://localhost:8123/health",
    }

    monkeypatch.setattr(
        repair_supervisor,
        "diagnose_agent",
        lambda *args, **kwargs: {"inspection": healthy},
    )

    def fake_emit(operation, selector, result, **kwargs):
        emitted.append(
            {
                "operation": operation,
                "selector": selector,
                "code": kwargs.get("success_code"),
                "ok": result.get("ok"),
            }
        )

    monkeypatch.setattr(repair_supervisor, "emit_result_event", fake_emit)

    result = repair_supervisor.repair_apply("demo-agent.local", root=tmp_path)

    assert result["ok"] is True
    assert emitted == [
        {
            "operation": "repair-apply",
            "selector": "demo-agent.local",
            "code": "REPAIR_APPLY_SKIPPED_HEALTHY",
            "ok": True,
        }
    ]
