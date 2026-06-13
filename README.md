<p align="center">
  <h1 align="center">rag-platform-qwen3</h1>
  <p align="center">Production-grade, fully self-hosted Agentic AI Platform with RAG, hybrid retrieval, and agent orchestration.</p>
</p>

<p align="center">

<!-- Build & Quality -->
<a href="https://github.com/sam1064max/rag-platform-qwen3/actions/workflows/ci.yml"><img src="https://github.com/sam1064max/rag-platform-qwen3/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI" style="flat-square"></a>
<a href="https://codecov.io/gh/sam1064max/rag-platform-qwen3"><img src="https://codecov.io/gh/sam1064max/rag-platform-qwen3/branch/main/graph/badge.svg" alt="Coverage" style="flat-square"></a>
<a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-3.13-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License"></a>
<a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/badge/ruff-checked-blue?style=flat-square&logo=ruff&logoColor=white" alt="Ruff"></a>
<a href="https://mypy-lang.org/"><img src="https://img.shields.io/badge/mypy-strict-blue?style=flat-square" alt="MyPy"></a>
<a href="https://pre-commit.com/"><img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=flat-square" alt="Pre-Commit"></a>

</p>

<p align="center">

<!-- Security -->
<a href="https://github.com/aquasecurity/trivy"><img src="https://img.shields.io/badge/trivy-passing-orange?style=flat-square&logo=trivy&logoColor=white" alt="Trivy"></a>
<a href="docs/architecture.md"><img src="https://img.shields.io/badge/SBOM-SPDX-orange?style=flat-square" alt="SBOM"></a>
<a href="docs/security.md"><img src="https://img.shields.io/badge/secrets-no--hardcoded-orange?style=flat-square" alt="No Hardcoded Secrets"></a>

</p>

<p align="center">

<!-- Release -->
<a href="https://github.com/sam1064max/rag-platform-qwen3/releases"><img src="https://img.shields.io/github/v/release/sam1064max/rag-platform-qwen3?style=flat-square" alt="Release"></a>
<a href="https://github.com/sam1064max/rag-platform-qwen3/releases"><img src="https://img.shields.io/badge/semver-2.0.0-blue?style=flat-square" alt="SemVer"></a>
<a href="CHANGELOG.md"><img src="https://img.shields.io/badge/changelog-kept--up--to--date-blue?style=flat-square" alt="Changelog"></a>

</p>

<p align="center">

<!-- AI Platform Stack -->
<img src="https://img.shields.io/badge/LLM-Qwen3-7B3FA0?style=flat-square&logo=openai&logoColor=white" alt="Qwen3">
<img src="https://img.shields.io/badge/inference-vLLM-3B7A57?style=flat-square" alt="vLLM">
<img src="https://img.shields.io/badge/agents-LangGraph-5851D8?style=flat-square" alt="LangGraph">
<img src="https://img.shields.io/badge/vector--db-Qdrant-E53832?style=flat-square&logo=qdrant&logoColor=white" alt="Qdrant">
<img src="https://img.shields.io/badge/API-FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI">
<img src="https://img.shields.io/badge/memory-Redis-DC382D?style=flat-square&logo=redis&logoColor=white" alt="Redis">
<img src="https://img.shields.io/badge/database-PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">
<img src="https://img.shields.io/badge/messaging-NATS-27AAE1?style=flat-square" alt="NATS">
<img src="https://img.shields.io/badge/gateway-LiteLLM-00D4AA?style=flat-square" alt="LiteLLM">
<img src="https://img.shields.io/badge/guardrails-NeMo-76B900?style=flat-square" alt="NeMo">

</p>

<p align="center">

<!-- Observability -->
<img src="https://img.shields.io/badge/Langfuse-tracing-3D34A1?style=flat-square" alt="Langfuse">
<img src="https://img.shields.io/badge/OpenTelemetry-traces-60E6D8?style=flat-square&logo=opentelemetry&logoColor=white" alt="OpenTelemetry">
<img src="https://img.shields.io/badge/Prometheus-metrics-E6522C?style=flat-square&logo=prometheus&logoColor=white" alt="Prometheus">
<img src="https://img.shields.io/badge/Grafana-dashboards-F46800?style=flat-square&logo=grafana&logoColor=white" alt="Grafana">

</p>

<p align="center">

<!-- Infrastructure -->
<img src="https://img.shields.io/badge/Docker-ready-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker">
<img src="https://img.shields.io/badge/Compose-ready-2496ED?style=flat-square" alt="Compose">
<img src="https://img.shields.io/badge/MinIO-storage-C72C48?style=flat-square" alt="MinIO">
<img src="https://img.shields.io/badge/OpenBao-secrets-FFC107?style=flat-square" alt="OpenBao">
<img src="https://img.shields.io/badge/self--hosted-yes-4CAF50?style=flat-square" alt="Self-Hosted">

</p>

<p align="center">

<!-- Capabilities -->
<img src="https://img.shields.io/badge/agentic--AI-enabled-9C27B0?style=flat-square" alt="Agentic AI">
<img src="https://img.shields.io/badge/RAG-platform-2196F3?style=flat-square" alt="RAG Platform">
<img src="https://img.shields.io/badge/hybrid--search-enabled-00BCD4?style=flat-square" alt="Hybrid Search">
<img src="https://img.shields.io/badge/MLOps-ready-FF5722?style=flat-square" alt="MLOps">
<img src="https://img.shields.io/badge/LLMOps-ready-FF9800?style=flat-square" alt="LLMOps">
<img src="https://img.shields.io/badge/production--ready-yes-4CAF50?style=flat-square" alt="Production Ready">
<img src="https://img.shields.io/badge/open--source-MIT-brightgreen?style=flat-square" alt="Open Source">

</p>

---

## Overview

A production-grade, fully self-hosted, open-source Retrieval-Augmented Generation (RAG) platform with agent orchestration. Query private document collections using Qwen3 LLMs without sending data to third-party services.

**Core capabilities:**
- **Hybrid Retrieval** — Dense (Qdrant) + Sparse (BM25) + RRF fusion + reranking
- **Agent Runtime** — LangGraph-based multi-step reasoning with tool selection
- **Parent-Child Chunking** — 1800/350 token hierarchy with context reconstruction
- **Guardrails** — Prompt injection, PII, toxicity, citation verification
- **Evaluation** — RAGAS + DeepEval with golden datasets
- **Observability** — OpenTelemetry + Langfuse + Prometheus + Grafana

## Architecture

```
User → FastAPI → Guardrails → Agent Runtime → Hybrid Retrieval → Reranking → Context → Generation
                              ├─ Planner (plan → act → observe)
                              ├─ Tool Selection
                              └─ Human-in-the-loop
                                ├─ Dense (Qdrant)
                                └─ Sparse (BM25) → RRF Fusion
```

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

## Documentation

| Doc | Location |
|-----|----------|
| System Spec | [`docs/spec.md`](docs/spec.md) |
| Architecture | [`docs/architecture.md`](docs/architecture.md) |
| Security | [`docs/security.md`](docs/security.md) |
| Badge Strategy | [`docs/readme-badge-strategy.md`](docs/readme-badge-strategy.md) |
| Ops Runbooks | [`docs/ops/runbooks.md`](docs/ops/runbooks.md) |
| Disaster Recovery | [`docs/ops/disaster_recovery.md`](docs/ops/disaster_recovery.md) |

## Development

```bash
uv sync --dev
make lint
make typecheck
make test
```

## Release History

See [`CHANGELOG.md`](CHANGELOG.md) for full release notes.

## License

MIT — see [`LICENSE`](LICENSE) for details.
