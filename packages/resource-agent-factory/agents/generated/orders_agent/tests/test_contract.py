# AUTO-GENERATED FILE. DO NOT EDIT.
# Source: /home/tom/github/wronai/hypervisor/contracts/agents/test_orders_agent.yaml
# Contract hash: sha256:9d461331e6fc19f635e3a1d67a8eb1bd9c774465ccfe4e804e2a180f089bc9c8

from agents.generated.orders_agent.agent_card import AGENT_CARD


def test_agent_card_has_expected_name():
    assert AGENT_CARD["name"] == "orders-agent"


def test_agent_card_has_capabilities():
    names = {cap["name"] for cap in AGENT_CARD["capabilities"]}
    assert names == ["read_order", "read_order_events"]


def test_agent_card_has_contract_hash():
    assert AGENT_CARD["generated_from"]["contract_hash"] == "sha256:9d461331e6fc19f635e3a1d67a8eb1bd9c774465ccfe4e804e2a180f089bc9c8"