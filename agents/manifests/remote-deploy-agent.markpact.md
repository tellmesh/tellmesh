# remote-deploy-agent

Deploy, verify and start generated agents on remote SSH hosts.

Canonical portable definition: contract, deployment, runtime and optional Docker service.

Sync: `hypervisor sync-agent-manifest remote-deploy-agent.local`

```markpact:agent remote-deploy-agent
version: 1
agent:
  id: agent://remote-deploy-agent
  name: remote-deploy-agent
  implementation: custom
  contract: contracts/agents/remote_deploy_agent.yaml
  package: agents/custom/remote_deploy_agent
  module: agents.custom.remote_deploy_agent.main:app
  version: 0.1.0
  python_package: remote_deploy_agent
  description: Deploy, verify and start generated agents on remote SSH hosts.
capabilities:
- name: plan_remote_deploy
  type: command
  uri: deploy://agents/plan
  command: PlanRemoteDeploy
  input_schema: app.deploy.v1.PlanRemoteDeployCommand
  output_schema: app.deploy.v1.RemoteDeployPlan
  renderer: detail
  description: Build rsync/verify plan for an SSH deployment selector.
- name: apply_remote_deploy
  type: command
  uri: deploy://agents/apply
  command: ApplyRemoteDeploy
  input_schema: app.deploy.v1.ApplyRemoteDeployCommand
  output_schema: app.deploy.v1.RemoteDeployResult
  renderer: detail
  description: Sync generated agent package to remote host and verify path.
- name: verify_remote_agent
  type: command
  uri: deploy://agents/verify
  command: VerifyRemoteAgent
  input_schema: app.deploy.v1.VerifyRemoteAgentCommand
  output_schema: app.deploy.v1.RemoteVerifyResult
  renderer: detail
  description: Verify SSH connectivity, remote path and health endpoint.
- name: start_remote_agent
  type: command
  uri: deploy://agents/start
  command: StartRemoteAgent
  input_schema: app.deploy.v1.StartRemoteAgentCommand
  output_schema: app.deploy.v1.RemoteStartResult
  renderer: detail
  description: Start agent process on remote host via SSH nohup and optional health
    wait.
- name: deploy_verify_start
  type: command
  uri: workflow://agents/deploy-verify-start
  command: DeployVerifyStart
  input_schema: app.deploy.v1.DeployVerifyStartCommand
  output_schema: app.deploy.v1.DeployVerifyStartResult
  renderer: detail
  description: End-to-end remote deploy, verify and start for an SSH deployment selector.
```

```markpact:deployment remote-deploy-agent.local
deployment:
  id: remote-deploy-agent.local
  agent_ref: agent://remote-deploy-agent
  target_uri: local://agents/custom/remote_deploy_agent
  status: generated
  health_uri: http://localhost:8135/health
  card_uri: http://localhost:8135/.well-known/agent-card.json
  view_uri: view://process/agent/remote-deploy-agent.local/latest
metadata:
  source: custom_agent
  role: remote_deploy_orchestrator
  contract: contracts/agents/remote_deploy_agent.yaml
runtime:
  run: hypervisor run-agent remote-deploy-agent.local --detach --wait-healthy
  inspect: hypervisor inspect-agent remote-deploy-agent.local
  describe: hypervisor describe-agent remote-deploy-agent.local
supervise:
  once: hypervisor supervise remote-deploy-agent.local --repair auto
  watch: hypervisor supervise remote-deploy-agent.local --watch --repair auto --interval
    15
logs:
  hypervisor: log://hypervisor?grep=remote-deploy-agent.local
  process: log://file/output/logs/agents/remote-deploy-agent.local.process.log
manifest:
  self: markpact://agents/manifests/remote-deploy-agent.markpact.md
```

```markpact:runtime remote-deploy-agent.local
runtime:
  module: agents.custom.remote_deploy_agent.main:app
  path: /home/tom/github/wronai/hypervisor/agents/custom/remote_deploy_agent
  port: 8135
  health_uri: http://localhost:8135/health
  card_uri: http://localhost:8135/.well-known/agent-card.json
  command: /home/tom/github/wronai/hypervisor/.venv/bin/python3 -m uvicorn agents.custom.remote_deploy_agent.main:app
    --host 0.0.0.0 --port 8135
```
