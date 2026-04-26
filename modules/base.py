"""Contratos basicos de modulos do produto."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ModuleManifest:
    key: str
    name: str
    status: str
    description: str
