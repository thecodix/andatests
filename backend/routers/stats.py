from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import Integer, case
from sqlmodel import Session, func, select

from auth import get_current_user
from database import get_session
from models import Pregunta, Respuesta, Sesion, Tema, Usuario

router = APIRouter(prefix="/stats", tags=["stats"])


def _user_sesiones(session: Session, user_id: int):
    return session.exec(
        select(Sesion)
        .where(Sesion.usuario_id == user_id)
        .order_by(Sesion.created_at)
    ).all()


def _compute_streak(sesiones: list[Sesion]) -> tuple[int, int]:
    from datetime import date
    days: set[date] = {s.created_at.date() for s in sesiones}
    if not days:
        return 0, 0
    today = datetime.now(timezone.utc).date()
    current = 0
    d = today
    if d not in days and (d - timedelta(days=1)) not in days:
        current = 0
    else:
        if d not in days:
            d -= timedelta(days=1)
        while d in days:
            current += 1
            d -= timedelta(days=1)
    best, run, prev = 0, 0, None
    for day in sorted(days):
        run = run + 1 if prev and (day - prev).days == 1 else 1
        best = max(best, run)
        prev = day
    return current, best


def _tema_stats(session: Session, user_id: int) -> dict[int, dict]:
    rows = session.exec(
        select(
            Pregunta.tema_id,
            func.count(Respuesta.id).label("intentos"),
            func.sum(func.cast(Respuesta.correcta, Integer)).label("aciertos"),
        )
        .join(Respuesta.pregunta)
        .join(Respuesta.sesion)
        .where(Sesion.usuario_id == user_id)
        .group_by(Pregunta.tema_id)
    ).all()
    stats = {}
    for tema_id, intentos, aciertos in rows:
        aciertos = aciertos or 0
        pct = round(aciertos / intentos * 100) if intentos else 0
        stats[tema_id] = {"intentos": intentos, "aciertos": aciertos, "pct": pct, "seen": intentos > 0}
    return stats


class ResumenOut(BaseModel):
    acierto_global: int
    total_hechas: int
    total_preguntas: int
    prediccion: str
    num_falladas: int
    racha: int
    mejor_racha: int
    total_sesiones: int
    temas_flojos: int


class TemaStat(BaseModel):
    tema_id: int
    intentos: int
    aciertos: int
    pct: int
    seen: bool


class VistaOut(BaseModel):
    pregunta_id: str
    veces: int
    bien: int
    mal: int


@router.get("/resumen", response_model=ResumenOut)
def get_resumen(session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    sesiones = _user_sesiones(session, current_user.id)
    total_intentos = sum(s.total for s in sesiones)
    total_aciertos = sum(s.aciertos for s in sesiones)
    acierto_global = round(total_aciertos / total_intentos * 100) if total_intentos else 0
    total_preguntas = session.exec(select(func.count()).select_from(Pregunta)).one()

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
    num_falladas = sum(1 for _, mal, bien in rows if (mal or 0) - (bien or 0) > 0)

    racha, mejor_racha = _compute_streak(sesiones)
    tema_stats = _tema_stats(session, current_user.id)
    temas_flojos = sum(1 for s in tema_stats.values() if s["seen"] and s["pct"] < 55)

    return ResumenOut(
        acierto_global=acierto_global,
        total_hechas=total_intentos,
        total_preguntas=total_preguntas,
        prediccion=f"{acierto_global / 100 * 10:.1f}",
        num_falladas=num_falladas,
        racha=racha,
        mejor_racha=mejor_racha,
        total_sesiones=len(sesiones),
        temas_flojos=temas_flojos,
    )


@router.get("/por-tema", response_model=list[TemaStat])
def get_por_tema(session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    temas = session.exec(select(Tema).order_by(Tema.orden)).all()
    stats = _tema_stats(session, current_user.id)
    return [
        TemaStat(tema_id=t.id, **stats.get(t.id, {"intentos": 0, "aciertos": 0, "pct": 0, "seen": False}))
        for t in temas
    ]


@router.get("/vistas", response_model=list[VistaOut])
def get_vistas(
    tema_id: Optional[int] = Query(None),
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    """Por cada pregunta ya respondida por el usuario: cuántas veces la ha visto y
    cuántas la acertó/falló. Permite que la selección evite repetir preguntas."""
    stmt = (
        select(
            Respuesta.pregunta_id,
            func.count(Respuesta.id).label("veces"),
            func.sum(case((Respuesta.correcta == True, 1), else_=0)).label("bien"),  # noqa: E712
            func.sum(case((Respuesta.correcta == False, 1), else_=0)).label("mal"),  # noqa: E712
        )
        .join(Respuesta.sesion)
        .where(Sesion.usuario_id == current_user.id)
        .group_by(Respuesta.pregunta_id)
    )
    if tema_id is not None:
        stmt = stmt.join(Respuesta.pregunta).where(Pregunta.tema_id == tema_id)
    rows = session.exec(stmt).all()
    return [
        VistaOut(pregunta_id=pid, veces=veces, bien=bien or 0, mal=mal or 0)
        for pid, veces, bien, mal in rows
    ]


@router.get("/evolucion", response_model=list[int])
def get_evolucion(
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    sesiones = session.exec(
        select(Sesion)
        .where(Sesion.usuario_id == current_user.id)
        .order_by(Sesion.created_at.desc())
        .limit(limit)
    ).all()
    return [round(s.aciertos / s.total * 100) if s.total else 0 for s in reversed(sesiones)]


@router.get("/calendario", response_model=list[str])
def get_calendario(
    dias: int = Query(35, ge=7, le=365),
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    since = datetime.now(timezone.utc) - timedelta(days=dias)
    sesiones = session.exec(
        select(Sesion).where(Sesion.usuario_id == current_user.id, Sesion.created_at >= since)
    ).all()
    return sorted({s.created_at.date().isoformat() for s in sesiones})
