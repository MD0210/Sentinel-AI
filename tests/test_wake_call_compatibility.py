# Tests for transcript and microphone wake-call compatibility.

import unittest
from unittest.mock import patch

from voice.wake_call import OpenWakeWordDetector, WakeCall


class FakeModel:
    def __init__(self, scores):
        self.scores = iter(scores)

    def predict(self, audio):
        return {"hey_jarvis": next(self.scores)}


class FakeAudio:
    def __init__(self, frames):
        self.frames = iter(frames)
        self.closed = False

    def read(self, frame_size):
        return next(self.frames)

    def close(self):
        self.closed = True


class WakeCallCompatibilityTests(unittest.TestCase):
    def test_transcript_wake_call_is_preserved(self):
        wake_call = WakeCall()
        self.assertTrue(wake_call.matches("  Hey   Sentinel  "))
        self.assertFalse(wake_call.matches("hello sentinel"))

    @patch("numpy.frombuffer")
    def test_microphone_detector_still_waits_for_threshold(self, frombuffer):
        frombuffer.side_effect = lambda frame, dtype: frame
        detector = OpenWakeWordDetector(FakeModel([0.2, 0.6]))
        audio = FakeAudio([b"one", b"two"])

        self.assertTrue(detector.wait_for_wake(audio))
        self.assertTrue(audio.closed)
        self.assertEqual(frombuffer.call_count, 2)


if __name__ == "__main__":
    unittest.main()
