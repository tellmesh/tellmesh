"""Tests for planned URI execution with auto-repair."""

from __future__ import annotations

from typing import Any

import pytest

from hypervisor_dashboard_agent.plan_runner import (
    PlanRunOptions,
    agent_id_from_uri,
    format_plan_run_markdown,
    run_planned_uris,
)


@pytest.mark.parametrize(
    ("uri", "agent_id"),
    [
        ("health://agent/demo.local", "demo.local"),
        ("repair://agent/demo.local/auto", "demo.local"),
        ("view://process/agent/demo.local/latest", "demo.local"),
        ("runtime://agent/demo.local/status", "demo.local"),
        ("domain://demo", None),
    ],
)
def test_agent_id_from_uri(uri: str, agent_id: str | None):
    assert agent_id_from_uri(uri) == agent_id


def test_run_planned_uris_success(monkeypatch: pytest.MonkeyPatch):
    calls: list[str] = []

    def fake_call(uri: str, **kwargs: Any) -> dict[str, Any]:
        calls.append(uri)
        return {"ok": True, "uri": uri, "result_type": "health"}

    monkeypatch.setattr(
        "hypervisor_dashboard_agent.plan_runner.call_system_uri",
        fake_call,
    )

    payload = run_planned_uris(
        PlanRunOptions(
            planned_uris=["health://agent/demo.local"],
            dry_run=True,
            auto_repair=False,
        )
    )

    assert payload["ok"] is True
    assert payload["count"] == 1
    assert calls == ["health://agent/demo.local"]
    assert "ok" in payload["message_markdown"]


def test_run_planned_uris_auto_repair_and_retry(monkeypatch: pytest.MonkeyPatch):
    uri = "health://agent/demo.local"
    attempts: list[str] = []

    def fake_call(call_uri: str, **kwargs: Any) -> dict[str, Any]:
        attempts.append(call_uri)
        if call_uri.startswith("repair://"):
            return {"ok": True, "uri": call_uri, "result_type": "repair"}
        if call_uri == uri and attempts.count(uri) == 1:
            return {"ok": False, "uri": call_uri, "result_type": "error", "error": "down"}
        return {"ok": True, "uri": call_uri, "result_type": "health"}

    monkeypatch.setattr(
        "hypervisor_dashboard_agent.plan_runner.call_system_uri",
        fake_call,
    )

    payload = run_planned_uris(
        PlanRunOptions(
            planned_uris=[uri],
            approved=True,
            dry_run=False,
            auto_repair=True,
            retry_after_repair=True,
        )
    )

    assert payload["ok"] is True
    assert attempts == [uri, "repair://agent/demo.local/auto", uri]
    step = payload["results"][0]
    assert step["ok"] is True
    assert step["auto_repair"]["ok"] is True
    assert step["retry"]["ok"] is True
    assert len(payload["repairs"]) == 1


def test_run_planned_uris_skips_repair_for_non_agent_uri(monkeypatch: pytest.MonkeyPatch):
    def fake_call(uri: str, **kwargs: Any) -> dict[str, Any]:
        return {"ok": False, "uri": uri, "error": "failed"}

    monkeypatch.setattr(
        "hypervisor_dashboard_agent.plan_runner.call_system_uri",
        fake_call,
    )

    payload = run_planned_uris(
        PlanRunOptions(planned_uris=["domain://demo"], auto_repair=True),
    )

    assert payload["ok"] is False
    assert payload["repairs"] == []
    assert "auto_repair" not in payload["results"][0]


def test_format_plan_run_markdown_includes_repair_lines():
    md = format_plan_run_markdown(
        [
            {
                "uri": "health://agent/demo.local",
                "ok": True,
                "auto_repair": {
                    "ok": True,
                    "repair_for_agent": "demo.local",
                },
                "retry": {"ok": True},
            }
        ],
        repairs=[{"ok": True}],
    )
    assert "auto-repair" in md
    assert "retry" in md
    assert "Auto-repair attempts: 1" in md
