from __future__ import annotations

from typing import Any

from uri3.results import ErrorEnvelope


def data_quality_error(
    *,
    code: str,
    source: str,
    detail: str,
    recoverable: bool,
    data_quality: dict[str, Any] | None = None,
) -> ErrorEnvelope:
    return ErrorEnvelope(
        code=code,
        source=source,
        recoverable=recoverable,
        detail=detail,
        data_quality=dict(data_quality or {}),
    )
