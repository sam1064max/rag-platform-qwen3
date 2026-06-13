import tiktoken


class TokenCounter:
    _encodings: dict[str, tiktoken.Encoding] = {}

    @classmethod
    def count(cls, text: str, model: str = "cl100k_base") -> int:
        if model not in cls._encodings:
            try:
                cls._encodings[model] = tiktoken.get_encoding(model)
            except Exception:
                return len(text.split())
        return len(cls._encodings[model].encode(text))

    @classmethod
    def truncate(
        cls, text: str, max_tokens: int, model: str = "cl100k_base"
    ) -> str:
        token_count = cls.count(text, model)
        if token_count <= max_tokens:
            return text
        try:
            encoding = cls._encodings.get(model) or tiktoken.get_encoding(model)
            tokens = encoding.encode(text)[:max_tokens]
            return encoding.decode(tokens)
        except Exception:
            words = text.split()[:max_tokens]
            return " ".join(words)
