"""
Knowledge Usage Observatory — Fase 8.1 MVP.

Registro anónimo de consultas para mejorar el catálogo.
Sin PII, sin IP persistente.
"""

from backend.observatory.engine import ObservatoryEngine
from backend.observatory.privacy import TRANSPARENCY_NOTICE

__all__ = ["ObservatoryEngine", "TRANSPARENCY_NOTICE"]
