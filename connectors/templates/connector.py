"""Plantilla de conector DB2S-GEO."""

from __future__ import annotations

from typing import Any

from connectors.base import NotImplementedConnector


class TemplateConnector(NotImplementedConnector):
    connector_id = "template"
    source_name = "TEMPLATE"
    version = "0.0.0"