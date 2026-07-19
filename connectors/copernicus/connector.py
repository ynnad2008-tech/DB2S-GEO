"""Connector placeholder: Copernicus — sin implementacion de acceso."""

from __future__ import annotations

from connectors.base import NotImplementedConnector


class CopernicusConnector(NotImplementedConnector):
    connector_id = "copernicus"
    source_name = "Copernicus"
    version = "0.0.0"