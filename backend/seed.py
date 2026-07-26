"""
Populate tema + pregunta tables from banco/temaN.json.
Safe to re-run: uses merge (upsert by PK).

Usage:
  cd backend
  python seed.py
"""
import json
import os
import sys

from sqlmodel import Session, SQLModel

sys.path.insert(0, os.path.dirname(__file__))

from database import engine
from models import Oposicion, Pregunta, Tarjeta, Tema

BANCO_DIR = os.path.join(os.path.dirname(__file__), "..", "banco")
TARJETAS_DIR = os.path.join(BANCO_DIR, "tarjetas")

# Cada oposición soportada tiene sus propios temas (id, título, ley), con IDs
# reservados por bloques de 1000 para que nunca choquen entre oposiciones —
# ver "Múltiples oposiciones" en CLAUDE.md. Añadir una oposición nueva es solo
# añadir una entrada aquí; no hace falta tocar el resto de este fichero.
OPOSICIONES = [
    {
        "id": 1,
        "slug": "aux-admin-c2-uhu",
        "nombre": "Escala Auxiliar Administrativa C2 · Universidad de Huelva",
        "descripcion": "Temario y exámenes de la Escala Auxiliar Administrativa (C2) de la Universidad de Huelva.",
        "temas": [
            (1,  "La Constitución Española de 1978",                        "CE 1978"),
            (2,  "Ley 39/2015 del Procedimiento Administrativo Común (I)",  "Ley 39/2015"),
            (3,  "Ley 39/2015 del Procedimiento Administrativo Común (II)", "Ley 39/2015"),
            (4,  "Ley 39/2015: recursos administrativos (III)",             "Ley 39/2015"),
            (5,  "Ley 40/2015 de Régimen Jurídico del Sector Público",      "Ley 40/2015"),
            (6,  "Estatuto Básico del Empleado Público (TREBEP)",           "RDL 5/2015"),
            (7,  "Protección de Datos Personales (LOPDGDD)",                "LO 3/2018"),
            (8,  "Transparencia y acceso a la información pública",         "Ley 19/2013"),
            (9,  "Igualdad de género en Andalucía",                         "Ley 12/2007"),
            (10, "Ley Orgánica del Sistema Universitario (LOSU)",           "LO 2/2023"),
            (11, "Estatutos de la Universidad de Huelva",                   "Decreto 232/2011"),
            (12, "Organización de las enseñanzas universitarias",           "RD 822/2021"),
            (13, "Información general de la Universidad de Huelva",         "UHU"),
            (14, "Bases de ejecución presupuestaria de la UHU",             "Presupuesto UHU"),
            (15, "Reglamento de permanencia y progreso (grado y máster)",   "Reglamento UHU"),
            (16, "Microsoft 365: Word",                                     "Microsoft 365"),
            (17, "Microsoft 365: Excel",                                    "Microsoft 365"),
        ],
    },
]


def seed():
    SQLModel.metadata.create_all(engine)
    total_temas = 0
    total_preguntas = 0
    total_tarjetas = 0
    with Session(engine) as s:
        for op_meta in OPOSICIONES:
            s.merge(Oposicion(
                id=op_meta["id"],
                slug=op_meta["slug"],
                nombre=op_meta["nombre"],
                descripcion=op_meta.get("descripcion"),
            ))

            for orden, (tid, titulo, ley) in enumerate(op_meta["temas"]):
                total_temas += 1
                s.merge(Tema(id=tid, titulo=titulo, ley=ley, orden=orden, oposicion_id=op_meta["id"]))

                path = os.path.join(BANCO_DIR, f"tema{tid}.json")
                if not os.path.exists(path):
                    print(f"  ⚠  Skipping tema {tid}: {path} not found")
                    continue

                with open(path, encoding="utf-8") as f:
                    preguntas = json.load(f)

                for i, p in enumerate(preguntas):
                    s.merge(Pregunta(
                        id=f"{tid}_{i}",
                        tema_id=tid,
                        enunciado=p["q"],
                        opciones=p["o"],          # stored as JSON, not serialized string
                        correcta=p["c"],
                        ref=p["ref"],
                        explicacion=p["exp"],
                    ))
                total_preguntas += len(preguntas)
                print(f"  Tema {tid:2d}: {len(preguntas)} preguntas")

                tarjetas_path = os.path.join(TARJETAS_DIR, f"tema{tid}.json")
                if not os.path.exists(tarjetas_path):
                    continue

                with open(tarjetas_path, encoding="utf-8") as f:
                    tarjetas = json.load(f)

                for i, t in enumerate(tarjetas):
                    s.merge(Tarjeta(
                        id=f"{tid}_{i}",
                        tema_id=tid,
                        frente=t["frente"],
                        dorso=t["dorso"],
                        ref=t["ref"],
                        explicacion=t.get("exp"),
                    ))
                total_tarjetas += len(tarjetas)
                print(f"           {len(tarjetas)} tarjetas")

        s.commit()


    print(f"\nSeed completado: {total_temas} temas, {total_preguntas} preguntas, {total_tarjetas} tarjetas.")


if __name__ == "__main__":
    seed()
