from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any


def _cap_value(capability: Any, field: str) -> Any:
    value = getattr(capability, field, None)
    if value is not None:
        return value
    if isinstance(capability, dict):
        return capability.get(field)
    return None


def _resource_read_check(capability: Any) -> dict[str, Any]:
    return {
        "agent": _cap_value(capability, "agent"),
        "capability": _cap_value(capability, "name"),
        "kind": "resource_read",
        "check": "uri_resolves_and_schema_matches",
        "uri": _cap_value(capability, "uri"),
        "expected_schema": _cap_value(capability, "output_schema"),
    }


def _command_check(capability: Any) -> dict[str, Any]:
    return {
        "agent": _cap_value(capability, "agent"),
        "capability": _cap_value(capability, "name"),
        "kind": "command",
        "check": "command_has_input_schema_and_emitted_events",
        "command": _cap_value(capability, "command"),
        "input_schema": _cap_value(capability, "input_schema"),
        "emits": _cap_value(capability, "emits"),
    }


_CAPABILITY_CHECK_BUILDERS: dict[str, Callable[[Any], dict[str, Any]]] = {
    "resource_read": _resource_read_check,
    "command": _command_check,
}


def build_capability_test_plan(capabilities: Iterable[Any]) -> list[dict[str, Any]]:
    """Build a generic capability verification plan from capability records."""
    plan: list[dict[str, Any]] = []
    for cap in capabilities:
        builder = _CAPABILITY_CHECK_BUILDERS.get(str(_cap_value(cap, "type") or ""))
        if builder is not None:
            plan.append(builder(cap))
    return plan
