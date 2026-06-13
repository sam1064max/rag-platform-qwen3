from src.observability.metrics import (
    rag_query_duration,
    rag_query_total,
    rag_guardrail_violations,
    rag_tokens_input,
    rag_tokens_output,
    rag_retrieval_recall,
)


class TestMetrics:
    def test_query_counter(self) -> None:
        rag_query_total.labels(status="success").inc()
        val = dict(rag_query_total.collect()[0].samples)
        matching = [v for name, v in val.items() if "success" in str(name)]
        assert len(matching) >= 1

    def test_histogram_exists(self) -> None:
        assert rag_query_duration._name == "rag_query_duration_ms"

    def test_guardrail_counter(self) -> None:
        rag_guardrail_violations.labels(check_type="injection").inc()
        val = dict(rag_guardrail_violations.collect()[0].samples)
        matching = [v for name, v in val.items() if "injection" in str(name)]
        assert len(matching) >= 1

    def test_token_counters(self) -> None:
        rag_tokens_input.inc(100)
        rag_tokens_output.inc(50)
        input_vals = dict(rag_tokens_input.collect()[0].samples)
        output_vals = dict(rag_tokens_output.collect()[0].samples)
        total_input = sum(rag_tokens_input.collect()[0].samples[0])
        assert total_input >= 1

    def test_retrieval_gauge(self) -> None:
        rag_retrieval_recall.set(0.92)
        val = list(rag_retrieval_recall.collect()[0].samples[0])[2]
        assert val == 0.92
