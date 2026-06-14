# nl2uri

`nl2uri` tłumaczy query w języku naturalnym na `URI Tree`.

## CLI

```bash
nl2uri generate --no-llm -p "generuj mape pogody dwa tygodnie do przodu w html" \
  --out domains/weather_map/uri_tree.yaml
```

Bez `--out` wypisuje YAML/JSON na stdout.

## Zachowanie

- domyślnie próbuje LLM (OpenRouter przez `.env`),
- z `--no-llm` używa plannera regułowego (reprodukowalne testy),
- wynik waliduj przez `uri3 validate-tree`.

## Powiązane

- [`docs/NL2A_DOMAIN_PACKS.md`](./NL2A_DOMAIN_PACKS.md) — pełny pipeline z Domain Pack
- [`examples/04_nl2a_weather_map/`](../examples/04_nl2a_weather_map/README.md)
- [`examples/01_quickstart_local/`](../examples/01_quickstart_local/README.md)
