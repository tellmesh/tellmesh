from __future__ import annotations

from hypervisor.contract_registry.cross_checks.proto_index import schema_exists
from hypervisor.contract_registry.models import ContractRegistry


def validate_capability_cross_refs(
    registry: ContractRegistry,
    *,
    resource_uris: set[str],
    resource_schemas: set[str],
    renderer_names: set[str],
    proto_text: str,
) -> list[str]:
    errors: list[str] = []
    for capability in registry.capabilities:
        label = f"{capability.agent}.{capability.name}"
        if capability.type == "resource_read":
            if not capability.uri:
                errors.append(f"capability {label} lacks uri")
            elif capability.uri not in resource_uris:
                errors.append(f"capability {label} references missing resource {capability.uri}")
            if capability.output_schema and capability.output_schema not in resource_schemas:
                errors.append(
                    f"capability {label} output_schema does not match any resource schema: {capability.output_schema}"
                )
        if capability.renderer and capability.renderer not in renderer_names:
            errors.append(f"capability {label} references unknown renderer {capability.renderer}")
        for schema_ref in [capability.input_schema, capability.output_schema]:
            if schema_ref and proto_text and not schema_exists(proto_text, schema_ref):
                errors.append(f"capability {label} references missing proto schema {schema_ref}")
    return errors
