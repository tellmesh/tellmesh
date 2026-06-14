from __future__ import annotations

import re
from typing import Any

from uri3.graph.graph_validator import validate_workflow_graph
from uri3.graph.operation_registry import (
    DEFAULT_KIND_BY_SCHEME,
    OPERATIONS_BY_SCHEME,
    allowed_operations,
    scheme_from_uri,
    validate_node_operation,
)
from uri3.graph.graph_serializer import normalize_graph_payload, task_steps_to_graph

OPERATION_ALIASES: dict[str, dict[str, str]] = {
    "browser": {"open_page": "open", "navigate": "open", "goto": "open", "screenshot": "capture"},
    "dom": {"get": "read", "extract_text": "read", "text": "read"},
    "screen": {"screenshot": "capture", "shot": "capture"},
    "assertion": {"contains": "check", "equals": "check", "match": "check", "verify": "check"},
    "hypervisor": {"command": "run", "deploy": "run", "start": "run", "stop": "restart"},
    "http": {"get": "read", "fetch": "read"},
    "https": {"get": "read", "fetch": "read"},
    "log": {"fetch": "read", "tail": "read"},
    "agent": {"query": "read", "info": "status"},
    "domain": {"create": "generate", "build": "generate"},
}


def _slug(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "task"


def _coerce_operation(scheme: str, operation: str) -> str:
    normalized = str(operation).strip().lower()
    aliases = OPERATION_ALIASES.get(scheme, {})
    if normalized in aliases:
        normalized = aliases[normalized]
    allowed = allowed_operations(scheme)
    if normalized in allowed:
        return normalized
    for candidate in ("read", "query", "check", "open", "run", "capture", "generate"):
        if candidate in allowed:
            return candidate
    return sorted(allowed)[0]


def extract_graph_payload(raw: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ValueError("LLM graph planner did not return a JSON object")
    if "nl2uri" in raw and isinstance(raw["nl2uri"], dict):
        raw = {key: value for key, value in raw.items() if key != "nl2uri"}
    if "graph" in raw and isinstance(raw["graph"], dict):
        return {"graph": raw["graph"]}
    if "task" in raw and "steps" in raw:
        return {"task": raw["task"], "steps": raw["steps"]}
    if "nodes" in raw:
        return {"graph": raw}
    if "steps" in raw and isinstance(raw["steps"], list):
        task = raw.get("task") if isinstance(raw.get("task"), dict) else {"id": "task"}
        return {"task": task, "steps": raw["steps"]}
    raise ValueError("LLM response missing graph or task/steps")


def normalize_to_kind(body: dict[str, Any], *, kind: str, prompt: str) -> dict[str, Any]:
    if kind == "workflow_graph" and "task" in body and "steps" in body:
        graph = task_steps_to_graph(body["task"], body["steps"])
        graph.kind = "workflow"
        if not graph.description:
            graph.description = prompt.strip()
        return {"graph": graph.to_dict()}
    if kind == "task_graph" and "graph" in body:
        graph_data = body["graph"]
        nodes = graph_data.get("nodes") or []
        if isinstance(nodes, dict):
            nodes = [dict(value, id=node_id) for node_id, value in nodes.items()]
        task = {
            "id": str(graph_data.get("id") or _slug(prompt[:80])),
            "description": str(graph_data.get("description") or prompt.strip()),
        }
        return {"task": task, "steps": list(nodes)}
    return body


def sanitize_node(node: dict[str, Any], *, warnings: list[str]) -> dict[str, Any] | None:
    node_id = str(node.get("id") or "").strip()
    uri = str(node.get("uri") or "").strip()
    if not node_id or not uri:
        warnings.append(f"dropped node with missing id or uri: {node!r}")
        return None
    scheme = scheme_from_uri(uri)
    if scheme not in OPERATIONS_BY_SCHEME:
        warnings.append(f"dropped node {node_id!r}: unsupported scheme {scheme!r}")
        return None
    operation = _coerce_operation(scheme, str(node.get("operation") or "read"))
    kind = node.get("kind") or DEFAULT_KIND_BY_SCHEME.get(scheme, "query")
    sanitized: dict[str, Any] = {
        "id": node_id,
        "uri": uri,
        "operation": operation,
        "kind": kind,
    }
    if node.get("type"):
        sanitized["type"] = node["type"]
    if isinstance(node.get("payload"), dict) and node["payload"]:
        sanitized["payload"] = dict(node["payload"])
    if node.get("condition"):
        sanitized["condition"] = node["condition"]
    if node.get("produces"):
        sanitized["produces"] = list(node["produces"])
    if node.get("emits"):
        sanitized["emits"] = list(node["emits"])
    if node.get("depends_on"):
        sanitized["depends_on"] = [str(item) for item in node["depends_on"]]
    return sanitized


def _sanitize_nodes(nodes: list[dict[str, Any]], *, warnings: list[str]) -> list[dict[str, Any]]:
    sanitized: list[dict[str, Any]] = []
    for node in nodes:
        item = sanitize_node(node, warnings=warnings)
        if item:
            sanitized.append(item)
    node_ids = {node["id"] for node in sanitized}
    for node in sanitized:
        deps = [dep for dep in node.get("depends_on") or [] if dep in node_ids]
        dropped = set(node.get("depends_on") or []) - set(deps)
        if dropped:
            warnings.append(f"{node['id']}: removed unknown depends_on {sorted(dropped)!r}")
        if deps:
            node["depends_on"] = deps
        elif "depends_on" in node:
            del node["depends_on"]
    return sanitized


def repair_graph_body(raw: dict[str, Any], prompt: str, *, kind: str) -> tuple[dict[str, Any], list[str]]:
    warnings: list[str] = []
    body = normalize_to_kind(extract_graph_payload(raw), kind=kind, prompt=prompt)
    if "graph" in body:
        graph_data = dict(body["graph"])
        nodes = graph_data.get("nodes") or []
        if isinstance(nodes, dict):
            nodes = [dict(value, id=node_id) for node_id, value in nodes.items()]
        graph_data["nodes"] = _sanitize_nodes(list(nodes), warnings=warnings)
        if not graph_data["nodes"]:
            raise ValueError("no valid nodes remain after repair")
        graph_data.setdefault("id", _slug(prompt[:80]))
        graph_data.setdefault("version", 1)
        graph_data.setdefault("kind", "workflow" if kind == "workflow_graph" else "task")
        graph_data.setdefault("description", prompt.strip())
        body = {"graph": graph_data}
    elif "task" in body and "steps" in body:
        task = dict(body["task"] or {})
        task.setdefault("id", _slug(prompt[:80]))
        task.setdefault("description", prompt.strip())
        steps = _sanitize_nodes(list(body["steps"] or []), warnings=warnings)
        if not steps:
            raise ValueError("no valid steps remain after repair")
        body = {"task": task, "steps": steps}
    else:
        raise ValueError("repaired body must contain graph or task/steps")
    return body, warnings


def repair_and_validate_graph(
    raw: dict[str, Any],
    prompt: str,
    *,
    kind: str,
    nl2uri_wrapper: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], list[str]]:
    body, warnings = repair_graph_body(raw, prompt, kind=kind)
    payload = dict(nl2uri_wrapper or {})
    payload.update(body)
    errors = validate_workflow_graph(payload)
    if errors:
        operation_errors = [error for error in errors if "operation" in error and "not allowed" in error]
        if operation_errors and "graph" in body:
            graph_data = dict(body["graph"])
            graph_data["nodes"] = [
                node
                for node in graph_data["nodes"]
                if validate_node_operation(normalize_graph_payload(graph_data).nodes[node["id"]]) is None
            ]
            if graph_data["nodes"]:
                body = {"graph": graph_data}
                payload = dict(nl2uri_wrapper or {})
                payload.update(body)
                errors = validate_workflow_graph(payload)
        if errors:
            raise ValueError("; ".join(errors[:5]))
    return body, warnings
