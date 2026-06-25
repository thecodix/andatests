"""
seed_reference.py — Script de referencia para poblar la base de datos de Andatest
a partir de los archivos banco/temaN.json.

Pensado para FastAPI + SQLModel. Ajusta los imports a tu estructura real.
Ejecutar una vez tras crear las tablas:  python seed_reference.py
"""
import json
import os
from sqlmodel import SQLModel, Session, create_engine, Field
from typing import Optional

# --- Modelos mínimos (mueve a tu models.py real) ---------------------------

class Tema(SQLModel, table=True):
    id: int = Field(primary_key=True)
    titulo: str
    ley: str
    orden: int

class Pregunta(SQLModel, table=True):
    id: str = Field(primary_key=True)          # "{tema}_{indice}", estable
    tema_id: int = Field(foreign_key="tema.id")
    enunciado: str
    opciones: str                              # JSON serializado (list[str])
    correcta: int
    ref: str
    explicacion: str

# --- Metadatos de los 17 temas (coinciden con banco.js) --------------------

META = [
    (1,  "La Constitución Española de 1978", "CE 1978"),
    (2,  "Ley 39/2015 del Procedimiento Administrativo Común (I)", "Ley 39/2015"),
    (3,  "Ley 39/2015 del Procedimiento Administrativo Común (II)", "Ley 39/2015"),
    (4,  "Ley 39/2015: recursos administrativos (III)", "Ley 39/2015"),
    (5,  "Ley 40/2015 de Régimen Jurídico del Sector Público", "Ley 40/2015"),
    (6,  "Estatuto Básico del Empleado Público (TREBEP)", "RDL 5/2015"),
    (7,  "Protección de Datos Personales (LOPDGDD)", "LO 3/2018"),
    (8,  "Transparencia y acceso a la información pública", "Ley 19/2013"),
    (9,  "Igualdad de género en Andalucía", "Ley 12/2007"),
    (10, "Ley Orgánica del Sistema Universitario (LOSU)", "LO 2/2023"),
    (11, "Estatutos de la Universidad de Huelva", "Decreto 232/2011"),
    (12, "Organización de las enseñanzas universitarias", "RD 822/2021"),
    (13, "Información general de la Universidad de Huelva", "UHU"),
    (14, "Bases de ejecución presupuestaria de la UHU", "Presupuesto UHU"),
    (15, "Reglamento de permanencia y progreso (grado y máster)", "Reglamento UHU"),
    (16, "Administración electrónica y el ENS", "RD 311/2022"),
    (17, "La Administración de la Junta de Andalucía", "Ley 9/2007"),
]

BANCO_DIR = "banco"  # carpeta con temaN.json

def seed(engine):
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        for orden, (tid, titulo, ley) in enumerate(META):
            s.merge(Tema(id=tid, titulo=titulo, ley=ley, orden=orden))
            path = os.path.join(BANCO_DIR, f"tema{tid}.json")
            if not os.path.exists(path):
                continue
            with open(path, encoding="utf-8") as f:
                preguntas = json.load(f)
            for i, p in enumerate(preguntas):
                s.merge(Pregunta(
                    id=f"{tid}_{i}",
                    tema_id=tid,
                    enunciado=p["q"],
                    opciones=json.dumps(p["o"], ensure_ascii=False),
                    correcta=p["c"],
                    ref=p["ref"],
                    explicacion=p["exp"],
                ))
        s.commit()
    print("Seed completado.")

if __name__ == "__main__":
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./andatest.db")
    engine = create_engine(DATABASE_URL, echo=False)
    seed(engine)
