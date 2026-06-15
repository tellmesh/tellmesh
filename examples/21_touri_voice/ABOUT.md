---
landing:
  cards:
    - id: touri-voice-connector
      layout: connector
      order: 128
      logo: TV
      docs: docs/examples.html#ex-21_touri_voice
      i18n:
        pl:
          tag: Voice
          title: Voice (STT + TTS + voice command)
          lead: stt_whisper / tts + voice_command.uri.capability — pełny głosowy interfejs do URI.
        en:
          tag: Voice
          title: Voice (STT + TTS + voice command)
          lead: stt_whisper / tts + voice_command.uri.capability — full voice interface to URI.
        de:
          tag: Voice
          title: Voice (STT + TTS + Voice Command)
          lead: stt_whisper / tts + voice_command.uri.capability — vollständige Sprachschnittstelle zu URI.
      snippet: |
        NL: "użyj głosu do wywołania health agenta"
        Caps: stt_whisper.uri.capability.yaml + tts_mock...
        Run: bash examples/21_touri_voice/run.sh

    - id: touri-voice-card
      layout: card
      order: 138
      docs: docs/examples.html#ex-21_touri_voice
      i18n:
        pl:
          tag: Głos
          title: stt + tts + voice
        en:
          tag: Voice
          title: stt + tts + voice
        de:
          tag: Stimme
          title: stt + tts + voice
      snippet: |
        urish call 'voice://command' --payload '{"text":"..."}'
---
<ul>
<li>STT (whisper local/cloud), TTS mock, voice command.</li>
<li>Capabilities w touri_examples_voice/.</li>
<li>Integracja z chat voice (example 21).</li>
</ul>
