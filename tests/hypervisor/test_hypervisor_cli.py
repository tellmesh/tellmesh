"""Hypervisor CLI tests."""

from __future__ import annotations

import json

from hypervisor.cli import main
from uri3.results import service_result


def test_cli_deployments_and_run_agent_dry_run(capsys):
    rc = main(["deployments"])
    assert rc == 0
    deployments = json.loads(capsys.readouterr().out)
    assert any(item["id"] == "weather-map-agent.local" for item in deployments)

    rc = main(["run-agent", "weather-map-agent.local", "--dry-run"])
    assert rc == 0
    plan = json.loads(capsys.readouterr().out)
    assert plan["module"] == "agents.generated.weather_map_agent.main:app"
    assert isinstance(plan["port"], int)
    assert plan["port"] > 0
    assert plan["health_uri"] == f"http://localhost:{plan['port']}/health"
    assert plan["env"]["RESOURCE_RUNTIME_URL"] == "http://localhost:8000"


def test_cli_ssh_run_agent_dry_run(capsys):
    rc = main(["run-agent", "weather-map-agent.ssh-dev", "--dry-run"])
    assert rc == 0
    plan = json.loads(capsys.readouterr().out)
    assert plan["transport"] == "ssh"
    assert "remote_command" in plan


def test_cli_deploy_agent_dry_run(capsys):
    rc = main(["deploy-agent", "weather-map-agent.ssh-dev"])
    assert rc == 0
    plan = json.loads(capsys.readouterr().out)
    assert plan["steps"][0]["action"] == "rsync"


def test_cli_agent_status_includes_runtime_fields(capsys):
    rc = main(["agent-status", "weather-map-agent.local", "--no-health"])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["runtime_status"] in {"stopped", "running", "stale"}
    assert "env" in payload


def test_cli_run_agent_dry_run_accepts_if_running(capsys):
    rc = main(["run-agent", "weather-map-agent.local", "--dry-run", "--if-running", "reuse"])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["module"] == "agents.generated.weather_map_agent.main:app"


def test_cli_run_agent_dry_run_emits_operation_event(monkeypatch, capsys):
    emitted: list[dict[str, object]] = []

    def fake_emit(code, message, **kwargs):
        emitted.append({"code": code, "message": message, **kwargs})

    monkeypatch.setattr("hypervisor.events.emit_operation_event", fake_emit)

    rc = main(["run-agent", "weather-map-agent.local", "--dry-run"])

    assert rc == 0
    json.loads(capsys.readouterr().out)
    assert emitted
    assert emitted[0]["code"] == "AGENT_RUN_PLANNED"
    assert emitted[0]["selector"] == "weather-map-agent.local"


def test_cli_run_agent_accepts_approve_compatibility_flag(capsys):
    rc = main(["run-agent", "desktop-operator.local", "--dry-run", "--approve"])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["module"] == "agents.operators.desktop_operator.main:app"
    assert payload["port"] == 8791


def test_cli_explain_operator_route(capsys):
    rc = main(["explain", "browser://chrome/page/open"])

    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["canonical_uri"] == "tellmesh://operators/browser/command/open"
    assert payload["hypervisor_resolution"]["agent_uri"] == "agent://browser-operator"
    assert payload["hypervisor_resolution"]["runtime"]["type"] == "uri2ops"


def test_cli_call_operator_route_uses_hypervisor_dispatch(monkeypatch, capsys):
    captured: dict[str, object] = {}

    def fake_run_backend(backend, payload, context):
        captured["backend"] = backend
        captured["payload"] = payload
        captured["context"] = context
        return service_result(ok=True, result_type="fake_operator", data={"ok": True})

    monkeypatch.setattr("uri2run.run_backend", fake_run_backend)

    rc = main(
        [
            "call",
            "browser://chrome/page/open",
            "--payload",
            '{"url":"https://example.com","environment":"mock"}',
            "--approve",
        ]
    )

    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["ok"] is True
    assert captured["backend"]["canonical_uri"] == "tellmesh://operators/browser/command/open"
    assert captured["backend"]["type"] == "uri2ops"


def test_cli_inspect_agent(monkeypatch, capsys):
    monkeypatch.setattr(
        "hypervisor.cli.inspect_agent",
        lambda selector, timeout=2.0, log_limit=20: {
            "ok": True,
            "id": selector,
            "service_status": "healthy",
        },
    )
    rc = main(["inspect-agent", "weather-map-agent.local"])
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["service_status"] == "healthy"


def test_cli_supervise_watch_limited(monkeypatch, capsys):
    ticks = [
        {"ok": False, "service_status": "degraded"},
        {"ok": True, "service_status": "healthy"},
    ]

    def fake_watch(selector, **kwargs):
        on_tick = kwargs.get("on_tick")
        emitted = []
        for index, item in enumerate(ticks, start=1):
            tick = {"tick": index, "ok": item["ok"], "status": item["service_status"]}
            emitted.append(tick)
            if on_tick:
                on_tick(tick)
        return {
            "ok": True,
            "result_type": "watch",
            "selector": selector,
            "watch": True,
            "tick_count": len(emitted),
            "log_path": "output/logs/hypervisor-watch.jsonl",
            "state_path": "output/runtime/watch/demo.json",
        }

    monkeypatch.setattr("hypervisor.cli.supervise_watch", fake_watch)
    rc = main(
        [
            "supervise",
            "weather-map-agent.local",
            "--watch",
            "--count",
            "2",
            "--interval",
            "0",
            "--repair",
            "auto",
        ]
    )
    assert rc == 0
    captured = capsys.readouterr().out.strip()
    lines = captured.splitlines()
    assert lines[0].startswith('{"tick": 1')
    assert lines[1].startswith('{"tick": 2')
    summary = json.loads("\n".join(lines[2:]))
    assert summary["watch"] is True
    assert summary["tick_count"] == 2


def test_cli_repair_heal(monkeypatch, capsys):
    monkeypatch.setattr(
        "hypervisor.repair.healer.run_uri_healer",
        lambda selector, **kwargs: {
            "ok": False,
            "healer": True,
            "result_type": "healer",
            "incident_uri": "incident://agent/demo/x",
        },
    )
    rc = main(["repair", "heal", "weather-map-agent.local"])
    assert rc == 1
    payload = json.loads(capsys.readouterr().out)
    assert payload["healer"] is True
