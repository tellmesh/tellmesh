"""URI resolver tests for uri3."""

from __future__ import annotations

import warnings

import pytest

from uri3.resolvers.router import Uri3Router, call, resolve


def test_env_uri_resolution(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "secret")
    result = resolve("env://OPENROUTER_API_KEY")
    assert result.kind == "env"
    assert result.target["exists"] is True
    assert result.target["value"] == "secret"


def test_llm_uri_resolution():
    result = resolve("llm://openrouter/qwen/qwen3-coder-next")
    assert result.kind == "llm"
    assert result.target["provider"] == "openrouter"
    assert result.target["api_key_uri"] == "env://OPENROUTER_API_KEY"


def test_pypi_uri_resolution():
    result = resolve("pypi://httpx")
    assert result.target["package"] == "httpx"


def test_python_uri_resolution():
    result = resolve("python://nl2uri.planner:rule_based_plan")
    assert result.target["module"] == "nl2uri.planner"
    assert result.target["function"] == "rule_based_plan"


def test_http_uri_resolution():
    result = resolve("https://example.com/health")
    assert result.target["transport"] == "http"


def test_a2a_uri_resolution():
    result = resolve("a2a://weather-map-agent/.well-known/agent-card.json")
    assert result.target["protocol"] == "a2a"
    assert result.target["agent"] == "weather-map-agent"


def test_mcp_uri_resolution():
    result = resolve("mcp://filesystem/tools/list")
    assert result.target["protocol"] == "mcp"


def test_resource_uri_resolution():
    result = resolve("domain://weather-map")
    assert result.kind == "domain"
    assert result.target["namespace"] == "weather-map"


def test_python_call():
    result = call("python://copy:deepcopy", {"prompt": "weather map"})
    assert result == {"prompt": "weather map"}


def test_router_resolve_returns_uri_resolution():
    result = Uri3Router().resolve("pypi://httpx")
    assert isinstance(result, type(resolve("pypi://httpx")))


def test_unsupported_scheme():
    with pytest.raises(ValueError, match="Unsupported URI scheme"):
        resolve("unknown://foo")


def test_deprecated_uri2llm_reexport():
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        from hypervisor.uri2llm import resolve as legacy_resolve

        result = legacy_resolve("pypi://httpx")
    assert any(issubclass(w.category, DeprecationWarning) for w in caught)
    assert result.target["package"] == "httpx"
