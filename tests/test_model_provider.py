import json
import os
import socket
import unittest
from unittest.mock import patch

from agent.model_provider import (
    HttpChatProvider,
    InvalidModelResponse,
    ModelTimeout,
    ProviderUnavailable,
    create_model_provider,
)


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


class ModelProviderTests(unittest.TestCase):
    def test_parses_ollama_response(self):
        provider = HttpChatProvider(
            endpoint="http://localhost:11434", model="test", response_format="ollama"
        )
        with patch("agent.model_provider.urlopen", return_value=FakeResponse(
            {"message": {"content": "  Hello from Sentinel  "}}
        )):
            self.assertEqual(provider.generate("Hi"), "Hello from Sentinel")

    def test_parses_openai_compatible_response(self):
        provider = HttpChatProvider(
            endpoint="https://example.test/v1",
            model="test",
            api_key="secret",
            response_format="openai",
        )
        with patch("agent.model_provider.urlopen", return_value=FakeResponse(
            {"choices": [{"message": {"content": "Hello"}}]}
        )):
            self.assertEqual(provider.generate("Hi"), "Hello")

    def test_empty_or_malformed_response_is_rejected(self):
        provider = HttpChatProvider(endpoint="http://localhost:11434", model="test")
        for payload in ({}, {"message": {"content": "  "}}):
            with self.subTest(payload=payload):
                with patch("agent.model_provider.urlopen", return_value=FakeResponse(payload)):
                    with self.assertRaises(InvalidModelResponse):
                        provider.generate("Hi")

    def test_timeout_is_normalized(self):
        provider = HttpChatProvider(endpoint="http://localhost:11434", model="test")
        with patch("agent.model_provider.urlopen", side_effect=socket.timeout()):
            with self.assertRaises(ModelTimeout):
                provider.generate("Hi")

    def test_unavailable_provider_is_normalized(self):
        provider = HttpChatProvider(endpoint="http://localhost:11434", model="test")
        with patch("agent.model_provider.urlopen", side_effect=ConnectionError()):
            with self.assertRaises(ProviderUnavailable):
                provider.generate("Hi")

    def test_blank_prompt_is_rejected(self):
        provider = HttpChatProvider(endpoint="http://localhost:11434", model="test")
        with self.assertRaises(InvalidModelResponse):
            provider.generate("  ")

    def test_factory_configures_ollama(self):
        with patch.dict(os.environ, {
            "SENTINEL_MODEL_PROVIDER": "ollama",
            "SENTINEL_MODEL_NAME": "qwen2.5:3b",
            "SENTINEL_MODEL_BASE_URL": "http://127.0.0.1:11434",
            "SENTINEL_MODEL_TIMEOUT": "15",
        }, clear=True):
            provider = create_model_provider()
        self.assertEqual(provider.model, "qwen2.5:3b")
        self.assertEqual(provider.timeout, 15)


if __name__ == "__main__":
    unittest.main()
