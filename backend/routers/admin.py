from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, func, select

from auth import require_admin
from database import get_session
from models import LoginEvento, Respuesta, Sesion, Usuario

router = APIRouter(prefix="/admin", tags=["admin"])


class ResumenAdminOut(BaseModel):
    total_usuarios: int
    usuarios_nuevos_7d: int
    total_sesiones: int
    sesiones_hoy: int
    sesiones_7d: int
    total_respuestas: int
    logins_hoy: int
    logins_7d: int
    usuarios_activos_7d: int


class UsuarioAdminOut(BaseModel):
    id: int
    email: str
    nombre: str
    created_at: datetime
    ultimo_login: Optional[datetime]
    total_sesiones: int
    total_preguntas_respondidas: int
    acierto_pct: int


@router.get("/resumen", response_model=ResumenAdminOut)
def get_resumen_admin(
    session: Session = Depends(get_session),
    _admin: Usuario = Depends(require_admin),
):
    ahora = datetime.utcnow()
    hace_7d = ahora - timedelta(days=7)
    hoy = ahora.date()

    total_usuarios = session.exec(select(func.count()).select_from(Usuario)).one()
    usuarios_nuevos_7d = session.exec(
        select(func.count()).select_from(Usuario).where(Usuario.created_at >= hace_7d)
    ).one()
    total_sesiones = session.exec(select(func.count()).select_from(Sesion)).one()
    sesiones = session.exec(select(Sesion.created_at)).all()
    sesiones_hoy = sum(1 for c in sesiones if c.date() == hoy)
    sesiones_7d = sum(1 for c in sesiones if c >= hace_7d)
    total_respuestas = session.exec(select(func.count()).select_from(Respuesta)).one()

    logins = session.exec(select(LoginEvento.created_at)).all()
    logins_hoy = sum(1 for c in logins if c.date() == hoy)
    logins_7d = sum(1 for c in logins if c >= hace_7d)

    usuarios_activos_7d = session.exec(
        select(func.count(func.distinct(Sesion.usuario_id))).where(Sesion.created_at >= hace_7d)
    ).one()

    return ResumenAdminOut(
        total_usuarios=total_usuarios,
        usuarios_nuevos_7d=usuarios_nuevos_7d,
        total_sesiones=total_sesiones,
        sesiones_hoy=sesiones_hoy,
        sesiones_7d=sesiones_7d,
        total_respuestas=total_respuestas,
        logins_hoy=logins_hoy,
        logins_7d=logins_7d,
        usuarios_activos_7d=usuarios_activos_7d,
    )


@router.get("/usuarios", response_model=list[UsuarioAdminOut])
def get_usuarios_admin(
    session: Session = Depends(get_session),
    _admin: Usuario = Depends(require_admin),
):
    usuarios = session.exec(select(Usuario).order_by(Usuario.created_at.desc())).all()

    sesiones_por_usuario: dict[int, list[Sesion]] = {}
    for s in session.exec(select(Sesion)).all():
        sesiones_por_usuario.setdefault(s.usuario_id, []).append(s)

    ultimo_login_por_usuario: dict[int, datetime] = {}
    for usuario_id, created_at in session.exec(
        select(LoginEvento.usuario_id, LoginEvento.created_at).order_by(LoginEvento.created_at)
    ).all():
        ultimo_login_por_usuario[usuario_id] = created_at

    out = []
    for u in usuarios:
        sesiones = sesiones_por_usuario.get(u.id, [])
        total_preguntas = sum(s.total for s in sesiones)
        total_aciertos = sum(s.aciertos for s in sesiones)
        acierto_pct = round(total_aciertos / total_preguntas * 100) if total_preguntas else 0
        out.append(
            UsuarioAdminOut(
                id=u.id,
                email=u.email,
                nombre=u.nombre,
                created_at=u.created_at,
                ultimo_login=ultimo_login_por_usuario.get(u.id),
                total_sesiones=len(sesiones),
                total_preguntas_respondidas=total_preguntas,
                acierto_pct=acierto_pct,
            )
        )
    return out
