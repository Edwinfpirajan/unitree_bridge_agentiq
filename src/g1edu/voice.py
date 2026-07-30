from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


class VoiceError(RuntimeError):
    pass


class VoicePort(Protocol):
    def list_voices(self) -> list[dict[str, str | None]]: ...
    def synthesize(self, text: str) -> bytes: ...


@dataclass(frozen=True)
class Personality:
    name: str
    language: str
    prompt_path: Path

    def prompt(self) -> str:
        return self.prompt_path.read_text(encoding="utf-8")


def validate_utterance(text: str, max_characters: int) -> str:
    clean = " ".join(text.split())
    if not clean:
        raise VoiceError("speech text cannot be empty")
    if len(clean) > max_characters:
        raise VoiceError(f"speech text exceeds the {max_characters}-character project limit")
    return clean

