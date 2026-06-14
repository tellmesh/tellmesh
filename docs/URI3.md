# uri3

`uri3` to niezależna paczka do pracy z URI: parser, normalizer, resolvery, skanery, graf zależności, walidacja URI Tree, logi (`log://`) i introspection schematów.

Hypervisor korzysta z `uri3` przez cienki adapter (`hypervisor.uri.client.Uri3Client`), ale `uri3` nie zależy od hypervisora.

## CLI

```bash
uri3 validate <uri>
uri3 validate-tree domains/weather_map/uri_tree.yaml
uri3 graph domains/weather_map/uri_tree.yaml
uri3 resolve <uri>
uri3 scan http://localhost:8101
uri3 logs 'log://hypervisor?level=ERROR&grep=deployment&limit=100'
uri3 logs 'log://hypervisor' --summary
uri3 schema 'log://'
uri3 schema 'log://hypervisor?level=ERROR'
uri3 schema --list
```

## Obsługiwane schematy

```txt
env llm log python pypi http https a2a mcp
resource artifact domain agent local input command event
ssh docker git
```

Pełna lista i opcje query: `uri3 schema --list` oraz `uri3 schema '<scheme>://'`.

## log://

Domyślne strumienie mapują na `output/logs/{stream}.log`:

```bash
uri3 logs 'log://hypervisor?level=ERROR&since=1h&limit=50'
uri3 logs 'log://file/output/logs/hypervisor.log'
```

Filtry: `level`, `grep`, `logger`, `since`, `until`, `limit`, `offset`, `tail`.

## Skanowanie

Skaner HTTP sprawdza m.in.:

```txt
/health
/capabilities
/.well-known/agent-card.json
/.well-known/agent.json
```

Skaner `log://` zwraca metadane pliku i liczbę dopasowanych wpisów.

> **Uwaga:** `uri3 scan ssh://...` nie jest jeszcze zaimplementowany. SSH testenv opisano w [`examples/03_ssh_remote_agent/`](../examples/03_ssh_remote_agent/README.md).

## Python API

```python
from uri3.resolvers.router import resolve, call
from uri3.logs.reader import read_logs, summarize_logs
from uri3.protocols.scheme_registry import get_scheme_schema, analyze_uri, describe_uri
```

## Powiązane dokumenty

- [`docs/ARCHITECTURE_V0_5.md`](./ARCHITECTURE_V0_5.md)
- [`docs/URI2LLM.md`](./URI2LLM.md) — historyczna warstwa routing (dziś `uri3.resolvers`)
- [`examples/02_uri3_scan_http/`](../examples/02_uri3_scan_http/README.md)
