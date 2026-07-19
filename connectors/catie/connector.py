"""Connector placeholder: CATIE — sin implementacion de acceso."""

from __future__ import annotations

from connectors.base import NotImplementedConnector


class CatieConnector(NotImplementedConnector):
    connector_id = "catie"
    source_name = "CATIE"
    version = "0.0.0"