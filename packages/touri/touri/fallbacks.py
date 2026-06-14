from __future__ import annotations

from typing import Any

from touri.backend_dispatch import call_backend
from touri.models import ServiceResult


def payload_from_params(params: dict[str, str], payload: dict[str, Any] | None) -> dict[str, Any]:
    merged: dict[str, Any] = dict(params)
    if payload:
        merged.update(payload)
    return merged


def error_codes(result: ServiceResult) -> list[str]:
    codes: list[str] = []
    for item in result.errors:
        code = getattr(item, "code", None) or (item.get("code") if isinstance(item, dict) else None)
        if code:
            codes.append(str(code))
    return codes


def fallback_matches(when: str | None, result: ServiceResult) -> bool:
    if not when or when in {"any", "*"}:
        return not result.ok
    return when in error_codes(result)


def fallback_entry_matches(backend: Any, when: Any, result: ServiceResult) -> bool:
    if not isinstance(backend, dict):
        return False
    return fallback_matches(str(when) if when else None, result)


def decorate_fallback_result(
    fallback_result: ServiceResult,
    original_result: ServiceResult,
    manifest,
    backend: dict[str, Any],
    when: Any,
) -> None:
    fallback_result.uri = original_result.uri
    fallback_result.capability = manifest.capability.id
    fallback_result.backend = str(backend.get("type") or "fallback")
    fallback_result.meta = {
        **fallback_result.meta,
        "fallback_from": manifest.capability.id,
        "fallback_when": when,
    }


def apply_fallbacks(
    manifest,
    result: ServiceResult,
    payload: dict[str, Any],
    context: dict[str, Any],
) -> ServiceResult:
    if result.ok or not manifest.fallbacks:
        return result
    for entry in manifest.fallbacks:
        if not isinstance(entry, dict):
            continue
        when = entry.get("when")
        backend = entry.get("backend")
        if not fallback_entry_matches(backend, when, result):
            continue
        fallback_result = call_backend(backend, payload, context)
        decorate_fallback_result(fallback_result, result, manifest, backend, when)
        if fallback_result.ok:
            fallback_result.warnings.append(f"fallback applied for {when or 'any'}")
            from touri.data_quality import apply_data_quality

            return apply_data_quality(manifest, fallback_result, payload, context)
    return result
