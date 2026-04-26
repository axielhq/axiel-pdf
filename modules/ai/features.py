"""Funcionalidades futuras de IA."""
from integrations.providers import AI_INTEGRATIONS
from modules.features import FutureFeature


AI_CAPABILITIES = (
    "Nomear e organizar documentos antes do merge",
    "Sugerir ordenacao inteligente",
    "Detectar duplicatas, arquivos corrompidos e paginas em branco",
    "Gerar indice ou sumario automatico",
    "Extrair metadados para renomeacao em lote",
)


AI_PROVIDERS = tuple(
    FutureFeature(
        key=provider.key,
        name=provider.name,
        icon_path=provider.icon_path,
        api_key_env=provider.api_key_env,
        api_token_env=provider.api_token_env,
        capabilities=AI_CAPABILITIES,
    )
    for provider in AI_INTEGRATIONS
)
