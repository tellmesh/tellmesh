from __future__ import annotations

import os
from typing import Any

from agents.operators.browser_operator.adapters import browser_mock, browser_playwright

_PLAYWRIGHT_READY: bool | None = None
BROWSER_SCHEMES = frozenset({"browser", "dom", "screen"})


def _playwright_ready() -> bool:
    global _PLAYWRIGHT_READY
    if _PLAYWRIGHT_READY is not None:
        return _PLAYWRIGHT_READY
    _PLAYWRIGHT_READY = browser_playwright.probe_playwright_ready()
    return _PLAYWRIGHT_READY


def playwright_ready() -> bool:
    return _playwright_ready()


def resolve_adapter_mode(scheme: str, context: dict[str, Any] | None = None) -> str:
    ctx = context or {}
    requested = str(ctx.get("adapter") or os.getenv("URI2OPS_BROWSER_ADAPTER", "auto")).lower()
    if scheme not in BROWSER_SCHEMES and scheme != "browser":
        return requested if requested != "auto" else "mock"
    if requested == "mock":
        return "mock"
    if requested == "playwright":
        return "playwright"
    return "playwright" if _playwright_ready() else "mock"


def _dispatch(
    operation: str,
    payload: dict[str, Any],
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = dict(payload)
    payload.setdefault("operation", operation)
    target_scheme = str(payload.get("target_uri", "browser://")).split(":", 1)[0]
    mode = resolve_adapter_mode(target_scheme, context)
    if mode == "playwright":
        if not browser_playwright.playwright_available():
            return browser_playwright.playwright_import_error()
        handlers = {
            "open": browser_playwright.open_page,
            "extract_dom": browser_playwright.extract_dom,
            "screenshot": browser_playwright.screenshot,
            "capture_page": browser_playwright.capture_page,
            "click": browser_playwright.click,
        }
        handler = handlers.get(operation, browser_playwright.execute)
        return handler(payload, context)
    handlers = {
        "open": browser_mock.open_page,
        "extract_dom": browser_mock.extract_dom,
        "screenshot": browser_mock.screenshot,
        "capture_page": browser_mock.capture_page,
        "click": browser_mock.click,
    }
    return handlers.get(operation, browser_mock.open_page)(payload, context)


def open_page(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    return _dispatch("open", payload, context)


def extract_dom(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    return _dispatch("extract_dom", payload, context)


def screenshot(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    return _dispatch("screenshot", payload, context)


def capture_page(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    return _dispatch("capture_page", payload, context)


def click(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    return _dispatch("click", payload, context)


def cleanup_browser_session(context: dict[str, Any] | None) -> None:
    browser_playwright.close_playwright_session(context)
