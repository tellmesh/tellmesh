from __future__ import annotations

from pathlib import Path

from hypervisor.deployment_registry.loader import load_deployment_registry
from hypervisor.deployment_registry.models import AgentDeployment


def resolve_deployment(
    selector: str,
    *,
    root: str | Path = ".",
) -> AgentDeployment:
    registry = load_deployment_registry(root)
    deployment = registry.by_id(selector)
    if deployment is None:
        matches = registry.by_agent_ref(selector if selector.startswith("agent://") else f"agent://{selector}")
        if len(matches) == 1:
            deployment = matches[0]
        elif len(matches) > 1:
            ids = ", ".join(item.id for item in matches)
            raise ValueError(f"Ambiguous agent selector {selector!r}; choose deployment id: {ids}")
    if deployment is None:
        raise ValueError(f"Deployment not found: {selector}")
    return deployment
