from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path

from g1edu.cli import _load_dotenv


def set_env_value(path: Path, key: str, value: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    replacement = f"{key}={value}"
    for index, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[index] = replacement
            break
    else:
        lines.append(replacement)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    _load_dotenv()
    api_key = os.environ["ELEVENLABS_API_KEY"]
    voice_id = os.environ["ELEVENLABS_VOICE_ID"]
    personality = Path("personality/g1-personality.md").read_text(encoding="utf-8")
    body = {
        "name": "Migo G1",
        "conversation_config": {
            "agent": {
                "first_message": "Hola, soy Migo. ¿En qué puedo ayudarte?",
                "language": "es",
                "prompt": {"prompt": personality},
            },
            "tts": {
                "voice_id": voice_id,
                "model_id": "eleven_flash_v2_5",
            },
        },
        "platform_settings": {"auth": {"enable_auth": True}},
        "tags": ["migo", "unitree-g1"],
    }
    request = urllib.request.Request(
        "https://api.elevenlabs.io/v1/convai/agents/create",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "xi-api-key": api_key},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"ElevenLabs agent creation failed ({error.code}): {detail}") from error
    agent_id = result["agent_id"]
    set_env_value(Path(".env"), "ELEVENLABS_AGENT_ID", agent_id)
    print("MIGO_AGENT_CONFIGURED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
