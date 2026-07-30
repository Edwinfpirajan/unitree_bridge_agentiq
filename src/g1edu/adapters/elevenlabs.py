from __future__ import annotations

import json
import os
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from ..config import VoiceConfig
from ..voice import VoiceError, validate_utterance


class ElevenLabsVoice:
    BASE_URL = "https://api.elevenlabs.io"

    def __init__(
        self,
        config: VoiceConfig,
        api_key: str | None = None,
        voice_id: str | None = None,
    ) -> None:
        self.config = config
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        self.voice_id = voice_id or os.getenv("ELEVENLABS_VOICE_ID")
        if not self.api_key:
            raise VoiceError("ELEVENLABS_API_KEY is not configured")

    def _request(self, request: Request) -> bytes:
        try:
            with urlopen(request, timeout=30) as response:
                return response.read()
        except HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")[:500]
            raise VoiceError(f"ElevenLabs returned HTTP {error.code}: {detail}") from error
        except URLError as error:
            raise VoiceError(f"could not reach ElevenLabs: {error.reason}") from error

    def list_voices(self) -> list[dict[str, str | None]]:
        request = Request(
            f"{self.BASE_URL}/v2/voices?page_size=100&include_total_count=false",
            headers={"xi-api-key": self.api_key, "Accept": "application/json"},
        )
        payload: dict[str, Any] = json.loads(self._request(request))
        return [
            {
                "voice_id": voice.get("voice_id"),
                "name": voice.get("name"),
                "category": voice.get("category"),
                "description": voice.get("description"),
            }
            for voice in payload.get("voices", [])
        ]

    def get_voice(self) -> dict[str, Any]:
        if not self.voice_id:
            raise VoiceError("ELEVENLABS_VOICE_ID is not configured")
        request = Request(
            f"{self.BASE_URL}/v1/voices/{quote(self.voice_id, safe='')}",
            headers={"xi-api-key": self.api_key, "Accept": "application/json"},
        )
        voice: dict[str, Any] = json.loads(self._request(request))
        return {
            "name": voice.get("name"),
            "category": voice.get("category"),
            "description": voice.get("description"),
            "labels": voice.get("labels", {}),
            "verified_languages": voice.get("verified_languages", []),
        }

    def synthesize(self, text: str, output_format: str | None = None) -> bytes:
        if not self.voice_id:
            raise VoiceError("ELEVENLABS_VOICE_ID is not configured")
        clean = validate_utterance(text, self.config.max_characters)
        query = urlencode({"output_format": output_format or self.config.output_format})
        url = f"{self.BASE_URL}/v1/text-to-speech/{quote(self.voice_id, safe='')}?{query}"
        body = json.dumps(
            {
                "text": clean,
                "model_id": self.config.model_id,
            }
        ).encode("utf-8")
        request = Request(
            url,
            data=body,
            method="POST",
            headers={
                "xi-api-key": self.api_key,
                "Content-Type": "application/json",
                "Accept": "audio/mpeg",
            },
        )
        return self._request(request)
