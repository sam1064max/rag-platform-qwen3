# Changelog

## v1.0.0 (2026-06-13)

### Features

- **Ingestion:** PDF, DOCX, TXT, Markdown parsing with metadata extraction
- **Chunking:** Hierarchical parent-child chunking (1800/350 tokens)
- **Embeddings:** Qwen3-Embedding-8B serving via vLLM with batch support
- **Vector Store:** Qdrant with HNSW indexing and scalar quantization
- **Hybrid Retrieval:** Dense + BM25 search with RRF fusion
- **Reranking:** Qwen3-Reranker (top-20 to top-5)
- **Context Reconstruction:** Token-budgeted parent reconstruction with citations
- **Guardrails:** Input/output safety checks (PII, injection, citation verification)
- **Generation:** Qwen3-32B-Instruct with streaming and structured output
- **LLM Providers:** vLLM, OpenAI-compatible API, OpenRouter abstraction
- **API:** FastAPI with /ingest, /query, /health, /ready, /metrics
- **Security:** OpenBao secrets management with mTLS
- **Observability:** OpenTelemetry, Langfuse, Prometheus, Grafana
- **Evaluation:** RAGAS + DeepEval with golden dataset support
- **Infrastructure:** Docker Compose with all services, GPU support
- **CI/CD:** Gitea Actions with lint, test, security scanning, build

### Documentation

- System specification (docs/spec.md)
- Architecture with TDRs (docs/architecture.md)
- Security guide (docs/security.md)
- Operations runbooks (docs/ops/)
- Repository strategy (docs/repository_strategy.md)

### Quality

- Test coverage: 90%+
- Type checking: mypy strict
- Linting: ruff
- Security scanning: Trivy
- SBOM generation
