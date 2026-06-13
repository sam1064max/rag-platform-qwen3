<p align="center">
  <h1 align="center">rag-platform-qwen3</h1>
  <p align="center">Production-grade, fully self-hosted Agentic AI Platform with RAG, hybrid retrieval, and agent orchestration.</p>
</p>

<p align="center">

<!-- Automated Status -->
<a href="https://github.com/sam1064max/rag-platform-qwen3/actions/workflows/ci.yml"><img src="https://github.com/sam1064max/rag-platform-qwen3/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI"></a>
<a href="https://github.com/sam1064max/rag-platform-qwen3/releases"><img src="https://img.shields.io/github/v/release/sam1064max/rag-platform-qwen3" alt="Release"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green" alt="License"></a>

</p>

<p align="center">

<!-- Documentation -->
<a href="docs/architecture.md"><img src="https://img.shields.io/badge/architecture-blue" alt="Architecture"></a>
<a href="docs/spec.md"><img src="https://img.shields.io/badge/API-docs-blue" alt="API Docs"></a>
<a href="docs/security.md"><img src="https://img.shields.io/badge/security-blue" alt="Security"></a>
<a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/contributing-blue" alt="Contributing"></a>
<a href="CHANGELOG.md"><img src="https://img.shields.io/badge/changelog-blue" alt="Changelog"></a>

</p>

<p align="center">

<!-- Architecture Evidence -->
<a href="docs/architecture.md#14-agent-runtime-architecture"><img src="https://img.shields.io/badge/agent--runtime-LangGraph-5851D8" alt="Agent Runtime"></a>
<a href="docs/architecture.md#8-retrieval-sequence-diagram"><img src="https://img.shields.io/badge/retrieval-hybrid--search-00BCD4" alt="Retrieval System"></a>
<a href="docs/security.md"><img src="https://img.shields.io/badge/guardrails-NeMo-76B900" alt="Guardrails"></a>
<a href="docs/architecture.md#11-observability-architecture"><img src="https://img.shields.io/badge/observability-OTel--Prometheus-60E6D8" alt="Observability"></a>
<a href="docs/spec.md#7-evaluation-requirements"><img src="https://img.shields.io/badge/evaluation-RAGAS--DeepEval-E91E63" alt="Evaluation"></a>

</p>

<p align="center">

<!-- Reports & Operational -->
<a href="docs/security.md#5-threat-model"><img src="https://img.shields.io/badge/security--report-STRIDE-orange" alt="Security Report"></a>
<a href="docs/spec.md#12-acceptance-criteria"><img src="https://img.shields.io/badge/production--readiness-spec-green" alt="Production Readiness"></a>
<a href="/docs"><img src="https://img.shields.io/badge/swagger-ui-docs-85EA7D" alt="Swagger"></a>

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

```text
User → FastAPI → Guardrails → Agent Runtime → Hybrid Retrieval → Reranking → Context → Generation
                              ├─ Planner (plan → act → observe)
                              ├─ Tool Selection
                              └─ Human-in-the-loop
                                ├─ Dense (Qdrant)
                                └─ Sparse (BM25) → RRF Fusion
```

See [`docs/architecture.md`](docs/architecture.md) for full system architecture.

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

| Doc | Description |
|-----|-------------|
| [`docs/spec.md`](docs/spec.md) | System specification and requirements |
| [`docs/architecture.md`](docs/architecture.md) | Architecture diagrams and design decisions |
| [`docs/security.md`](docs/security.md) | Threat model and security controls |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Development setup and contribution guide |
| [`CHANGELOG.md`](CHANGELOG.md) | Release history |
| [`ROADMAP.md`](ROADMAP.md) | Feature roadmap |

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
