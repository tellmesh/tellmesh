# weather-map-agent

Generate forecast weather maps as HTML URL artifacts.

Canonical portable definition: contract, deployment, runtime and optional Docker service.

Sync: `hypervisor sync-agent-manifest weather-map-agent.local`

```markpact:agent weather-map-agent
version: 1
agent:
  id: agent://weather-map-agent
  name: weather-map-agent
  implementation: generated
  contract: contracts/agents/weather_map_agent.yaml
  package: agents/generated/weather_map_agent
  module: agents.generated.weather_map_agent.main:app
  version: 0.1.0
  python_package: weather_map_agent
  description: Generate forecast weather maps as HTML URL artifacts.
capabilities:
- name: read_weather_map
  type: resource_read
  description: Read generated weather map HTML view for a location and forecast horizon.
  uri: resource://weather/maps/{place}/forecast/{days}
  output_schema: app.weather.v1.WeatherMapHtmlView
  renderer: html
- name: generate_weather_map
  type: command
  description: Generate a weather map forecast HTML view for a location.
  command: GenerateWeatherMap
  input_schema: app.weather.v1.GenerateWeatherMapCommand
  emits:
  - WeatherMapGenerationRequested
  - WeatherMapGenerated
```

```markpact:deployment weather-map-agent.local
deployment:
  id: weather-map-agent.local
  agent_ref: agent://weather-map-agent
  target_uri: local://agents/generated/weather_map_agent
  status: generated
  health_uri: http://localhost:8105/health
  card_uri: http://localhost:8105/.well-known/agent-card.json
  view_uri: view://process/agent/weather-map-agent.local/latest
metadata:
  source: uri_tree
  domain_id: weather_map
  contract: contracts/agents/weather_map_agent.yaml
runtime:
  run: hypervisor run-agent weather-map-agent.local --detach --wait-healthy
  inspect: hypervisor inspect-agent weather-map-agent.local
  describe: hypervisor describe-agent weather-map-agent.local
supervise:
  once: hypervisor supervise weather-map-agent.local --repair auto
  watch: hypervisor supervise weather-map-agent.local --watch --repair auto --interval
    15
logs:
  hypervisor: log://hypervisor?grep=weather-map-agent.local
  process: log://file/output/logs/agents/weather-map-agent.local.process.log
manifest:
  self: markpact://agents/manifests/weather-map-agent.markpact.md
```

```markpact:runtime weather-map-agent.local
runtime:
  module: agents.generated.weather_map_agent.main:app
  path: /home/tom/github/tellmesh/tellmesh/agents/generated/weather_map_agent
  port: 8105
  health_uri: http://localhost:8105/health
  card_uri: http://localhost:8105/.well-known/agent-card.json
  command: /home/tom/github/tellmesh/tellmesh/.venv/bin/python3 -m uvicorn agents.generated.weather_map_agent.main:app
    --host 0.0.0.0 --port 8105
```

```markpact:docker weather-map-agent
service:
  name: weather-map-agent
  build:
    context: .
    dockerfile: agents/generated/weather_map_agent/Dockerfile
  container_name: weather-map-agent
  ports:
  - 8105:8105
  healthcheck:
    test:
    - CMD
    - curl
    - -f
    - http://localhost:8105/health
  environment:
    RESOURCE_RUNTIME_URL: http://host.docker.internal:8000
compose:
  output: output/deployments/weather-map-agent/docker-compose.yaml
```
