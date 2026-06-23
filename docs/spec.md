# System Specification: rag-platform-qwen3

## 1. Business Objectives

### 1.1 Primary Objective
Build a production-grade, fully self-hosted, open-source Retrieval-Augmented Generation (RAG) platform that enables organizations to query their private document collections using LLMs without sending data to third-party services.

### 1.2 Strategic Goals

| Goal | Description |
|------|-------------|
| Data Sovereignty | All data processing, storage, and inference occurs on owned infrastructure |
| Operational Autonomy | Zero dependency on proprietary SaaS for any critical path |
| Vertical Scalability | Handle 10K → 1M+ documents with predictable resource scaling |
| Production Readiness | Meet enterprise SLOs for latency, availability, and accuracy |
| Extensibility | Pluggable architecture for custom retrievers, rerankers, and generators |

### 1.3 Success Metrics

| Metric | Target |
|--------|--------|
| Query latency (p95) | < 5s end-to-end |
| Retrieval recall@5 | > 0.90 |
| Answer faithfulness | > 0.85 |
| System availability | 99.5% (excluding model serving) |
| Documents ingested per hour | > 1000 (PDF equivalent) |

---

## 1.5 Model Input Limitations

### 1.5.1 Image Input Not Supported

The default inference model (`deepseek-v4-flash-free`) does **not** support image inputs. Attempts to pass images (screenshots, scanned PDFs, photos) to the query endpoint will fail:

```
ERROR: Cannot read 'image.png' (this model does not support image input).
```

**Workaround for users:** Extract text from images before querying. Use an external OCR tool (e.g., Tesseract, Amazon Textract) to convert image-based documents to text.

**Future enhancement:** An OCR pipeline could be added as a preprocessing step (P2 priority) to automatically extract text from image-based inputs before passing them to the model.

### 1.5.2 Affected Features

| Feature | Status | Notes |
|---------|--------|-------|
| Text-based queries | Supported | Primary use case |
| Image upload as query input | **Not supported** | Returns error above |
| Scanned PDF query input | **Not supported** | Requires OCR preprocessing |
| Screenshot as query context | **Not supported** | Requires OCR preprocessing |

---

## 2. Functional Requirements

### 2.1 Document Ingestion

| ID | Requirement | Priority |
|----|-------------|----------|
| F-01 | System shall accept PDF, DOCX, TXT, and Markdown files | P0 |
| F-02 | System shall extract metadata (title, author, date, page count) | P0 |
| F-03 | System shall generate SHA-256 checksums for deduplication | P0 |
| F-04 | System shall support batch upload (1-100 files per request) | P1 |
| F-05 | System shall implement retry with exponential backoff on failure | P0 |
| F-06 | System shall maintain an ingestion audit log | P1 |
| F-07 | System shall support document fingerprinting for content-level dedup | P1 |
| F-08 | System shall handle OCR for scanned PDFs (optional) | P2 |
| F-09 | System shall document that image-only inputs are not supported (text extraction required) | P3 |

### 2.2 Document Chunking

| ID | Requirement | Priority |
|----|-------------|----------|
| F-10 | System shall implement parent-child chunking strategy | P0 |
| F-11 | Parent chunk size: 1800 tokens (±10%) | P0 |
| F-12 | Child chunk size: 350 tokens (±10%) | P0 |
| F-13 | System shall maintain parent-child relationship graph | P0 |
| F-14 | System shall preserve hierarchical metadata (section, subsection) | P0 |
| F-15 | System shall support configurable overlap between chunks | P1 |
| F-16 | System shall provide token budget tracking per document | P1 |

### 2.3 Embedding Generation

| ID | Requirement | Priority |
|----|-------------|----------|
| F-20 | System shall serve Qwen3-Embedding-8B via vLLM | P0 |
| F-21 | System shall support batch embedding (max 32 docs per batch) | P0 |
| F-22 | System shall cache embeddings by content hash | P0 |
| F-23 | System shall emit metrics: embedding latency, batch size, throughput | P1 |
| F-24 | System shall support GPU memory optimization (continuous batching) | P1 |
| F-25 | System shall fall back to CPU with reduced throughput on GPU failure | P2 |

### 2.4 Vector Storage

