from dataclasses import dataclass, field
from typing import Any

import yaml


@dataclass
class AppConfig:
    env: str = "development"
    log_level: str = "info"
    qdrant_host: str = "localhost"
    qdrant_port: int = 6334
    qdrant_api_key: str = ""
    qdrant_collection: str = "documents"
    minio_host: str = "localhost"
    minio_port: int = 9000
    minio_access_key: str = ""
    minio_secret_key: str = ""
    openbao_addr: str = "http://localhost:8200"
    openbao_token: str = ""
    otel_endpoint: str = "http://localhost:4317"
    langfuse_host: str = "http://localhost:3000"
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    llm_provider: str = "vllm"
    llm_model: str = "Qwen3-32B-Instruct"
    llm_api_base: str = "http://localhost:8012/v1"
    llm_api_key: str = "not-needed"
    embedding_model: str = "Qwen/Qwen3-Embedding-8B"
    embedding_endpoint: str = "http://localhost:8010/v1"
    reranker_model: str = "Qwen/Qwen3-Reranker"
    reranker_endpoint: str = "http://localhost:8011/v1"
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_yaml(cls, path: str) -> "AppConfig":
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        return cls(**{k.lower(): v for k, v in data.items()})


def load_config(path: str | None = None) -> AppConfig:
    import os

    if path and os.path.exists(path):
        return AppConfig.from_yaml(path)
    return AppConfig()
