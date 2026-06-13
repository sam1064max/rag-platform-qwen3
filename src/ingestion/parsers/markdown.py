import re

from src.ingestion.parsers.base import DocumentParser, ParseResult


class MarkdownParser(DocumentParser):
    async def parse(self, content: bytes, filename: str) -> ParseResult:
        raw = content.decode("utf-8", errors="replace")
        text = re.sub(r"!\[.*?\]\(.*?\)", "", raw)
        text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
        text = re.sub(r"#{1,6}\s+", "", text)
        text = re.sub(r"[*_~`]", "", text)
        text = re.sub(r"\n{3,}", "\n\n", text.strip())

        headings = re.findall(r"^#{1,6}\s+(.+)$", raw, re.MULTILINE)
        code_blocks = len(re.findall(r"```", raw)) // 2

        return ParseResult(
            text=text,
            metadata={
                "filename": filename,
                "format": "markdown",
                "headings": len(headings),
                "code_blocks": code_blocks,
                "chars": len(raw),
            },
        )

    def supported_extensions(self) -> set[str]:
        return {".md", ".markdown"}
