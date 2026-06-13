from dataclasses import dataclass, field
from typing import Any


@dataclass
class ReconstructedContext:
    text: str
    token_count: int
    citations: list[dict[str, Any]] = field(default_factory=list)


class ContextReconstructor:
    def __init__(self, max_tokens: int = 4096) -> None:
        self._max_tokens = max_tokens

    def _count_tokens(self, text: str) -> int:
        try:
            import tiktoken

            enc = tiktoken.get_encoding("cl100k_base")
            return len(enc.encode(text))
        except Exception:
            return len(text.split())

    def reconstruct(
        self,
        child_results: list[dict[str, Any]],
    ) -> ReconstructedContext:
        selected: list[dict[str, Any]] = []
        total_tokens = 0

        for result in child_results:
            parent_text = result.get("parent_text", result.get("text", ""))
            tokens = self._count_tokens(parent_text)

            if total_tokens + tokens > self._max_tokens:
                remaining = self._max_tokens - total_tokens
                if remaining > 100:
                    words = parent_text.split()[:remaining]
                    parent_text = " ".join(words)
                    tokens = remaining
                else:
                    continue

            total_tokens += tokens
            selected.append(result)

        citations = []
        text_parts = []

        for i, item in enumerate(selected):
            chunk_text = item.get("parent_text", item.get("text", ""))
            doc_id = item.get("document_id", "")
            filename = item.get("metadata", {}).get("filename", "")
            score = item.get("rerank_score", item.get("score", 0))

            text_parts.append(f"[{i + 1}] {chunk_text}")

            citations.append(
                {
                    "citation_id": i + 1,
                    "document_id": doc_id,
                    "filename": filename,
                    "text_snippet": chunk_text[:200],
                    "relevance_score": score,
                }
            )

        return ReconstructedContext(
            text="\n\n".join(text_parts),
            token_count=total_tokens,
            citations=citations,
        )
