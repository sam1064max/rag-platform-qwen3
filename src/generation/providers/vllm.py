import time
from collections.abc import AsyncIterator

from openai import AsyncOpenAI

from src.generation.providers.base import (
    GenerationResult,
    LLMProvider,
    ProviderConfig,
    ProviderType,
)


class VLLMProvider(LLMProvider):
    def __init__(self, config: ProviderConfig) -> None:
        super().__init__(config)
        self._client = AsyncOpenAI(
            base_url=config.api_base or "http://localhost:8000/v1",
            api_key=config.api_key or "not-needed",
            timeout=config.timeout_seconds,
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
            model=self.config.model or "Qwen3-32B-Instruct",
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
            provider=ProviderType.VLLM,
            model=self.config.model or "Qwen3-32B-Instruct",
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
            model=self.config.model or "Qwen3-32B-Instruct",
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
