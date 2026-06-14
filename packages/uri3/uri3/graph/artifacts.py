from __future__ import annotations

import json
from pathlib import Path

from uri3.graph.execution_models import ExecutionContext


def artifact_path(context: ExecutionContext, step_id: str, suffix: str) -> Path:
    return (
        context.root
        / "output"
        / "artifacts"
        / "workflows"
        / context.workflow_id
        / context.run_id
        / step_id
        / suffix
    )


def artifact_uri(context: ExecutionContext, step_id: str, suffix: str) -> str:
    return f"artifact://operator/workflows/{context.workflow_id}/{context.run_id}/{step_id}/{suffix}"


def write_artifact(context: ExecutionContext, step_id: str, suffix: str, content: bytes | str) -> tuple[Path, str]:
    path = artifact_path(context, step_id, suffix)
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, str):
        path.write_text(content, encoding="utf-8")
    else:
        path.write_bytes(content)
    return path, artifact_uri(context, step_id, suffix)
