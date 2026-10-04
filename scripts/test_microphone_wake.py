"""Local microphone smoke test for Sentinel's openWakeWord adapter.

Run this on the Windows machine with the Sentinel voice dependencies installed.
It exercises real microphone capture but uses the available "hey_jarvis"
acoustic model; the four Sentinel transcript phrases remain unchanged.
"""

from voice.wake_call import create_microphone_source, create_openwakeword_detector


def main() -> None:
    print("Sentinel microphone wake-word smoke test")
    print("Audio format: 16 kHz, 16-bit PCM, mono")
    print("Acoustic test model: hey_jarvis")
    print("Say 'Hey Jarvis' to test detection, or press Ctrl+C to stop.")

    detector = create_openwakeword_detector("hey_jarvis", threshold=0.5)
    audio = create_microphone_source(frames_per_buffer=detector.FRAME_SIZE)

    try:
        if detector.wait_for_wake(audio):
            print("Wake word detected.")
    except KeyboardInterrupt:
        print("Microphone test stopped.")
        audio.close()


if __name__ == "__main__":
    main()
