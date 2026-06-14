# hypervisor


## AI Cost Tracking

![PyPI](https://img.shields.io/badge/pypi-costs-blue) ![Version](https://img.shields.io/badge/version-0.1.1-blue) ![Python](https://img.shields.io/badge/python-3.9+-blue) ![License](https://img.shields.io/badge/license-Apache--2.0-green)
![AI Cost](https://img.shields.io/badge/AI%20Cost-$0.03-orange) ![Human Time](https://img.shields.io/badge/Human%20Time-2.0h-blue) ![Model](https://img.shields.io/badge/Model-openrouter%2Fqwen%2Fqwen3--coder--next-lightgrey)

- 🤖 **LLM usage:** $0.0301 (1 commits)
- 👤 **Human dev:** ~$200 (2.0h @ $100/h, 30min dedup)

Generated on 2026-06-14 using [openrouter/qwen/qwen3-coder-next](https://openrouter.ai/qwen/qwen3-coder-next)

---

**WronAI Hypervisor** — centralny orchestrator i warstwa kontrolna (control plane) dla AI-powered desktop automation, pipeline'ów NLP-to-URI / NLP-to-action, flot agentów (koru, proxeen, tellm) oraz zwirtualizowanych środowisk wykonawczych.

> Repozytorium: https://github.com/wronai/hypervisor

## 🚀 Główne cechy (v0.1)

- Konfiguracja zunifikowana wokół `nlp2uri.yaml` (desktop URI compiler + rozszerzenia hypervisora)
- `Hypervisor` jako główny obiekt sterujący (start/stop, rejestracja agentów, status)
- Wbudowane domyślne konfiguracje + wyszukiwanie w XDG + nadpisywanie ENV
- CLI `hypervisor` z komendami: `status`, `config`, `start`, `stop`, `agent`
- Przygotowany pod event sourcing, pluginy i multi-agent supervision (stub w 0.1)
- Pełna kompatybilność z ekosystemem wronai (koru, nlp2uri, proxeen, vdisplay, iterun itp.)

## 📦 Instalacja

```bash
# z repo (editable)
pip install -e ".[dev]"

# po publikacji na PyPI
pip install hypervisor
```

## Szybki start

```bash
# wersja
hypervisor --version

# status
hypervisor status

# pełna konfiguracja (efektywna)
hypervisor config

# tylko ścieżka do configu
hypervisor config --path

# uruchom (stub — blokuje do Ctrl+C)
hypervisor start

# zarejestruj agenta (w pamięci)
hypervisor agent register koru-desktop-01
hypervisor status
```

### Python API

```python
from hypervisor import Hypervisor, get_config, load_config

hv = Hypervisor()
print(hv)
# Hypervisor(running=False, profile='normal', agents=0/8, ...)

hv.register_agent("proxeen-main")
hv.start()
print(hv.status())

# z własnym configiem
hv2 = Hypervisor.from_config("./my-nlp2uri.yaml")
```

## Konfiguracja

Hypervisor dziedziczy i rozszerza format `nlp2uri.yaml`:

```yaml
platform: auto
host_platform: linux
dry_run: false
capture_dir: /tmp/nlp2uri-captures

hypervisor:
  log_level: INFO
  max_agents: 8
  default_profile: normal          # fast | normal | full
  enable_event_sourcing: true
```

Kolejność precedencji (od najwyższej):
1. `--config /ścieżka/do/pliku.yaml`
2. `./nlp2uri.yaml` (bieżący katalog)
3. `~/.config/hypervisor/nlp2uri.yaml` (lub `$XDG_CONFIG_HOME`)
4. Wbudowane wartości domyślne pakietu

Nadpisania przez zmienne środowiskowe:
- `NLP2URI_PLATFORM`, `NLP2URI_DRY_RUN`, `NLP2URI_CAPTURE_DIR` itd.
- `HYPERVISOR_LOG_LEVEL`, `HYPERVISOR_MAX_AGENTS`, `HYPERVISOR_DEFAULT_PROFILE`

## Struktura projektu

```
hypervisor/
├── hypervisor/
│   ├── __init__.py
│   ├── cli.py
│   ├── config.py
│   ├── core.py
│   ├── data/
│   │   └── nlp2uri.yaml          # embedded defaults
│   └── py.typed
├── tests/
├── pyproject.toml
├── LICENSE
└── README.md
```

## Rozwój

```bash
# instalacja w trybie deweloperskim
pip install -e ".[dev]"

# testy
pytest -v

# lint
ruff check .

# uruchom CLI bezpośrednio
python -m hypervisor.cli status
```

## Powiązane projekty (wronai)

- [proxeen](https://github.com/wronai/proxeen) — AI Desktop Assistant (screen + voice + agents)
- [fraq](https://github.com/wronai/fraq) — Fractal Query Data Library + NLP2CMD
- [tellm](https://github.com/wronai/tellm) — voice / LLM components
- koru / nlp2uri / iterun / vdisplay — warstwa sterowania desktopem i URI

## Licencja

Apache-2.0 — patrz [LICENSE](LICENSE)

## Status

Alpha (0.1.x). API i komendy CLI mogą się jeszcze zmieniać do wersji 0.2 / 1.0.

Pull requesty i issue mile widziane.
