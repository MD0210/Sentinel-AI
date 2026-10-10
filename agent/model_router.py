"""Deterministic task-based model routing for Sentinel Core."""

from __future__ import annotations

import re
from collections.abc import Mapping

from agent.model_provider import ModelProvider, create_model_provider


_TASK_PATTERNS = {
    "coding": re.compile(
        r"\b(code|coding|program(?:ming)?|python|javascript|typescript|sql|debug|"
        r"bug|traceback|stack trace|function|class|script|compile|exception|"
        r"algorithm|api|repository|git|unit test|pytest|unittest)\b",
        re.IGNORECASE,
    ),
    "reasoning": re.compile(
        r"\b(analy[sz]e|analysis|compare|comparison|evaluate|reason(?:ing)?|"
        r"plan(?:ning)?|trade.?off|pros and cons|decision|solve|problem|strategy|"
        r"architecture|design|why|explain|recommend(?:ation)?)\b",
        re.IGNORECASE,
    ),
}


def classify_task(prompt: str) -> str:
    """Classify a prompt using transparent keyword rules, without another model call.

    Coding takes precedence over reasoning when a request contains both types of
    cues. Anything not matched is routed to the general model.
    """
    if not isinstance(prompt, str) or not prompt.strip():
        return "general"
    if _TASK_PATTERNS["coding"].search(prompt):
        return "coding"
    if _TASK_PATTERNS["reasoning"].search(prompt):
        return "reasoning"
    return "general"


class ModelRouter:
    """Select a configured specialist provider, falling back to the default."""

    def __init__(
        self,
        default_provider: ModelProvider,
        *,
        providers: Mapping[str, ModelProvider] | None = None,
    ):
        self.default_provider = default_provider
        self.providers = dict(providers or {})
        self.last_route = "general"
        self.last_provider = "default"

    def provider_for(self, task: str) -> ModelProvider:
        """Return the specialist provider for a task, or the default provider."""
        if task in self.providers:
            self.last_provider = task
            return self.providers[task]
        self.last_provider = "default"
        return self.default_provider

    def generate(self, prompt: str) -> str:
        """Route the prompt to a specialist when configured, otherwise default."""
        self.last_route = classify_task(prompt)
        return self.provider_for(self.last_route).generate(prompt)


def create_model_router() -> ModelRouter:
    """Create a default model and any explicitly configured specialist models.

    Existing SENTINEL_MODEL_* variables configure the default model. Optional
    specialist routes require both SENTINEL_MODEL_<TASK>_PROVIDER and
    SENTINEL_MODEL_<TASK>_NAME (TASK is CODING or REASONING).
    """
    default_provider = create_model_provider()
    providers: dict[str, ModelProvider] = {}

    for task in ("coding", "reasoning"):
        prefix = f"SENTINEL_MODEL_{task.upper()}"
        provider_configured = bool(__import__("os").getenv(f"{prefix}_PROVIDER", "").strip())
        model_configured = bool(__import__("os").getenv(f"{prefix}_NAME", "").strip())
        if provider_configured != model_configured:
            raise ValueError(
                f"Configure both {prefix}_PROVIDER and {prefix}_NAME, or neither."
            )
        if provider_configured:
            providers[task] = create_model_provider(prefix=prefix)

    return ModelRouter(default_provider, providers=providers)
