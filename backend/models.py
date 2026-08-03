from datetime import date, datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Column
from sqlalchemy import Enum as SAEnum
from sqlalchemy import JSON, UniqueConstraint
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


class Oposicion(SQLModel, table=True):
    """Agrupa un temario/banco de preguntas independiente (p.ej. una oposición distinta
    a la Escala Auxiliar Administrativa C2 de la UHU). Cada `Tema` pertenece a una."""
    id: int = Field(primary_key=True)
    slug: str = Field(unique=True, index=True)
    nombre: str
    descripcion: Optional[str] = None

    temas: list["Tema"] = Relationship(back_populates="oposicion")


class Tema(SQLModel, table=True):
    id: int = Field(primary_key=True)
    titulo: str
    ley: str
    orden: int
    oposicion_id: int = Field(default=1, foreign_key="oposicion.id", index=True)

    preguntas: list["Pregunta"] = Relationship(back_populates="tema")
    oposicion: Optional[Oposicion] = Relationship(back_populates="temas")


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
    # Pregunta de seguridad para verificar la identidad al restablecer la contraseña.
    # Nullable porque las cuentas creadas antes de esta funcionalidad no la tienen
    # todavía configurada (deben añadirla vía PUT /api/auth/security-question).
    pregunta_seguridad: Optional[str] = Field(default=None)
    respuesta_seguridad_hash: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    sesiones: list["Sesion"] = Relationship(back_populates="usuario")
    oposiciones: list["UsuarioOposicion"] = Relationship(back_populates="usuario")


class UsuarioOposicion(SQLModel, table=True):
    """Oposiciones que un usuario ha añadido a su cuenta (puede tener varias);
    `favorita` marca cuál se carga por defecto al entrar. Solo una favorita
    por usuario, se garantiza a nivel de aplicación, no de constraint de BD."""
    __table_args__ = (UniqueConstraint("usuario_id", "oposicion_id", name="uq_usuario_oposicion"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", index=True)
    oposicion_id: int = Field(foreign_key="oposicion.id", index=True)
    favorita: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    usuario: Optional[Usuario] = Relationship(back_populates="oposiciones")


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


class AsistenteUso(SQLModel, table=True):
    """Contador diario de mensajes al asistente por usuario, para acotar el coste del LLM."""
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", index=True)
    fecha: date = Field(index=True)
    mensajes: int = Field(default=0)


class AsistenteMensaje(SQLModel, table=True):
    """Historial persistente de la conversación con el asistente, por usuario y tema."""
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", index=True)
    tema_id: int = Field(foreign_key="tema.id", index=True)
    role: str  # "user" | "assistant"
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)


class NotaDia(SQLModel, table=True):
    """Nota libre y persistente que el usuario asocia a un día del roadmap."""
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", index=True)
    fecha: date = Field(index=True)
    contenido: str
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TarjetaEstado(SQLModel, table=True):
    """Estado de repetición espaciada (SM-2 simplificado) de una tarjeta para un usuario.
    Si no existe fila para un (usuario, tarjeta), la tarjeta es "nueva" (nunca repasada)."""
    __table_args__ = (UniqueConstraint("usuario_id", "tarjeta_id", name="uq_tarjeta_usuario_tarjeta"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", index=True)
    tarjeta_id: str = Field(foreign_key="tarjeta.id", index=True)
    ease: float = Field(default=2.5)
    interval_dias: int = Field(default=0)
    repeticiones: int = Field(default=0)
    proxima_revision: date = Field(default_factory=date.today, index=True)
    ultima_revision: Optional[datetime] = None


class Tarjeta(SQLModel, table=True):
    """Tarjeta de repaso (Anki-style) redactada para poder estudiarse de forma aislada:
    a diferencia de Pregunta, no depende de ver un listado de opciones A/B/C/D. Generada
    por el agente tarjetas-generator a partir del temario oficial, no de los exámenes."""
    id: str = Field(primary_key=True)  # "{tema_id}_{indice}"
    tema_id: int = Field(foreign_key="tema.id", index=True)
    frente: str
    dorso: str
    ref: str
    explicacion: Optional[str] = None


class LoginEvento(SQLModel, table=True):
    """Un registro por cada login correcto, para el dashboard de administración
    (últimos accesos, usuarios activos). Tabla nueva (no columna añadida a Usuario)
    para no requerir migración de una tabla ya existente."""
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuario.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
