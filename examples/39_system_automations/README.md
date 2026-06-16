# Example 39: System automations (TUI + GUI)

Ten przykład pokazuje **10 automatyzacji systemowych** od sprawdzenia `env://`, przez `apt` i Docker, po sterowanie przeglądarką (`browser://`) i pulpitem (`kvm://`, `him://`, `ocr://`, `llm://`, `rdp://`).

Format wejściowy: kompaktowy **uri2flow** (`*.uri.flow.yaml`).

## Flow

| # | Plik | Opis |
|---|------|------|
| 01 | `01-check-env.uri.flow.yaml` | `env://` health + masked secret + echo |
| 02 | `02-apt-update.uri.flow.yaml` | `apt-get update/upgrade` (TUI) |
| 03 | `03-install-browser.uri.flow.yaml` | instalacja Chromium |
| 04 | `04-docker-stack.uri.flow.yaml` | uruchom stacki urisys + health HTTP |
| 05 | `05-browser-health.uri.flow.yaml` | Chrome → health agenta |
| 06 | `06-browser-capture.uri.flow.yaml` | Chrome → example.com |
| 07 | `07-gui-software-center.uri.flow.yaml` | HIM + KVM (Software Center) |
| 08 | `08-llm-guided-click.uri.flow.yaml` | OCR + LLM vision → klik |
| 09 | `09-rdp-session-smoke.uri.flow.yaml` | RDP + KVM smoke |
| 10 | `10-full-system-browser.uri.flow.yaml` | master: apt → browser → KVM |

## Mock smoke (domyślnie)

```bash
bash examples/39_system_automations/run.sh
```

Pipeline:

- **Wszystkie 10 flow:** `uri2flow validate` → `expand`
- **uri3 (env + browser):** flow 01, 05, 06 → `uri3 validate-workflow` → `dry-run`
- **shell:// (TUI):** flow 02–04, 10 → kompilacja uri2flow; wykonanie przez `uri2run` / `urish call`
- **urisys (KVM/HIM/OCR/LLM/RDP):** flow 07–09 → kompilacja; wykonanie przez `urisys-rdp flow --dry-run`

## Voice (opcjonalnie)

```bash
URISYS_RUN_VOICE=1 bash examples/39_system_automations/run.sh
```

Używa `stt://mock/transcribe` → `voice://command/from-text` → `uri2flow expand` (jak example 21).

## Real (opcjonalnie)

Wymaga działających kontenerów `uribrowser-docker` (:8792), `urikvm-docker` (:8793), `urirdp-docker` (:8795), `urienv-docker` (:8790):

```bash
URISYS_RUN_REAL=1 bash examples/39_system_automations/run.sh
```

## llm:// i env://

Handlery `llm://` w `urirdp`/`urikvm` rozwiązują `LLM_MODEL`, `OPENROUTER_API_KEY` itd. przez **`env://` policy** (allowlist w `urienv-docker/docker/config/env-policy.yaml`), z fallbackiem do `os.environ` / `urisys/.env`.

## Powiązane

- [`urisys/urisys-automation-lab`](../../../urisys/urisys-automation-lab/) — 10 flow + STT/chat/WebRTC UI (:8099)
- [`examples/15_compact_uri_flow`](../15_compact_uri_flow/README.md) — format uri2flow
- [`examples/21_touri_voice`](../21_touri_voice/README.md) — `stt://` / `voice://`
- [`urisys/urikvm-docker/flows/kvm-click-ok.uri.flow.yaml`](../../../urisys/urikvm-docker/flows/kvm-click-ok.uri.flow.yaml) — wzorzec KVM
