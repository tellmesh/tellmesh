"""Tests for continuous hypervisor supervision."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from hypervisor.deployment_registry.watch import WATCH_LOG_RELATIVE, supervise_watch


def _read_watch_events(root: Path) -> list[dict[str, Any]]:
    path = root / WATCH_LOG_RELATIVE
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def _healthy() -> dict[str, Any]:
    return {
        "ok": True,
        "id": "demo-agent.local",
        "status": "healthy",
        "after": {"ok": True, "service_status": "healthy", "incidents": []},
        "actions": [],
    }


def _failed(code: str = "HEALTH_FAILED") -> dict[str, Any]:
    return {
        "ok": False,
        "id": "demo-agent.local",
        "status": "blocked",
        "after": {
            "ok": False,
            "service_status": "stopped",
            "incidents": [{"code": code, "detail": "probe failed"}],
        },
        "actions": [],
    }


def test_supervise_watch_emits_health_change_only_on_signature_change(
    tmp_path: Path,
    monkeypatch,
):
    results = [_healthy(), _healthy(), _failed()]

    def fake_supervise(*args, **kwargs):
        return results.pop(0)

    monkeypatch.setattr("hypervisor.deployment_registry.watch.supervise_agent", fake_supervise)

    summary = supervise_watch(
        "demo-agent.local",
        root=tmp_path,
        repair="none",
        interval=0,
        count=3,
    )

    events = _read_watch_events(tmp_path)
    codes = [event["event"]["code"] for event in events]
    assert summary["tick_count"] == 3
    assert codes == ["AGENT_HEALTH_CHANGED", "AGENT_HEALTH_CHANGED"]
    assert events[-1]["level"] == "WARNING"


def test_supervise_watch_applies_repair_backoff_for_repeated_failure(
    tmp_path: Path,
    monkeypatch,
):
    repairs: list[str] = []

    def fake_supervise(*args, **kwargs):
        repairs.append(kwargs["repair"])
        return _failed()

    monkeypatch.setattr("hypervisor.deployment_registry.watch.supervise_agent", fake_supervise)

    supervise_watch(
        "demo-agent.local",
        root=tmp_path,
        repair="auto",
        interval=0,
        count=3,
        repair_backoff_ticks=2,
    )

    assert repairs == ["auto", "none", "auto"]


def test_supervise_watch_creates_one_incident_during_backoff(
    tmp_path: Path,
    monkeypatch,
    ):
    repair_calls: list[str] = []
    inspect_repairs: list[str] = []

    def fake_supervise_with_repair(*args, **kwargs):
        repair_calls.append(kwargs["repair"])
        return {
            **_failed(),
            "incident_uri": "incident://agent/demo-agent.local/inc_1",
            "incident_path": str(tmp_path / "output/incidents/inc_1.yaml"),
            "heal_attempt": {
                "actions": [
                    {"strategy": "restart", "result": {"ok": False}},
                ]
            },
        }

    def fake_supervise(*args, **kwargs):
        inspect_repairs.append(kwargs["repair"])
        return _failed()

    monkeypatch.setattr(
        "hypervisor.repair.supervisor.supervise_with_repair",
        fake_supervise_with_repair,
    )
    monkeypatch.setattr("hypervisor.deployment_registry.watch.supervise_agent", fake_supervise)

    supervise_watch(
        "demo-agent.local",
        root=tmp_path,
        repair="auto",
        interval=0,
        count=4,
        learn=True,
        repair_backoff_ticks=1,
    )

    events = _read_watch_events(tmp_path)
    codes = [event["event"]["code"] for event in events]
    assert repair_calls == ["auto"]
    assert inspect_repairs == ["auto", "auto", "auto"]
    assert codes.count("INCIDENT_CREATED") == 1
    assert codes.count("REPAIR_STARTED") == 1
    assert codes.count("REPAIR_FAILED") == 1
