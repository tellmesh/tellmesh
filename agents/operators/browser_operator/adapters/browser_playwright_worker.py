"""Isolated Playwright worker entrypoint (fresh interpreter, no asyncio loop pollution)."""

from __future__ import annotations

import json
import sys
from typing import Any

from uri2ops.operator.artifacts import write_step_artifact


def capture_page(payload: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    try:
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError as exc:
        from agents.operators.browser_operator.adapters.browser_playwright import playwright_import_error

        return playwright_import_error(exc)

    url = str(payload.get("url") or payload.get("target_uri") or "about:blank")
    task_id = str(context.get("task_id") or "task")
    run_id = str(context.get("run_id") or "run")
    root = context.get("root")
    step_id = str(payload.get("step_id") or "capture_page")
    timeout_ms = int(payload.get("timeout_ms") or payload.get("navigation_timeout_ms") or 30_000)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.set_default_navigation_timeout(timeout_ms)
            page.set_default_timeout(timeout_ms)
            response = page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
            image = page.screenshot(full_page=True)
            meta = {
                "ok": True,
                "url": url,
                "title": page.title(),
                "status_code": response.status if response else None,
            }
        except Exception as exc:
            return {"ok": False, "error": "capture_failed", "detail": str(exc), "url": url}
        finally:
            browser.close()

    _, open_uri = write_step_artifact(
        task_id,
        run_id,
        step_id,
        "open.json",
        json.dumps(meta, indent=2, ensure_ascii=False),
        root=root,
    )
    path, shot_uri = write_step_artifact(
        task_id,
        run_id,
        step_id,
        "screenshot.png",
        image,
        root=root,
    )
    return {
        **meta,
        "artifact_uri": shot_uri,
        "screenshot_uri": shot_uri,
        "path": str(path),
        "open_artifact_uri": open_uri,
    }


def main() -> int:
    request = json.loads(sys.stdin.read() or "{}")
    operation = str(request.get("operation") or "capture_page")
    payload = dict(request.get("payload") or {})
    context = dict(request.get("context") or {})
    if operation == "capture_page":
        result = capture_page(payload, context)
    else:
        result = {"ok": False, "error": f"unsupported worker operation: {operation}"}
    sys.stdout.write(json.dumps(result))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
