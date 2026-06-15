---
landing:
  cards:
    - id: nl2a-weather-connector
      layout: connector
      order: 15
      logo: NL
      docs: docs/examples.html#ex-04_nl2a_weather_map
      i18n:
        pl:
          tag: NL2A · pogoda
          title: Prompt NL → agent pogodowy (mapa HTML)
          lead: Z jednego zdania w NL powstaje kontrakt, kod agenta, capabilities i workflow — bez ręcznego pisania YAML.
        en:
          tag: NL2A · weather
          title: NL prompt → weather agent (HTML map)
          lead: One NL sentence becomes contract, agent code, capabilities and workflow — no manual YAML.
        de:
          tag: NL2A · Wetter
          title: NL-Prompt → Wetter-Agent (HTML-Karte)
          lead: Ein NL-Satz wird zu Vertrag, Agent-Code, Capabilities und Workflow — kein manuelles YAML.
      snippet: |
        NL: "generuj mapę pogody na 14 dni w html"
        URI: resource://weather/maps/krakow/forecast/14
        Agent: agents/generated/weather_map_agent

    - id: nl2a-weather-card
      layout: card
      order: 25
      docs: docs/examples.html#ex-04_nl2a_weather_map
      i18n:
        pl:
          tag: NL → kod
          title: nl2a · generator · urigen
        en:
          tag: NL → code
          title: nl2a · generator · urigen
        de:
          tag: NL → Code
          title: nl2a · Generator · urigen
      snippet: |
        nl2a -p "..." --no-llm
        make generate
        urish ecosystem apply ...
---
<ul>
<li>Pełny pipeline NL → domain pack → kontrakt → wygenerowany agent + README z markpact.</li>
<li>Pliki w agents/generated/ + .generated.yaml z file:// dla markpact_readme.</li>
<li>Workflowy i capabilities gotowe do użycia przez touri/urish.</li>
</ul>
