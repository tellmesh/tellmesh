# invoices-agent

Generated thin agent for invoices resources.

Canonical portable definition: contract, deployment, runtime and optional Docker service.

Sync: `hypervisor sync-agent-manifest invoices-agent.local`

```markpact:agent invoices-agent
version: 1
agent:
  id: agent://invoices-agent
  name: invoices-agent
  implementation: generated
  contract: contracts/agents/invoices_agent.yaml
  package: agents/generated/invoices_agent
  module: agents.generated.invoices_agent.main:app
  version: 0.1.0
  python_package: invoices_agent
  description: Generated thin agent for invoices resources.
capabilities:
- name: read_invoice
  type: resource_read
  description: Read resource://invoices/{invoice_id} from the shared Resource Runtime.
  uri: resource://invoices/{invoice_id}
  output_schema: app.invoices.v1.InvoiceView
  renderer: detail
- name: read_invoice_events
  type: resource_read
  description: Read resource://invoices/{invoice_id}/events from the shared Resource
    Runtime.
  uri: resource://invoices/{invoice_id}/events
  output_schema: app.invoices.v1.InvoiceEventsView
  renderer: timeline
- name: create_invoice
  type: command
  description: Execute CreateInvoice through the shared Resource Runtime.
  command: CreateInvoice
  input_schema: app.invoices.v1.CreateInvoiceCommand
  emits:
  - CreateInvoiceRequested
```

```markpact:deployment invoices-agent.local
deployment:
  id: invoices-agent.local
  agent_ref: agent://invoices-agent
  target_uri: local://agents/generated/invoices_agent
  status: generated
  health_uri: http://localhost:8123/health
  card_uri: http://localhost:8123/.well-known/agent-card.json
  view_uri: view://process/agent/invoices-agent.local/latest
metadata:
  source: contract
  contract: contracts/agents/invoices_agent.yaml
runtime:
  run: hypervisor run-agent invoices-agent.local --detach --wait-healthy
  inspect: hypervisor inspect-agent invoices-agent.local
  describe: hypervisor describe-agent invoices-agent.local
supervise:
  once: hypervisor supervise invoices-agent.local --repair auto
  watch: hypervisor supervise invoices-agent.local --watch --repair auto --interval
    15
logs:
  hypervisor: log://hypervisor?grep=invoices-agent.local
  process: log://file/output/logs/agents/invoices-agent.local.process.log
manifest:
  self: markpact://agents/manifests/invoices-agent.markpact.md
```

```markpact:runtime invoices-agent.local
runtime:
  module: agents.generated.invoices_agent.main:app
  path: /home/tom/github/tellmesh/tellmesh/agents/generated/invoices_agent
  port: 8123
  health_uri: http://localhost:8123/health
  card_uri: http://localhost:8123/.well-known/agent-card.json
  command: /home/tom/github/tellmesh/tellmesh/.venv/bin/python3 -m uvicorn agents.generated.invoices_agent.main:app
    --host 0.0.0.0 --port 8123
```

```markpact:docker invoices-agent
service:
  name: invoices-agent
  build:
    context: .
    dockerfile: agents/generated/invoices_agent/Dockerfile
  container_name: invoices-agent
  ports:
  - 8123:8123
  healthcheck:
    test:
    - CMD
    - curl
    - -f
    - http://localhost:8123/health
  environment:
    RESOURCE_RUNTIME_URL: http://host.docker.internal:8000
compose:
  output: output/deployments/invoices-agent/docker-compose.yaml
```
