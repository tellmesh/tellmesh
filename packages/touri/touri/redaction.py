from __future__ import annotations

from typing import Any

from uri2ops.operator.redaction import redact_payload

from .models import ServiceResult


def should_redact(policy: dict[str, Any] | None) -> bool:
    if not policy:
        return True
    return policy.get("redact_secrets", True) is not False


def apply_redaction(result: ServiceResult, policy: dict[str, Any] | None) -> ServiceResult:
    if not should_redact(policy):
        return result
    if isinstance(result.data, dict):
        result.data = redact_payload(result.data)
    elif isinstance(result.data, list):
        result.data = [redact_payload(item) if isinstance(item, dict) else item for item in result.data]
    if isinstance(result.meta, dict):
        result.meta = redact_payload(result.meta)
    return result
