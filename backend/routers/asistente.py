from datetime import date
import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

import knowledge
import llm
from auth import get_current_user
from config import settings
from database import get_session
from models import AsistenteMensaje, AsistenteUso, Pregunta, Tema, Usuario

router = APIRouter(prefix="/asistente", tags=["asistente"])

SYSTEM_BASE = (
    "Eres el tutor de estudio de Andatest, una app para preparar la oposición de "
    "Escala Auxiliar Administrativa (C2) de la Universidad de Huelva. "
    "Responde SOLO apoyándote en el contexto proporcionado (preguntas ya auditadas "
    "del banco de la app, con su artículo de referencia y explicación oficial). "
    "Si el contexto no cubre lo que se pregunta, dilo claramente en vez de inventar "
    "una respuesta. Sé breve y claro, cita el artículo (campo Referencia) cuando "
    "esté disponible, y responde siempre en español."
)

HISTORIAL_MAX = 60


class MensajeIn(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatIn(BaseModel):
    mensaje: str
    tema_id: int
    pregunta_id: str | None = None
    historial: list[MensajeIn] = []


class ChatOut(BaseModel):
    respuesta: str


class MensajeOut(BaseModel):
    role: str
    content: str


class HistorialOut(BaseModel):
    mensajes: list[MensajeOut]


class PreguntaPersonalizadaIn(BaseModel):
    tema_id: int


class PreguntaPersonalizadaOut(BaseModel):
    enunciado: str
    opciones: list[str]
    correcta: int
    ref: str
    explicacion: str


class MensajeQuizIn(BaseModel):
    tema_id: int
    elegida_texto: str
    feedback_texto: str


def _check_y_registra_limite(session: Session, usuario_id: int) -> None:
    hoy = date.today()
    uso = session.exec(
        select(AsistenteUso).where(AsistenteUso.usuario_id == usuario_id, AsistenteUso.fecha == hoy)
    ).first()
    if uso is None:
        uso = AsistenteUso(usuario_id=usuario_id, fecha=hoy, mensajes=0)
    if uso.mensajes >= settings.asistente_limite_diario:
        raise HTTPException(429, "Has alcanzado el límite diario de preguntas al asistente. Vuelve mañana.")
    uso.mensajes += 1
    session.add(uso)
    session.commit()


def _guarda_mensaje(session: Session, usuario_id: int, tema_id: int, role: str, content: str) -> None:
    session.add(AsistenteMensaje(usuario_id=usuario_id, tema_id=tema_id, role=role, content=content))
    session.commit()


@router.get("/historial", response_model=HistorialOut)
def historial(
    tema_id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    tema = session.get(Tema, tema_id)
    if not tema:
        raise HTTPException(404, f"Tema {tema_id} no encontrado")
    mensajes = session.exec(
        select(AsistenteMensaje)
        .where(AsistenteMensaje.usuario_id == current_user.id, AsistenteMensaje.tema_id == tema_id)
        .order_by(AsistenteMensaje.created_at)
    ).all()
    mensajes = mensajes[-HISTORIAL_MAX:]
    return HistorialOut(mensajes=[MensajeOut(role=m.role, content=m.content) for m in mensajes])


@router.post("/chat", response_model=ChatOut)
def chat(
    body: ChatIn,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    tema = session.get(Tema, body.tema_id)
    if not tema:
        raise HTTPException(404, f"Tema {body.tema_id} no encontrado")

    if body.pregunta_id:
        pregunta = session.get(Pregunta, body.pregunta_id)
        if not pregunta or pregunta.tema_id != body.tema_id:
            raise HTTPException(404, "Pregunta no encontrada")
        contexto = knowledge.formatea_contexto(tema, [pregunta])
        system = (
            f"{SYSTEM_BASE}\n\nEl alumno tiene dudas sobre esta pregunta concreta, "
            f"que ya ha fallado antes:\n\n{contexto}"
        )
    else:
        preguntas = knowledge.contexto_tema(session, body.tema_id, body.mensaje)
        contexto = knowledge.formatea_contexto(tema, preguntas)
        system = f"{SYSTEM_BASE}\n\nContexto relevante del tema:\n\n{contexto}"

    _check_y_registra_limite(session, current_user.id)

    historial_msgs = [{"role": m.role, "content": m.content} for m in body.historial[-6:]]
    try:
        respuesta = llm.ask_groq(system=system, historial=historial_msgs, mensaje=body.mensaje)
    except llm.LLMError as e:
        raise HTTPException(502, str(e))

    _guarda_mensaje(session, current_user.id, body.tema_id, "user", body.mensaje)
    _guarda_mensaje(session, current_user.id, body.tema_id, "assistant", respuesta)

    return ChatOut(respuesta=respuesta)


@router.post("/pregunta-personalizada", response_model=PreguntaPersonalizadaOut)
def pregunta_personalizada(
    body: PreguntaPersonalizadaIn,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    tema = session.get(Tema, body.tema_id)
    if not tema:
        raise HTTPException(404, f"Tema {body.tema_id} no encontrado")

    _check_y_registra_limite(session, current_user.id)

    muestra = knowledge.muestra_tema(session, body.tema_id, k=6)
    if not muestra:
        raise HTTPException(404, f"El tema {body.tema_id} no tiene preguntas en el banco todavía")
    contexto = knowledge.formatea_contexto(tema, muestra)

    system = (
        "Eres un generador de preguntas tipo test para practicar el temario de la "
        "oposición de Escala Auxiliar Administrativa (C2) de la Universidad de Huelva. "
        "A partir del contexto (preguntas ya auditadas de ese tema, con su artículo y "
        "explicación oficiales), genera UNA pregunta tipo test NUEVA y ORIGINAL — no "
        "copies literalmente ninguna de las de abajo — que evalúe la comprensión del "
        "mismo contenido. Devuelve EXCLUSIVAMENTE un objeto JSON con este formato exacto, "
        "sin texto adicional ni markdown:\n"
        '{"enunciado": "...", "opciones": ["...", "...", "...", "..."], "correcta": 0, '
        '"ref": "...", "explicacion": "..."}\n'
        '"opciones" debe tener exactamente 4 elementos y "correcta" es el índice (0-3) '
        "de la opción correcta. Responde siempre en español.\n\n"
        f"Contexto:\n\n{contexto}"
    )
    try:
        raw = llm.ask_groq(system=system, historial=[], mensaje="Genera la pregunta.", max_tokens=600, json_mode=True)
    except llm.LLMError as e:
        raise HTTPException(502, str(e))

    try:
        data = json.loads(raw)
        opciones = data["opciones"]
        correcta = int(data["correcta"])
        enunciado = str(data["enunciado"]).strip()
        ref = str(data.get("ref", "")).strip()
        explicacion = str(data.get("explicacion", "")).strip()
        if not isinstance(opciones, list) or len(opciones) != 4 or not (0 <= correcta < 4) or not enunciado:
            raise ValueError("formato inesperado")
        opciones = [str(o) for o in opciones]
    except Exception:
        raise HTTPException(502, "El asistente generó un formato inválido, inténtalo de nuevo.")

    letras = "ABCD"
    texto_msg = f"📝 Pregunta nueva:\n\n{enunciado}\n\n" + "\n".join(
        f"{letras[i]}) {o}" for i, o in enumerate(opciones)
    )
    _guarda_mensaje(session, current_user.id, body.tema_id, "assistant", texto_msg)

    return PreguntaPersonalizadaOut(
        enunciado=enunciado, opciones=opciones, correcta=correcta, ref=ref, explicacion=explicacion
    )


@router.post("/mensaje-quiz")
def mensaje_quiz(
    body: MensajeQuizIn,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    """Persiste la respuesta del alumno a una pregunta personalizada y el feedback
    (calculado en el cliente, sin nueva llamada al LLM ni consumo del límite diario)."""
    tema = session.get(Tema, body.tema_id)
    if not tema:
        raise HTTPException(404, f"Tema {body.tema_id} no encontrado")
    _guarda_mensaje(session, current_user.id, body.tema_id, "user", body.elegida_texto)
    _guarda_mensaje(session, current_user.id, body.tema_id, "assistant", body.feedback_texto)
    return {"ok": True}
