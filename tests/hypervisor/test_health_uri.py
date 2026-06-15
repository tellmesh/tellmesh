"""Tests for runtime health URI resolution."""

from __future__ import annotations

from hypervisor.deployment_registry.health_uri import (
    command_port_from_runtime,
    resolve_effective_health_uri,
)


def test_resolve_effective_health_uri_prefers_network_effective_uri():
    state = {
        "network": {
            "effective_health_uri": "http://localhost:8105/health",
            "declared_health_uri": "http://localhost:8101/health",
        },
        "health_uri": "http://localhost:8101/health",
    }
    plan = {"health_uri": "http://localhost:8101/health"}
    assert resolve_effective_health_uri(state, plan) == "http://localhost:8105/health"


def test_resolve_effective_health_uri_uses_process_command():
    state = {
        "process": {
            "command": "/usr/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8105",
        },
        "health_uri": "http://localhost:8101/health",
    }
    plan = {"health_uri": "http://localhost:8101/health"}
    assert resolve_effective_health_uri(state, plan) == "http://localhost:8105/health"


def test_command_port_from_runtime_uses_network_effective_port():
    state = {
        "network": {"effective_port": 8105},
        "health_uri": "http://localhost:8101/health",
    }
    plan = {"health_uri": "http://localhost:8101/health"}
    assert command_port_from_runtime(state, plan) == 8105
