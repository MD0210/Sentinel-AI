"""Basic authorization policy for Sentinel.

This is intentionally small; resource-specific permissions can be added later.
"""

from enum import Enum


class Role(str, Enum):
    USER = "user"
    ADMIN = "admin"


class AuthorizationPolicy:
    def __init__(self):
        self._permissions = {
            Role.USER: {"request"},
            Role.ADMIN: {"request", "admin"},
        }

    def allowed(self, role: Role, action: str) -> bool:
        return action in self._permissions.get(role, set())
