# rag-platform-qwen3

[![CI](https://github.com/sam1064max/rag-platform-qwen3/actions/workflows/ci.yml/badge.svg)](https://github.com/sam1064max/rag-platform-qwen3/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.13-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Release](https://img.shields.io/github/v/release/sam1064max/rag-platform-qwen3)](https://github.com/sam1064max/rag-platform-qwen3/releases)
[![Coverage](https://codecov.io/gh/sam1064max/rag-platform-qwen3/branch/main/graph/badge.svg)](https://codecov.io/gh/sam1064max/rag-platform-qwen3)

Production-grade, fully self-hosted, open-source Retrieval-Augmented Generation (RAG) platform.

**Stack:** Qwen3 (Embedding-8B, 32B-Instruct, Reranker) · vLLM · Qdrant · MinIO · OpenBao · FastAPI · NeMo Guardrails · Langfuse · Prometheus · Grafana

## Architecture

```
User → FastAPI → Guardrails → Hybrid Retrieval → Reranking → Context Reconstruction → Generation → Response
                              ├─ Dense (Qdrant)
                              └─ Sparse (BM25) → RRF Fusion
```

## Features

- **Hybrid Search** — Dense retrieval + BM25 + RRF fusion + reranking
- **Parent-Child Chunking** — 1800/350 token hierarchy with context reconstruction
- **LLM Provider Abstraction** — vLLM (self-hosted), OpenAI-compatible API, OpenRouter
- **Guardrails** — Prompt injection, PII, toxicity, citation verification
- **Secrets Management** — OpenBao with mTLS, auto-rotation, audit logging
- **Observability** — OpenTelemetry, Langfuse tracing, Prometheus metrics, Grafana dashboards
- **Evaluation** — RAGAS + DeepEval with golden datasets (faithfulness, recall, precision)
- **Containerized** — Docker Compose, multi-stage builds, non-root, health checks

## Quick Start

```bash
git clone https://github.com/sam1064max/rag-platform-qwen3.git
cd rag-platform-qwen3

cp .env.example .env

docker compose up -d
docker compose -f docker/vllm/docker-compose.gpu.yml up -d
```

## Deploy Options

| Target | Method |
|--------|--------|
| VPS | Docker Compose |
| Proxmox | Docker Compose + LXC |
| Bare Metal | Docker Compose |
| Kubernetes | K8s manifests (planned) |

## LLM Providers

| Provider | Type | Config |
|----------|------|--------|
| vLLM (self-hosted) | Default | `provider: vllm` |
| OpenAI-compatible API | External | `provider: openai_compat` |
| OpenRouter | External | `provider: openrouter` |

## Project Status

| Metric | Status |
|--------|--------|
| CI Pipeline | ✅ Passing |
| Test Coverage | 90%+ |
| Type Checking | mypy strict |
| Code Quality | ruff |
| Security Scanning | Trivy |
| SBOM | SPDX |
| Latest Release | v1.0.0 |

## Documentation

| Doc | Location |
|-----|----------|
| System Spec | `docs/spec.md` |
| Architecture | `docs/architecture.md` |
| Security | `docs/security.md` |
| Ops Runbooks | `docs/ops/runbooks.md` |
| Disaster Recovery | `docs/ops/disaster_recovery.md` |

## Development

```bash
uv sync --dev
make lint
make typecheck
make test
```

## Release History

- **v1.0.0** (2026-06-13) — Initial production release. Full RAG pipeline with guardrails, evaluation, observability, and CI/CD.

## License

MIT — see [LICENSE](LICENSE) for details.
