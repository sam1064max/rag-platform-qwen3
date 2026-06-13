from src.api.models import (
    HealthResponse,
    IngestResponse,
    QueryRequest,
    QueryResponse,
    ReadyResponse,
)


class TestModels:
    def test_health_response(self) -> None:
        resp = HealthResponse(status="healthy", components={"qdrant": "connected"})
        assert resp.status == "healthy"
        assert resp.components["qdrant"] == "connected"

    def test_ready_response(self) -> None:
        resp = ReadyResponse(ready=True)
        assert resp.ready is True

    def test_query_request(self) -> None:
        req = QueryRequest(query="test query", top_k=5)
        assert req.query == "test query"
        assert req.top_k == 5
        assert req.stream is False

    def test_query_response(self) -> None:
        resp = QueryResponse(
            query_id="q-1",
            answer="test answer",
            citations=[],
            metrics={"latency_ms": 100},
            guardrail_results={"check": "passed"},
        )
        assert resp.query_id == "q-1"
        assert resp.answer == "test answer"

    def test_ingest_response(self) -> None:
        resp = IngestResponse(
            job_id="j-1",
            documents=[],
            total_documents=0,
            total_size_bytes=0,
        )
        assert resp.job_id == "j-1"
        assert resp.total_documents == 0
