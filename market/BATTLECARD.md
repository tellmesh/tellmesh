# Battlecard — Taskinity vs konkurencja

Szybkie porównanie na rozmowy sprzedażowe i discovery (1 strona mental model).

## Kiedy używać

- Klient pyta: „Czym różnicie się od LangSmith / n8n / Contro1?”
- Pitch do tech leada software house’u
- Przygotowanie do demo

## Taskinity w jednym zdaniu (sprzedaż)

**Prosty command center dla automatyzacji** — co działa, co padło, dlaczego, co dalej (chat + dashboard).

Technicznie: URI execution and repair layer — ten sam URI z chatu, API, CLI.

---

## vs LangSmith + LangSmith Engine ⚠️ najgroźniejsza konkurencja

| | LangSmith / Engine | Taskinity |
|---|-------------------|-----------|
| **Główna wartość** | Trace, eval, **Engine: root cause → fix → PR** | Operational control **wszystkich** procesów |
| **Zakres repair** | Agenty LangChain / production traces | Skrypty, cron, API, Docker, n8n, shell, agenci, tickety |
| **ID operacji** | thread_id, run_id | `repair://`, `incident://`, `ticket://` |
| **Chat = CLI** | ❌ | ✅ ten sam URI |
| **Ticket → evolution** | ❌ native | ✅ `ticket://` → `evolution://` |

**Pitch:** „LangSmith Engine naprawia agentów LangChain z trace’ów. Taskinity spinamy cały chaos automatyzacji — nie tylko jeden framework.”

**Nie mów:** „Mamy observe → repair, oni nie” — Engine to już robi.

**Mów:** „Jeden model URI dla webhooków, cronów, n8n i agentów — nie tylko LangGraph.”

Źródło: [LangSmith Engine overview](https://docs.langchain.com/langsmith/engine-overview)

---

## vs LangGraph Control Plane API (deployment)

| | LangGraph CP API | Taskinity |
|---|------------------|-----------|
| **Cel** | Deploy preview → prod, revisions | Operacje runtime gdy coś padnie |
| **Repair** | Redeploy / CI | diagnose → apply → incident → ticket |

**Pitch:** „LangGraph deployuje. My operujemy po wdrożeniu.”

---

## vs n8n (+ self-healing trend 2026)

| | n8n | Taskinity |
|---|-----|-----------|
| **Główna wartość** | Workflow automation | Agent/process control plane |
| **Self-healing** | Error workflow, retry, AI patch node | URI loop diagnose → apply → incident → evolve |
| **Model** | Workflow ID | URI everywhere |
| **Agenty LLM** | Dodatek | First-class deployment + health |
| **Kiedy my** | Chaotyczny mix n8n + skrypty + agenci, brak jednego ops modelu |
| **Kiedy oni** | Prosta automatyzacja SaaS bez agentów |

**Pitch:** „n8n naprawia workflow w n8n. Taskinity daje wspólny język dla n8n, skryptów i agentów — health, repair, ticket.”

**Strategia:** integracja, nie replacement — webhook n8n → `incident://`.

---

## vs Langfuse / Arize Phoenix (observability)

| | Langfuse/Phoenix | Taskinity |
|---|------------------|-----------|
| **Główna wartość** | Traces, costs, evals | Control: repair, ticket, evolve |
| **Persona** | MLOps | Tech lead + PM (chat) |
| **incident → ticket** | ❌ native | ✅ |
| **Kiedy my** | „Widzimy trace, ale nie wiemy co zrobić” |
| **Kiedy oni** | Głęboka analityka jakości LLM |

**Pitch:** „Observability pod spodem; Taskinity warstwa operacyjna nad nią.”

---

## vs Contro1 / AIControl / Astrix / Fiddler / Speakeasy (enterprise CP)

| | Enterprise CP | Taskinity |
|---|---------------|-----------|
| **Główna wartość** | Governance, identity, audit, SOC2 | Operational chaos MŚP |
| **Kategoria** | **Zatłoczona** — wszyscy mówią „control plane” | „Command center” — unikaj CP na pierwszym ekranie |
| **Kiedy my** | MŚP, software house, integrator |
| **Kiedy oni** | Bank, korpo, regulated |

**Pitch:** „Oni: czy wolno. My: co padło i jak naprawić.”

---

## vs Kestra / Make / Zapier

| | Workflow SaaS | Taskinity |
|---|---------------|-----------|
| **Integracje** | ✅✅ | ⚠️ przez URI/http |
| **Agent health** | ❌ | ✅ |
| **Developer-first** | ⚠️ | ✅ |
| **Kiedy my** | Zespół techniczny, własny runtime, agenci |
| **Kiedy oni** | Biznes user, proste Zaps |

---

## Macierz decyzyjna

```text
Trace LLM + eval + Engine fix PR?     → LangSmith
Governance SOC2 / audit?              → Contro1 / Astrix / Fiddler
Automatyzacja SaaS (Zapier)?          → n8n / Make
Chaos: skrypty + n8n + API + agenci?  → Taskinity
```

## Unikalne dowody (demo)

1. Ten sam URI w chacie, curl i CLI
2. `incident://` → `evolution://` bez Jira
3. **`urish proof`** — 30-sekundowy proof wszystkich warstw
4. Historia sprzedażowa: faktury → API 401 → incident → ticket

## Słabości Taskinity (mów wprost)

| Słabość | Co powiedzieć |
|---------|---------------|
| Brak trace/cost jak LangSmith | „Integrujemy OTel/Langfuse jako read; nasza wartość to control” |
| MCP HTTP nie stdio | „Mostek dla Cursor w roadmapie; uri2ops działa HTTP” |
| Mniejszy ekosystem | „Self-host, open pipeline — nie vendor lock-in” |
| Docker demo wymaga dopracowania | „Pilot domyka pod Wasz deploy” |

## Linki wewnętrzne

- [DEMO_SCRIPT.md](./DEMO_SCRIPT.md)
- [POSITIONING.md](./POSITIONING.md)
- [COMPETITIVE_LANDSCAPE.md](./COMPETITIVE_LANDSCAPE.md)
