# device-robot-operator

Generic physical device and robot operation agent backed by uri2ops.

Canonical portable definition: contract, deployment, runtime and optional Docker service.

Sync: `hypervisor sync-agent-manifest device-robot-operator.local`

```markpact:agent device-robot-operator
version: 1
agent:
  id: agent://device-robot-operator
  name: device-robot-operator
  implementation: operator
  contract: agents/operators/device_robot_operator/device_robot_operator.yaml
  package: agents/operators/device_robot_operator
  module: agents.operators.device_robot_operator.main:app
operator:
  kind: hypervisor.operator_agent
  runtime_package: agents/operators/device_robot_operator
```

```markpact:deployment device-robot-operator.local
deployment:
  id: device-robot-operator.local
  agent_ref: agent://device-robot-operator
  target_uri: local://agents/operators/device_robot_operator
  status: generated
  health_uri: http://localhost:8792/health
  card_uri: http://localhost:8792/.well-known/agent-card.json
  view_uri: view://process/agent/device-robot-operator.local/latest
metadata:
  source: operator_agent
  role: device_robot_operator
  contract: agents/operators/device_robot_operator/device_robot_operator.yaml
  domain_pack: domains/physical_ops/domain.yaml
  operator_registry: domains/physical_ops/operator_registry.yaml
  expected_service: uri2ops
runtime:
  run: hypervisor run-agent device-robot-operator.local --detach --wait-healthy
  inspect: hypervisor inspect-agent device-robot-operator.local
  describe: hypervisor describe-agent device-robot-operator.local
supervise:
  once: hypervisor supervise device-robot-operator.local --repair auto
  watch: hypervisor supervise device-robot-operator.local --watch --repair auto --interval
    15
logs:
  hypervisor: log://hypervisor?grep=device-robot-operator.local
  process: log://file/output/logs/agents/device-robot-operator.local.process.log
manifest:
  self: markpact://agents/manifests/device-robot-operator.markpact.md
env:
  URI2OPS_BASE_URL: http://localhost:8792
```

```markpact:runtime device-robot-operator.local
runtime:
  module: agents.operators.device_robot_operator.main:app
  path: /home/tom/github/wronai/hypervisor/agents/operators/device_robot_operator
  port: 8792
  health_uri: http://localhost:8792/health
  card_uri: http://localhost:8792/.well-known/agent-card.json
  command: /home/tom/github/wronai/hypervisor/.venv/bin/python3 -m uvicorn agents.operators.device_robot_operator.main:app
    --host 0.0.0.0 --port 8792
```
