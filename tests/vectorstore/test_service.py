from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.vectorstore.service import SearchResult, VectorStoreService


class TestVectorStoreService:
    @pytest.mark.asyncio
    async def test_health_check(self) -> None:
        svc = VectorStoreService(host="test")
        with patch.object(svc._client, "get_collections", AsyncMock(return_value=MagicMock())):
            result = await svc.health_check()
            assert result is True

    @pytest.mark.asyncio
    async def test_health_check_failure(self) -> None:
        svc = VectorStoreService(host="test")
        with patch.object(svc._client, "get_collections", AsyncMock(side_effect=Exception("fail"))):
            result = await svc.health_check()
            assert result is False

    def test_search_result_creation(self) -> None:
        result = SearchResult(
            chunk_id="c1",
            document_id="d1",
            text="test text",
            score=0.95,
            metadata={"source": "test"},
        )
        assert result.chunk_id == "c1"
        assert result.score == 0.95
