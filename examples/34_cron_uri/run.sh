#!/usr/bin/env bash
# Example 34 — cron:// URI via touri (manifest → shell monitor).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

echo "== 34_cron_uri =="
echo "Registry: examples/20_touri_capabilities"

echo
echo "== touri validate =="
python -m touri.cli validate examples/20_touri_capabilities/www_landing_monitor_cron.uri.capability.yaml

echo
echo "== uri explain cron://www/monitor/landing =="
python -m urish.cli explain cron://www/monitor/landing

echo
echo "== uri call cron://www/monitor/landing --dry-run =="
python -m urish.cli call cron://www/monitor/landing --dry-run

echo
echo "== touri call (registry dry-run payload) =="
python -m touri.cli call cron://www/monitor/landing \
  --registry examples/20_touri_capabilities \
  --payload '{"dry_run":true}'

echo
echo "== host crontab status (optional) =="
bash scripts/www/install-cron.sh --status 2>/dev/null || echo "(no crontab entry yet — use install-cron.sh --install)"

echo
echo "PASS examples/34_cron_uri"
