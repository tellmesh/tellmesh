from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from hypervisor.deployment_registry.loader import load_deployment_registry
from hypervisor.paths import find_repo_root
from hypervisor.routing.explain import explain_executable_uri
from hypervisor.routing.system_dispatch import (
    call_hypervisor_system_uri,
    supports_hypervisor_system_uri,
)
from hypervisor.routing.system_request import uri_path_parts
from hypervisor.routing.view_handlers import (
    ViewEnvelope,
    handle_view_uri,
    resolve_view_envelope,
    supports_view_uri,
)

# Register Jinja renderer for process views.
from hypervisor_dashboard_agent import view_builder as _view_builder  # noqa: F401


@dataclass(frozen=True)
class _SystemUriRequest:
    uri: str
    repo: Path
    approved: bool
    dry_run: bool
    payload: dict[str, Any] | None
    scheme: str
    parts: list[str]
    artifact_root: Path | None = None


_SystemUriHandler = Callable[[_SystemUriRequest], dict[str, Any]]


def _repo_root(root: Path | None = None) -> Path:
    return root or find_repo_root()


def uri_implies_dry_run(uri: str) -> bool:
    """True when the URI path ends with a dry-run segment (e.g. workflow://…/dry-run)."""
    parts = uri_path_parts(uri)
    return bool(parts) and parts[-1] == "dry-run"


def list_agent_deployments(*, root: Path | None = None) -> list[dict[str, Any]]:
    registry = load_deployment_registry(root=_repo_root(root))
    items: list[dict[str, Any]] = []
    for deployment in registry.deployments:
        items.append(
            {
                "id": deployment.id,
                "agent_ref": deployment.agent_ref,
                "target_uri": deployment.target_uri,
                "status": deployment.status,
                "health_uri": deployment.health_uri,
                "view_uri": f"view://process/agent/{deployment.id}/latest",
            }
        )
    return items


def resolve_view_uri(view_uri: str, *, root: Path | None = None) -> ViewEnvelope:
    return resolve_view_envelope(view_uri, root=_repo_root(root))


def _is_presentation_request(request: _SystemUriRequest) -> bool:
    return request.scheme in {"html", "markdown"}


def _html_request(request: _SystemUriRequest) -> dict[str, Any]:
    from hypervisor_dashboard_agent.presentation import resolve_html_presentation

    return resolve_html_presentation(request.uri, root=request.repo)


def _markdown_request(request: _SystemUriRequest) -> dict[str, Any]:
    from hypervisor_dashboard_agent.presentation import resolve_markdown_presentation

    return resolve_markdown_presentation(request.uri, root=request.repo)


def _is_touri_run_request(request: _SystemUriRequest) -> bool:
    return request.scheme in {"workflow", "flow", "cron"}


def _touri_run_request(request: _SystemUriRequest) -> dict[str, Any]:
    from urish.backends.run import run_target

    effective_dry_run = request.dry_run or uri_implies_dry_run(request.uri)
    approve = request.approved and not effective_dry_run
    return run_target(
        request.uri,
        approve=approve,
        dry_run=effective_dry_run,
        adapter="mock",
        payload=request.payload,
        artifact_root=request.artifact_root or request.repo,
    )


def _is_http_request(request: _SystemUriRequest) -> bool:
    return request.scheme in {"http", "https"}


_OPERATOR_SCHEMES = frozenset(
    {"browser", "dom", "screen", "input", "android", "pcwin", "robot", "device"}
)


def _infer_operator_operation(parts: list[str]) -> str:
    if not parts:
        return "call"
    if parts[-1] == "dry-run" and len(parts) > 1:
        return parts[-2]
    if "mission" in parts and parts[-1] == "start":
        return "mission_start"
    return parts[-1]


def _is_operator_request(request: _SystemUriRequest) -> bool:
    return request.scheme in _OPERATOR_SCHEMES


