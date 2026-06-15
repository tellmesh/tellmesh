# Operator Agents

Operator agents expose generic execution capabilities. They are not business
domains and must not contain customer workflows, scenario routing or generated
domain-agent code.

## Desktop Operator

[`desktop_operator.yaml`](./desktop_operator.yaml) defines
`agent://desktop-operator`, a uri2ops-backed capability agent for:

- browser operations,
- screen observations,
- typed input,
- Windows UI Automation operations,
- Android device operations.

Run it directly:

```bash
uri2ops serve --host 127.0.0.1 --port 8791
```

Guide: [`docs/DESKTOP_AUTONOMY.md`](../../docs/DESKTOP_AUTONOMY.md).

Generic capability routing lives in
[`domains/desktop_ops/`](../../domains/desktop_ops/). Keep vertical workflows in
their own domain packs and reference `browser://`, `pcwin://`, `android://`,
`screen://` or `input://` URIs from there.

## Device And Robot Operator

[`device_robot_operator.yaml`](./device_robot_operator.yaml) defines
`agent://device-robot-operator`, a uri2ops-backed capability agent for:

- robot state, movement, stop and mission start,
- device status, read and write operations.

Run it directly:

```bash
uri2ops serve --host 127.0.0.1 --port 8792
```

Guide: [`docs/PHYSICAL_AUTONOMY.md`](../../docs/PHYSICAL_AUTONOMY.md).

Generic physical routing lives in
[`domains/physical_ops/`](../../domains/physical_ops/). Keep factory,
warehouse, office or customer-specific workflows in their own domain packs and
reference `robot://` or `device://` URIs from there.
