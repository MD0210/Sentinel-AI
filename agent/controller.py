class SentinelAgent:
    """Minimal Sentinel AI agent controller."""

    def __init__(self):
        self.authenticated = False

    def authenticate(self) -> str:
        """Stub authentication for the initial vertical slice."""
        self.authenticated = True
        return "Sentinel authenticated."

    def handle_request(self, request: str) -> str:
        """Handle a request after authentication."""
        if not self.authenticated:
            return "Authentication required."

        return f"I received your request: {request}"
