"""Short-lived microphone recording helpers for Sentinel authentication."""

from voice.wake_call import AudioSource

SAMPLE_RATE = 16_000
FRAME_SIZE = 1_280


def record_audio(audio_source: AudioSource, seconds: int = 5) -> bytes:
    """Capture a fixed-length 16 kHz PCM sample in memory only."""
    if seconds < 1:
        raise ValueError("recording duration must be at least one second")
    total_bytes = SAMPLE_RATE * seconds * 2
    frames = (SAMPLE_RATE * seconds + FRAME_SIZE - 1) // FRAME_SIZE
    audio = b"".join(audio_source.read(FRAME_SIZE) for _ in range(frames))
    return audio[:total_bytes]