| ID | Requirement | Priority |
|----|-------------|----------|
| F-30 | System shall store embeddings in Qdrant collections | P0 |
| F-31 | System shall support payload indexing for metadata filtering | P0 |
| F-32 | System shall implement collection-per-tenant isolation | P1 |
| F-33 | System shall support schema migration for collections | P1 |
| F-34 | System shall implement scheduled backup to MinIO | P1 |
| F-35 | System shall support HNSW index configuration per collection | P1 |

### 2.5 Hybrid Retrieval

| ID | Requirement | Priority |
|----|-------------|----------|
| F-40 | System shall implement dense retrieval using Qdrant vector search | P0 |
| F-41 | System shall implement BM25 sparse retrieval | P0 |
| F-42 | System shall combine results using Reciprocal Rank Fusion (RRF) | P0 |
| F-43 | System shall support metadata filtering (date range, doc type, tenant) | P0 |
| F-44 | System shall support query expansion hooks | P2 |
| F-45 | System shall return relevance scores with each result | P1 |

### 2.6 Reranking

| ID | Requirement | Priority |
|----|-------------|----------|
| F-50 | System shall serve Qwen3-Reranker via vLLM | P0 |
| F-51 | System shall rerank top-20 retrieved chunks to top-5 | P0 |
| F-52 | System shall preserve original retrieval scores alongside rerank scores | P1 |
| F-53 | System shall support configurable k values for reranking depth | P1 |

### 2.7 Context Reconstruction

| ID | Requirement | Priority |
|----|-------------|----------|
| F-60 | System shall retrieve child chunks, then reconstruct parent context | P0 |
| F-61 | System shall enforce token budget for context window | P0 |
| F-62 | System shall maintain citation mapping (source doc, page, chunk) | P0 |
| F-63 | System shall support context expansion (siblings, adjacent chunks) | P1 |

### 2.8 Guardrails

| ID | Requirement | Priority |
|----|-------------|----------|
| F-70 | System shall detect prompt injection attempts | P0 |
| F-71 | System shall detect jailbreak attempts | P0 |
| F-72 | System shall detect and redact PII in inputs | P0 |
| F-73 | System shall detect toxic or harmful content | P0 |
| F-74 | System shall validate retrieved sources against access permissions | P1 |
| F-75 | System shall verify citations in generated output | P0 |
| F-76 | System shall detect hallucinated content (unsubstantiated claims) | P1 |
| F-77 | System shall detect PII leakage in generated output | P0 |

### 2.9 Answer Generation

| ID | Requirement | Priority |
|----|-------------|----------|
| F-80 | System shall serve Qwen3-32B-Instruct via vLLM (default) | P0 |
| F-80a | System shall support provider abstraction for LLM backends | P0 |
| F-80b | System shall support OpenAI-compatible API providers | P1 |
| F-80c | System shall support OpenRouter as an inference provider | P1 |
| F-80d | Providers shall be configurable via OpenBao secrets | P0 |
| F-80e | Provider selection shall be per-request or per-tenant | P2 |
| F-81 | System shall support streaming responses | P0 |
| F-82 | System shall support structured output (JSON mode) | P1 |
| F-83 | System shall enforce citation inclusion in generated answers | P0 |
| F-84 | System shall validate response structure before returning | P1 |

### 2.10 API Layer

| ID | Requirement | Priority |
|----|-------------|----------|
| F-90 | POST /ingest - Upload and process documents | P0 |
| F-91 | POST /query - Submit question and receive answer | P0 |
| F-92 | GET /health - Liveness probe | P0 |
| F-93 | GET /ready - Readiness probe | P0 |
| F-94 | GET /metrics - Prometheus metrics endpoint | P0 |
| F-95 | DELETE /documents/{id} - Remove document and its chunks | P1 |
| F-96 | GET /documents/{id} - Retrieve document status and metadata | P1 |

---

## 3. Non-Functional Requirements

### 3.1 Performance

| ID | Requirement | Target |
|----|-------------|--------|
| N-01 | End-to-end query latency (p95) | < 5 seconds |
| N-02 | End-to-end query latency (p99) | < 10 seconds |
| N-03 | Embedding throughput | > 100 docs/minute (GPU) |
| N-04 | Ingestion throughput | > 1000 pages/hour |
| N-05 | Concurrent query support | > 50 simultaneous users |
| N-06 | Streaming TTFB (time to first token) | < 500ms |

### 3.2 Availability

