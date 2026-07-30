import unittest

from g1edu.adapters.unitree_audio import stream_pcm
from g1edu.voice import VoiceError


class FakeAudioClient:
    def __init__(self, result: int = 0) -> None:
        self.result = result
        self.chunks: list[bytes] = []
        self.stopped = False

    def PlayStream(self, app_name: str, stream_id: str, chunk: bytes):
        self.chunks.append(chunk)
        return self.result, None

    def PlayStop(self, app_name: str) -> None:
        self.stopped = True


class UnitreeAudioTests(unittest.TestCase):
    def test_pcm_is_chunked_and_stopped(self) -> None:
        client = FakeAudioClient()
        stream_pcm(client, b"12345678", chunk_size=4, delay_seconds=0)
        self.assertEqual(client.chunks, [b"1234", b"5678"])
        self.assertTrue(client.stopped)

    def test_service_error_stops_playback(self) -> None:
        client = FakeAudioClient(result=7)
        with self.assertRaises(VoiceError):
            stream_pcm(client, b"12", delay_seconds=0)
        self.assertTrue(client.stopped)


if __name__ == "__main__":
    unittest.main()
