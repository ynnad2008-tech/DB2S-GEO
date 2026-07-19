"""Connector placeholder: DANE — sin implementacion de acceso."""

from __future__ import annotations

from connectors.base import NotImplementedConnector


class DaneConnector(NotImplementedConnector):
    connector_id = "dane"
    source_name = "DANE"
    version = "0.0.0"