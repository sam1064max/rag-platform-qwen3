from src.chunking.engine import ChunkingEngine, ChunkType


class TestChunkingEngine:
    def test_short_text_creates_single_parent(self) -> None:
        engine = ChunkingEngine(parent_size=100, child_size=50)
        text = "Short text."
        chunks, _relations = engine.chunk(text, "doc-1")
        assert len(chunks) >= 1
        assert chunks[0].chunk_type == ChunkType.PARENT

    def test_long_text_creates_multiple_chunks(self) -> None:
        engine = ChunkingEngine(parent_size=50, child_size=20)
        text = " ".join(["word"] * 200)
        chunks, _relations = engine.chunk(text, "doc-1")
        assert len(chunks) > 1
        assert any(c.chunk_type == ChunkType.CHILD for c in chunks)

    def test_relations_are_consistent(self) -> None:
        engine = ChunkingEngine(parent_size=100, child_size=30)
        text = " ".join(["word"] * 300)
        chunks, relations = engine.chunk(text, "doc-1")
        parent_ids = {c.chunk_id for c in chunks if c.chunk_type == ChunkType.PARENT}
        child_ids = {c.chunk_id for c in chunks if c.chunk_type == ChunkType.CHILD}
        for rel in relations:
            assert rel.parent_id in parent_ids
            assert rel.child_id in child_ids

    def test_token_count_positive(self) -> None:
        engine = ChunkingEngine()
        text = "Hello world. This is a test document."
        chunks, _ = engine.chunk(text, "doc-1")
        for chunk in chunks:
            assert chunk.token_count > 0

    def test_document_id_preserved(self) -> None:
        engine = ChunkingEngine(parent_size=100, child_size=50)
        text = "Test document content here."
        chunks, _ = engine.chunk(text, "doc-42")
        for chunk in chunks:
            assert chunk.document_id == "doc-42"

    def test_position_ordering(self) -> None:
        engine = ChunkingEngine(parent_size=100, child_size=50)
        text = " ".join(["word"] * 500)
        chunks, _ = engine.chunk(text, "doc-1")
        parents = [c for c in chunks if c.chunk_type == ChunkType.PARENT]
        positions = [c.position for c in parents]
        assert positions == sorted(positions)
