---
landing:
  cards:
    - id: quickstart-connector
      layout: connector
      order: 5
      logo: QS
      docs: docs/examples.html#ex-01_quickstart_local
      i18n:
        pl:
          tag: Quickstart
          title: Pierwszy lokalny agent w 2 minuty
          lead: Uruchom agenta z gotowego szablonu, sprawdź health i wykonaj pierwsze wywołanie przez urish/uri.
        en:
          tag: Quickstart
          title: First local agent in 2 minutes
          lead: Start an agent from template, check health and make first call via urish/uri.
        de:
          tag: Quickstart
          title: Erster lokaler Agent in 2 Minuten
          lead: Agent aus Vorlage starten, Health prüfen und ersten Aufruf über urish/uri.
      snippet: |
        NL: "uruchom prosty agent lokalnie i sprawdź health"
        URI: health://agent/quickstart.local
        Run: urish run-agent quickstart.local --detach

    - id: quickstart-card
      layout: card
      order: 15
      docs: docs/examples.html#ex-01_quickstart_local
      i18n:
        pl:
          tag: Lokalny
          title: Uruchom · health · call
        en:
          tag: Local
          title: Run · health · call
        de:
          tag: Lokal
          title: Run · Health · Call
      snippet: |
        urish agent run quickstart.local
        urish agent health quickstart.local
        uri call health://agent/quickstart.local
---
<ul>
<li>Minimalny szablon agenta — gotowy Dockerfile, agent_card, health.</li>
<li>urish/uri jako jedyny interfejs do kontroli (run, status, logs via log://).</li>
<li>file:// dla źródeł i logów — spójne z nowymi przykładami (task_graph, markpact).</li>
</ul>
