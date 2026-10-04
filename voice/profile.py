"""Local persistence for Sentinel's derived speaker profile.

Only the speaker embedding is persisted. Raw audio is never written.
"""

from __future__ import annotations

import json
from pathlib import Path

from voice.enrollment import VoiceProfile


def save_voice_profile(path: str | Path, profile: VoiceProfile) -> None:
    """Atomically save a derived speaker embedding as local JSON."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = {"version": 1, "embedding": list(profile.embedding)}
    temporary = target.with_suffix(target.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(target)


def load_voice_profile(path: str | Path) -> VoiceProfile:
    """Load and validate a local speaker profile."""
    target = Path(path)
    if not target.is_file():
        raise FileNotFoundError(f"voice profile not found: {target}")
    payload = json.loads(target.read_text(encoding="utf-8"))
    if payload.get("version") != 1:
        raise ValueError("unsupported voice profile version")
    embedding = payload.get("embedding")
    if not isinstance(embedding, list) or not embedding:
        raise ValueError("voice profile embedding is missing or empty")
    try:
        values = tuple(float(value) for value in embedding)
    except (TypeError, ValueError) as exc:
        raise ValueError("voice profile embedding is invalid") from exc
    return VoiceProfile(values)
