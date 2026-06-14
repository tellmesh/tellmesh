"""Tests for touri voice capability pack (example 21)."""

from __future__ import annotations

from pathlib import Path

import pytest
from touri.executor import call_uri
from touri.loader import load_registry
from uri2flow import expand_flow
from uri3.graph import run_workflow, validate_workflow_graph

VOICE_PROMPT = "wygeneruj agenta pogodowego, uruchom go lokalnie i sprawdź health w Chrome"


@pytest.fixture
def voice_registry(repo_root: Path) -> Path:
    return repo_root / "examples" / "21_touri_voice"


def test_voice_registry_lists_capabilities(voice_registry: Path):
    registry = load_registry(voice_registry)
    ids = {item.capability.id for item in registry}
    assert "stt.mock.transcribe" in ids
    assert "tts.mock.speak" in ids
    assert "voice.command.from_text" in ids


def test_stt_mock_transcribes(voice_registry: Path):
    result = call_uri(
        "stt://mock/transcribe",
        voice_registry,
        payload={"text": "otwórz Chrome i sprawdź health"},
    )
    payload = result.to_dict()
    assert payload["ok"] is True
    assert payload["result_type"] == "transcript"
    assert payload["data"]["text"] == "otwórz Chrome i sprawdź health"
    assert payload["service_result_status"] == "succeeded"


def test_stt_mock_default_transcript_when_empty(voice_registry: Path):
    result = call_uri("stt://mock/transcribe", voice_registry, payload={})
    payload = result.to_dict()
    assert payload["ok"] is True
    assert "health" in payload["data"]["text"].lower()


def test_stt_mock_reads_transcript_file(voice_registry: Path, tmp_path: Path):
    transcript = tmp_path / "transcript.txt"
    transcript.write_text("sprawdz status agenta", encoding="utf-8")
    result = call_uri(
        "stt://mock/transcribe",
        voice_registry,
        payload={"transcript_file": str(transcript)},
    )
    payload = result.to_dict()
    assert payload["ok"] is True
    assert payload["data"]["text"] == "sprawdz status agenta"


def test_tts_mock_speaks(voice_registry: Path, tmp_path: Path):
    result = call_uri(
        "tts://mock/speak",
        voice_registry,
        payload={"text": "Agent działa poprawnie"},
        context={"root": str(tmp_path)},
    )
    payload = result.to_dict()
    assert payload["ok"] is True
    assert payload["result_type"] == "artifact"
    assert payload["artifact_uri"].startswith("artifact://voice/")
    artifact_path = Path(payload["meta"]["artifact_path"])
    assert artifact_path.is_file()


def test_voice_command_plans_flow(voice_registry: Path, tmp_path: Path):
    result = call_uri(
        "voice://command/from-text",
        voice_registry,
        payload={"text": VOICE_PROMPT},
        context={"root": str(tmp_path)},
    )
    payload = result.to_dict()
    assert payload["ok"] is True
    assert payload["result_type"] == "uri_flow"
    assert "flow:" in payload["data"]["flow_yaml"]
    assert "do:" in payload["data"]["flow_yaml"]
    assert payload["data"]["flow_id"]
    flow_file = Path(payload["data"]["flow_file"])
    assert flow_file.is_file()
    graph = expand_flow(flow_file)
    assert validate_workflow_graph(graph) == []


def test_voice_command_rejects_empty_text(voice_registry: Path):
    result = call_uri(
        "voice://command/from-text",
        voice_registry,
        payload={"text": "   "},
    )
    payload = result.to_dict()
    assert payload["ok"] is False
    assert payload["errors"][0]["code"] == "EMPTY_TEXT"


def test_full_mock_voice_pipeline(voice_registry: Path, tmp_path: Path):
    stt = call_uri("stt://mock/transcribe", voice_registry, payload={})
    transcript = stt.to_dict()["data"]["text"]

    voice = call_uri(
        "voice://command/from-text",
        voice_registry,
        payload={"text": transcript},
        context={"root": str(tmp_path)},
    )
    flow_file = Path(voice.to_dict()["data"]["flow_file"])
    graph = expand_flow(flow_file)
    workflow = run_workflow(graph, dry_run=True, root=tmp_path, browser_mode="mock")
    assert workflow.ok is True

    tts = call_uri(
        "tts://mock/speak",
        voice_registry,
        payload={"text": "Workflow zostal przygotowany."},
        context={"root": str(tmp_path)},
    )
    tts_payload = tts.to_dict()
    assert tts_payload["ok"] is True
    assert Path(tts_payload["meta"]["artifact_path"]).is_file()
