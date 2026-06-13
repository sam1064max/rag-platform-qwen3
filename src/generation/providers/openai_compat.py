import time
from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from src.generation.providers.base import (
    GenerationResult,
    LLMProvider,
    ProviderConfig,
    ProviderType,
)


class OpenAICompatibleProvider(LLMProvider):
    def __init__(self, config: ProviderConfig) -> None:
        super().__init__(config)
        if not config.api_key:
            raise ValueError("api_key is required for OpenAI-compatible providers")
        if not config.api_base:
            raise ValueError("api_base is required for OpenAI-compatible providers")
        self._client = AsyncOpenAI(
            base_url=config.api_base,
            api_key=config.api_key,
            timeout=config.timeout_seconds,
            default_headers=config.extra_headers,
        )

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> GenerationResult:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        start = time.monotonic()
        response = await self._client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            top_p=self.config.top_p,
        )
        latency = (time.monotonic() - start) * 1000

        choice = response.choices[0]
        usage = response.usage

        return GenerationResult(
            text=choice.message.content or "",
            provider=ProviderType.OPENAI_COMPAT,
            model=self.config.model,
            input_tokens=usage.prompt_tokens if usage else 0,
            output_tokens=usage.completion_tokens if usage else 0,
            total_tokens=usage.total_tokens if usage else 0,
            latency_ms=latency,
        )

    async def generate_stream(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> AsyncIterator[str]:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        stream = await self._client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            top_p=self.config.top_p,
            stream=True,
        )

        async for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def health_check(self) -> bool:
        try:
            await self._client.models.list()
            return True
        except Exception:
            return False
