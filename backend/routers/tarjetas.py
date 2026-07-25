from datetime import date, datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from auth import get_current_user
from database import get_session
from models import Tarjeta, TarjetaEstado, Usuario

router = APIRouter(prefix="/tarjetas", tags=["tarjetas"])


class TarjetaEstadoOut(BaseModel):
    tarjeta_id: str
    ease: float
    interval_dias: int
    repeticiones: int
    proxima_revision: date
    ultima_revision: Optional[datetime]


class RevisarIn(BaseModel):
    tarjeta_id: str
    grade: int  # 0 Otra vez, 1 Difícil, 2 Bien, 3 Fácil


class ResumenTarjetasOut(BaseModel):
    pendientes: int
    racha: int
    mejor_racha: int


def _get_estado(session: Session, usuario_id: int, tarjeta_id: str) -> Optional[TarjetaEstado]:
    return session.exec(
        select(TarjetaEstado).where(
            TarjetaEstado.usuario_id == usuario_id,
            TarjetaEstado.tarjeta_id == tarjeta_id,
        )
    ).first()


def _aplicar_sm2(estado: TarjetaEstado, grade: int) -> TarjetaEstado:
    """SM-2 simplificado a 4 botones (0 Otra vez, 1 Difícil, 2 Bien, 3 Fácil)."""
    if grade <= 0:
        estado.repeticiones = 0
        estado.interval_dias = 1
        estado.ease = max(1.3, estado.ease - 0.2)
    else:
        if estado.repeticiones == 0:
            estado.interval_dias = 1
        elif estado.repeticiones == 1:
            estado.interval_dias = 6
        else:
            estado.interval_dias = max(1, round(estado.interval_dias * estado.ease))
        estado.repeticiones += 1
        delta = {1: -0.15, 2: 0.0, 3: 0.15}.get(grade, 0.0)
        estado.ease = max(1.3, estado.ease + delta)
    estado.proxima_revision = date.today() + timedelta(days=estado.interval_dias)
    estado.ultima_revision = datetime.utcnow()
    return estado


def _streak_from_days(days: set) -> tuple[int, int]:
    if not days:
        return 0, 0
    today = date.today()
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


@router.get("/estado", response_model=list[TarjetaEstadoOut])
def get_estado(session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    estados = session.exec(select(TarjetaEstado).where(TarjetaEstado.usuario_id == current_user.id)).all()
    return estados


@router.post("/revisar", response_model=TarjetaEstadoOut)
def revisar_tarjeta(
    body: RevisarIn,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    if body.grade not in (0, 1, 2, 3):
        raise HTTPException(400, "grade debe ser 0, 1, 2 o 3")
    tarjeta = session.get(Tarjeta, body.tarjeta_id)
    if not tarjeta:
        raise HTTPException(404, f"Tarjeta '{body.tarjeta_id}' no encontrada")

    estado = _get_estado(session, current_user.id, body.tarjeta_id)
    if not estado:
        estado = TarjetaEstado(usuario_id=current_user.id, tarjeta_id=body.tarjeta_id)
    _aplicar_sm2(estado, body.grade)
    session.add(estado)
    session.commit()
    session.refresh(estado)
    return estado


@router.get("/resumen", response_model=ResumenTarjetasOut)
def get_resumen(session: Session = Depends(get_session), current_user: Usuario = Depends(get_current_user)):
    estados = session.exec(select(TarjetaEstado).where(TarjetaEstado.usuario_id == current_user.id)).all()
    hoy = date.today()
    pendientes = sum(1 for e in estados if e.proxima_revision <= hoy)
    dias = {e.ultima_revision.date() for e in estados if e.ultima_revision}
    racha, mejor_racha = _streak_from_days(dias)
    return ResumenTarjetasOut(pendientes=pendientes, racha=racha, mejor_racha=mejor_racha)
