from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Annotated

import typer

app = typer.Typer(help="uri2verify — data quality, replay, capability verification plans")


@app.command("replay")
def replay_cmd(
    source: Annotated[str, typer.Argument(help="Workflow JSONL event log path or workflow id")],
    json_out: Annotated[bool, typer.Option("--json", help="Output JSON")] = False,
    timeline: Annotated[
        bool, typer.Option("--timeline", help="Include full event timeline")
    ] = False,
    create_test: Annotated[
        str, typer.Option("--create-test", help="Write pytest regression file")
    ] = "",
) -> None:
    from uri2verify.replay import create_regression_test, replay_workflow_events

    if create_test:
        payload = create_regression_test(source, out=create_test)
        typer.echo(json.dumps(payload, indent=2, ensure_ascii=False))
        return
    payload = replay_workflow_events(source)
    if not timeline:
        payload = {key: value for key, value in payload.items() if key != "timeline"}
    if json_out:
        typer.echo(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        typer.echo(_render_replay(payload))


@app.command("capability-plan")
def capability_plan_cmd(
    root: Annotated[Path, typer.Argument(help="Repo root with contract registry")] = Path("."),
) -> None:
    from hypervisor.contract_registry.loader import load_contract_registry
    from hypervisor.contract_registry.validate import validate_registry

    from uri2verify.capability_tests import capability_test_plan_from_registry

    registry = load_contract_registry(root)
    errors = validate_registry(registry)
    if errors:
        typer.echo("Cannot build capability test plan; registry invalid:", err=True)
        for error in errors:
            typer.echo(f"- {error}", err=True)
        raise typer.Exit(code=1)
    plan = capability_test_plan_from_registry(registry)
    typer.echo(json.dumps({"capability_tests": plan}, indent=2, ensure_ascii=False))


@app.command("data-quality")
def data_quality_cmd(
    registry: Annotated[Path, typer.Argument(help="Capability registry directory")],
    uri: Annotated[str, typer.Argument(help="URI to call")],
    payload_json: Annotated[str, typer.Option("--payload", help="JSON payload")] = "{}",
) -> None:
    from touri.executor import call_uri

    from uri2verify.result_checks import enrich_result_dict, technical_vs_business_ok

    payload = json.loads(payload_json)
    result = call_uri(uri, str(registry), payload=payload)
    body = enrich_result_dict(result.to_dict())
    body["technical_vs_business"] = technical_vs_business_ok(body)
    typer.echo(json.dumps(body, indent=2, ensure_ascii=False))


def _render_replay(payload: dict) -> str:
    return "\n".join(
        [
            *_render_replay_header(payload),
            *_render_replay_events("failed_steps", payload.get("failed_steps") or [], "error"),
            *_render_replay_events("blocked_steps", payload.get("blocked_steps") or [], "reason"),
        ]
    )


def _render_replay_header(payload: dict) -> list[str]:
    lines = [
        f"workflow_id: {payload.get('workflow_id')}",
        f"event_log: {payload.get('event_log')}",
        f"event_count: {payload.get('event_count')}",
    ]
    completed = payload.get("workflow_completed") or {}
    if completed:
        lines.append(f"workflow_completed: ok={completed.get('ok')} mode={completed.get('mode')}")
    return lines


def _render_replay_events(name: str, events: list[dict], detail_key: str) -> list[str]:
    lines = [f"{name}: {len(events)}"]
    for event in events:
        lines.append(f"  - {event.get('step_id')}: {event.get(detail_key) or event}")
    return lines


def main(argv: list[str] | None = None) -> int:
    try:
        app(prog_name="uri2verify", args=argv or sys.argv[1:])
    except typer.Exit as exc:
        return int(exc.code or 0)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
