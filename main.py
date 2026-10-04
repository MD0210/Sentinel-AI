"""Sentinel AI command-line entry point with wake-call and voice authentication."""

from agent.controller import SentinelAgent
from voice.auth import EcapaTdnnSpeakerModel, SpeakerVerifier
from voice.profile import load_voice_profile
from voice.recording import record_audio
from voice.wake_call import create_microphone_source

PROFILE_PATH = "config/voice_profile.json"


def authenticate_by_voice(sentinel: SentinelAgent) -> bool:
    """Capture a short live sample and verify it against the enrolled profile."""
    profile = load_voice_profile(PROFILE_PATH)
    model = EcapaTdnnSpeakerModel()
    verifier = SpeakerVerifier(model, profile.embedding)
    audio_source = create_microphone_source(frames_per_buffer=1280)
    try:
        print("Speak naturally for 5 seconds to verify your voice.")
        audio = record_audio(audio_source, seconds=5)
    finally:
        audio_source.close()
    verified = verifier.verify(audio)
    if verified:
        sentinel.security.record_success()
    else:
        sentinel.security.record_failure()
    return verified


def main() -> None:
    sentinel = SentinelAgent()
    print("Sentinel AI starting...")
    print("Say the wake phrase to activate Sentinel.")
    while True:
        wake_text = input("Wake phrase: ")
        if wake_text.strip().lower() in {"exit", "quit"}:
            return
        if sentinel.check_wake_call(wake_text):
            break
        print("Wake phrase not recognized.")

    print("Wake phrase recognized.")
    print("Voice authentication required.")
    try:
        voice_verified = authenticate_by_voice(sentinel)
    except (FileNotFoundError, ValueError, ImportError, OSError) as exc:
        print(f"Voice authentication unavailable: {exc}")
        voice_verified = False

    if not voice_verified:
        print("Voice authentication failed or is unavailable.")
        print("Use the secure Q&A fallback to authenticate.")
        if not sentinel.authenticate_fallback_from_environment():
            print("Authentication failed. Sentinel will not accept requests.")
            return

    print("Sentinel authenticated.")
    while True:
        request = input("You: ")
        if request.strip().lower() in {"exit", "quit"}:
            break
        print(f"Sentinel: {sentinel.handle_request(request)}")


if __name__ == "__main__":
    main()
