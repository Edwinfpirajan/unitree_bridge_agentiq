from __future__ import annotations

import queue
import struct
import subprocess
import threading
import time
from collections.abc import Callable
from pathlib import Path


class G1LiveAudioInterface:
    """Capture the Windows microphone and stream ElevenLabs PCM output to G1 PC2."""

    INPUT_FRAMES_PER_BUFFER = 1600  # 100 ms: lower turn-detection latency than the SDK default.
    OUTPUT_BATCH_BYTES = 32_000  # One second of PCM; reduces SDK2 RPC request pressure.
    OUTPUT_BATCH_MAX_WAIT = 0.12

    def __init__(
        self,
        *,
        host: str = "192.168.123.164",
        user: str = "unitree",
        interface: str = "eth0",
        volume: int = 100,
        identity_file: Path | None = None,
    ) -> None:
        try:
            import pyaudio
        except ImportError as error:
            raise ImportError("G1 live audio requires PyAudio") from error
        self.pyaudio = pyaudio
        self.host = host
        self.user = user
        self.interface = interface
        self.volume = volume
        self.identity_file = identity_file or Path.home() / ".ssh" / "migo_g1_ed25519"
        self._queue: queue.Queue[bytes | None] = queue.Queue()
        self._write_lock = threading.Lock()
        self._mute_lock = threading.Lock()
        self._mute_until = 0.0

    def start(self, input_callback: Callable[[bytes], None]) -> None:
        self.input_callback = input_callback
        remote = (
            "source /home/unitree/cyclonedds_ws/install/setup.bash"
            " && python3 /home/unitree/g1_audio_stream_stdin.py"
            f" {self.interface} --volume {self.volume}"
        )
        self.process = subprocess.Popen(
            [
                "ssh.exe",
                "-T",
                "-o",
                "BatchMode=yes",
                "-i",
                str(self.identity_file),
                f"{self.user}@{self.host}",
                "bash",
                "-lc",
                f'"{remote}"',
            ],
            stdin=subprocess.PIPE,
        )
        if self.process.stdin is None:
            raise RuntimeError("could not open the G1 audio transport")
        time.sleep(1.0)
        if self.process.poll() is not None:
            raise RuntimeError(f"G1 audio transport stopped with code {self.process.returncode}")

        self.should_stop = threading.Event()
        self.output_thread = threading.Thread(
            target=self._output_worker, name="g1-live-audio", daemon=True
        )
        self.output_thread.start()
        self.p = self.pyaudio.PyAudio()
        self.in_stream = self.p.open(
            format=self.pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            stream_callback=self._in_callback,
            frames_per_buffer=self.INPUT_FRAMES_PER_BUFFER,
            start=True,
        )

    def stop(self) -> None:
        if getattr(self, "in_stream", None) is not None:
            self.in_stream.stop_stream()
            self.in_stream.close()
        if getattr(self, "p", None) is not None:
            self.p.terminate()
        self.should_stop.set()
        self._queue.put(None)
        self.output_thread.join(timeout=3)
        if self.process.poll() is None:
            self._send(b"Q")
            if self.process.stdin:
                self.process.stdin.close()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.terminate()

    def output(self, audio: bytes) -> None:
        # Half-duplex echo guard. The PC microphone can hear the G1 speaker and
        # otherwise ElevenLabs treats Migo's own voice as an interruption.
        duration = len(audio) / 32_000  # PCM16 mono at 16 kHz.
        with self._mute_lock:
            now = time.monotonic()
            queued_audio_end = max(now, self._mute_until - 0.15)
            self._mute_until = queued_audio_end + duration + 0.15
        self._queue.put(audio)

    def interrupt(self) -> None:
        try:
            while True:
                self._queue.get_nowait()
        except queue.Empty:
            pass
        self._send(b"I")

    def _output_worker(self) -> None:
        while not self.should_stop.is_set():
            audio = self._queue.get()
            if audio is None:
                return
            batch = bytearray(audio)
            deadline = time.monotonic() + self.OUTPUT_BATCH_MAX_WAIT
            while len(batch) < self.OUTPUT_BATCH_BYTES:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    break
                try:
                    chunk = self._queue.get(timeout=remaining)
                except queue.Empty:
                    break
                if chunk is None:
                    break
                batch.extend(chunk)
            self._send(b"A" + struct.pack("!I", len(batch)) + batch)

    def _send(self, packet: bytes) -> None:
        with self._write_lock:
            if self.process.poll() is not None:
                raise RuntimeError(f"G1 audio transport stopped with code {self.process.returncode}")
            assert self.process.stdin is not None
            self.process.stdin.write(packet)
            self.process.stdin.flush()

    def _in_callback(self, in_data, frame_count, time_info, status):
        with self._mute_lock:
            muted = time.monotonic() < self._mute_until
        if not muted:
            self.input_callback(in_data)
        return (None, self.pyaudio.paContinue)