| ID | Requirement | Target |
|----|-------------|--------|
| N-10 | System uptime (API + retrieval) | 99.5% |
| N-11 | Planned maintenance window | Monthly, off-hours |
| N-12 | Recovery time objective (RTO) | < 1 hour |
| N-13 | Recovery point objective (RPO) | < 15 minutes |

### 3.3 Scalability

| ID | Requirement | Target |
|----|-------------|--------|
| N-20 | Document capacity (initial) | 100,000 documents |
| N-21 | Document capacity (target) | 1,000,000+ documents |
| N-22 | Vector index size | < 2x raw embedding size |
| N-23 | Horizontal scaling | Add Qdrant nodes without downtime |

### 3.4 Security

| ID | Requirement | Target |
|----|-------------|--------|
| N-30 | All inter-service communication | mTLS |
| N-31 | Secrets at rest | Encrypted (OpenBao) |
| N-32 | Secrets in transit | TLS 1.3 |
| N-33 | Container images | Non-root user, no CVEs |
| N-34 | Audit logging | All admin operations logged |
| N-35 | Access control | RBAC per collection |

### 3.5 Reliability

| ID | Requirement | Target |
|----|-------------|--------|
| N-40 | Retry strategy | Exponential backoff, max 3 retries |
| N-41 | Circuit breaker | Trip after 5 consecutive failures |
| N-42 | Bulkhead isolation | Separate thread pools per service |
| N-43 | Graceful degradation | Return cached/partial results on failure |

---

## 4. API Contracts

### 4.1 POST /ingest

**Description:** Upload documents for processing and indexing.

```
POST /api/v1/ingest
Content-Type: multipart/form-data
Authorization: Bearer <token>
```

**Request:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| files | File[] | Yes | One or more documents (PDF, DOCX, TXT, MD) |
| tenant_id | String | No | Tenant identifier for multi-tenancy |
| metadata | JSON | No | Custom metadata key-value pairs |

**Response 202:**

```json
{
  "job_id": "uuid",
  "documents": [
    {
      "document_id": "uuid",
      "filename": "report.pdf",
      "status": "queued",
      "checksum": "sha256-hash",
      "size_bytes": 1048576
    }
  ],
  "total_documents": 1,
  "total_size_bytes": 1048576
}
```

**Response 422:**

```json
{
  "detail": [
    {
      "loc": ["body", "files"],
      "msg": "Unsupported file type: .exe",
      "type": "value_error"
    }
  ]
}
```

### 4.2 POST /query

**Description:** Submit a question and receive an AI-generated answer with citations.

```
POST /api/v1/query
Content-Type: application/json
Authorization: Bearer <token>
```

**Request:**

```json
{
  "query": "What is the process for data access requests?",
  "tenant_id": "acme-corp",
  "filters": {
    "date_from": "2024-01-01",
    "date_to": "2024-12-31",
    "doc_types": ["policy", "procedure"]
  },
  "top_k": 5,
  "stream": false
}
```

**Response 200 (non-streaming):**

```json
{
  "query_id": "uuid",
  "answer": "The data access request process requires...",
  "citations": [
    {
      "document_id": "uuid",
      "filename": "data-governance-policy.pdf",
      "page": 3,
      "chunk_text": "Data access requests must be submitted...",
      "relevance_score": 0.94,
      "rerank_score": 0.87
    }
  ],
  "metrics": {
    "retrieval_time_ms": 152,
    "reranking_time_ms": 45,
    "generation_time_ms": 2340,
    "total_tokens": 1456,
    "input_tokens": 1024,
    "output_tokens": 432
  },
  "guardrail_results": {
    "input_check": "passed",
    "retrieval_check": "passed",
    "output_check": "passed"
  }
}
```

**Response 200 (streaming):**

```
data: {"type": "start", "query_id": "uuid"}
data: {"type": "token", "text": "The"}
data: {"type": "token", "text": " data"}
data: {"type": "token", "text": " access"}
data: {"type": "done", "citations": [...], "metrics": {...}}
```

### 4.3 GET /health

**Description:** Liveness probe for orchestration platforms.

```
GET /api/v1/health
```

**Response 200:**

