from __future__ import annotations

import os
import shlex
import subprocess
from typing import Any

from uri3.results import ServiceResult, service_result

from uri2run.result import error_result


def _command_with_args(command: str, payload: dict[str, Any]) -> str:
    args = payload.get("args")
    if not isinstance(args, list):
        return command
    suffix = " ".join(shlex.quote(str(arg)) for arg in args)
    return f"{command} {suffix}".strip()


def _extra_args(payload: dict[str, Any]) -> list[str]:
    args = payload.get("args")
    if not isinstance(args, list):
        return []
    return [str(arg) for arg in args]


def _argv(command: str, payload: dict[str, Any]) -> list[str]:
    raw_argv = payload.get("argv")
    if isinstance(raw_argv, list) and raw_argv:
        return [str(arg) for arg in raw_argv] + _extra_args(payload)
    return shlex.split(command) + _extra_args(payload)


def _env(payload: dict[str, Any], context: dict[str, Any]) -> dict[str, str] | None:
    raw_env = payload.get("env", context.get("env"))
    if not isinstance(raw_env, dict):
        return None
    env = dict(os.environ)
    env.update({str(key): str(value) for key, value in raw_env.items()})
    return env


def run_shell(command: str, payload: dict[str, Any], context: dict[str, Any]) -> ServiceResult:
    timeout = payload.get("timeout", context.get("timeout"))
    shell = bool(payload.get("shell", "argv" not in payload))
    command_or_argv: str | list[str]
    command_or_argv = _command_with_args(command, payload) if shell else _argv(command, payload)

    try:
        completed = subprocess.run(
            command_or_argv,
            shell=shell,
            text=True,
            capture_output=True,
            check=False,
            timeout=float(timeout) if timeout is not None else None,
            cwd=payload.get("cwd", context.get("cwd")),
            env=_env(payload, context),
            input=payload.get("input"),
        )
    except subprocess.TimeoutExpired as exc:
        return error_result("SHELL_TIMEOUT", str(exc), result_type="shell")
    except OSError as exc:
        return error_result("SHELL_EXEC_FAILED", str(exc), result_type="shell")
    return service_result(
        ok=completed.returncode == 0,
        result_type="shell",
        data={
            "stdout": completed.stdout,
            "stderr": completed.stderr,
            "returncode": completed.returncode,
        },
        meta={"transport": "shell", "shell": shell},
    )


def run_shell_transport(
    backend: dict[str, Any],
    payload: dict[str, Any],
    context: dict[str, Any],
) -> ServiceResult:
    command = backend.get("command") or backend.get("target")
    if not command:
        return error_result("BACKEND_INVALID", "shell backend missing command")
    return run_shell(str(command), {**backend, **payload}, context)
