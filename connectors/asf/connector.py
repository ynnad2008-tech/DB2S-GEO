"""Connector placeholder: ASF — sin implementacion de acceso."""

from __future__ import annotations

from connectors.base import NotImplementedConnector


class AsfConnector(NotImplementedConnector):
    connector_id = "asf"
    source_name = "ASF"
    version = "0.0.0"