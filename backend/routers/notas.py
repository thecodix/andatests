from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from auth import get_current_user
from database import get_session
from models import NotaDia, Usuario

router = APIRouter(prefix="/notas", tags=["notas"])


class NotaOut(BaseModel):
    id: int
    fecha: date
    contenido: str


class NotaCreate(BaseModel):
    fecha: date
    contenido: str


class NotaUpdate(BaseModel):
    contenido: str


def _nota_propia(nota_id: int, session: Session, current_user: Usuario) -> NotaDia:
    nota = session.get(NotaDia, nota_id)
    if not nota or nota.usuario_id != current_user.id:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    return nota


@router.get("", response_model=list[NotaOut])
def listar_notas(
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    notas = session.exec(
        select(NotaDia).where(NotaDia.usuario_id == current_user.id)
    ).all()
    return [NotaOut(id=n.id, fecha=n.fecha, contenido=n.contenido) for n in notas]


@router.post("", response_model=NotaOut, status_code=201)
def crear_nota(
    body: NotaCreate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    contenido = body.contenido.strip()
    if not contenido:
        raise HTTPException(status_code=400, detail="La nota no puede estar vacía")
    nota = NotaDia(usuario_id=current_user.id, fecha=body.fecha, contenido=contenido)
    session.add(nota)
    session.commit()
    session.refresh(nota)
    return NotaOut(id=nota.id, fecha=nota.fecha, contenido=nota.contenido)


@router.put("/{nota_id}", response_model=NotaOut)
def actualizar_nota(
    nota_id: int,
    body: NotaUpdate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    nota = _nota_propia(nota_id, session, current_user)
    contenido = body.contenido.strip()
    if not contenido:
        raise HTTPException(status_code=400, detail="La nota no puede estar vacía")
    nota.contenido = contenido
    nota.updated_at = datetime.utcnow()
    session.add(nota)
    session.commit()
    session.refresh(nota)
    return NotaOut(id=nota.id, fecha=nota.fecha, contenido=nota.contenido)


@router.delete("/{nota_id}", status_code=204)
def borrar_nota(
    nota_id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    nota = _nota_propia(nota_id, session, current_user)
    session.delete(nota)
    session.commit()
