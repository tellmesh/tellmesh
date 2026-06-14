from __future__ import annotations

from hypervisor.contract_registry.models import ContractRegistry


def validate_resource_read_capability(registry: ContractRegistry, cap) -> list[str]:
    label = f"{cap.agent}.{cap.name}"
    if not cap.uri:
        return [f"{label}: resource_read requires uri"]
    resource = registry.resource_by_uri(cap.uri)
    if not resource:
        return [f"{label}: references unknown uri {cap.uri}"]
    errors: list[str] = []
    if cap.output_schema and cap.output_schema != resource.schema:
        errors.append(f"{label}: output_schema {cap.output_schema} != resource schema {resource.schema}")
    if cap.renderer and cap.renderer != resource.renderer:
        errors.append(f"{label}: renderer {cap.renderer} != resource renderer {resource.renderer}")
    return errors


def validate_command_capability(cap) -> list[str]:
    label = f"{cap.agent}.{cap.name}"
    errors: list[str] = []
    if not cap.command:
        errors.append(f"{label}: command capability requires command")
    if not cap.input_schema:
        errors.append(f"{label}: command capability requires input_schema")
    return errors


def validate_capabilities(registry: ContractRegistry) -> list[str]:
    errors: list[str] = []
    for cap in registry.capabilities:
        if cap.type == "resource_read":
            errors.extend(validate_resource_read_capability(registry, cap))
        elif cap.type == "command":
            errors.extend(validate_command_capability(cap))
        else:
            errors.append(f"{cap.agent}.{cap.name}: unsupported capability type {cap.type}")
    return errors
