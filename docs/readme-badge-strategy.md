# README Badge Strategy

**Date:** 2026-06-13
**Branch:** feature/readme-badges

## Badge Categories

### 1. Build & Quality
Badges that communicate code health and CI status.

| Badge | Source | Style | Rationale |
|-------|--------|-------|-----------|
| CI | GitHub Actions workflow | `flat-square` | Primary build health indicator |
| Coverage | Codecov | `flat-square` | Test coverage quality signal |
| Python | shields.io | `flat-square` | Runtime version requirement |
| License | shields.io | `flat-square` | Legal clarity |
| Ruff | shields.io | `flat-square` | Linter status (code quality) |
| MyPy | shields.io | `flat-square` | Type checking (code correctness) |
| Pre-Commit | shields.io | `flat-square` | Development workflow maturity |

### 2. Security
Badges that communicate security posture.

| Badge | Source | Style | Rationale |
|-------|--------|-------|-----------|
| Trivy | shields.io | `flat-square` | Vulnerability scanning |
| SBOM | shields.io | `flat-square` | Software bill of materials |
| No Hardcoded Secrets | shields.io | `flat-square` | Security policy indicator |

### 3. Release Management
Badges that communicate release maturity.

| Badge | Source | Style | Rationale |
|-------|--------|-------|-----------|
| Release | GitHub Releases | `flat-square` | Latest version |
| SemVer | shields.io | `flat-square` | Versioning discipline |
| Changelog | shields.io | `flat-square` | Release documentation |

### 4. AI Platform Stack
Badges showing the core technology stack.

| Badge | Source | Style | Rationale |
|-------|--------|-------|-----------|
| LLM: Qwen3 | shields.io | `flat-square` | Model family |
| Inference: vLLM | shields.io | `flat-square` | Serving runtime |
| Agents: LangGraph | shields.io | `flat-square` | Agent orchestration |
| Vector DB: Qdrant | shields.io | `flat-square` | Vector storage |
| API: FastAPI | shields.io | `flat-square` | API framework |
| Memory: Redis | shields.io | `flat-square` | Working memory |
| Database: PostgreSQL | shields.io | `flat-square` | Persistent storage |
| Messaging: NATS | shields.io | `flat-square` | Event bus |
| Gateway: LiteLLM | shields.io | `flat-square` | Model gateway |
| Guardrails: NeMo | shields.io | `flat-square` | Content safety |

### 5. Observability
Badges showing observability stack.

| Badge | Source | Style | Rationale |
|-------|--------|-------|-----------|
| Langfuse | shields.io | `flat-square` | LLM tracing |
| OpenTelemetry | shields.io | `flat-square` | Distributed tracing |
| Prometheus | shields.io | `flat-square` | Metrics |
| Grafana | shields.io | `flat-square` | Dashboards |

### 6. Infrastructure
Badges showing deployment infrastructure.

| Badge | Source | Style | Rationale |
|-------|--------|-------|-----------|
| Docker | shields.io | `flat-square` | Container support |
| Compose | shields.io | `flat-square` | Orchestration |
| MinIO | shields.io | `flat-square` | Object storage |
| OpenBao | shields.io | `flat-square` | Secrets management |
| Self-Hosted | shields.io | `flat-square` | Deployment model |

### 7. Capabilities
Badges showing platform capabilities.

| Badge | Source | Style | Rationale |
|-------|--------|-------|-----------|
| Agentic AI | shields.io | `flat-square` | Core capability |
| RAG Platform | shields.io | `flat-square` | Core capability |
| Hybrid Search | shields.io | `flat-square` | Retrieval capability |
| MLOps | shields.io | `flat-square` | Operations maturity |
| LLMOps | shields.io | `flat-square` | LLM operations |
| Production Ready | shields.io | `flat-square` | Deployment readiness |
| Open Source | shields.io | `flat-square` | License model |

## Badge Style Guide

- All badges use `flat-square` style for consistency
- Color scheme follows semantic meaning:
  - Blue: technology/runtime
  - Green: status/quality
  - Orange: security
  - Purple: capabilities
  - Gray: infrastructure
  - Red: alerts (not used in positive badges)

## URL Patterns

```
Static:  https://img.shields.io/badge/{label}-{message}-{color}?style=flat-square
Dynamic: https://img.shields.io/github/{metric}/{owner}/{repo}?style=flat-square
CI:      https://github.com/{owner}/{repo}/actions/workflows/{workflow}/badge.svg
Codecov: https://codecov.io/gh/{owner}/{repo}/branch/main/graph/badge.svg
```