```json
{
  "status": "healthy",
  "timestamp": "2026-06-13T11:00:00Z",
  "version": "1.0.0",
  "components": {
    "qdrant": "connected",
    "minio": "connected",
    "openbao": "connected",
    "vllm-embed": "ready",
    "vllm-rerank": "ready",
    "vllm-generate": "ready"
  }
}
```

### 4.4 GET /ready

**Description:** Readiness probe. Indicates the service can accept traffic.

```
GET /api/v1/ready
```

**Response 200:**

```json
{
  "ready": true,
  "timestamp": "2026-06-13T11:00:00Z"
}
```

### 4.5 GET /metrics

**Description:** Prometheus metrics endpoint.

```
GET /api/v1/metrics
```

**Response 200:** Prometheus text format.

### 4.6 DELETE /documents/{id}

**Description:** Remove a document and all associated chunks.

```
DELETE /api/v1/documents/{document_id}
Authorization: Bearer <token>
```

**Response 200:**

```json
{
  "document_id": "uuid",
  "status": "deleted",
  "chunks_removed": 42
}
```

---

## 5. Security Requirements

### 5.1 Authentication

| ID | Requirement |
|----|-------------|
| S-01 | API access requires Bearer token authentication |
| S-02 | Tokens are issued by the platform auth service |
| S-03 | Token lifetime: max 24 hours, refreshable |
| S-04 | All inter-service communication uses mTLS |
| S-05 | OpenBao issues short-lived certificates for mTLS |

### 5.2 Authorization

| ID | Requirement |
|----|-------------|
| S-10 | RBAC enforced at API gateway level |
| S-11 | Tenant isolation at collection level |
| S-12 | Role definitions: admin, operator, reader |
| S-13 | All access decisions logged for audit |

### 5.3 Data Protection

| ID | Requirement |
|----|-------------|
| S-20 | Secrets stored encrypted in OpenBao |
| S-21 | Data at rest encrypted (MinIO SSE-S3) |
| S-22 | Data in transit encrypted (TLS 1.3) |
| S-23 | PII detected and redacted before storage |
| S-24 | Document content never logged |

### 5.4 Secrets Management

| ID | Requirement |
|----|-------------|
| S-30 | All secrets managed via OpenBao |
| S-31 | No secrets in environment variables in production |
| S-32 | Secret rotation supported with zero downtime |
| S-33 | Access audit trail for every secret read |

---

## 6. Guardrail Requirements

### 6.1 Input Guardrails

| ID | Guardrail | Action |
|----|-----------|--------|
| G-01 | Prompt injection detection | Block request, log alert |
| G-02 | Jailbreak detection | Block request, log alert |
| G-03 | PII detection | Redact PII, log detection |
| G-04 | Toxicity detection | Block request, log alert |
| G-05 | Query length validation | Truncate or reject |

### 6.2 Retrieval Guardrails

| ID | Guardrail | Action |
|----|-----------|--------|
| G-10 | Source validation | Filter unapproved sources |
| G-11 | Authorization check | Verify tenant access |
| G-12 | Metadata validation | Enforce filter constraints |
| G-13 | Staleness check | Flag or exclude outdated documents |

### 6.3 Output Guardrails

| ID | Guardrail | Action |
|----|-----------|--------|
| G-20 | Citation verification | Verify each claim cites a retrieved chunk |
| G-21 | Hallucination detection | Flag unsubstantiated claims |
| G-22 | PII leakage detection | Redact or block output |
| G-23 | Response validation | Enforce structure and format |
| G-24 | Toxicity check | Block harmful output |

### 6.4 Guardrail Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| Input guardrail mode | `enforce` | `enforce`, `log`, or `disable` |
| Output guardrail mode | `enforce` | `enforce`, `log`, or `disable` |
| PII redaction strategy | `mask` | `mask`, `replace`, or `block` |
| Max query length | 4096 chars | Reject queries exceeding this |
| Citation threshold | 0.70 | Minimum rerank score for citation |

---

## 7. Evaluation Requirements

### 7.1 Evaluation Metrics

