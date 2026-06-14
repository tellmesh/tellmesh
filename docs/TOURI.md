# touri

`touri` is a generic URI-to-capability layer.

It solves this problem:

> Do not create a new library for every new URI. Create a capability manifest that maps the URI to an existing function, script, service, flow, graph, MCP tool, A2A skill, Docker action, or HTTP endpoint.

## Role in the architecture

```txt
nl2uri      -> prompt -> flow/tree/graph
uri2flow    -> compact flow -> workflow graph
uri3        -> URI validation, routing, graph execution
uri2ops     -> OS/UI/browser operations
touri       -> generic new URI -> reusable capability backend
hypervisor  -> lifecycle, policy, deployment, registry
```

## Manifest naming

Use:

```txt
*.uri.capability.yaml
```

`touri` can also load capability manifests from README code blocks:

````md
```markpact:capability weather.forecast.markpact
version: 1
capability:
  id: weather.forecast.markpact
  scheme: weather
  uri_template: weather://markpact/{place}/{days}/html
backend:
  type: python
  target: python://touri_examples.weather:handler
```
````

```bash
touri list markpact://examples/22_markpact_weather/README.md
touri call weather://markpact/Gdansk/14/html \
  --registry markpact://examples/22_markpact_weather/README.md
```

See [`MARKPACT_WITH_TOURI.md`](./MARKPACT_WITH_TOURI.md).

Example:

```yaml
version: 1
capability:
  id: weather.forecast.html
  scheme: weather
  uri_template: weather://forecast/{place}/{days}/html
  operation: generate
  kind: command
backend:
  type: python
  target: python://touri_examples.weather:handler
```

## Backends

MVP supports:

- `python`
- `mock`
- `shell`
- `uri_flow` — expand `*.uri.flow.yaml` via uri2flow, run/dry-run via uri3
- `uri_graph` — load workflow graph YAML, run/dry-run via uri3
- `uri2ops` — dispatch operator schemes through uri2ops operation registry

Planned:

- `http`, `docker`, `mcp`, `a2a`

```yaml
backend:
  type: uri_flow
  flow: examples/15_compact_uri_flow/weather.uri.flow.yaml
  dry_run: true
  browser: mock
```

Register a manifest and verify uri3 resolution:

```bash
touri register examples/20_touri_capabilities/weather_forecast.uri.capability.yaml \
  --registry examples/20_touri_capabilities --install
uri3 explain weather://forecast/Gdansk/14/html
```

Redact secret-like fields in results (default on):

```yaml
policy:
  redact_secrets: true
```

## Data quality

Capability manifests may declare validation policy:

```yaml
data_quality:
  relevance_required: true
  min_confidence: 0.75
  failure_code: PRICE_RESULT_NOT_RELEVANT
  validators:
    - python://validators.price:validate_relevance
```

Results use the shared [`ServiceResult`](./SERVICE_RESULT.md) envelope with three status levels. See [`ANTI_TELLM.md`](./ANTI_TELLM.md).

## Fallbacks

When primary backend or data quality fails, optional fallbacks may run:

```yaml
fallbacks:
  - when: PRICE_RESULT_NOT_RELEVANT
    backend:
      type: mock
  - when: any
    backend:
      type: python
      target: python://providers.ceneo:search
```

## URI resolution

```bash
uri3 explain weather://forecast/Gdansk/14/html
```

Resolution order: uri3 → touri → uri2ops → hypervisor → denied (`config/touri.uri.yaml`).

## Security

Secrets should be referenced by URI, not embedded directly:

```yaml
api_key: env://OPENROUTER_API_KEY
```

`touri` should return structured service results and avoid logging secret payloads.

Voice capability pack (STT/TTS): [`VOICE_WITH_TOURI.md`](./VOICE_WITH_TOURI.md).
