"""Sentinel AI agent controller with security and voice-layer integration."""

from security.auth import SecurityManager
from security.policy import AuthorizationPolicy, Role
from security.qa_config import create_fallback_from_environment
from security.two_question import TwoQuestionFallback
from voice.auth import VoiceAuthenticator, VoiceAuthProvider
from voice.wake_call import WakeCall


class SentinelAgent:
    """Coordinate authentication, wake-call activation, and requests."""

    def __init__(
        self,
        security: SecurityManager | None = None,
        policy: AuthorizationPolicy | None = None,
        wake_call: WakeCall | None = None,
    ):
        self.security = security or SecurityManager()
        self.policy = policy or AuthorizationPolicy()
        self.wake_call = wake_call or WakeCall()
        self.role = Role.USER

    @property
    def authenticated(self) -> bool:
        return self.security.state.authenticated

    def authenticate(self) -> str:
        """Authenticate the current user through the foundation path."""
        if self.security.is_locked():
            return "Authentication locked."
        self.security.record_success()
        return "Sentinel authenticated."

    def authenticate_voice(
        self, audio: bytes, provider: VoiceAuthProvider
    ) -> bool:
        """Authenticate using a supplied trusted voice provider."""
        if self.security.is_locked():
            return False
        verified = VoiceAuthenticator(provider).authenticate(audio)
        if verified:
            self.security.record_success()
        else:
            self.security.record_failure()
        return verified

    def authenticate_fallback(
        self, answers: tuple[str, str], fallback: TwoQuestionFallback
    ) -> bool:
        """Authenticate through a configured two-question fallback."""
        if self.security.is_locked():
            return False
        verified = fallback.verify(answers)
        if verified:
            self.security.record_success()
        else:
            self.security.record_failure()
        return verified

    def authenticate_fallback_from_environment(
        self, answers: tuple[str, str]
    ) -> bool:
        """Authenticate using the locally configured Q&A fallback."""
        fallback = create_fallback_from_environment()
        return self.authenticate_fallback(answers, fallback)

    def check_wake_call(self, text: str) -> bool:
        """Return True when the wake phrase is detected."""
        return self.wake_call.activate(text)

    def handle_request(self, request: str) -> str:
        """Handle a normal user request after authentication."""
        if self.security.is_locked() or not self.authenticated:
            return "Authentication required."
        if not self.policy.allowed(self.role, "request"):
            return "Request not authorized."
        return f"I received your request: {request}"
