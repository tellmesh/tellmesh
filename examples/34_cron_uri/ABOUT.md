---
landing:
  cards:
    - id: api-sites-card
      layout: card
      order: 90
      docs: docs/examples.html#ex-34_cron_uri
      i18n:
        pl:
          tag: Strony · API
          title: Inne strony i systemy
        en:
          tag: Sites · API
          title: Other sites and systems
        de:
          tag: Seiten · API
          title: Andere Seiten und Systeme
      snippet: |
        curl -X POST http://localhost:8788/api/uri/call \
          -H "Content-Type: application/json" \
          -d '{"uri":"health://agent/invoices-agent.local","dry_run":true}'
---

<ul>
<li>Webhook <code>POST /api/uri/call</code> z Twojej aplikacji (formularz, SaaS, panel klienta).</li>
<li>Monitor URL co 5 min — <code>cron://www/monitor/landing</code> (patrz <a href="docs/examples.html#ex-34_cron_uri">example 34</a>).</li>
<li>Reverse proxy (nginx) → health check na <code>/health</code> agenta.</li>
</ul>
