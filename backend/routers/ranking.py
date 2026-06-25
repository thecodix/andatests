from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, func, select

from auth import get_current_user
from database import get_session
from models import Sesion, Usuario

router = APIRouter(tags=["ranking"])


class RankingEntry(BaseModel):
    pos: int
    nombre: str
    puntos: int
    es_yo: bool


@router.get("/ranking/semanal", response_model=list[RankingEntry])
def get_ranking_semanal(
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    since = datetime.now(timezone.utc) - timedelta(days=7)
    rows = session.exec(
        select(
            Sesion.usuario_id,
            func.sum(Sesion.aciertos).label("sum_aciertos"),
            func.count(Sesion.id).label("num_sesiones"),
        )
        .where(Sesion.created_at >= since)
        .group_by(Sesion.usuario_id)
    ).all()

    entries = []
    for usuario_id, sum_aciertos, num_sesiones in rows:
        user = session.get(Usuario, usuario_id)
        nombre = user.nombre if user else f"Usuario {usuario_id}"
        puntos = (sum_aciertos or 0) * 10 + (num_sesiones or 0) * 20
        entries.append({"nombre": nombre, "puntos": puntos, "es_yo": usuario_id == current_user.id})

    entries.sort(key=lambda e: e["puntos"], reverse=True)
    return [RankingEntry(pos=i + 1, **e) for i, e in enumerate(entries)]
