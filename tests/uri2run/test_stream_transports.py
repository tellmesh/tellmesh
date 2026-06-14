"""Tests for uri2run stdio/sse/ws transports and uri3 runtime adapter."""

from __future__ import annotations

from uri2run import run_backend, run_target
from uri3.graph import run_workflow


def test_stdio_transport_json_roundtrip():
    command = (
        "python -c 'import json,sys; "
        'print(json.dumps({"ok": True, "data": {"echo": json.load(sys.stdin)["x"]}}))'
        "'"
    )
    result = run_backend({"type": "stdio", "command": command}, {"x": 42}, {})
    payload = result.to_dict()
    assert payload["ok"] is True
    assert payload["data"]["echo"] == 42
    assert payload["meta"]["runtime"] == "uri2run"
    assert payload["meta"]["transport"] == "stdio"


def test_run_target_stdio_scheme():
    command = 'python -c \'import json,sys; print(json.dumps({"ok": True, "data": {"y": 1}}))\''
    result = run_target(f"stdio://{command}", {}, {})
    assert result.ok is True


def test_sse_transport_parses_events(monkeypatch):
    class FakeResponse:
        status_code = 200

        def iter_lines(self):
            yield 'data: {"event": "ready"}'
            yield 'data: {"event": "done"}'

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    def fake_stream(method, target, timeout=None):
        return FakeResponse()

    monkeypatch.setattr("uri2run.transports.sse_transport.httpx.stream", fake_stream)
    result = run_backend({"type": "sse", "url": "http://testserver/events"}, {}, {})
    payload = result.to_dict()
    assert payload["ok"] is True
    assert payload["data"]["count"] == 2


def test_ws_transport_without_dependency():
    result = run_backend(
        {"type": "ws", "url": "ws://localhost:8090/ws"},
        {"message": {"type": "ping"}},
        {},
    )
    payload = result.to_dict()
    assert payload["ok"] is False
    assert payload["errors"][0]["code"] in {"WS_DEPENDENCY_MISSING", "WS_TRANSPORT_FAILED"}


def test_uri3_workflow_python_runtime_adapter(tmp_path):
    task = {
        "task": {"id": "runtime-python", "description": "python runtime via uri2run"},
        "steps": [
            {
                "id": "transcribe",
                "uri": "python://uri2voice.stt:transcribe",
                "operation": "read",
                "kind": "command",
                "payload": {"text": "hello"},
            }
        ],
    }
    result = run_workflow(task, approve=True, dry_run=False, root=tmp_path, browser_mode="mock")
    assert result.ok is True
    step = result.steps[0]
    assert step.ok is True
    assert step.result.get("runtime") == "uri2run"
    assert step.result.get("data", {}).get("text") == "hello"
