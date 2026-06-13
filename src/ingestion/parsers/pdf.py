import fitz

from src.ingestion.parsers.base import DocumentParser, ParseResult


class PDFParser(DocumentParser):
    async def parse(self, content: bytes, filename: str) -> ParseResult:
        doc = fitz.open(stream=content, filetype="pdf")
        text_parts: list[str] = []
        metadata: dict[str, str | int | float] = {
            "filename": filename,
            "format": "pdf",
            "pages": doc.page_count,
        }

        if doc.metadata:
            for key in ("title", "author", "subject"):
                if doc.metadata.get(key):
                    metadata[key] = doc.metadata[key]

        for page_num in range(doc.page_count):
            page = doc[page_num]
            text_parts.append(page.get_text())

        doc.close()
        return ParseResult(
            text="\n".join(text_parts),
            metadata=metadata,
            pages=doc.page_count,
        )

    def supported_extensions(self) -> set[str]:
        return {".pdf"}
