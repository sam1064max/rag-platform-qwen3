import json
from typing import Any

import httpx

from src.security.secret_provider import Secret, SecretCategory, SecretProvider


class OpenBaoProvider(SecretProvider):
    def __init__(self, addr: str = "http://localhost:8200", token: str = "") -> None:
        self._addr = addr.rstrip("/")
        self._token = token
        self._client = httpx.AsyncClient(
            base_url=self._addr,
            headers={"X-Vault-Token": self._token},
            timeout=30.0,
        )

    async def get_secret(self, path: str, key: str) -> Secret:
        url = f"/v1/{path.lstrip('/')}"
        response = await self._client.get(url)
        response.raise_for_status()
        data = response.json()

        secret_data = data.get("data", {}).get("data", {})
        if key not in secret_data:
            raise KeyError(f"Key '{key}' not found in path '{path}'")

        metadata = data.get("data", {}).get("metadata", {})
        return Secret(
            key=key,
            value=str(secret_data[key]),
            category=SecretCategory.LLM_CREDENTIALS,
            version=metadata.get("version", 1),
        )

    async def set_secret(
        self, path: str, key: str, value: str, category: SecretCategory
    ) -> None:
        url = f"/v1/{path.lstrip('/')}"
        payload: dict[str, Any] = {"data": {key: value}}

        if category:
            payload["data"]["_category"] = category.value

        response = await self._client.post(url, json=payload)
        response.raise_for_status()

    async def delete_secret(self, path: str, key: str) -> None:
        url = f"/v1/{path.lstrip('/')}"
        response = await self._client.delete(url)
        response.raise_for_status()

    async def list_secrets(self, path: str) -> list[str]:
        url = f"/v1/{path.lstrip('/')}"
        response = await self._client.request("LIST", url)
        response.raise_for_status()
        data = response.json()
        return data.get("data", {}).get("keys", [])

    async def health_check(self) -> bool:
        try:
            response = await self._client.get("/v1/sys/health")
            return response.status_code in (200, 429)
        except Exception:
            return False

    async def close(self) -> None:
        await self._client.aclose()
