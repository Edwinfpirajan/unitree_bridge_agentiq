import os
import unittest
from unittest.mock import patch

from g1edu.conversation import run_elevenlabs_conversation
from g1edu.voice import VoiceError


class ConversationTests(unittest.TestCase):
    @patch.dict(os.environ, {}, clear=True)
    def test_missing_api_key_is_rejected(self) -> None:
        with self.assertRaises(VoiceError):
            run_elevenlabs_conversation()

    @patch.dict(os.environ, {"ELEVENLABS_API_KEY": "test"}, clear=True)
    def test_missing_agent_id_is_rejected(self) -> None:
        with self.assertRaises(VoiceError):
            run_elevenlabs_conversation()


if __name__ == "__main__":
    unittest.main()
