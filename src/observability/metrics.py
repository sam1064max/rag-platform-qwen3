from prometheus_client import Counter, Gauge, Histogram

rag_query_total = Counter(
    "rag_query_total",
    "Total queries received",
    ["status"],
)

rag_query_duration = Histogram(
    "rag_query_duration_ms",
    "Query latency in milliseconds",
    buckets=[100, 250, 500, 1000, 2500, 5000, 10000],
)

rag_retrieval_latency = Histogram(
    "rag_retrieval_latency_ms",
    "Retrieval latency in milliseconds",
    buckets=[10, 25, 50, 100, 250, 500, 1000],
)

rag_reranking_latency = Histogram(
    "rag_reranking_latency_ms",
    "Reranking latency in milliseconds",
    buckets=[10, 25, 50, 100, 250, 500],
)

rag_generation_latency = Histogram(
    "rag_generation_latency_ms",
    "Generation latency in milliseconds",
    buckets=[100, 500, 1000, 2500, 5000, 10000, 30000],
)

rag_guardrail_violations = Counter(
    "rag_guardrail_violations_total",
    "Total guardrail violations",
    ["check_type"],
)

rag_tokens_input = Counter(
    "rag_tokens_input_total",
    "Total input tokens",
)

rag_tokens_output = Counter(
    "rag_tokens_output_total",
    "Total output tokens",
)

rag_retrieval_recall = Gauge(
    "rag_retrieval_recall_at_5",
    "Retrieval recall at 5",
)
