from __future__ import annotations

from typing import Any

from uri2run import run_backend
from uri3.results import ServiceResult


def call_uri_flow_backend(
    flow_path: str,
    payload: dict[str, Any],
    context: dict[str, Any],
    *,
    backend_extra: dict[str, Any] | None = None,
) -> ServiceResult:
    backend = {**(backend_extra or {}), "type": "uri_flow", "flow": flow_path}
    return run_backend(backend, payload, context)


def call_uri_graph_backend(
    graph_path: str,
    payload: dict[str, Any],
    context: dict[str, Any],
    *,
    backend_extra: dict[str, Any] | None = None,
) -> ServiceResult:
    backend = {**(backend_extra or {}), "type": "uri_graph", "graph": graph_path}
    return run_backend(backend, payload, context)
