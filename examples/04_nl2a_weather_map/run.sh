#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
bash "$ROOT/../resource-agent-hypervisor/scripts/ci/ensure_editable_install.sh"
make nl2a-weather
test -d domains/weather_map
test -f domains/weather_map/uri_tree.yaml
echo "PASS examples/04_nl2a_weather_map"
