from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.generation.providers.base import LLMProvider, ProviderConfig, ProviderType
from src.generation.providers.factory import create_provider


class TestProviderConfig:
    def test_default_values(self) -> None:
        config = ProviderConfig(provider_type=ProviderType.VLLM)
        assert config.provider_type == ProviderType.VLLM
        assert config.api_key == ""
        assert config.api_base == ""
        assert config.model == ""
        assert config.max_tokens == 4096
        assert config.temperature == 0.0
        assert config.top_p == 0.9
        assert config.timeout_seconds == 120
        assert config.extra_headers == {}

    def test_custom_values(self) -> None:
        config = ProviderConfig(
            provider_type=ProviderType.OPENROUTER,
            api_key="sk-test",
            api_base="https://test.api.com/v1",
            model="qwen3-32b",
            max_tokens=2048,
            temperature=0.7,
            extra_headers={"X-Custom": "value"},
        )
        assert config.api_key == "sk-test"
        assert config.api_base == "https://test.api.com/v1"
        assert config.model == "qwen3-32b"
        assert config.extra_headers == {"X-Custom": "value"}


class TestProviderFactory:
    def test_create_vllm_provider(self) -> None:
        config = ProviderConfig(provider_type=ProviderType.VLLM)
        provider = create_provider(config)
        assert isinstance(provider, LLMProvider)
        assert provider.config.provider_type == ProviderType.VLLM

    def test_create_openai_compat_provider(self) -> None:
        config = ProviderConfig(
            provider_type=ProviderType.OPENAI_COMPAT,
            api_key="sk-test",
            api_base="https://api.openai.com/v1",
            model="gpt-4",
        )
        provider = create_provider(config)
        assert provider.config.provider_type == ProviderType.OPENAI_COMPAT

    def test_create_openrouter_provider(self) -> None:
        config = ProviderConfig(
            provider_type=ProviderType.OPENROUTER,
            api_key="sk-test",
            model="qwen3-32b",
        )
        provider = create_provider(config)
        assert provider.config.provider_type == ProviderType.OPENROUTER

    def test_invalid_provider_type(self) -> None:
        config = ProviderConfig(provider_type="unknown")  # type: ignore
        with pytest.raises(ValueError, match="Unknown provider type"):
            create_provider(config)


class TestVLLMProvider:
    @pytest.mark.asyncio
    async def test_health_check(self) -> None:
        config = ProviderConfig(
            provider_type=ProviderType.VLLM,
            api_base="http://localhost:8000/v1",
        )
        with patch(
            "src.generation.providers.vllm.AsyncOpenAI"
        ) as mock_client:
            instance = mock_client.return_value
            instance.models.list = AsyncMock(
                return_value=MagicMock()
            )
            provider = create_provider(config)
            result = await provider.health_check()
            assert result is True

    @pytest.mark.asyncio
    async def test_health_check_failure(self) -> None:
        config = ProviderConfig(
            provider_type=ProviderType.VLLM,
            api_base="http://localhost:8000/v1",
        )
        with patch(
            "src.generation.providers.vllm.AsyncOpenAI"
        ) as mock_client:
            instance = mock_client.return_value
            instance.models.list = AsyncMock(
                side_effect=Exception("Connection refused")
            )
            provider = create_provider(config)
            result = await provider.health_check()
            assert result is False


class TestOpenAICompatibleProvider:
    def test_missing_api_key(self) -> None:
        config = ProviderConfig(
            provider_type=ProviderType.OPENAI_COMPAT,
            api_base="https://api.openai.com/v1",
            model="gpt-4",
        )
        with pytest.raises(ValueError, match="api_key is required"):
            create_provider(config)

    def test_missing_api_base(self) -> None:
        config = ProviderConfig(
            provider_type=ProviderType.OPENAI_COMPAT,
            api_key="sk-test",
            model="gpt-4",
        )
        with pytest.raises(ValueError, match="api_base is required"):
            create_provider(config)


class TestOpenRouterProvider:
    def test_missing_api_key(self) -> None:
        config = ProviderConfig(
            provider_type=ProviderType.OPENROUTER,
            model="qwen3-32b",
        )
        with pytest.raises(ValueError, match="api_key is required"):
            create_provider(config)

    @pytest.mark.asyncio
    async def test_default_headers(self) -> None:
        config = ProviderConfig(
            provider_type=ProviderType.OPENROUTER,
            api_key="sk-test",
            model="qwen3-32b",
        )
        with patch(
            "src.generation.providers.openrouter.AsyncOpenAI"
        ) as mock_client:
            mock_client.return_value.models.list = AsyncMock(
                return_value=MagicMock()
            )
            provider = create_provider(config)
            result = await provider.health_check()
            assert result is True
