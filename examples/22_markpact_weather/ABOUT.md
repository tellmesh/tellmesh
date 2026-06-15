---
landing:
  cards:
    - id: markpact-weather-connector
      layout: connector
      order: 142
      logo: MW
      docs: docs/examples.html#ex-22_markpact_weather
      i18n:
        pl:
          tag: Markpact
          title: Markpact + weather (README jako źródło)
          lead: README z markpact blocks → capabilities + flows (uri2pact + touri).
        en:
          tag: Markpact
          title: Markpact + weather (README as source)
          lead: README with markpact blocks → capabilities + flows (uri2pact + touri).
        de:
          tag: Markpact
          title: Markpact + Wetter (README als Quelle)
          lead: README mit Markpact-Blöcken → Capabilities + Flows.
      snippet: |
        NL: "użyj markpact z README do weather"
        Run: bash examples/22_markpact_weather/run.sh
        Registry: markpact://...

    - id: markpact-weather-card
      layout: card
      order: 152
      docs: docs/examples.html#ex-22_markpact_weather
      i18n:
        pl:
          tag: Markpact
          title: README + markpact + uri2pact
        en:
          tag: Markpact
          title: README + markpact + uri2pact
        de:
          tag: Markpact
          title: README + markpact + uri2pact
      snippet: |
        urish touri call ... --registry markpact://...
---
<ul>
<li>Markpact w README jako ludzkoczytelne źródło capabilities.</li>
<li>file:// do README (po zmianach w core) + load via uri2pact.</li>
<li>Przykład jak dokumentacja staje się executable registry.</li>
</ul>
