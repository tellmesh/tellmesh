# Pozycjonowanie Taskinity

## Zasada: dwa poziomy komunikacji

| Poziom | Odbiorca | Hasło |
|--------|----------|-------|
| **Sprzedażowy (pierwszy ekran)** | Właściciel, COO, PM, integrator | Command center dla automatyzacji |
| **Techniczny (demo, drugi ekran)** | Tech lead, DevOps, architekt | URI execution and repair layer |

**Nie używać na pierwszym ekranie:** „URI-first Agent Control Plane” — kategoria zatłoczona przez Astrix, Fiddler, Contro1, Speakeasy, IBM (governance, identity, audit).

Szczegóły: [ASSESSMENT.md](./ASSESSMENT.md).

---

## Kategoria (sprzedażowa)

> **Taskinity to prosty command center dla automatyzacji, skryptów i agentów AI.**  
> Jeden widok: co działa, co padło, dlaczego i co zrobić dalej.

Nie: framework agenta. Nie: workflow builder. Nie: observability SaaS. Nie: enterprise governance.

---

## Kategoria (techniczna)

> **URI execution and repair layer** over agents, workflows and tools.

Taskinity stoi **warstwę wyżej** niż MCP/A2A/`agent://` — wykorzystuje je, ale wystawia operational URI: repair, ticket, evolve, view.

---

## Teza produktowa

Rynek ma rozłączone warstwy:

1. **Build** — LangGraph, CrewAI, n8n
2. **Observe** — Langfuse, Phoenix, LangSmith traces
3. **Govern** — Contro1, Astrix, AIControl (enterprise CP)
4. **Brak:** operational control dla MŚP — **chaos skryptów, cron, webhooków, API, agentów**

Taskinity wypełnia #4 jednym modelem URI i wieloma powierzchniami (chat, API, CLI, runtime).

---

## One-linery

### PL — właściciel / biznes

> Zamiast szukać po logach, webhookach i Excelach, pytasz w chacie: „co się stało z procesem faktur?” — i dostajesz status, przyczynę, logi, ticket i propozycję naprawy.

### PL — tech lead (pitch)

> Taskinity to prosty command center dla automatyzacji i agentów. Pod spodem każdy proces jest URI — to samo URI z chatu, API, CLI, shella, Dockera i HTTP.

### PL — integrator n8n/Make

> Warstwa utrzymania i SLA dla wdrożeń: status procesów, błędy, ticket, rekomendacja naprawy — bez zastępowania n8n.

### EN — standardy / konferencje

> Taskinity is a URI execution and repair layer over agents, workflows and tools — observe, repair, ticket, and evolve across chat, CLI, and runtime.

---

## Przewaga vs LangSmith Engine

LangSmith Engine ([docs](https://docs.langchain.com/langsmith/engine-overview)) robi repair loop na trace’ach LangChain (root cause → fix → PR).

**Nasza przewaga nie brzmi:** „mamy observe → repair”.

**Brzmi:**

> Spinamy **dowolne** procesy: skrypty, cron, API, Docker, SSH, n8n, Make, shell, workflow, agenty i tickety — jednym modelem URI.

Battlecard: [BATTLECARD.md](./BATTLECARD.md).

---

## Relacja do observability

Nie buduj własnego Langfuse. Taskinity = status, health, logi, zdarzenia procesów. Głęboki tracing LLM → integracja Langfuse/Phoenix/LangSmith.

| Observability | Taskinity |
|---------------|-----------|
| Trace, koszt, eval | Stan procesu, naprawa, ticket |
| Pasywne | Operacyjne („co zrobić teraz”) |

---

## Relacja do workflow (n8n, Make, Zapier)

> Masz już automatyzacje. My pokazujemy, które działają, które padły, gdzie jest błąd i jak to naprawić.

Integracja, nie replacement.

---

## Relacja do enterprise control plane

Enterprise CP = CISO, SOC2, approvals. Taskinity = tech lead / integrator, 5–80 osób, self-host, policy gate.

---

## Persony

| Persona | Potrzeba | Powierzchnia |
|---------|----------|--------------|
| Właściciel / COO | „Co padło?” bez technikaliów | Chat |
| Tech lead | Health, repair, audit | CLI, dashboard |
| Integrator n8n | Panel serwisowy dla klientów | Dashboard + API |
| Developer | Ten sam kontrakt co CI | CLI, API |

Język bólu: [PAIN_LANGUAGE.md](./PAIN_LANGUAGE.md).

---

## Landing page

Copy: [LANDING_COPY.md](./LANDING_COPY.md).

---

## Czego nie mówimy

- „URI-first agent control plane” na pierwszym slajdzie
- „Zastępujemy n8n / LangSmith”
- „Enterprise governance / SOC2”
- „Definiujemy standard agent://”

---

## Core sentence (wewnętrznie / docs techniczne)

```text
An agent has capabilities.
Each capability has a URI.
Every URI can be explained, verified, run, observed in UI, and stored as an artifact.
```

Źródło: [docs/MENTAL_MODEL.md](../docs/MENTAL_MODEL.md)
