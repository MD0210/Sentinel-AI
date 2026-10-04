import unittest
from pathlib import Path

from voice.auth import SpeakerEnrollment, SpeakerVerifier, VoiceAuthenticator, cosine_similarity
from voice.enrollment import VoiceEnrollment, average_embeddings


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


class VoiceEnrollmentTests(unittest.TestCase):
    def test_average_embeddings_normalizes_mean(self):
        profile = average_embeddings(((1.0, 0.0), (1.0, 0.0)))
        self.assertEqual(profile.embedding, (1.0, 0.0))

    def test_enrollment_uses_all_samples(self):
        profile = VoiceEnrollment(FakeEmbeddingModel()).enroll((b"owner", b"same"))
        self.assertAlmostEqual(profile.embedding[0], 1.0)
        self.assertAlmostEqual(profile.embedding[1], 0.0)

    def test_empty_samples_rejected(self):
        with self.assertRaises(ValueError):
            VoiceEnrollment(FakeEmbeddingModel()).enroll(())

    def test_mismatched_embeddings_rejected(self):
        with self.assertRaises(ValueError):
            average_embeddings(((1.0, 0.0), (1.0,)))


if __name__ == "__main__":
    unittest.main()


class EcapaAdapterTests(unittest.TestCase):
    def test_ecapa_adapter_rejects_empty_audio_without_loading_model(self):
        # Constructor/model loading is intentionally not exercised in unit tests.
        from voice.auth import EcapaTdnnSpeakerModel
        with self.assertRaises(ValueError):
            EcapaTdnnSpeakerModel.__new__(EcapaTdnnSpeakerModel).embed(b"")




class LocalStrategyConfigurationTests(unittest.TestCase):
    def test_ecapa_source_uses_windows_safe_copy_strategy(self):
        source = Path("voice/auth.py").read_text(encoding="utf-8")
        self.assertIn("LocalStrategy.COPY", source)

