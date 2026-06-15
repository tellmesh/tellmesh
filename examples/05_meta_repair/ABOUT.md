---
landing:
  cards:
    - id: meta-repair-connector
      layout: connector
      order: 20
      logo: MR
      docs: docs/examples.html#ex-05_meta_repair
      i18n:
        pl:
          tag: Meta · repair
          title: Naprawa zepsutego agenta przez meta-agent
          lead: meta_agent repair analizuje broken_agent.yaml, proponuje zmiany i stosuje — pełny cykl samonaprawy.
        en:
          tag: Meta · repair
          title: Repair broken agent via meta-agent
          lead: meta_agent repair analyzes broken_agent.yaml, proposes changes and applies — full self-healing cycle.
        de:
          tag: Meta · Repair
          title: Reparatur eines kaputten Agenten über Meta-Agent
          lead: meta_agent repair analysiert broken_agent.yaml, schlägt Änderungen vor und wendet sie an.
      snippet: |
        NL: "napraw zepsutego agenta z pliku broken_agent.yaml"
        Command: python -m meta_agent.cli repair examples/05_meta_repair/broken_agent.yaml
        Check: "changed: true"

    - id: meta-repair-card
      layout: card
      order: 30
      docs: docs/examples.html#ex-05_meta_repair
      i18n:
        pl:
          tag: Samonaprawa
          title: meta_agent · diagnose · apply
        en:
          tag: Self-healing
          title: meta_agent · diagnose · apply
        de:
          tag: Selbstheilung
          title: meta_agent · diagnose · apply
      snippet: |
        python -m meta_agent.cli repair examples/05_meta_repair/broken_agent.yaml
---
<ul>
<li>Analiza → propozycja → apply bez ręcznej edycji.</li>
<li>Integracja z repair loops w hypervisorze (urish repair diagnose/apply).</li>
<li>Przykład jak agenci mogą się "uczyć" i naprawiać na podstawie incydentów.</li>
</ul>
