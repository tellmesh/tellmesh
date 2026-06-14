from __future__ import annotations

import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from hypervisor.deployment_registry.env import default_log_uri, resolve_deployment_env
from hypervisor.deployment_registry.models import AgentDeployment
from hypervisor.deployment_registry.status import infer_port


def local_target_to_relative_path(target_uri: str) -> Path:
    parsed = urlparse(target_uri)
    if parsed.scheme != "local":
        raise ValueError(f"Only local:// targets can be started directly: {target_uri}")
    if parsed.netloc:
        return Path(f"{parsed.netloc}/{parsed.path.lstrip('/')}")
    return Path(parsed.path.lstrip("/"))


def local_target_to_module(target_uri: str) -> str:
    relative = local_target_to_relative_path(target_uri)
    parts = relative.parts
    if len(parts) >= 3 and parts[0] == "agents" and parts[1] == "generated":
        package = parts[2]
        return f"agents.generated.{package}.main:app"
    raise ValueError(f"Unsupported local agent path: {target_uri}")


def build_local_run_plan(
    deployment: AgentDeployment,
    *,
    repo: Path,
    port: int | None = None,
    host: str = "0.0.0.0",
    reload: bool = False,
) -> dict[str, Any]:
    chosen_port = port or infer_port(deployment)
    module = local_target_to_module(deployment.target_uri)
    agent_path = repo / local_target_to_relative_path(deployment.target_uri)
    if not agent_path.exists():
        raise FileNotFoundError(f"Generated agent path not found: {agent_path}")
    command = [
        sys.executable,
        "-m",
        "uvicorn",
        module,
        "--host",
        host,
        "--port",
        str(chosen_port),
    ]
    if reload:
        command.append("--reload")
    health_uri = deployment.health_uri or f"http://localhost:{chosen_port}/health"
    display_env = resolve_deployment_env(
        deployment.id, deployment.agent_ref, deployment.env, root=repo, resolve_secrets=False
    )
    return {
        "deployment_id": deployment.id,
        "agent_ref": deployment.agent_ref,
        "target_uri": deployment.target_uri,
        "module": module,
        "path": str(agent_path),
        "host": host,
        "port": chosen_port,
        "health_uri": health_uri,
        "card_uri": deployment.card_uri or f"http://localhost:{chosen_port}/.well-known/agent-card.json",
        "command": command,
        "command_string": " ".join(command),
        "env": display_env,
        "log_uri": default_log_uri(deployment.id, deployment.agent_ref, root=repo),
        "runtime_state_path": str((repo / "output" / "runtime" / "agents" / deployment.id / "state.json")),
    }
