from __future__ import annotations

from pathlib import Path

import pytest
from hypervisor.agent_manifest import (
    materialize_agent_manifest,
    sync_agent_manifest,
    sync_all_agent_manifests,
)
from uri2pact import extract_markpact_blocks


def test_sync_weather_map_agent_manifest(repo_root: Path):
    result = sync_agent_manifest("weather-map-agent.local", root=repo_root)
    path = repo_root / result["manifest_path"]
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "```markpact:agent weather-map-agent" in text
    assert "```markpact:deployment weather-map-agent.local" in text
    assert "```markpact:runtime weather-map-agent.local" in text
    assert "generate_weather_map" in text
    assert result["contract_path"] == "contracts/agents/weather_map_agent.yaml"


def test_sync_screenshot_custom_agent_manifest(repo_root: Path):
    result = sync_agent_manifest("screenshot-analysis-agent.local", root=repo_root)
    path = repo_root / result["manifest_path"]
    text = path.read_text(encoding="utf-8")
    blocks = extract_markpact_blocks(text, "agent")
    assert blocks
    body = blocks[0]["body"]
    assert "implementation: custom" in body
    assert "agents/custom/screenshot_analysis_agent" in body


def test_materialize_manifest_roundtrip(repo_root: Path):
    sync_agent_manifest("invoices-agent.local", root=repo_root)
    path = repo_root / "agents/manifests/invoices-agent.markpact.md"
    parsed = materialize_agent_manifest(path, repo=repo_root)
    assert parsed["ok"] is True
    assert parsed["agent_ref"] == "agent://invoices-agent"
    assert parsed["implementation"] == "generated"
    assert "agent" in parsed["blocks"]
    assert "deployment" in parsed["blocks"]


def test_sync_all_agent_manifests(repo_root: Path):
    result = sync_all_agent_manifests(root=repo_root)
    assert result["ok"] is True
    assert result["count"] >= 10
    manifest_dir = repo_root / "agents/manifests"
    assert (manifest_dir / "weather-map-agent.markpact.md").is_file()
    assert (manifest_dir / "browser-operator.markpact.md").is_file() or any(
        p.name.endswith(".markpact.md") for p in manifest_dir.glob("browser*.markpact.md")
    )


def test_manifest_has_docker_block_for_weather(repo_root: Path):
    sync_agent_manifest("weather-map-agent.local", root=repo_root)
    text = (repo_root / "agents/manifests/weather-map-agent.markpact.md").read_text()
    blocks = extract_markpact_blocks(text, "docker")
    assert blocks
    assert "8102:8102" in blocks[0]["body"]

