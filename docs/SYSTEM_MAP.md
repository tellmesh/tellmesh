# System map

Source: [`project/map.toon.yaml`](../project/map.toon.yaml), generated 2026-06-15.

This document is the human-readable navigation layer for maintainers. The
checked-in `project/map.toon.yaml` was generated before the package split and
still includes extracted `packages/uri*` sources; regenerate it after the split
stabilizes before using the counts as a strict filesystem inventory.

## Current Snapshot

| Metric | Value |
|--------|-------|
| Modules | 943 |
| Lines | 64968 |
| Functions | 2916 |
| Classes | 0, because the map generator reports function-oriented exports; dataclass-like entries are listed in details |
| Average cyclomatic complexity | 3.7 |
| Critical functions | 22 |
| Dependency cycles | 0 |
| Trend | flat: 3.7 -> 3.7 |

Interpretation of the checked-in snapshot: the project is broad, but the
dependency graph is currently acyclic and average complexity is under the budget documented in
[`URI2RUN_ARCHITECTURE.md`](./URI2RUN_ARCHITECTURE.md). The main risk is not
cycle growth; it is fan-out in orchestration modules and large UI/runtime files.

## Main Runtime Layers

The URI libraries are split packages. In this workspace their local checkouts
live under `/home/tom/github/tellmesh/*`; this repository resolves them through
`tool.uv.sources` in [`pyproject.toml`](../pyproject.toml), currently pointing
at those local checkouts. The matching upstream repositories still live under
`https://github.com/tellmesh/*`. This repository now
owns the control-plane workspace (`resource-agent-hypervisor`,
`resource-agent-factory`, dashboard agent) plus domain packs, operators,
deployments and docs.

| Layer | Main paths | Responsibility |
|-------|------------|----------------|
| URI core | `tellmesh/uri3` package | URI schemes, semantic routing, resolver dispatch, workflow graph, logs, doctor, result envelopes |
| NL planning | `tellmesh/nl2uri` package | Natural language to URI, task, flow and graph plans |
| Flow compiler | `tellmesh/uri2flow` package | Compact URI flow to workflow graph, including `markpact://` flow loading |
| Operation runtime | `tellmesh/uri2ops` package | A2A/MCP framework, dispatcher, union registry (adapters in `agents/operators/`) |
| Runtime transports | `tellmesh/uri2run` package | Python, shell, HTTP, stdio, SSE, WS, Docker, SSH, MCP, A2A, flow and graph transports |
| Capabilities | `tellmesh/touri` package | Capability manifests, matching, fallback and delegation to runtime backends |
| Agent lifecycle | `packages/resource-agent-hypervisor/hypervisor/deployment_registry/` | Deployment registry, run plans, process lifecycle, health, runtime state, supervisor |
| Hypervisor routing | `packages/resource-agent-hypervisor/hypervisor/routing/` | System URI dispatch, operator URI resolution, policy decisions, runtime/environment selection |
| Repair loop | `packages/resource-agent-hypervisor/hypervisor/repair/` | Diagnose, classify, plan, apply playbooks, learn from incidents |
| Agent generation | `packages/resource-agent-factory/generator/` and `agents/generated/*` | Deterministic thin agents from contracts |
| Ecosystem generation | `tellmesh/urigen` package | Proposal, generated ecosystem, verify, explain, apply, rollback |
| URI shell | `tellmesh/urish` package | User-facing `uri` / `urish` commands, policy, shortcuts, dashboard, repair, ticket/evolve |
| Dashboard agent | `agents/system/hypervisor_dashboard/` | API and system-agent UI for observing and controlling hypervisor flows |
| WWW product UI | `www/` | Landing, markdown chat, examples gallery, API bridge, monitor scripts |

## Critical Paths

### NL To Runnable Agent

```text
prompt
  -> urish ask / nl2uri
  -> URI plan or ecosystem proposal
  -> urigen generate or nl2a domain pack
  -> contracts + deployment fragment
  -> generator creates agents/generated/*
  -> hypervisor run-agent
  -> inspect / supervise / repair
```

### URI Execution

```text
uri / urish
  -> policy gate
  -> uri3 explain / semantic routing / workflow
  -> hypervisor routing for system and operator URIs
  -> touri capability match when a capability manifest exists
  -> uri2run transport
  -> uri2ops operation adapter for operator schemes
  -> result envelope with workflow_status, execution_status, service_result_status
```

### Self-Healing Agent Runtime

```text
hypervisor inspect-agent
  -> runtime_state + PID check
  -> /health probe
  -> agent card probe
  -> hypervisor log + process log
  -> readiness report
  -> repair diagnose
  -> prioritized repair plan
  -> hypervisor repair apply
  -> re-inspect after every playbook
```

Important separation:

