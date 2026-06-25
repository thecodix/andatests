import random
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import case
from sqlmodel import Session, func, select

from auth import get_current_user
from database import get_session
from models import Pregunta, Respuesta, Sesion, Tema, Usuario

router = APIRouter(tags=["contenido"])


class TemaOut(BaseModel):
    id: int
    titulo: str
    ley: str
    orden: int
    total_preguntas: int


class PreguntaOut(BaseModel):
    id: str
    tema_id: int
    enunciado: str
    opciones: list[str]
    correcta: int
    ref: str
    explicacion: str


class FalladaOut(PreguntaOut):
    veces: int


@router.get("/temas", response_model=list[TemaOut])
def get_temas(session: Session = Depends(get_session), _: Usuario = Depends(get_current_user)):
    temas = session.exec(select(Tema).order_by(Tema.orden)).all()
    result = []
    for t in temas:
        count = session.exec(select(func.count()).where(Pregunta.tema_id == t.id)).one()
        result.append(TemaOut(id=t.id, titulo=t.titulo, ley=t.ley, orden=t.orden, total_preguntas=count))
    return result


@router.get("/temas/{tema_id}/preguntas", response_model=list[PreguntaOut])
def get_preguntas(tema_id: int, session: Session = Depends(get_session), _: Usuario = Depends(get_current_user)):
    tema = session.get(Tema, tema_id)
    if not tema:
        raise HTTPException(404, f"Tema {tema_id} no encontrado")
    return session.exec(select(Pregunta).where(Pregunta.tema_id == tema_id)).all()


@router.get("/preguntas/aleatorias", response_model=list[PreguntaOut])
def get_aleatorias(
    n: int = Query(10, ge=1, le=100),
    temas: Optional[str] = Query(None),
    session: Session = Depends(get_session),
    _: Usuario = Depends(get_current_user),
):
    stmt = select(Pregunta)
    if temas:
        ids = [int(x) for x in temas.split(",") if x.strip().isdigit()]
        stmt = stmt.where(Pregunta.tema_id.in_(ids))
    all_qs = session.exec(stmt).all()
    return random.sample(all_qs, min(n, len(all_qs)))


@router.get("/falladas", response_model=list[FalladaOut])
def get_falladas(
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    rows = session.exec(
        select(
            Respuesta.pregunta_id,
            func.sum(case((Respuesta.correcta == False, 1), else_=0)).label("mal"),  # noqa: E712
            func.sum(case((Respuesta.correcta == True, 1), else_=0)).label("bien"),  # noqa: E712
        )
        .join(Respuesta.sesion)
        .where(Sesion.usuario_id == current_user.id)
        .group_by(Respuesta.pregunta_id)
    ).all()

    falladas = []
    for pregunta_id, mal, bien in rows:
        if (mal or 0) - (bien or 0) > 0:
            p = session.get(Pregunta, pregunta_id)
            if p:
                falladas.append(FalladaOut(
                    id=p.id, tema_id=p.tema_id, enunciado=p.enunciado,
                    opciones=p.opciones, correcta=p.correcta,
                    ref=p.ref, explicacion=p.explicacion, veces=(mal or 0) - (bien or 0),
                ))
    falladas.sort(key=lambda f: f.veces, reverse=True)
    return falladas
