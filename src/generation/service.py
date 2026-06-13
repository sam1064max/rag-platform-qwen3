from collections.abc import AsyncIterator

from src.generation.providers.base import (
    GenerationResult,
    LLMProvider,
)


class GenerationService:
    def __init__(self, provider: LLMProvider) -> None:
        self._provider = provider

    async def generate(
        self,
        query: str,
        context: str,
        system_prompt: str | None = None,
    ) -> GenerationResult:
        prompt = (
            "Answer the question based on the provided context.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {query}\n\n"
            "Answer the question using only the information from the context. "
            "If the context does not contain enough information, state that clearly. "
            "Include citations in [N] format."
        )

        return await self._provider.generate(
            prompt=prompt,
            system_prompt=system_prompt,
        )

    async def generate_stream(
        self,
        query: str,
        context: str,
        system_prompt: str | None = None,
    ) -> AsyncIterator[str]:
        prompt = (
            "Answer the question based on the provided context.\n\n"
            f"Context:\n{context}\n\n"
            f"Question: {query}\n\n"
            "Answer the question using only the information from the context. "
            "If the context does not contain enough information, state that clearly. "
            "Include citations in [N] format."
        )

        async for token in self._provider.generate_stream(
            prompt=prompt,
            system_prompt=system_prompt,
        ):
            yield token

    async def health_check(self) -> bool:
        return await self._provider.health_check()
