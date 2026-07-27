"""
Registro de conectores MVP (Fases 1–2).

Solo incluye fuentes priorizadas y curadas humanamente.
No auto-registra conectores skeleton post-MVP.
"""

from __future__ import annotations

from connectors.ani.connector import AniConnector
from connectors.ansv.connector import AnsvConnector
from connectors.asf.connector import AsfConnector
from connectors.catie.connector import CatieConnector
from connectors.base import BaseConnector
from connectors.cioh.connector import CiohConnector
from connectors.contraloria.connector import ContraloriaConnector
from connectors.copernicus.connector import CopernicusConnector
from connectors.dane.connector import DaneConnector
from connectors.ebird.connector import EbirdConnector
from connectors.global_forest_watch.connector import GlobalForestWatchConnector
from connectors.sib_colombia.connector import SibColombiaConnector
from connectors.soilgrids.connector import SoilgridsConnector
from connectors.dimar.connector import DimarConnector
from connectors.dnp.connector import DnpConnector
from connectors.gee_copernicus_sentinel2.connector import DynamicworldConnector as GeeCopernicusSentinel2Connector
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
from connectors.world_bank.connector import WorldBankConnector
from connectors.worldpop.connector import WorldpopConnector

# Orden estable MVP (enriquecimiento completo del índice actual)
MVP_CONNECTOR_IDS: tuple[str, ...] = (
    "ideam",
    "invemar",
    "dimar",
    "cioh",
    "gbif",
    "fao",
    "worldpop",
    "gee",
    "sgc",
    "gee-copernicus-sentinel2",
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
    "global-forest-watch",
    "sib_colombia",
    "ebird",
    "soilgrids",
    "asf",
    "catie",
    "copernicus",
    "world_bank",
)


def build_python_mvp_connectors() -> dict[str, BaseConnector]:
    """Instancia conectores Python legacy (fallback / exportación)."""
    instances: list[BaseConnector] = [
        IdeamConnector(),
        InvemarConnector(),
        DimarConnector(),
        CiohConnector(),
        GbifConnector(),
        FaoConnector(),
        WorldpopConnector(),
        GeeConnector(),
        SgcConnector(),
        GeeCopernicusSentinel2Connector(),
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
        GlobalForestWatchConnector(),
        SibColombiaConnector(),
        EbirdConnector(),
        SoilgridsConnector(),
        AsfConnector(),
        CatieConnector(),
        CopernicusConnector(),
        WorldBankConnector(),
    ]
    return {c.connector_id: c for c in instances}


def build_mvp_connectors() -> dict[str, BaseConnector]:
    """
    Runtime preferente: catálogo JSON (solo status=active).

    Fallback: conectores Python si catalog/sources está vacío.
    """
    from connectors.catalog_loader import (
        build_connectors_from_catalog,
        catalog_available,
    )

    if catalog_available():
        return build_connectors_from_catalog()
    return build_python_mvp_connectors()
