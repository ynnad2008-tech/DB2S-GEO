"""
Watcher Engine — Fase 5 MVP.

Observa fuentes vía Discovery + Metadata, compara snapshots y registra eventos.
NO modifica el catálogo. NO actualiza conectores. Curaduría humana obligatoria.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from connectors.registry import MVP_CONNECTOR_IDS
from backend.watcher.compare import build_snapshot, compare_snapshots
from backend.watcher.store import WatcherStore

if TYPE_CHECKING:
    from backend.discovery.engine import DiscoveryEngine
    from backend.metadata.engine import MetadataEngine

# Persistencia por defecto relativa a la raíz del repo.
DEFAULT_DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "watcher"


class WatcherEngine:
    """Motor de observación y alerta (sin auto-gobernanza)."""

    status = "mvp"

    def __init__(
        self,
        discovery: DiscoveryEngine | None = None,
        metadata: MetadataEngine | None = None,
        store: WatcherStore | None = None,
        data_dir: Path | str | None = None,
        source_ids: tuple[str, ...] | None = None,
    ) -> None:
        self._discovery = discovery
        self._metadata = metadata
        self._store = store or WatcherStore(data_dir or DEFAULT_DATA_DIR)
        self._source_ids = source_ids or MVP_CONNECTOR_IDS

    def bind(
        self,
        discovery: DiscoveryEngine,
        metadata: MetadataEngine,
    ) -> None:
        self._discovery = discovery
        self._metadata = metadata

    def info(self) -> dict[str, Any]:
        stats = self._store.stats()
        return {
            "engine": "WatcherEngine",
            "status": self.status,
            "monitored_sources": list(self._source_ids),
            "auto_updates_catalog": False,
            "auto_updates_connectors": False,
            "human_curation": True,
            "principle": "El sistema se automonitorea. El sistema no se autogobierna.",
            "event_types": [
                "NEW_RESOURCE",
                "REMOVED_RESOURCE",
                "RESOURCE_CHANGED",
                "NEW_ACCESS_METHOD",
                "ACCESS_METHOD_REMOVED",
                "METADATA_CHANGED",
                "SOURCE_UNAVAILABLE",
                "BASELINE_CREATED",
            ],
            "severities": ["info", "warning", "critical"],
            "persistence": "json_local",
            "built_from": ["discovery", "metadata"],
            "ai": False,
            "read_only": True,
            **stats,
        }

    def run(self, source_ids: list[str] | None = None) -> dict[str, Any]:
        """
        Ejecuta un ciclo de observación.

        Para cada fuente:
          1. Construye snapshot actual
          2. Compara con snapshot anterior
          3. Persiste eventos (sin aplicar cambios)
          4. Guarda snapshot actual
        """
        if self._discovery is None or self._metadata is None:
            raise RuntimeError("Discovery y Metadata son requeridos")

        targets = source_ids or list(self._source_ids)
        all_events: list[dict[str, Any]] = []
        per_source: list[dict[str, Any]] = []

        for source_id in targets:
            sid = source_id.strip().lower()
            previous = self._store.load_snapshot(sid)
            current = build_snapshot(sid, self._discovery, self._metadata)
            events = compare_snapshots(previous, current)
            self._store.append_events(events)
            self._store.save_snapshot(sid, current)
            all_events.extend(events)
            per_source.append(
                {
                    "source": sid,
                    "available": current.get("available", False),
                    "events_detected": len(events),
                    "resources_observed": len(current.get("resources") or {}),
                    "baseline": previous is None,
                }
            )

        return {
            "status": "ok",
            "sources_checked": len(targets),
            "events_detected": len(all_events),
            "events": all_events,
            "per_source": per_source,
            "auto_applied": False,
            "curation": "human_required",
            "message": (
                "Cambios detectados y registrados. "
                "Ningún catálogo/conector fue modificado automáticamente."
            ),
        }

    def list_events(
        self,
        *,
        source_id: str | None = None,
        event_type: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        return self._store.list_events(
            source_id=source_id,
            event_type=event_type,
            limit=limit,
        )

    def get_snapshot(self, source_id: str) -> dict[str, Any] | None:
        return self._store.load_snapshot(source_id)
