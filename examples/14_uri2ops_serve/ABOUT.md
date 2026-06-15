---
landing:
  cards:
    - id: uri2ops-serve-connector
      layout: connector
      order: 62
      logo: O2S
      docs: docs/examples.html#ex-14_uri2ops_serve
      i18n:
        pl:
          tag: URI2OPS
          title: Serwer operacji (A2A/MCP/REST)
          lead: uri2ops serve wystawia registry capabilities jako API — agenci i zewnętrzne systemy wołają przez URI.
        en:
          tag: URI2OPS
          title: Operations server (A2A/MCP/REST)
          lead: uri2ops serve exposes registry capabilities as API — agents and external systems call via URI.
        de:
          tag: URI2OPS
          title: Operations-Server (A2A/MCP/REST)
          lead: uri2ops serve stellt Registry-Capabilities als API bereit.
      snippet: |
        NL: "uruchom serwer operacji i wystaw capabilities"
        Run: bash examples/14_uri2ops_serve/run.sh
        Call: urish call browser://... (via served registry)

    - id: uri2ops-serve-card
      layout: card
      order: 72
      docs: docs/examples.html#ex-14_uri2ops_serve
      i18n:
        pl:
          tag: Serwer
          title: serve · registry · call
        en:
          tag: Server
          title: serve · registry · call
        de:
          tag: Server
          title: serve · registry · call
      snippet: |
        urish uri2ops serve --port 8791
        curl http://localhost:8791/health
---
<ul>
<li>Operator runtime jako usługa — A2A, MCP, REST.</li>
<li>Centralna registry capabilities (touri).</li>
<li>Bezpieczne proxy dla browser/desktop ops.</li>
</ul>
