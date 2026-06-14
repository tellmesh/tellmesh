# Example 23 — Tutorial: NL → URI → wykonanie → agent HTTP

Przewodnik krok po kroku: od zdania po polsku do działającego agenta pod adresem URL.

## Szybki start

```bash
cd /path/to/hypervisor
pip install -e '.[dev]'
bash examples/23_nl_to_agent_tutorial/run.sh
```

Skrypt robi wszystko po kolei i zapisuje plany w `output/tutorial/`.

## Architektura (co robi który pakiet)

```txt
nl2uri   → tłumaczy język naturalny na plan URI (YAML)
uri2flow → rozwija krótki *.uri.flow.yaml do workflow graph
uri3     → waliduje i wykonuje workflow (mock / Playwright)
uri2ops  → rejestr operacji + adaptery OS/browser + serve A2A/MCP
nl2a     → generuje agenta HTTP z promptu (Domain Pack + kod)
hypervisor → rejestr deploymentów + run/stop agenta lokalnie
```

**Zasada:** `nl2uri` tylko **planuje**. Wykonanie to `uri3 run-workflow` / `uri3 run-flow` albo `uri2ops run`.

## Krok 1 — Rejestry URI

| Rejestr | Pytanie | Komenda |
|---------|---------|---------|
| Schematy URI | Czy `browser://…` jest poprawne? | `uri3 list --schemes` |
| Operacje | Co mogę zrobić z `browser://…`? | `uri2ops registry list` · `uri2ops operations describe browser open` |
| Deploymenty | Gdzie działa agent? | `hypervisor deployments` |

Pliki YAML:

```txt
packages/uri2ops/uri2ops/operation_registry/registry.yaml
config/operator_registry.uri.yaml
deployments/agent_deployments.yaml
```

## Krok 2 — Operator task z NL (Chrome + health)

Prompt:

```txt
otwórz Chrome i sprawdź localhost:8101/health
```

```bash
# klasyfikacja
nl2uri classify -p "otwórz Chrome i sprawdź localhost:8101/health"
# → task_graph

# plan YAML
nl2uri task -p "otwórz Chrome i sprawdź localhost:8101/health" --validate \
  > output/tutorial/task_graph.yaml

# wykonanie
uri3 plan-workflow output/tutorial/task_graph.yaml
uri3 run-workflow output/tutorial/task_graph.yaml --dry-run
uri3 run-workflow output/tutorial/task_graph.yaml --approve --browser mock
```

Kroki `kind: command` wymagają `--approve` (policy gate).

## Krok 3 — Flow z NL (generuj agenta → uruchom → sprawdź)

Prompt (plik [`prompt.txt`](prompt.txt)):

```txt
wygeneruj agenta pogodowego, uruchom go lokalnie i sprawdź health w Chrome
```

```bash
nl2uri flow -p "$(cat examples/23_nl_to_agent_tutorial/prompt.txt)" --validate \
  > output/tutorial/weather.uri.flow.yaml

uri3 expand-flow output/tutorial/weather.uri.flow.yaml \
  --out output/tutorial/weather.uri.graph.yaml

uri3 run-flow output/tutorial/weather.uri.flow.yaml --dry-run
uri3 run-flow output/tutorial/weather.uri.flow.yaml --approve --browser mock
```

Compact flow wygląda m.in. tak:

```yaml
flow:
  id: weather-agent-health
do:
  - agent://weather-generator
  - hypervisor://local/weather-agent/run
  - browser://chrome/page/open:
      url: http://localhost:8101/health
```

## Krok 4 — Wygeneruj nowego agenta (nl2a)

```bash
nl2a --no-llm -p "generuj mapę pogody dwa tygodnie do przodu w html"
make verify
```

Artefakty:

```txt
domains/weather_map/uri_tree.yaml
contracts/agents/weather_map_agent.yaml
agents/generated/weather_map_agent/
deployments/agent_deployments.yaml   → weather-map-agent.local
```

## Krok 5 — Uruchom agenta pod URL

```bash
hypervisor run-agent weather-map-agent.local --detach
curl http://localhost:8101/health
curl http://localhost:8101/.well-known/agent-card.json
curl "http://localhost:8101/skills/read_weather_map?place=Gdansk&days=14"
```

Jeśli port `8101` jest zajęty (np. przez Docker), tutorial wybiera wolny port automatycznie:

```bash
bash examples/23_nl_to_agent_tutorial/run.sh
# lub ręcznie:
hypervisor run-agent weather-map-agent.local --detach --port 8111
```

Agent wystawia **REST API** (health, commands, skills) — nie gotowe okno chat.
Interakcja „chat-like” możliwa przez A2A/MCP na `uri2ops serve` albo własny frontend na widokach HTML z kontraktu.

```bash
hypervisor agent-status weather-map-agent.local
hypervisor stop-agent weather-map-agent.local
```

## Krok 6 — Alternatywy interakcji

**Shell operator (uri2ops):**

```bash
uri2ops run examples/10_browser_operator/task.health.yaml --adapter mock --approve
```

**HTTP daemon (A2A + rejestr operacji):**

```bash
uri2ops serve --port 8791
curl http://127.0.0.1:8791/registry
```

**Nowe URI capability bez pełnego nl2a (touri):**

```bash
touri list examples/20_touri_capabilities
touri call weather://forecast/Gdansk/14/html --registry examples/20_touri_capabilities
```

## Mapa trybów nl2uri

| Komenda | Kiedy |
|---------|-------|
| `nl2uri plan` | auto — system wybiera tryb |
| `nl2uri task` | liniowy proces operatora |
| `nl2uri flow` | sekwencja kroków (preferowane) |
| `nl2uri graph` | workflow z warunkami (`jeśli…`) |
| `nl2uri tree` | hierarchia domeny (Domain Pack) |

## Powiązane przykłady

- [`13_nl2uri_multi_uri_graph/`](../13_nl2uri_multi_uri_graph/) — wszystkie tryby nl2uri
- [`17_flow_vs_graph/`](../17_flow_vs_graph/) — compact flow vs expanded graph
- [`04_nl2a_weather_map/`](../04_nl2a_weather_map/) — generacja agenta
- [`09_run_agent_hypervisor/`](../09_run_agent_hypervisor/) — lifecycle agenta
- [`14_workflow_executor_mock/`](../14_workflow_executor_mock/) — uri3 executor

Dokumentacja: [`docs/NL2URI.md`](../../docs/NL2URI.md) · [`docs/HYPERVISOR_WORKFLOW.md`](../../docs/HYPERVISOR_WORKFLOW.md)
