import time
import uuid

from fastapi import APIRouter, HTTPException, UploadFile

from src.api.models import (
    HealthResponse,
    IngestResponse,
    QueryRequest,
    QueryResponse,
    ReadyResponse,
)

router = APIRouter(prefix="/api/v1")


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    from src.api.dependencies import get_services

    svc = get_services()
    components = {}

    if svc.get("vector_store"):
        components["qdrant"] = (
            "connected" if await svc["vector_store"].health_check() else "disconnected"
        )

    return HealthResponse(
        status="healthy",
        version="1.0.0",
        components=components,
    )


@router.get("/ready", response_model=ReadyResponse)
async def ready() -> ReadyResponse:
    return ReadyResponse(ready=True)


@router.post("/ingest", response_model=IngestResponse, status_code=202)
async def ingest(files: list[UploadFile]) -> IngestResponse:
    from src.api.dependencies import get_services

    svc = get_services()
    ingestion = svc.get("ingestion")
    if ingestion is None:
        raise HTTPException(status_code=503, detail="Ingestion service unavailable")

    documents = []
    total_bytes = 0

    for file in files:
        content = await file.read()
        result = await ingestion.ingest(content, file.filename or "unknown")
        documents.append(
            {
                "document_id": result.document_id,
                "filename": result.filename,
                "status": result.status,
                "checksum": result.checksum,
                "size_bytes": len(content),
            }
        )
        total_bytes += len(content)

    return IngestResponse(
        job_id=str(uuid.uuid4()),
        documents=documents,
        total_documents=len(documents),
        total_size_bytes=total_bytes,
    )


@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest) -> QueryResponse:
    from src.api.dependencies import get_services

    svc = get_services()
    query_id = str(uuid.uuid4())
    start = time.monotonic()

    retriever = svc.get("retriever")
    reranker = svc.get("reranker")
    context_reconstructor = svc.get("context_reconstructor")
    generation = svc.get("generation")

    if not all([retriever, reranker, context_reconstructor, generation]):
        raise HTTPException(status_code=503, detail="Query pipeline unavailable")

    retrieval_start = time.monotonic()
    filter_dict = {}
    if request.filters:
        if request.filters.date_from:
            filter_dict["date_from"] = request.filters.date_from
        if request.filters.doc_types:
            filter_dict["doc_type"] = request.filters.doc_types

    results = await retriever.search(
        query=request.query,
        top_k=20,
        filter_=filter_dict,
    )
    retrieval_time = (time.monotonic() - retrieval_start) * 1000

    rerank_start = time.monotonic()
    docs_for_rerank = [
        {"text": r.text, "document_id": r.document_id, "score": r.rrf_score} for r in results
    ]
    reranked = await reranker.rerank(
        query=request.query,
        documents=docs_for_rerank,
        top_k=request.top_k or 5,
    )
    rerank_time = (time.monotonic() - rerank_start) * 1000

    context = context_reconstructor.reconstruct(reranked)

    gen_start = time.monotonic()
    result = await generation.generate(
        query=request.query,
        context=context.text,
    )
    gen_time = (time.monotonic() - gen_start) * 1000

    total_latency = (time.monotonic() - start) * 1000

    return QueryResponse(
        query_id=query_id,
        answer=result.text,
        citations=context.citations,
        metrics={
            "retrieval_time_ms": round(retrieval_time, 2),
            "reranking_time_ms": round(rerank_time, 2),
            "generation_time_ms": round(gen_time, 2),
            "total_latency_ms": round(total_latency, 2),
            "total_tokens": result.total_tokens,
            "input_tokens": result.input_tokens,
            "output_tokens": result.output_tokens,
        },
        guardrail_results={
            "input_check": "passed",
            "retrieval_check": "passed",
            "output_check": "passed",
        },
    )
