"""Thin wrapper to call Groq's chat completions API for the student assistant.

Kept separate from lib/llm.js (used offline by the Node content-generation
scripts) because this runs inside the FastAPI request/response cycle.
"""
import re
import time

import httpx

from config import settings

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


class LLMError(Exception):
    pass


def _parse_retry_after_ms(body: str) -> float | None:
    """Parses Groq's "Please try again in 12.34s" / "...in 1m2.5s" hint."""
    m = re.search(r"try again in ([\d.]+)m?([\d.]+)?s", body)
    if not m:
        return None
    if m.group(2) is not None:
        return (float(m.group(1)) * 60 + float(m.group(2))) * 1000
    return float(m.group(1)) * 1000


def ask_groq(
    system: str,
    historial: list[dict],
    mensaje: str,
    max_tokens: int = 800,
    retries: int = 2,
    json_mode: bool = False,
) -> str:
    if not settings.groq_api_key:
        raise LLMError("GROQ_API_KEY no configurada en el servidor.")

    messages = [{"role": "system", "content": system}, *historial, {"role": "user", "content": mensaje}]

    payload = {
        "model": settings.groq_model,
        "max_tokens": max_tokens,
        "temperature": 0.3,
        "messages": messages,
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    last_error = ""
    for attempt in range(retries + 1):
        try:
            resp = httpx.post(
                GROQ_URL,
                headers={"Authorization": f"Bearer {settings.groq_api_key}"},
                json=payload,
                timeout=30,
            )
        except httpx.HTTPError as e:
            last_error = str(e)
            if attempt < retries:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise LLMError(f"Error de conexión con Groq: {last_error}") from e

        if resp.status_code == 200:
            data = resp.json()
            content = data.get("choices", [{}])[0].get("message", {}).get("content")
            if not content:
                raise LLMError("Groq devolvió una respuesta vacía.")
            return content

        is_rate_limit = resp.status_code == 429 or "rate_limit_exceeded" in resp.text
        if is_rate_limit and attempt < retries:
            wait_ms = _parse_retry_after_ms(resp.text) or 3000 * (attempt + 1)
            time.sleep(wait_ms / 1000)
            continue

        raise LLMError(f"Groq API error {resp.status_code}: {resp.text[:300]}")

    raise LLMError("No se pudo obtener respuesta de Groq.")
