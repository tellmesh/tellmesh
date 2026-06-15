---
landing:
  cards:
    - id: ssh-remote-connector
      layout: connector
      order: 12
      logo: SSH
      docs: docs/examples.html#ex-03_ssh_remote_agent
      i18n:
        pl:
          tag: Zdalny · SSH
          title: Agent na zdalnej maszynie przez SSH
          lead: Docker testenv + SSH — deploy, scan i call agenta bez ręcznego kopiowania kluczy.
        en:
          tag: Remote · SSH
          title: Agent on remote machine via SSH
          lead: Docker testenv + SSH — deploy, scan and call the agent without manual key copying.
        de:
          tag: Remote · SSH
          title: Agent auf Remote-Maschine über SSH
          lead: Docker-Testumgebung + SSH — Deployment, Scan und Aufruf ohne manuelles Key-Copying.
      snippet: |
        NL: "zeskanuj agenta przez SSH i wywołaj health"
        URI: ssh://... + uri3 scan ssh

    - id: ssh-remote-card
      layout: card
      order: 22
      docs: docs/examples.html#ex-03_ssh_remote_agent
      i18n:
        pl:
          tag: SSH
          title: Docker + SSH testenv
        en:
          tag: SSH
          title: Docker + SSH testenv
        de:
          tag: SSH
          title: Docker + SSH-Testumgebung
      snippet: |
        make docker-ssh-up
        urish uri3 scan ssh://...
---
<ul>
<li>Symulacja zdalnego hosta (Docker + ssh na porcie 2222).</li>
<li>Pełny cykl: deploy → scan → health/call przez urish.</li>
<li>Bezpieczne — hasło w env, bez ręcznego scp.</li>
</ul>
