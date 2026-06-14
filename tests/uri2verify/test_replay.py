"""Tests for uri2verify replay helpers."""

from __future__ import annotations

from pathlib import Path

from uri2verify.replay import build_task_payload_from_events, create_regression_test, replay_workflow_events


def test_replay_workflow_events(repo_root: Path):
    log_path = repo_root / "output" / "events" / "workflows" / "check-agent-health.jsonl"
    if not log_path.is_file():
        return
    summary = replay_workflow_events(log_path, root=repo_root)
    assert summary["workflow_id"]
    assert summary["event_count"] > 0


def test_build_task_payload_from_step_started_events():
    events = [
        {"type": "WorkflowStarted", "workflow_id": "demo"},
        {
            "type": "StepStarted",
            "step_id": "open_health",
            "uri": "browser://chrome/page/open",
            "operation": "open",
            "kind": "command",
            "payload": {"url": "http://localhost:8101/health"},
        },
    ]
    payload = build_task_payload_from_events(events)
    assert payload["task"]["id"] == "demo"
    assert len(payload["steps"]) == 1
    assert payload["steps"][0]["id"] == "open_health"


def test_create_regression_test_from_events(tmp_path: Path):
    log = tmp_path / "demo.jsonl"
    log.write_text(
        "\n".join(
            [
                '{"type":"WorkflowStarted","workflow_id":"demo","run_id":"r1","mode":"execute"}',
                '{"type":"StepStarted","workflow_id":"demo","step_id":"s1","uri":"agent://x/status","operation":"read","kind":"query"}',
                '{"type":"StepCompleted","workflow_id":"demo","step_id":"s1","ok":true}',
                '{"type":"WorkflowCompleted","workflow_id":"demo","ok":true,"mode":"execute"}',
            ]
        ),
        encoding="utf-8",
    )
    out = tmp_path / "test_replay_demo.py"
    payload = create_regression_test(log, out=out, root=tmp_path)
    assert payload["ok"] is True
    assert out.is_file()
    assert "test_replay_regression" in out.read_text(encoding="utf-8")
