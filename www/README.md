# Taskinity WWW (`www/`)

Product site + chat interface connected to the `hypervisor-dashboard-agent` API.

Polish version: [`README.pl.md`](./README.pl.md)

## Pages

| URL | File | Description |
|-----|------|-------------|
| `/www/` | `index.html` | **Landing** — presentation, integrations, office, offer |
| `/www/chat.html` | `chat.html` | **Live chat** — NL → URI plan, API calls |
| `/www/przyklady.html` | `przyklady.html` | **Integration lab** — PASS cards + filters |
| `/www/docs/examples.html` | `docs/examples.html` | **Docs examples** — full `examples/*/*` content |
| `/www/demo.html` | `demo.html` | Technical URI demo (static) |

**Repo index:** [`docs/README.md`](../docs/README.md) · [`examples/README.md`](../examples/README.md) · [`TODO.md`](../TODO.md) · [`CHANGELOG.md`](../CHANGELOG.md)

Default language is **English** (`en`). Users can switch to PL or DE via the nav language toggle; preference is stored in `localStorage` (`taskinity.lang`).

## Generated assets (`make www-docs`)

| Output | Source |
|--------|--------|
| `www/docs/examples.html` | `examples/*/README.md` + source files |
| `www/index.html` `#integracje` cards | `examples/*/ABOUT.md` (YAML + markdown/HTML body) |
| `www/generated/integrations-i18n.js` | i18n from ABOUT frontmatter |
| `www/generated/examples-manifest.js` | `examples/*/README.md` titles + `run.sh` |

Integration cards use WordPress-style frontmatter in `examples/*/ABOUT.md`:

```yaml
---
landing:
  cards:
    - id: woocommerce-connector
      layout: connector   # connector | card | spotlight
      order: 20
      logo: WC
      i18n:
        pl: { tag: ..., title: ..., lead: ..., body: ..., cta_label: ..., cta_hint: ... }
        en: { ... }
      snippet: |
        URI: workflow://order/woocommerce-to-erp
---

<ul><li>HTML body for <code>card</code> layout lists</li></ul>
Spotlight <code>body</code>, <code>cta_label</code> and <code>cta_hint</code> live in <code>i18n.*</code> (PL/EN/DE).
Optional per-card <code>body:</code> in frontmatter overrides the shared markdown/HTML block after <code>---</code>.
Office chains: <code>examples/office_chains.yaml</code> → <code>examples-manifest.js</code> (<code>officeChains</code>).
```

After editing ABOUT.md or README: `make www-docs` (CI: `make www-docs-check`).

## Run

### Docker (recommended)

```bash
make start          # build + start container
make www-smoke      # test health / www / chat / api/ask
make stop           # stop container
make www-logs       # logs
```

- Landing: http://localhost:8788/www/
- Chat: http://localhost:8788/www/chat.html

Compose uses host networking/PID visibility and mounts runtime directories from the host
(see `docker-compose.yml`). `deployments/` and `output/` are writable so approved real-run
repair can rebind ports, persist runtime state and show process logs in the chat.

### Local (without Docker)

```bash
urish www serve
# or
urish www open
```

## Landing page

Files:

- `index.html` — section structure (hero, problem, tour, offer, FAQ)
- `landing.css` — style, animations, responsiveness
- `landing.js` — interactive 6-step presentation (autoplay, pause, navigation)

The **“How it works in practice”** section shows invoices → ERP 401 → chat → incident → ticket → technical proof.

The **“Integrations in 3 steps”** section shows a simple pattern for connecting existing systems:
WordPress, WooCommerce, BaseLinker, Allegro.pl, ERP/CRM and web portals. Each example has an NL prompt,
target URI and health/repair checkpoint.

Landing has preference toggles in the nav:

- language: `PL`, `EN`, `DE`,
- theme: `Warm`, `Dark`, `Light`.

Choice is stored locally in `localStorage` (`taskinity.lang`, `taskinity.theme`) and works without a backend.

