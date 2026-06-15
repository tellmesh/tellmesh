"""Unit checks for the dynamic real-browser example runner."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "examples" / "effective_weather_playwright.py"
SPEC = importlib.util.spec_from_file_location("effective_weather_playwright", SCRIPT)
assert SPEC is not None
runner = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(runner)


def test_flow_text_with_screenshot_is_valid_compact_flow():
    payload = yaml.safe_load(
        runner._flow_text(
            "weather-agent-effective-health-screenshot",
            "http://localhost:8118/health",
            include_screenshot=True,
        )
    )

    assert payload["flow"]["id"] == "weather-agent-effective-health-screenshot"
    assert payload["do"][0]["with"]["url"] == "http://localhost:8118/health"
    assert payload["do"][2]["uri"] == "screen://browser/active/screenshot"
    assert payload["do"][2]["operation"] == "capture"


def test_artifact_uri_maps_to_workflow_output_path():
    path = runner._artifact_to_path(
        "artifact://workflow/demo-flow/run-123/screenshot/screenshot.png"
    )

    expected = runner.ROOT / "output/artifacts/workflows"
    expected = expected / "demo-flow/run-123/screenshot/screenshot.png"
    assert path == expected
