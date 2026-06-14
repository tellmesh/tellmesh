# Example 12 — uri2ops Android operator (v0.3)

Mock run (no device required):

```bash
python -m uri2ops.cli validate examples/12_android_operator/task.android.yaml
python -m uri2ops.cli run examples/12_android_operator/task.android.yaml --adapter mock --approve
```

ADB run (device or emulator connected):

```bash
adb devices
python -m uri2ops.cli run examples/12_android_operator/task.android.yaml --adapter adb --approve
```

Auto picks ADB when a device is online, otherwise mock:

```bash
python -m uri2ops.cli run examples/12_android_operator/task.android.yaml --adapter auto --approve
```

Supported URIs:

- `android://device/{id}/screenshot`
- `android://device/{id}/dump_ui`
- `android://device/{id}/tap`

Tap payload accepts `x`/`y` coordinates or a `selector` matched against the UI Automator XML dump.
