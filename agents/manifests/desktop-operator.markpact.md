# desktop-operator

Generic screen, input, Windows UI and Android UI operation agent backed by uri2ops.

Canonical portable definition: contract, deployment, runtime and optional Docker service.

Sync: `hypervisor sync-agent-manifest desktop-operator.local`

```markpact:agent desktop-operator
version: 1
agent:
  id: agent://desktop-operator
  name: desktop-operator
  implementation: operator
  contract: agents/operators/desktop_operator/desktop_operator.yaml
  package: agents/operators/desktop_operator
  module: agents.operators.desktop_operator.main:app
operator:
  kind: hypervisor.operator_agent
  runtime_package: agents/operators/desktop_operator
```

```markpact:deployment desktop-operator.local
deployment:
  id: desktop-operator.local
  agent_ref: agent://desktop-operator
  target_uri: local://agents/operators/desktop_operator
  status: generated
  health_uri: http://localhost:8791/health
  card_uri: http://localhost:8791/.well-known/agent-card.json
  view_uri: view://process/agent/desktop-operator.local/latest
metadata:
  source: operator_agent
  role: desktop_operator
  contract: agents/operators/desktop_operator/desktop_operator.yaml
  domain_pack: domains/desktop_ops/domain.yaml
  operator_registry: domains/desktop_ops/operator_registry.yaml
  expected_service: uri2ops
runtime:
  run: hypervisor run-agent desktop-operator.local --detach --wait-healthy
  inspect: hypervisor inspect-agent desktop-operator.local
  describe: hypervisor describe-agent desktop-operator.local
supervise:
  once: hypervisor supervise desktop-operator.local --repair auto
  watch: hypervisor supervise desktop-operator.local --watch --repair auto --interval
    15
logs:
  hypervisor: log://hypervisor?grep=desktop-operator.local
  process: log://file/output/logs/agents/desktop-operator.local.process.log
manifest:
  self: markpact://agents/manifests/desktop-operator.markpact.md
env:
  URI2OPS_BASE_URL: http://localhost:8791
```

```markpact:runtime desktop-operator.local
runtime:
  module: agents.operators.desktop_operator.main:app
  path: /home/tom/github/tellmesh/tellmesh/agents/operators/desktop_operator
  port: 8791
  health_uri: http://localhost:8791/health
  card_uri: http://localhost:8791/.well-known/agent-card.json
  command: /home/tom/github/tellmesh/tellmesh/.venv/bin/python3 -m uvicorn agents.operators.desktop_operator.main:app
    --host 0.0.0.0 --port 8791
```
