import json
import tempfile
import unittest
from pathlib import Path

from voice.enrollment import VoiceProfile
from voice.profile import load_voice_profile, save_voice_profile


class VoiceProfileTests(unittest.TestCase):
    def test_save_and_load_profile(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "voice_profile.json"
            profile = VoiceProfile((0.1, 0.2, 0.3))
            save_voice_profile(path, profile)
            self.assertEqual(load_voice_profile(path), profile)
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(set(data), {"version", "embedding"})
            self.assertNotIn("audio", data)

    def test_missing_profile_is_rejected(self):
        with self.assertRaises(FileNotFoundError):
            load_voice_profile("does-not-exist.json")

    def test_invalid_profile_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "voice_profile.json"
            path.write_text(json.dumps({"version": 1, "embedding": []}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_voice_profile(path)


if __name__ == "__main__":
    unittest.main()
