from dataclasses import dataclass, field
from typing import Any

from src.embeddings.service import EmbeddingService
from src.vectorstore.service import VectorStoreService


@dataclass
class RetrievalResult:
    chunk_id: str
    document_id: str
    text: str
    dense_score: float = 0.0
    sparse_score: float = 0.0
    rrf_score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


class HybridRetriever:
    def __init__(
        self,
        vector_store: VectorStoreService,
        embedding_service: EmbeddingService,
        rrf_k: int = 60,
        top_k: int = 20,
    ) -> None:
        self._vector_store = vector_store
        self._embedding_service = embedding_service
        self._rrf_k = rrf_k
        self._top_k = top_k

    def _rrf(self, results: list[list[RetrievalResult]]) -> list[RetrievalResult]:
        score_map: dict[str, float] = {}
        result_map: dict[str, RetrievalResult] = {}

        for rank_list in results:
            for rank, result in enumerate(rank_list, 1):
                chunk_id = result.chunk_id
                if chunk_id not in result_map:
                    result_map[chunk_id] = result
                score_map[chunk_id] = score_map.get(chunk_id, 0.0) + 1.0 / (
                    self._rrf_k + rank
                )

        sorted_results = sorted(
            score_map.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        for chunk_id, rrf_score in sorted_results[: self._top_k]:
            result_map[chunk_id].rrf_score = rrf_score

        return [result_map[cid] for cid, _ in sorted_results[: self._top_k]]

    async def search(
        self,
        query: str,
        top_k: int | None = None,
        filter_: dict[str, Any] | None = None,
    ) -> list[RetrievalResult]:
        k = top_k or self._top_k
        query_embedding = await self._embedding_service.embed(query)

        dense_results = await self._vector_store.search(
            vector=query_embedding.vector,
            top_k=k * 2,
            filter_=filter_,
        )

        dense_list = [
            RetrievalResult(
                chunk_id=r.chunk_id,
                document_id=r.document_id,
                text=r.text,
                dense_score=r.score,
                metadata=r.metadata,
            )
            for r in dense_results
        ]

        sparse_list = await self._bm25_search(query, k * 2, filter_)

        return self._rrf([dense_list, sparse_list])

    async def _bm25_search(
        self,
        query: str,
        top_k: int,
        filter_: dict[str, Any] | None = None,
    ) -> list[RetrievalResult]:
        query_terms = query.lower().split()
        results = await self._vector_store.search(
            vector=[0.0] * 4096,
            top_k=top_k * 4,
            filter_=filter_,
        )

        scored: list[RetrievalResult] = []
        for result in results:
            text_lower = result.text.lower()
            score = sum(
                1.0 for term in query_terms if term in text_lower
            ) / max(len(query_terms), 1)

            if score > 0:
                scored.append(
                    RetrievalResult(
                        chunk_id=result.chunk_id,
                        document_id=result.document_id,
                        text=result.text,
                        sparse_score=score,
                        metadata=result.metadata,
                    )
                )

        scored.sort(key=lambda x: x.sparse_score, reverse=True)
        return scored[:top_k]
