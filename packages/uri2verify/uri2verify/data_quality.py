from __future__ import annotations

from typing import Any, Protocol

from uri3.results import ServiceResult

from uri2verify.errors import data_quality_error

_DATA_QUALITY_SOURCE = "uri2verify.data_quality"


class ValidatorRunner(Protocol):
    def __call__(
        self,
        validator_uri: str,
        payload: dict[str, Any],
        context: dict[str, Any],
    ) -> ServiceResult: ...


def _validator_payload(result: ServiceResult, payload: dict[str, Any]) -> dict[str, Any]:
    return {"result": result.to_dict(), "payload": payload}


def _validation_detail(validation: ServiceResult) -> str:
    if validation.errors:
        return str(validation.errors[0].detail)
    return str(validation.meta.get("detail") or "validation failed")


def _append_quality_error(
    result: ServiceResult,
    *,
    code: str,
    source: str,
    detail: str,
    recoverable: bool,
    data_quality: dict[str, Any] | None = None,
) -> None:
    result.ok = False
    result.result_type = "error"
    result.errors.append(
        data_quality_error(
            code=code,
            source=source,
            detail=detail,
            recoverable=recoverable,
            data_quality=data_quality,
        )
    )


def _with_verification_statuses(
    result: ServiceResult,
    *,
    data_quality_checked: bool,
) -> ServiceResult:
    from uri2verify.result_checks import apply_verification_statuses

    return apply_verification_statuses(
        result,
        data_quality_checked=data_quality_checked,
    )


def run_validators(
    *,
    data_quality: dict[str, Any],
    result: ServiceResult,
    payload: dict[str, Any],
    context: dict[str, Any],
    source: str,
    failure_code: str,
    recoverable: bool,
    run_validator: ValidatorRunner,
) -> ServiceResult | None:
    for validator_uri in data_quality.get("validators") or []:
        validation = run_validator(str(validator_uri), _validator_payload(result, payload), context)
        if validation.ok:
            continue
        _append_quality_error(
            result,
            code=str(validation.meta.get("failure_code") or failure_code),
            source=source,
            detail=_validation_detail(validation),
            recoverable=recoverable,
            data_quality=dict(validation.meta.get("data_quality") or {}),
        )
        return _with_verification_statuses(
            result.finalize(refresh_statuses=True),
            data_quality_checked=True,
        )
    return None


def check_confidence(
    result: ServiceResult,
    *,
    min_confidence: Any,
    source: str,
    failure_code: str,
    recoverable: bool,
) -> bool:
    confidence = result.meta.get("confidence")
    if min_confidence is None or confidence is None:
        return False
    try:
        if float(confidence) >= float(min_confidence):
            return False
    except (TypeError, ValueError):
        result.warnings.append(f"invalid confidence value: {confidence!r}")
        return False
    _append_quality_error(
        result,
        code=failure_code,
        source=source,
        detail=f"confidence {confidence} below min_confidence {min_confidence}",
        recoverable=recoverable,
        data_quality={"confidence": confidence, "min_confidence": min_confidence},
    )
    return True


def check_relevance_required(
    result: ServiceResult,
    *,
    required: Any,
    source: str,
    failure_code: str,
) -> bool:
    if not required or result.data is not None:
        return False
    _append_quality_error(
        result,
        code=failure_code,
        source=source,
        detail="relevance_required but result data is empty",
        recoverable=True,
    )
    return True


def _quality_settings(data_quality: dict[str, Any]) -> tuple[str, bool]:
    failure_code = str(data_quality.get("failure_code") or "DATA_QUALITY_FAILED")
    recoverable = bool(data_quality.get("recoverable", True))
    return failure_code, recoverable


def _check_result_quality(
    result: ServiceResult,
    data_quality: dict[str, Any],
    *,
    failure_code: str,
    recoverable: bool,
) -> bool:
    refresh_statuses = check_confidence(
        result,
        min_confidence=data_quality.get("min_confidence"),
        source=_DATA_QUALITY_SOURCE,
        failure_code=failure_code,
        recoverable=recoverable,
    )
    relevance_failed = check_relevance_required(
        result,
        required=data_quality.get("relevance_required"),
        source=_DATA_QUALITY_SOURCE,
        failure_code=failure_code,
    )
    return refresh_statuses or relevance_failed


def apply_data_quality(
    *,
    data_quality: dict[str, Any],
    result: ServiceResult,
    payload: dict[str, Any],
    context: dict[str, Any],
    source: str,
    run_validator: ValidatorRunner,
) -> ServiceResult:
    dq = data_quality or {}
    if not dq or not result.ok:
        return result.finalize()

    failure_code, recoverable = _quality_settings(dq)

    validator_failure = run_validators(
        data_quality=dq,
        result=result,
        payload=payload,
        context=context,
        source=_DATA_QUALITY_SOURCE,
        failure_code=failure_code,
        recoverable=recoverable,
        run_validator=run_validator,
    )
    if validator_failure is not None:
        return validator_failure

    refresh_statuses = _check_result_quality(
        result,
        dq,
        failure_code=failure_code,
        recoverable=recoverable,
    )

    result = result.finalize(refresh_statuses=refresh_statuses)
    return _with_verification_statuses(result, data_quality_checked=bool(dq))
