---
landing:
  cards:
    - id: pw-browser-connector
      layout: connector
      order: 80
      logo: PB
      docs: docs/examples.html#ex-15_playwright_browser
      i18n:
        pl:
          tag: Playwright
          title: Browser task z Playwright (mock + real)
          lead: Prosty przykład otwarcia + screenshot z task.health + browser.
        en:
          tag: Playwright
          title: Browser task with Playwright (mock + real)
          lead: Simple open + screenshot example with task.health + browser.
        de:
          tag: Playwright
          title: Browser-Task mit Playwright (Mock + Real)
          lead: Einfaches Open + Screenshot-Beispiel mit task.health + Browser.
      snippet: |
        NL: "otwórz stronę i sprawdź health"
        Run: bash examples/15_playwright_browser/run.sh

    - id: pw-browser-card
      layout: card
      order: 90
      docs: docs/examples.html#ex-15_playwright_browser
      i18n:
        pl:
          tag: Browser
          title: task + browser (mock/real)
        en:
          tag: Browser
          title: task + browser (mock/real)
        de:
          tag: Browser
          title: task + browser (mock/real)
      snippet: |
        urish run task.health.yaml --adapter mock
        # real: --adapter playwright (with [browser])
---
<ul>
<li>Minimalny przykład browser automation.</li>
<li>Mock do testów, real do zrzutów PNG.</li>
<li>Łatwo rozszerzyć o file:// / log:// watching.</li>
</ul>
