import time
from typing import Any

import httpx


class RerankerService:
    def __init__(
        self,
        endpoint: str = "http://localhost:8011/v1",
        model: str = "Qwen/Qwen3-Reranker",
        api_key: str = "not-needed",
    ) -> None:
        self._endpoint = endpoint.rstrip("/")
        self._model = model
        self._api_key = api_key
        self._client = httpx.AsyncClient(timeout=30.0)

    async def rerank(
        self,
        query: str,
        documents: list[dict[str, Any]],
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        start = time.monotonic()
        texts = [d.get("text", "") for d in documents]

        response = await self._client.post(
            f"{self._endpoint}/rerank",
            json={
                "model": self._model,
                "query": query,
                "documents": texts,
                "top_k": top_k,
            },
            headers={"Authorization": f"Bearer {self._api_key}"},
        )
        response.raise_for_status()
        data = response.json()
        latency = (time.monotonic() - start) * 1000

        results = []
        for item in data.get("results", []):
            idx = item["index"]
            doc = documents[idx]
            results.append(
                {
                    **doc,
                    "rerank_score": item.get("relevance_score", 0.0),
                    "rerank_latency_ms": latency,
                }
            )

        results.sort(key=lambda x: x.get("rerank_score", 0), reverse=True)
        return results[:top_k]

    async def health_check(self) -> bool:
        try:
            response = await self._client.get(f"{self._endpoint}/models")
            return response.status_code == 200
        except Exception:
            return False
