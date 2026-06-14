from __future__ import annotations

import json
import subprocess
from typing import Any

from uri3.results import ServiceResult

from uri2run.result import error_result, result_from_output


def run_stdio(command: str, payload: dict[str, Any], context: dict[str, Any]) -> ServiceResult:
    timeout = payload.get("timeout", context.get("timeout"))
    try:
        completed = subprocess.run(
            command,
            shell=True,
            input=json.dumps(payload, ensure_ascii=False),
            text=True,
            capture_output=True,
            check=False,
            timeout=float(timeout) if timeout is not None else None,
        )
    except subprocess.TimeoutExpired as exc:
        return error_result("STDIO_TIMEOUT", str(exc), result_type="stdio")
    if completed.returncode != 0:
        return error_result(
            "STDIO_FAILED",
            completed.stderr or f"exit code {completed.returncode}",
            result_type="stdio",
        )
    stdout = completed.stdout.strip()
    if not stdout:
        return service_result_ok({"stdout": "", "stderr": completed.stderr})
    try:
        parsed = json.loads(stdout)
    except json.JSONDecodeError:
        return service_result_ok({"stdout": stdout, "stderr": completed.stderr})
    return result_from_output(parsed)


def service_result_ok(data: Any) -> ServiceResult:
    from uri3.results import service_result

    return service_result(ok=True, result_type="stdio", data=data, meta={"transport": "stdio"})


def run_stdio_transport(
    backend: dict[str, Any],
    payload: dict[str, Any],
    context: dict[str, Any],
) -> ServiceResult:
    command = backend.get("command") or backend.get("target")
    if not command:
        return error_result("BACKEND_INVALID", "stdio backend missing command")
    return run_stdio(str(command), payload, context)
