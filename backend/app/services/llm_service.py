"""
LLM Service - Multi-Provider Smart Router

Unified interface to 4 LLM providers using LiteLLM.
Automatically routes requests to the best provider based on task type,
with automatic fallback if the primary provider fails or is rate-limited.

Providers:
    - Ollama (local, unlimited, primary)
    - Gemini Flash (free tier, complex reasoning)
    - Groq (free tier, ultra-fast grading)
    - DeepSeek (free tier, coding tasks)
"""

import logging
from typing import Optional
from litellm import acompletion
from litellm.exceptions import (
    RateLimitError,
    APIConnectionError,
    ServiceUnavailableError,
)

from app.config import settings

logger = logging.getLogger(__name__)


# Smart routing: maps task types to ordered provider preferences
# First provider is preferred; falls back to next if unavailable
ROUTING_TABLE: dict[str, list[str]] = {
    "curriculum_generation": ["gemini", "groq", "deepseek", "ollama"],    # Complex planning needs strong model
    "teaching":             ["gemini", "groq", "deepseek", "ollama"],      # Prefer cloud for speed/reliability
    "quiz_generation":      ["gemini", "groq", "deepseek", "ollama"],      # Generate test questions
    "quiz_grading":         ["groq", "gemini", "deepseek", "ollama"],        # Speed matters for grading
    "coding_challenges":    ["deepseek", "gemini", "groq", "ollama"],    # DeepSeek excels at code
    "code_evaluation":      ["deepseek", "groq", "gemini", "ollama"],      # Code grading
    "analysis":             ["gemini", "groq", "deepseek", "ollama"],       # Pattern detection needs reasoning
    "strategy":             ["gemini", "groq", "deepseek", "ollama"],       # Adaptation decisions
    "general":              ["gemini", "groq", "deepseek", "ollama"],       # Default: cloud first
}

# Provider → LiteLLM model string mapping
PROVIDER_MODELS: dict[str, str] = {
    "ollama": f"ollama/{settings.ollama_model}",
    "gemini": "gemini/gemini-2.0-flash",
    "groq": "groq/llama-3.1-8b-instant",
    "deepseek": "deepseek/deepseek-chat",
}

# Provider-specific API base URLs
PROVIDER_BASES: dict[str, Optional[str]] = {
    "ollama": settings.ollama_base_url,
    "gemini": None,   # LiteLLM handles this via GEMINI_API_KEY env var
    "groq": None,     # LiteLLM handles this via GROQ_API_KEY env var
    "deepseek": None,  # LiteLLM handles this via DEEPSEEK_API_KEY env var
}


class LLMService:
    """
    Unified LLM interface with smart routing and automatic failover.

    Usage:
        llm = LLMService()
        response = await llm.generate(
            prompt="Explain Python decorators",
            task_type="teaching",
            system_prompt="You are a patient tutor.",
        )
    """

    def __init__(self) -> None:
        self.available_providers = settings.available_providers
        logger.info(f"LLM Service initialized with providers: {self.available_providers}")

    def _get_provider_chain(self, task_type: str) -> list[str]:
        """
        Get ordered list of providers to try for a given task type.
        Filters out providers that aren't configured.
        """
        preferred = ROUTING_TABLE.get(task_type, ROUTING_TABLE["general"])
        # Only include providers that are actually available
        return [p for p in preferred if p in self.available_providers]

    async def generate(
        self,
        prompt: str,
        task_type: str = "general",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        json_mode: bool = False,
    ) -> str:
        """
        Generate a response using the best available provider for the task.

        Args:
            prompt: The user/agent prompt
            task_type: Type of task (maps to ROUTING_TABLE)
            system_prompt: Optional system-level instruction
            temperature: Creativity (0.0 = deterministic, 1.0 = creative)
            max_tokens: Maximum response length
            json_mode: If True, request JSON output format

        Returns:
            Generated text response

        Raises:
            RuntimeError: If all providers fail
        """
        provider_chain = self._get_provider_chain(task_type)

        if not provider_chain:
            raise RuntimeError(
                f"No LLM providers available for task '{task_type}'. "
                f"Available: {self.available_providers}"
            )

        # Build messages
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        # Try each provider in order
        last_error = None
        for provider in provider_chain:
            try:
                model = PROVIDER_MODELS[provider]
                api_base = PROVIDER_BASES[provider]

                logger.debug(
                    f"Trying provider '{provider}' (model: {model}) for task '{task_type}'"
                )

                kwargs = {
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }

                if api_base:
                    kwargs["api_base"] = api_base

                if json_mode:
                    kwargs["response_format"] = {"type": "json_object"}

                response = await acompletion(**kwargs)
                result = response.choices[0].message.content

                logger.info(
                    f"✅ Provider '{provider}' succeeded for task '{task_type}' "
                    f"({len(result)} chars)"
                )
                return result

            except (RateLimitError, APIConnectionError, ServiceUnavailableError) as e:
                logger.warning(
                    f"⚠️ Provider '{provider}' failed for task '{task_type}': {e}. "
                    f"Trying next..."
                )
                last_error = e
                continue
            except Exception as e:
                logger.error(
                    f"❌ Provider '{provider}' unexpected error: {e}"
                )
                last_error = e
                continue

        raise RuntimeError(
            f"All LLM providers failed for task '{task_type}'. "
            f"Tried: {provider_chain}. Last error: {last_error}"
        )

    async def health_check(self) -> dict[str, str]:
        """
        Check which providers are currently responsive.
        Returns status for each configured provider.
        """
        results = {}
        for provider in self.available_providers:
            try:
                model = PROVIDER_MODELS[provider]
                api_base = PROVIDER_BASES[provider]

                kwargs = {
                    "model": model,
                    "messages": [{"role": "user", "content": "Say 'ok'"}],
                    "max_tokens": 5,
                }
                if api_base:
                    kwargs["api_base"] = api_base

                await acompletion(**kwargs)
                results[provider] = "healthy"
            except Exception as e:
                results[provider] = f"error: {str(e)[:100]}"

        return results


# Singleton instance
llm_service = LLMService()
