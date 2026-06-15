# AUTO-GENERATED FILE. DO NOT EDIT.
# Source: contracts/agents/user_agent.yaml
# Contract hash: sha256:740801960691f1c4aefee04d0cc5a7e27aa3a9915ef2eb73a729f9226a10ce45

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
        "agent": "user-agent",
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


@router.get("/skills/read_user")
def skill_read_user(user_id: str) -> dict[str, Any]:
    uri = "resource://users/{user_id}"
    uri = uri.replace("{user_id}", user_id)
    return read_uri(client, uri)
@router.get("/skills/read_user_roles")
def skill_read_user_roles(user_id: str) -> dict[str, Any]:
    uri = "resource://users/{user_id}/roles"
    uri = uri.replace("{user_id}", user_id)
    return read_uri(client, uri)

@router.post("/skills/create_user")
def skill_create_user(payload: dict[str, Any]) -> dict[str, Any]:
    return dispatch_command(
        client,
        "CreateUser",
        payload,
        uri=None,
    )
@router.post("/skills/assign_user_role")
def skill_assign_user_role(payload: dict[str, Any]) -> dict[str, Any]:
    return dispatch_command(
        client,
        "AssignUserRole",
        payload,
        uri=None,
    )
