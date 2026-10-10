import unittest

from agent.controller import SentinelAgent
from security.two_question import Question, TwoQuestionFallback


class FakeVoiceProvider:
    def __init__(self, result):
        self.result = result

    def verify(self, audio):
        return self.result


class FakeModelProvider:
    def __init__(self, response="Model response"):
        self.response = response
        self.prompts = []

    def generate(self, prompt):
        self.prompts.append(prompt)
        return self.response


class AgentIntegrationTests(unittest.TestCase):
    def test_wake_call_and_request(self):
        model = FakeModelProvider("Ready to help.")
        agent = SentinelAgent(model_provider=model)
        self.assertTrue(agent.check_wake_call("Hey Sentinel"))
        self.assertEqual(agent.handle_request("status"), "Authentication required.")
        agent.authenticate()
        self.assertEqual(agent.handle_request("status"), "Ready to help.")
        self.assertEqual(model.prompts, ["status"])

    def test_voice_authentication(self):
        agent = SentinelAgent(model_provider=FakeModelProvider())
        self.assertTrue(agent.authenticate_voice(b"audio", FakeVoiceProvider(True)))
        self.assertTrue(agent.authenticated)

    def test_fallback_authentication(self):
        agent = SentinelAgent(model_provider=FakeModelProvider())
        fallback = TwoQuestionFallback(
            (Question("First?"), Question("Second?")),
            ("blue", "coffee"),
        )
        self.assertTrue(agent.authenticate_fallback(("blue", "coffee"), fallback))
        self.assertTrue(agent.authenticated)


if __name__ == "__main__":
    unittest.main()
