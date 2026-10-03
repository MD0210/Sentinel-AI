"""Two-question fallback authentication.

Answers are stored only as salted PBKDF2-HMAC-SHA256 digests, never plaintext.
"""

from dataclasses import dataclass
import hashlib
import hmac
import secrets


@dataclass(frozen=True)
class Question:
    prompt: str


class TwoQuestionFallback:
    ITERATIONS = 310_000
    DIGEST = "sha256"
    SALT_BYTES = 16

    def __init__(self, questions: tuple[Question, Question], answers: tuple[str, str]):
        if len(questions) != 2 or len(answers) != 2:
            raise ValueError("exactly two questions and two answers are required")
        self.questions = questions
        self._stored = tuple(self._hash_answer(answer) for answer in answers)

    def _hash_answer(self, answer: str) -> tuple[bytes, bytes]:
        salt = secrets.token_bytes(self.SALT_BYTES)
        digest = hashlib.pbkdf2_hmac(
            self.DIGEST, answer.strip().casefold().encode("utf-8"),
            salt, self.ITERATIONS
        )
        return salt, digest

    def verify(self, answers: tuple[str, str]) -> bool:
        if len(answers) != 2:
            return False
        for answer, (salt, expected) in zip(answers, self._stored):
            actual = hashlib.pbkdf2_hmac(
                self.DIGEST, answer.strip().casefold().encode("utf-8"),
                salt, self.ITERATIONS
            )
            if not hmac.compare_digest(actual, expected):
                return False
        return True
