from __future__ import annotations

from typing import Any

import httpx
from uri3.results import service_result

from uri2run.result import error_result


def _response_data(response: httpx.Response) -> Any:
    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            return response.json()
        except ValueError:
            return {"raw": response.text, "json_error": "invalid_json"}
    return response.text


def _mapping(value: Any) -> dict[str, Any] | None:
    return value if isinstance(value, dict) else None


def run_http(target: str, payload: dict[str, Any], context: dict[str, Any]):
    method = str(payload.get("method") or "GET").upper()
    timeout = float(payload.get("timeout", context.get("timeout", 10.0)))
    json_body = payload.get("json")
    params = _mapping(payload.get("params"))
    headers = _mapping(payload.get("headers"))
    data = payload.get("data", payload.get("body"))
    content = payload.get("content")
    retries = int(payload.get("retries", 0) or 0)
    attempts = retries + 1
    attempt_count = 0
    last_error: httpx.HTTPError | None = None
    response = None

    for _attempt in range(attempts):
        attempt_count += 1
        try:
            request_kwargs: dict[str, Any] = {"timeout": timeout}
            if json_body is not None:
                request_kwargs["json"] = json_body
            if data is not None:
                request_kwargs["data"] = data
            if content is not None:
                request_kwargs["content"] = content
            if params is not None:
                request_kwargs["params"] = params
            if headers is not None:
                request_kwargs["headers"] = headers
            response = httpx.request(method, target, **request_kwargs)
            break
        except httpx.HTTPError as exc:
            last_error = exc

    if response is None:
        detail = str(last_error) if last_error else "HTTP transport failed"
        return error_result("HTTP_TRANSPORT_FAILED", detail, result_type="http")

    return service_result(
        ok=200 <= response.status_code < 400,
        result_type="http",
        data={
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "body": _response_data(response),
        },
        meta={"transport": "http", "method": method, "attempts": attempt_count},
    )


def run_http_transport(
    backend: dict[str, Any],
    payload: dict[str, Any],
    context: dict[str, Any],
):
    target = backend.get("target") or backend.get("url")
    if not target:
        return error_result("BACKEND_INVALID", "http backend missing target/url")
    return run_http(str(target), payload, context)
