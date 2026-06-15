---
landing:
  cards:
    - id: golden-path-connector
      layout: connector
      order: 155
      logo: GP
      docs: docs/examples.html#ex-30_golden_path
      i18n:
        pl:
          tag: Golden
          title: Złota ścieżka (end-to-end happy path)
          lead: Prosty, kompletny happy path od NL do wyniku — wzorzec dla innych przykładów.
        en:
          tag: Golden
          title: Golden path (end-to-end happy path)
          lead: Simple, complete happy path from NL to result — pattern for other examples.
        de:
          tag: Golden
          title: Golden Path (End-to-End Happy Path)
          lead: Einfacher, kompletter Happy Path von NL zum Ergebnis.
      snippet: |
        NL: "wykonaj złotą ścieżkę dla prostego przypadku"
        Run: bash examples/30_golden_path/run.sh

    - id: golden-path-card
      layout: card
      order: 165
      docs: docs/examples.html#ex-30_golden_path
      i18n:
        pl:
          tag: Wzorzec
          title: end-to-end + dry-run + approve
        en:
          tag: Pattern
          title: end-to-end + dry-run + approve
        de:
          tag: Muster
          title: end-to-end + dry-run + approve
      snippet: |
        urish run ... --dry-run
        urish run ... --approve
---
<ul>
<li>Najprostszy kompletny przykład do nauki.</li>
<li>Pokazuje cały stack: NL → plan → dry → execute.</li>
<li>Dobry punkt startowy przed bardziej złożonymi (31-35).</li>
</ul>
