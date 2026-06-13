from dataclasses import dataclass, field
import time

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential


@dataclass
class EmbeddingResult:
    vector: list[float]
    model: str
    latency_ms: float
    tokens_used: int = 0


class EmbeddingService:
    def __init__(
        self,
        endpoint: str = "http://localhost:8010/v1",
        model: str = "Qwen/Qwen3-Embedding-8B",
        api_key: str = "not-needed",
        batch_size: int = 32,
    ) -> None:
        self._endpoint = endpoint.rstrip("/")
        self._model = model
        self._api_key = api_key
        self._batch_size = batch_size
        self._client = httpx.AsyncClient(timeout=60.0)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
    )
    async def embed(self, text: str) -> EmbeddingResult:
        start = time.monotonic()
        response = await self._client.post(
            f"{self._endpoint}/embeddings",
            json={
                "model": self._model,
                "input": text,
                "encoding_format": "float",
            },
            headers={"Authorization": f"Bearer {self._api_key}"},
        )
        response.raise_for_status()
        data = response.json()
        latency = (time.monotonic() - start) * 1000

        return EmbeddingResult(
            vector=data["data"][0]["embedding"],
            model=data.get("model", self._model),
            latency_ms=latency,
            tokens_used=data.get("usage", {}).get("prompt_tokens", 0),
        )

    async def embed_batch(self, texts: list[str]) -> list[EmbeddingResult]:
        results: list[EmbeddingResult] = []
        for i in range(0, len(texts), self._batch_size):
            batch = texts[i : i + self._batch_size]
            start = time.monotonic()
            response = await self._client.post(
                f"{self._endpoint}/embeddings",
                json={
                    "model": self._model,
                    "input": batch,
                    "encoding_format": "float",
                },
                headers={"Authorization": f"Bearer {self._api_key}"},
            )
            response.raise_for_status()
            data = response.json()
            latency = (time.monotonic() - start) * 1000

            for item in data["data"]:
                results.append(
                    EmbeddingResult(
                        vector=item["embedding"],
                        model=data.get("model", self._model),
                        latency_ms=latency / len(batch),
                    )
                )
        return results

    async def health_check(self) -> bool:
        try:
            response = await self._client.get(f"{self._endpoint}/models")
            return response.status_code == 200
        except Exception:
            return False
