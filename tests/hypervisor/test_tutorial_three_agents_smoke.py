from __future__ import annotations

from urish.backends.ask import ask_prompt
from urish.backends.proof import proof_uri
from urish.intent import detect_intent


def test_three_agents_tutorial_smoke_routes_core_commands():
    weather = detect_intent("pokaż proces agenta weather-map-agent.local")
    invoices = detect_intent("zdiagnozuj agenta invoices-agent.local")
    desktop = detect_intent("sprawdz desktop operator i pokaz stan runtime")

    assert weather["kind"] == "agent"
    assert weather["uri"] == "view://process/agent/weather-map-agent.local/latest"
    assert invoices["kind"] == "agent"
    assert invoices["uri"] == "repair://agent/invoices-agent.local/diagnose"
    assert desktop["kind"] == "desktop_ops"
    assert "health://agent/desktop-operator.local" in desktop["planned_uris"]


def test_three_agents_tutorial_smoke_ask_batch():
    result = ask_prompt(
        "pokaż proces agenta weather-map-agent.local\n"
        "zdiagnozuj agenta invoices-agent.local\n"
        "sprawdz desktop operator i pokaz stan runtime"
    )
    data = result["data"]

    assert data["batch"] is True
    assert data["detected_kind"] == "batch"
    assert len(data["actions"]) == 3
    assert data["actions"][0]["detected_kind"] == "agent"
    assert data["actions"][1]["detected_subtype"] == "diagnose"
    assert data["actions"][2]["detected_kind"] == "desktop_ops"


def test_three_agents_tutorial_smoke_proof_dry_run():
    result = proof_uri("view://process/agent/weather-map-agent.local/latest")

    checks = {item["name"]: item for item in result["data"]["checks"]}
    assert result["ok"] is True
    assert checks["cli"]["ok"] is True
    assert checks["uri"]["ok"] is True
    assert checks["policy"]["ok"] is True
