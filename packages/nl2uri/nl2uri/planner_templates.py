from __future__ import annotations

import os
import re
from typing import Any

DEFAULT_MODEL_URI = "llm://openrouter/qwen/qwen3-coder-next"


def slug(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "generated-domain"


def llm_uri_from_env() -> str:
    from uri3.config.llm_profiles import resolve_llm_profile

    profile_name = os.getenv("DEFAULT_LLM_PROFILE", "domain_planner")
    try:
        return resolve_llm_profile(profile_name, resolve_secrets=False).model_uri
    except Exception:
        raw = os.getenv("DOMAIN_PLANNER_LLM") or os.getenv("LLM_MODEL")
        if not raw:
            return DEFAULT_MODEL_URI
        if raw.startswith("llm://"):
            return raw
        if raw.startswith("openrouter/"):
            return raw.replace("openrouter/", "llm://openrouter/", 1)
        return f"llm://{raw}"


def is_weather_prompt(prompt: str) -> bool:
    return bool(re.search(r"pogod|weather|forecast|map", prompt, re.I))


def deterministic_weather_plan(prompt: str) -> dict[str, Any]:
    days = 14 if re.search(r"dwa\s*tygod|two\s*weeks|14", prompt, re.I) else 7
    domain_id = "weather_map"
    agent_id = "weather-map-agent"
    return {
        "domain": {"id": domain_id, "uri": "domain://weather-map", "name": "weather-map", "description": "Generate forecast weather maps as HTML URL artifacts."},
        "standards": {"uri_tree_schema": "schemas/uri_tree.schema.json", "data_contract": "protobuf", "agent_manifest": "a2a_agent_card", "resource_model": "mcp_resources"},
        "inputs": {
            "place": {"uri": "input://weather-map/place", "type": "string", "required": True},
            "days": {"uri": "input://weather-map/days", "type": "integer", "default": days},
            "forecast_model": {"uri": "input://weather-map/forecast-model", "type": "string", "default": "auto"},
        },
        "llm": {"planner": {"uri": llm_uri_from_env(), "api_key_uri": "env://OPENROUTER_API_KEY"}},
        "commands": {
            "generate_weather_map": {
                "uri": "command://weather-map/generate",
                "name": "GenerateWeatherMap",
                "handler_uri": "python://domains.weather_map.handlers.generate_weather_map:handler",
                "input_schema_ref": "app.weather.v1.GenerateWeatherMapCommand",
                "emits": ["event://weather-map/WeatherMapGenerationRequested", "event://weather-map/WeatherMapGenerated"],
            }
        },
        "events": {
            "generation_requested": {"uri": "event://weather-map/WeatherMapGenerationRequested", "name": "WeatherMapGenerationRequested", "schema_ref": "app.weather.v1.WeatherMapGenerationRequested"},
            "generated": {"uri": "event://weather-map/WeatherMapGenerated", "name": "WeatherMapGenerated", "schema_ref": "app.weather.v1.WeatherMapGenerated"},
        },
        "resources": {
            "forecast_data": {"uri_template": "resource://weather/forecast/{place}/{days}", "schema_ref": "app.weather.v1.ForecastDataView", "renderer_ref": "json", "mime_type": "application/json"},
            "html_map": {"uri_template": "resource://weather/maps/{place}/forecast/{days}", "schema_ref": "app.weather.v1.WeatherMapHtmlView", "renderer_ref": "html", "mime_type": "text/html"},
        },
        "artifacts": {
            "html_file": {"uri_template": "artifact://weather-map/{place}/forecast/{days}/index.html", "mime_type": "text/html", "public_url_template": "http://localhost:8000/artifacts/weather-map/{place}/forecast/{days}/index.html"}
        },
        "agent": {
            "id": agent_id,
            "uri": f"agent://{agent_id}",
            "name": agent_id,
            "card_uri": f"a2a://{agent_id}/.well-known/agent-card.json",
            "capabilities": [
                {"name": "generate_weather_map", "type": "command", "uri": f"a2a://{agent_id}/skills/generate_weather_map"},
                {"name": "read_weather_map", "type": "resource_read", "uri": f"a2a://{agent_id}/skills/read_weather_map"},
            ],
        },
        "deployment": {"default": {"uri": "local://agents/generated/weather_map_agent"}},
        "mcp": {"resources_read": {"uri": f"mcp://{agent_id}/resources/read"}, "tools_call": {"uri": f"mcp://{agent_id}/tools/call"}},
        "dependencies": ["pypi://httpx", "pypi://jinja2", "pypi://pydantic"],
    }


def generic_plan(prompt: str) -> dict[str, Any]:
    slug_value = slug(prompt[:80])
    domain_id = slug_value.replace("-", "_")
    agent_id = f"{slug_value}-agent"
    return {
        "domain": {"id": domain_id, "uri": f"domain://{slug_value}", "name": slug_value, "description": prompt},
        "standards": {"uri_tree_schema": "schemas/uri_tree.schema.json", "data_contract": "protobuf", "agent_manifest": "a2a_agent_card", "resource_model": "mcp_resources"},
        "inputs": {"input": {"uri": f"input://{slug_value}/input", "type": "string", "required": True}},
        "commands": {"run": {"uri": f"command://{slug_value}/run", "name": "RunTask", "handler_uri": f"python://domains.{domain_id}.handlers.run:handler", "input_schema_ref": f"app.{domain_id}.v1.RunTaskCommand", "emits": [f"event://{slug_value}/TaskRequested", f"event://{slug_value}/TaskCompleted"]}},
        "events": {"requested": {"uri": f"event://{slug_value}/TaskRequested", "name": "TaskRequested", "schema_ref": f"app.{domain_id}.v1.TaskRequested"}, "completed": {"uri": f"event://{slug_value}/TaskCompleted", "name": "TaskCompleted", "schema_ref": f"app.{domain_id}.v1.TaskCompleted"}},
        "resources": {"result": {"uri_template": f"resource://{slug_value}/result/{{id}}", "schema_ref": f"app.{domain_id}.v1.TaskResultView", "renderer_ref": "json", "mime_type": "application/json"}},
        "artifacts": {},
        "agent": {"id": agent_id, "uri": f"agent://{agent_id}", "name": agent_id, "card_uri": f"a2a://{agent_id}/.well-known/agent-card.json", "capabilities": [{"name": "run", "type": "command", "uri": f"a2a://{agent_id}/skills/run"}]},
        "deployment": {"default": {"uri": f"local://agents/generated/{agent_id.replace('-', '_')}"}},
        "mcp": {"resources_read": {"uri": f"mcp://{agent_id}/resources/read"}},
        "dependencies": ["pypi://pydantic"],
    }
