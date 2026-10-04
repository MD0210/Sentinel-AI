"""Record microphone samples and create a local Sentinel voice profile.

This script stores only the derived ECAPA speaker embedding. Raw microphone
recordings are held in memory and are not written to disk.
"""

from pathlib import Path

from voice.auth import EcapaTdnnSpeakerModel
from voice.enrollment import VoiceEnrollment
from voice.profile import save_voice_profile
from voice.wake_call import create_microphone_source

PROFILE_PATH = Path("config/voice_profile.json")
SAMPLE_RATE = 16_000
SECONDS_PER_SAMPLE = 5
SAMPLES_REQUIRED = 5
FRAME_SIZE = 1280


def record_sample(audio_source, seconds: int) -> bytes:
    """Record one fixed-length microphone sample in memory."""
    chunks = []
    frames = SAMPLE_RATE * seconds // FRAME_SIZE
    remainder = SAMPLE_RATE * seconds % FRAME_SIZE
    for _ in range(frames):
        chunks.append(audio_source.read(FRAME_SIZE))
    if remainder:
        chunks.append(audio_source.read(remainder))
    return b"".join(chunks)


def main() -> None:
    print("Sentinel AI voice enrollment")
    print(f"You will record {SAMPLES_REQUIRED} samples of {SECONDS_PER_SAMPLE} seconds each.")
    print("Speak naturally and use the same voice you will use with Sentinel.")
    print("Raw recordings are kept only in memory and are not saved.\n")

    model = EcapaTdnnSpeakerModel()
    enrollment = VoiceEnrollment(model)
    samples = []

    for number in range(1, SAMPLES_REQUIRED + 1):
        input(f"Press Enter, then speak for {SECONDS_PER_SAMPLE} seconds (sample {number}/{SAMPLES_REQUIRED})...")
        audio = create_microphone_source(frames_per_buffer=FRAME_SIZE)
        try:
            samples.append(record_sample(audio, SECONDS_PER_SAMPLE))
        finally:
            audio.close()
        print("Sample captured.\n")

    profile = enrollment.enroll(samples)
    save_voice_profile(PROFILE_PATH, profile)
    print(f"Voice profile created: {PROFILE_PATH}")
    print("Enrollment complete. No raw audio was stored.")


if __name__ == "__main__":
    main()
