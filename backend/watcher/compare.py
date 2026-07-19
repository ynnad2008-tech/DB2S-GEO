"""
Construcción y comparación de snapshots — Watcher Engine MVP.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from backend.watcher.models import DETECTED_BY, default_severity

if TYPE_CHECKING:
    from backend.discovery.engine import DiscoveryEngine
    from backend.metadata.engine import MetadataEngine


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def build_snapshot(
    source_id: str,
    discovery: DiscoveryEngine,
    metadata: MetadataEngine,
) -> dict[str, Any]:
    """Observa el estado actual vía Discovery + Metadata (read-only)."""
    source = discovery.get_source(source_id)
    if source is None:
        return {
            "source_id": source_id,
            "source": source_id,
            "available": False,
            "domains": [],
            "access_methods": [],
            "resources": {},
            "captured_at": utc_now(),
        }

    resources_meta = metadata.list_resources(source_id, summary=False) or []
    resources: dict[str, dict[str, Any]] = {}
    for item in resources_meta:
        rid = item.get("resource_id")
        if not rid:
            continue
        # Solo campos observables (no inventar).
        fingerprint_payload = {
            "title": item.get("title"),
            "domain": item.get("domain"),
            "domains": item.get("domains"),
            "keywords": item.get("keywords"),
            "access_methods": item.get("access_methods"),
            "license": item.get("license"),
            "spatial_scope": item.get("spatial_scope"),
            "temporal_scope": item.get("temporal_scope"),
        }
        resources[rid] = {
            **fingerprint_payload,
            "resource_id": rid,
            "fingerprint": _fingerprint(fingerprint_payload),
        }

    return {
        "source_id": source.get("source_id") or source_id,
        "source": source.get("source") or source_id,
        "institution": source.get("institution"),
        "domains": list(source.get("domains") or []),
        "access_methods": list(source.get("access_methods") or []),
        "homepage": source.get("homepage"),
        "license": source.get("license"),
        "resources": resources,
        "available": True,
        "captured_at": utc_now(),
    }


def compare_snapshots(
    previous: dict[str, Any] | None,
    current: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Compara snapshots y genera eventos.

    Primera observación (sin previous): solo BASELINE_CREATED.
    No marca todos los recursos como NEW_RESOURCE (evita ruido).
    """
    source_id = current.get("source_id", "unknown")
    timestamp = current.get("captured_at") or utc_now()
    events: list[dict[str, Any]] = []

    if previous is None:
        events.append(
            _event(
                "BASELINE_CREATED",
                source_id,
                resource="",
                timestamp=timestamp,
                detail={
                    "resources_count": len(current.get("resources") or {}),
                    "access_methods": current.get("access_methods") or [],
                    "note": "Snapshot inicial. Sin auto-aplicación al catálogo.",
                },
            )
        )
        return events

    # Disponibilidad
    prev_ok = bool(previous.get("available", True))
    curr_ok = bool(current.get("available", True))
    if prev_ok and not curr_ok:
        events.append(
            _event(
                "SOURCE_UNAVAILABLE",
                source_id,
                resource="",
                timestamp=timestamp,
                detail={"previous_available": True, "current_available": False},
            )
        )
        return events

    if not curr_ok:
        return events

    prev_resources = previous.get("resources") or {}
    curr_resources = current.get("resources") or {}
    prev_ids = set(prev_resources.keys())
    curr_ids = set(curr_resources.keys())

    for rid in sorted(curr_ids - prev_ids):
        events.append(
            _event(
                "NEW_RESOURCE",
                source_id,
                resource=rid,
                timestamp=timestamp,
                detail={"title": (curr_resources.get(rid) or {}).get("title")},
            )
        )

    for rid in sorted(prev_ids - curr_ids):
        events.append(
            _event(
                "REMOVED_RESOURCE",
                source_id,
                resource=rid,
                timestamp=timestamp,
                detail={"title": (prev_resources.get(rid) or {}).get("title")},
            )
        )

    for rid in sorted(prev_ids & curr_ids):
        prev_fp = (prev_resources.get(rid) or {}).get("fingerprint")
        curr_fp = (curr_resources.get(rid) or {}).get("fingerprint")
        if prev_fp != curr_fp:
            events.append(
                _event(
                    "RESOURCE_CHANGED",
                    source_id,
                    resource=rid,
                    timestamp=timestamp,
                    detail={
                        "previous_fingerprint": prev_fp,
                        "current_fingerprint": curr_fp,
                    },
                )
            )
            events.append(
                _event(
                    "METADATA_CHANGED",
                    source_id,
                    resource=rid,
                    timestamp=timestamp,
                    detail={
                        "previous": _safe_meta(prev_resources.get(rid)),
                        "current": _safe_meta(curr_resources.get(rid)),
                    },
                )
            )

    prev_access = set(previous.get("access_methods") or [])
    curr_access = set(current.get("access_methods") or [])
    for method in sorted(curr_access - prev_access):
        events.append(
            _event(
                "NEW_ACCESS_METHOD",
                source_id,
                resource="",
                timestamp=timestamp,
                detail={"access_method": method},
            )
        )
    for method in sorted(prev_access - curr_access):
        events.append(
            _event(
                "ACCESS_METHOD_REMOVED",
                source_id,
                resource="",
                timestamp=timestamp,
                detail={"access_method": method},
            )
        )

    # Metadatos a nivel fuente (dominios / institution)
    if (previous.get("domains") or []) != (current.get("domains") or []) or (
        previous.get("institution") != current.get("institution")
    ):
        events.append(
            _event(
                "METADATA_CHANGED",
                source_id,
                resource="",
                timestamp=timestamp,
                detail={
                    "scope": "source",
                    "previous_domains": previous.get("domains"),
                    "current_domains": current.get("domains"),
                },
            )
        )

    return events


def _event(
    event_type: str,
    source: str,
    *,
    resource: str,
    timestamp: str,
    detail: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "event_id": str(uuid4()),
        "event_type": event_type,
        "source": source,
        "resource": resource,
        "timestamp": timestamp,
        "severity": default_severity(event_type),
        "detected_by": DETECTED_BY,
        "detail": detail or {},
        "curation": "human_required",
        "auto_applied": False,
    }


def _fingerprint(payload: dict[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]


def _safe_meta(resource: dict[str, Any] | None) -> dict[str, Any]:
    if not resource:
        return {}
    return {
        k: resource.get(k)
        for k in (
            "title",
            "domain",
            "domains",
            "keywords",
            "access_methods",
            "license",
        )
    }
