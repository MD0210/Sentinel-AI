import unittest

from voice.auth import VoiceAuthenticator


class FakeProvider:
    def __init__(self, result):
        self.result = result

    def verify(self, audio):
        return self.result


class VoiceAuthenticatorTests(unittest.TestCase):
    def test_provider_success_authenticates(self):
        self.assertTrue(VoiceAuthenticator(FakeProvider(True)).authenticate(b"audio"))

    def test_provider_failure_rejects(self):
        self.assertFalse(VoiceAuthenticator(FakeProvider(False)).authenticate(b"audio"))


if __name__ == "__main__":
    unittest.main()
