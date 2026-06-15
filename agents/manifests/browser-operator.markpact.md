# browser-operator

Generic browser and DOM operation agent backed by uri2ops.

Canonical portable definition: contract, deployment, runtime and optional Docker service.

Sync: `hypervisor sync-agent-manifest browser-operator.local`

```markpact:agent browser-operator
version: 1
agent:
  id: agent://browser-operator
  name: browser-operator
  implementation: operator
  contract: agents/operators/browser_operator/browser_operator.yaml
  package: agents/operators/browser_operator
  module: agents.operators.browser_operator.main:app
operator:
  kind: hypervisor.operator_agent
  runtime_package: agents/operators/browser_operator
```

```markpact:deployment browser-operator.local
deployment:
  id: browser-operator.local
  agent_ref: agent://browser-operator
  target_uri: local://agents/operators/browser_operator
  status: generated
  health_uri: http://localhost:8793/health
  card_uri: http://localhost:8793/.well-known/agent-card.json
  view_uri: view://process/agent/browser-operator.local/latest
metadata:
  source: operator_agent
  role: browser_operator
  contract: agents/operators/browser_operator/browser_operator.yaml
  domain_pack: domains/browser_ops/domain.yaml
  operator_registry: domains/browser_ops/operator_registry.yaml
  expected_service: uri2ops
runtime:
  run: hypervisor run-agent browser-operator.local --detach --wait-healthy
  inspect: hypervisor inspect-agent browser-operator.local
  describe: hypervisor describe-agent browser-operator.local
supervise:
  once: hypervisor supervise browser-operator.local --repair auto
  watch: hypervisor supervise browser-operator.local --watch --repair auto --interval
    15
logs:
  hypervisor: log://hypervisor?grep=browser-operator.local
  process: log://file/output/logs/agents/browser-operator.local.process.log
manifest:
  self: markpact://agents/manifests/browser-operator.markpact.md
env:
  URI2OPS_BASE_URL: http://localhost:8793
```

```markpact:runtime browser-operator.local
runtime:
  module: agents.operators.browser_operator.main:app
  path: /home/tom/github/wronai/hypervisor/agents/operators/browser_operator
  port: 8793
  health_uri: http://localhost:8793/health
  card_uri: http://localhost:8793/.well-known/agent-card.json
  command: /home/tom/github/wronai/hypervisor/.venv/bin/python3 -m uvicorn agents.operators.browser_operator.main:app
    --host 0.0.0.0 --port 8793
```
