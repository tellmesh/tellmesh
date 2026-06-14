from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from uri2ops import __version__


class TaskRequest(BaseModel):
    task: dict[str, Any]
    dry_run: bool = False
    approve: bool = False
    adapter: str = "mock"


class McpToolCallRequest(BaseModel):
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


def health_router() -> APIRouter:
    router = APIRouter()

    @router.get("/health")
    def health() -> dict[str, Any]:
        return {"ok": True, "service": "uri2ops", "version": __version__}

    return router
