from __future__ import annotations

from typing import Any

from uri2verify.data_quality import apply_data_quality as _apply_data_quality

from .backends.python_backend import call_python_backend
from .models import ServiceResult


def apply_data_quality(
    manifest,
    result: ServiceResult,
    payload: dict[str, Any],
    context: dict[str, Any],
) -> ServiceResult:
    def run_validator(
        validator_uri: str, body: dict[str, Any], ctx: dict[str, Any]
    ) -> ServiceResult:
        return call_python_backend(validator_uri, body, ctx)

    return _apply_data_quality(
        data_quality=manifest.data_quality or {},
        result=result,
        payload=payload,
        context=context,
        source=f"touri://capability/{manifest.capability.id}",
        run_validator=run_validator,
    )
