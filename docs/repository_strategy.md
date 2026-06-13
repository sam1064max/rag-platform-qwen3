# Repository Strategy

## Overview

This document defines the repository strategy for `rag-platform-qwen3`, a production-grade, self-hosted Retrieval-Augmented Generation (RAG) platform following Specification-Driven Development (SDD).

## Repository Locations

| Role         | URL                                              |
|-------------|--------------------------------------------------|
| **Primary**  | Gitea (Self-Hosted)                              |
| **Mirror**   | GitHub (Public)                                  |

## Git Identity

- **Name:** Sushant Shambharkar
- **Email:** sam1064max@gmail.com

## Remote Configuration

```bash
git remote add origin <gitea-repo-url>
git remote add github <github-repo-url>
```

Push mirroring is configured from Gitea (origin) to GitHub (github). All pushes go to both remotes.

## Branch Strategy

| Branch   | Purpose                                           |
|----------|---------------------------------------------------|
| `main`   | Production-ready code. Protected. Requires PR.    |
| `develop`| Integration branch. Feature branches merge here.  |
| `feat/*` | Feature branches. One per spec-driven phase.      |
| `fix/*`  | Bugfix branches.                                  |
| `docs/*` | Documentation-only changes.                       |

## Commit Convention

All commits follow **Conventional Commits**:

```
<type>(<scope>): <description>

[optional body]
```

### Types

| Type       | Usage                                         |
|------------|-----------------------------------------------|
| `feat`     | New feature or capability                     |
| `fix`      | Bugfix                                        |
| `docs`     | Documentation changes                         |
| `chore`    | Maintenance, tooling, config                  |
| `test`     | Test additions or changes                     |
| `refactor` | Code restructuring without behavior change    |
| `perf`     | Performance improvements                      |
| `ci`       | CI/CD pipeline changes                        |
| `security` | Security fixes or improvements                |
| `infra`    | Infrastructure definitions                    |

### Scope Examples

`repo`, `spec`, `arch`, `infra`, `security`, `ingestion`, `chunking`, `embeddings`, `vectorstore`, `retrieval`, `reranking`, `context`, `guardrails`, `generation`, `api`, `eval`, `observability`, `docker`, `ci`, `test`, `ops`, `release`

### Example Commits

```
feat(spec): create system specification

docs(architecture): complete platform architecture

chore(repo): initialize repository structure

feat(infra): add platform infrastructure stack
```

## Commit Policy

- **Minimum:** 30 commits
- **Maximum:** 60 commits
- **Scope:** 22 phases, each producing 1-3 commits
- Every commit must:
  - Build successfully
  - Pass tests
  - Represent a meaningful milestone

## Quality Gates

- No `TODO` placeholders in production code
- No pseudo-code or stubs in production code
- No mocked production dependencies
- Every feature includes: tests, documentation, observability, error handling

## Release Strategy

| Version | Phase            |
|---------|------------------|
| v0.1.0  | Core retrieval   |
| v0.2.0  | Generation       |
| v0.3.0  | Guardrails       |
| v0.4.0  | Evaluation       |
| v0.5.0  | Observability    |
| v1.0.0  | Production Ready |

Releases are tagged from `main` using signed tags.

## Mirroring

- Gitea is the **source of truth**.
- GitHub is a **read-only mirror**.
- Push mirroring ensures GitHub stays in sync.
- All CI/CD runs on Gitea Actions.
- GitHub mirror validation runs in CI.

## Security

- No secrets committed to the repository.
- All secrets injected via OpenBao at runtime.
- Container images scanned for vulnerabilities.
- SBOM generated for every release.

## Directory Structure

```
rag-platform-qwen3/
├── docs/              # Architecture, specs, runbooks
├── src/               # Source code
│   ├── ingestion/     # Document ingestion pipeline
│   ├── chunking/      # Parent-child chunking
│   ├── embeddings/    # Embedding generation
│   ├── vectorstore/   # Qdrant vector storage
│   ├── retrieval/     # Hybrid retrieval (BM25 + Dense + RRF)
│   ├── reranking/     # Qwen3-Reranker service
│   ├── context/       # Context reconstruction
│   ├── generation/    # Qwen3-32B-Instruct generation
│   ├── api/           # FastAPI endpoints
│   ├── security/      # Secrets management
│   ├── observability/ # Tracing and monitoring
│   └── common/        # Shared utilities
├── tests/             # Test suite
├── scripts/           # Utility scripts
├── docker/            # Container definitions
├── infra/             # Infrastructure configs
├── configs/           # Application configs
├── guardrails/        # NeMo Guardrails configs
├── evaluations/       # RAGAS and DeepEval tests
├── observability/     # Prometheus/Grafana dashboards
└── .github/           # CI/CD workflows
```