- `process_status` answers whether the tracked PID is alive.
- `health_status` answers whether the service responds correctly.
- `warning_codes` are non-blocking drift signals.
- `incident_codes` are blocking failures used by the repair planner.

## Structural Hotspots

The map reports these current hotspots:

| Hotspot | Signal | Recommended handling |
|---------|--------|----------------------|
| `createVoiceController` | fan-out 37, CC 29 | Split chat voice UI setup from event binding and API calls |
| `main` | fan-out 30 | Keep command/app bootstrap thin; move behavior into backend modules |
| `mcp_router` | fan-out 25 | Keep MCP request parsing separate from operation dispatch |
| `_render_markdown` | fan-out 25, CC 70 | Split rendering sections and cover with snapshot fixtures |
| `analyze_artifact` | fan-out 24 | Keep artifact analysis rules declarative and fixture-backed |

## Largest Files To Watch

| File | Lines | Note |
|------|-------|------|
| `planfile.yaml` | 1319 | Task backlog and generated tickets |
| `www/generated/integrations-i18n.js` | 1143 | Generated integration UI strings |
| `www/landing.js` | 836 | Product UI tour, language/theme handling, animation, scenario lab |
| `www/app.js` | 731 | Chat and UI behavior |
| `www/landing-i18n.js` | 719 | Landing copy and language resources |
| `packages/resource-agent-hypervisor/hypervisor/agent_describe.py` | 677 | Agent description report rendering |
| `packages/resource-agent-hypervisor/hypervisor/cli.py` | 563 | Hypervisor CLI |
| `packages/resource-agent-hypervisor/hypervisor/contract_registry/uri_resolver.py` | 562 | Contract URI resolution and validation |
| `goal.yaml` | 511 | Goal/test workflow metadata |
| `www/generated/examples-manifest.js` | 477 | Generated examples manifest |
| `scripts/examples/effective_weather_playwright.py` | 466 | Example browser workflow |

## Entry Points Worth Knowing

| Entry point | Purpose |
|-------------|---------|
| `uri` / `urish` | Primary human shell for ask, call, run, repair, ticket, evolve, dashboard |
| `uri3` | URI resolver, workflow, doctor, logs, schema, replay |
| `uri2run` | Runtime transport calls |
| `uri2ops` | Operator task validation, execution and serve mode |
| `touri` | Capability registry validation and capability calls |
| `urigen` | URI ecosystem proposal/generate/verify/explain/apply |
| `hypervisor` | Deployment registry, lifecycle, inspect, supervise, repair |
| `scripts/test-all-examples.sh` | Sequential shell smoke for examples |
| `make ci-gate` | Architecture gate, pytest and examples integration |

## Maintenance Rules

1. Keep generated agents thin. Edit contracts, templates or custom handlers, not
   `agents/generated/*` directly.
2. Keep CLI modules thin. When fan-out rises, move behavior into backend modules
   or declarative registries.
3. Keep `uri3` as the resolver/workflow core. Runtime execution belongs in
   `uri2run` or `uri2ops`.
4. Keep repair bounded and observable. Every autonomous repair must leave
   runtime state, logs, incidents or proposals.
5. Keep `warning_codes` out of blocking repair decisions unless the service is
   actually unhealthy.
6. When changing `www/landing.js` or `www/app.js`, run the WWW smoke and monitor
   tests because those files are now system-facing UX surfaces.

## Verification Commands

```bash
python -m pytest -q tests/hypervisor/test_runtime_state.py \
  tests/hypervisor/test_agent_runner.py \
  tests/hypervisor/test_sprint1_autonomy.py \
  tests/hypervisor/test_agent_lifecycle.py

python -m ruff check packages/resource-agent-hypervisor/hypervisor \
  agents/system/hypervisor_dashboard tests/hypervisor

uri3 doctor
make examples-test
bash scripts/test-all-examples.sh
```

Use the narrow hypervisor test set while editing lifecycle or repair behavior.
Use `uri3 doctor` and `make examples-test` before publishing or changing public
contracts.

## Responsibility Audit

Use the planning audit when deciding the next refactor slice from the generated
TOON snapshots:

```bash
make architecture-responsibility-audit
python scripts/architecture_responsibility_audit.py --format json --out output/architecture-responsibility-audit.json
```

The script reads `project/map.toon.yaml` and `project/duplication.toon.yaml`,
classifies files into system, app, command, domain, runtime, generated and docs
areas, then reports:

- generic packages containing domain vocabulary,
- duplication crossing responsibility boundaries,
- generated snapshots that duplicate source packages,
- large command/app/runtime files that should be split before adding behavior.

It is report-only by default. Use `--fail-on warning` only after known legacy
findings are converted into explicit refactor tasks or exceptions.
