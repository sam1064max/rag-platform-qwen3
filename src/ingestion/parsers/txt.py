from src.ingestion.parsers.base import DocumentParser, ParseResult


class TxtParser(DocumentParser):
    async def parse(self, content: bytes, filename: str) -> ParseResult:
        text = content.decode("utf-8", errors="replace")
        lines = text.splitlines()
        return ParseResult(
            text=text,
            metadata={
                "filename": filename,
                "format": "txt",
                "lines": len(lines),
                "chars": len(text),
            },
        )

    def supported_extensions(self) -> set[str]:
        return {".txt"}
