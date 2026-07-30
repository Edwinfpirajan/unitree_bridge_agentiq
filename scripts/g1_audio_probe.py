from __future__ import annotations

import argparse

from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.g1.audio.g1_audio_client import AudioClient


def main() -> int:
    parser = argparse.ArgumentParser(description="Read the G1 speaker volume without changing it.")
    parser.add_argument("interface", help="Linux network interface connected to the G1")
    args = parser.parse_args()

    ChannelFactoryInitialize(0, args.interface)
    client = AudioClient()
    client.SetTimeout(5.0)
    client.Init()
    result = client.GetVolume()
    print(f"GetVolume={result}")
    return 0 if result[0] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
