import unittest

from g1edu.adapters.mock import MockRobot
from g1edu.application import RobotApplication
from g1edu.config import AppConfig, SafetyConfig
from g1edu.domain import RobotMode, VelocityCommand
from g1edu.safety import SafetyGate


class MockApplicationTests(unittest.TestCase):
    def test_mock_application_stops_on_shutdown(self) -> None:
        cfg = AppConfig(
            "test",
            "g1",
            "UNCONFIRMED",
            RobotMode.MOCK,
            "lo",
            1,
            SafetyConfig(False, True, 0.15, 0.25, 100, 250),
        )
        robot = MockRobot()
        app = RobotApplication(robot, SafetyGate(cfg))
        app.connect()
        app.move(VelocityCommand(x_mps=0.1))
        app.shutdown()
        self.assertEqual(robot.last_command, VelocityCommand())
        self.assertFalse(robot.read_state().connected)


if __name__ == "__main__":
    unittest.main()
