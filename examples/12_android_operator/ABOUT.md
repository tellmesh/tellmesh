---
landing:
  cards:
    - id: android-connector
      layout: connector
      order: 48
      logo: AND
      docs: docs/examples.html#ex-12_android_operator
      i18n:
        pl:
          tag: Android
          title: Operator Android (UI Automator / pcwin)
          lead: Automatyzacja Androida z poziomu URI — open app, wpisywanie, screenshot.
        en:
          tag: Android
          title: Android operator (UI Automator / pcwin)
          lead: Android automation via URI — open app, type, screenshot.
        de:
          tag: Android
          title: Android-Operator (UI Automator / pcwin)
          lead: Android-Automatisierung via URI — App öffnen, tippen, Screenshot.
      snippet: |
        NL: "otwórz apkę i wpisz tekst na Androidzie"
        Task: examples/12_android_operator/task.android.yaml
        Run: bash .../run.sh

    - id: android-card
      layout: card
      order: 58
      docs: docs/examples.html#ex-12_android_operator
      i18n:
        pl:
          tag: Mobile
          title: Android task + operator
        en:
          tag: Mobile
          title: Android task + operator
        de:
          tag: Mobile
          title: Android task + operator
      snippet: |
        urish run task.android.yaml --approve
---
<ul>
<li>Cross-platform: Android + pcwin (Windows) w jednym modelu URI.</li>
<li>task.*.yaml definiuje kroki — wykonywane przez operator.</li>
<li>Logi i artefakty z file:// / log:// dla inspekcji.</li>
</ul>
