from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from prometheus_client import make_asgi_app

from src.api.dependencies import register_services
from src.api.routes import router

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("rag-platform-qwen3 starting...")
    register_services({})
    yield
    logger.info("rag-platform-qwen3 shutting down...")


app = FastAPI(
    title="RAG Platform Qwen3",
    description="Production-grade self-hosted RAG platform",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

metrics_app = make_asgi_app()


@app.get("/")
async def root():
    return {"service": "rag-platform-qwen3", "version": "1.0.0"}


app.mount("/api/v1/metrics", metrics_app)
app.include_router(router)


def main() -> None:
    import uvicorn

    uvicorn.run(
        "rag_platform_qwen3.main:app",
        host="0.0.0.0",
        port=8000,
        workers=4,
        log_level="info",
    )


if __name__ == "__main__":
    main()
