from __future__ import annotations

import json
from typing import Any

from nl2uri.planner_templates import deterministic_weather_plan, generic_plan, is_weather_prompt


def validate_tree_data(tree: dict[str, Any]) -> list[str]:
    from uri3.validators.uri_tree_validator import SCHEMA_PATH

    from jsonschema import Draft202012Validator

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(tree), key=lambda item: item.path)
    return [f"{list(error.path)}: {error.message}" for error in errors]


def is_structured_uri_tree(tree: dict[str, Any]) -> bool:
    if not isinstance(tree, dict):
        return False
    domain = tree.get("domain")
    if not isinstance(domain, dict) or not domain.get("id") or not domain.get("uri"):
        return False
    if not isinstance(tree.get("commands"), dict):
        return False
    if not isinstance(tree.get("resources"), dict):
        return False
    agent = tree.get("agent")
    if not isinstance(agent, dict) or not agent.get("id") or not agent.get("uri"):
        return False
    return True


def normalize_llm_tree(prompt: str, candidate: dict[str, Any]) -> dict[str, Any]:
    if is_weather_prompt(prompt):
        base = deterministic_weather_plan(prompt)
        if not is_structured_uri_tree(candidate):
            base["planner_warning"] = "LLM returned simplified URI Tree; deterministic weather template used."
            return base
        errors = validate_tree_data(candidate)
        if errors:
            base["planner_warning"] = (
                "LLM URI Tree failed schema validation; deterministic weather template used. "
                + "; ".join(errors[:3])
            )
            return base
        if candidate.get("domain", {}).get("id") != "weather_map":
            base["planner_warning"] = "LLM changed weather domain id; deterministic weather template used."
            return base
        return candidate
    if not is_structured_uri_tree(candidate):
        plan = generic_plan(prompt)
        plan["planner_warning"] = "LLM returned simplified URI Tree; generic deterministic template used."
        return plan
    errors = validate_tree_data(candidate)
    if errors:
        plan = generic_plan(prompt)
        plan["planner_warning"] = (
            "LLM URI Tree failed schema validation; generic deterministic template used. "
            + "; ".join(errors[:3])
        )
        return plan
    return candidate
