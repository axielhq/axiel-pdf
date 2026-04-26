"""Contrato para funcionalidades planejadas."""
from dataclasses import dataclass


@dataclass(frozen=True)
class FutureFeature:
    key: str
    name: str
    icon_path: str
    api_key_env: str | None = None
    api_token_env: str | None = None
    capabilities: tuple[str, ...] = ()