def explain_system_uri(
    uri: str,
    *,
    root: Path | None = None,
    approved: bool = False,
    dry_run: bool = False,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return explain_executable_uri(
        uri,
        root=_repo_root(root),
        approved=approved,
        dry_run=dry_run,
        payload=payload,
    )


def _operator_request(request: _SystemUriRequest) -> dict[str, Any]:
    effective_dry_run = request.dry_run or uri_implies_dry_run(request.uri)
    payload = dict(request.payload or {})
    payload.setdefault("adapter", "mock")
    operation = _infer_operator_operation(request.parts)
    if request.scheme == "browser" and operation == "open" and "url" not in payload:
        payload.setdefault("url", "https://supplier-portal.example.local/reports/monthly")
    if effective_dry_run:
        explain = explain_system_uri(
            request.uri,
            root=request.repo,
            approved=request.approved,
            dry_run=True,
            payload=payload,
        )
        return {
            "ok": True,
            "result_type": "plan",
            "workflow_status": "planned",
            "service_result_status": "preview",
            "uri": request.uri,
            "dry_run": True,
            "explain": explain.get("explain", explain),
            "hypervisor_resolution": explain.get("hypervisor_resolution"),
        }

    from hypervisor.routing import call_uri as hypervisor_call_uri

    result = hypervisor_call_uri(
        request.uri,
        payload,
        root=request.repo,
        approved=request.approved,
    )
    body = result.to_dict()
    body.setdefault("result_type", "operator")
    body.setdefault("uri", request.uri)
    return body


def _is_chat_request(request: _SystemUriRequest) -> bool:
    return (
        request.scheme == "chat"
        and bool(request.parts)
        and request.parts[-1] == "prompt"
    )


def _chat_request(request: _SystemUriRequest) -> dict[str, Any]:
    from urish.chat_uri import execute_chat_prompt_uri

    return execute_chat_prompt_uri(
        request.uri,
        dry_run=request.dry_run,
        use_llm=False,
        payload=request.payload,
    )


def _is_nl_request(request: _SystemUriRequest) -> bool:
    return request.scheme == "nl"


def _nl_request(request: _SystemUriRequest) -> dict[str, Any]:
    from urish.nl_uri import execute_nl_uri

    return execute_nl_uri(
        request.uri,
        dry_run=request.dry_run,
        use_llm=False,
        payload=request.payload,
    )


def _http_request(request: _SystemUriRequest) -> dict[str, Any]:
    import httpx

    try:
        response = httpx.get(request.uri, timeout=15.0, follow_redirects=True)
    except httpx.HTTPError as exc:
        return {
            "ok": False,
            "result_type": "http",
            "workflow_status": "completed_with_service_error",
            "service_result_status": "failed",
            "uri": request.uri,
            "error": str(exc),
        }
    payload: Any
    json_ok = False
    try:
        payload = response.json()
        json_ok = isinstance(payload, dict)
    except Exception:
        payload = response.text[:2000]
    return {
        "ok": response.is_success,
        "result_type": "http",
        "workflow_status": "completed",
        "service_result_status": "succeeded" if response.is_success else "failed",
        "uri": request.uri,
        "status_code": response.status_code,
        "json_ok": json_ok,
        "payload": payload,
    }


def _presentation_request(request: _SystemUriRequest) -> dict[str, Any]:
    if request.scheme == "html":
        return _html_request(request)
    return _markdown_request(request)


_DASHBOARD_URI_DISPATCH: tuple[tuple[Callable[[_SystemUriRequest], bool], _SystemUriHandler], ...] = (
    (_is_presentation_request, _presentation_request),
    (_is_touri_run_request, _touri_run_request),
    (_is_nl_request, _nl_request),
    (_is_chat_request, _chat_request),
    (_is_operator_request, _operator_request),
    (_is_http_request, _http_request),
)


def _select_dashboard_uri_handler(request: _SystemUriRequest) -> _SystemUriHandler | None:
    for matches, handler in _DASHBOARD_URI_DISPATCH:
        if matches(request):
            return handler
    return None


def call_system_uri(
    uri: str,
    *,
    root: Path | None = None,
    artifact_root: Path | None = None,
    approved: bool = False,
    dry_run: bool = False,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    repo = _repo_root(root)
    if supports_view_uri(uri):
        return handle_view_uri(
            uri,
            repo=repo,
            approved=approved,
            dry_run=dry_run,
            payload=payload,
            system_uri_handler=call_hypervisor_system_uri,
        )
    if supports_hypervisor_system_uri(uri):
        return call_hypervisor_system_uri(
            uri,
            root=repo,
            artifact_root=artifact_root,
            approved=approved,
            dry_run=dry_run,
            payload=payload,
        )

    parsed = urlparse(uri)
    request = _SystemUriRequest(
        uri=uri,
        repo=repo,
        approved=approved,
        dry_run=dry_run,
        payload=payload,
        scheme=parsed.scheme,
        parts=uri_path_parts(uri),
        artifact_root=artifact_root,
    )
    handler = _select_dashboard_uri_handler(request)
    if handler:
        return handler(request)

    if dry_run:
        return {
            "ok": True,
            "result_type": "dry_run",
            "uri": uri,
            "payload": payload or {},
            "status": "preview",
            "service_result_status": "preview",
            "workflow_status": "planned",
        }

    raise ValueError(f"unsupported or unimplemented URI: {uri}")
