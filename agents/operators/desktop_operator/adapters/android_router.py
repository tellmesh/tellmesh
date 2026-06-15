from __future__ import annotations

import os
from typing import Any

from agents.operators.desktop_operator.adapters import android_adb, android_mock

ANDROID_SCHEMES = frozenset({"android"})
_ADB_READY: bool | None = None


def _adb_ready() -> bool:
    global _ADB_READY
    if _ADB_READY is not None:
        return _ADB_READY
    _ADB_READY = android_adb.adb_available() and bool(android_adb.list_devices())
    return _ADB_READY


def resolve_adapter_mode(scheme: str, context: dict[str, Any] | None = None) -> str:
    ctx = context or {}
    requested = str(ctx.get("adapter") or os.getenv("URI2OPS_ANDROID_ADAPTER", "auto")).lower()
    if scheme not in ANDROID_SCHEMES:
        return requested if requested != "auto" else "mock"
    if requested == "mock":
        return "mock"
    if requested == "adb":
        return "adb"
    return "adb" if _adb_ready() else "mock"


def _dispatch(operation: str, payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    mode = resolve_adapter_mode("android", context)
    handlers = {
        "screenshot": android_adb.screenshot if mode == "adb" else android_mock.screenshot,
        "dump_ui": android_adb.dump_ui if mode == "adb" else android_mock.dump_ui,
        "tap": android_adb.tap if mode == "adb" else android_mock.tap,
    }
    handler = handlers.get(operation)
    if handler is None:
        return {"ok": False, "error": f"unsupported android operation: {operation}"}
    return handler(payload, context)


def screenshot(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    return _dispatch("screenshot", payload, context)


def dump_ui(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    return _dispatch("dump_ui", payload, context)


def tap(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    return _dispatch("tap", payload, context)
