from __future__ import annotations

from pathlib import Path
from typing import Any

from touri.models import ServiceResult, service_result
from uri2flow import expand_flow
from uri3.graph import build_execution_plan, dry_run_workflow, load_workflow_graph, run_workflow, validate_workflow_graph


def _resolve_path(path: str, context: dict[str, Any]) -> Path:
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    root = context.get("root")
    if root:
        return Path(root) / candidate
    from uri3.config.repo_root import find_repo_root

    return find_repo_root() / candidate


def _execution_options(payload: dict[str, Any], backend_extra: dict[str, Any]) -> dict[str, Any]:
    return {
        "dry_run": bool(payload.get("dry_run", backend_extra.get("dry_run", True))),
        "approve": bool(payload.get("approve", backend_extra.get("approve", False))),
        "browser": str(payload.get("browser", backend_extra.get("browser", "mock"))),
    }


def call_uri_flow_backend(
    flow_path: str,
    payload: dict[str, Any],
    context: dict[str, Any],
    *,
    backend_extra: dict[str, Any] | None = None,
) -> ServiceResult:
    extra = backend_extra or {}
    path = _resolve_path(flow_path, context)
    if not path.is_file():
        return service_result(
            ok=False,
            result_type="error",
            errors=[{"code": "FLOW_NOT_FOUND", "detail": f"Flow file not found: {path}"}],
        )

    options = _execution_options(payload, extra)
    try:
        graph = expand_flow(path)
    except Exception as exc:
        return service_result(
            ok=False,
            result_type="error",
            errors=[{"code": "FLOW_EXPAND_FAILED", "detail": str(exc)}],
        )

    errors = validate_workflow_graph(graph)
    if errors:
        return service_result(
            ok=False,
            result_type="error",
            errors=[{"code": "FLOW_INVALID", "detail": "; ".join(errors[:5])}],
        )

    workflow = load_workflow_graph(graph)
    root = path.parent if path.parent.is_dir() else _resolve_path(".", context).parent

    if options["dry_run"]:
        simulation = dry_run_workflow(workflow)
        data = {
            "flow": str(path),
            "plan": build_execution_plan(workflow),
            "simulation": simulation,
        }
        ok = bool((simulation.get("workflow_result") or {}).get("ok", True))
        return service_result(ok=ok, result_type="plan", data=data)

    result = run_workflow(
        workflow,
        approve=options["approve"],
        dry_run=False,
        browser_mode=options["browser"],
        root=root,
    )
    body = result.to_dict()
    ok = bool((body.get("workflow_result") or {}).get("ok", False))
    return service_result(ok=ok, result_type="workflow", data=body)
