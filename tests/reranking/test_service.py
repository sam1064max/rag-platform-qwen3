from unittest.mock import AsyncMock, patch

import pytest

from src.reranking.service import RerankerService


class TestRerankerService:
    @pytest.mark.asyncio
    async def test_health_check_success(self) -> None:
        svc = RerankerService(endpoint="http://test:8000/v1")
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_get.return_value = AsyncMock(status_code=200)
            result = await svc.health_check()
            assert result is True

    @pytest.mark.asyncio
    async def test_health_check_failure(self) -> None:
        svc = RerankerService(endpoint="http://test:8000/v1")
        with patch("httpx.AsyncClient.get") as mock_get:
            mock_get.side_effect = Exception("fail")
            result = await svc.health_check()
            assert result is False
