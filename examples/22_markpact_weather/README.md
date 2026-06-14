# Example 22: markpact capability for touri

This README is a `markpact://` registry for `touri`.

It defines a `weather://...` capability directly in Markdown:

```markpact:capability weather.forecast.markpact
version: 1

capability:
  id: weather.forecast.markpact
  scheme: weather
  uri_template: weather://markpact/{place}/{days}/html
  operation: generate
  kind: command
  description: Generate demo weather HTML artifact result from a markpact README.

input:
  params:
    place:
      type: string
    days:
      type: integer
      default: 14

output:
  result_type: artifact
  schema:
    type: object
    properties:
      html_url:
        type: string
      artifact_uri:
        type: string

backend:
  type: python
  target: python://touri_examples.weather:handler

policy:
  side_effects: true
  requires_approval: false

events:
  emits:
    - WeatherForecastRequested
    - WeatherForecastGenerated
```

## Try It

```bash
touri list markpact://examples/22_markpact_weather/README.md
```

```bash
touri call weather://markpact/Gdansk/14/html \
  --registry markpact://examples/22_markpact_weather/README.md
```

You can also select a single capability by fragment:

```bash
touri list markpact://examples/22_markpact_weather/README.md#weather.forecast.markpact
```

## Compact flow for uri2flow

The same README can declare a compact URI flow block:

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

Expand it with uri2flow:

```bash
uri2flow expand markpact://examples/22_markpact_weather/README.md#weather-health \
  --out output/weather-health.uri.graph.yaml
```

Compare with the YAML source flow:

```bash
uri2flow expand examples/15_compact_uri_flow/weather.uri.flow.yaml
```
