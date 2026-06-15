# AUTO-GENERATED FILE. DO NOT EDIT.
# Source: contracts/agents/generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html_agent.yaml
# Contract hash: sha256:1032ca7c45efe2b94b47aa66b6bda819294316637b494c4ac51dd2724c009bda

from agents.generated.generuj_mape_pogody_dwa_tygodnie_do_przodu_w_html_agent.agent_card import AGENT_CARD


def test_agent_card_has_expected_name():
    assert AGENT_CARD["name"] == "generuj-mape-pogody-dwa-tygodnie-do-przodu-w-html-agent"


def test_agent_card_has_capabilities():
    names = [cap["name"] for cap in AGENT_CARD["capabilities"]]
    assert names == ["run"]


def test_agent_card_has_contract_hash():
    assert AGENT_CARD["generated_from"]["contract_hash"] == (
        "sha256:1032ca7c45efe2b94b47aa66b6bda819294316637b494c4ac51dd2724c009bda"
    )
