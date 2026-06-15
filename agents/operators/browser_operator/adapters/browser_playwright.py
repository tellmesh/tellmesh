from __future__ import annotations

import json
import queue
import threading
from typing import Any, Callable, TypeVar
from urllib.parse import urlparse

from agents.operators.browser_operator.adapters import browser_mock
from uri2ops.operator.artifacts import write_step_artifact

T = TypeVar("T")

def playwright_install_hint() -> str:
    import sys

    exe = sys.executable
    return (
        f"Playwright Python package missing for {exe}. "
        f"Run: {exe} -m pip install -e '.[browser]' && {exe} -m playwright install chromium"
    )


def playwright_browsers_hint() -> str:
    import sys

    exe = sys.executable
    return (
        f"Playwright browsers missing for {exe}. "
        f"Run: {exe} -m playwright install chromium"
    )


def playwright_import_error(exc: Exception | None = None) -> dict[str, Any]:
    detail = playwright_install_hint()
    if exc is not None:
        detail = f"{detail} ({exc})"
    return {"ok": False, "error": "playwright_not_installed", "detail": detail}


def playwright_browsers_error(exc: Exception | None = None) -> dict[str, Any]:
    detail = playwright_browsers_hint()
    if exc is not None:
        detail = f"{detail} ({exc})"
    return {"ok": False, "error": "playwright_browsers_missing", "detail": detail}


def playwright_available() -> bool:
    try:
        import playwright.sync_api  # noqa: F401
    except ModuleNotFoundError:
        return False
    return True


def json_dumps(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False)


class _PlaywrightWorker:
    """Dedicated thread for sync Playwright (greenlet-safe, asyncio-loop-safe)."""

    def __init__(self) -> None:
        self._jobs: queue.Queue[tuple[Callable[[], Any], queue.Queue[Any]] | None] = queue.Queue()
        self._thread = threading.Thread(target=self._loop, name="uri2ops-playwright", daemon=True)
        self._thread.start()

    def _loop(self) -> None:
        while True:
            item = self._jobs.get()
            if item is None:
                return
            work, reply = item
            try:
                reply.put(work())
            except Exception as exc:  # pragma: no cover - surfaced to caller
                reply.put(exc)

    def run(self, work: Callable[[], T]) -> T:
        reply: queue.Queue[Any] = queue.Queue(maxsize=1)
        self._jobs.put((work, reply))
        result = reply.get()
        if isinstance(result, Exception):
            raise result
        return result


_WORKER: _PlaywrightWorker | None = None


def _playwright_worker() -> _PlaywrightWorker:
    global _WORKER
    if _WORKER is None:
        _WORKER = _PlaywrightWorker()
    return _WORKER


def _run_sync(work: Callable[[], T]) -> T:
    """Always run sync Playwright on the dedicated worker thread."""
    return _playwright_worker().run(work)


def probe_playwright_ready() -> bool:
    """Check Chromium launch without leaving sync Playwright on the caller thread."""

    def _probe() -> bool:
        try:
            from playwright.sync_api import sync_playwright
        except ModuleNotFoundError:
            return False
        try:
            playwright = sync_playwright().start()
            try:
                browser = playwright.chromium.launch(headless=True)
                browser.close()
                return True
            finally:
                playwright.stop()
        except Exception:
            return False

    return _run_sync(_probe)


def _session(context: dict[str, Any] | None) -> dict[str, Any]:
    if context is None:
        raise ValueError("playwright browser session requires a mutable context dict")
    return context.setdefault("session", {})


def _task_context(context: dict[str, Any] | None) -> tuple[str, str, str | None]:
    if context is None:
        context = {}
    return str(context.get("task_id") or "task"), str(context.get("run_id") or "run"), context.get("root")


def close_playwright_session(context: dict[str, Any] | None) -> None:
    def _close() -> None:
        state = _session(context).get("playwright") or {}
        page = state.get("page")
        browser = state.get("browser")
        playwright = state.get("playwright")
        owner_thread = state.get("owner_thread")
        if owner_thread is not None and owner_thread != threading.get_ident():
            _session(context).pop("playwright", None)
            return
        for closer in (
            lambda: page.close() if page is not None else None,
            lambda: browser.close() if browser is not None else None,
            lambda: playwright.stop() if playwright is not None else None,
        ):
            try:
                closer()
            except Exception:
                pass
        _session(context).pop("playwright", None)

    try:
        _run_sync(_close)
    except Exception:
        if context is not None:
            session = context.setdefault("session", {})
            session.pop("playwright", None)


