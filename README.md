# rag-platform-qwen3

Production-grade, fully self-hosted, open-source Retrieval-Augmented Generation (RAG) platform.

**Stack:** Qwen3 (Embedding-8B, 32B-Instruct, Reranker) · vLLM · Qdrant · MinIO · OpenBao · FastAPI · NeMo Guardrails · Langfuse

## Architecture

```
User → FastAPI → Guardrails → Hybrid Retrieval → Reranking → Context Reconstruction → Generation → Response
                              ├─ Dense (Qdrant)
                              └─ Sparse (BM25) → RRF Fusion
```

## Quick Start

```bash
# Clone
git clone https://github.com/sam1064max/rag-platform-qwen3.git
cd rag-platform-qwen3

# Copy env
cp .env.example .env

# Start infrastructure
docker compose up -d

# Start vLLM (GPU required)
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

Supports multiple backends via pluggable provider abstraction:

| Provider | Type | Config |
|----------|------|--------|
| vLLM (self-hosted) | Default | `provider: vllm` |
| OpenAI-compatible API | External | `provider: openai_compat` |
| OpenRouter | External | `provider: openrouter` |

## Documentation

| Doc | Location |
|-----|----------|
| System Spec | `docs/spec.md` |
| Architecture | `docs/architecture.md` |
| Security | `docs/security.md` |
| Ops Runbooks | `docs/ops/` |

## Development

```bash
uv sync --group dev
make lint
make typecheck
make test
```

## License

MIT
