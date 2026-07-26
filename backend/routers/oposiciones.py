from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlmodel import Session, select

from auth import get_current_user
from database import get_session
from models import Oposicion, Usuario, UsuarioOposicion

router = APIRouter(tags=["oposiciones"])


class OposicionOut(BaseModel):
    id: int
    slug: str
    nombre: str
    descripcion: str | None = None


class MiOposicionOut(OposicionOut):
    favorita: bool


class AddOposicionIn(BaseModel):
    oposicion_id: int


@router.get("/oposiciones", response_model=list[OposicionOut])
def get_oposiciones(session: Session = Depends(get_session)):
    """Listado público de oposiciones disponibles (usado en el registro y al
    añadir una oposición nueva a una cuenta ya existente)."""
    return session.exec(select(Oposicion).order_by(Oposicion.id)).all()


@router.get("/me/oposiciones", response_model=list[MiOposicionOut])
def get_mis_oposiciones(
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    rows = session.exec(
        select(UsuarioOposicion, Oposicion)
        .where(UsuarioOposicion.usuario_id == current_user.id)
        .where(UsuarioOposicion.oposicion_id == Oposicion.id)
        .order_by(Oposicion.id)
    ).all()
    return [
        MiOposicionOut(
            id=oposicion.id,
            slug=oposicion.slug,
            nombre=oposicion.nombre,
            descripcion=oposicion.descripcion,
            favorita=uo.favorita,
        )
        for uo, oposicion in rows
    ]


@router.post("/me/oposiciones", response_model=list[MiOposicionOut], status_code=status.HTTP_201_CREATED)
def add_mi_oposicion(
    body: AddOposicionIn,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    """Añade una oposición a la cuenta del usuario. La primera que se añade
    (incluida la del registro) queda como favorita; el resto no, salvo que
    luego se marque explícitamente vía PUT .../favorita."""
    oposicion = session.get(Oposicion, body.oposicion_id)
    if not oposicion:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Oposición no encontrada")

    ya_anadida = session.exec(
        select(UsuarioOposicion).where(
            UsuarioOposicion.usuario_id == current_user.id,
            UsuarioOposicion.oposicion_id == oposicion.id,
        )
    ).first()
    if ya_anadida:
        raise HTTPException(status.HTTP_409_CONFLICT, "Ya tienes añadida esa oposición")

    tiene_alguna = session.exec(
        select(UsuarioOposicion).where(UsuarioOposicion.usuario_id == current_user.id)
    ).first()
    session.add(UsuarioOposicion(
        usuario_id=current_user.id,
        oposicion_id=oposicion.id,
        favorita=tiene_alguna is None,
    ))
    session.commit()
    return get_mis_oposiciones(session=session, current_user=current_user)


@router.put("/me/oposiciones/{oposicion_id}/favorita", response_model=list[MiOposicionOut])
def marcar_favorita(
    oposicion_id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    objetivo = session.exec(
        select(UsuarioOposicion).where(
            UsuarioOposicion.usuario_id == current_user.id,
            UsuarioOposicion.oposicion_id == oposicion_id,
        )
    ).first()
    if not objetivo:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No tienes añadida esa oposición")

    todas = session.exec(
        select(UsuarioOposicion).where(UsuarioOposicion.usuario_id == current_user.id)
    ).all()
    for uo in todas:
        uo.favorita = uo.oposicion_id == oposicion_id
        session.add(uo)
    session.commit()
    return get_mis_oposiciones(session=session, current_user=current_user)
