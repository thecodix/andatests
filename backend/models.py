from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Column
from sqlalchemy import Enum as SAEnum
from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel


class ModoTest(str, Enum):
    tema = "tema"
    aleatorio = "aleatorio"
    simulacro = "simulacro"
    falladas = "falladas"


class FeedbackMode(str, Enum):
    inmediato = "inmediato"
    final = "final"


# ---------------------------------------------------------------------------
# Tables
# ---------------------------------------------------------------------------


class Tema(SQLModel, table=True):
    id: int = Field(primary_key=True)
    titulo: str
    ley: str
    orden: int

    preguntas: list["Pregunta"] = Relationship(back_populates="tema")


class Pregunta(SQLModel, table=True):
    id: str = Field(primary_key=True)  # "{tema_id}_{indice}", stable
    tema_id: int = Field(foreign_key="tema.id", index=True)
    enunciado: str
    opciones: list[str] = Field(sa_column=Column(JSON, nullable=False))
    correcta: int
    ref: str
    explicacion: str

    tema: Optional[Tema] = Relationship(back_populates="preguntas")
    respuestas: list["Respuesta"] = Relationship(back_populates="pregunta")


class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    nombre: str
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    sesiones: list["Sesion"] = Relationship(back_populates="usuario")


class Sesion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", index=True)
    modo: ModoTest = Field(sa_column=Column(SAEnum(ModoTest), nullable=False))
    feedback: FeedbackMode = Field(sa_column=Column(SAEnum(FeedbackMode), nullable=False))
    tema_id: Optional[int] = Field(default=None, foreign_key="tema.id")
    total: int
    aciertos: int
    segundos: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    usuario: Optional[Usuario] = Relationship(back_populates="sesiones")
    respuestas: list["Respuesta"] = Relationship(back_populates="sesion")


class Respuesta(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sesion_id: int = Field(foreign_key="sesion.id", index=True)
    pregunta_id: str = Field(foreign_key="pregunta.id", index=True)
    elegida: Optional[int] = None  # index 0..3, None = unanswered
    correcta: bool  # convenience copy

    sesion: Optional[Sesion] = Relationship(back_populates="respuestas")
    pregunta: Optional[Pregunta] = Relationship(back_populates="respuestas")
