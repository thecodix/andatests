from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, EmailStr, field_validator
from sqlmodel import Session, select

from auth import (
    create_access_token,
    get_current_user,
    hash_password,
    hash_respuesta_seguridad,
    verify_password,
    verify_respuesta_seguridad,
)
from database import get_session
from models import Oposicion, Usuario, UsuarioOposicion
from rate_limit import limiter

router = APIRouter(prefix="/auth", tags=["auth"])

# Mensaje genérico para no revelar si el email existe o no tiene pregunta de
# seguridad configurada (evita enumeración de cuentas en este endpoint).
SIN_PREGUNTA_SEGURIDAD = "No es posible restablecer la contraseña para ese email todavía"


class RegisterIn(BaseModel):
    email: EmailStr
    nombre: str
    password: str
    # Por defecto la oposición ya existente: el frontend todavía no manda este
    # campo (selector pendiente), así que el registro actual sigue funcionando
    # igual hasta que se añada el selector de oposición al formulario.
    oposicion_id: int = 1
    pregunta_seguridad: str
    respuesta_seguridad: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        return v

    @field_validator("pregunta_seguridad", "respuesta_seguridad")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("La pregunta y la respuesta de seguridad no pueden estar vacías")
        return v


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class ResetIn(BaseModel):
    email: EmailStr


class PreguntaSeguridadOut(BaseModel):
    pregunta_seguridad: str


class ResetPasswordIn(BaseModel):
    email: EmailStr
    respuesta_seguridad: str
    nueva_password: str

    @field_validator("nueva_password")
    @classmethod
    def min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("La nueva contraseña debe tener al menos 8 caracteres")
        return v


class SecurityQuestionIn(BaseModel):
    pregunta_seguridad: str
    respuesta_seguridad: str

    @field_validator("pregunta_seguridad", "respuesta_seguridad")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("La pregunta y la respuesta de seguridad no pueden estar vacías")
        return v


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    nombre: str


class MeOut(BaseModel):
    id: int
    email: str
    nombre: str


@router.post("/register", response_model=TokenOut, status_code=201)
@limiter.limit("10/hour")
def register(request: Request, body: RegisterIn, session: Session = Depends(get_session)):
    existing = session.exec(select(Usuario).where(Usuario.email == body.email)).first()
    if existing:
        raise HTTPException(status.HTTP_409_CONFLICT, "Email ya registrado")
    oposicion = session.get(Oposicion, body.oposicion_id)
    if not oposicion:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Oposición no encontrada")
    user = Usuario(
        email=body.email,
        nombre=body.nombre,
        hashed_password=hash_password(body.password),
        pregunta_seguridad=body.pregunta_seguridad.strip(),
        respuesta_seguridad_hash=hash_respuesta_seguridad(body.respuesta_seguridad),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    session.add(UsuarioOposicion(usuario_id=user.id, oposicion_id=oposicion.id, favorita=True))
    session.commit()
    return TokenOut(access_token=create_access_token(user.id), nombre=user.nombre)


@router.post("/login", response_model=TokenOut)
@limiter.limit("5/minute")
def login(request: Request, body: LoginIn, session: Session = Depends(get_session)):
    user = session.exec(select(Usuario).where(Usuario.email == body.email)).first()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Email o contraseña incorrectos")
    return TokenOut(access_token=create_access_token(user.id), nombre=user.nombre)


@router.post("/reset-password/pregunta", response_model=PreguntaSeguridadOut)
@limiter.limit("5/minute")
def obtener_pregunta_seguridad(request: Request, body: ResetIn, session: Session = Depends(get_session)):
    """Primer paso del reseteo: devuelve la pregunta de seguridad del usuario,
    necesaria para poder responderla en el segundo paso."""
    user = session.exec(select(Usuario).where(Usuario.email == body.email)).first()
    if not user or not user.pregunta_seguridad or not user.respuesta_seguridad_hash:
        raise HTTPException(status.HTTP_404_NOT_FOUND, SIN_PREGUNTA_SEGURIDAD)
    return PreguntaSeguridadOut(pregunta_seguridad=user.pregunta_seguridad)


@router.post("/reset-password", response_model=TokenOut)
@limiter.limit("5/minute")
def reset_password(request: Request, body: ResetPasswordIn, session: Session = Depends(get_session)):
    """Segundo paso del reseteo: verifica la respuesta de seguridad y, si
    coincide, establece la nueva contraseña elegida por el usuario."""
    user = session.exec(select(Usuario).where(Usuario.email == body.email)).first()
    if not user or not user.pregunta_seguridad or not user.respuesta_seguridad_hash:
        raise HTTPException(status.HTTP_404_NOT_FOUND, SIN_PREGUNTA_SEGURIDAD)
    if not verify_respuesta_seguridad(body.respuesta_seguridad, user.respuesta_seguridad_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Respuesta de seguridad incorrecta")
    user.hashed_password = hash_password(body.nueva_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return TokenOut(access_token=create_access_token(user.id), nombre=user.nombre)


@router.put("/security-question", response_model=MeOut)
def set_security_question(
    body: SecurityQuestionIn,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    """Permite a un usuario ya autenticado configurar o cambiar su pregunta de
    seguridad — necesario para cuentas creadas antes de esta funcionalidad."""
    current_user.pregunta_seguridad = body.pregunta_seguridad.strip()
    current_user.respuesta_seguridad_hash = hash_respuesta_seguridad(body.respuesta_seguridad)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return MeOut(id=current_user.id, email=current_user.email, nombre=current_user.nombre)


@router.get("/me", response_model=MeOut)
def me(current_user: Usuario = Depends(get_current_user)):
    return MeOut(id=current_user.id, email=current_user.email, nombre=current_user.nombre)
