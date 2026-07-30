import unittest

from g1edu.config import VoiceConfig
from g1edu.adapters.elevenlabs import ElevenLabsVoice
from g1edu.voice import VoiceError, validate_utterance


class VoiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = VoiceConfig(
            "elevenlabs",
            "eleven_multilingual_v2",
            "mp3_44100_128",
            "es",
            "David Martin - Confident and Balanced",
            "Latin American",
            "audio-output",
            20,
        )

    def test_missing_key_is_rejected(self) -> None:
        with self.assertRaises(VoiceError):
            ElevenLabsVoice(self.config, api_key="")

    def test_empty_text_is_rejected(self) -> None:
        with self.assertRaises(VoiceError):
            validate_utterance("  ", 20)

    def test_text_is_normalized(self) -> None:
        self.assertEqual(validate_utterance("hola   mundo", 20), "hola mundo")

    def test_project_character_limit_is_enforced(self) -> None:
        with self.assertRaises(VoiceError):
            validate_utterance("x" * 21, 20)


if __name__ == "__main__":
    unittest.main()