| Metric | Tool | Target | Description |
|--------|------|--------|-------------|
| Faithfulness | RAGAS | > 0.85 | Answers are grounded in retrieved context |
| Answer Relevancy | RAGAS | > 0.90 | Answers address the question |
| Context Precision | RAGAS | > 0.85 | Retrieved chunks are relevant |
| Context Recall | RAGAS | > 0.80 | All needed context is retrieved |
| Answer Correctness | DeepEval | > 0.80 | Answers match ground truth |
| Hallucination Rate | DeepEval | < 5% | Claims not supported by context |
| Retrieval Recall@5 | Custom | > 0.90 | Relevant doc in top 5 |
| MRR (Mean Reciprocal Rank) | Custom | > 0.85 | Rank of first relevant result |
| NDCG@10 | Custom | > 0.80 | Ranking quality |

### 7.2 Evaluation Datasets

| Dataset | Size | Purpose |
|---------|------|---------|
| Golden Dataset | 200 Q/A pairs | Regression testing |
| Adversarial Dataset | 50 queries | Guardrail effectiveness |
| Performance Dataset | 100 queries | Latency benchmarking |

### 7.3 Evaluation Cadence

| Trigger | Action |
|---------|--------|
| Every PR | Run golden dataset evaluation |
| Daily (scheduled) | Full regression suite |
| Weekly | Adversarial evaluation |
| Per release | Full evaluation + report |

---

## 8. Architecture Requirements

### 8.1 System Constraints

| Constraint | Requirement |
|------------|-------------|
| Self-hosted | Zero SaaS dependencies |
| Deployment targets | VPS, Proxmox, Bare Metal, Kubernetes |
| GPU requirement | Minimum 1x A100 80GB (or equivalent) |
| Python version | 3.13+ |
| Package manager | uv |
| Container runtime | Docker + Docker Compose |

### 8.2 Integration Requirements

| Integration | Purpose |
|-------------|---------|
| Qdrant | Vector database for embeddings |
| MinIO | Object storage for documents and backups |
| OpenBao | Secrets management |
| Langfuse | LLM observability and tracing |
| Prometheus + Grafana | Metrics and dashboards |
| OpenTelemetry | Distributed tracing |
| vLLM | LLM inference server |
| NVIDIA NeMo Guardrails | Content safety |

### 8.3 Extensibility

| Extension Point | Mechanism |
|-----------------|-----------|
| Custom retrievers | Plugin interface |
| Custom chunkers | Strategy pattern |
| Custom guardrails | Colang configuration |
| Custom evaluators | Base class inheritance |

---

## 9. Operational Requirements

### 9.1 Deployment

| Requirement | Detail |
|-------------|--------|
| Container orchestration | Docker Compose (default), K8s manifests (optional) |
| Image registry | Local registry or Docker Hub |
| Secret injection | OpenBao sidecar or init container |
| Database migrations | Automated on startup |

### 9.2 Backup and Restore

| Component | Backup Strategy | Frequency |
|-----------|----------------|-----------|
| Qdrant snapshots | MinIO bucket | Hourly |
| MinIO data | Replication / offsite | Daily |
| OpenBao | Raft snapshot | Daily |
| Langfuse | PostgreSQL dump | Daily |
| Configuration | Git (IaC) | Every change |

### 9.3 Monitoring

| Signal | Tool | Purpose |
|--------|------|---------|
| Metrics | Prometheus | System health, performance |
| Logs | Stdout + file rotation | Debugging |
| Traces | OpenTelemetry + Langfuse | Request flow |
| Alerts | Grafana | Incident notification |
| Dashboards | Grafana | Visual monitoring |

### 9.4 Logging

| Requirement | Detail |
|-------------|--------|
| Format | Structured JSON |
| Level | INFO (production), DEBUG (dev) |
| Destination | stdout (container), file (local) |
| Retention | 30 days |
| PII | Never logged |

---

## 10. Service Level Objectives (SLOs)

### 10.1 Performance SLOs

| Metric | Target | Measurement Period | Burn Rate |
|--------|--------|-------------------|-----------|
| p95 query latency | < 5s | 30 days | 2% / month |
| p99 query latency | < 10s | 30 days | 2% / month |
| Streaming TTFB | < 500ms | 7 days | 5% / week |
| Ingestion throughput | > 1000 pages/hr | 7 days | 5% / week |

### 10.2 Accuracy SLOs

| Metric | Target | Measurement Period |
|--------|--------|-------------------|
| Faithfulness | > 0.85 | Per evaluation run |
| Context Recall | > 0.80 | Per evaluation run |
| Retrieval Recall@5 | > 0.90 | Per evaluation run |

### 10.3 Availability SLOs

