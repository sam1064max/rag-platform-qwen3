from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    timestamp: str = ""
    version: str = "1.0.0"
    components: dict[str, str] = {}


class ReadyResponse(BaseModel):
    ready: bool


class IngestDocument(BaseModel):
    document_id: str
    filename: str
    status: str
    checksum: str
    size_bytes: int


class IngestResponse(BaseModel):
    job_id: str
    documents: list[IngestDocument]
    total_documents: int
    total_size_bytes: int


class QueryFilters(BaseModel):
    date_from: str | None = None
    date_to: str | None = None
    doc_types: list[str] | None = None


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=4096)
    tenant_id: str | None = None
    filters: QueryFilters | None = None
    top_k: int = 5
    stream: bool = False


class Citation(BaseModel):
    citation_id: int
    document_id: str
    filename: str
    text_snippet: str
    relevance_score: float


class QueryResponse(BaseModel):
    query_id: str
    answer: str
    citations: list[Citation] | list[dict] = []
    metrics: dict[str, float | int] = {}
    guardrail_results: dict[str, str] = {}
