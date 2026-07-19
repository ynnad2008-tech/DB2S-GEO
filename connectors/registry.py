"""
Registro de conectores MVP (Fases 1–2).

Solo incluye fuentes priorizadas y curadas humanamente.
No auto-registra conectores skeleton post-MVP.
"""

from __future__ import annotations

from connectors.base import BaseConnector
from connectors.fao.connector import FaoConnector
from connectors.gbif.connector import GbifConnector
from connectors.gee.connector import GeeConnector
from connectors.ideam.connector import IdeamConnector
from connectors.invemar.connector import InvemarConnector
from connectors.worldpop.connector import WorldpopConnector

# Orden estable MVP (Fase 2: + INVEMAR)
MVP_CONNECTOR_IDS: tuple[str, ...] = (
    "ideam",
    "invemar",
    "gbif",
    "fao",
    "worldpop",
    "gee",
)


def build_mvp_connectors() -> dict[str, BaseConnector]:
    """Instancia los conectores MVP registrados."""
    instances: list[BaseConnector] = [
        IdeamConnector(),
        InvemarConnector(),
        GbifConnector(),
        FaoConnector(),
        WorldpopConnector(),
        GeeConnector(),
    ]
    return {c.connector_id: c for c in instances}
