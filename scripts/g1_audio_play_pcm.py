from __future__ import annotations

import argparse
from pathlib import Path
from time import sleep, time

from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.g1.audio.g1_audio_client import AudioClient


def main() -> int:
    parser = argparse.ArgumentParser(description="Play PCM16 mono 16 kHz through the G1.")
    parser.add_argument("interface")
    parser.add_argument("pcm", type=Path)
    parser.add_argument("--volume", type=int, default=40)
    parser.add_argument("--confirm-g1-audio", action="store_true")
    args = parser.parse_args()
    if not args.confirm_g1_audio:
        parser.error("--confirm-g1-audio is required")
    if not 0 <= args.volume <= 100:
        parser.error("--volume must be between 0 and 100")

    pcm = args.pcm.read_bytes()
    if not pcm:
        parser.error("PCM file is empty")

    ChannelFactoryInitialize(0, args.interface)
    client = AudioClient()
    client.SetTimeout(10.0)
    client.Init()
    if client.SetVolume(args.volume) != 0:
        raise RuntimeError("G1 rejected SetVolume")

    app_name = "migo"
    stream_id = str(int(time() * 1000))
    chunk_size = 96_000
    try:
        for offset in range(0, len(pcm), chunk_size):
            code, _ = client.PlayStream(
                app_name, stream_id, pcm[offset : offset + chunk_size]
            )
            if code != 0:
                raise RuntimeError(f"G1 rejected PlayStream with code {code}")
            # Match Unitree's official WAV example: let the service consume every
            # accepted chunk, including the final one, before calling PlayStop.
            sleep(1.0)
    finally:
        client.PlayStop(app_name)
    print("G1_AUDIO_PLAYBACK_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
