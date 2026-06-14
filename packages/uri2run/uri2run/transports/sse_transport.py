from __future__ import annotations

import json
from typing import Any

import httpx
from uri3.results import ServiceResult, service_result

from uri2run.result import error_result


def _parse_sse_line(line: str) -> dict[str, Any] | None:
    if not line.startswith("data:"):
        return None
    body = line.split(":", 1)[1].strip()
    if not body:
        return None
    try:
        parsed = json.loads(body)
        return parsed if isinstance(parsed, dict) else {"data": parsed}
    except json.JSONDecodeError:
        return {"data": body}


def run_sse(target: str, payload: dict[str, Any], context: dict[str, Any]) -> ServiceResult:
    timeout = float(payload.get("timeout", context.get("timeout", 10.0)))
    max_events = int(payload.get("max_events", 50))
    events: list[dict[str, Any]] = []
    try:
        with httpx.stream("GET", target, timeout=timeout) as response:
            if response.status_code >= 400:
                return error_result(
                    "SSE_HTTP_ERROR",
                    f"HTTP {response.status_code} for {target}",
                    result_type="sse",
                )
            for line in response.iter_lines():
                if not line:
                    continue
                event = _parse_sse_line(line)
                if event is not None:
                    events.append(event)
                if len(events) >= max_events:
                    break
    except httpx.HTTPError as exc:
        return error_result("SSE_TRANSPORT_FAILED", str(exc), result_type="sse")
    return service_result(
        ok=True,
        result_type="sse",
        data={"events": events, "count": len(events), "url": target},
        meta={"transport": "sse"},
    )


def run_sse_transport(
    backend: dict[str, Any],
    payload: dict[str, Any],
    context: dict[str, Any],
) -> ServiceResult:
    target = backend.get("target") or backend.get("url")
    if not target:
        return error_result("BACKEND_INVALID", "sse backend missing target/url")
    return run_sse(str(target), payload, context)
