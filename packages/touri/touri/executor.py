from __future__ import annotations

from typing import Any

from touri.backend_dispatch import call_primary_backend
from touri.fallbacks import apply_fallbacks, payload_from_params
from touri.models import ServiceResult


def call_uri(
    uri: str,
    registry_root: str,
    payload: dict[str, Any] | None = None,
    context: dict[str, Any] | None = None,
) -> ServiceResult:
    from touri.data_quality import apply_data_quality
    from touri.loader import load_registry
    from touri.matcher import require_match
    from touri.redaction import apply_redaction

    registry = load_registry(registry_root)
    match = require_match(uri, registry)
    manifest = match.manifest
    ctx = dict(context or {})
    ctx.update(
        {
            "uri": uri,
            "capability": manifest.capability.id,
            "scheme": manifest.capability.scheme,
            "operation": manifest.capability.operation,
        }
    )
    final_payload = payload_from_params(match.params, payload)
    result = call_primary_backend(manifest, uri, final_payload, ctx)
    result.uri = uri
    result.capability = manifest.capability.id
    result.backend = manifest.backend.type
    result = apply_data_quality(manifest, result, final_payload, ctx)
    result = apply_fallbacks(manifest, result, final_payload, ctx)
    result = apply_redaction(result, manifest.policy)
    return result
