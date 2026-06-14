from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from uri3.resolvers.explain import (
    default_touri_registry,
    explain_uri,
    load_touri_config,
)


def _check(id: str, ok: bool, **detail: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {"id": id, "ok": ok}
    payload.update(detail)
    return payload


def check_config(root: Path) -> dict[str, Any]:
    touri_cfg_path = root / "config" / "touri.uri.yaml"
    operator_cfg_path = root / "config" / "operator_registry.uri.yaml"
    uri3_cfg_path = root / "config" / "uri3.uri.yaml"
    touri_cfg = load_touri_config(root)
    registry_path = default_touri_registry(root)
    missing = [
        name
        for name, path in (
            ("config/touri.uri.yaml", touri_cfg_path),
            ("config/operator_registry.uri.yaml", operator_cfg_path),
            ("config/uri3.uri.yaml", uri3_cfg_path),
        )
        if not path.is_file()
    ]
    return _check(
        "config",
        ok=not missing,
        paths={
            "touri": str(touri_cfg_path),
            "operator_registry": str(operator_cfg_path),
            "uri3": str(uri3_cfg_path),
        },
        registry_path=str(registry_path),
        resolution_order=list(touri_cfg.get("resolution_order") or []),
        missing=missing,
    )


def check_contract_registry(root: Path) -> dict[str, Any]:
    try:
        from hypervisor.contract_registry.loader import load_contract_registry
        from hypervisor.contract_registry.schema_validator import validate_contract_files
        from hypervisor.contract_registry.validate import validate_registry
    except ImportError as exc:
        return _check("contract_registry", ok=False, errors=[f"hypervisor unavailable: {exc}"])

    schema_results = validate_contract_files(root)
    schema_errors = [f"{item.path}: {err}" for item in schema_results if not item.ok for err in item.errors]
    registry = load_contract_registry(root)
    logical_errors = validate_registry(registry)
    errors = [*schema_errors, *logical_errors]
    return _check(
        "contract_registry",
        ok=not errors,
        counts={
            "resources": len(registry.resources),
            "views": len(registry.views),
            "capabilities": len(registry.capabilities),
        },
        errors=errors,
    )


def check_touri_registry(root: Path, registry_path: Path) -> dict[str, Any]:
    from touri.loader import iter_manifest_paths, load_registry
    from touri.validator import validate_manifest

    if not registry_path.exists():
        return _check(
            "touri.registry",
            ok=False,
            registry=str(registry_path),
            errors=[f"registry path not found: {registry_path}"],
        )

    manifests = load_registry(registry_path)
    invalid: list[dict[str, str]] = []
    for path in iter_manifest_paths(registry_path):
        validation = validate_manifest(path)
        if not validation["ok"]:
            invalid.append({"path": str(path), "errors": "; ".join(validation.get("errors") or [])})

    return _check(
        "touri.registry",
        ok=not invalid,
        registry=str(registry_path),
        manifests=len(manifests),
        capability_ids=[manifest.capability.id for manifest in manifests],
        invalid=invalid,
    )


def check_uri2ops_registry(root: Path) -> dict[str, Any]:
    try:
        from uri2ops.operation_registry.validator import validate_operation_registry
        from uri2ops.remote_registry.loader import list_remote_sources, resolve_operation_registry
    except ImportError as exc:
        return _check("uri2ops.registry", ok=False, errors=[f"uri2ops unavailable: {exc}"])

    registry = resolve_operation_registry(root=root)
    errors = validate_operation_registry(registry)
    schemes = sorted({scheme for scheme, _operation in registry.operations})
    return _check(
        "uri2ops.registry",
        ok=not errors,
        operations=len(registry.operations),
        schemes=schemes,
        remotes=list_remote_sources(root=root),
        errors=errors,
    )


def check_explain_smoke(root: Path, registry_path: Path) -> dict[str, Any]:
    from touri.loader import load_registry
    from touri.register import sample_uri_from_template

    if not registry_path.exists():
        return _check("explain.smoke", ok=False, mismatches=[], errors=["registry path missing"])

    mismatches: list[dict[str, str]] = []
    for manifest in load_registry(registry_path):
        sample_uri = sample_uri_from_template(manifest.capability.uri_template)
        explain = explain_uri(sample_uri, registry_root=registry_path, root=root)
        matched = explain.get("matched_registry")
        if matched != "touri":
            mismatches.append(
                {
                    "capability": manifest.capability.id,
                    "sample_uri": sample_uri,
                    "matched_registry": str(matched),
                }
            )
    return _check(
        "explain.smoke",
        ok=not mismatches,
        checked=len(load_registry(registry_path)),
        mismatches=mismatches,
    )


def check_result_envelope() -> dict[str, Any]:
    try:
        from uri3.results import service_result
        from uri2verify.result_checks import enrich_result_dict, technical_vs_business_ok
    except ImportError as exc:
        return _check("envelope.exports", ok=False, errors=[str(exc)])

    sample = service_result(ok=True, result_type="data", data={"x": 1})
    payload = enrich_result_dict(sample.to_dict())
    required = ("workflow_status", "execution_status", "service_result_status")
    missing = [field for field in required if field not in payload]
    split = technical_vs_business_ok(payload)
    return _check(
        "envelope.exports",
        ok=not missing,
        missing_fields=missing,
        sample_statuses={field: payload.get(field) for field in required},
        technical_vs_business=split,
    )


def check_recent_workflow_logs(root: Path, *, strict: bool = False) -> dict[str, Any]:
    logs_dir = root / "output" / "events" / "workflows"
    if not logs_dir.is_dir():
        return _check("envelope.recent_logs", ok=True, logs=0, missing_fields=0, note="no workflow logs directory")

    required = ("workflow_status", "execution_status", "service_result_status")
    missing_fields = 0
    logs_checked = 0
    for path in sorted(logs_dir.glob("*.jsonl")):
        logs_checked += 1
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            event = json.loads(line)
            if event.get("type") != "WorkflowCompleted":
                continue
            missing_fields += sum(1 for field in required if field not in event)
    legacy = missing_fields > 0
    return _check(
        "envelope.recent_logs",
        ok=(missing_fields == 0) if strict else True,
        logs=logs_checked,
        missing_fields=missing_fields,
        legacy_logs=legacy,
        strict=strict,
        directory=str(logs_dir),
        note="legacy workflow logs missing status envelope fields" if legacy and not strict else "",
    )


def check_capability_plan(root: Path) -> dict[str, Any]:
    try:
        from hypervisor.contract_registry.loader import load_contract_registry
        from hypervisor.contract_registry.validate import validate_registry
        from uri2verify.capability_tests import capability_test_plan_from_registry
    except ImportError as exc:
        return _check("uri2verify.capability_plan", ok=False, errors=[str(exc)])

    registry = load_contract_registry(root)
    errors = validate_registry(registry)
    if errors:
        return _check("uri2verify.capability_plan", ok=False, errors=errors)
    plan = capability_test_plan_from_registry(registry)
    return _check("uri2verify.capability_plan", ok=True, tests=len(plan))


def check_replay_failures(root: Path) -> dict[str, Any]:
    logs_dir = root / "output" / "events" / "workflows"
    if not logs_dir.is_dir():
        return _check("uri2verify.replay_failures", ok=True, failures=[], note="no workflow logs directory")

    from uri2verify.replay import replay_workflow_events

    failures: list[dict[str, Any]] = []
    for path in sorted(logs_dir.glob("*.jsonl")):
        summary = replay_workflow_events(path, root=root)
        failed = summary.get("failed_steps") or []
        blocked = summary.get("blocked_steps") or []
        completed = summary.get("workflow_completed") or {}
        if failed or blocked or completed.get("ok") is False:
            failures.append(
                {
                    "workflow_id": summary.get("workflow_id"),
                    "event_log": summary.get("event_log"),
                    "failed_steps": len(failed),
                    "blocked_steps": len(blocked),
                    "workflow_ok": completed.get("ok"),
                }
            )
    return _check("uri2verify.replay_failures", ok=not failures, failures=failures)
