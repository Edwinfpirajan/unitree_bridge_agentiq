from __future__ import annotations

from .domain import VelocityCommand
from .ports import RobotPort
from .safety import SafetyGate


class RobotApplication:
    def __init__(self, robot: RobotPort, safety: SafetyGate) -> None:
        self.robot = robot
        self.safety = safety

    def connect(self) -> None:
        self.safety.validate_startup()
        self.robot.connect()

    def move(self, command: VelocityCommand) -> None:
        self.safety.validate_motion(command, self.robot.read_state())
        self.robot.command_velocity(command)

    def shutdown(self) -> None:
        try:
            self.robot.stop()
        finally:
            self.robot.close()

