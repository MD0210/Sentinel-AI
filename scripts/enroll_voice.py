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
SAMPLES_REQUIRED = 20
FRAME_SIZE = 1280

SAMPLE_SENTENCES = (
    "Sentinel is my personal AI assistant for helping me with my daily work.",
    "I want Sentinel to help me manage data engineering tasks safely and efficiently.",
    "Today I am testing my voice authentication to make sure it recognizes me correctly.",
    "My goal is to build a secure assistant that can work with my computer and development tools.",
    "I am speaking naturally so Sentinel can learn the characteristics of my voice.",
    "I use Sentinel to help me stay organized while working on technical projects.",
    "Please listen to my normal speaking voice and use it for authentication.",
    "I want my assistant to protect my computer and data from unauthorized access.",
    "Good security should require authentication before Sentinel accepts requests.",
    "I am testing different sentences so my voice profile can be more reliable.",
    "Sentinel should respond only after it confirms that I am the authorized user.",
    "I want the assistant to be useful while keeping sensitive information private.",
    "Today I am creating a stronger voice profile with multiple natural samples.",
    "My voice may sound slightly different depending on how I speak during the day.",
    "I will speak clearly and naturally without trying to change my normal voice.",
    "Sentinel will eventually help me with files, code, GitHub, and other tools.",
    "I want important actions to require confirmation before they are performed.",
    "A secure personal assistant should follow clear permissions and safety rules.",
    "I am completing the voice enrollment process one sample at a time.",
    "This final sample completes my Sentinel voice enrollment for today.",
)


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

    for number, sentence in enumerate(SAMPLE_SENTENCES, start=1):
        input(
            f"Press Enter, then speak the following sentence for "
            f"{SECONDS_PER_SAMPLE} seconds (sample {number}/{SAMPLES_REQUIRED}):\n"
            f'"{sentence}"\n'
        )
        audio = create_microphone_source(frames_per_buffer=FRAME_SIZE)
        try:
            samples.append(record_sample(audio, SECONDS_PER_SAMPLE))
        finally:
            audio.close()
        print("Sample captured.\n")

    profile = enrollment.enroll(samples)
    save_voice_profile(PROFILE_PATH, profile)
    print(f"Voice profile created: {PROFILE_PATH}")
    print(f"Enrollment complete using {SAMPLES_REQUIRED} samples. No raw audio was stored.")


if __name__ == "__main__":
    main()
