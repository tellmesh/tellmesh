---
landing:
  cards:
    - id: touri-caps-connector
      layout: connector
      order: 115
      logo: TC
      docs: docs/examples.html#ex-20_touri_capabilities
      i18n:
        pl:
          tag: Touri
          title: Rejestr capabilities (touri + markpact)
          lead: Dużo .uri.capability.yaml + markpact z README — centralna registry do discovery i call.
        en:
          tag: Touri
          title: Capabilities registry (touri + markpact)
          lead: Many .uri.capability.yaml + markpact from READMEs — central registry for discovery and call.
        de:
          tag: Touri
          title: Capabilities-Registry (touri + markpact)
          lead: Viele .uri.capability.yaml + Markpact aus READMEs.
      snippet: |
        NL: "pokaż capabilities dla weather i order"
        Registry: examples/20_touri_capabilities
        Call: urish touri call workflow... --registry ...

    - id: touri-caps-card
      layout: card
      order: 125
      docs: docs/examples.html#ex-20_touri_capabilities
      i18n:
        pl:
          tag: Registry
          title: touri + capabilities + markpact
        en:
          tag: Registry
          title: touri + capabilities + markpact
        de:
          tag: Registry
          title: touri + capabilities + markpact
      snippet: |
        urish touri call ... --registry examples/20_touri_capabilities
---
<ul>
<li>Centralne capabilities dla weather, bank, order, portal, screenshot itp.</li>
<li>Markpact z README (file://) + yaml — mieszane źródła.</li>
<li>Podstawa dla wszystkich workflow w innych przykładach.</li>
</ul>
