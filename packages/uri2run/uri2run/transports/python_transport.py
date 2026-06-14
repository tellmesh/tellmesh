from __future__ import annotations

import importlib
from typing import Any

from uri3.results import ServiceResult

from uri2run.result import error_result, result_from_output


def split_python_uri(uri: str) -> tuple[str, str]:
    if not uri.startswith("python://"):
        raise ValueError(f"Expected python:// URI, got {uri}")
    ref = uri.removeprefix("python://")
    if ":" not in ref:
        raise ValueError("python backend target must be python://module:function")
    module, func = ref.split(":", 1)
    return module, func


def run_python(target: str, payload: dict[str, Any], context: dict[str, Any]) -> ServiceResult:
    try:
        module_name, func_name = split_python_uri(target)
        module = importlib.import_module(module_name)
        func = getattr(module, func_name)
        output = func(payload, context) if callable(func) else func
    except Exception as exc:
        return error_result("PYTHON_TRANSPORT_FAILED", str(exc))
    return result_from_output(output)


def run_python_transport(
    backend: dict[str, Any],
    payload: dict[str, Any],
    context: dict[str, Any],
) -> ServiceResult:
    target = backend.get("target")
    if not target:
        return error_result("BACKEND_INVALID", "python backend missing target")
    return run_python(str(target), payload, context)
