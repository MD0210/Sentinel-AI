import os
import unittest
from unittest.mock import patch

from security.qa_config import create_fallback_from_environment


class QAConfigTests(unittest.TestCase):
    def test_environment_answers_create_working_fallback(self):
        with patch.dict(
            os.environ,
            {
                "SENTINEL_QA_ANSWER_1": "answer one",
                "SENTINEL_QA_ANSWER_2": "answer two",
            },
            clear=False,
        ):
            fallback = create_fallback_from_environment()

        self.assertEqual(fallback.questions[0].prompt, "What are the names of my dogs?")
        self.assertEqual(fallback.questions[1].prompt, "What is my catchphrase?")
        self.assertTrue(fallback.verify(("ANSWER ONE", "answer two")))

    def test_missing_environment_answer_is_rejected(self):
        with patch.dict(
            os.environ,
            {
                "SENTINEL_QA_ANSWER_1": "",
                "SENTINEL_QA_ANSWER_2": "answer two",
            },
            clear=False,
        ):
            with self.assertRaises(RuntimeError):
                create_fallback_from_environment()


if __name__ == "__main__":
    unittest.main()
