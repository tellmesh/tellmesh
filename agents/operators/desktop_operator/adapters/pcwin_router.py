from __future__ import annotations

import os
from typing import Any

from agents.operators.desktop_operator.adapters import pcwin_mock, pcwin_uia

PCWIN_SCHEMES = frozenset({"pcwin"})
_UIA_READY: bool | None = None


def _uia_ready() -> bool:
    global _UIA_READY
    if _UIA_READY is not None:
        return _UIA_READY
    _UIA_READY = pcwin_uia.uia_available()
    return _UIA_READY


def resolve_adapter_mode(scheme: str, context: dict[str, Any] | None = None) -> str:
    ctx = context or {}
    requested = str(ctx.get("adapter") or os.getenv("URI2OPS_PCWIN_ADAPTER", "auto")).lower()
    if scheme not in PCWIN_SCHEMES:
        return requested if requested != "auto" else "mock"
    if requested == "mock":
        return "mock"
    if requested in {"uia", "windows"}:
        return "uia"
    return "uia" if _uia_ready() else "mock"


def _dispatch(operation: str, payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    mode = resolve_adapter_mode("pcwin", context)
    handlers = {
        "focus": pcwin_uia.focus if mode == "uia" else pcwin_mock.focus,
        "click": pcwin_uia.click if mode == "uia" else pcwin_mock.click,
    }
    handler = handlers.get(operation)
    if handler is None:
        return {"ok": False, "error": f"unsupported pcwin operation: {operation}"}
    return handler(payload, context)


def focus(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    return _dispatch("focus", payload, context)


def click(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    return _dispatch("click", payload, context)
