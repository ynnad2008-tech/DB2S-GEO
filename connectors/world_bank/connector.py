"""Connector placeholder: World Bank — sin implementacion de acceso."""

from __future__ import annotations

from connectors.base import NotImplementedConnector


class WorldBankConnector(NotImplementedConnector):
    connector_id = "world_bank"
    source_name = "World Bank"
    version = "0.0.0"