| Component | Target | Calculation |
|-----------|--------|-------------|
| API Service | 99.5% | (total - downtime) / total minutes |
| Qdrant | 99.9% | Cluster health checks |
| MinIO | 99.9% | Object storage availability |
| vLLM | 99.0% | Model readiness checks |
| OpenBao | 99.95% | Seal status monitoring |

### 10.4 Error Budget

| SLO | Error Budget (Monthly) |
|-----|----------------------|
| 99.5% | 216 minutes |
| 99.0% | 432 minutes |
| 95.0% | 2160 minutes |

---

## 11. Failure Scenarios

### 11.1 Infrastructure Failures

| Scenario | Impact | Mitigation |
|----------|--------|------------|
| GPU failure | Embedding/Generation unavailable | CPU fallback (degraded), alert |
| Disk full | Ingestion/storage failure | Monitoring, auto-cleanup, alert |
| Network partition | Service isolation | Retry, circuit breaker, alert |
| Node failure (K8s) | Pod restart | Replica sets, PDB |
| Power outage | Full system down | UPS, graceful shutdown, recovery |

### 11.2 Service Failures

| Scenario | Impact | Mitigation |
|----------|--------|------------|
| Qdrant down | No retrieval | Read replica, circuit breaker |
| vLLM OOM | Model unresponsive | Graceful restart, resource limits |
| OpenBao sealed | No secrets access | Auto-unseal, HA mode |
| MinIO unavailable | No storage | Caching, circuit breaker |
| Langfuse down | No tracing | Non-blocking telemetry |

### 11.3 Data Failures

| Scenario | Impact | Mitigation |
|----------|--------|------------|
| Corrupt embedding | Wrong retrieval results | Checksum validation |
| Corrupt index | No search results | Snapshot restore |
| Duplicate documents | Bloated context window | Dedup on ingestion |
| Data inconsistency | Mismatched parent-child | Consistency check job |

### 11.4 Security Incidents

| Scenario | Impact | Mitigation |
|----------|--------|------------|
| Secret leak | Credential exposure | Immediate rotation, audit |
| Injection attack | Unauthorized data access | Guardrails, rate limiting |
| DoS attack | Service degradation | Rate limiting, IP blocking |
| Data breach | Confidential data exposed | Encryption, access audit |

---

## 12. Acceptance Criteria

### 12.1 Phase Gates

| Phase | Gate Criteria |
|-------|---------------|
| P0 Repo | Git initialized, docs/repository_strategy.md committed |
| P1 Spec | docs/spec.md covers all sections, committed |
| P2 Arch | docs/architecture.md with all diagrams, committed |
| P3 Bootstrap | uv project initialized, all lint/type checks pass |
| P4 Infra | docker-compose.yml starts all services |
| P5 Security | OpenBao initialized, secrets injectable |
| P6 Ingestion | PDF/DOCX/TXT/MD files indexed successfully |
| P7 Chunking | Parent-child relationships stored correctly |
| P8 Embeddings | Qwen3-Embedding-8B serving via vLLM |
| P9 Vectorstore | Qdrant collections queryable with filters |
| P10 Retrieval | Hybrid search returns ranked results |
| P11 Reranking | Top-20 → top-5 reranking working |
| P12 Context | Reconstructed context within token budget |
| P13 Guardrails | Input/retrieval/output checks passing |
| P14 Generation | Streaming answers with citations |
| P15 API | All endpoints functional, OpenAPI spec valid |
| P16 Eval | RAGAS + DeepEval metrics meet targets |
| P17 Observability | Traces, metrics, logs flowing to dashboards |
| P18 Docker | Images built, scanned, non-root, health checks |
| P19 CI/CD | Pipeline passes lint, test, security, build |
| P20 Tests | Coverage >= 90%, all tests pass |
| P21 Ops | Runbooks complete, DR tested |
| P22 Release | v1.0.0 tagged, changelog complete |

### 12.2 Final Acceptance

| Criterion | Standard |
|-----------|----------|
| Code quality | ruff pass, mypy strict, no TODOs |
| Test coverage | >= 90% |
| Documentation | Complete spec, architecture, runbooks |
| Security review | All findings resolved |
| Performance | SLOs met under load test |
| Deployment | One-command deploy on Docker Compose |
| Observability | All dashboards populated |
| Evaluation | All metrics meet targets |
