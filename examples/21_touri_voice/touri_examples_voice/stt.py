"""Deprecated — use ``uri2voice`` handlers directly."""

from uri2voice.stt import transcribe
from uri2voice.tts import speak
from uri2voice.voice_command import plan_voice_command

__all__ = ["transcribe", "speak", "plan_voice_command"]
