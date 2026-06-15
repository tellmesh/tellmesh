# Example 36 — physical ops robot/device URIs

Mock run; no robot or field device required:

```bash
python -m uri2ops.cli validate examples/36_physical_ops/task.robot.yaml
python -m uri2ops.cli run examples/36_physical_ops/task.robot.yaml --adapter mock --approve
python -m uri2ops.cli validate examples/36_physical_ops/task.device.yaml
python -m uri2ops.cli run examples/36_physical_ops/task.device.yaml --adapter mock --approve
```

Supported URI shapes:

- `robot://robot/{id}/state`
- `robot://robot/{id}/move`
- `robot://robot/{id}/stop`
- `robot://robot/{id}/mission/{mission_id}/start`
- `device://device/{id}/status`
- `device://device/{id}/read`
- `device://device/{id}/write`

`robot.move`, `robot.stop`, `robot.mission_start` and `device.write` are physical
mutations. Production adapters must require explicit approval and should add a
human/safety gate before the command.
