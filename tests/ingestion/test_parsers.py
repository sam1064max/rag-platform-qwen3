import pytest

from src.ingestion.parsers.txt import TxtParser
from src.ingestion.parsers.markdown import MarkdownParser


class TestTxtParser:
    @pytest.mark.asyncio
    async def test_parse_text(self) -> None:
        parser = TxtParser()
        content = b"Hello, world!\nThis is a test."
        result = await parser.parse(content, "test.txt")
        assert result.text == "Hello, world!\nThis is a test."
        assert result.metadata["format"] == "txt"
        assert result.metadata["lines"] == 2

    def test_supported_extensions(self) -> None:
        parser = TxtParser()
        assert ".txt" in parser.supported_extensions()


class TestMarkdownParser:
    @pytest.mark.asyncio
    async def test_parse_markdown(self) -> None:
        parser = MarkdownParser()
        content = b"# Heading\n\nThis is **bold** and [link](http://example.com)."
        result = await parser.parse(content, "test.md")
        assert "# Heading" not in result.text
        assert "bold" in result.text
        assert result.metadata["format"] == "markdown"
        assert result.metadata["headings"] == 1

    def test_supported_extensions(self) -> None:
        parser = MarkdownParser()
        assert ".md" in parser.supported_extensions()
        assert ".markdown" in parser.supported_extensions()


class TestDeduplication:
    def test_checksum(self) -> None:
        from src.ingestion.dedup import DeduplicationEngine

        engine = DeduplicationEngine()
        cs1 = engine.compute_checksum(b"hello")
        cs2 = engine.compute_checksum(b"hello")
        cs3 = engine.compute_checksum(b"world")
        assert cs1 == cs2
        assert cs1 != cs3

    def test_dedup(self) -> None:
        from src.ingestion.dedup import DeduplicationEngine

        engine = DeduplicationEngine()
        cs = engine.compute_checksum(b"test")
        assert not engine.is_duplicate_checksum(cs)
        engine.mark_checksum(cs)
        assert engine.is_duplicate_checksum(cs)

    def test_fingerprint(self) -> None:
        from src.ingestion.dedup import DeduplicationEngine

        engine = DeduplicationEngine()
        fp1 = engine.compute_fingerprint("The quick brown fox")
        fp2 = engine.compute_fingerprint("quick brown fox The")
        assert fp1 == fp2

    def test_reset(self) -> None:
        from src.ingestion.dedup import DeduplicationEngine

        engine = DeduplicationEngine()
        cs = engine.compute_checksum(b"test")
        engine.mark_checksum(cs)
        engine.reset()
        assert not engine.is_duplicate_checksum(cs)


class TestIngestionService:
    @pytest.mark.asyncio
    async def test_ingest_txt(self) -> None:
        from src.ingestion.service import IngestionService

        service = IngestionService()
        service.register_parser(TxtParser())
        result = await service.ingest(b"Hello world", "test.txt")
        assert result.status == "ingested"
        assert result.filename == "test.txt"
        assert len(result.checksum) == 64  # SHA-256

    @pytest.mark.asyncio
    async def test_ingest_duplicate_checksum(self) -> None:
        from src.ingestion.service import IngestionService

        service = IngestionService()
        service.register_parser(TxtParser())
        await service.ingest(b"hello", "a.txt")
        result = await service.ingest(b"hello", "b.txt")
        assert result.status == "skipped_duplicate"

    @pytest.mark.asyncio
    async def test_unsupported_format(self) -> None:
        from src.ingestion.service import IngestionService

        service = IngestionService()
        with pytest.raises(ValueError, match="Unsupported file type"):
            await service.ingest(b"data", "test.exe")
