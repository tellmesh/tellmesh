from __future__ import annotations

from pathlib import Path
from typing import Any

from jinja2 import Environment, PackageLoader, select_autoescape

from hypervisor.routing.views.process import build_process_view_data

from hypervisor_dashboard_agent.models import ProcessViewModel, UriAction

_env = Environment(
    loader=PackageLoader("hypervisor_dashboard_agent", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
)


def _process_model_from_data(data: dict[str, Any]) -> ProcessViewModel:
    actions = [
        UriAction(
            str(item.get("label") or ""),
            str(item.get("uri") or ""),
            bool(item.get("requires_approval")),
            str(item.get("kind") or "read"),
        )
        for item in data.get("actions") or []
        if isinstance(item, dict)
    ]
    return ProcessViewModel(
        agent_id=str(data["agent_id"]),
        agent_ref=str(data["agent_ref"]),
        title=str(data["title"]),
        service_status=str(data["service_status"]),
        deployment_status=str(data["deployment_status"]),
        process_status=str(data["process_status"]),
        health_status=str(data["health_status"]),
        recommended_action=str(data["recommended_action"]),
        effective_health_uri=data.get("effective_health_uri"),
        effective_port=data.get("effective_port"),
        incidents=list(data.get("incidents") or []),
        warnings=list(data.get("warnings") or []),
        readiness=dict(data.get("readiness") or {}),
        related_uris=dict(data.get("related_uris") or {}),
        actions=actions,
        inspection=dict(data.get("inspection") or {}),
    )


def build_process_view(agent_id: str, *, root: Path | None = None) -> ProcessViewModel:
    return _process_model_from_data(build_process_view_data(agent_id, root=root))


def render_process_html(model: ProcessViewModel) -> str:
    template = _env.get_template("process.html")
    return template.render(model=model, view=model.to_dict())


def _dashboard_view_renderer(view_uri: str, data: dict[str, Any]) -> str | None:
    if data.get("view_kind") != "process":
        return None
    return render_process_html(_process_model_from_data(data))


def register_dashboard_view_renderer() -> None:
    from hypervisor.routing.view_handlers import register_view_renderer

    register_view_renderer(_dashboard_view_renderer)


register_dashboard_view_renderer()
