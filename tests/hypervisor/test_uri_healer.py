"""Tests for uri-healer wrapper."""

from __future__ import annotations

from hypervisor.repair.healer import run_uri_healer


def test_run_uri_healer_delegates_to_supervise_with_repair(monkeypatch):
    captured: dict = {}

    def fake_supervise(*args, **kwargs):
        captured.update(kwargs)
        return {"ok": False, "phase": "learn", "incident_uri": "incident://agent/demo/x"}

    monkeypatch.setattr("hypervisor.repair.healer.supervise_with_repair", fake_supervise)

    payload = run_uri_healer("demo-agent.local", learn=True, max_attempts=2)

    assert payload["healer"] is True
    assert payload["result_type"] == "healer"
    assert captured["learn"] is True
    assert captured["max_attempts"] == 2
