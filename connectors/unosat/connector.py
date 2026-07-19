"""Connector placeholder: UNOSAT — sin implementacion de acceso."""

from __future__ import annotations

from connectors.base import NotImplementedConnector


class UnosatConnector(NotImplementedConnector):
    connector_id = "unosat"
    source_name = "UNOSAT"
    version = "0.0.0"