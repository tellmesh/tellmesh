---
landing:
  cards:
    - id: compact-flow-connector
      layout: connector
      order: 78
      logo: CF
      docs: docs/examples.html#ex-15_compact_uri_flow
      i18n:
        pl:
          tag: Flow
          title: Kompaktowy URI flow → expanded graph
          lead: Krótki .uri.flow.yaml z branchami → pełny workflow_graph z edges (uri2flow).
        en:
          tag: Flow
          title: Compact URI flow → expanded graph
          lead: Short .uri.flow.yaml with branches → full workflow_graph with edges (uri2flow).
        de:
          tag: Flow
          title: Kompakter URI-Flow → erweiterter Graph
          lead: Kurze .uri.flow.yaml mit Branches → voller Workflow-Graph.
      snippet: |
        NL: "zrób kompaktowy flow z branchami"
        File: branching.uri.flow.yaml
        Expand: urish uri2flow expand ...

    - id: compact-flow-card
      layout: card
      order: 88
      docs: docs/examples.html#ex-15_compact_uri_flow
      i18n:
        pl:
          tag: uri2flow
          title: compact flow + expand + run
        en:
          tag: uri2flow
          title: compact flow + expand + run
        de:
          tag: uri2flow
          title: compact flow + expand + run
      snippet: |
        urish uri2flow expand branching.uri.flow.yaml
        urish run ... --dry-run
---
<ul>
<li>Prosty, czytelny format flow dla ludzi.</li>
<li>Automatyczna ekspansja do pełnego grafu (edges, depends).</li>
<li>Dry-run i approve — bezpieczne uruchamianie.</li>
</ul>
