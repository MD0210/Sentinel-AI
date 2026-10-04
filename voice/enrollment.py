"""Secure local voice-enrollment helpers.

Enrollment stores only a derived speaker embedding, never raw recordings.
Biometric profile persistence is deliberately kept separate from source code.
"""

from dataclasses import dataclass
from math import sqrt
from typing import Iterable


@dataclass(frozen=True)
class VoiceProfile:
    """Normalized speaker embedding used for local verification."""
    embedding: tuple[float, ...]


def average_embeddings(embeddings: Iterable[Iterable[float]]) -> VoiceProfile:
    """Average multiple embeddings and normalize the resulting profile."""
    vectors = [tuple(float(value) for value in embedding) for embedding in embeddings]
    if not vectors:
        raise ValueError("at least one embedding is required")
    size = len(vectors[0])
    if size == 0 or any(len(vector) != size for vector in vectors):
        raise ValueError("embeddings must be non-empty and the same length")
    averaged = tuple(sum(vector[i] for vector in vectors) / len(vectors) for i in range(size))
    norm = sqrt(sum(value * value for value in averaged))
    if norm == 0:
        raise ValueError("the averaged embedding must have non-zero magnitude")
    return VoiceProfile(tuple(value / norm for value in averaged))


class VoiceEnrollment:
    """Build an enrolled profile from multiple trusted audio samples."""
    def __init__(self, model):
        self.model = model

    def enroll(self, audio_samples: Iterable[bytes]) -> VoiceProfile:
        samples = list(audio_samples)
        if not samples or any(not sample for sample in samples):
            raise ValueError("enrollment audio samples must not be empty")
        embeddings = [self.model.embed(sample) for sample in samples]
        return average_embeddings(embeddings)
