# hypervisor-dashboard

System observer/renderer agent — URI process dashboard with approval-gated actions.

Canonical portable definition: contract, deployment, runtime and optional Docker service.

Sync: `hypervisor sync-agent-manifest hypervisor-dashboard.local`

```markpact:agent hypervisor-dashboard
version: 1
agent:
  id: agent://hypervisor-dashboard
  name: hypervisor-dashboard
  implementation: system
  contract: contracts/agents/hypervisor_dashboard_agent.yaml
  package: agents/system/hypervisor_dashboard
  module: agents.system.hypervisor_dashboard.main:app
  version: 0.1.0
  python_package: hypervisor_dashboard_agent
  description: "System observer/renderer agent \u2014 URI process dashboard with approval-gated\
    \ actions."
capabilities:
- name: process_view
  type: resource_read
  uri: resource://dashboard/process/agent/{agent_id}/latest
  output_schema: dashboard.v1.ProcessView
  renderer: html
  description: Render latest process view for a deployed agent.
- name: workflow_timeline
  type: resource_read
  uri: resource://dashboard/workflow/{workflow_id}/timeline
  output_schema: dashboard.v1.WorkflowTimelineView
  renderer: html
  description: Render workflow timeline view.
- name: incident_explain
  type: resource_read
  uri: resource://dashboard/incident/{incident_id}/explain
  output_schema: dashboard.v1.IncidentExplainView
  renderer: html
  description: Explain an incident artifact.
- name: repair_diagnose
  type: resource_read
  uri: resource://dashboard/repair/agent/{agent_id}/diagnosis
  output_schema: dashboard.v1.RepairDiagnosisView
  renderer: json
  description: Diagnose agent health and build repair plan envelope.
- name: repair_action
  type: command
  uri: repair://agent/{agent_id}/apply
  command: ApplySafeRepair
  input_schema: dashboard.v1.ApplySafeRepairCommand
  description: Apply safe repair playbooks (requires approval).
- name: uri_call
  type: command
  uri: hypervisor://dashboard/uri/call
  command: UriCall
  input_schema: dashboard.v1.UriCallCommand
  description: Execute URI through dashboard policy gate.
```

```markpact:deployment hypervisor-dashboard.local
deployment:
  id: hypervisor-dashboard.local
  agent_ref: agent://hypervisor-dashboard
  target_uri: local://agents/system/hypervisor_dashboard
  status: generated
  health_uri: http://localhost:8788/health
  card_uri: http://localhost:8788/.well-known/agent-card.json
  view_uri: view://process/agent/hypervisor-dashboard.local/latest
metadata:
  source: system_agent
  role: observer_renderer_controller
  contract: contracts/agents/hypervisor_dashboard_agent.yaml
runtime:
  run: hypervisor run-agent hypervisor-dashboard.local --detach --wait-healthy
  inspect: hypervisor inspect-agent hypervisor-dashboard.local
  describe: hypervisor describe-agent hypervisor-dashboard.local
supervise:
  once: hypervisor supervise hypervisor-dashboard.local --repair auto
  watch: hypervisor supervise hypervisor-dashboard.local --watch --repair auto --interval
    15
logs:
  hypervisor: log://hypervisor?grep=hypervisor-dashboard.local
  process: log://file/output/logs/agents/hypervisor-dashboard.local.process.log
manifest:
  self: markpact://agents/manifests/hypervisor-dashboard.markpact.md
```

```markpact:runtime hypervisor-dashboard.local
runtime:
  module: agents.system.hypervisor_dashboard.main:app
  path: /home/tom/github/wronai/hypervisor/agents/system/hypervisor_dashboard
  port: 8788
  health_uri: http://localhost:8788/health
  card_uri: http://localhost:8788/.well-known/agent-card.json
  command: /home/tom/github/wronai/hypervisor/.venv/bin/python3 -m uvicorn agents.system.hypervisor_dashboard.main:app
    --host 0.0.0.0 --port 8788
```
