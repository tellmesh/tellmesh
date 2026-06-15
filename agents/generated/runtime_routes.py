"""Shared HTTP/runtime helpers for generated thin agents."""

from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

from fastapi import HTTPException
from pydantic import BaseModel, Field
from runtime_client.client import ResourceRuntimeClient


class CommandRequest(BaseModel):
    command: str = Field(..., description="Runtime command name")
    payload: dict[str, Any] = Field(default_factory=dict)


def uri_allowed(uri: str, templates: list[str | None]) -> bool:
    for template in templates:
        if not template:
            continue
        prefix = template.split("{")[0]
        if uri.startswith(prefix):
            return True
    return False


def read_uri(client: ResourceRuntimeClient, uri: str) -> dict[str, Any]:
    scheme = urlparse(uri).scheme
    if scheme == "resource":
        return client.read_resource(uri)
    if scheme == "file":
        from uri3.resolvers.resolve_core import resolve

        resolved = resolve(uri)
        return {
            "ok": True,
            "uri": uri,
            "result_type": "file",
            "data": resolved.target,
        }
    from urish.backends.call import call_uri

    return call_uri(uri, {}, dry_run=False)


def command_uri(agent_card: dict[str, Any], command: str) -> str | None:
    for cap in agent_card["capabilities"]:
        if cap.get("type") == "command" and cap.get("command") == command:
            uri = cap.get("uri")
            return str(uri) if uri else None
    return None


def dispatch_command(
    client: ResourceRuntimeClient,
    command: str,
    payload: dict[str, Any],
    *,
    uri: str | None = None,
) -> dict[str, Any]:
    if uri:
        from urish.backends.call import call_uri

        return call_uri(uri, payload, dry_run=bool(payload.get("dry_run", False)))
    return client.dispatch_command(command, payload)


def assert_resource_allowed(agent_card: dict[str, Any], uri: str) -> None:
    allowed = [
        cap.get("uri")
        for cap in agent_card["capabilities"]
        if cap.get("type") == "resource_read"
    ]
    if not uri_allowed(uri, allowed):
        raise HTTPException(status_code=403, detail=f"URI not exposed by this agent: {uri}")


def assert_command_allowed(agent_card: dict[str, Any], command: str) -> None:
    allowed = [
        cap.get("command")
        for cap in agent_card["capabilities"]
        if cap.get("type") == "command"
    ]
    if command not in allowed:
        raise HTTPException(
            status_code=403,
            detail=f"Command not exposed by this agent: {command}",
        )
