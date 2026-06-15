# Deployment registry (markpact export)

Human-readable export of [`agent_deployments.yaml`](./agent_deployments.yaml) for import into external systems via `markpact://deployments/README.md`.

Load blocks:

```python
from pathlib import Path
import yaml
from uri2pact import extract_markpact_blocks

markdown = Path("deployments/README.md").read_text(encoding="utf-8")
for block in extract_markpact_blocks(markdown, "deploy"):
    print(yaml.safe_load(block["body"])["deployment"]["id"])
```

## weather-map-agent.local

```markpact:deploy weather-map-agent.local
deployment:
  id: weather-map-agent.local
  agent_ref: agent://weather-map-agent
  target_uri: local://agents/generated/weather_map_agent
  status: generated
  health_uri: http://localhost:8118/health
  card_uri: http://localhost:8118/.well-known/agent-card.json
  view_uri: view://process/agent/weather-map-agent.local/latest
source:
  contract: domains/weather_map/uri_tree.yaml
  generated: agents/generated/weather_map_agent/README.md
runtime:
  run: hypervisor run-agent weather-map-agent.local --detach --wait-healthy
  inspect: hypervisor inspect-agent weather-map-agent.local
supervise:
  once: hypervisor supervise weather-map-agent.local --repair auto
  watch: hypervisor supervise weather-map-agent.local --watch --repair auto --interval 15
logs:
  hypervisor: log://hypervisor?grep=weather-map-agent.local
  process: log://file/output/logs/agents/weather-map-agent.local.process.log
  watch: log://file/output/logs/hypervisor-watch.jsonl
markpact:
  agent_generation: markpact://agents/generated/weather_map_agent/README.md#weather-map-agent
```

## invoices-agent.local

```markpact:deploy invoices-agent.local
deployment:
  id: invoices-agent.local
  agent_ref: agent://invoices-agent
  target_uri: local://agents/generated/invoices_agent
  status: generated
  health_uri: http://localhost:8123/health
  card_uri: http://localhost:8123/.well-known/agent-card.json
  view_uri: view://process/agent/invoices-agent.local/latest
source:
  contract: contracts/agents/invoices_agent.yaml
  generated: agents/generated/invoices_agent/README.md
runtime:
  run: hypervisor run-agent invoices-agent.local --detach --wait-healthy
  inspect: hypervisor inspect-agent invoices-agent.local
supervise:
  once: hypervisor supervise invoices-agent.local --repair auto
  watch: hypervisor supervise invoices-agent.local --watch --repair auto --interval 15
logs:
  hypervisor: log://hypervisor?grep=invoices-agent.local
  process: log://file/output/logs/agents/invoices-agent.local.process.log
  watch: log://file/output/logs/hypervisor-watch.jsonl
markpact:
  agent_generation: markpact://agents/generated/invoices_agent/README.md#invoices-agent
```

## user-agent.local

```markpact:deploy user-agent.local
deployment:
  id: user-agent.local
  agent_ref: agent://user-agent
  target_uri: local://agents/generated/user_agent
  status: generated
  health_uri: http://localhost:8102/health
  card_uri: http://localhost:8102/.well-known/agent-card.json
  view_uri: view://process/agent/user-agent.local/latest
source:
  contract: contracts/agents/user_agent.yaml
  generated: agents/generated/user_agent/README.md
runtime:
  run: hypervisor run-agent user-agent.local --detach --wait-healthy
  inspect: hypervisor inspect-agent user-agent.local
supervise:
  once: hypervisor supervise user-agent.local --repair auto
  watch: hypervisor supervise user-agent.local --watch --repair auto --interval 15
logs:
  hypervisor: log://hypervisor?grep=user-agent.local
  process: log://file/output/logs/agents/user-agent.local.process.log
  watch: log://file/output/logs/hypervisor-watch.jsonl
markpact:
  agent_generation: markpact://agents/generated/user_agent/README.md#user-agent
```

## hypervisor-dashboard.local

