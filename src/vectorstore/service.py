from dataclasses import dataclass, field
from typing import Any

from qdrant_client import AsyncQdrantClient
from qdrant_client.http import models


@dataclass
class SearchResult:
    chunk_id: str
    document_id: str
    text: str
    score: float
    metadata: dict[str, Any] = field(default_factory=dict)


class VectorStoreService:
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6334,
        api_key: str = "",
        collection: str = "documents",
        vector_size: int = 4096,
    ) -> None:
        self._client = AsyncQdrantClient(
            host=host,
            port=port,
            api_key=api_key,
            grpc_port=port,
            prefer_grpc=True,
        )
        self._collection = collection
        self._vector_size = vector_size

    async def ensure_collection(self) -> None:
        collections = await self._client.get_collections()
        exists = any(c.name == self._collection for c in collections.collections)
        if not exists:
            await self._client.create_collection(
                collection_name=self._collection,
                vectors_config=models.VectorParams(
                    size=self._vector_size,
                    distance=models.Distance.COSINE,
                    on_disk=True,
                ),
                hnsw_config=models.HNSWConfigDiff(
                    m=16,
                    ef_construct=100,
                ),
                optimizers_config=models.OptimizersConfigDiff(
                    memmap_threshold_kb=20000,
                ),
                quantization_config=models.ScalarQuantization(
                    scalar=models.ScalarQuantizationConfig(
                        type=models.ScalarType.INT8,
                        always_ram=True,
                    ),
                ),
            )

    async def upsert(
        self,
        chunk_id: str,
        vector: list[float],
        payload: dict[str, Any],
    ) -> None:
        await self._client.upsert(
            collection_name=self._collection,
            points=[
                models.PointStruct(
                    id=chunk_id,
                    vector=vector,
                    payload=payload,
                )
            ],
        )

    async def upsert_batch(
        self,
        points: list[tuple[str, list[float], dict[str, Any]]],
    ) -> None:
        point_structs = [
            models.PointStruct(id=pid, vector=vec, payload=pld) for pid, vec, pld in points
        ]
        await self._client.upsert(
            collection_name=self._collection,
            points=point_structs,
        )

    async def search(
        self,
        vector: list[float],
        top_k: int = 20,
        filter_: dict[str, Any] | None = None,
    ) -> list[SearchResult]:
        qdrant_filter = None
        if filter_:
            conditions = []
            for key, value in filter_.items():
                conditions.append(
                    models.FieldCondition(
                        key=key,
                        match=models.MatchValue(value=value),
                    )
                )
            qdrant_filter = models.Filter(
                must=conditions,
            )

        results = await self._client.search(
            collection_name=self._collection,
            query_vector=vector,
            limit=top_k,
            query_filter=qdrant_filter,
            with_payload=True,
        )

        return [
            SearchResult(
                chunk_id=str(result.id),
                document_id=str(result.payload.get("document_id", "")),
                text=str(result.payload.get("text", "")),
                score=result.score,
                metadata={k: v for k, v in result.payload.items() if k != "text"},
            )
            for result in results
        ]

    async def delete_document(self, document_id: str) -> None:
        await self._client.delete(
            collection_name=self._collection,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="document_id",
                            match=models.MatchValue(value=document_id),
                        )
                    ]
                )
            ),
        )

    async def create_snapshot(self) -> str:
        result = await self._client.create_snapshot(
            collection_name=self._collection,
        )
        return result.name

    async def health_check(self) -> bool:
        try:
            await self._client.get_collections()
            return True
        except Exception:
            return False

    async def close(self) -> None:
        await self._client.close()
