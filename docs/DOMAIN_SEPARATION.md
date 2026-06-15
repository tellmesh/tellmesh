# Domain Separation

The system separates generic libraries from project/domain data.

## Rule

Generic packages may implement loaders, validators, routers and execution
adapters. They must not embed business scenarios, specific customer workflows or
generated agent facts.

| Layer | Allowed | Not allowed |
|------|---------|-------------|
| `tellmesh/urish` package | NL shell, URI planning facade, scenario registry loader | Invoice, WooCommerce, ZUS, ERP, bank-specific scenario data |
| `tellmesh/uri3` package | Semantic URI routing, graph execution, log/resource schemes | Project-specific workflow examples as hidden defaults |
| `tellmesh/uri2ops` package | Operation registry loader, A2A/MCP serve runtime, dispatcher, policy | Business workflows, scenario routing, adapter implementations |
| `packages/resource-agent-factory` | Generate agents from contracts | Hand-authored generated output |
| `agents/` | Generated agents, scenario registries, markpact provenance | Generic runtime code |
| `agents/operators/` | Capability-agent contracts, registries, adapters, deployment entry | Domain scenarios, customer workflow defaults |
| `agents/system/` | Control-plane agents (dashboard) — thin deployment entry | Generic runtime libraries |
| `domains/*` | Domain packs, workflow vocabulary, scenario registries | Desktop adapter implementation |
| `examples/` | Demonstrations and mock workflows | Required hidden runtime state |

## Current Fix

The former office routing data in the pre-split `urish.office_*` modules:

```txt
urish.office_intent
urish.office_scenarios
```

has been moved to:

```txt
domains/office/scenario_registry.yaml
domains/office/README.md          # markpact:scenario + markpact:scenario_registry
agents/scenarios/                 # pointer README only
```

The old `urish.office_*` compatibility modules have been removed. Use the
generic scenario registry API instead:

```python
from urish.scenario_registry import match_scenario, scenarios_for_kind

scenario = match_scenario(prompt, kind="office")
all_office_scenarios = scenarios_for_kind("office")
```

## How `urish` Uses It

```text
NL prompt
  -> urish.intent.detect_intent
  -> urish.scenario_registry loads domains/*/scenario_registry.yaml + markpact scenarios
  -> planned_uris + next_steps + artifact refs
```

Override the scenario source:

```bash
URISH_SCENARIO_REGISTRY=/path/to/project/agents/scenarios urish ask "..."
```

## Operator Domain Boundaries

Operator capability agents use dedicated domain packs and fixed deployment
profiles:

```txt
agents/operators/browser_operator/        -> domains/browser_ops/    (:8793)
agents/operators/desktop_operator/        -> domains/desktop_ops/    (:8791)
agents/operators/device_robot_operator/   -> domains/physical_ops/   (:8792)
agents/system/hypervisor_dashboard/       -> control plane UI        (:8788)
```

Each pack describes operator capability vocabulary and NL routing. It must not
contain office, invoice, bank or other vertical workflow data.

Domain packages may reference operation URIs in their own workflows. The
domain remains in `domains/<domain>/`; URI normalization lives in the
installed `uri3.routing` package from `tellmesh/uri3`; operator selection,
deployment, policy and audit remain in `hypervisor`; the `uri2ops` framework
(A2A/MCP/dispatcher) lives in the installed `tellmesh/uri2ops` package;
executable adapters live in `agents/operators/<name>/adapters/`.

Guide: [`DESKTOP_AUTONOMY.md`](./DESKTOP_AUTONOMY.md).

## Audit Notes

Known demo seeds that still contain example-specific names:

- `tellmesh/nl2uri` planner templates and graph/flow planners contain
  weather demo defaults used by examples and deterministic tests.
- the split `tellmesh/urigen` package contains sample capability/flow mappings
  and demo URIs for generated ecosystems.
- the split `tellmesh/urigen` generator still emits a weather demo deployment
  when no explicit agent profile is supplied.
- the split `tellmesh/uri3` package contains mirrored example contracts for the bundled
  weather demo.

Those are demo-generation defaults, not the generic chat router. They should be
converted into profile artifacts when `urigen` profiles are externalized.

## Generated Agent Provenance

Every generated agent README should expose:

- source contract URI/path,
- contract hash,
- exact generation command,
- runtime command,
- `log://` URIs,
- `markpact:agent_generation` and `markpact:run_log` blocks.

This makes generated output reproducible and inspectable without reading package
internals.
