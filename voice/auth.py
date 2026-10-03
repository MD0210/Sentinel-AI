"""Voice authentication interface.

This module defines a provider-neutral contract. It does not claim to perform
biometric verification until a trusted audio/voice provider is integrated.
"""

from typing import Protocol


class VoiceAuthProvider(Protocol):
    def verify(self, audio: bytes) -> bool:
        """Return whether the supplied audio passes provider verification."""
        ...


class VoiceAuthenticator:
    def __init__(self, provider: VoiceAuthProvider):
        self.provider = provider

    def authenticate(self, audio: bytes) -> bool:
        return bool(self.provider.verify(audio))
