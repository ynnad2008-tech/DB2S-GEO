"""Connector placeholder: IGAC — sin implementacion de acceso."""

from __future__ import annotations

from connectors.base import NotImplementedConnector


class IgacConnector(NotImplementedConnector):
    connector_id = "igac"
    source_name = "IGAC"
    version = "0.0.0"