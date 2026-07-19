"""Connector placeholder: eBird — sin implementacion de acceso."""

from __future__ import annotations

from connectors.base import NotImplementedConnector


class EbirdConnector(NotImplementedConnector):
    connector_id = "ebird"
    source_name = "eBird"
    version = "0.0.0"