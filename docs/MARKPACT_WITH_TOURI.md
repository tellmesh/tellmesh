# Markpact With touri and uri2flow

`touri` and `uri2flow` can load declarations from Markdown README files through
`markpact://` registry references.

This keeps the execution boundary unchanged:

```txt
README.md -> markpact block -> validated manifest/flow -> runtime
```

The loaders only parse fenced code blocks. They do not execute `markpact`.

## Capability Blocks (touri)

Use a fenced block named `markpact:capability`:

````md
```markpact:capability weather.forecast.markpact
version: 1

capability:
  id: weather.forecast.markpact
  scheme: weather
  uri_template: weather://markpact/{place}/{days}/html
  operation: generate
  kind: command

backend:
  type: python
  target: python://touri_examples.weather:handler
```
````

Then use the README as the `touri` registry:

```bash
touri list markpact://examples/22_markpact_weather/README.md

touri call weather://markpact/Gdansk/14/html \
  --registry markpact://examples/22_markpact_weather/README.md
```

Fragments select one block:

```bash
touri list markpact://examples/22_markpact_weather/README.md#weather.forecast.markpact
```

## Flow Blocks (uri2flow)

Use a fenced block named `markpact:flow`:

````md
```markpact:flow weather-health
flow:
  id: weather-health
  description: Generate weather agent, run it locally and verify health in Chrome.

do:
  - agent://weather-generator
  - hypervisor://local/weather-agent/run
  - browser://chrome/page/open:
      url: http://localhost:8101/health
```
````

Expand it with uri2flow:

```bash
uri2flow expand markpact://examples/22_markpact_weather/README.md#weather-health \
  --out output/weather-health.uri.graph.yaml

uri2flow validate markpact://examples/22_markpact_weather/README.md#weather-health
uri2flow print markpact://examples/22_markpact_weather/README.md#weather-health
```

When a README contains multiple `markpact:flow` blocks, specify `#flow.id` in the URI.

## Example

See [`examples/22_markpact_weather`](../examples/22_markpact_weather/README.md).

## Scope

Implemented now:

```txt
markpact:capability -> touri load_registry/call/list
markpact:flow       -> uri2flow load_flow/expand/validate/print
```

Planned later:

```txt
uri3 scan markpact://...
uri3 scan pactown://workspace/...
nlp2dsl export -> markpact README
iterun retry/repair for uri3 run-workflow
```

## Security

- `markpact://` provides declarations only
- `touri` / `uri2flow` validate structure before execution
- Do not auto-run `markpact:run` blocks when loading registries
