# Architecture v0.5

Skanowanie usług, graf URI i `nl2uri` są w paczkach `uri3` / `nl2uri`. Hypervisor zarządza rejestrem, polityką i lifecycle.

## Podział odpowiedzialności

```txt
uri3       = discovery, routing, graph, validation, log://, schema introspection
nl2uri     = natural language -> URI Tree
nl2a       = prompt -> URI Tree -> Domain Pack -> agent
hypervisor = policy, registry, lifecycle, deployment
generator  = deterministyczny kod cienkiego agenta
Domain Pack = logika domenowa (domains/*)
Generated Agent = cienki adapter (agents/generated/*)
```

## Monorepo

```txt
packages/uri3/
packages/nl2uri/          (+ nl2a)
packages/resource-agent-hypervisor/
packages/resource-agent-factory/
```

Wspólne zasoby repo: `contracts/`, `schemas/`, `domains/`, `agents/`, `deployments/`, `tests/`.

Instalacja: [`packages/README.md`](../packages/README.md).

## Pipeline

```txt
prompt -> nl2uri -> URI Tree -> uri3 validate/graph
       -> Domain Pack -> contracts/agents/*.yaml
       -> generator -> agents/generated/<agent>/
       -> deployment registry sync
```

## Przykłady

Uporządkowane w [`examples/`](../examples/README.md) (`examples/*/*`):

- lokalny quickstart,
- skan HTTP,
- Docker + SSH testenv,
- weather-map nl2a,
- meta repair,
- orders/invoices,
- evolution proposals.

## Dokumentacja

- [`docs/URI3.md`](./URI3.md)
- [`docs/NL2URI.md`](./NL2URI.md)
- [`docs/NL2A_DOMAIN_PACKS.md`](./NL2A_DOMAIN_PACKS.md)
- [`docs/DEPLOYMENT.md`](./DEPLOYMENT.md)
- [`docs/META_AGENT.md`](./META_AGENT.md)
