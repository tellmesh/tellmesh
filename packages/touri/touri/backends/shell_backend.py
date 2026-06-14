from __future__ import annotations

from typing import Any

from uri2run import run_backend
from uri3.results import ServiceResult


def call_shell_backend(
    command: str, payload: dict[str, Any], context: dict[str, Any]
) -> ServiceResult:
    return run_backend({"type": "shell", "command": command}, payload, context)
