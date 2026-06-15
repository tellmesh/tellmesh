from __future__ import annotations

from hypervisor.routing.explain import explain_executable_uri
from hypervisor.routing.view_handlers import resolve_view_envelope


def test_explain_executable_uri_operator_includes_resolution(repo_root):
    result = explain_executable_uri(
        "browser://chrome/page/open",
        root=repo_root,
        payload={"url": "https://example.com", "environment": "mock"},
    )

    assert result["canonical_uri"] == "tellmesh://operators/browser/command/open"
    assert result["hypervisor_resolution"]["agent_uri"] == "agent://browser-operator"
    assert result.get("semantic_route") is not None


def test_resolve_view_envelope_process_without_renderer(repo_root):
    from hypervisor.routing.view_handlers import register_view_renderer

    register_view_renderer(None)
    envelope = resolve_view_envelope(
        "view://process/agent/user-agent.local/latest",
        root=repo_root,
        renderer=None,
    )

    assert envelope.content_type == "text/html"
    assert envelope.data["agent_id"] == "user-agent.local"
    assert envelope.html is None
