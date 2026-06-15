---
landing:
  cards:
    - id: uri3-scan-connector
      layout: connector
      order: 8
      logo: U3
      docs: docs/examples.html#ex-02_uri3_scan_http
      i18n:
        pl:
          tag: URI3 · scan
          title: Skan HTTP i odkrywanie zasobów
          lead: uri3 scan http znajduje dostępne endpointy, health, capabilities — bez pisania klienta.
        en:
          tag: URI3 · scan
          title: HTTP scan and resource discovery
          lead: uri3 scan http discovers endpoints, health, capabilities — no custom client needed.
        de:
          tag: URI3 · Scan
          title: HTTP-Scan und Ressourcen-Erkennung
          lead: uri3 scan http entdeckt Endpunkte, Health, Capabilities — kein eigener Client nötig.
      snippet: |
        NL: "zeskanuj lokalny agent i pokaż co oferuje"
        URI: uri3 scan http://localhost:8101

    - id: uri3-scan-card
      layout: card
      order: 18
      docs: docs/examples.html#ex-02_uri3_scan_http
      i18n:
        pl:
          tag: Odkrywanie
          title: Scan · explain · call
        en:
          tag: Discovery
          title: Scan · explain · call
        de:
          tag: Entdeckung
          title: Scan · Explain · Call
      snippet: |
        urish uri3 scan http://localhost:8105
        urish explain health://agent/weather-map-agent.local
---
<ul>
<li>Automatyczne odkrywanie bez znajomości API agenta.</li>
<li>Połączone z explain i call — jeden spójny model URI.</li>
<li>file:// i markpact dla źródeł definicji — łatwe audytowanie.</li>
</ul>
