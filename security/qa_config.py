"""Build the two-question fallback from local environment values.

The .env file is intentionally ignored by Git. Answers are passed directly to
the existing TwoQuestionFallback, which stores only salted PBKDF2 hashes.
"""

import os

from security.two_question import Question, TwoQuestionFallback


QUESTION_ONE = "What are the names of my dogs?"
QUESTION_TWO = "What is my catchphrase?"


def create_fallback_from_environment() -> TwoQuestionFallback:
    answer_one = os.getenv("SENTINEL_QA_ANSWER_1")
    answer_two = os.getenv("SENTINEL_QA_ANSWER_2")

    if not answer_one or not answer_two:
        raise RuntimeError(
            "SENTINEL_QA_ANSWER_1 and SENTINEL_QA_ANSWER_2 must be configured"
        )

    return TwoQuestionFallback(
        (Question(QUESTION_ONE), Question(QUESTION_TWO)),
        (answer_one, answer_two),
    )
