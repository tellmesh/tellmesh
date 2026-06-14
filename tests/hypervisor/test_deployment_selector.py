from __future__ import annotations

from hypervisor.deployment_registry.selector import parse_hypervisor_uri, resolve_deployment


def test_parse_hypervisor_local_uri():
    selector, action = parse_hypervisor_uri("hypervisor://local/weather-agent/run")
    assert selector == "weather-agent"
    assert action == "run"


def test_parse_hypervisor_deployment_uri():
    selector, action = parse_hypervisor_uri("hypervisor://deployment/weather-map-agent.local/run")
    assert selector == "weather-map-agent.local"
    assert action == "run"


def test_resolve_local_weather_agent_alias():
    deployment = resolve_deployment("weather-agent", prefer_local=True)
    assert deployment.id == "weather-map-agent.local"
