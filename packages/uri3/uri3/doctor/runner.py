from __future__ import annotations

from pathlib import Path
from typing import Any

from uri3.doctor import checks
from uri3.doctor.registry_index import write_registry_indexes
from uri3.doctor.envelope_migrate import migrate_workflow_logs
from uri3.resolvers.explain import default_touri_registry


def run_doctor(
    *,
    root: Path | None = None,
    registry: str | Path | None = None,
    capability_plan: bool = False,
    replay_failures: bool = False,
    build_registry: bool = False,
    strict_envelope: bool = False,
    migrate_envelope: bool = False,
) -> dict[str, Any]:
    from uri3.config.repo_root import find_repo_root

    repo_root = root or find_repo_root()
    registry_path = Path(registry) if registry else default_touri_registry(repo_root)
    migration: dict[str, Any] | None = None
    if migrate_envelope:
        migration = migrate_workflow_logs(repo_root)

    results: list[dict[str, Any]] = [
        checks.check_config(repo_root),
        checks.check_contract_registry(repo_root),
        checks.check_touri_registry(repo_root, registry_path),
        checks.check_uri2ops_registry(repo_root),
        checks.check_explain_smoke(repo_root, registry_path),
        checks.check_result_envelope(),
        checks.check_recent_workflow_logs(repo_root, strict=strict_envelope),
    ]
    if capability_plan:
        results.append(checks.check_capability_plan(repo_root))
    if replay_failures:
        results.append(checks.check_replay_failures(repo_root))

    warnings: list[str] = []
    for item in results:
        note = item.get("note")
        if note:
            warnings.append(f"{item['id']}: {note}")
        for error in item.get("errors") or []:
            warnings.append(f"{item['id']}: {error}")
        for mismatch in item.get("mismatches") or []:
            warnings.append(f"{item['id']}: {mismatch}")
        for failure in item.get("failures") or []:
            warnings.append(f"{item['id']}: {failure}")

    payload: dict[str, Any] = {
        "ok": all(item["ok"] for item in results),
        "checks": results,
        "warnings": warnings,
        "registry": str(registry_path),
    }
    if build_registry:
        index_result = write_registry_indexes(repo_root, registry_path=registry_path)
        payload["registry_index"] = index_result
        if not index_result.get("ok"):
            payload["ok"] = False
    if migration is not None:
        payload["envelope_migration"] = migration
        if migration.get("updated_events"):
            results.append(
                {
                    "id": "envelope.migration",
                    "ok": True,
                    "updated_events": migration.get("updated_events"),
                    "files": migration.get("files"),
                }
            )
            payload["checks"] = results
    return payload
