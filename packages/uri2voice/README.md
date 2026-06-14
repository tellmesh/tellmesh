# uri2voice

Execution layer for voice-related URI schemes. Capability manifests stay in `touri`
(or example packs under `examples/21_touri_voice/`).

## Schemes

```txt
stt://...    speech-to-text
tts://...    text-to-speech (artifact output)
voice://...  voice command → nl2uri compact flow
```

## Handlers (mock MVP)

| URI | Handler |
|-----|---------|
| `stt://mock/transcribe` | `uri2voice.stt:transcribe` |
| `tts://mock/speak` | `uri2voice.tts:speak` |
| `voice://command/from-text` | `uri2voice.voice_command:plan_voice_command` |

## Usage via touri

```bash
touri call stt://mock/transcribe \
  --registry examples/21_touri_voice \
  --payload '{"text":"otwórz Chrome i sprawdź health"}'
```

See [`examples/21_touri_voice/`](../../examples/21_touri_voice/) and [`docs/VOICE_WITH_TOURI.md`](../../docs/VOICE_WITH_TOURI.md).
