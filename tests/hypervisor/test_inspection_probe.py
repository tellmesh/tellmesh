from __future__ import annotations

import httpx
from hypervisor.deployment_registry.inspection.probe import probe_http


def test_probe_http_rewrites_localhost_when_probe_host_is_set(monkeypatch):
    captured: dict[str, object] = {}

    def fake_get(uri: str, *, timeout: float) -> httpx.Response:
        captured["uri"] = uri
        captured["timeout"] = timeout
        return httpx.Response(200, json={"ok": True, "agent": "invoices-agent"})

    monkeypatch.setenv("HYPERVISOR_PROBE_HOST", "host.docker.internal")
    monkeypatch.setattr(httpx, "get", fake_get)

    result = probe_http(
        "http://localhost:8122/health",
        timeout=1.5,
        expected_agent="invoices-agent",
    )

    assert captured == {"uri": "http://host.docker.internal:8122/health", "timeout": 1.5}
    assert result["uri"] == "http://localhost:8122/health"
    assert result["probe_uri"] == "http://host.docker.internal:8122/health"
    assert result["ok"] is True


def test_probe_http_keeps_non_localhost_targets(monkeypatch):
    captured: dict[str, object] = {}

    def fake_get(uri: str, *, timeout: float) -> httpx.Response:
        captured["uri"] = uri
        return httpx.Response(200, json={"ok": True})

    monkeypatch.setenv("HYPERVISOR_PROBE_HOST", "host.docker.internal")
    monkeypatch.setattr(httpx, "get", fake_get)

    result = probe_http("http://example.test/health", timeout=1.0)

    assert captured["uri"] == "http://example.test/health"
    assert "probe_uri" not in result
    assert result["ok"] is True


def test_probe_http_accepts_expected_service_without_agent(monkeypatch):
    def fake_get(uri: str, *, timeout: float) -> httpx.Response:
        return httpx.Response(200, json={"ok": True, "service": "uri2ops"})

    monkeypatch.setattr(httpx, "get", fake_get)

    result = probe_http(
        "http://localhost:8791/health",
        timeout=1.0,
        expected_agent="desktop-operator",
        expected_service="uri2ops",
    )

    assert result["ok"] is True
    assert result["service"] == "uri2ops"
    assert result["foreign_service"] is None


def test_probe_http_rejects_unexpected_service_without_agent(monkeypatch):
    def fake_get(uri: str, *, timeout: float) -> httpx.Response:
        return httpx.Response(200, json={"ok": True, "service": "other-service"})

    monkeypatch.setattr(httpx, "get", fake_get)

    result = probe_http(
        "http://localhost:8791/health",
        timeout=1.0,
        expected_agent="desktop-operator",
        expected_service="uri2ops",
    )

    assert result["ok"] is False
    assert result["foreign_service"] == "other-service"
