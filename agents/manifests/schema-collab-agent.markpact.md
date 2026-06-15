# schema-collab-agent

Generated from NL prompt: stworz nowego agenta schema-collab-agent, ktory czyta file:// README, sprawdza device://device/sensor-1/status i robot://robot/amr-1/state oraz ma komende cron monitor

Canonical portable definition: contract, deployment, runtime and optional Docker service.

Sync: `hypervisor sync-agent-manifest schema-collab-agent.local`

```markpact:agent schema-collab-agent
version: 1
agent:
  id: agent://schema-collab-agent
  name: schema-collab-agent
  implementation: generated
  contract: contracts/agents/schema_collab_agent.yaml
  package: agents/generated/schema_collab_agent
  module: agents.generated.schema_collab_agent.main:app
  version: 0.1.0
  python_package: schema_collab_agent
  description: 'Generated from NL prompt: stworz nowego agenta schema-collab-agent,
    ktory czyta file:// README, sprawdza device://device/sensor-1/status i robot://robot/amr-1/state
    oraz ma komende cron monitor'
capabilities:
- name: read_markpact_source
  type: resource_read
  uri: file://agents/generated/schema_collab_agent/README.md
  output_schema: app.codex.v1.MarkpactSourceView
  renderer: text
  description: Read generated agent README/provenance through file://.
- name: read_device_status
  type: resource_read
  uri: device://device/sensor-1/status
  output_schema: operator.device.v1.DeviceStatus
  renderer: detail
  description: Read device status through uri2ops.
- name: read_robot_state
  type: resource_read
  uri: robot://robot/amr-1/state
  output_schema: operator.robot.v1.RobotState
  renderer: detail
  description: Read robot state through uri2ops.
- name: run_cron_monitor
  type: command
  uri: cron://www/monitor/landing
  command: RunCronMonitor
  input_schema: app.codex.v1.RunCronMonitorCommand
  emits:
  - CronMonitorRequested
  description: Dispatch a scheduled monitor through cron:// URI.
```

```markpact:deployment schema-collab-agent.local
deployment:
  id: schema-collab-agent.local
  agent_ref: agent://schema-collab-agent
  target_uri: local://agents/generated/schema_collab_agent
  status: generated
  health_uri: http://localhost:8131/health
  card_uri: http://localhost:8131/.well-known/agent-card.json
  view_uri: view://process/agent/schema-collab-agent.local/latest
metadata:
  source: nl_agent_factory
  contract: contracts/agents/schema_collab_agent.yaml
runtime:
  run: hypervisor run-agent schema-collab-agent.local --detach --wait-healthy
  inspect: hypervisor inspect-agent schema-collab-agent.local
  describe: hypervisor describe-agent schema-collab-agent.local
supervise:
  once: hypervisor supervise schema-collab-agent.local --repair auto
  watch: hypervisor supervise schema-collab-agent.local --watch --repair auto --interval
    15
logs:
  hypervisor: log://hypervisor?grep=schema-collab-agent.local
  process: log://file/output/logs/agents/schema-collab-agent.local.process.log
manifest:
  self: markpact://agents/manifests/schema-collab-agent.markpact.md
```

```markpact:runtime schema-collab-agent.local
runtime:
  module: agents.generated.schema_collab_agent.main:app
  path: /home/tom/github/wronai/hypervisor/agents/generated/schema_collab_agent
  port: 8131
  health_uri: http://localhost:8131/health
  card_uri: http://localhost:8131/.well-known/agent-card.json
  command: /home/tom/github/wronai/hypervisor/.venv/bin/python3 -m uvicorn agents.generated.schema_collab_agent.main:app
    --host 0.0.0.0 --port 8131
```

```markpact:docker schema-collab-agent
service:
  name: schema-collab-agent
  build:
    context: .
    dockerfile: agents/generated/schema_collab_agent/Dockerfile
  container_name: schema-collab-agent
  ports:
  - 8131:8131
  healthcheck:
    test:
    - CMD
    - curl
    - -f
    - http://localhost:8131/health
  environment:
    RESOURCE_RUNTIME_URL: http://host.docker.internal:8000
compose:
  output: output/deployments/schema-collab-agent/docker-compose.yaml
```
