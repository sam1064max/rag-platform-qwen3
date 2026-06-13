from src.context.reconstructor import ContextReconstructor


class TestContextReconstructor:
    def test_reconstruct_single_child(self) -> None:
        reconstructor = ContextReconstructor(max_tokens=1000)
        results = [
            {
                "text": "Hello world.",
                "document_id": "doc1",
                "metadata": {"filename": "test.txt"},
                "score": 0.95,
            }
        ]
        ctx = reconstructor.reconstruct(results)
        assert ctx.token_count > 0
        assert len(ctx.citations) == 1

    def test_reconstruct_multiple_children(self) -> None:
        reconstructor = ContextReconstructor(max_tokens=5000)
        results = [
            {"text": f"Chunk {i}", "document_id": f"doc{i}", "metadata": {}, "score": 0.9}
            for i in range(5)
        ]
        ctx = reconstructor.reconstruct(results)
        assert len(ctx.citations) == 5

    def test_token_budget_enforced(self) -> None:
        reconstructor = ContextReconstructor(max_tokens=10)
        results = [
            {
                "text": "This is a very long chunk " * 100,
                "document_id": "doc1",
                "metadata": {},
                "score": 0.9,
            },
            {
                "text": "Second chunk " * 100,
                "document_id": "doc2",
                "metadata": {},
                "score": 0.8,
            },
        ]
        ctx = reconstructor.reconstruct(results)
        assert ctx.token_count <= 10

    def test_citation_mapping(self) -> None:
        reconstructor = ContextReconstructor()
        results = [
            {
                "text": "Content A",
                "document_id": "doc1",
                "metadata": {"filename": "a.txt"},
                "score": 0.9,
                "rerank_score": 0.85,
            }
        ]
        ctx = reconstructor.reconstruct(results)
        assert ctx.citations[0]["citation_id"] == 1
        assert ctx.citations[0]["document_id"] == "doc1"
