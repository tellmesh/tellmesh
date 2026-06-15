# screenshot-analysis-agent

Analyze screenshot artifacts captured by desktop-operator and persist observations.

Canonical portable definition: contract, deployment, runtime and optional Docker service.

Sync: `hypervisor sync-agent-manifest screenshot-analysis-agent.local`

```markpact:agent screenshot-analysis-agent
version: 1
agent:
  id: agent://screenshot-analysis-agent
  name: screenshot-analysis-agent
  implementation: custom
  contract: contracts/agents/screenshot_analysis_agent.yaml
  package: agents/custom/screenshot_analysis_agent
  module: agents.custom.screenshot_analysis_agent.main:app
  version: 0.1.0
  python_package: screenshot_analysis_agent
  description: Analyze screenshot artifacts captured by desktop-operator and persist
    observations.
capabilities:
- name: analyze_screenshot
  type: command
  uri: analysis://screenshots/analyze
  command: AnalyzeScreenshot
  input_schema: app.screenshots.v1.AnalyzeScreenshotCommand
  output_schema: app.screenshots.v1.ScreenshotObservation
  emits:
  - ScreenshotObservationRecorded
  renderer: detail
  description: Analyze an artifact:// or file:// screenshot and append JSONL/Markdown
    observations.
- name: capture_and_analyze
  type: command
  uri: workflow://screenshots/capture-and-analyze
  command: CaptureAndAnalyze
  input_schema: app.screenshots.v1.CaptureAndAnalyzeCommand
  output_schema: app.screenshots.v1.CaptureAndAnalysisResult
  emits:
  - ScreenshotCaptured
  - ScreenshotObservationRecorded
  renderer: detail
  description: Ask desktop-operator to capture a page, then analyze the returned artifact.
- name: scheduled_capture_analysis
  type: command
  uri: cron://screenshots/capture-analysis/every-5-min
  command: RunScheduledCaptureAnalysis
  input_schema: app.screenshots.v1.CaptureAndAnalyzeCommand
  output_schema: app.screenshots.v1.CaptureAndAnalysisResult
  emits:
  - ScreenshotCaptureAnalysisTick
  renderer: detail
  description: Host schedule hook for running capture_and_analyze every five minutes.
```

```markpact:deployment screenshot-analysis-agent.local
deployment:
  id: screenshot-analysis-agent.local
  agent_ref: agent://screenshot-analysis-agent
  target_uri: local://agents/custom/screenshot_analysis_agent
  status: generated
  health_uri: http://localhost:8134/health
  card_uri: http://localhost:8134/.well-known/agent-card.json
  view_uri: view://process/agent/screenshot-analysis-agent.local/latest
metadata:
  source: custom_agent
  role: screenshot_analyzer
  contract: contracts/agents/screenshot_analysis_agent.yaml
runtime:
  run: hypervisor run-agent screenshot-analysis-agent.local --detach --wait-healthy
  inspect: hypervisor inspect-agent screenshot-analysis-agent.local
  describe: hypervisor describe-agent screenshot-analysis-agent.local
supervise:
  once: hypervisor supervise screenshot-analysis-agent.local --repair auto
  watch: hypervisor supervise screenshot-analysis-agent.local --watch --repair auto
    --interval 15
logs:
  hypervisor: log://hypervisor?grep=screenshot-analysis-agent.local
  process: log://file/output/logs/agents/screenshot-analysis-agent.local.process.log
manifest:
  self: markpact://agents/manifests/screenshot-analysis-agent.markpact.md
```

```markpact:runtime screenshot-analysis-agent.local
runtime:
  module: agents.custom.screenshot_analysis_agent.main:app
  path: /home/tom/github/wronai/hypervisor/agents/custom/screenshot_analysis_agent
  port: 8134
  health_uri: http://localhost:8134/health
  card_uri: http://localhost:8134/.well-known/agent-card.json
  command: /home/tom/github/wronai/hypervisor/.venv/bin/python3 -m uvicorn agents.custom.screenshot_analysis_agent.main:app
    --host 0.0.0.0 --port 8134
```
