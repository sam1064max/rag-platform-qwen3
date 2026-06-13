from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import AsyncIterator


class ProviderType(str, Enum):
    VLLM = "vllm"
    OPENAI_COMPAT = "openai_compat"
    OPENROUTER = "openrouter"


@dataclass
class ProviderConfig:
    provider_type: ProviderType
    api_key: str = ""
    api_base: str = ""
    model: str = ""
    max_tokens: int = 4096
    temperature: float = 0.0
    top_p: float = 0.9
    timeout_seconds: int = 120
    extra_headers: dict[str, str] = field(default_factory=dict)


@dataclass
class GenerationResult:
    text: str
    provider: ProviderType
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    latency_ms: float = 0.0


class LLMProvider(ABC):
    def __init__(self, config: ProviderConfig) -> None:
        self.config = config

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> GenerationResult:
        ...

    @abstractmethod
    async def generate_stream(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ) -> AsyncIterator[str]:
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        ...
