"""Contratos de integracoes externas."""
from dataclasses import dataclass


@dataclass(frozen=True)
class IntegrationConfig:
    key: str
    name: str
    icon_path: str
    api_key_env: str | None = None
    api_token_env: str | None = None
    status: str = "planned"
