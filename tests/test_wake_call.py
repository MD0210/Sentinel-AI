import unittest

from voice.wake_call import WakeCall


class WakeCallTests(unittest.TestCase):
    def setUp(self):
        self.wake_call = WakeCall()

    def test_default_phrase_matches_case_insensitively(self):
        self.assertTrue(self.wake_call.matches("Hey Sentinel"))

    def test_whitespace_is_normalized(self):
        self.assertTrue(self.wake_call.matches("  hey   sentinel  "))

    def test_unrelated_text_does_not_activate(self):
        self.assertFalse(self.wake_call.matches("hello sentinel"))

    def test_activate_uses_same_matching_rule(self):
        self.assertTrue(self.wake_call.activate("HEY SENTINEL"))


if __name__ == "__main__":
    unittest.main()
