"""
Interfaz base del Connector Framework.

Contrato Fase 1 — Discovery Engine MVP.
Implementaciones deben operar en modo read-only con metadatos curados.
No descargar datos ni ejecutar código externo.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseConnector(ABC):
    """Contrato mínimo para conectores DB2S-GEO."""

    connector_id: str = "base"
    source_name: str = "UNSPECIFIED"
    version: str = "0.0.0"

    @abstractmethod
    def identify(self) -> dict[str, Any]:
        """Metadatos de identificación de la fuente (estructura normalizada)."""

    @abstractmethod
    def discover(self, query: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Descubrimiento de recursos curados (sin descarga)."""

    @abstractmethod
    def describe(self, resource_id: str) -> dict[str, Any]:
        """Descripción de un recurso curado."""

    @abstractmethod
    def access_info(self, resource_id: str) -> dict[str, Any]:
        """Información de acceso — sin ejecutar acceso real ni descargas."""

    @abstractmethod
    def cite(self, resource_id: str) -> dict[str, Any]:
        """Metadatos de citación y atribución."""


class NotImplementedConnector(BaseConnector):
    """Stub para carpetas de conector aún no desarrolladas (post-MVP)."""

    def identify(self) -> dict[str, Any]:
        return {
            "connector_id": self.connector_id,
            "source_name": self.source_name,
            "status": "skeleton",
        }

    def discover(self, query: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        return []

    def describe(self, resource_id: str) -> dict[str, Any]:
        return {"resource_id": resource_id, "status": "not_implemented"}

    def access_info(self, resource_id: str) -> dict[str, Any]:
        return {"resource_id": resource_id, "status": "not_implemented"}

    def cite(self, resource_id: str) -> dict[str, Any]:
        return {"resource_id": resource_id, "status": "not_implemented"}
