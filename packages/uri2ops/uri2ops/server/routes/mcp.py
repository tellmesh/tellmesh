from __future__ import annotations

from fastapi import APIRouter, HTTPException

from uri2ops.operation_registry.dispatcher import dispatch
from uri2ops.server.mcp_wrapper import list_mcp_tools, mcp_tool_name_for_operation
from uri2ops.server.routes.health import McpToolCallRequest, TaskRequest
from uri2ops.server.routes.tasks import run_task_handler
from uri2ops.server.service import OperatorService


def mcp_router(service: OperatorService) -> APIRouter:
    router = APIRouter()

    @router.get("/mcp/tools")
    def mcp_tools() -> dict:
        return {"tools": list_mcp_tools(service.registry())}

    @router.post("/mcp/tools/call")
    def mcp_tools_call(body: McpToolCallRequest) -> dict:
        if body.name == "run_operator_task":
            task = body.arguments.get("task")
            if not isinstance(task, dict):
                raise HTTPException(status_code=400, detail="arguments.task must be an object")
            return run_task_handler(
                service,
                TaskRequest(
                    task=task,
                    dry_run=bool(body.arguments.get("dry_run")),
                    approve=bool(body.arguments.get("approve")),
                    adapter=str(body.arguments.get("adapter") or "mock"),
                ),
            )

        registry = service.registry()
        for spec in registry.list():
            if mcp_tool_name_for_operation(spec.scheme, spec.operation) != body.name:
                continue
            uri = str(body.arguments.get("uri") or f"{spec.scheme}://local/{spec.operation}")
            payload = dict(body.arguments.get("payload") or {})
            payload.setdefault("target_uri", uri)
            context = {
                "adapter": str(body.arguments.get("adapter") or "mock"),
                "task_id": "mcp-call",
                "run_id": body.name,
                "root": str(service.root),
                "session": {},
            }
            if spec.requires_policy and not body.arguments.get("approve"):
                raise HTTPException(status_code=403, detail=f"{body.name} requires approve=true")
            try:
                return dispatch(spec.scheme, spec.operation, payload, context)
            except Exception as exc:
                raise HTTPException(status_code=500, detail=str(exc)) from exc
        raise HTTPException(status_code=404, detail=f"Unknown MCP tool: {body.name}")

    return router
