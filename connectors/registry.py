"""
Registro de conectores MVP (Fases 1–2).

Solo incluye fuentes priorizadas y curadas humanamente.
No auto-registra conectores skeleton post-MVP.
"""

from __future__ import annotations

from connectors.ani.connector import AniConnector
from connectors.ansv.connector import AnsvConnector
from connectors.base import BaseConnector
from connectors.contraloria.connector import ContraloriaConnector
from connectors.dane.connector import DaneConnector
from connectors.dnp.connector import DnpConnector
from connectors.dynamicworld.connector import DynamicworldConnector
from connectors.fao.connector import FaoConnector
from connectors.gbif.connector import GbifConnector
from connectors.gee.connector import GeeConnector
from connectors.ideam.connector import IdeamConnector
from connectors.igac.connector import IgacConnector
from connectors.invemar.connector import InvemarConnector
from connectors.invias.connector import InviasConnector
from connectors.mapbiomas.connector import MapbiomasConnector
from connectors.mintransporte.connector import MintransporteConnector
from connectors.nasa.connector import NasaConnector
from connectors.sgc.connector import SgcConnector
from connectors.supertransporte.connector import SupertransporteConnector
from connectors.superservicios.connector import SuperserviciosConnector
from connectors.unosat.connector import UnosatConnector
from connectors.upit.connector import UpitConnector
from connectors.upra.connector import UpraConnector
from connectors.worldpop.connector import WorldpopConnector

# Orden estable MVP (enriquecimiento completo del índice actual)
MVP_CONNECTOR_IDS: tuple[str, ...] = (
    "ideam",
    "invemar",
    "gbif",
    "fao",
    "worldpop",
    "gee",
    "sgc",
    "dynamicworld",
    "nasa",
    "mapbiomas",
    "unosat",
    "igac",
    "upra",
    "dane",
    "dnp",
    "contraloria",
    "superservicios",
    "mintransporte",
    "upit",
    "invias",
    "ansv",
    "ani",
    "supertransporte",
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
        SgcConnector(),
        DynamicworldConnector(),
        NasaConnector(),
        MapbiomasConnector(),
        UnosatConnector(),
        IgacConnector(),
        UpraConnector(),
        DaneConnector(),
        DnpConnector(),
        ContraloriaConnector(),
        SuperserviciosConnector(),
        MintransporteConnector(),
        UpitConnector(),
        InviasConnector(),
        AnsvConnector(),
        AniConnector(),
        SupertransporteConnector(),
    ]
    return {c.connector_id: c for c in instances}
