from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from agents.generated.runtime_routes import (
    assert_resource_allowed,
    command_uri,
    uri_allowed,
)
from fastapi import HTTPException
from hypervisor.agent_manifest.compose import materialize_compose_from_manifest
from hypervisor.agent_manifest import sync_agent_manifest


def test_uri_allowed_prefix_match():
    assert uri_allowed("resource://weather/maps/Gdansk/forecast/7", ["resource://weather/maps/{place}/forecast/{days}"])


def test_assert_resource_allowed_rejects_unknown():
    card = {
        "capabilities": [
            {"type": "resource_read", "uri": "resource://weather/maps/{place}/forecast/{days}"},
        ]
    }
    with pytest.raises(HTTPException) as exc:
        assert_resource_allowed(card, "resource://invoices/1")
    assert exc.value.status_code == 403


def test_command_uri_from_agent_card():
    card = {
        "capabilities": [
            {"type": "command", "command": "GenerateWeatherMap", "uri": "workflow://weather/generate"},
        ]
    }
    assert command_uri(card, "GenerateWeatherMap") == "workflow://weather/generate"


def test_materialize_compose_from_weather_manifest(repo_root: Path):
    sync_agent_manifest("weather-map-agent.local", root=repo_root)
    manifest = repo_root / "agents/manifests/weather-map-agent.markpact.md"
    result = materialize_compose_from_manifest(manifest, repo=repo_root)
    compose_path = repo_root / result["compose_path"]
    assert compose_path.is_file()
    doc = yaml.safe_load(compose_path.read_text(encoding="utf-8"))
    service = doc["services"]["weather-map-agent"]
    assert service["build"]["dockerfile"] == "agents/generated/weather_map_agent/Dockerfile"
    assert "8102:8102" in service["ports"]
