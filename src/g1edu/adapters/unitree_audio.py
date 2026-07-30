from __future__ import annotations

from time import sleep, time
from typing import Any

from ..voice import VoiceError


def stream_pcm(
    client: Any,
    pcm: bytes,
    app_name: str = "nexo",
    chunk_size: int = 96_000,
    delay_seconds: float = 1.0,
) -> None:
    if not pcm:
        raise VoiceError("cannot stream empty PCM audio")
    stream_id = str(int(time() * 1000))
    for offset in range(0, len(pcm), chunk_size):
        chunk = pcm[offset : offset + chunk_size]
        code, _ = client.PlayStream(app_name, stream_id, chunk)
        if code != 0:
            client.PlayStop(app_name)
            raise VoiceError(f"Unitree voice service rejected an audio chunk with code {code}")
        # Unitree's official WAV example waits after every accepted chunk,
        # including the last one, before stopping the stream.
        sleep(delay_seconds)
    client.PlayStop(app_name)


class UnitreeAudioSpeaker:
    """Official G1 SDK2 `voice` service adapter; audio only, no motor APIs."""

    def __init__(self, network_interface: str, volume: int = 60) -> None:
        if not network_interface or network_interface in {"lo", "localhost"}:
            raise VoiceError("a physical G1 network interface is required")
        if not 0 <= volume <= 100:
            raise VoiceError("volume must be between 0 and 100")
        try:
            from unitree_sdk2py.core.channel import ChannelFactoryInitialize
            from unitree_sdk2py.g1.audio.g1_audio_client import AudioClient
        except ImportError as error:
            raise VoiceError(
                "unitree_sdk2py is missing; install the official SDK2 Python package on Linux/PC2"
            ) from error

        ChannelFactoryInitialize(0, network_interface)
        self.client = AudioClient()
        self.client.SetTimeout(10.0)
        self.client.Init()
        code = self.client.SetVolume(volume)
        if code != 0:
            raise VoiceError(f"could not set G1 audio volume; service code {code}")

    def play_pcm16_mono_16khz(self, pcm: bytes) -> None:
        stream_pcm(self.client, pcm)
