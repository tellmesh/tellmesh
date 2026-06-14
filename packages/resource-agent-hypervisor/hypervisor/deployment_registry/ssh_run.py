from __future__ import annotations

import shlex
import sys
from pathlib import Path
from typing import Any

from hypervisor.deployment_registry.env import resolve_deployment_env
from hypervisor.deployment_registry.ssh_helpers import remote_module_for
from hypervisor.deployment_registry.status import infer_port
from hypervisor.paths import find_repo_root
from uri3.resolvers.ssh_resolver import parse_ssh_uri


def build_ssh_run_plan(
    deployment,
    *,
    root: Path | None = None,
    port: int | None = None,
    host: str = "0.0.0.0",
) -> dict[str, Any]:
    repo = root or find_repo_root()
    ssh_ref = parse_ssh_uri(deployment.target_uri)
    chosen_port = port or infer_port(deployment)
    remote_path = ssh_ref["path"]
    module = remote_module_for(deployment)
    display_env = resolve_deployment_env(
        deployment.id, deployment.agent_ref, deployment.env, root=repo, resolve_secrets=False
    )
    env_prefix = " ".join(f"{key}={shlex.quote(value)}" for key, value in display_env.items())
    remote_command = (
        f"cd {shlex.quote(remote_path)} && "
        f"{env_prefix + ' ' if env_prefix else ''}"
        f"{shlex.quote(sys.executable)} -m uvicorn {module} "
        f"--host {shlex.quote(host)} --port {chosen_port}"
    )
    from uri3.resolvers.ssh_resolver import build_ssh_command

    command = build_ssh_command(ssh_ref, remote_command)
    health_uri = deployment.health_uri or f"http://{ssh_ref['host']}:{chosen_port}/health"
    return {
        "deployment_id": deployment.id,
        "agent_ref": deployment.agent_ref,
        "target_uri": deployment.target_uri,
        "transport": "ssh",
        "ssh": ssh_ref,
        "remote_path": remote_path,
        "module": module,
        "host": host,
        "port": chosen_port,
        "health_uri": health_uri,
        "card_uri": deployment.card_uri or f"http://{ssh_ref['host']}:{chosen_port}/.well-known/agent-card.json",
        "remote_command": remote_command,
        "command": command,
        "command_string": " ".join(command),
        "env": display_env,
        "hint": "Remote start is dry-run only in v0.6; deploy first, then run manually or via future remote detach.",
    }
