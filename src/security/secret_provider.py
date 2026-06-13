from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import StrEnum


class SecretCategory(StrEnum):
    LLM_CREDENTIALS = "llm"
    DATABASE_CREDENTIALS = "database"
    STORAGE_CREDENTIALS = "storage"
    API_KEYS = "api"
    OBSERVABILITY_TOKENS = "observability"
    TLS_CERTIFICATES = "tls"


@dataclass
class Secret:
    key: str
    value: str
    category: SecretCategory
    version: int = 1


class SecretProvider(ABC):
    @abstractmethod
    async def get_secret(self, path: str, key: str) -> Secret: ...

    @abstractmethod
    async def set_secret(
        self, path: str, key: str, value: str, category: SecretCategory
    ) -> None: ...

    @abstractmethod
    async def delete_secret(self, path: str, key: str) -> None: ...

    @abstractmethod
    async def list_secrets(self, path: str) -> list[str]: ...

    @abstractmethod
    async def health_check(self) -> bool: ...
