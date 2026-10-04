import unittest

from voice.recording import record_audio


class FakeAudioSource:
    def __init__(self):
        self.calls = []

    def read(self, frame_size):
        self.calls.append(frame_size)
        return b"x" * (frame_size * 2)

    def close(self):
        pass


class RecordingTests(unittest.TestCase):
    def test_records_expected_pcm_bytes(self):
        source = FakeAudioSource()
        audio = record_audio(source, seconds=1)
        self.assertEqual(len(audio), 16_000 * 2)
        self.assertEqual(source.calls[-1], 1_280)


if __name__ == "__main__":
    unittest.main()
