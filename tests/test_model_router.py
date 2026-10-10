import os
import unittest
from unittest.mock import patch

from agent.model_router import ModelRouter, classify_task, create_model_router


class FakeProvider:
    def __init__(self, response):
        self.response = response
        self.prompts = []

    def generate(self, prompt):
        self.prompts.append(prompt)
        return self.response


class ModelRouterTests(unittest.TestCase):
    def test_classifies_coding_requests(self):
        self.assertEqual(classify_task("Debug this Python function"), "coding")
        self.assertEqual(classify_task("Write a SQL query"), "coding")

    def test_classifies_reasoning_requests(self):
        self.assertEqual(classify_task("Compare these two approaches"), "reasoning")
        self.assertEqual(classify_task("Help me plan a migration"), "reasoning")

    def test_defaults_to_general(self):
        self.assertEqual(classify_task("Hello Sentinel"), "general")
        self.assertEqual(classify_task("   "), "general")

    def test_coding_takes_precedence_over_reasoning(self):
        self.assertEqual(
            classify_task("Analyze this Python traceback and debug it"),
            "coding",
        )

    def test_uses_specialist_when_configured(self):
        default = FakeProvider("default response")
        coding = FakeProvider("coding response")
        router = ModelRouter(default, providers={"coding": coding})

        self.assertEqual(router.generate("Debug this Python function"), "coding response")
        self.assertEqual(router.last_route, "coding")
        self.assertEqual(router.last_provider, "coding")
        self.assertEqual(coding.prompts, ["Debug this Python function"])
        self.assertEqual(default.prompts, [])

    def test_falls_back_to_default_for_unconfigured_route(self):
        default = FakeProvider("default response")
        router = ModelRouter(default)

        self.assertEqual(router.generate("Compare two options"), "default response")
        self.assertEqual(router.last_route, "reasoning")
        self.assertEqual(router.last_provider, "default")
        self.assertEqual(default.prompts, ["Compare two options"])

    def test_factory_builds_optional_specialist_routes(self):
        with patch.dict(os.environ, {
            "SENTINEL_MODEL_PROVIDER": "ollama",
            "SENTINEL_MODEL_NAME": "llama3.2",
            "SENTINEL_MODEL_CODING_PROVIDER": "ollama",
            "SENTINEL_MODEL_CODING_NAME": "qwen2.5-coder:3b",
        }, clear=True):
            with patch("agent.model_router.create_model_provider") as factory:
                default = FakeProvider("default")
                coding = FakeProvider("coding")
                factory.side_effect = [default, coding]
                router = create_model_router()

        self.assertIs(router.default_provider, default)
        self.assertIs(router.providers["coding"], coding)
        self.assertNotIn("reasoning", router.providers)
        self.assertEqual(factory.call_count, 2)
        factory.assert_any_call()
        factory.assert_any_call(prefix="SENTINEL_MODEL_CODING")

    def test_factory_rejects_partial_specialist_configuration(self):
        with patch.dict(os.environ, {
            "SENTINEL_MODEL_PROVIDER": "ollama",
            "SENTINEL_MODEL_NAME": "llama3.2",
            "SENTINEL_MODEL_CODING_PROVIDER": "ollama",
        }, clear=True):
            with patch("agent.model_router.create_model_provider", return_value=FakeProvider("ok")):
                with self.assertRaisesRegex(ValueError, "Configure both SENTINEL_MODEL_CODING_PROVIDER"):
                    create_model_router()


if __name__ == "__main__":
    unittest.main()
