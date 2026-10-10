"""Sentinel AI request controller with configurable model responses."""

from getpass import getpass

from agent.model_provider import ModelProvider, ModelProviderError
from agent.model_router import create_model_router
from security.auth import SecurityManager
from security.policy import AuthorizationPolicy, Role
from security.qa_config import create_fallback_from_environment
from security.two_question import TwoQuestionFallback
from voice.auth import VoiceAuthenticator, VoiceAuthProvider
from voice.wake_call import WakeCall


class SentinelAgent:
    """Coordinate authentication, request authorization, and model responses."""

    def __init__(
        self,
        security: SecurityManager | None = None,
        policy: AuthorizationPolicy | None = None,
        wake_call: WakeCall | None = None,
        model_provider: ModelProvider | None = None,
    ):
        self.security = security or SecurityManager()
        self.policy = policy or AuthorizationPolicy()
        self.wake_call = wake_call or WakeCall()
        self.model_provider = model_provider or create_model_router()
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
        """Authenticate through a supplied two-question fallback."""
        if self.security.is_locked():
            return False
        verified = fallback.verify(answers)
        if verified:
            self.security.record_success()
        else:
            self.security.record_failure()
        return verified

    def authenticate_fallback_from_environment(
        self, answers: tuple[str, str] | None = None
    ) -> bool:
        """Authenticate with local Q&A, prompting securely when answers are omitted."""
        fallback = create_fallback_from_environment()
        if answers is None:
            answers = (
                getpass(f"{fallback.questions[0].prompt} "),
                getpass(f"{fallback.questions[1].prompt} "),
            )
        return self.authenticate_fallback(answers, fallback)

    def check_wake_call(self, text: str) -> bool:
        """Return True when the wake phrase is detected."""
        return self.wake_call.activate(text)

    def handle_request(self, request: str) -> str:
        """Generate a response to a normal user request after authorization."""
        if self.security.is_locked() or not self.authenticated:
            return "Authentication required."
        if not self.policy.allowed(self.role, "request"):
            return "Request not authorized."
        if not request or not request.strip():
            return "Please enter a request."
        try:
            response = self.model_provider.generate(request.strip())
        except ModelProviderError as exc:
            # Provider exceptions are deliberately normalized; do not expose raw
            # HTTP bodies, credentials, or other provider internals to the user.
            return f"Sentinel model error: {exc.user_message}"
        return response
