"""Connector placeholder: NASA — sin implementacion de acceso."""

from __future__ import annotations

from connectors.base import NotImplementedConnector


class NasaConnector(NotImplementedConnector):
    connector_id = "nasa"
    source_name = "NASA"
    version = "0.0.0"