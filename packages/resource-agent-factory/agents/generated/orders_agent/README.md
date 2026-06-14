<!-- AUTO-GENERATED FILE. DO NOT EDIT. -->
<!-- Source: /home/tom/github/wronai/hypervisor/contracts/agents/test_orders_agent.yaml -->
<!-- Contract hash: sha256:9d461331e6fc19f635e3a1d67a8eb1bd9c774465ccfe4e804e2a180f089bc9c8 -->
# orders-agent

Generated thin resource agent.

- Version: `0.1.0`
- Source: `/home/tom/github/wronai/hypervisor/contracts/agents/test_orders_agent.yaml`
- Contract hash: `sha256:9d461331e6fc19f635e3a1d67a8eb1bd9c774465ccfe4e804e2a180f089bc9c8`

## Run

```bash
uvicorn agents.generated.orders_agent.main:app --reload --port 8101
```

## Endpoints

```txt
GET /health
GET /capabilities
GET /.well-known/agent.json
GET /.well-known/agent-card.json
GET /resources/read?uri=...
POST /commands
```

## Capabilities

- `read_order` — `resource_read`, URI: `resource://orders/{order_id}`- `read_order_events` — `resource_read`, URI: `resource://orders/{order_id}/events`