import os

from src.security.secret_provider import Secret, SecretCategory, SecretProvider


class EnvProvider(SecretProvider):
    def __init__(self, prefix: str = "RAG_SECRET_") -> None:
        self._prefix = prefix

    async def get_secret(self, path: str, key: str) -> Secret:
        env_key = f"{self._prefix}{path.upper().replace('/', '_')}_{key.upper()}"
        value = os.environ.get(env_key)
        if value is None:
            raise KeyError(f"Environment variable '{env_key}' not found (path={path}, key={key})")
        return Secret(
            key=key,
            value=value,
            category=SecretCategory.API_KEYS,
        )

    async def set_secret(self, path: str, key: str, value: str, _category: SecretCategory) -> None:
        env_key = f"{self._prefix}{path.upper().replace('/', '_')}_{key.upper()}"
        os.environ[env_key] = value

    async def delete_secret(self, path: str, key: str) -> None:
        env_key = f"{self._prefix}{path.upper().replace('/', '_')}_{key.upper()}"
        os.environ.pop(env_key, None)

    async def list_secrets(self, path: str) -> list[str]:
        prefix = f"{self._prefix}{path.upper().replace('/', '_')}_"
        return [k.replace(prefix, "") for k in os.environ if k.startswith(prefix)]

    async def health_check(self) -> bool:
        return True
