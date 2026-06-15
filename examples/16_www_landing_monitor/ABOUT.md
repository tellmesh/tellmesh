---
landing:
  cards:
    - id: www-landing-monitor-connector
      layout: connector
      order: 85
      logo: WM
      docs: docs/examples.html#ex-16_www_landing_monitor
      i18n:
        pl:
          tag: Monitor
          title: Monitor landing page (cron + health)
          lead: cron://www/monitor/landing co 5 min — health, diff, webhook przy zmianie.
        en:
          tag: Monitor
          title: Landing page monitor (cron + health)
          lead: cron://www/monitor/landing every 5 min — health, diff, webhook on change.
        de:
          tag: Monitor
          title: Landing-Page-Monitor (Cron + Health)
          lead: cron://www/monitor/landing alle 5 Min — Health, Diff, Webhook bei Änderung.
      snippet: |
        NL: "monitoruj landing i alertuj przy zmianie"
        Cron: cron://www/monitor/landing
        Install: scripts/www/install-cron.sh

    - id: www-landing-monitor-card
      layout: card
      order: 95
      docs: docs/examples.html#ex-16_www_landing_monitor
      i18n:
        pl:
          tag: Cron monitor
          title: landing monitor + webhook
        en:
          tag: Cron monitor
          title: landing monitor + webhook
        de:
          tag: Cron monitor
          title: landing monitor + webhook
      snippet: |
        urish run workflow://... (or cron)
        # events → output/events/ + webhook
---
<ul>
<li>Automatyczny monitoring stron co X min.</li>
<li>Diff + incident przy zmianie (health, content).</li>
<li>Integracja z cron hosta i webhook (file:// + log://).</li>
</ul>
