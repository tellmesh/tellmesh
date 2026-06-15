from __future__ import annotations

import os
from typing import Any

from agents.operators.desktop_operator.adapters import screen_gnome, screen_mock

SCREEN_SCHEMES = frozenset({"screen"})
_GNOME_READY: bool | None = None


def _gnome_ready() -> bool:
    global _GNOME_READY
    if _GNOME_READY is not None:
        return _GNOME_READY
    _GNOME_READY = screen_gnome.gnome_available()
    return _GNOME_READY


def resolve_adapter_mode(scheme: str, context: dict[str, Any] | None = None) -> str:
    ctx = context or {}
    requested = str(ctx.get("adapter") or os.getenv("URI2OPS_SCREEN_ADAPTER", "auto")).lower()
    if scheme not in SCREEN_SCHEMES:
        return requested if requested != "auto" else "mock"
    if requested in {"mock", "playwright"}:
        return "mock"
    if requested == "gnome":
        return "gnome"
    return "gnome" if _gnome_ready() else "mock"


def observe(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    mode = resolve_adapter_mode("screen", context)
    if mode == "gnome":
        return screen_gnome.observe(payload, context)
    return screen_mock.observe(payload, context)
