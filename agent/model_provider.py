"""Provider-neutral language-model adapters for Sentinel Core.

Only the Python standard library is required. The default provider is local Ollama.
Hosted providers can use an OpenAI-compatible chat-completions endpoint.
"""

from __future__ import annotations

import json
import os
import socket
from typing import Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


class ModelProviderError(RuntimeError):
    """Base class for safe, user-displayable model provider errors."""

    user_message = "The model could not complete this request."


class ProviderUnavailable(ModelProviderError):
    user_message = "the configured provider is unavailable. Check its URL and that it is running."


class ModelTimeout(ModelProviderError):
    user_message = "the model request timed out. Try again or increase the configured model timeout."


class InvalidModelResponse(ModelProviderError):
    user_message = "the provider returned an invalid or empty response."


class ModelProvider(Protocol):
    """Minimal contract implemented by all model adapters."""

    def generate(self, prompt: str) -> str:
        """Return a non-empty assistant response for a user prompt."""


class HttpChatProvider:
    """Chat-completions adapter for Ollama or OpenAI-compatible endpoints."""

    def __init__(
        self,
        *,
        endpoint: str,
        model: str,
        timeout: float = 60.0,
        api_key: str | None = None,
        response_format: str = "ollama",
    ):
        self.endpoint = endpoint.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.api_key = api_key
        self.response_format = response_format

    def generate(self, prompt: str) -> str:
        if not isinstance(prompt, str) or not prompt.strip():
            raise InvalidModelResponse()

        if self.response_format == "ollama":
            url = f"{self.endpoint}/api/chat"
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            }
        else:
            url = f"{self.endpoint}/chat/completions"
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            }

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        request = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        try:
            with urlopen(request, timeout=self.timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
        except (socket.timeout, TimeoutError) as exc:
            raise ModelTimeout() from exc
        except HTTPError as exc:
            # Do not include provider response bodies or headers in surfaced errors.
            if exc.code in (401, 403, 404, 429, 500, 502, 503, 504):
                raise ProviderUnavailable() from exc
            raise ModelProviderError() from exc
        except (URLError, ConnectionError, OSError) as exc:
            if isinstance(exc, (socket.timeout, TimeoutError)):
                raise ModelTimeout() from exc
            raise ProviderUnavailable() from exc
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            raise InvalidModelResponse() from exc

        try:
            if self.response_format == "ollama":
                content = data["message"]["content"]
            else:
                content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise InvalidModelResponse() from exc

        if not isinstance(content, str) or not content.strip():
            raise InvalidModelResponse()
        return content.strip()


def create_model_provider(prefix: str = "SENTINEL_MODEL") -> ModelProvider:
    """Create an adapter from environment variables.

    The default model uses SENTINEL_MODEL_PROVIDER, SENTINEL_MODEL_NAME,
    SENTINEL_MODEL_BASE_URL, SENTINEL_MODEL_API_KEY, and SENTINEL_MODEL_TIMEOUT.

    Specialist prefixes (for example SENTINEL_MODEL_CODING) use
    <PREFIX>_PROVIDER, <PREFIX>_NAME, <PREFIX>_BASE_URL, <PREFIX>_API_KEY,
    and <PREFIX>_TIMEOUT.
    """
    is_default = prefix == "SENTINEL_MODEL"
    provider_var = f"{prefix}_PROVIDER"
    model_var = "SENTINEL_MODEL_NAME" if is_default else f"{prefix}_NAME"
    base_url_var = f"{prefix}_BASE_URL"
    api_key_var = f"{prefix}_API_KEY"
    timeout_var = f"{prefix}_TIMEOUT"

    provider = os.getenv(provider_var, "ollama" if is_default else "").strip().lower()
    model = os.getenv(model_var, "llama3.2" if is_default else "").strip()
    timeout_raw = os.getenv(timeout_var, "60").strip()
    if not provider:
        raise ValueError(f"{provider_var} must be configured.")
    if not model:
        raise ValueError(f"{model_var} cannot be empty.")

    try:
        timeout = float(timeout_raw)
        if timeout <= 0:
            raise ValueError
    except ValueError as exc:
        raise ValueError(f"{timeout_var} must be a positive number.") from exc

    if provider == "ollama":
        endpoint = os.getenv(
            base_url_var, "http://127.0.0.1:11434"
        ).strip()
        if not endpoint:
            raise ValueError(f"{base_url_var} cannot be empty.")
        return HttpChatProvider(
            endpoint=endpoint, model=model, timeout=timeout, response_format="ollama"
        )

    if provider in {"openai-compatible", "openai_compatible"}:
        endpoint = os.getenv(
            base_url_var, "https://api.openai.com/v1"
        ).strip()
        api_key = os.getenv(api_key_var, "").strip()
        if not endpoint:
            raise ValueError(f"{base_url_var} cannot be empty.")
        if not api_key:
            raise ProviderUnavailable()
        return HttpChatProvider(
            endpoint=endpoint,
            model=model,
            timeout=timeout,
            api_key=api_key,
            response_format="openai",
        )

    raise ValueError(
        f"{provider_var} must be 'ollama' or 'openai-compatible'."
    )