Office scenarios are expanded in [`../examples/31_office_day/`](../examples/31_office_day/) (full mock day) and [`../examples/33_office_workflows/`](../examples/33_office_workflows/) (landing card → Touri URIs).

Marketing copy: [`../market/LANDING_COPY.md`](../market/LANDING_COPY.md)

## Docs examples (`docs/examples.html`)

Full documentation for the `examples/` directory — generated from repo sources:

```bash
make www-docs
# or
python3 scripts/www/build_examples_docs.py
```

Content: `examples/README.md`, each `examples/*/README.md` plus YAML/TXT/SH files (run.sh, task.*, prompt.txt).

URL: http://localhost:8788/www/docs/examples.html

## Chat (`chat.html`)

**Flow:** NL or voice → `POST /api/ask` (plan) → user clicks URI / Run plan or runs the CLI equivalent. Chat does **not** auto-run the full workflow on Enter.

| Action | Endpoint |
|--------|----------|
| NL prompt (single or batch) | `POST /api/ask` |
| URI preview | `POST /api/uri/preview` |
| URI call | `POST /api/uri/call` |
| Planned URI sequence | `POST /api/plan/run` |
| Voice transcription | `POST /api/voice/transcribe` |
| Agents | `GET /api/agents` |
| Events snapshot | `GET /api/events` |
| Events live feed | `GET /api/events/stream` |

Features:

- **Quick prompts** — six office scenarios (same quotes as landing cards)
- **Batch** — paste one command per line → `Detected N commands`
- **Office card click** → prefills chat via `localStorage.taskinity.chatPrompt`
- **Run plan** — executes all planned URIs in dry-run or approved mode through the policy gate
- **Live sidebar** — agents plus incident/monitor/health events over SSE
- **Voice** — browser microphone → mock/Whisper STT → normal NL planning path
- Default **English** UI; landing cards i18n PL/EN/DE via `office-cards-i18n.js`
- Cache-busted `app.js` — hard refresh after updates

Files: `app.js`, `styles.css`. Full guide: [`docs/CHAT_AND_WORKFLOWS.md`](../docs/CHAT_AND_WORKFLOWS.md)

```bash
curl -s -X POST http://localhost:8788/api/ask \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"pokaż proces agenta weather-map-agent.local","dry_run":true}'

curl -s -X POST http://localhost:8788/api/plan/run \
  -H 'Content-Type: application/json' \
  -d '{"planned_uris":["health://agent/invoices-agent.local"],"dry_run":true}'

curl -s -X POST http://localhost:8788/api/voice/transcribe \
  -H 'Content-Type: application/json' \
  -d '{"engine":"mock","text":"zdiagnozuj agenta invoices-agent.local"}'
```

## Docker mounts

Compose runs with `network_mode: host` and `pid: host`, then bind-mounts `www/`,
`packages/`, `agents/generated/`, `deployments/`, `output/`, etc., so API code, probes,
ports and generated agents match the host repo without rebuild. `deployments/` is writable
by design for approved repair actions; use dry-run/preview for read-only planning.

## Create via NL (CLI)

```bash
urish ask "create hypervisor dashboard agent"
urish www create "create a simple markdown chat connected to the system API" --plan-only
```

## Landing monitoring

```bash
make www-monitor       # run checks now
make www-monitor-test  # monitoring, webhook and cron tests
make www-monitor-reset # new price baseline after intentional change
```

Cron:

```bash
bash scripts/www/install-cron.sh            # preview cron entry
bash scripts/www/install-cron.sh --install  # install every 5 min
bash scripts/www/install-cron.sh --status   # status + last log lines
bash scripts/www/install-cron.sh --remove   # remove entry
```

`--install` prepares `/tmp/taskinity-monitor.log`, so `tail -f /tmp/taskinity-monitor.log`
should not fail before the first cron run. For n8n/Slack/Make provide a real URL:

```bash
bash scripts/www/install-cron.sh --update --webhook "https://hooks.n8n.cloud/webhook/real-token"
```

Placeholder addresses like `twoja-instancja...`, `hooks.example...` or `abc123` are treated as placeholders and are not sent to the webhook.
