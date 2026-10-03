"""Basic authentication state, failed-attempt tracking, cooldown, and audit logging.

This foundation intentionally does not store passwords, voiceprints, or secrets.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone


@dataclass
class AuthState:
    authenticated: bool = False
    failed_attempts: int = 0
    locked_until: datetime | None = None
    audit_log: list[str] = field(default_factory=list)


class SecurityManager:
    def __init__(self, max_attempts: int = 3, lockout_seconds: int = 30):
        self.max_attempts = max_attempts
        self.lockout_seconds = lockout_seconds
        self.state = AuthState()

    def _now(self) -> datetime:
        return datetime.now(timezone.utc)

    def is_locked(self) -> bool:
        if self.state.locked_until is None:
            return False
        if self._now() >= self.state.locked_until:
            self.state.locked_until = None
            self.state.failed_attempts = 0
            self._audit("lockout expired")
            return False
        return True

    def record_success(self) -> None:
        self.state.authenticated = True
        self.state.failed_attempts = 0
        self.state.locked_until = None
        self._audit("authentication succeeded")

    def record_failure(self) -> None:
        self.state.authenticated = False
        self.state.failed_attempts += 1
        self._audit("authentication failed")

        if self.state.failed_attempts >= self.max_attempts:
            self.state.locked_until = self._now() + timedelta(
                seconds=self.lockout_seconds
            )
            self._audit("authentication locked out")

    def logout(self) -> None:
        self.state.authenticated = False
        self._audit("logged out")

    def _audit(self, event: str) -> None:
        timestamp = self._now().isoformat()
        self.state.audit_log.append(f"{timestamp} - {event}")
