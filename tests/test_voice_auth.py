import unittest

from voice.auth import SpeakerEnrollment, SpeakerVerifier, VoiceAuthenticator, cosine_similarity


class FakeEmbeddingModel:
    def embed(self, audio):
        return {"owner": (1.0, 0.0), "other": (0.0, 1.0), "same": (1.0, 0.0)}[audio.decode()]


class VoiceAuthenticatorTests(unittest.TestCase):
    def test_cosine_similarity(self):
        self.assertAlmostEqual(cosine_similarity((1, 0), (1, 0)), 1.0)
        self.assertAlmostEqual(cosine_similarity((1, 0), (0, 1)), 0.0)

    def test_enrollment_creates_embedding(self):
        enrolled = SpeakerEnrollment(FakeEmbeddingModel()).enroll(b"owner")
        self.assertEqual(enrolled, (1.0, 0.0))

    def test_verifier_accepts_matching_speaker(self):
        verifier = SpeakerVerifier(FakeEmbeddingModel(), (1.0, 0.0), threshold=0.75)
        self.assertTrue(verifier.verify(b"same"))

    def test_verifier_rejects_different_speaker(self):
        verifier = SpeakerVerifier(FakeEmbeddingModel(), (1.0, 0.0), threshold=0.75)
        self.assertFalse(verifier.verify(b"other"))

    def test_empty_enrollment_audio_rejected(self):
        with self.assertRaises(ValueError):
            SpeakerEnrollment(FakeEmbeddingModel()).enroll(b"")

    def test_existing_provider_contract_remains(self):
        verifier = SpeakerVerifier(FakeEmbeddingModel(), (1.0, 0.0))
        self.assertTrue(VoiceAuthenticator(verifier).authenticate(b"same"))


if __name__ == "__main__":
    unittest.main()
