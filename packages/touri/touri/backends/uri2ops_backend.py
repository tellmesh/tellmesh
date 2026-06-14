from __future__ import annotations

from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from touri.models import ServiceResult, service_result
from uri2ops.operation_registry.dispatcher import dispatch
from uri3.results import normalize_error

_OPERATOR_SCHEMES = frozenset({"browser", "dom", "screen", "input", "android", "pcwin"})
_OPERATION_MAP: dict[tuple[str, str], str] = {
    ("browser", "read"): "extract_dom",
    ("browser", "extract"): "extract_dom",
    ("dom", "read"): "extract_dom",
    ("dom", "extract"): "extract_dom",
    ("dom", "extract_dom"): "extract_dom",
    ("browser", "capture"): "screenshot",
    ("browser", "screenshot"): "screenshot",
    ("screen", "capture"): "observe",
    ("screen", "screenshot"): "observe",
    ("input", "call"): "type",
    ("input", "type"): "type",
}


def _registry_scheme(scheme: str) -> str:
    if scheme == "dom":
        return "browser"
    return scheme


def _registry_operation(scheme: str, operation: str) -> str:
    return _OPERATION_MAP.get((scheme, operation), operation)


def _resolve_root(context: dict[str, Any]) -> Path:
    root = context.get("root")
    if root:
        return Path(root)
    from uri3.config.repo_root import find_repo_root

    return find_repo_root()


def call_uri2ops_backend(
    uri: str,
    scheme: str,
    operation: str,
    payload: dict[str, Any],
    context: dict[str, Any],
    *,
    backend_extra: dict[str, Any] | None = None,
) -> ServiceResult:
    extra = backend_extra or {}
    if scheme not in _OPERATOR_SCHEMES:
        return service_result(
            ok=False,
            result_type="error",
            errors=[{"code": "URI2OPS_SCHEME_UNSUPPORTED", "detail": f"scheme not supported by uri2ops: {scheme}"}],
        )

    registry_scheme = _registry_scheme(scheme)
    registry_operation = _registry_operation(scheme, str(extra.get("operation") or operation))
    dispatch_payload = dict(payload)
    dispatch_payload.setdefault("target_uri", uri)
    dispatch_payload.setdefault("step_id", context.get("capability") or urlparse(uri).path.strip("/") or "step")

    runtime_context = {
        "adapter": str(payload.get("adapter", extra.get("adapter", "mock"))),
        "root": str(_resolve_root(context)),
        "task_id": str(context.get("capability") or "touri"),
        "run_id": str(context.get("run_id") or "touri-call"),
        "session": dict(context.get("session") or {}),
    }

    try:
        output = dispatch(registry_scheme, registry_operation, dispatch_payload, runtime_context)
    except Exception as exc:
        return service_result(
            ok=False,
            result_type="error",
            errors=[{"code": "URI2OPS_DISPATCH_FAILED", "detail": str(exc)}],
        )

    if isinstance(output, ServiceResult):
        return output.finalize()

    if isinstance(output, dict) and "ok" in output:
        errors = [normalize_error(item) for item in output.get("errors") or []]
        return service_result(
            ok=bool(output.get("ok")),
            result_type=str(output.get("result_type", "data")),
            data=output.get("data", output),
            artifact_uri=output.get("artifact_uri"),
            warnings=list(output.get("warnings") or []),
            errors=errors,
            meta=dict(output.get("meta") or {}),
            workflow_status=output.get("workflow_status"),
            execution_status=output.get("execution_status"),
            service_result_status=output.get("service_result_status"),
        )

    return service_result(ok=True, result_type="data", data=output)
