---
landing:
  cards:
    - id: physical-ops-connector
      layout: connector
      order: 170
      logo: PO
      docs: docs/examples.html#ex-36_physical_ops
      i18n:
        pl:
          tag: Fizyczne
          title: Operacje fizyczne (device + robot)
          lead: task.device.yaml + task.robot.yaml — sterowanie urządzeniami i robotami przez URI.
        en:
          tag: Physical
          title: Physical operations (device + robot)
          lead: task.device.yaml + task.robot.yaml — control devices and robots via URI.
        de:
          tag: Physisch
          title: Physische Operationen (Gerät + Roboter)
          lead: task.device.yaml + task.robot.yaml — Steuerung von Geräten und Robotern via URI.
      snippet: |
        NL: "wykonaj operację na robocie i urządzeniu"
        Tasks: task.device.yaml + task.robot.yaml
        Run: bash examples/36_physical_ops/run.sh

    - id: physical-ops-card
      layout: card
      order: 180
      docs: docs/examples.html#ex-36_physical_ops
      i18n:
        pl:
          tag: Robot/Device
          title: physical ops + tasks
        en:
          tag: Robot/Device
          title: physical ops + tasks
        de:
          tag: Roboter/Gerät
          title: physical ops + tasks
      snippet: |
        urish run task.device.yaml --approve
        urish run task.robot.yaml --approve
---
<ul>
<li>Ekstensja URI na świat fizyczny (roboty, urządzenia).</li>
<li>task.*.yaml jako definicja kroków.</li>
<li>Logi, artefakty i file:// dla inspekcji operacji.</li>
</ul>
