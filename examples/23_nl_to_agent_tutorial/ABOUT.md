---
landing:
  cards:
    - id: wordpress-connector
      layout: connector
      order: 10
      logo: WP
      docs: docs/examples.html#ex-23_nl_to_agent_tutorial
      i18n:
        pl:
          tag: WordPress
          title: Lead z formularza do CRM
          lead: Hook formularza lub REST API wysyła zdarzenie do Taskinity, a agent dopisuje kontakt w CRM i odsyła potwierdzenie.
        en:
          tag: WordPress
          title: Form lead to CRM
          lead: Form hook or REST API sends an event to Taskinity; the agent adds the contact in CRM and sends confirmation.
        de:
          tag: WordPress
          title: Formular-Lead ins CRM
          lead: Form-Hook oder REST-API sendet Event an Taskinity; Agent trägt Kontakt ins CRM ein.
      snippet: |
        NL: "połącz formularz WordPress z CRM i alertuj błędy"
        URI: workflow://lead/wordpress-to-crm
        API: POST /api/uri/call

    - id: wordpress-card
      layout: card
      order: 110
      docs: docs/examples.html#ex-23_nl_to_agent_tutorial
      i18n:
        pl:
          tag: WordPress
          title: WP · formularze · REST
        en:
          tag: WordPress
          title: WP · forms · REST
        de:
          tag: WordPress
          title: WP · Formulare · REST
      snippet: |
        wp_remote_post('http://taskinity.local/api/uri/call', [
          'body' => json_encode(['uri' => 'workflow://order/wp-to-crm', 'dry_run' => true]),
        ]);
---

<ul>
<li>Plugin lub <code>functions.php</code>: hook <code>woocommerce_order_status_changed</code> → webhook do Taskinity.</li>
<li>Application Password + REST API — odczyt statusu bez edycji core WP.</li>
<li>Formularz kontaktowy / lead → URI workflow (mail → CRM → potwierdzenie).</li>
</ul>
