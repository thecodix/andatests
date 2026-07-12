from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlmodel import Session, select

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


class SesionListItem(BaseModel):
    id: int
    modo: ModoTest
    feedback: FeedbackMode
    tema_id: Optional[int]
    total: int
    aciertos: int
    pct: int
    segundos: Optional[int]
    created_at: datetime


class RespuestaDetalle(BaseModel):
    pregunta_id: str
    tema_id: int
    enunciado: str
    opciones: list[str]
    elegida: Optional[int]
    correcta_idx: int
    acertada: bool


class SesionDetalle(SesionListItem):
    respuestas: list[RespuestaDetalle]


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


@router.get("/sesiones", response_model=list[SesionListItem])
def list_sesiones(
    limit: int = Query(50, ge=1, le=500),
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    sesiones = session.exec(
        select(Sesion)
        .where(Sesion.usuario_id == current_user.id)
        .order_by(Sesion.created_at.desc())
        .limit(limit)
    ).all()
    return [
        SesionListItem(
            id=s.id, modo=s.modo, feedback=s.feedback, tema_id=s.tema_id,
            total=s.total, aciertos=s.aciertos,
            pct=round(s.aciertos / s.total * 100) if s.total else 0,
            segundos=s.segundos, created_at=s.created_at,
        )
        for s in sesiones
    ]


@router.delete("/sesiones/{sesion_id}", status_code=204)
def delete_sesion(
    sesion_id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    s = session.get(Sesion, sesion_id)
    if not s or s.usuario_id != current_user.id:
        raise HTTPException(404, "Sesión no encontrada")

    for r in s.respuestas:
        session.delete(r)
    session.delete(s)
    session.commit()


@router.get("/sesiones/{sesion_id}", response_model=SesionDetalle)
def get_sesion(
    sesion_id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    s = session.get(Sesion, sesion_id)
    if not s or s.usuario_id != current_user.id:
        raise HTTPException(404, "Sesión no encontrada")

    respuestas: list[RespuestaDetalle] = []
    for r in s.respuestas:
        p = session.get(Pregunta, r.pregunta_id)
        respuestas.append(RespuestaDetalle(
            pregunta_id=r.pregunta_id,
            tema_id=p.tema_id if p else 0,
            enunciado=p.enunciado if p else "(pregunta no disponible)",
            opciones=p.opciones if p else [],
            elegida=r.elegida,
            correcta_idx=p.correcta if p else -1,
            acertada=r.correcta,
        ))

    return SesionDetalle(
        id=s.id, modo=s.modo, feedback=s.feedback, tema_id=s.tema_id,
        total=s.total, aciertos=s.aciertos,
        pct=round(s.aciertos / s.total * 100) if s.total else 0,
        segundos=s.segundos, created_at=s.created_at,
        respuestas=respuestas,
    )
