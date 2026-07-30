from __future__ import annotations

from time import monotonic

from ..domain import RobotState, VelocityCommand


class MockRobot:
    def __init__(self) -> None:
        self._connected = False
        self.last_command = VelocityCommand()

    def connect(self) -> None:
        self._connected = True

    def read_state(self) -> RobotState:
        return RobotState(connected=self._connected, battery_percent=100.0, observed_at=monotonic())

    def command_velocity(self, command: VelocityCommand) -> None:
        self.last_command = command

    def stop(self) -> None:
        self.last_command = VelocityCommand()

    def close(self) -> None:
        self.stop()
        self._connected = False

