---
landing:
  cards:
    - id: playwright-browser-connector
      layout: connector
      order: 42
      logo: PW
      docs: docs/examples.html#ex-11_playwright_browser
      i18n:
        pl:
          tag: Playwright
          title: Browser automation z Playwright (real)
          lead: Task health + browser open/screenshot — end-to-end z prawdziwą przeglądarką.
        en:
          tag: Playwright
          title: Browser automation with Playwright (real)
          lead: Task health + browser open/screenshot — end-to-end with real browser.
        de:
          tag: Playwright
          title: Browser-Automatisierung mit Playwright (real)
          lead: Task health + browser open/screenshot — End-to-End mit echtem Browser.
      snippet: |
        NL: "sprawdź health strony i zrób screenshot"
        Run: bash examples/11_playwright_browser/run.sh (with [browser] extra)

    - id: playwright-browser-card
      layout: card
      order: 52
      docs: docs/examples.html#ex-11_playwright_browser
      i18n:
        pl:
          tag: E2E
          title: task.health + playwright
        en:
          tag: E2E
          title: task.health + playwright
        de:
          tag: E2E
          title: task.health + playwright
      snippet: |
        pip install -e '.[browser]'
        playwright install chromium
        urish run ... --adapter playwright
---
<ul>
<li>Realne zrzuty ekranu (PNG) + health check strony.</li>
<li>Wymaga extra [browser] i playwright chromium.</li>
<li>Artefakty + logi dostępne przez file:// i log://.</li>
</ul>
