from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session

from auth import get_current_user
from database import get_session
from models import FeedbackMode, ModoTest, Pregunta, Respuesta, Sesion, Usuario

router = APIRouter(tags=["sesiones"])


class RespuestaIn(BaseModel):
    pregunta_id: str
    elegida: Optional[int] = None


class SesionIn(BaseModel):
    modo: ModoTest
    feedback: FeedbackMode
    tema_id: Optional[int] = None
    segundos: Optional[int] = None
    respuestas: list[RespuestaIn]


class SesionOut(BaseModel):
    sesion_id: int
    aciertos: int
    total: int
    pct: int
    nota: str


@router.post("/sesiones", response_model=SesionOut, status_code=201)
def create_sesion(
    body: SesionIn,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    if not body.respuestas:
        raise HTTPException(400, "La sesión debe tener al menos una respuesta")

    respuestas_out: list[Respuesta] = []
    aciertos = 0

    for r in body.respuestas:
        p = session.get(Pregunta, r.pregunta_id)
        if not p:
            raise HTTPException(404, f"Pregunta '{r.pregunta_id}' no encontrada")
        is_correct = r.elegida == p.correcta
        if is_correct:
            aciertos += 1
        respuestas_out.append(Respuesta(
            pregunta_id=r.pregunta_id,
            elegida=r.elegida,
            correcta=is_correct,
        ))

    total = len(body.respuestas)
    pct = round(aciertos / total * 100) if total else 0

    sesion = Sesion(
        usuario_id=current_user.id,
        modo=body.modo,
        feedback=body.feedback,
        tema_id=body.tema_id,
        total=total,
        aciertos=aciertos,
        segundos=body.segundos,
    )
    session.add(sesion)
    session.flush()

    for r in respuestas_out:
        r.sesion_id = sesion.id
        session.add(r)

    session.commit()
    session.refresh(sesion)

    return SesionOut(
        sesion_id=sesion.id,
        aciertos=aciertos,
        total=total,
        pct=pct,
        nota=f"{pct / 100 * 10:.1f}",
    )
