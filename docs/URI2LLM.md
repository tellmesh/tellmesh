# uri2llm routing layer

> **Historyczny dokument (v0.4).** Resolver URI jest dziś w paczce **`uri3`** (`uri3.resolvers.router`). Hypervisor korzysta z cienkiego adaptera `hypervisor.uri.client.Uri3Client`. Aktualne API: [`docs/URI3.md`](./URI3.md).

`uri2llm` była warstwą routingu hypervisora — mapowaniem typowanych adresów URI na modele, sekrety, protokoły, funkcje, pakiety i zasoby.

## Supported URI schemes

```txt
env://OPENROUTER_API_KEY
llm://openrouter/qwen/qwen3-coder-next
log://hypervisor?level=ERROR
python://domains.weather_map.handlers.generate_weather_map:handler
pypi://httpx
resource://weather/maps/{place}/forecast/{days}
domain://weather-map
a2a://weather-map-agent/.well-known/agent-card.json
mcp://weather-map-agent/resources/read
artifact://weather-map/Gdansk/forecast/14/index.html
ssh://deploy@localhost:2222/opt/agents
```

Introspection opcji: `uri3 schema '<scheme>://'`.

## Rules

- LLM may reference `env://...` but must not read or print secret values.
- LLM may propose `pypi://...` dependencies, but policy gate decides whether they are allowed.
- Generated handlers should be referenced by `python://...` and called through `uri3.resolvers.router.call`.
- A2A/MCP endpoints are protocol addresses, not core domain logic.

## Migration note

Stary import:

```python
from hypervisor.uri2llm import resolve  # deprecated re-export
```

Aktualny:

```python
from uri3.resolvers.router import resolve, call
```

Deprecated shim: `hypervisor/uri2llm/` (re-eksporty).
