# Voice with touri

STT/TTS from `tellm` are implemented as a **touri capability pack**, not a monolithic server.

```txt
Etap 1 (now): examples/21_touri_voice — manifesty + Python handlery
Etap 2: wspólne modele audio, profile, testy integracyjne
Etap 3: packages/uri2voice (gdy urośnie)
```

## Architecture

```txt
microphone / text
    → stt://...           (touri capability)
    → voice://command/... (nl2uri flow)
    → uri2flow expand
    → uri3 validate/run
    → tts://...           (touri capability)
```

`touri` resolves URIs through `*.uri.capability.yaml` — same pattern as weather or browser operator capabilities.

## Capability pack

| URI | Capability | Backend |
|-----|------------|---------|
| `stt://mock/transcribe` | `stt.mock.transcribe` | `uri2voice.stt:transcribe` |
| `tts://mock/speak` | `tts.mock.speak` | `uri2voice.tts:speak` |
| `voice://command/from-text` | `voice.command.from_text` | `uri2voice.voice_command:plan_voice_command` |

Location: [`examples/21_touri_voice/`](../examples/21_touri_voice/README.md)

## Commands

```bash
touri call stt://mock/transcribe \
  --registry examples/21_touri_voice \
  --payload '{"text":"otwórz Chrome i sprawdź health"}'

touri call voice://command/from-text \
  --registry examples/21_touri_voice \
  --payload '{"text":"wygeneruj agenta pogodowego, uruchom go lokalnie i sprawdź health w Chrome"}'

touri call tts://mock/speak \
  --registry examples/21_touri_voice \
  --payload '{"text":"Agent działa poprawnie"}'
```

## Pipeline after voice planning

```bash
uri2flow expand output/artifacts/voice/voice_command.uri.flow.yaml \
  --out output/artifacts/voice/voice_command.uri.graph.yaml

uri3 validate-workflow output/artifacts/voice/voice_command.uri.graph.yaml
uri3 run-workflow output/artifacts/voice/voice_command.uri.graph.yaml --dry-run
```

## What we took from tellm

| tellm concept | touri equivalent |
|---------------|------------------|
| `TellmBot.transcribe` | `stt://...` capability handler |
| `TellmBot.speak` | `tts://...` capability handler |
| `service_result` | shared `uri3.results.ServiceResult` envelope |
| `generate_test_audio` | mock STT with `text` / `transcript_file` |
| `TellmServer.process_request` | **not ported** — too monolithic |

## Real STT/TTS (later)

### Local whisper

```yaml
capability:
  id: stt.local.whisper
  scheme: stt
  uri_template: stt://local/whisper
backend:
  type: python
  target: python://touri_examples_voice.whisper_local:transcribe
```

### Local piper

```yaml
capability:
  id: tts.local.piper
  scheme: tts
  uri_template: tts://local/piper
backend:
  type: python
  target: python://touri_examples_voice.piper_local:speak
```

### Cloud (secrets by URI)

Never embed API keys in manifests:

```yaml
backend:
  type: python
  target: python://touri_examples_voice.openai_stt:transcribe
  extra:
    model: gpt-4o-transcribe
    api_key: env://OPENAI_API_KEY
```

Or reference `config/llm.uri.yaml` profiles from handler code.

## Anti-tellm rules

- Mock STT must not pretend to read real audio without validation
- TTS artifacts are metadata mocks until real audio engines are wired
- `voice://command/from-text` produces **flow proposals** — validate with `uri2flow` / `uri3` before execution
- Use `ServiceResult` with structured `errors[].code`, not bare `ok=true`

See [`ANTI_TELLM.md`](./ANTI_TELLM.md) and [`TOURI.md`](./TOURI.md).

## Tests

```bash
pytest tests/touri/test_voice_capabilities.py -q
make voice-demo
```
