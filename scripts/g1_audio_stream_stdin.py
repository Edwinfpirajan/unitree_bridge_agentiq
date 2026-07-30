from __future__ import annotations

import argparse
import struct
import sys
import traceback
from time import time

from unitree_sdk2py.core.channel import ChannelFactoryInitialize
from unitree_sdk2py.g1.audio.g1_audio_client import AudioClient


def read_exact(size: int) -> bytes:
    data = bytearray()
    while len(data) < size:
        chunk = sys.stdin.buffer.read(size - len(data))
        if not chunk:
            raise EOFError
        data.extend(chunk)
    return bytes(data)


def main() -> int:
    parser = argparse.ArgumentParser(description="Stream framed PCM16/16k/mono stdin to G1.")
    parser.add_argument("interface")
    parser.add_argument("--volume", type=int, default=100)
    args = parser.parse_args()
    if not 0 <= args.volume <= 100:
        parser.error("--volume must be between 0 and 100")

    ChannelFactoryInitialize(0, args.interface)
    client = AudioClient()
    client.SetTimeout(10.0)
    client.Init()
    if client.SetVolume(args.volume) != 0:
        raise RuntimeError("G1 rejected SetVolume")

    app_name = "migo-live"
    stream_id = str(int(time() * 1000))
    consecutive_timeouts = 0
    print("G1_LIVE_AUDIO_READY", file=sys.stderr, flush=True)
    try:
        while True:
            command = read_exact(1)
            if command == b"A":
                size = struct.unpack("!I", read_exact(4))[0]
                audio = read_exact(size)
                code, _ = client.PlayStream(app_name, stream_id, audio)
                if code == 3104:
                    consecutive_timeouts += 1
                    with open("/home/unitree/migo-live-audio.log", "a", encoding="utf-8") as log:
                        print(
                            f"recoverable PlayStream timeout ({consecutive_timeouts})",
                            file=log,
                        )
                    if consecutive_timeouts >= 3:
                        client.PlayStop(app_name)
                        stream_id = str(int(time() * 1000))
                        consecutive_timeouts = 0
                elif code != 0:
                    raise RuntimeError(f"G1 rejected PlayStream with code {code}")
                else:
                    consecutive_timeouts = 0
            elif command == b"I":
                client.PlayStop(app_name)
                stream_id = str(int(time() * 1000))
            elif command == b"Q":
                break
            else:
                raise RuntimeError(f"unknown command {command!r}")
    except EOFError:
        pass
    except Exception:
        with open("/home/unitree/migo-live-audio.log", "a", encoding="utf-8") as log:
            traceback.print_exc(file=log)
        raise
    finally:
        client.PlayStop(app_name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