def open_page(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    def _open() -> dict[str, Any]:
        try:
            from playwright.sync_api import sync_playwright
        except ModuleNotFoundError as exc:
            return playwright_import_error(exc)

        url = str(payload.get("url") or payload.get("target_uri") or "about:blank")
        task_id, run_id, root = _task_context(context)
        step_id = str(payload.get("step_id") or "open_page")
        state = _session(context)
        playwright = sync_playwright().start()
        try:
            browser = playwright.chromium.launch(headless=True)
        except Exception as exc:
            playwright.stop()
            return playwright_browsers_error(exc)
        page = browser.new_page()
        timeout_ms = int(payload.get("timeout_ms") or payload.get("navigation_timeout_ms") or 30_000)
        page.set_default_navigation_timeout(timeout_ms)
        page.set_default_timeout(timeout_ms)
        try:
            response = page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
        except Exception as exc:
            browser.close()
            playwright.stop()
            return {"ok": False, "error": "navigation_failed", "detail": str(exc), "url": url}
        state["playwright"] = {
            "playwright": playwright,
            "browser": browser,
            "page": page,
            "url": url,
            "owner_thread": threading.get_ident(),
        }
        meta = {
            "ok": True,
            "url": url,
            "adapter": "playwright",
            "title": page.title(),
            "status_code": response.status if response else None,
            "text": page.inner_text("body"),
        }
        _, artifact_uri = write_step_artifact(
            task_id, run_id, step_id, "open.json", json_dumps(meta), root=root
        )
        return {**meta, "artifact_uri": artifact_uri}

    return _run_sync(_open)


def extract_dom(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    def _extract() -> dict[str, Any]:
        state = _session(context).get("playwright") or {}
        page = state.get("page")
        if page is None:
            return {"ok": False, "error": "browser session not open; run browser open first"}
        task_id, run_id, root = _task_context(context)
        step_id = str(payload.get("step_id") or "extract_dom")
        text = page.inner_text("body")
        html = page.content()
        meta = {"ok": True, "text": text, "html": html}
        _, artifact_uri = write_step_artifact(
            task_id, run_id, step_id, "dom.json", json_dumps(meta), root=root
        )
        return {**meta, "artifact_uri": artifact_uri}

    return _run_sync(_extract)


def screenshot(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    def _capture() -> dict[str, Any]:
        state = _session(context).get("playwright") or {}
        page = state.get("page")
        if page is None:
            return {"ok": False, "error": "browser session not open; run browser open first"}
        task_id, run_id, root = _task_context(context)
        step_id = str(payload.get("step_id") or "screenshot")
        image = page.screenshot(full_page=True)
        path, artifact_uri = write_step_artifact(
            task_id, run_id, step_id, "screenshot.png", image, root=root
        )
        return {"ok": True, "artifact_uri": artifact_uri, "screenshot_uri": artifact_uri, "path": str(path)}

    return _run_sync(_capture)


def click(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    def _click() -> dict[str, Any]:
        state = _session(context).get("playwright") or {}
        page = state.get("page")
        if page is None:
            return {"ok": False, "error": "browser session not open; run browser open first"}
        selector = payload.get("selector")
        if selector:
            page.click(str(selector))
        elif payload.get("x") is not None and payload.get("y") is not None:
            page.mouse.click(float(payload["x"]), float(payload["y"]))
        else:
            return {"ok": False, "error": "click requires selector or x/y coordinates"}
        task_id, run_id, root = _task_context(context)
        step_id = str(payload.get("step_id") or "click")
        meta = {"ok": True, "selector": selector, "x": payload.get("x"), "y": payload.get("y")}
        _, artifact_uri = write_step_artifact(
            task_id, run_id, step_id, "click.json", json_dumps(meta), root=root
        )
        return {**meta, "artifact_uri": artifact_uri}

    return _run_sync(_click)


def capture_page(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    import subprocess
    import sys

    runtime = dict(context or {})
    proc = subprocess.run(
        [sys.executable, "-m", "agents.operators.browser_operator.adapters.browser_playwright_worker"],
        input=json.dumps(
            {
                "operation": "capture_page",
                "payload": payload,
                "context": {
                    "task_id": runtime.get("task_id"),
                    "run_id": runtime.get("run_id"),
                    "root": runtime.get("root"),
                },
            }
        ),
        capture_output=True,
        text=True,
        timeout=int(payload.get("timeout_ms") or payload.get("navigation_timeout_ms") or 120_000) // 1000 + 30,
    )
    if proc.returncode != 0 and not proc.stdout.strip():
        detail = (proc.stderr or "").strip() or f"playwright worker exited {proc.returncode}"
        return {"ok": False, "error": "capture_failed", "detail": detail}
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "error": "capture_failed", "detail": proc.stdout or proc.stderr}


def execute(payload: dict[str, Any], context: dict[str, Any] | None = None) -> dict[str, Any]:
    target_uri = str(payload.get("target_uri") or "")
    operation = str(payload.get("operation") or "")
    scheme = urlparse(target_uri).scheme
    if scheme == "browser" and operation == "open":
        return open_page(payload, context)
    if operation in {"extract_dom", "read", "extract"} or scheme in {"dom", "browser"}:
        return extract_dom(payload, context)
    if operation in {"screenshot", "capture"} or scheme == "screen":
        return screenshot(payload, context)
    if operation in {"capture_page", "capture"} and payload.get("url"):
        return capture_page(payload, context)
    if operation == "click":
        return click(payload, context)
    return browser_mock.open_page(payload, context)