```markpact:deploy hypervisor-dashboard.local
deployment:
  id: hypervisor-dashboard.local
  agent_ref: agent://hypervisor-dashboard
  target_uri: local://agents/system/hypervisor_dashboard
  status: generated
  health_uri: http://localhost:8788/health
  card_uri: http://localhost:8788/.well-known/agent-card.json
  view_uri: view://process/agent/hypervisor-dashboard.local/latest
role:
  - observer
  - renderer
  - controller
runtime:
  run: make start
  chat: http://localhost:8788/www/chat.html
  agents_ui: http://localhost:8788/ui/agents
api:
  agents: GET /api/agents
  events: GET /api/events
  events_stream: GET /api/events/stream
logs:
  watch: log://file/output/logs/hypervisor-watch.jsonl
markpact:
  profile: dashboard-agent
```

## browser-operator.local

```markpact:deploy browser-operator.local
deployment:
  id: browser-operator.local
  agent_ref: agent://browser-operator
  target_uri: local://agents/operators/browser_operator
  status: generated
  health_uri: http://localhost:8793/health
  card_uri: http://localhost:8793/.well-known/agent-card.json
  view_uri: view://process/agent/browser-operator.local/latest
source:
  contract: agents/operators/browser_operator.yaml
runtime:
  run: hypervisor run-agent browser-operator.local --detach --wait-healthy
  inspect: hypervisor inspect-agent browser-operator.local
  direct: uvicorn agents.operators.browser_operator.main:app --host 127.0.0.1 --port 8793
api:
  a2a: POST /a2a/tasks
  mcp_tools: GET /mcp/tools
  mcp_call: POST /mcp/tools/call
  environments: GET /environments
capabilities:
  schemes:
    - browser
execution_environments:
  local: in-process Playwright on host (pip install -e '.[browser]' && playwright install chromium)
  docker: Playwright container (requires Docker; URI2OPS_DOCKER_NETWORK=host on Linux)
  mock: no browser deps
  remote: delegate to another uri2ops via remote_url / URI2OPS_REMOTE_URL
logs:
  process: log://file/output/logs/agents/browser-operator.local.process.log
markpact:
  operator_contract: markpact://agents/operators/browser_operator.yaml#browser-operator
```

## desktop-operator.local

```markpact:deploy desktop-operator.local
deployment:
  id: desktop-operator.local
  agent_ref: agent://desktop-operator
  target_uri: local://agents/operators/browser_operator
  status: generated
  health_uri: http://localhost:8791/health
  card_uri: http://localhost:8791/.well-known/agent-card.json
  view_uri: view://process/agent/desktop-operator.local/latest
source:
  contract: agents/operators/desktop_operator.yaml
runtime:
  run: hypervisor run-agent desktop-operator.local --detach --wait-healthy
  inspect: hypervisor inspect-agent desktop-operator.local
  direct: uvicorn agents.operators.desktop_operator.main:app --host 127.0.0.1 --port 8791
api:
  a2a: POST /a2a/tasks
  mcp_tools: GET /mcp/tools
  mcp_call: POST /mcp/tools/call
capabilities:
  schemes:
    - screen
    - input
    - pcwin
    - android
logs:
  process: log://file/output/logs/agents/desktop-operator.local.process.log
  watch: log://file/output/logs/hypervisor-watch.jsonl
markpact:
  operator_contract: markpact://agents/operators/desktop_operator.yaml#desktop-operator
```

## Fleet watch (all local agents)

Run one watch loop per deployment (separate terminals or systemd units):

```bash
hypervisor supervise weather-map-agent.local --watch --repair auto --interval 15
hypervisor supervise invoices-agent.local --watch --repair auto --interval 15
hypervisor supervise user-agent.local --watch --repair auto --interval 15
hypervisor supervise browser-operator.local --watch --repair auto --interval 15
hypervisor supervise desktop-operator.local --watch --repair auto --interval 15
```

Smoke test (2 ticks, no sleep):

```bash
hypervisor supervise weather-map-agent.local --watch --repair auto --count 2 --interval 0
```

Watch events append to `output/logs/hypervisor-watch.jsonl` and appear in dashboard `/api/events` as `log.event` (with `agent_id` when `uri.subject` is set).

See [`docs/MARKPACT_WITH_TOURI.md`](../docs/MARKPACT_WITH_TOURI.md) · [`docs/TUTORIAL_THREE_AGENTS.md`](../docs/TUTORIAL_THREE_AGENTS.md).
