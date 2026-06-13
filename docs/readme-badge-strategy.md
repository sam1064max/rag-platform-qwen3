# README Badge Strategy

**Date:** 2026-06-13
**Updated:** 2026-06-13 (refactor from marketing to evidence-driven)
**Branch:** feature/readme-badge-refactor

## Principle

Every badge must answer: **"What happens when someone clicks this?"**

If the answer is "nothing useful", the badge is removed.

## Badge Categories

### 1. Automated Status (3 badges)

Badges linked to real-time CI/CD systems. No manual claims.

| Badge | Links To | Evidence |
|-------|----------|----------|
| CI | GitHub Actions workflow | Build status, test results |
| Coverage | Codecov dashboard | Test coverage percentage |
| Release | GitHub Releases | Latest tagged version |

### 2. Documentation (5 badges)

Badges linking to project documentation files.

| Badge | Links To | Content |
|-------|----------|---------|
| License | LICENSE | MIT license file |
| Architecture | docs/architecture.md | System architecture |
| API Docs | docs/spec.md | API contracts |
| Security | docs/security.md | Threat model |
| Contributing | CONTRIBUTING.md | Development guide |
| Changelog | CHANGELOG.md | Release history |

### 3. Architecture Evidence (5 badges)

Badges linking to specific architecture sections describing implemented capabilities.

| Badge | Links To | Evidence |
|-------|----------|----------|
| Agent Runtime | docs/architecture.md#14 | LangGraph StateGraph design |
| Retrieval System | docs/architecture.md#8 | Hybrid retrieval sequence |
| Guardrails | docs/security.md | Threat model + guardrail config |
| Observability | docs/architecture.md#11 | OTel + Prometheus + Grafana |
| Evaluation | docs/spec.md#7 | RAGAS + DeepEval metrics |

### 4. Reports (2 badges)

Badges linking to analysis and readiness evidence.

| Badge | Links To | Evidence |
|-------|----------|----------|
| Security Report | docs/security.md#5 | STRIDE threat model |
| Production Readiness | docs/spec.md#12 | Acceptance criteria |

### 5. Operational (1 badge)

Badges linking to live operational interfaces.

| Badge | Links To | Destination |
|-------|----------|-------------|
| Swagger UI | /docs | FastAPI OpenAPI docs |

## Badge Style

- Default shields.io style (no `flat-square`)
- Color follows semantic meaning:
  - Blue: documentation
  - Green: quality/license
  - Orange: security
  - Purple: capabilities
  - Cyan: retrieval/observability
  - Red-pink: evaluation

## URL Patterns

```
Static:    https://img.shields.io/badge/{label}-{message}-{color}
Dynamic:   https://img.shields.io/github/{metric}/{owner}/{repo}
CI:        https://github.com/{owner}/{repo}/actions/workflows/{workflow}/badge.svg
Codecov:   https://codecov.io/gh/{owner}/{repo}/branch/main/graph/badge.svg
```

## Removed Badges (with reasons)

| Badge | Reason |
|-------|--------|
| Qwen3, vLLM, FastAPI | Technology logos with no destination |
| Redis, PostgreSQL, NATS, LiteLLM | Not implemented yet |
| NeMo, Langfuse, OpenTelemetry, Prometheus, Grafana | Technology logos with no live evidence |
| Docker, Compose, MinIO, OpenBao | Infrastructure logos with no destination |
| Self-Hosted | Claim, not evidence |
| Agentic AI, RAG Platform, Hybrid Search | Marketing claims |
| MLOps Ready, LLMOps Ready | Marketing claims |
| Production Ready, Open Source | Claims without evidence |
| Pre-Commit | No project-specific link |
| Trivy, SBOM, No Hardcoded Secrets | No live scan results |
| SemVer | Redundant with Release badge |
