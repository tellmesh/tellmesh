"""Tests for port conflict classification via socket and /proc probes."""

from __future__ import annotations

from unittest.mock import patch

from hypervisor.deployment_registry.port_conflict import (
    classify_port_listeners,
    port_conflict_detail,
)


def test_classify_port_listeners_marks_foreign_process():
    plan = {"module": "agents.generated.user_agent.main:app", "path": "/app/agents"}
    with patch(
        "hypervisor.deployment_registry.port_conflict.is_port_free",
        return_value=False,
    ), patch(
        "hypervisor.deployment_registry.port_conflict.pids_listening_on_port",
        return_value={111, 222},
    ), patch(
        "hypervisor.deployment_registry.port_conflict.command_line",
        side_effect=["uvicorn agents.generated.user_agent.main:app", "python -m http.server"],
    ), patch(
        "hypervisor.deployment_registry.port_conflict.command_matches_plan",
        side_effect=[True, False],
    ):
        probe = classify_port_listeners(8102, plan=plan)

    assert probe["occupied"] is True
    assert probe["conflict"] is True
    assert len(probe["foreign_listeners"]) == 1
    assert probe["foreign_listeners"][0]["pid"] == 222


def test_port_conflict_detail_includes_probe_payload():
    health = {"ok": False, "foreign_service": "other-agent"}
    with patch(
        "hypervisor.deployment_registry.port_conflict.classify_port_listeners",
        return_value={
            "port": 8102,
            "free": False,
            "occupied": True,
            "listeners": [{"pid": 9, "command": "other", "owned_by_agent": False}],
            "foreign_listeners": [{"pid": 9, "command": "other", "owned_by_agent": False}],
            "conflict": True,
        },
    ), patch(
        "hypervisor.deployment_registry.port_utils.health_matches_agent",
        return_value=False,
    ):
        incident = port_conflict_detail(
            port=8102,
            health=health,
            expected_agent="user-agent",
        )

    assert incident is not None
    assert incident["code"] == "PORT_OCCUPIED"
    assert incident["port_probe"]["conflict"] is True


def test_port_conflict_detail_ignores_owned_listener():
    health = {"ok": True, "service": "uri2ops"}
    with patch(
        "hypervisor.deployment_registry.port_conflict.classify_port_listeners",
        return_value={
            "port": 8791,
            "free": False,
            "occupied": True,
            "listeners": [{"pid": 9, "command": "uvicorn uri2ops.main:app", "owned_by_agent": True}],
            "foreign_listeners": [],
            "conflict": False,
        },
    ):
        incident = port_conflict_detail(
            port=8791,
            health=health,
            expected_agent="desktop-operator",
        )

    assert incident is None
