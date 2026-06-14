# Scenariusz demo

Dwa warianty:

1. **Demo sprzedażowe** (8 min) — historia faktur, język klienta → [priorytet na spotkania]
2. **Demo techniczne** (12 min) — jedno URI przez wszystkie warstwy

Strategia: [ASSESSMENT.md](./ASSESSMENT.md).

---

## Demo sprzedażowe (priorytet)

**Cel:** Klient rozumie efekt, nie architekturę.

### Historia

```text
Firma ma automatyzację faktur.
Proces działał codziennie o 7:00.
Dziś nie przetworzył 14 faktur.

Użytkownik pyta w chacie:
„Dlaczego faktury nie weszły do systemu?”

Taskinity:
- proces znaleziony,
- ostatni run: failed,
- przyczyna: API ERP zwróciło 401,
- możliwa przyczyna: wygasły token,
- utworzono incident,
- można utworzyć ticket,
- można uruchomić repair: odśwież token / sprawdź secret / retry.
```

### Prompt w chacie (przykład)

> Dlaczego faktury nie weszły do systemu?

### Komunikat zamykający

> „Nie szukacie 3 godzin po logach. Jeden chat — status, przyczyna, ticket, naprawa.”

---

## Proof 30 sekund (`urish proof`)

Dowód, że URI nie jest tylko nazwą. **Jeden przycisk / jedna komenda:**

```bash
urish proof view://process/agent/weather-map-agent.local/latest
```

Oczekiwany wynik (docelowy kontrakt produktu):

```text
Chat layer        OK
Web API           OK
CLI               OK
Runtime           OK
Transport shell   OK
Transport http    OK
Docker check      OK
Incident          OK
Ticket            OK
Repair proposal   OK
```

> **Status implementacji:** komenda `urish proof` — roadmap MVP ([PRODUCT_READINESS.md](./PRODUCT_READINESS.md)). Do czasu implementacji użyć ręcznego przejścia Akt 1–6 poniżej.

---

## Demo techniczne: jedno URI przez wszystkie warstwy

Czas: **8–12 minut** (nagranie + live).

## Cel demo

Pokazać, że **ten sam identyfikator URI** przechodzi przez:

1. Chat (NL → plan)
2. Web UI (widok procesu)
3. REST API
4. CLI (`urish`)
5. Repair loop (dry-run → approve)
6. Eskalacja ticket → evolution

Konkurencja zwykle pokazuje dashboard + API — **nie** spójny URI-first model.

## Prerequisites

```bash
# Opcja A: golden path (host)
bash examples/30_golden_path/run.sh

# Opcja B: chat Docker
make start
# http://localhost:8788/www/

# Opcja C: MCP/A2A (osobny terminal)
uri2ops serve --host 127.0.0.1 --port 8791
```

Agent przykładowy: `weather-map-agent.local` (lub inny z deployment registry).

## Akt 1 — Obserwacja (2 min)

### Chat

1. Otwórz `http://localhost:8788/www/`
2. Wpisz: **„sprawdź health agenta pogodowego”**
3. Pokaż markdown z planem URI i `next_steps`
4. Zaznacz **dry-run** włączony

### Ten sam URI — CLI

```bash
urish call health://agent/weather-map-agent.local
# lub
hypervisor inspect-agent weather-map-agent.local
```

### Ten sam URI — API

```bash
curl -s -X POST http://localhost:8788/api/uri/call \
  -H 'Content-Type: application/json' \
  -d '{"uri":"health://agent/weather-map-agent.local","dry_run":true}'
```

**Komunikat:** „To nie są trzy różne integracje — to ten sam kontrakt `ServiceResult`.”

## Akt 2 — Widok procesu (1 min)

```bash
urish call view://process/agent/weather-map-agent.local/latest
```

Lub klik URI w chacie → **Preview** / **Run** (dry-run).

Pokaż panel: stan procesu, health, ostatnie logi (jeśli dostępne).

## Akt 3 — Symulacja awarii / diagnose (2 min)

```bash
urish repair diagnose weather-map-agent.local
```

URI: `repair://agent/weather-map-agent.local/diagnose`

Pokaż **RepairPlan** — klasyfikacja, bezpieczne playbooki.

W chacie: **„zdiagnozuj agenta pogodowego”** → ten sam URI w planie.

## Akt 4 — Repair z policy gate (2 min)

```bash
# Najpierw dry-run
urish repair apply weather-map-agent.local --dry-run

# Potem approve
urish repair apply weather-map-agent.local --approve
```

W UI: odznacz dry-run tylko po pokazaniu preview → **Approve**.

**Komunikat:** „Mutacje wymagają świadomej zgody — to nie jest autonomiczny chaos.”

## Akt 5 — Incident → evolution (2 min)

Gdy repair nie wystarczy (lub symulacja):

```bash
# Artifact incydentu (jeśli powstał)
ls output/incidents/

urish evolve from-incident output/incidents/.../inc_*.yaml
urish proposal verify evolution/proposals/from_incident_*.yaml
urish proposal apply evolution/proposals/from_incident_*.yaml --sandbox
```

URI chain:

```text
incident://agent/weather-map-agent.local/{id}
  → evolution://proposal/from-incident/{id}
```

## Akt 6 — Ticket (planfile) (1 min)

```bash
urish ticket show ticket://feature/PL-10
urish evolve from-ticket ticket://feature/PL-10
```

**Komunikat:** „Od incydentu produkcyjnego do propozycji zmiany w repo — jeden model artifactów.”

## Akt 7 (opcjonalny) — MCP/A2A (1 min)

```bash
curl -s http://127.0.0.1:8791/.well-known/agent-card.json | head
curl -s http://127.0.0.1:8791/mcp/tools | head
```

**Komunikat:** „Taskinity operuje runtime’em; MCP/A2A to transporty pod spodem.”

## Slajd podsumowujący (1 slajd)

```text
Chat          →  POST /api/ask        →  plan URI
Chat / UI     →  POST /api/uri/call   →  repair://...
CLI           →  urish repair apply   →  ten sam URI
API           →  curl /api/uri/call   →  ten sam kontrakt
Runtime       →  uri2run docker/ssh   →  ten sam model
MCP/A2A       →  uri2ops :8791        →  operator tasks
```

## Troubleshooting demo

| Problem | Obejście |
|---------|----------|
| Repair 500 w Docker | Uruchom repair z hosta lub dodaj volume `agents/generated` |
| Agent nie działa | `hypervisor run-agent weather-map-agent.local --detach --wait-healthy` |
| uri2ops nie startuje | Akt 7 pomiń; wspomnij „osobny proces :8791” |
| Długi `/api/ask` | Użyj krótszego promptu lub wcześniej wygenerowanego planu |

## CTA po demo

> „W pilocie wdrażamy ten sam model na Waszych 2–3 automatyzacjach — health dashboard, chat i repair flow pod nadzorem.”

Zobacz [GTM_POLAND.md](./GTM_POLAND.md).
