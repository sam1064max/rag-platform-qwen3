from dataclasses import dataclass, field
from enum import StrEnum


class ChunkType(StrEnum):
    PARENT = "parent"
    CHILD = "child"


@dataclass
class Chunk:
    chunk_id: str
    document_id: str
    chunk_type: ChunkType
    text: str
    token_count: int
    position: int
    metadata: dict[str, str | int | float] = field(default_factory=dict)


@dataclass
class ChunkRelation:
    parent_id: str
    child_id: str
    position: int


class ChunkingEngine:
    def __init__(
        self,
        parent_size: int = 1800,
        child_size: int = 350,
        overlap: int = 50,
    ) -> None:
        self._parent_size = parent_size
        self._child_size = child_size
        self._overlap = overlap

    def _count_tokens(self, text: str) -> int:
        import tiktoken

        try:
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        except Exception:
            return len(text.split())

    def _split_into_sentences(self, text: str) -> list[str]:
        import re

        sentences = re.split(r"(?<=[.!?])\s+", text)
        return [s.strip() for s in sentences if s.strip()]

    def _chunk_by_tokens(self, text: str, max_tokens: int, overlap: int) -> list[str]:
        import tiktoken

        try:
            encoding = tiktoken.get_encoding("cl100k_base")
            tokens = encoding.encode(text)
        except Exception:
            tokens = text.split()

        if len(tokens) <= max_tokens:
            return [text]

        chunks: list[str] = []
        start = 0

        while start < len(tokens):
            end = min(start + max_tokens, len(tokens))
            chunk_tokens = tokens[start:end]

            try:
                chunk_text = encoding.decode(chunk_tokens)
            except Exception:
                chunk_text = " ".join(chunk_tokens)

            chunks.append(chunk_text)
            start += max_tokens - overlap

        return chunks

    def chunk(
        self,
        text: str,
        document_id: str,
        metadata: dict[str, str | int | float] | None = None,
    ) -> tuple[list[Chunk], list[ChunkRelation]]:
        import uuid

        metadata = metadata or {}
        total_tokens = self._count_tokens(text)

        parent_chunks = self._chunk_by_tokens(text, self._parent_size, self._overlap)

        chunks: list[Chunk] = []
        relations: list[ChunkRelation] = []

        for parent_idx, parent_text in enumerate(parent_chunks):
            parent_id = str(uuid.uuid4())
            parent_tokens = self._count_tokens(parent_text)

            chunks.append(
                Chunk(
                    chunk_id=parent_id,
                    document_id=document_id,
                    chunk_type=ChunkType.PARENT,
                    text=parent_text,
                    token_count=parent_tokens,
                    position=parent_idx,
                    metadata={
                        **metadata,
                        "total_document_tokens": total_tokens,
                    },
                )
            )

            child_texts = self._chunk_by_tokens(parent_text, self._child_size, 0)

            for child_idx, child_text in enumerate(child_texts):
                child_id = str(uuid.uuid4())
                child_tokens = self._count_tokens(child_text)

                chunks.append(
                    Chunk(
                        chunk_id=child_id,
                        document_id=document_id,
                        chunk_type=ChunkType.CHILD,
                        text=child_text,
                        token_count=child_tokens,
                        position=child_idx,
                        metadata={
                            "parent_id": parent_id,
                            "parent_position": parent_idx,
                        },
                    )
                )

                relations.append(
                    ChunkRelation(
                        parent_id=parent_id,
                        child_id=child_id,
                        position=child_idx,
                    )
                )

        return chunks, relations
