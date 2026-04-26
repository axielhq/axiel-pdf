"""Registro de provedores externos planejados."""
from integrations.base import IntegrationConfig


OPENAI = IntegrationConfig(
    key="openai",
    name="OpenAI",
    icon_path="assets/providers/openai.svg",
    api_key_env="OPENAI_API_KEY",
    api_token_env="OPENAI_API_TOKEN",
)

ANTHROPIC = IntegrationConfig(
    key="anthropic",
    name="Anthropic",
    icon_path="assets/providers/anthropic.svg",
    api_key_env="ANTHROPIC_API_KEY",
    api_token_env="ANTHROPIC_API_TOKEN",
)

GEMINI = IntegrationConfig(
    key="gemini",
    name="Gemini",
    icon_path="assets/providers/gemini.svg",
    api_key_env="GEMINI_API_KEY",
    api_token_env="GEMINI_API_TOKEN",
)

AI_INTEGRATIONS = (OPENAI, ANTHROPIC, GEMINI)
