"""Tests que las migraciones reales de Alembic (no el `create_all()` a
ciegas) construyen el esquema completo desde cero en una BD limpia."""
import os
import sqlite3
import subprocess
import sys
import tempfile

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXPECTED_TABLES = {
    "tema", "usuario", "asistentemensaje", "asistenteuso", "notadia",
    "pregunta", "sesion", "tarjeta", "respuesta", "tarjetaestado",
    "oposicion", "usuariooposicion",
}


def test_alembic_upgrade_head_crea_el_esquema_completo_en_bd_limpia():
    fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    os.remove(db_path)  # sqlite crea el fichero al conectar por primera vez

    env = os.environ.copy()
    env["DATABASE_URL"] = f"sqlite:///{db_path}"

    try:
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "upgrade", "head"],
            cwd=BACKEND_DIR,
            env=env,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr

        con = sqlite3.connect(db_path)
        try:
            tables = {row[0] for row in con.execute(
                "select name from sqlite_master where type='table'"
            )}
            assert EXPECTED_TABLES <= tables

            usuario_cols = {row[1] for row in con.execute("pragma table_info(usuario)")}
            assert {"pregunta_seguridad", "respuesta_seguridad_hash"} <= usuario_cols

            tema_cols = {row[1] for row in con.execute("pragma table_info(tema)")}
            assert "oposicion_id" in tema_cols

            oposiciones = list(con.execute("select id, slug from oposicion"))
            assert (1, "aux-admin-c2-uhu") in oposiciones
        finally:
            con.close()
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
