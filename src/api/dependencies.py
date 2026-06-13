from typing import Any

_service_registry: dict[str, Any] = {}


def register_services(services: dict[str, Any]) -> None:
    _service_registry.clear()
    _service_registry.update(services)


def get_services() -> dict[str, Any]:
    return _service_registry
