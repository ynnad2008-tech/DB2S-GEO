"""
Tipos de eventos y severidades — Watcher Engine MVP (Fase 5).
"""

from __future__ import annotations

from typing import Any, Literal, TypedDict

EventType = Literal[
    "NEW_RESOURCE",
    "REMOVED_RESOURCE",
    "RESOURCE_CHANGED",
    "NEW_ACCESS_METHOD",
    "ACCESS_METHOD_REMOVED",
    "METADATA_CHANGED",
    "SOURCE_UNAVAILABLE",
    "BASELINE_CREATED",
]

Severity = Literal["info", "warning", "critical"]

EVENT_SEVERITY: dict[str, Severity] = {
    "NEW_RESOURCE": "info",
    "REMOVED_RESOURCE": "warning",
    "RESOURCE_CHANGED": "info",
    "NEW_ACCESS_METHOD": "info",
    "ACCESS_METHOD_REMOVED": "warning",
    "METADATA_CHANGED": "info",
    "SOURCE_UNAVAILABLE": "critical",
    "BASELINE_CREATED": "info",
}

DETECTED_BY = "watcher_engine"


class WatcherEvent(TypedDict, total=False):
    event_id: str
    event_type: EventType
    source: str
    resource: str
    timestamp: str
    severity: Severity
    detected_by: str
    detail: dict[str, Any]
    curation: str
    auto_applied: bool


def default_severity(event_type: str) -> Severity:
    return EVENT_SEVERITY.get(event_type, "info")
