# AUTO-GENERATED FILE. DO NOT EDIT.
# Source: /home/tom/github/wronai/hypervisor/contracts/agents/test_orders_agent.yaml
# Contract hash: sha256:9d461331e6fc19f635e3a1d67a8eb1bd9c774465ccfe4e804e2a180f089bc9c8

AGENT_CARD = {
  "capabilities": [
    {
      "command": null,
      "description": "Read resource://orders/{order_id} from the shared Resource Runtime.",
      "emits": [],
      "input_schema": null,
      "name": "read_order",
      "output_schema": "app.orders.v1.OrderView",
      "renderer": "detail",
      "type": "resource_read",
      "uri": "resource://orders/{order_id}"
    },
    {
      "command": null,
      "description": "Read resource://orders/{order_id}/events from the shared Resource Runtime.",
      "emits": [],
      "input_schema": null,
      "name": "read_order_events",
      "output_schema": "app.orders.v1.OrderEventsView",
      "renderer": "timeline",
      "type": "resource_read",
      "uri": "resource://orders/{order_id}/events"
    }
  ],
  "description": "Generated thin agent for orders resources.",
  "generated_from": {
    "contract": "/home/tom/github/wronai/hypervisor/contracts/agents/test_orders_agent.yaml",
    "contract_hash": "sha256:9d461331e6fc19f635e3a1d67a8eb1bd9c774465ccfe4e804e2a180f089bc9c8"
  },
  "name": "orders-agent",
  "version": "0.1.0"
}