"""Tests for multi-line NL prompt splitting."""

from __future__ import annotations

from urish.backends.ask import ask_prompt
from urish.intent import split_nl_commands


def test_split_nl_commands_single_line():
    assert split_nl_commands("pokaż proces agenta weather-map-agent.local") == [
        "pokaż proces agenta weather-map-agent.local"
    ]


def test_split_nl_commands_multiline():
    text = "line one\nline two\n"
    assert split_nl_commands(text) == ["line one", "line two"]


def test_ask_prompt_batch():
    prompt = (
        "pokaż proces agenta weather-map-agent.local\n"
        "zdiagnozuj agenta invoices-agent.local"
    )
    result = ask_prompt(prompt)
    data = result["data"]
    assert data["batch"] is True
    assert len(data["actions"]) == 2
    assert (
        "view://process/agent/weather-map-agent.local/latest"
        in data["actions"][0]["planned_uris"]
    )
    assert "repair://agent/invoices-agent.local/diagnose" in data["actions"][1]["planned_uris"]
