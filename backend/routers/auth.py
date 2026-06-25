from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlmodel import Session, select

from auth import create_access_token, get_current_user, hash_password, verify_password
from database import get_session
from models import Usuario

router = APIRouter(prefix="/auth", tags=["auth"])


class RegisterIn(BaseModel):
    email: EmailStr
    nombre: str
    password: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    nombre: str


class MeOut(BaseModel):
    id: int
    email: str
    nombre: str


@router.post("/register", response_model=TokenOut, status_code=201)
def register(body: RegisterIn, session: Session = Depends(get_session)):
    existing = session.exec(select(Usuario).where(Usuario.email == body.email)).first()
    if existing:
        raise HTTPException(status.HTTP_409_CONFLICT, "Email ya registrado")
    user = Usuario(
        email=body.email,
        nombre=body.nombre,
        hashed_password=hash_password(body.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return TokenOut(access_token=create_access_token(user.id), nombre=user.nombre)


@router.post("/login", response_model=TokenOut)
def login(body: LoginIn, session: Session = Depends(get_session)):
    user = session.exec(select(Usuario).where(Usuario.email == body.email)).first()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Email o contraseña incorrectos")
    return TokenOut(access_token=create_access_token(user.id), nombre=user.nombre)


@router.get("/me", response_model=MeOut)
def me(current_user: Usuario = Depends(get_current_user)):
    return MeOut(id=current_user.id, email=current_user.email, nombre=current_user.nombre)
