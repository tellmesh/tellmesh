from __future__ import annotations

from typing import Any

from .errors import normalize_error
from .statuses import (
    EXECUTION_COMPLETED,
    EXECUTION_FAILED,
    SERVICE_FAILED,
    SERVICE_SUCCEEDED,
    WORKFLOW_COMPLETED,
    WORKFLOW_COMPLETED_WITH_SERVICE_ERROR,
    WORKFLOW_FAILED,
    derive_statuses,
)


def step_execution_status(*, status: str, has_result: bool = False, dry_run: bool = False) -> str:
    del dry_run
    if status == "skipped":
        return EXECUTION_COMPLETED
    if status == "blocked":
        return EXECUTION_FAILED
    if status == "failed" and not has_result:
        return EXECUTION_FAILED
    return EXECUTION_COMPLETED


def step_service_result_status(*, ok: bool, status: str) -> str:
    if status == "skipped" and ok:
        return SERVICE_SUCCEEDED
    if ok:
        return SERVICE_SUCCEEDED
    return SERVICE_FAILED


def workflow_aggregate_statuses(
    *,
    ok: bool,
    steps: list[dict[str, Any]],
    pending_approval: list[str] | None = None,
    dry_run: bool = False,
) -> tuple[str, str, str]:
    del dry_run
    if pending_approval:
        return WORKFLOW_FAILED, EXECUTION_FAILED, SERVICE_FAILED
    service_failed = any(
        step.get("service_result_status") == SERVICE_FAILED
        or (not step.get("ok", True) and step.get("status") not in {"skipped"})
        for step in steps
    )
    execution_failed = any(step.get("execution_status") == EXECUTION_FAILED for step in steps)
    if ok and not service_failed:
        return WORKFLOW_COMPLETED, EXECUTION_COMPLETED, SERVICE_SUCCEEDED
    if execution_failed or pending_approval:
        workflow_status = WORKFLOW_FAILED
    elif service_failed:
        workflow_status = WORKFLOW_COMPLETED_WITH_SERVICE_ERROR
    else:
        workflow_status = WORKFLOW_COMPLETED if ok else WORKFLOW_FAILED
    execution_status = EXECUTION_FAILED if execution_failed else EXECUTION_COMPLETED
    service_result_status = SERVICE_FAILED if service_failed or not ok else SERVICE_SUCCEEDED
    return workflow_status, execution_status, service_result_status


def enrich_step_dict(step: dict[str, Any], *, dry_run: bool = False) -> dict[str, Any]:
    status = str(step.get("status") or "completed")
    ok = bool(step.get("ok", True))
    execution_status = step_execution_status(
        status=status,
        has_result=bool(step.get("result")),
        dry_run=dry_run,
    )
    service_result_status = step_service_result_status(ok=ok, status=status)
    payload = dict(step)
    payload["execution_status"] = execution_status
    payload["service_result_status"] = service_result_status
    result = dict(payload.get("result") or {})
    if result:
        workflow_status, _, _ = derive_statuses(ok and service_result_status == SERVICE_SUCCEEDED)
        result.setdefault("workflow_status", workflow_status)
        result.setdefault("execution_status", execution_status)
        result.setdefault("service_result_status", service_result_status)
        payload["result"] = result
    return payload


def enrich_workflow_dict(payload: dict[str, Any], *, dry_run: bool = False) -> dict[str, Any]:
    body = dict(payload)
    steps = [enrich_step_dict(step, dry_run=dry_run) for step in body.get("steps") or []]
    body["steps"] = steps
    workflow_result = dict(body.get("workflow_result") or {})
    wf_status, ex_status, svc_status = workflow_aggregate_statuses(
        ok=bool(workflow_result.get("ok", False)),
        steps=steps,
        pending_approval=list(workflow_result.get("pending_approval") or []),
        dry_run=dry_run,
    )
    workflow_result["workflow_status"] = wf_status
    workflow_result["execution_status"] = ex_status
    workflow_result["service_result_status"] = svc_status
    failed_nodes = [
        str(step.get("id"))
        for step in steps
        if not bool(step.get("ok", True)) and step.get("status") != "skipped"
    ]
    if failed_nodes:
        workflow_result["failed_nodes"] = failed_nodes
        workflow_result["errors"] = [
            normalize_error(
                {
                    "code": _workflow_step_error_code(step),
                    "source": str(step.get("uri") or ""),
                    "recoverable": step.get("status") == "blocked",
                    "detail": _workflow_step_error_detail(step),
                }
            ).to_dict()
            for step in steps
            if str(step.get("id")) in failed_nodes
        ]
    body["workflow_result"] = workflow_result
    return body


def _workflow_step_error_code(step: dict[str, Any]) -> str:
    if step.get("status") == "blocked":
        return "STEP_BLOCKED"
    if step.get("execution_status") == EXECUTION_FAILED:
        return "STEP_EXECUTION_FAILED"
    return "STEP_SERVICE_FAILED"


def _workflow_step_error_detail(step: dict[str, Any]) -> str:
    result = step.get("result") or {}
    if isinstance(result, dict) and result.get("error"):
        return str(result["error"])
    if step.get("error"):
        return str(step["error"])
    return f"step {step.get('id')} failed"


_LIFECYCLE_OK_STATUSES = frozenset(
    {"running", "stopped", "deployed", "verified", "healthy", "generated"}
)


def enrich_lifecycle_dict(payload: dict[str, Any]) -> dict[str, Any]:
    body = dict(payload)
    if all(key in body for key in ("workflow_status", "execution_status", "service_result_status")):
        return body

    status = str(body.get("status") or "")
    runtime_state = body.get("runtime_state")
    runtime_status = str(body.get("runtime_status") or "")
    if isinstance(runtime_state, dict) and runtime_state.get("status"):
        runtime_status = str(runtime_state["status"])

    if (
        (body.get("command_string") and not status)
        or status in _LIFECYCLE_OK_STATUSES
        or runtime_status == "running"
    ):
        ok = True
    elif "ok" in body:
        ok = bool(body["ok"])
    else:
        ok = status not in {"failed", "error"} and status != ""

    workflow_status, execution_status, service_result_status = derive_statuses(ok)
    body["ok"] = ok
    body["workflow_status"] = workflow_status
    body["execution_status"] = execution_status
    body["service_result_status"] = service_result_status
    body.setdefault("result_type", "lifecycle")
    return body
