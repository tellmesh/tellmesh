# Examples

Przykłady są uporządkowane według schematu `examples/*/*` — każdy katalog ma własny `README.md` i artefakty do uruchomienia.

| # | Katalog | Opis |
|---|---------|------|
| 01 | [`01_quickstart_local`](./01_quickstart_local/) | Lokalny przepływ `prompt -> URI Tree`. |
| 02 | [`02_uri3_scan_http`](./02_uri3_scan_http/) | Skanowanie HTTP/A2A-like przez `uri3`. |
| 03 | [`03_ssh_remote_agent`](./03_ssh_remote_agent/) | Docker + SSH + mock agent. |
| 04 | [`04_nl2a_weather_map`](./04_nl2a_weather_map/) | Prompt weather-map → Domain Pack. |
| 05 | [`05_meta_repair`](./05_meta_repair/) | Uszkodzony kontrakt agenta → `meta_agent repair`. |
| 06 | [`06_orders_agent`](./06_orders_agent/) | Przykładowy kontrakt agenta zamówień. |
| 07 | [`07_invoices_agent`](./07_invoices_agent/) | Prompt do agenta faktur. |
| 08 | [`08_evolution`](./08_evolution/) | Evolution proposals (`add_orders_agent`, `add_invoices_agent`). |

Zasada architektury:

```txt
uri3 = skanowanie, routing, discovery i graf URI
hypervisor = registry, policy, lifecycle i decyzje
nl2uri = natural language -> URI Tree
nl2a = pipeline prompt -> URI Tree -> Domain Pack -> agent
```

Szybkie komendy:

```bash
make uri-tree
make nl2a-weather
make meta-repair
make docker-ssh-up
make scan-http
make evolution-check
python -m meta_agent.cli plan "$(cat examples/07_invoices_agent/create_invoices_agent_prompt.txt)"
```
