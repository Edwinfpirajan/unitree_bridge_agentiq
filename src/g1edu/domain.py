from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from time import monotonic


class RobotMode(str, Enum):
    MOCK = "mock"
    SIMULATION = "simulation"
    HARDWARE = "hardware"


@dataclass(frozen=True)
class VelocityCommand:
    x_mps: float = 0.0
    y_mps: float = 0.0
    yaw_rps: float = 0.0


@dataclass(frozen=True)
class RobotState:
    connected: bool
    standing: bool = False
    emergency_stop: bool = False
    battery_percent: float | None = None
    observed_at: float = 0.0

    @classmethod
    def disconnected(cls) -> "RobotState":
        return cls(connected=False, observed_at=monotonic())

