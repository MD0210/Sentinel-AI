import os
import unittest
from unittest.mock import patch

from agent.controller import SentinelAgent


class AgentQAEnvironmentTests(unittest.TestCase):
    def test_agent_can_authenticate_with_local_q_and_a(self):
        with patch.dict(
            os.environ,
            {
                "SENTINEL_QA_ANSWER_1": "answer one",
                "SENTINEL_QA_ANSWER_2": "answer two",
            },
            clear=False,
        ):
            agent = SentinelAgent()
            self.assertTrue(
                agent.authenticate_fallback_from_environment(
                    ("ANSWER ONE", "answer two")
                )
            )
            self.assertTrue(agent.authenticated)

    def test_wrong_answer_does_not_authenticate(self):
        with patch.dict(
            os.environ,
            {
                "SENTINEL_QA_ANSWER_1": "answer one",
                "SENTINEL_QA_ANSWER_2": "answer two",
            },
            clear=False,
        ):
            agent = SentinelAgent()
            self.assertFalse(
                agent.authenticate_fallback_from_environment(
                    ("wrong", "answer two")
                )
            )
            self.assertFalse(agent.authenticated)


if __name__ == "__main__":
    unittest.main()
