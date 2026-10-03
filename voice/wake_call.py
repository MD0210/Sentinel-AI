"""Wake-call detection interface for Sentinel AI.

The detector is intentionally engine-agnostic so a real wake-word backend can
be connected later without changing the agent-facing API.
"""

from dataclasses import dataclass


@dataclass
class WakeCall:
    phrase: str = "hey sentinel"

    def matches(self, text: str) -> bool:
        """Return True when the normalized text contains the wake phrase."""
        normalized = " ".join(text.casefold().strip().split())
        return normalized == self.phrase.casefold()

    def activate(self, text: str) -> bool:
        """Check a spoken/text transcript and report whether Sentinel is active."""
        return self.matches(text)
