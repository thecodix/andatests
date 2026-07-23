"""Construye el contexto que se le pasa al LLM del asistente de estudio.

No usa embeddings ni una base vectorial: el corpus (banco/temaN.json, ya
cargado en la BD) es pequeño y cada pregunta ya trae su artículo de
referencia y explicación auditados, así que un scoring simple por
solapamiento de palabras entre la pregunta del alumno y el enunciado /
explicación / referencia de cada `Pregunta` es suficiente para elegir qué
incluir como contexto.
"""
import re

from sqlmodel import Session, select

from models import Pregunta, Tema

_WORD_RE = re.compile(r"[a-záéíóúñü]{4,}", re.IGNORECASE)

# Palabras demasiado frecuentes en el temario como para discriminar nada.
_STOPWORDS = {
    "para", "como", "este", "esta", "estos", "estas", "sobre", "entre", "cual",
    "cuales", "según", "cuando", "donde", "desde", "hasta", "cada", "cuyo",
    "cuya", "puede", "podrá", "deberá", "serán", "dicho", "dicha", "artículo",
}


def _words(text: str) -> set[str]:
    return {w.lower() for w in _WORD_RE.findall(text or "") if w.lower() not in _STOPWORDS}


def contexto_tema(session: Session, tema_id: int, mensaje: str, k: int = 8) -> list[Pregunta]:
    """Devuelve las `k` preguntas del tema más relevantes para `mensaje`."""
    preguntas = session.exec(select(Pregunta).where(Pregunta.tema_id == tema_id)).all()
    query_words = _words(mensaje)
    if not query_words:
        return preguntas[:k]

    def score(p: Pregunta) -> int:
        return len(query_words & _words(f"{p.enunciado} {p.explicacion} {p.ref}"))

    ranked = sorted(preguntas, key=score, reverse=True)
    # Si nada solapa (pregunta muy genérica), igualmente devolvemos una muestra
    # para que el asistente tenga algo de contexto del tema.
    return ranked[:k] if score(ranked[0]) > 0 else preguntas[:k]


def muestra_tema(session: Session, tema_id: int, k: int = 6) -> list[Pregunta]:
    """Muestra representativa (espaciada, no aleatoria) de preguntas del tema,
    pensada para dar contexto de estilo/contenido sin sesgar hacia el principio
    del banco. Usada para generar preguntas nuevas por el LLM."""
    preguntas = session.exec(select(Pregunta).where(Pregunta.tema_id == tema_id)).all()
    n = len(preguntas)
    if n <= k:
        return preguntas
    idxs = sorted({int(i * n / k) for i in range(k)})
    return [preguntas[i] for i in idxs]


def formatea_contexto(tema: Tema, preguntas: list[Pregunta]) -> str:
    bloques = [f"Tema {tema.id}: {tema.titulo} ({tema.ley})", ""]
    for p in preguntas:
        opciones = "; ".join(f"{chr(65 + i)}) {o}" for i, o in enumerate(p.opciones))
        correcta = p.opciones[p.correcta] if 0 <= p.correcta < len(p.opciones) else ""
        bloques.append(
            f"- Pregunta: {p.enunciado}\n"
            f"  Opciones: {opciones}\n"
            f"  Correcta: {correcta}\n"
            f"  Referencia: {p.ref}\n"
            f"  Explicación: {p.explicacion}"
        )
    return "\n".join(bloques)
