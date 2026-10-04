import unittest

from voice.wake_call import WakeCall


class WakeCallTests(unittest.TestCase):
    def setUp(self):
        self.wake_call = WakeCall()

    def test_default_phrase_matches_case_insensitively(self):
        self.assertTrue(self.wake_call.matches("Hey Sentinel"))

    def test_all_supported_phrases_match(self):
        for phrase in ("Hey Sentinel", "Hi Sentinel", "Hello Sentinel", "Sentinel"):
            with self.subTest(phrase=phrase):
                self.assertTrue(self.wake_call.matches(phrase))

    def test_whitespace_is_normalized(self):
        self.assertTrue(self.wake_call.matches("  hello   sentinel  "))

    def test_unrelated_text_does_not_activate(self):
        self.assertFalse(self.wake_call.matches("hello assistant"))

    def test_partial_phrase_does_not_activate(self):
        self.assertFalse(self.wake_call.matches("please say hello sentinel"))

    def test_activate_uses_same_matching_rule(self):
        self.assertTrue(self.wake_call.activate("SENTINEL"))


if __name__ == "__main__":
    unittest.main()
