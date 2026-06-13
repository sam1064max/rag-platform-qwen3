from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class ParseResult:
    text: str
    metadata: dict[str, str | int | float] = field(default_factory=dict)
    pages: int = 0


class DocumentParser(ABC):
    @abstractmethod
    async def parse(self, content: bytes, filename: str) -> ParseResult:
        ...

    @abstractmethod
    def supported_extensions(self) -> set[str]:
        ...
