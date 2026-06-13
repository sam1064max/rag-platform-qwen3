import io

from docx import Document

from src.ingestion.parsers.base import DocumentParser, ParseResult


class DOCXParser(DocumentParser):
    async def parse(self, content: bytes, filename: str) -> ParseResult:
        doc = Document(io.BytesIO(content))
        text_parts: list[str] = []

        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_parts.append(paragraph.text)

        metadata: dict[str, str | int | float] = {
            "filename": filename,
            "format": "docx",
            "paragraphs": len(text_parts),
        }

        props = doc.core_properties
        if props.title:
            metadata["title"] = props.title
        if props.author:
            metadata["author"] = props.author
        if props.created:
            metadata["created"] = str(props.created)

        return ParseResult(
            text="\n".join(text_parts),
            metadata=metadata,
        )

    def supported_extensions(self) -> set[str]:
        return {".docx"}
