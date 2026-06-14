"""Tests for touri uri_flow and uri_graph backends."""

from __future__ import annotations

from pathlib import Path

from touri.executor import call_uri


def test_uri_flow_backend_dry_run(repo_root: Path):
    registry = repo_root / "examples" / "20_touri_capabilities"
    result = call_uri("workflow://flow/weather/dry-run", registry, context={"root": repo_root})
    payload = result.to_dict()
    assert payload["ok"] is True
    assert payload["capability"] == "workflow.weather.flow"
    assert payload["backend"] == "uri_flow"
    assert payload["result_type"] == "plan"
    assert payload["data"]["plan"]["graph_id"] == "weather-agent-local-health"


def test_uri_graph_backend_dry_run(repo_root: Path):
    registry = repo_root / "examples" / "20_touri_capabilities"
    result = call_uri("workflow://graph/check-agent-health/dry-run", registry, context={"root": repo_root})
    payload = result.to_dict()
    assert payload["ok"] is True
    assert payload["capability"] == "workflow.check_health.graph"
    assert payload["backend"] == "uri_graph"
    assert payload["result_type"] == "plan"
    assert payload["data"]["plan"]["graph_id"] == "check-agent-health"
