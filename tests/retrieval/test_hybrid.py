from src.retrieval.hybrid import RetrievalResult


class TestRetrievalResult:
    def test_default_scores(self) -> None:
        r = RetrievalResult(chunk_id="c1", document_id="d1", text="hello")
        assert r.dense_score == 0.0
        assert r.sparse_score == 0.0
        assert r.rrf_score == 0.0

    def test_metadata(self) -> None:
        r = RetrievalResult(
            chunk_id="c1",
            document_id="d1",
            text="hello",
            metadata={"key": "val"},
        )
        assert r.metadata["key"] == "val"

    def test_rrf_score_ordering(self) -> None:
        r1 = RetrievalResult(chunk_id="c1", document_id="d1", text="a", rrf_score=0.9)
        r2 = RetrievalResult(chunk_id="c2", document_id="d2", text="b", rrf_score=0.5)
        items = [r2, r1]
        items.sort(key=lambda x: x.rrf_score, reverse=True)
        assert items[0].chunk_id == "c1"
