# Documentation index

## Start here

- [`README.md`](../README.md) — instalacja, Makefile, przykłady
- [`examples/README.md`](../examples/README.md) — katalog `examples/*/*`
- [`CHANGELOG.md`](../CHANGELOG.md) · [`TODO.md`](../TODO.md)

## v0.6 (aktualne)

| Dokument | Temat |
|----------|--------|
| [`FLOW_FORMAT.md`](./FLOW_FORMAT.md) | Compact URI flow — format wejściowy |
| [`URI2FLOW.md`](./URI2FLOW.md) | Kompilator compact flow → workflow graph |
| [`URI2OPS.md`](./URI2OPS.md) | Operator runtime, adaptery, `uri2ops serve` |
| [`TOURI.md`](./TOURI.md) | Capability manifests `*.uri.capability.yaml`, backend routing |
| [`MARKPACT_WITH_TOURI.md`](./MARKPACT_WITH_TOURI.md) | `markpact://` capability loader for `touri`, flow loader for `uri2flow` |
| [`VOICE_WITH_TOURI.md`](./VOICE_WITH_TOURI.md) | STT/TTS as a `touri` capability pack |
| [`SERVICE_RESULT.md`](./SERVICE_RESULT.md) | Shared result envelope (`workflow_status`, `ErrorEnvelope`) |
| [`ANTI_TELLM.md`](./ANTI_TELLM.md) | Safeguards vs tellm-style LLM/provider failures |
| [`OPERATOR_RUNTIME.md`](./OPERATOR_RUNTIME.md) | Przepływ validate → plan → run |
| [`URI_OPERATION_REGISTRY.md`](./URI_OPERATION_REGISTRY.md) | Format operation registry |
| [`OPERATOR_SECURITY.md`](./OPERATOR_SECURITY.md) | Polityka, redaction, artifact URIs |
| [`NL2URI.md`](./NL2URI.md) | Multi-output, task/graph, LLM planner |
| [`URI3.md`](./URI3.md) | Workflow CLI: `validate/plan/run-workflow` |
| [`ROADMAP.md`](./ROADMAP.md) | v0.6 done + v0.7 plan |

## v0.5

| Dokument | Temat |
|----------|--------|
| [`HYPERVISOR_WORKFLOW.md`](./HYPERVISOR_WORKFLOW.md) | Generacja + run-agent + logi |
| [`CONFIG_URI_YAML.md`](./CONFIG_URI_YAML.md) | Konwencja `*.uri.yaml` |
| [`ARCHITECTURE_V0_5.md`](./ARCHITECTURE_V0_5.md) | Podział uri3 / nl2uri / uri2ops / hypervisor |
| [`NL2A_DOMAIN_PACKS.md`](./NL2A_DOMAIN_PACKS.md) | Domain Pack pipeline |
| [`DEPLOYMENT.md`](./DEPLOYMENT.md) | Lokalnie, Docker, hypervisor `run-agent` |
| [`META_AGENT.md`](./META_AGENT.md) | Meta-agent CLI/API |
| [`EVOLUTION.md`](./EVOLUTION.md) | Evolution proposals |
| [`AUTO_EVOLUTION_PIPELINE.md`](./AUTO_EVOLUTION_PIPELINE.md) | Kontrolowana autoewolucja |
| [`STANDARDS.md`](./STANDARDS.md) | MCP, Protobuf, JSON Schema |

## Pakiet uri2flow

| Dokument | Temat |
|----------|--------|
| [`../packages/uri2flow/README.md`](../packages/uri2flow/README.md) | CLI, format, pipeline |
| [`../packages/uri2flow/docs/FLOW_FORMAT.md`](../packages/uri2flow/docs/FLOW_FORMAT.md) | Spec compact flow |
| [`../packages/uri2flow/CHANGELOG.md`](../packages/uri2flow/CHANGELOG.md) | Historia v0.1 |

## Pakiet uri2ops

| Dokument | Temat |
|----------|--------|
| [`../packages/uri2ops/README.md`](../packages/uri2ops/README.md) | CLI, adaptery, przykłady |
| [`../packages/uri2ops/CHANGELOG.md`](../packages/uri2ops/CHANGELOG.md) | Historia v0.1–v0.5 |
| [`../packages/uri2ops/TODO.md`](../packages/uri2ops/TODO.md) | Roadmapa pakietu |

## Pakiet touri

| Dokument | Temat |
|----------|--------|
| [`TOURI.md`](./TOURI.md) | Manifesty `*.uri.capability.yaml`, backend routing |
| [`../packages/touri/README.md`](../packages/touri/README.md) | CLI, install, demo |
| [`../packages/touri/CHANGELOG.md`](../packages/touri/CHANGELOG.md) | Historia v0.1 |

## Kontrakty i generator

| Dokument | Temat |
|----------|--------|
| [`CONTRACTS.md`](./CONTRACTS.md) | Format YAML agentów |
| [`GENERATOR.md`](./GENERATOR.md) | Agent factory |
| [`CONTRACT_REGISTRY.md`](./CONTRACT_REGISTRY.md) | Registry kontraktów |
| [`COMPATIBILITY_GOVERNANCE.md`](./COMPATIBILITY_GOVERNANCE.md) | Zasady kompatybilności |
| [`CAPABILITY_VERIFICATION.md`](./CAPABILITY_VERIFICATION.md) | Weryfikacja capability |

## Historyczne

| Dokument | Uwaga |
|----------|--------|
| [`URI2LLM.md`](./URI2LLM.md) | → dziś `uri3.resolvers` |
| [`HYPERVISOR_V0_4.md`](./HYPERVISOR_V0_4.md) | nl2a, uri2llm |
| [`HYPERVISOR_V0_3.md`](./HYPERVISOR_V0_3.md) | contract registry v0.3 |
| [`HYPERVISOR_V0_2.md`](./HYPERVISOR_V0_2.md) | wczesna architektura |
| [`ARCHITECTURE.md`](./ARCHITECTURE.md) | ogólna architektura |
| [`ARCHITECTURE_META_FACTORY.md`](./ARCHITECTURE_META_FACTORY.md) | meta-factory |

## Makefile (skrót)

```bash
make uri-tree graph nl2a-weather test
make validate generate verify
make meta-repair meta-pipeline
make docker-ssh-up scan-http docker-ssh-down
make evolution-check
make run-weather-agent
```

## Testy

```bash
python -m pytest -q
uri2ops registry validate
```
