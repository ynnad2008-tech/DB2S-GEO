"""DB2S-GEO Connector Framework — Fase 1 Discovery MVP."""

from connectors.base import BaseConnector, NotImplementedConnector
from connectors.registry import MVP_CONNECTOR_IDS, build_mvp_connectors

__all__ = [
    "BaseConnector",
    "NotImplementedConnector",
    "MVP_CONNECTOR_IDS",
    "build_mvp_connectors",
]
