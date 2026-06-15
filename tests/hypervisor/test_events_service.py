"""Tests for dashboard event feed."""

from __future__ import annotations

from pathlib import Path

import yaml
from hypervisor.deployment_registry.watch import WATCH_LOG_RELATIVE
from hypervisor_dashboard_agent.events_service import collect_system_events
from uri3.logs.writer import append_log


def test_collect_system_events_includes_log_event(tmp_path: Path, monkeypatch):
    logs_dir = tmp_path / "output" / "logs" / "agents"
    logs_dir.mkdir(parents=True)
    log_line = (
        '{"kind":"LogEvent","level":"ERROR","timestamp":"2026-06-14T13:00:00Z",'
        '"message":"agent crashed","event":{"code":"AGENT_CRASH","message":"agent crashed"},'
        '"uri":{"self":"log://hypervisor?grep=demo-agent.local"}}'
    )
    (logs_dir / "demo-agent.local.jsonl").write_text(log_line + "\n", encoding="utf-8")

    monkeypatch.setattr(
        "hypervisor_dashboard_agent.events_service.list_agent_deployments",
        lambda **kwargs: [],
    )
    events = collect_system_events(root=tmp_path, limit=10)
    log_events = [event for event in events if event["type"] == "log.event"]
    assert log_events
    assert log_events[0]["level"] == "ERROR"
    assert "agent crashed" in log_events[0]["summary"]


def test_collect_system_events_includes_hypervisor_operation_events(
    tmp_path: Path,
    monkeypatch,
):
    append_log(
        "hypervisor-events",
        "demo-agent.local run-agent completed",
        level="INFO",
        logger="hypervisor.events",
        root=tmp_path,
        subject_uri="health://agent/demo-agent.local",
        event_code="AGENT_RUN_COMPLETED",
        operation="run-agent",
    )

    monkeypatch.setattr(
        "hypervisor_dashboard_agent.events_service.list_agent_deployments",
        lambda **kwargs: [],
    )
    events = collect_system_events(root=tmp_path, limit=10)

    log_events = [event for event in events if event["type"] == "log.event"]
    assert log_events
    assert log_events[0]["agent_id"] == "demo-agent.local"
    assert "run-agent completed" in log_events[0]["summary"]


def test_collect_system_events_prefers_latest_log_lines(tmp_path: Path, monkeypatch):
    log_path = tmp_path / "output" / "logs" / "hypervisor-events.jsonl"
    log_path.parent.mkdir(parents=True)
    lines = []
    for index in range(6):
        code = f"EVENT_{index}"
        lines.append(
            (
                '{"kind":"LogEvent","level":"INFO",'
                f'"timestamp":"2026-06-14T13:00:0{index}Z",'
                f'"message":"message {index}",'
                f'"event":{{"code":"{code}","message":"message {index}"}},'
                '"uri":{"self":"log://hypervisor-events",'
                '"subject":"health://agent/demo-agent.local"}}'
            )
        )
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    monkeypatch.setattr(
        "hypervisor_dashboard_agent.events_service.list_agent_deployments",
        lambda **kwargs: [],
    )
    events = collect_system_events(root=tmp_path, limit=2)

    summaries = [event["summary"] for event in events]
    assert any("message 5" in item for item in summaries)


def test_collect_system_events_includes_supervise_watch_log_event(
    tmp_path: Path,
    monkeypatch,
):
    log_path = tmp_path / WATCH_LOG_RELATIVE
    log_path.parent.mkdir(parents=True)
    log_path.write_text(
        (
            '{"kind":"LogEvent","level":"WARNING","timestamp":"2026-06-14T13:00:00Z",'
            '"message":"demo-agent.local health changed to stopped",'
            '"event":{"code":"AGENT_HEALTH_CHANGED","message":"health changed"},'
            '"uri":{"self":"log://file/output/logs/hypervisor-watch.jsonl",'
            '"subject":"health://agent/demo-agent.local"}}'
        )
        + "\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(
        "hypervisor_dashboard_agent.events_service.list_agent_deployments",
        lambda **kwargs: [],
    )
    events = collect_system_events(root=tmp_path, limit=10)

    log_events = [event for event in events if event["type"] == "log.event"]
    assert log_events
    assert log_events[0]["level"] == "WARNING"
    assert "health changed" in log_events[0]["summary"]


def test_collect_system_events_includes_watch_log_with_agent_id(tmp_path: Path, monkeypatch):
    logs_dir = tmp_path / "output" / "logs"
    logs_dir.mkdir(parents=True)
    log_line = (
        '{"kind":"LogEvent","level":"WARNING","timestamp":"2026-06-15T08:00:00Z",'
        '"message":"weather-map-agent.local health changed to degraded",'
        '"uri":{"self":"log://file/output/logs/hypervisor-watch.jsonl",'
        '"subject":"health://agent/weather-map-agent.local"},'
        '"event":{"code":"AGENT_HEALTH_CHANGED","message":"health changed"}}'
    )
    (logs_dir / "hypervisor-watch.jsonl").write_text(log_line + "\n", encoding="utf-8")

    monkeypatch.setattr(
        "hypervisor_dashboard_agent.events_service.list_agent_deployments",
        lambda **kwargs: [],
    )
    events = collect_system_events(root=tmp_path, limit=10)
    log_events = [event for event in events if event["type"] == "log.event"]
    assert log_events
    assert log_events[0]["agent_id"] == "weather-map-agent.local"
    assert "degraded" in log_events[0]["summary"]


def test_collect_system_events_includes_incident(tmp_path: Path, monkeypatch):
    day = "2026-06-14"
    agent_dir = tmp_path / "output" / "incidents" / day / "demo-agent.local"
    agent_dir.mkdir(parents=True)
    incident = {
        "metadata": {
            "id": "inc_test",
            "agent_id": "demo-agent.local",
            "created_at": "2026-06-14T12:00:00Z",
        },
        "uri": {"self": "incident://agent/demo-agent.local/inc_test"},
        "symptoms": [{"code": "HEALTH_FAILED", "message": "health probe failed"}],
    }
    (agent_dir / "inc_test.yaml").write_text(yaml.dump(incident), encoding="utf-8")

    monkeypatch.setattr(
        "hypervisor_dashboard_agent.events_service.list_agent_deployments",
        lambda **kwargs: [],
    )
    events = collect_system_events(root=tmp_path, limit=10)
    types = {event["type"] for event in events}
    assert "incident.created" in types


def test_collect_system_events_treats_http_healthy_unmanaged_agent_as_healthy(
    tmp_path: Path,
    monkeypatch,
):
    monkeypatch.setattr(
        "hypervisor_dashboard_agent.events_service.list_agent_deployments",
        lambda **kwargs: [
            {
                "id": "dashboard.local",
                "health_uri": "http://localhost:8788/health",
                "view_uri": "view://process/agent/dashboard.local/latest",
            }
        ],
    )
    monkeypatch.setattr(
        "hypervisor_dashboard_agent.events_service.inspect_agent",
        lambda *args, **kwargs: {
            "ok": False,
            "service_status": "stopped",
            "health": {"ok": True},
            "incidents": [],
        },
    )

    events = collect_system_events(root=tmp_path, limit=10)

    assert events[0]["type"] == "agent.health"
    assert events[0]["ok"] is True
    assert events[0]["summary"] == "healthy"
