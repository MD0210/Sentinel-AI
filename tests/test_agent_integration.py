import unittest

from agent.controller import SentinelAgent
from security.two_question import Question, TwoQuestionFallback


class FakeVoiceProvider:
    def __init__(self, result):
        self.result = result

    def verify(self, audio):
        return self.result


class AgentIntegrationTests(unittest.TestCase):
    def test_wake_call_and_request(self):
        agent = SentinelAgent()
        self.assertTrue(agent.check_wake_call("Hey Sentinel"))
        self.assertEqual(agent.handle_request("status"), "Authentication required.")
        agent.authenticate()
        self.assertEqual(agent.handle_request("status"), "I received your request: status")

    def test_voice_authentication(self):
        agent = SentinelAgent()
        self.assertTrue(agent.authenticate_voice(b"audio", FakeVoiceProvider(True)))
        self.assertTrue(agent.authenticated)

    def test_fallback_authentication(self):
        agent = SentinelAgent()
        fallback = TwoQuestionFallback(
            (Question("First?"), Question("Second?")),
            ("blue", "coffee"),
        )
        self.assertTrue(agent.authenticate_fallback(("blue", "coffee"), fallback))
        self.assertTrue(agent.authenticated)


if __name__ == "__main__":
    unittest.main()
