from dataclasses import replace
from time import monotonic
import unittest

from g1edu.config import AppConfig, SafetyConfig
from g1edu.domain import RobotMode, RobotState, VelocityCommand
from g1edu.safety import SafetyGate, SafetyViolation


def config(mode: RobotMode = RobotMode.MOCK) -> AppConfig:
    return AppConfig(
        name="test",
        model="g1",
        variant="UNCONFIRMED",
        mode=mode,
        network_interface="lo",
        dds_domain_id=1,
        safety=SafetyConfig(False, True, 0.15, 0.25, 100, 250),
    )


class SafetyTests(unittest.TestCase):
    def test_mock_startup_is_allowed(self) -> None:
        SafetyGate(config()).validate_startup()

    def test_hardware_is_blocked_by_default(self) -> None:
        with self.assertRaises(SafetyViolation):
            SafetyGate(config(RobotMode.HARDWARE)).validate_startup()

    def test_velocity_limit_is_enforced(self) -> None:
        state = RobotState(connected=True, observed_at=monotonic())
        with self.assertRaises(SafetyViolation):
            SafetyGate(config()).validate_motion(VelocityCommand(x_mps=0.2), state)

    def test_confirming_variant_alone_does_not_enable_hardware(self) -> None:
        confirmed = replace(config(RobotMode.HARDWARE), variant="29dof")
        with self.assertRaises(SafetyViolation):
            SafetyGate(confirmed).validate_startup()


if __name__ == "__main__":
    unittest.main()
