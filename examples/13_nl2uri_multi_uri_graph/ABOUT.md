---
landing:
  cards:
    - id: nl2uri-graph-connector
      layout: connector
      order: 55
      logo: N2G
      docs: docs/examples.html#ex-13_nl2uri_multi_uri_graph
      i18n:
        pl:
          tag: NL2URI · graph
          title: Prompt NL → multi-URI graph (task + workflow)
          lead: Jeden prompt generuje task_plan + workflow_graph — złożone przepływy z zależnościami.
        en:
          tag: NL2URI · graph
          title: NL prompt → multi-URI graph (task + workflow)
          lead: One prompt generates task_plan + workflow_graph — complex flows with dependencies.
        de:
          tag: NL2URI · Graph
          title: NL-Prompt → Multi-URI-Graph (Task + Workflow)
          lead: Ein Prompt erzeugt task_plan + workflow_graph — komplexe Flows mit Abhängigkeiten.
      snippet: |
        NL: "zrób plan i graf dla multi-uri flow"
        Files: task_plan.yaml + workflow_graph.yaml + expanded.expected

    - id: nl2uri-graph-card
      layout: card
      order: 65
      docs: docs/examples.html#ex-13_nl2uri_multi_uri_graph
      i18n:
        pl:
          tag: Graph
          title: task + workflow graph
        en:
          tag: Graph
          title: task + workflow graph
        de:
          tag: Graph
          title: task + workflow graph
      snippet: |
        urish nl "..." --out task_plan.yaml
        urish uri2flow expand ...
---
<ul>
<li>NL → structured graph z edges i depends_on.</li>
<li>Porównanie task vs workflow (17_flow_vs_graph).</li>
<li>file:// do task_graph.yaml jako źródło (walidacja, explain).</li>
</ul>
