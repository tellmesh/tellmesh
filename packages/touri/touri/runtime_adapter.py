from __future__ import annotations

from typing import Any

from touri.models import BackendRef


def backend_to_dict(backend: BackendRef | dict[str, Any]) -> dict[str, Any]:
    if isinstance(backend, dict):
        return dict(backend)
    data: dict[str, Any] = {"type": backend.type}
    for key in ("target", "command", "method", "url", "operation", "flow", "graph"):
        value = getattr(backend, key, None)
        if value:
            data[key] = value
    if backend.extra:
        data.update(backend.extra)
    return data
