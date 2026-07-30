from __future__ import annotations

from ..domain import RobotState, VelocityCommand


class UnitreeRobot:
    """Physical adapter boundary. Implement only against the confirmed SDK/firmware."""

    def connect(self) -> None:
        raise NotImplementedError(
            "Physical control is intentionally disabled; complete docs/hardware-profile.md first"
        )

    def read_state(self) -> RobotState:
        raise NotImplementedError

    def command_velocity(self, command: VelocityCommand) -> None:
        raise NotImplementedError

    def stop(self) -> None:
        raise NotImplementedError

    def close(self) -> None:
        raise NotImplementedError

