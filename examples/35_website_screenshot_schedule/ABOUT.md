---
landing:
  cards:
    - id: screenshot-schedule-connector
      layout: connector
      order: 45
      logo: SS
      docs: docs/examples.html#ex-35_website_screenshot_schedule
      i18n:
        pl:
          tag: Screenshot · monitor
          title: Harmonogram rzutów ekranu stron
          lead: Chat rozpoznaje prompt NL i planuje stabilny workflow URI — dry-run, approve, opcjonalnie Playwright i cron na hoście.
        en:
          tag: Screenshot · monitor
          title: Website screenshot schedule
          lead: Chat detects NL prompts and plans a stable workflow URI — dry-run, approve, optional Playwright and host cron.
        de:
          tag: Screenshot · Monitor
          title: Website-Screenshot-Zeitplan
          lead: Chat erkennt NL-Prompts und plant eine stabile Workflow-URI — Dry-run, Approve, optional Playwright und Host-Cron.
      snippet: |
        NL: "rob rzuty ekranów stron softreck.com co 5 minut do ~/images/"
        URI: workflow://graph/website-screenshot-schedule/dry-run
        Run: uri run workflow://graph/website-screenshot-schedule --approve --adapter playwright

    - id: screenshot-schedule-card
      layout: card
      order: 95
      docs: docs/examples.html#ex-35_website_screenshot_schedule
      i18n:
        pl:
          tag: Chat · workflow
          title: Stabilny URI z batch demo
        en:
          tag: Chat · workflow
          title: Stable URI from batch demo
        de:
          tag: Chat · Workflow
          title: Stabile URI aus Batch-Demo
      snippet: |
        curl -X POST :8788/api/ask -d '{"prompt":"zaplanuj harmonogram screenshotów..."}'
        → workflow://graph/website-screenshot-schedule/dry-run

    - id: screenshot-spotlight
      layout: spotlight
      order: 210
      cta:
        href: chat.html
      i18n:
        pl:
          title: "Przykład: harmonogram screenshotów z chatu (stabilny URI)"
          cta_label: Wypróbuj pytanie w chacie
          cta_hint: Trzecia linia z batch demo Taskinity Chat planuje ten workflow.
          body: |
            Typowy pilot monitorowania stron — chat NL, stabilny workflow, opcjonalny cron:

            ```
            1. Chat NL (batch)     →  workflow://graph/website-screenshot-schedule/dry-run
            2. Dry-run / approve   →  mock browser lub Playwright → ~/images/
            3. Host cron (opcja)   →  cron://www/monitor/landing + install-cron.sh
            4. Taskinity           →  health co 5 min + logi + chat przy awarii
            ```

            - Prompt „rob rzuty ekranów…” **nie** tworzy losowego `domain://` — zawsze ten sam workflow ID.
            - `bash examples/35_website_screenshot_schedule/run.sh` — PASS w CI.
            - Po edycji: `make www-docs` i restart kontenera WWW (Docker).
        en:
          title: "Example: screenshot schedule from chat (stable URI)"
          cta_label: Try a question in chat
          cta_hint: Line 3 of the Taskinity Chat batch demo plans this workflow.
          body: |
            A typical site monitoring pilot — NL chat, stable workflow, optional cron:

            ```
            1. NL chat (batch)     →  workflow://graph/website-screenshot-schedule/dry-run
            2. Dry-run / approve   →  mock browser or Playwright → ~/images/
            3. Host cron (opt.)    →  cron://www/monitor/landing + install-cron.sh
            4. Taskinity           →  health every 5 min + logs + chat on failure
            ```

            - A prompt like “take screenshots of these sites…” does **not** create a random `domain://` slug — same workflow ID every time.
            - `bash examples/35_website_screenshot_schedule/run.sh` — PASS in CI.
            - After edits: `make www-docs` and restart the WWW container (Docker).
        de:
          title: "Beispiel: Screenshot-Zeitplan aus Chat (stabile URI)"
          cta_label: Frage im Chat testen
          cta_hint: Zeile 3 der Taskinity-Chat-Batch-Demo plant diesen Workflow.
          body: |
            Typischer Site-Monitoring-Pilot — NL-Chat, stabiler Workflow, optional Cron:

            ```
            1. NL-Chat (Batch)     →  workflow://graph/website-screenshot-schedule/dry-run
            2. Dry-run / Approve   →  Mock-Browser oder Playwright → ~/images/
            3. Host-Cron (opt.)    →  cron://www/monitor/landing + install-cron.sh
            4. Taskinity           →  Health alle 5 Min + Logs + Chat bei Ausfall
            ```

            - Prompts wie „Screenshots dieser Seiten…” erzeugen **keine** zufällige `domain://`-URI — immer dieselbe Workflow-ID.
            - `bash examples/35_website_screenshot_schedule/run.sh` — PASS in CI.
            - Nach Änderungen: `make www-docs` und WWW-Container neu starten (Docker).
---

<ul>
<li>Stabilny URI: <code>workflow://graph/website-screenshot-schedule/dry-run</code> — patrz <a href="docs/examples.html#ex-35_website_screenshot_schedule">example 35</a>.</li>
<li>Batch chat (linia 3) planuje workflow zamiast <code>domain://</code>.</li>
<li>Cron hosta: <code>bash scripts/www/install-cron.sh --install</code> (example <a href="docs/examples.html#ex-34_cron_uri">34</a>).</li>
</ul>
