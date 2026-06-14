# uri2pact

Shared loader for `markpact://` registries embedded in README files.

Used by:

- `touri` — `markpact:capability` blocks → capability manifests
- `uri2flow` — `markpact:flow` blocks → compact URI flows

## Example

```bash
touri list markpact://examples/22_markpact_weather/README.md
uri2flow expand markpact://examples/22_markpact_weather/README.md#weather-local-health
```

See [`docs/MARKPACT_WITH_TOURI.md`](../../docs/MARKPACT_WITH_TOURI.md).
