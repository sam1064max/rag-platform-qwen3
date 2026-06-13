FROM python:3.13-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# ── Builder Stage ──────────────────────────────
FROM base AS builder

COPY --from=ghcr.io/astral-sh/uv:0.5 /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
RUN uv sync --no-install-project --frozen --no-dev

# ── Production Stage ───────────────────────────
FROM base AS production

RUN groupadd -r rag && useradd -r -g rag -d /app -s /sbin/nologin rag

COPY --from=builder /app/.venv /app/.venv
COPY src/ /app/src/
COPY configs/ /app/configs/

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src:$PYTHONPATH"

USER rag

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=40s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health')"

CMD ["uvicorn", "rag_platform_qwen3.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
