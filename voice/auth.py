"""Local speaker-verification provider interface and embedding comparison.

The concrete model backend is intentionally isolated behind SpeakerEmbeddingModel.
This milestone provides the security-safe comparison/enrollment logic without
shipping a biometric model or storing raw audio.
"""

from dataclasses import dataclass
from math import sqrt
from typing import Protocol


class SpeakerEmbeddingModel(Protocol):
    def embed(self, audio: bytes): ...


def cosine_similarity(left, right) -> float:
    """Return cosine similarity for two numeric embeddings."""
    if len(left) != len(right) or not left:
        raise ValueError("embeddings must be non-empty and the same length")

    dot = sum(a * b for a, b in zip(left, right))
    left_norm = sqrt(sum(a * a for a in left))
    right_norm = sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        raise ValueError("embeddings must have non-zero magnitude")
    return dot / (left_norm * right_norm)


@dataclass(frozen=True)
class SpeakerVerifier:
    """Compare live speaker embeddings with one enrolled embedding."""

    model: SpeakerEmbeddingModel
    enrolled_embedding: tuple[float, ...]
    threshold: float = 0.75

    def verify(self, audio: bytes) -> bool:
        embedding = tuple(float(value) for value in self.model.embed(audio))
        return cosine_similarity(embedding, self.enrolled_embedding) >= self.threshold


class SpeakerEnrollment:
    """Create an enrolled embedding from a trusted enrollment recording."""

    def __init__(self, model: SpeakerEmbeddingModel):
        self.model = model

    def enroll(self, audio: bytes) -> tuple[float, ...]:
        if not audio:
            raise ValueError("enrollment audio must not be empty")
        return tuple(float(value) for value in self.model.embed(audio))
