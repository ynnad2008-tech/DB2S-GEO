"""Tests — intérprete NL opcional (Gemini) con fallback determinista."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.decision_support import llm_interpreter
from backend.decision_support.concepts import expand_concepts, primary_need_label
from backend.decision_support.intents import detect_intents


@pytest.fixture(autouse=True)
def sin_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    monkeypatch.delenv("GEMINI_TIMEOUT", raising=False)
    llm_interpreter._clear_cooldown()  # estado global limpio entre tests


def test_sin_key_usa_determinista() -> None:
    q = "necesito datos de precipitacion en el tolima"
    r = llm_interpreter.interpret_query(q)
    assert r["source"] == "deterministic"
    assert r["model"] is None
    assert r["fallback"] is False
    assert r["error"] is None
    assert r["intents"] == detect_intents(q)
    assert r["concepts"] == expand_concepts(q)
    assert r["need"] == primary_need_label(expand_concepts(q), q)


def test_respuesta_gemini_valida(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "clave-de-prueba")
    fake = {
        "intents": ["analizar", "descargar"],
        "need": "evaluar pérdida de bosque reciente",
        "concepts": ["deforestacion", "coberturas", "bosques", "colombia"],
    }

    def _fake_call(prompt, *, model, key, timeout):
        assert model == "gemini-3.7-flash"  # primer modelo de la cadena
        assert key == "clave-de-prueba"
        return fake

    monkeypatch.setattr(llm_interpreter, "_call_gemini", _fake_call)
    r = llm_interpreter.interpret_query("quiero ver la perdida de bosque")
    assert r["source"] == "gemini"
    assert r["model"] == "gemini-3.7-flash"
    assert r["intents"] == ["analizar", "descargar"]
    assert r["need"] == "evaluar pérdida de bosque reciente"
    # "colombia" es keyword genérica → filtrada; resto conservado
    assert r["concepts"] == ["deforestacion", "coberturas", "bosques"]


def test_cadena_de_modelos_ante_404(monkeypatch: pytest.MonkeyPatch) -> None:
    import urllib.error

    monkeypatch.setenv("GEMINI_API_KEY", "clave-de-prueba")
    calls: list[str] = []

    def _fake_call(prompt, *, model, key, timeout):
        calls.append(model)
        if model == "gemini-3.7-flash":
            raise urllib.error.HTTPError(
                "url", 404, "modelo retirado", {}, None
            )
        return {
            "intents": ["estudiar"],
            "need": "algo",
            "concepts": ["dem", "cuencas"],
        }

    monkeypatch.setattr(llm_interpreter, "_call_gemini", _fake_call)
    r = llm_interpreter.interpret_query("x")
    assert calls == ["gemini-3.7-flash", "gemini-3.1-pro-preview"]
    assert r["source"] == "gemini"
    assert r["model"] == "gemini-3.1-pro-preview"
    assert r["fallback"] is False


def test_gemini_error_cae_a_determinista(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "clave-de-prueba")

    def _fail(*args, **kwargs):
        raise TimeoutError("sin red")

    monkeypatch.setattr(llm_interpreter, "_call_gemini", _fail)
    q = "inundacion maritima"
    r = llm_interpreter.interpret_query(q)
    assert r["source"] == "deterministic"
    assert r["fallback"] is True
    assert "TimeoutError" in r["error"]
    assert r["intents"] == detect_intents(q)
    assert r["concepts"] == expand_concepts(q)


def test_gemini_json_invalido_cae_a_determinista(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "clave-de-prueba")
    monkeypatch.setattr(llm_interpreter, "_call_gemini", lambda *a, **k: "no soy json")
    r = llm_interpreter.interpret_query("erosion costera")
    assert r["source"] == "deterministic"
    assert r["fallback"] is True
    assert r["error"]


def test_intents_desconocidos_se_descartan(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "clave-de-prueba")
    monkeypatch.setattr(
        llm_interpreter,
        "_call_gemini",
        lambda *a, **k: {
            "intents": ["volar", "analizar"],
            "need": "algo",
            "concepts": ["a", "dem", "colombia", "suelos"],
        },
    )
    r = llm_interpreter.interpret_query("x")
    assert r["source"] == "gemini"
    assert r["intents"] == ["analizar"]  # "volar" no existe
    assert r["concepts"] == ["dem", "suelos"]  # "a" corto, "colombia" genérica


def test_circuit_breaker_evita_reintentos(monkeypatch: pytest.MonkeyPatch) -> None:
    import urllib.error

    monkeypatch.setenv("GEMINI_API_KEY", "clave-de-prueba")
    llamadas: list[str] = []

    def _fake_call(prompt, *, model, key, timeout):
        llamadas.append(model)
        raise urllib.error.HTTPError("url", 429, "cuota", {}, None)

    monkeypatch.setattr(llm_interpreter, "_call_gemini", _fake_call)

    # Primera consulta: intenta la cadena y entra en cooldown
    r1 = llm_interpreter.interpret_query("x")
    assert r1["fallback"] is True
    assert len(llamadas) >= 2  # reintento en el primer modelo
    llamadas.clear()

    # Segunda consulta: cooldown activo → fallback inmediato, sin llamadas
    r2 = llm_interpreter.interpret_query("y")
    assert r2["fallback"] is True
    assert "cooldown" in r2["error"]
    assert llamadas == []

    # Al liberar el cooldown, vuelve a intentar
    llm_interpreter._clear_cooldown()
    r3 = llm_interpreter.interpret_query("z")
    assert r3["fallback"] is True
    assert len(llamadas) >= 2
