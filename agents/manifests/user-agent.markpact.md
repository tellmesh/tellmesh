# user-agent

Thin generated agent for reading users and dispatching user commands.

Canonical portable definition: contract, deployment, runtime and optional Docker service.

Sync: `hypervisor sync-agent-manifest user-agent.local`

```markpact:agent user-agent
version: 1
agent:
  id: agent://user-agent
  name: user-agent
  implementation: generated
  contract: contracts/agents/user_agent.yaml
  package: agents/generated/user_agent
  module: agents.generated.user_agent.main:app
  version: 0.1.0
  python_package: user_agent
  description: Thin generated agent for reading users and dispatching user commands.
capabilities:
- name: read_user
  type: resource_read
  uri: resource://users/{user_id}
  output_schema: app.users.v1.UserView
  renderer: detail
  description: Read a single user view by user_id.
- name: read_user_roles
  type: resource_read
  uri: resource://users/{user_id}/roles
  output_schema: app.users.v1.UserRolesView
  renderer: table
  description: Read roles assigned to a user.
- name: create_user
  type: command
  command: CreateUser
  input_schema: app.users.v1.CreateUserCommand
  emits:
  - UserCreated
  description: Create a user by emitting UserCreated.
- name: assign_user_role
  type: command
  command: AssignUserRole
  input_schema: app.users.v1.AssignUserRoleCommand
  emits:
  - UserRoleAssigned
  description: Assign a role to a user.
```

```markpact:deployment user-agent.local
deployment:
  id: user-agent.local
  agent_ref: agent://user-agent
  target_uri: local://agents/generated/user_agent
  status: generated
  health_uri: http://localhost:8102/health
  card_uri: http://localhost:8102/.well-known/agent-card.json
  view_uri: view://process/agent/user-agent.local/latest
metadata:
  source: contract
  contract: contracts/agents/user_agent.yaml
runtime:
  run: hypervisor run-agent user-agent.local --detach --wait-healthy
  inspect: hypervisor inspect-agent user-agent.local
  describe: hypervisor describe-agent user-agent.local
supervise:
  once: hypervisor supervise user-agent.local --repair auto
  watch: hypervisor supervise user-agent.local --watch --repair auto --interval 15
logs:
  hypervisor: log://hypervisor?grep=user-agent.local
  process: log://file/output/logs/agents/user-agent.local.process.log
manifest:
  self: markpact://agents/manifests/user-agent.markpact.md
```

```markpact:runtime user-agent.local
runtime:
  module: agents.generated.user_agent.main:app
  path: /home/tom/github/wronai/hypervisor/agents/generated/user_agent
  port: 8102
  health_uri: http://localhost:8102/health
  card_uri: http://localhost:8102/.well-known/agent-card.json
  command: /home/tom/github/wronai/hypervisor/.venv/bin/python3 -m uvicorn agents.generated.user_agent.main:app
    --host 0.0.0.0 --port 8102
```

```markpact:docker user-agent
service:
  name: user-agent
  build:
    context: .
    dockerfile: agents/generated/user_agent/Dockerfile
  container_name: user-agent
  ports:
  - 8102:8102
  healthcheck:
    test:
    - CMD
    - curl
    - -f
    - http://localhost:8102/health
  environment:
    RESOURCE_RUNTIME_URL: http://host.docker.internal:8000
compose:
  output: output/deployments/user-agent/docker-compose.yaml
```
