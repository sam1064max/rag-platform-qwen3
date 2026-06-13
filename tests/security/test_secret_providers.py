import os

import pytest

from src.security.secret_provider import SecretCategory
from src.security.providers.env import EnvProvider


class TestEnvProvider:
    @pytest.mark.asyncio
    async def test_get_secret(self) -> None:
        os.environ["RAG_SECRET_LLM_API_KEY"] = "test-key-123"
        provider = EnvProvider(prefix="RAG_SECRET_")
        secret = await provider.get_secret("llm", "api_key")
        assert secret.key == "api_key"
        assert secret.value == "test-key-123"
        os.environ.pop("RAG_SECRET_LLM_API_KEY", None)

    @pytest.mark.asyncio
    async def test_get_secret_not_found(self) -> None:
        provider = EnvProvider(prefix="RAG_SECRET_")
        with pytest.raises(KeyError, match="not found"):
            await provider.get_secret("nonexistent", "key")

    @pytest.mark.asyncio
    async def test_set_and_delete(self) -> None:
        provider = EnvProvider(prefix="RAG_SECRET_")
        await provider.set_secret("test", "foo", "bar", SecretCategory.API_KEYS)
        assert os.environ.get("RAG_SECRET_TEST_FOO") == "bar"
        await provider.delete_secret("test", "foo")
        assert os.environ.get("RAG_SECRET_TEST_FOO") is None

    @pytest.mark.asyncio
    async def test_health_check(self) -> None:
        provider = EnvProvider()
        assert await provider.health_check() is True

    @pytest.mark.asyncio
    async def test_list_secrets(self) -> None:
        os.environ["RAG_SECRET_DB_PASS"] = "secret1"
        os.environ["RAG_SECRET_DB_USER"] = "secret2"
        provider = EnvProvider(prefix="RAG_SECRET_")
        keys = await provider.list_secrets("db")
        assert "pass" in keys
        assert "user" in keys
        os.environ.pop("RAG_SECRET_DB_PASS", None)
        os.environ.pop("RAG_SECRET_DB_USER", None)


class TestSecretCategory:
    def test_categories(self) -> None:
        assert SecretCategory.LLM_CREDENTIALS.value == "llm"
        assert SecretCategory.DATABASE_CREDENTIALS.value == "database"
        assert SecretCategory.STORAGE_CREDENTIALS.value == "storage"
        assert SecretCategory.API_KEYS.value == "api"
        assert SecretCategory.OBSERVABILITY_TOKENS.value == "observability"
        assert SecretCategory.TLS_CERTIFICATES.value == "tls"
