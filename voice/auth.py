"""Local speaker-verification providers.

The ECAPA-TDNN adapter uses SpeechBrain's pretrained VoxCeleb speaker encoder.
The model is downloaded by SpeechBrain on first use and remains local afterward.
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


class EcapaTdnnSpeakerModel:
    """SpeechBrain ECAPA-TDNN speaker embedding adapter.

    Input audio must be raw signed 16-bit PCM, mono, 16 kHz, matching Sentinel's
    existing microphone capture format. Model files are downloaded to the local
    SpeechBrain cache on first initialization.
    """

    SAMPLE_RATE = 16_000
    SAMPLE_WIDTH_BYTES = 2
    MIN_SAMPLES = 16_000

    def __init__(
        self,
        source: str = "speechbrain/spkrec-ecapa-voxceleb",
        savedir: str = "pretrained_models/spkrec-ecapa-voxceleb",
    ):
        from speechbrain.inference.speaker import EncoderClassifier

        self._classifier = EncoderClassifier.from_hparams(
            source=source,
            savedir=savedir,
            run_opts={"device": "cpu"},
        )

    def embed(self, audio: bytes) -> tuple[float, ...]:
        """Convert 16-bit mono PCM audio into an ECAPA speaker embedding."""
        if not audio or len(audio) % self.SAMPLE_WIDTH_BYTES:
            raise ValueError("audio must contain complete 16-bit PCM samples")

        sample_count = len(audio) // self.SAMPLE_WIDTH_BYTES
        if sample_count < self.MIN_SAMPLES:
            raise ValueError("speaker verification audio must contain at least 1 second")

        import numpy as np
        import torch

        samples = np.frombuffer(audio, dtype=np.int16).copy()
        waveform = torch.from_numpy(samples).float().div(32768.0).unsqueeze(0)

        with torch.no_grad():
            embedding = self._classifier.encode_batch(waveform)

        return tuple(float(value) for value in embedding.reshape(-1).cpu().tolist())
