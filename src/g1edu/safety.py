from __future__ import annotations

from dataclasses import dataclass
from time import monotonic

from .config import AppConfig
from .domain import RobotMode, RobotState, VelocityCommand


class SafetyViolation(RuntimeError):
    pass


@dataclass(frozen=True)
class SafetyGate:
    config: AppConfig

    def validate_startup(self) -> None:
        if self.config.mode is RobotMode.HARDWARE:
            if not self.config.safety.hardware_enabled:
                raise SafetyViolation("hardware mode requires safety.hardware_enabled=true")
            if self.config.variant == "UNCONFIRMED":
                raise SafetyViolation("confirm the robot variant before enabling hardware")
            if self.config.network_interface in {"lo", "localhost"}:
                raise SafetyViolation("hardware mode cannot use the loopback interface")

    def validate_motion(self, command: VelocityCommand, state: RobotState) -> None:
        if not state.connected:
            raise SafetyViolation("robot state is disconnected")
        if state.emergency_stop:
            raise SafetyViolation("emergency stop is active")
        age_ms = (monotonic() - state.observed_at) * 1000
        if age_ms > self.config.safety.state_stale_after_ms:
            raise SafetyViolation("robot state is stale")
        if max(abs(command.x_mps), abs(command.y_mps)) > self.config.safety.max_linear_speed_mps:
            raise SafetyViolation("linear velocity exceeds configured limit")
        if abs(command.yaw_rps) > self.config.safety.max_angular_speed_rps:
            raise SafetyViolation("angular velocity exceeds configured limit")

