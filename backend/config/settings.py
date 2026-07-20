"""
Configuración mínima — Preview 0.1.0.

Variables de entorno (opcionales):
  ENVIRONMENT, TELEMETRY_DB_PATH, PORT, HOST
"""

from __future__ import annotations

import os

ENVIRONMENT = os.environ.get("ENVIRONMENT", "preview")
APP_PHASE = "preview"
APP_VERSION = "0.2.0-preview"
READ_ONLY = True
DOWNLOADS_ENABLED = False
GRAPH_BACKEND = "python_memory"
RECOMMENDATION_AI = False
WATCHER_AUTO_APPLY = False
SOURCE_DISCOVERY_AUTO_APPROVE = False
DECISION_SUPPORT_AI = False
OBSERVATORY_STORE_PII = False
OBSERVATORY_STORE_IP = False
WORKBENCH_ENABLED = True
TELEMETRY_DB_PATH = os.environ.get("TELEMETRY_DB_PATH", "")
