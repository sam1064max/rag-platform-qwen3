from unittest.mock import AsyncMock, patch

import pytest

from src.embeddings.service import EmbeddingService


class TestEmbeddingService:
    @pytest.mark.asyncio
    async def test_health_check_success(self) -> None:
        svc = EmbeddingService(endpoint="http://test:8000/v1")
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_get.return_value = AsyncMock(status_code=200)
            result = await svc.health_check()
            assert result is True

    @pytest.mark.asyncio
    async def test_health_check_failure(self) -> None:
        svc = EmbeddingService(endpoint="http://test:8000/v1")
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_get.side_effect = Exception("fail")
            result = await svc.health_check()
            assert result is False

    def test_batch_size_default(self) -> None:
        svc = EmbeddingService()
        assert svc._batch_size == 32
