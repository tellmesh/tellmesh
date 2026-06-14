# Example 21: touri voice capabilities

STT/TTS/voice command as a **touri capability pack** backed by **`uri2voice`** execution handlers.

Schemes:

```txt
stt://...
tts://...
voice://...
```

Handlers live in `packages/uri2voice/uri2voice/` (mock MVP). Capability manifests remain in this example directory.

## Quick start

```bash
pip install -e '.[dev]'
```

Run the full mock pipeline:

```bash
examples/21_touri_voice/run.sh
```

## Mock STT

```bash
touri validate examples/21_touri_voice/stt_mock.uri.capability.yaml
touri call stt://mock/transcribe \
  --registry examples/21_touri_voice \
  --payload '{"text":"otwórz Chrome i sprawdź health"}'
```

Without `text`, returns a default weather-agent prompt (useful for pipeline demos).

## Mock TTS

```bash
touri call tts://mock/speak \
  --registry examples/21_touri_voice \
  --payload '{"text":"Agent działa poprawnie"}'
```

Writes `output/artifacts/voice/tts_*.json` and returns `artifact_uri`.

## Voice command → nl2uri flow

```bash
touri call voice://command/from-text \
  --registry examples/21_touri_voice \
  --payload '{"text":"wygeneruj agenta pogodowego, uruchom go lokalnie i sprawdź health w Chrome"}'
```

Writes `output/artifacts/voice/voice_command.uri.flow.yaml`.

## Full mock pipeline

```bash
touri call stt://mock/transcribe \
  --registry examples/21_touri_voice \
  --payload '{"text":"wygeneruj agenta pogodowego, uruchom go lokalnie i sprawdź health w Chrome"}'

touri call voice://command/from-text \
  --registry examples/21_touri_voice \
  --payload '{"text":"wygeneruj agenta pogodowego, uruchom go lokalnie i sprawdź health w Chrome"}'

uri2flow expand output/artifacts/voice/voice_command.uri.flow.yaml \
  --out output/artifacts/voice/voice_command.uri.graph.yaml

uri3 validate-workflow output/artifacts/voice/voice_command.uri.graph.yaml
uri3 run-workflow output/artifacts/voice/voice_command.uri.graph.yaml --dry-run

touri call tts://mock/speak \
  --registry examples/21_touri_voice \
  --payload '{"text":"Workflow został przygotowany i przeszedł walidację."}'
```

## List capabilities

```bash
touri list examples/21_touri_voice
```

## Next steps

- `stt://local/whisper`, `tts://local/piper` — local engines
- Cloud STT/TTS via `env://` secrets (never embed keys in manifests)

See [`docs/VOICE_WITH_TOURI.md`](../../docs/VOICE_WITH_TOURI.md).
