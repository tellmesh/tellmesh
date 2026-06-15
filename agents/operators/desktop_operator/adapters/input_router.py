from __future__ import annotations

import os
from typing import Any

from agents.operators.desktop_operator.adapters import input_gnome, input_mock

INPUT_SCHEMES = frozenset({"input"})
_GNOME_READY: bool | None = None


def _gnome_ready() -> bool:
    global _GNOME_READY
    if _GNOME_READY is not None:
        return _GNOME_READY
    _GNOME_READY = input_gnome.gnome_input_available()
    return _GNOME_READY


def resolve_adapter_mode(scheme: str, context: dict[str, Any] | None = None) -> str:
    ctx = context or {}
    requested = str(ctx.get("adapter") or os.getenv("URI2OPS_INPUT_ADAPTER", "auto")).lower()
    if scheme not in INPUT_SCHEMES:
        return requested if requested != "auto" else "mock"
    if requested == "mock":
        return "mock"
    if requested == "gnome":
        return "gnome"
    return "gnome" if _gnome_ready() else "mock"


def type_text(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    mode = resolve_adapter_mode("input", context)
    if mode == "gnome":
        return input_gnome.type_text(payload, context)
    return input_mock.type_text(payload, context)
