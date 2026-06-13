from src.generation.providers.base import LLMProvider, ProviderConfig, ProviderType
from src.generation.providers.vllm import VLLMProvider
from src.generation.providers.openai_compat import OpenAICompatibleProvider
from src.generation.providers.openrouter import OpenRouterProvider


def create_provider(config: ProviderConfig) -> LLMProvider:
    providers = {
        ProviderType.VLLM: VLLMProvider,
        ProviderType.OPENAI_COMPAT: OpenAICompatibleProvider,
        ProviderType.OPENROUTER: OpenRouterProvider,
    }
    provider_cls = providers.get(config.provider_type)
    if not provider_cls:
        raise ValueError(f"Unknown provider type: {config.provider_type}")
    return provider_cls(config)
