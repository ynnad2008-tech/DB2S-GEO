"""
Configuración placeholder.

Reservado para variables de entorno y settings (Pydantic Settings / similar).
No cargar secretos en el repositorio.
"""

# Configuración mínima Alpha 0.9 (sin secretos)
ENVIRONMENT = "alpha"
APP_PHASE = "alpha-release"
APP_VERSION = "0.9.0-alpha"
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
