# Example 13 — uri2ops Windows UI Automation operator (v0.4)

Mock run (works on any OS):

```bash
python -m uri2ops.cli validate examples/13_pcwin_operator/task.pcwin.yaml
python -m uri2ops.cli run examples/13_pcwin_operator/task.pcwin.yaml --adapter mock --approve
```

Real UIA run on Windows:

```powershell
pip install -e ".[windows]"
python -m uri2ops.cli run examples/13_pcwin_operator/task.pcwin.yaml --adapter uia --approve
```

Auto picks UIA on Windows when `pywinauto` is installed, otherwise mock:

```bash
python -m uri2ops.cli run examples/13_pcwin_operator/task.pcwin.yaml --adapter auto --approve
```

Supported URIs:

- `pcwin://window/{id}/focus`
- `pcwin://control/{automation_id}/click`

The focused window is kept in the task session; subsequent `click` steps search controls in that window by AutomationId or name.
