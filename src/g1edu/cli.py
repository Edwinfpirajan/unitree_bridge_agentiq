from __future__ import annotations

import argparse
import json
import os
import socket
from datetime import datetime, timezone
from pathlib import Path

from .adapters.mock import MockRobot
from .adapters.unitree import UnitreeRobot
from .application import RobotApplication
from .config import load_config
from .domain import RobotMode
from .safety import SafetyGate
from .adapters.elevenlabs import ElevenLabsVoice
from .adapters.unitree_audio import UnitreeAudioSpeaker
from .voice import VoiceError
from .conversation import run_elevenlabs_conversation


def _load_dotenv(path: Path = Path(".env")) -> None:
    if not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("\"'"))


def _app(config_path: str) -> RobotApplication:
    config = load_config(config_path)
    robot = MockRobot() if config.mode is RobotMode.MOCK else UnitreeRobot()
    return RobotApplication(robot, SafetyGate(config))


def main() -> int:
    parser = argparse.ArgumentParser(prog="g1ctl")
    parser.add_argument("--config", default="config/robot.toml")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    sub.add_parser("doctor")
    voices = sub.add_parser("voices")
    voices.add_argument("--search")
    sub.add_parser("voice-info")
    sub.add_parser("converse")
    speak = sub.add_parser("speak")
    speak.add_argument("text")
    robot_speak = sub.add_parser("robot-speak")
    robot_speak.add_argument("text")
    robot_speak.add_argument("--interface", required=True)
    robot_speak.add_argument("--volume", type=int, default=60)
    robot_speak.add_argument("--confirm-g1-audio", action="store_true")
    args = parser.parse_args()

    _load_dotenv()
    config = load_config(args.config)
    if args.command == "doctor":
        report = {
            "config_exists": Path(args.config).is_file(),
            "hostname": socket.gethostname(),
            "mode": config.mode.value,
            "variant_confirmed": config.variant != "UNCONFIRMED",
            "hardware_enabled": config.safety.hardware_enabled,
            "safe_to_run_mock": config.mode is RobotMode.MOCK,
        }
        print(json.dumps(report, indent=2))
        return 0 if report["config_exists"] else 1

    if args.command == "converse":
        try:
            conversation_id = run_elevenlabs_conversation()
            print(f"conversation_id={conversation_id}")
            return 0
        except VoiceError as error:
            parser.exit(2, f"conversation error: {error}\n")

    if args.command in {"voices", "voice-info", "speak", "robot-speak"}:
        if config.voice is None:
            parser.error("the [voice] configuration is missing")
        try:
            voice = ElevenLabsVoice(config.voice)
            if args.command == "voices":
                available = voice.list_voices()
                if args.search:
                    needle = args.search.casefold()
                    available = [
                        item
                        for item in available
                        if needle
                        in " ".join(str(value or "") for value in item.values()).casefold()
                    ]
                print(json.dumps(available, ensure_ascii=False, indent=2))
                return 0
            if args.command == "voice-info":
                print(json.dumps(voice.get_voice(), ensure_ascii=False, indent=2))
                return 0
            if args.command == "robot-speak":
                if not args.confirm_g1_audio:
                    parser.error("robot-speak requires --confirm-g1-audio")
                pcm = voice.synthesize(args.text, output_format="pcm_16000")
                speaker = UnitreeAudioSpeaker(args.interface, args.volume)
                speaker.play_pcm16_mono_16khz(pcm)
                print("G1 audio playback completed")
                return 0
            audio = voice.synthesize(args.text)
            output_dir = Path(config.voice.output_directory)
            output_dir.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            output = output_dir / f"speech-{stamp}.mp3"
            output.write_bytes(audio)
            print(output.resolve())
            return 0
        except VoiceError as error:
            parser.exit(2, f"voice error: {error}\n")

    app = _app(args.config)
    try:
        app.connect()
        print(json.dumps(app.robot.read_state().__dict__, indent=2))
        return 0
    finally:
        app.shutdown()


if __name__ == "__main__":
    raise SystemExit(main())
