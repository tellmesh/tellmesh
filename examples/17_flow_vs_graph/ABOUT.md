---
landing:
  cards:
    - id: flow-vs-graph-connector
      layout: connector
      order: 98
      logo: FVG
      docs: docs/examples.html#ex-17_flow_vs_graph
      i18n:
        pl:
          tag: Porównanie
          title: Compact flow vs pełny graph
          lead: Ten sam przypadek biznesowy wyrażony jako krótki flow i jako pełny task_graph — różnice w czytelności i wykonaniu.
        en:
          tag: Comparison
          title: Compact flow vs full graph
          lead: Same business case as short flow vs full task_graph — readability vs execution differences.
        de:
          tag: Vergleich
          title: Kompakter Flow vs. voller Graph
          lead: Derselbe Anwendungsfall als kurzer Flow vs. voller Task-Graph.
      snippet: |
        NL: "porównaj flow i graph dla tego samego przypadku"
        Files: weather.uri.flow.yaml + expanded.expected.uri.graph.yaml

    - id: flow-vs-graph-card
      layout: card
      order: 108
      docs: docs/examples.html#ex-17_flow_vs_graph
      i18n:
        pl:
          tag: Flow vs Graph
          title: uri2flow + graph
        en:
          tag: Flow vs Graph
          title: uri2flow + graph
        de:
          tag: Flow vs Graph
          title: uri2flow + graph
      snippet: |
        urish uri2flow expand weather.uri.flow.yaml
        diff ... expanded.expected...
---
<ul>
<li>Dwa modele dla tego samego: compact (ludzki) vs expanded (wykonywalny).</li>
<li>uri2flow jako mostek.</li>
<li>Walidacja i explain działają na obu (file:// graph).</li>
</ul>
