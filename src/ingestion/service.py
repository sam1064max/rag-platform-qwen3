from dataclasses import dataclass, field
from datetime import datetime, timezone

from tenacity import retry, stop_after_attempt, wait_exponential

from src.ingestion.dedup import DeduplicationEngine
from src.ingestion.parsers.base import DocumentParser, ParseResult


@dataclass
class IngestionResult:
    document_id: str
    filename: str
    checksum: str
    status: str
    pages: int = 0
    chunks: int = 0
    error: str | None = None
    metadata: dict[str, str | int | float] = field(default_factory=dict)


class IngestionService:
    def __init__(self) -> None:
        self._parsers: dict[str, DocumentParser] = {}
        self._dedup = DeduplicationEngine()

    def register_parser(self, parser: DocumentParser) -> None:
        for ext in parser.supported_extensions():
            self._parsers[ext.lower()] = parser

    def _get_parser(self, filename: str) -> DocumentParser:
        import os.path

        ext = os.path.splitext(filename)[1].lower()
        parser = self._parsers.get(ext)
        if parser is None:
            raise ValueError(f"Unsupported file type: {ext}")
        return parser

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
    )
    async def ingest(
        self,
        content: bytes,
        filename: str,
        document_id: str | None = None,
    ) -> IngestionResult:
        import uuid

        doc_id = document_id or str(uuid.uuid4())
        checksum = self._dedup.compute_checksum(content)

        if self._dedup.is_duplicate_checksum(checksum):
            return IngestionResult(
                document_id=doc_id,
                filename=filename,
                checksum=checksum,
                status="skipped_duplicate",
            )

        try:
            parser = self._get_parser(filename)
            result = await parser.parse(content, filename)

            fingerprint = self._dedup.compute_fingerprint(result.text)
            if self._dedup.is_duplicate_fingerprint(fingerprint):
                return IngestionResult(
                    document_id=doc_id,
                    filename=filename,
                    checksum=checksum,
                    status="skipped_duplicate_content",
                )

            self._dedup.mark_checksum(checksum)
            self._dedup.mark_fingerprint(fingerprint)

            full_metadata = {
                **result.metadata,
                "checksum": checksum,
                "document_id": doc_id,
                "ingested_at": datetime.now(timezone.utc).isoformat(),
                "content_length": len(result.text),
            }

            return IngestionResult(
                document_id=doc_id,
                filename=filename,
                checksum=checksum,
                status="ingested",
                pages=result.pages,
                metadata=full_metadata,
            )

        except ValueError:
            raise
        except Exception as exc:
            return IngestionResult(
                document_id=doc_id,
                filename=filename,
                checksum=checksum,
                status="failed",
                error=str(exc),
            )
