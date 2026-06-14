from __future__ import annotations

from typing import Any

from uri2run import run_backend
from uri3.results import ServiceResult


def call_uri2ops_backend(
    uri: str,
    scheme: str,
    operation: str,
    payload: dict[str, Any],
    context: dict[str, Any],
    *,
    backend_extra: dict[str, Any] | None = None,
) -> ServiceResult:
    backend = {
        **(backend_extra or {}),
        "type": "uri2ops",
        "uri": uri,
        "scheme": scheme,
        "operation": operation,
    }
    return run_backend(backend, payload, context)
