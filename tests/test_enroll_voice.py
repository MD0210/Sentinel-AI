import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.enroll_voice import record_sample, save_profile


class FakeAudioSource:
    def __init__(self, frame=b"abcd"):
        self.frame = frame
        self.calls = []

    def read(self, frame_size):
        self.calls.append(frame_size)
        return self.frame

    def close(self):
        pass


class EnrollmentScriptTests(unittest.TestCase):
    def test_record_sample_reads_expected_frames(self):
        source = FakeAudioSource()
        with patch("scripts.enroll_voice.SAMPLE_RATE", 8), patch("scripts.enroll_voice.FRAME_SIZE", 4):
            audio = record_sample(source, 1)
        self.assertEqual(audio, b"abcd" * 2)
        self.assertEqual(source.calls, [4, 4])

    def test_save_profile_writes_only_embedding(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "voice_profile.json"
            save_profile(path, (0.5, 0.5))
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data, {"embedding": [0.5, 0.5]})


if __name__ == "__main__":
    unittest.main()
