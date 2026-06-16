#!/usr/bin/env bash
# Example 34 — cron:// URI via touri (manifest → shell monitor).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

cleanup() {
  if [[ -n "${WWW_PID:-}" ]]; then
    kill "$WWW_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT

start_demo_www() {
  "${PYTHON:-python3}" - <<'PY' &
import http.server
import threading

HTML = b"""<!doctype html><html><body>
<article class="price-card"><h3>Audit</h3><div class="price">1000 PLN<span>meta</span></div></article>
<article class="price-card"><h3>Pilot</h3><div class="price">2000 PLN<span>meta</span></div></article>
</body></html>"""

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.rstrip("/") == "/www":
            self.path = "/www/"
        if self.path == "/www/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(HTML)
            return
        self.send_response(404)
        self.end_headers()

    def log_message(self, format, *args):
        return

server = http.server.ThreadingHTTPServer(("127.0.0.1", 8788), Handler)
threading.Thread(target=server.serve_forever, daemon=True).start()
print("demo www on http://127.0.0.1:8788/www/", flush=True)
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass
PY
  WWW_PID=$!
  sleep 0.5
}

echo "== 34_cron_uri =="
echo "Registry: examples/20_touri_capabilities"
start_demo_www

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
echo "== seed monitor baseline =="
rm -f output/monitoring/www-prices.json
python scripts/www/monitor_landing.py --url http://localhost:8788/www/ --reset-baseline

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
