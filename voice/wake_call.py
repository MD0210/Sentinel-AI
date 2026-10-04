"""Microphone-backed wake-call adapter using openWakeWord.

The adapter keeps audio capture outside the agent and reports only wake-word
activation. It is optional so the existing transcript implementation remains
available for tests and environments without audio dependencies.
"""

from typing import Protocol


class AudioSource(Protocol):
    def read(self, frame_size: int) -> bytes:
        """Return one frame of 16-bit mono PCM audio."""
        ...

    def close(self) -> None:
        """Release the audio input resource."""
        ...


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

    model = Model()
    return OpenWakeWordDetector(model, wakeword=wakeword, threshold=threshold)
