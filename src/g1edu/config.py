from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import tomllib

from .domain import RobotMode


@dataclass(frozen=True)
class SafetyConfig:
    hardware_enabled: bool
    require_operator_confirmation: bool
    max_linear_speed_mps: float
    max_angular_speed_rps: float
    command_timeout_ms: int
    state_stale_after_ms: int


@dataclass(frozen=True)
class VoiceConfig:
    provider: str
    model_id: str
    output_format: str
    language: str
    preferred_voice_name: str
    preferred_accent: str
    output_directory: str
    max_characters: int


@dataclass(frozen=True)
class AppConfig:
    name: str
    model: str
    variant: str
    mode: RobotMode
    network_interface: str
    dds_domain_id: int
    safety: SafetyConfig
    voice: VoiceConfig | None = None


def load_config(path: str | Path) -> AppConfig:
    with Path(path).open("rb") as handle:
        raw = tomllib.load(handle)
    robot, safety = raw["robot"], raw["safety"]
    voice = raw.get("voice")
    return AppConfig(
        name=robot["name"],
        model=robot["model"],
        variant=robot["variant"],
        mode=RobotMode(robot["mode"]),
        network_interface=robot["network_interface"],
        dds_domain_id=int(robot["dds_domain_id"]),
        safety=SafetyConfig(**safety),
        voice=VoiceConfig(**voice) if voice else None,
    )
