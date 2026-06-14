# Mapa konkurencji

Synteza kategorii i wymiarów (2026-06).  
**Korekta:** [ASSESSMENT.md](./ASSESSMENT.md) — kategoria „agent control plane” jest **zatłoczona**.

## 0. Zatłoczona kategoria „AI agent control plane”

Termin przejęty przez **enterprise governance** — nie używać jako głównego hasła Taskinity.

| Gracz | Fokus |
|-------|-------|
| [Astrix](https://astrix.security/product/deploy-and-provisions-ai-agent-discovery/) | Creds, policy, secure deploy |
| [Fiddler](https://www.fiddler.ai/) | Telemetria, eval, governance |
| [Contro1](https://contro1.com/) | Approvals, audit evidence |
| [Speakeasy](https://www.speakeasy.com/resources/ai-control-plane) | Identity, policy, observability |
| IBM, Singulr, Microsoft Agent 365 | Fleet governance, operations |

**Taskinity na rynku:** „command center dla automatyzacji” (operational), nie „control plane” (governance).

---

## 2. LangSmith Engine — najgroźniejsza konkurencja w repair

[LangSmith Engine](https://docs.langchain.com/langsmith/engine-overview): production traces → powtarzalne błędy → root cause → fix → evaluator → **pull request**.

**Teza „nikt nie ma repair loop” — osłabić.** Engine robi repair dla ekosystemu LangChain.

**Przewaga Taskinity:** URI model dla **dowolnych** procesów (http, shell, docker, n8n, cron), nie tylko LangGraph agents + ticket/evolution natywnie.

---

## 3. Co znaczy „agent control plane” na rynku (kontekst)

- governance i routing (kto może, co wolno, audit),
- approvals na tool calls,
- krótkotrwałe creds, compliance (SOC2, EU AI Act),
- deployment lifecycle agentów w produkcji.

**Wspólny mianownik:** enterprise governance — nie URI-first operational control.

Przykłady: [Astrix ACP](https://astrix.security/product/deploy-and-provisions-ai-agent-discovery/), [AIControl](https://aictl.io), [Contro1 compare](https://contro1.com/compare/best-ai-agent-control-plane-tools), [Opper](https://opper.ai/ai-control-plane), [Ingenimax](https://ingenimax.ai/solutions/agent-control-plane).

## 4. Agent observability i self-healing

Segment observability koncentruje się na:

- traces (prompts, tool calls, latency, koszty),
- ewaluacje i drift,
- dashboardy dla MLOps/platform teams.

„Self-healing” w treściach marketingowych = meta-agent zmienia prompt/model/workflow na podstawie danych observability — **nie** spójny URI loop incident → repair → ticket → evolve.

Przykłady: [Braintrust guide 2026](https://www.braintrust.dev/articles/best-ai-observability-tools-2026), [Maxim observability guide](https://www.getmaxim.ai/articles/agent-observability-the-definitive-guide-to-monitoring-evaluating-and-perfecting-production-grade-ai-agents/), [DataRobot monitoring](https://www.datarobot.com/blog/best-ai-agent-monitoring-tools/).

## 5. Kategorie vs Taskinity

| Kategoria | Przykłady | Co robią dobrze | Czego brakuje (Taskinity) |
|----------|-----------|-----------------|---------------------------|
| Frameworki agentów | LangGraph, CrewAI, AutoGen, Dify | Budowa agentów, orkiestracja kroków | Brak URI-first control plane, brak health/repair/ticket/evolution jako bytów |
| Low-code / workflow | n8n, Make, Zapier, Kestra | Automatyzacje SaaS, prosty UX | Brak agent-first modelu, brak spójnego URI runtime |
| RPA / enterprise | UiPath, Power Automate | E2E procesy biznesowe, governance | Ciężki stack, mało developer-first |
| Agent observability | LangSmith, Langfuse, Phoenix, Braintrust | Tracing, evals, koszty | Brak repair/ticket/evolution jako produktu |
| Agent control plane (gov) | Contro1, AIControl, Microsoft Agent 365 | Approvals, audit, routing | „Czy wolno?” nie „jak naprawić proces?” |
| Protokoły | MCP, A2A, `agent://` draft | Interoperacyjność | Brak warstwy produktowej dla ludzi |

## 6. Macierz wymiarów

| Wymiar | LangGraph + LangSmith | n8n / Kestra | Contro1 / AIControl | Phoenix / Langfuse | **Taskinity** |
|--------|----------------------|--------------|---------------------|-------------------|---------------|
| URI jako obiekt wykonania | ❌ graph/thread ID | ❌ workflow ID | ❌ action/policy | ❌ trace ID | ✅ |
| Chat = ten sam ID co CLI | ❌ | ❌ | ❌ | ❌ | ✅ |
| Observe (traces/logs) | ✅✅ | ⚠️ | ⚠️ | ✅✅ | ⚠️ lokalne |
| Repair loop | ⚠️ **Engine: trace→PR** | ⚠️ retry/DLQ | ❌ | ❌ | ✅ playbooks + all process types |
| incident → ticket → evolution | ❌ | ❌ | ❌ (Jira ext.) | ❌ | ✅ natywnie |
| Enterprise governance | ⚠️ | ❌ | ✅✅ | ⚠️ | ⚠️ policy gate |
| MCP/A2A | ⚠️ ekosystem | ⚠️ Kestra MCP | ⚠️ | ❌ | ✅ uri2ops |
| Developer-first / self-host | ✅ | ✅ | ⚠️ | ✅ OSS | ✅✅ |
| Cena MŚP PL | $$$ | $$ | $$$$ | $ / OSS | pilot 5–12k zł |

## 7. Najbliżsi konkurenci per wymiar

### LangGraph „Control Plane API”

LangSmith ma [Control Plane API](https://docs.langchain.com/langgraph-platform/api-ref-control-plane) — **deployment lifecycle** (preview → prod, revisions, Docker image). Nie operational URI (`repair://`, `ticket://`).

**Pozycja Taskinity:** obok LangGraph — oni budują i deployują, my operujemy runtime.

### n8n self-healing (2025–2026)

Trend: global Error Workflow, AI auto-fix, retry/DLQ, klasyfikacja TRANSIENT/LOGIC/FATAL ([przykłady](https://www.aifloxium.online/blog/self-healing-n8n-workflows)).

**Różnica:** workflow-centric, brak jednego URI przez chat/CLI/API, brak `incident://` → `evolution://`.

**Pozycja Taskinity:** integracja n8n jako runtime pod spodem, nie konkurencja head-on.

### Futurum ACPF / Activant

Reference model control plane: identity, permissions, lifecycle, observability-native ([Futurum ACPF](https://futurumgroup.com/press-release/futurum-agent-control-plane-framework-a-reference-model-for-production-ai-agents/), [Activant research](https://activantcapital.com/research/the-agent-control-plane)).

**Pozycja Taskinity:** „ACPF Layer 0–2 for teams of 5–30” — execution + repair + evolution bez multi-tenant SOC2.

### Govcraft / agent-uri-rs

Open-source implementacja `agent://` ([GitHub](https://github.com/Govcraft/agent-uri-rs)) — **sąsiad techniczny**, potencjalny komponent discovery, nie produkt control plane.

## 8. Odpowiedzi na pytania badawcze

| Pytanie | Odpowiedź |
|---------|-----------|
| Czy istnieje produkt URI-first control plane jak Taskinity? | **Nie jako gotowy SaaS.** Kombinacja schematów + multi-surface jest unikalna w open-source. |
| To samo URI z chat/API/CLI/workflow? | **Taskinity tak.** Reszta — różne ID per warstwa. |
| Self-healing agentów? | Częściowo wszędzie; **spójny URI loop** — praktycznie tylko Taskinity. |
| incident → ticket → proposal? | **Natywnie Taskinity.** Reszta — integracje z Jira/ServiceNow. |
| Dashboard dla nietechnicznego? | Enterprise = inżynierowie; **chat-first Taskinity** = nisza MŚP. |
| Polskie MŚP? | **Tak** — enterprise za drogie, OSS observability za skomplikowane. |

## 9. Luka rynkowa (wniosek)

- `agent://` (IETF) = addressing layer, nie governance/repair
- MCP/A2A = interoperacyjność, nie UX control plane
- Observability = watch, nie control
- Enterprise CP = approve, nie napraw całego procesu

**Taskinity:** URI-first operational control plane spinający observe → repair → ticket → evolve z chatu, CLI, API i runtime.
