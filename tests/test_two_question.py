import unittest

from security.two_question import Question, TwoQuestionFallback


class TwoQuestionFallbackTests(unittest.TestCase):
    def setUp(self):
        self.fallback = TwoQuestionFallback(
            (Question("First?"), Question("Second?")),
            ("Blue", "Coffee"),
        )

    def test_correct_answers_verify(self):
        self.assertTrue(self.fallback.verify(("blue", "coffee")))

    def test_wrong_answer_fails(self):
        self.assertFalse(self.fallback.verify(("blue", "tea")))

    def test_wrong_number_of_answers_fails(self):
        self.assertFalse(self.fallback.verify(("blue",)))


if __name__ == "__main__":
    unittest.main()
