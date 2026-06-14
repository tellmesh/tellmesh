from __future__ import annotations

import asyncio
import json
from typing import Any

from uri3.results import ServiceResult, service_result

from uri2run.result import error_result


def run_ws(target: str, payload: dict[str, Any], context: dict[str, Any]) -> ServiceResult:
    try:
        import websockets
    except ImportError:
        return error_result(
            "WS_DEPENDENCY_MISSING",
            "install websockets package for ws:// transport",
            result_type="ws",
        )

    message = payload.get("message", payload)
    timeout = float(payload.get("timeout", context.get("timeout", 10.0)))

    async def _call() -> dict[str, Any]:
        async with websockets.connect(target) as websocket:
            if message is not None:
                await websocket.send(json.dumps(message, ensure_ascii=False))
            raw = await asyncio.wait_for(websocket.recv(), timeout=timeout)
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return {"text": raw}

    try:
        data = asyncio.run(_call())
    except Exception as exc:
        return error_result("WS_TRANSPORT_FAILED", str(exc), result_type="ws")

    if isinstance(data, dict) and "ok" in data:
        from uri2run.result import result_from_output

        return result_from_output(data)
    return service_result(ok=True, result_type="ws", data=data, meta={"transport": "ws"})


def run_ws_transport(
    backend: dict[str, Any],
    payload: dict[str, Any],
    context: dict[str, Any],
) -> ServiceResult:
    target = backend.get("target") or backend.get("url")
    if not target:
        return error_result("BACKEND_INVALID", "ws backend missing target/url")
    return run_ws(str(target), payload, context)
