from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any


def start_process(
    plan: dict[str, Any],
    *,
    root: Path,
    detach: bool,
    runtime_env: dict[str, str] | None = None,
) -> subprocess.Popen[Any] | None:
    env = os.environ.copy()
    env.update(runtime_env or plan.get("env") or {})
    cwd = str(root)
    command = plan["command"]
    if detach:
        return subprocess.Popen(
            command,
            cwd=cwd,
            env=env,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    subprocess.run(command, check=True, cwd=cwd, env=env)
    return None
