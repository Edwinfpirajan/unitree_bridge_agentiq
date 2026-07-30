from __future__ import annotations

import argparse
from pathlib import Path

from g1edu.adapters.elevenlabs import ElevenLabsVoice
from g1edu.cli import _load_dotenv
from g1edu.config import load_config


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate PCM audio without contacting the robot.")
    parser.add_argument("text")
    parser.add_argument("output", type=Path)
    parser.add_argument("--config", default="config/robot.toml")
    args = parser.parse_args()

    _load_dotenv()
    config = load_config(args.config)
    if config.voice is None:
        parser.error("the [voice] configuration is missing")
    pcm = ElevenLabsVoice(config.voice).synthesize(args.text, output_format="pcm_16000")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(pcm)
    print(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
