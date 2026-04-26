"""Configuracao central da aplicacao."""
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderCredentials:
    api_key: str | None = None
    api_token: str | None = None


def read_provider_credentials(api_key_env: str | None, api_token_env: str | None) -> ProviderCredentials:
    api_key = os.getenv(api_key_env) if api_key_env else None
    api_token = os.getenv(api_token_env) if api_token_env else None
    return ProviderCredentials(api_key=api_key, api_token=api_token)
