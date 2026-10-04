"""Microphone-backed wake-call adapters using openWakeWord.

The audio source is intentionally kept separate from wake-word detection so the
detector remains easy to test without microphone hardware.
"""

from dataclasses import dataclass
from typing import Protocol


@dataclass
class WakeCall:
    """Transcript-based wake phrase detector retained for compatibility."""

    phrase: str = "hey sentinel"

    DEFAULT_PHRASES = ("hey sentinel", "hi sentinel", "hello sentinel", "sentinel")

    def matches(self, text: str) -> bool:
        """Return True when normalized text exactly matches an accepted wake phrase."""
        normalized = " ".join(text.casefold().strip().split())
        accepted_phrases = {
            self.phrase.casefold(),
            *(phrase.casefold() for phrase in self.DEFAULT_PHRASES),
        }
        return normalized in accepted_phrases

    def activate(self, text: str) -> bool:
        """Check a transcript and report whether Sentinel should activate."""
        return self.matches(text)


class AudioSource(Protocol):
    def read(self, frame_size: int) -> bytes:
        """Return one frame of 16-bit mono PCM audio."""
        ...

    def close(self) -> None:
        """Release the audio input resource."""
        ...


class PyAudioInputSource:
    """Windows microphone source using PyAudioWPatch."""

    SAMPLE_RATE = 16_000
    CHANNELS = 1
    SAMPLE_WIDTH_BYTES = 2

    def __init__(self, device_index: int | None = None, frames_per_buffer: int = 1280):
        import pyaudiowpatch as pyaudio

        self._pyaudio = pyaudio
        self._pa = pyaudio.PyAudio()
        self._stream = self._pa.open(
            format=pyaudio.paInt16,
            channels=self.CHANNELS,
            rate=self.SAMPLE_RATE,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=frames_per_buffer,
        )

    def read(self, frame_size: int) -> bytes:
        """Read one 16-bit mono PCM frame from the microphone."""
        return self._stream.read(frame_size, exception_on_overflow=False)

    def close(self) -> None:
        """Stop and release the microphone stream."""
        self._stream.stop_stream()
        self._stream.close()
        self._pa.terminate()


class OpenWakeWordDetector:
    """Detect a configured wake word from 16 kHz microphone PCM frames."""

    SAMPLE_RATE = 16_000
    FRAME_SIZE = 1280

    def __init__(self, model, wakeword: str = "hey_jarvis", threshold: float = 0.5):
        self.model = model
        self.wakeword = wakeword
        self.threshold = threshold

    def process(self, frame: bytes) -> bool:
        """Return True when the wake-word model crosses the configured threshold."""
        import numpy as np

        audio = np.frombuffer(frame, dtype=np.int16)
        predictions = self.model.predict(audio)
        score = predictions.get(self.wakeword, 0.0)
        return float(score) >= self.threshold

    def wait_for_wake(self, audio_source: AudioSource) -> bool:
        """Block until the wake word is detected, then release the audio source."""
        try:
            while True:
                if self.process(audio_source.read(self.FRAME_SIZE)):
                    return True
        finally:
            audio_source.close()


def create_openwakeword_detector(
    wakeword: str = "hey_jarvis", threshold: float = 0.5
) -> OpenWakeWordDetector:
    """Create a detector using the openWakeWord model package."""
    from openwakeword.model import Model

    model = Model(inference_framework="onnx")
    return OpenWakeWordDetector(model, wakeword=wakeword, threshold=threshold)


def create_microphone_source(
    device_index: int | None = None, frames_per_buffer: int = 1280
) -> PyAudioInputSource:
    """Create a 16 kHz, 16-bit mono Windows microphone source."""
    return PyAudioInputSource(
        device_index=device_index,
        frames_per_buffer=frames_per_buffer,
    )
