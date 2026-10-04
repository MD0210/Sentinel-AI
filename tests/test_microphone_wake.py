"""Tests for the microphone wake-word adapter."""

import unittest
from unittest.mock import patch

from voice.wake_call import OpenWakeWordDetector


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


class MicrophoneWakeWordTests(unittest.TestCase):
    @patch("numpy.frombuffer")
    def test_detector_waits_until_threshold(self, frombuffer):
        frombuffer.side_effect = lambda frame, dtype: frame
        detector = OpenWakeWordDetector(FakeModel([0.2, 0.6]))
        audio = FakeAudio([b"one", b"two"])

        self.assertTrue(detector.wait_for_wake(audio))
        self.assertTrue(audio.closed)
        self.assertEqual(frombuffer.call_count, 2)

    @patch("numpy.frombuffer")
    def test_detector_rejects_below_threshold(self, frombuffer):
        frombuffer.return_value = b"audio"
        detector = OpenWakeWordDetector(FakeModel([0.4]))
        self.assertFalse(detector.process(b"audio"))


if __name__ == "__main__":
    unittest.main()
