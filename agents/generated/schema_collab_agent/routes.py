# AUTO-GENERATED FILE. DO NOT EDIT.
# Source: contracts/agents/schema_collab_agent.yaml
# Contract hash: sha256:17b3d806a8ebef60fa04b5234c2f32ccc2b94d7745234e05cbbd5c7e51bb4bd3

from __future__ import annotations

import os
from typing import Any

from fastapi import APIRouter, Query
from agents.generated.runtime_routes import (
    CommandRequest,
    assert_command_allowed,
    assert_resource_allowed,
    command_uri,
    dispatch_command,
    read_uri,
)
from runtime_client.client import ResourceRuntimeClient

from .agent_card import AGENT_CARD

router = APIRouter()

RUNTIME_URL = os.getenv("RESOURCE_RUNTIME_URL", "http://localhost:8000")
client = ResourceRuntimeClient(base_url=RUNTIME_URL)


@router.get("/health")
def health() -> dict[str, Any]:
    return {
        "ok": True,
        "agent": "schema-collab-agent",
        "version": "0.1.0",
        "runtime_url": RUNTIME_URL,
    }


@router.get("/capabilities")
def capabilities() -> dict[str, Any]:
    return {"capabilities": AGENT_CARD["capabilities"]}


@router.get("/.well-known/agent.json")
def well_known_agent_json() -> dict[str, Any]:
    return AGENT_CARD


@router.get("/.well-known/agent-card.json")
def well_known_agent_card_json() -> dict[str, Any]:
    return AGENT_CARD


@router.get("/resources/read")
def read_resource(uri: str = Query(...)) -> dict[str, Any]:
    assert_resource_allowed(AGENT_CARD, uri)
    return read_uri(client, uri)


@router.post("/commands")
def dispatch_command_route(request: CommandRequest) -> dict[str, Any]:
    assert_command_allowed(AGENT_CARD, request.command)
    return dispatch_command(
        client,
        request.command,
        request.payload,
        uri=command_uri(AGENT_CARD, request.command),
    )


@router.get("/skills/read_markpact_source")
def skill_read_markpact_source() -> dict[str, Any]:
    uri = "file://agents/generated/schema_collab_agent/README.md"
    return read_uri(client, uri)
@router.get("/skills/read_device_status")
def skill_read_device_status() -> dict[str, Any]:
    uri = "device://device/sensor-1/status"
    return read_uri(client, uri)
@router.get("/skills/read_robot_state")
def skill_read_robot_state() -> dict[str, Any]:
    uri = "robot://robot/amr-1/state"
    return read_uri(client, uri)

@router.post("/skills/run_cron_monitor")
def skill_run_cron_monitor(payload: dict[str, Any]) -> dict[str, Any]:
    return dispatch_command(
        client,
        "RunCronMonitor",
        payload,
        uri="cron://www/monitor/landing",
    )
