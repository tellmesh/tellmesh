from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from uri3.graph.event_log import workflow_event_path


def _resolve_event_path(source: str | Path, root: Path) -> Path:
    path = Path(source)
    if path.exists():
        return path
    candidate = workflow_event_path(str(source), root)
    if candidate.exists():
        return candidate
    raise FileNotFoundError(f"workflow event log not found for {source!r}")


def load_workflow_events(source: str | Path, *, root: Path | None = None) -> list[dict[str, Any]]:
    from uri3.config.repo_root import find_repo_root

    repo_root = root or find_repo_root()
    path = _resolve_event_path(source, repo_root)
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            events.append(json.loads(line))
    return events


def replay_workflow_events(source: str | Path, *, root: Path | None = None) -> dict[str, Any]:
    from uri3.config.repo_root import find_repo_root

    repo_root = root or find_repo_root()
    path = _resolve_event_path(source, repo_root)
    events = load_workflow_events(path, root=repo_root)
    workflow_id = next((event.get("workflow_id") for event in events if event.get("workflow_id")), path.stem)
    failed_steps = [event for event in events if event.get("type") == "StepFailed"]
    blocked_steps = [event for event in events if event.get("type") == "StepBlocked"]
    completed = next((event for event in reversed(events) if event.get("type") == "WorkflowCompleted"), None)
    return {
        "workflow_id": workflow_id,
        "event_log": str(path),
        "event_count": len(events),
        "failed_steps": failed_steps,
        "blocked_steps": blocked_steps,
        "workflow_completed": completed,
        "timeline": events,
    }


def build_task_payload_from_events(events: list[dict[str, Any]]) -> dict[str, Any]:
    workflow_id = next((event.get("workflow_id") for event in events if event.get("workflow_id")), "replay-workflow")
    steps: list[dict[str, Any]] = []
    for event in events:
        if event.get("type") != "StepStarted":
            continue
        step: dict[str, Any] = {
            "id": str(event["step_id"]),
            "uri": str(event["uri"]),
            "operation": str(event["operation"]),
            "kind": str(event.get("kind") or "query"),
        }
        payload = event.get("payload")
        if isinstance(payload, dict) and payload:
            step["payload"] = payload
        steps.append(step)
    return {
        "task": {
            "id": workflow_id,
            "description": f"Replay regression for {workflow_id}",
        },
        "steps": steps,
    }


def render_regression_test(
    task_payload: dict[str, Any],
    *,
    expected_ok: bool,
    approve: bool,
    browser_mode: str = "mock",
    blocked_step_ids: list[str] | None = None,
    failed_step_ids: list[str] | None = None,
) -> str:
    task_json = json.dumps(task_payload, indent=4, ensure_ascii=False)
    blocked = blocked_step_ids or []
    failed = failed_step_ids or []
    lines = [
        '"""Auto-generated regression test from uri3 replay --create-test."""',
        "",
        "from __future__ import annotations",
        "",
        "from pathlib import Path",
        "",
        "from uri3.graph import run_workflow",
        "",
        f"TASK_PAYLOAD = {task_json}",
        "",
        "",
        "def test_replay_regression(tmp_path: Path):",
        f"    result = run_workflow(TASK_PAYLOAD, approve={approve!r}, root=tmp_path, browser_mode={browser_mode!r})",
        "    payload = result.to_dict()",
        "    workflow = payload['workflow_result']",
        f"    assert workflow['ok'] is {expected_ok!r}",
    ]
    if blocked:
        lines.append(f"    assert workflow.get('pending_approval') == {blocked!r} or payload['steps'][0]['status'] == 'blocked'")
    if failed:
        lines.append(f"    failed_nodes = workflow.get('failed_nodes') or []")
        lines.append(f"    assert set(failed_nodes) >= set({failed!r})")
    return "\n".join(lines) + "\n"


def create_regression_test(
    source: str | Path,
    *,
    out: str | Path,
    root: Path | None = None,
) -> dict[str, Any]:
    from uri3.config.repo_root import find_repo_root

    repo_root = root or find_repo_root()
    summary = replay_workflow_events(source, root=repo_root)
    timeline = summary.get("timeline") or []
    task_payload = build_task_payload_from_events(timeline)
    if not task_payload["steps"]:
        raise ValueError("No StepStarted events found; cannot create regression test")

    blocked_ids = [str(event.get("step_id")) for event in summary.get("blocked_steps") or [] if event.get("step_id")]
    failed_ids = [str(event.get("step_id")) for event in summary.get("failed_steps") or [] if event.get("step_id")]
    completed = summary.get("workflow_completed") or {}
    expected_ok = bool(completed.get("ok"))
    approve = not blocked_ids

    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    content = render_regression_test(
        task_payload,
        expected_ok=expected_ok,
        approve=approve,
        blocked_step_ids=blocked_ids,
        failed_step_ids=failed_ids,
    )
    out_path.write_text(content, encoding="utf-8")
    return {
        "ok": True,
        "test_path": str(out_path),
        "workflow_id": summary.get("workflow_id"),
        "expected_ok": expected_ok,
        "approve": approve,
        "blocked_step_ids": blocked_ids,
        "failed_step_ids": failed_ids,
    }
