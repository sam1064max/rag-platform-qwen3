from src.common.token_counter import TokenCounter


class TestTokenCounter:
    def test_count_basic(self) -> None:
        count = TokenCounter.count("Hello world")
        assert count > 0

    def test_count_empty(self) -> None:
        count = TokenCounter.count("")
        assert count == 0

    def test_truncate_short_text(self) -> None:
        result = TokenCounter.truncate("Hello world", max_tokens=100)
        assert result == "Hello world"

    def test_truncate_long_text(self) -> None:
        text = "word " * 1000
        result = TokenCounter.truncate(text, max_tokens=10)
        token_count = TokenCounter.count(result)
        assert token_count <= 10

    def test_truncate_edge(self) -> None:
        text = "Hello world this is a test"
        result = TokenCounter.truncate(text, max_tokens=2)
        assert len(result) < len(text)
