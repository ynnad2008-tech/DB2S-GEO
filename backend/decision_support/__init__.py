"""
Decision Support Engine — Fase 8 MVP.

Consulta → necesidad → rutas de acción → fuente → recursos → justificación.
Sin IA / embeddings / LLMs. Solo fuentes MVP + Recommendation Engine + KG.
"""

from backend.decision_support.engine import DecisionSupportEngine

__all__ = ["DecisionSupportEngine"]
