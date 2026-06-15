# AUTO-GENERATED FILE. DO NOT EDIT.
# Source: contracts/agents/weather_map_agent.yaml
# Contract hash: sha256:47b69e7e4fc1b3b3e56e5778021526be07db596966aac1362c0782a766ca2485

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
        "agent": "weather-map-agent",
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


@router.get("/skills/read_weather_map")
def skill_read_weather_map(place: str, days: str) -> dict[str, Any]:
    uri = "resource://weather/maps/{place}/forecast/{days}"
    uri = uri.replace("{place}", place)
    uri = uri.replace("{days}", days)
    return read_uri(client, uri)

@router.post("/skills/generate_weather_map")
def skill_generate_weather_map(payload: dict[str, Any]) -> dict[str, Any]:
    return dispatch_command(
        client,
        "GenerateWeatherMap",
        payload,
        uri=None,
    )
