"""add oposicion multi tenant support

Revision ID: 6b2352c5a8b8
Revises: a1c8f3d2e9b4
Create Date: 2026-07-26 23:28:18.702670

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '6b2352c5a8b8'
down_revision: Union[str, Sequence[str], None] = 'a1c8f3d2e9b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# La oposición ya existente (Escala Auxiliar Administrativa C2, UHU) pasa a ser
# la fila id=1 de la nueva tabla `oposicion` — los temas 1-17 actuales y los
# usuarios existentes se backfillean a este id, sin cambiar su comportamiento.
OPOSICION_INICIAL_ID = 1
OPOSICION_INICIAL_SLUG = "aux-admin-c2-uhu"
OPOSICION_INICIAL_NOMBRE = "Escala Auxiliar Administrativa C2 · Universidad de Huelva"
OPOSICION_INICIAL_DESCRIPCION = (
    "Temario y exámenes de la Escala Auxiliar Administrativa (C2) de la Universidad de Huelva."
)


def upgrade() -> None:
    """Upgrade schema.

    Guardado paso a paso (a diferencia del early-return de la migración
    inicial) porque aquí sí hace falta backfillear datos sobre tablas que ya
    existían antes de esta migración (`tema`, `usuario`), sin importar si
    esas tablas las creó Alembic o el create_all() histórico.
    """
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = set(inspector.get_table_names())

    if "oposicion" not in existing_tables:
        op.create_table(
            "oposicion",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("slug", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("nombre", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
            sa.Column("descripcion", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
            sa.PrimaryKeyConstraint("id"),
        )
        with op.batch_alter_table("oposicion", schema=None) as batch_op:
            batch_op.create_index(batch_op.f("ix_oposicion_slug"), ["slug"], unique=True)

    # Backfill de la oposición inicial (idempotente: solo si no existe ya).
    oposicion_table = sa.table(
        "oposicion",
        sa.column("id", sa.Integer()),
        sa.column("slug", sa.String()),
        sa.column("nombre", sa.String()),
        sa.column("descripcion", sa.String()),
    )
    ya_existe = bind.execute(
        sa.select(oposicion_table.c.id).where(oposicion_table.c.id == OPOSICION_INICIAL_ID)
    ).first()
    if ya_existe is None:
        bind.execute(
            oposicion_table.insert().values(
                id=OPOSICION_INICIAL_ID,
                slug=OPOSICION_INICIAL_SLUG,
                nombre=OPOSICION_INICIAL_NOMBRE,
                descripcion=OPOSICION_INICIAL_DESCRIPCION,
            )
        )

    if "usuariooposicion" not in existing_tables:
        op.create_table(
            "usuariooposicion",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("usuario_id", sa.Integer(), nullable=False),
            sa.Column("oposicion_id", sa.Integer(), nullable=False),
            sa.Column("favorita", sa.Boolean(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(["oposicion_id"], ["oposicion.id"]),
            sa.ForeignKeyConstraint(["usuario_id"], ["usuario.id"]),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("usuario_id", "oposicion_id", name="uq_usuario_oposicion"),
        )
        with op.batch_alter_table("usuariooposicion", schema=None) as batch_op:
            batch_op.create_index(batch_op.f("ix_usuariooposicion_oposicion_id"), ["oposicion_id"], unique=False)
            batch_op.create_index(batch_op.f("ix_usuariooposicion_usuario_id"), ["usuario_id"], unique=False)

    if "tema" in existing_tables:
        existing_cols = {c["name"] for c in inspector.get_columns("tema")}
        if "oposicion_id" not in existing_cols:
            with op.batch_alter_table("tema", schema=None) as batch_op:
                batch_op.add_column(sa.Column("oposicion_id", sa.Integer(), nullable=True))

            tema_table = sa.table("tema", sa.column("oposicion_id", sa.Integer()))
            bind.execute(tema_table.update().values(oposicion_id=OPOSICION_INICIAL_ID))

            with op.batch_alter_table("tema", schema=None) as batch_op:
                batch_op.alter_column("oposicion_id", existing_type=sa.Integer(), nullable=False)
                batch_op.create_index(batch_op.f("ix_tema_oposicion_id"), ["oposicion_id"], unique=False)
                batch_op.create_foreign_key("fk_tema_oposicion_id_oposicion", "oposicion", ["oposicion_id"], ["id"])

    # Backfill: cada usuario existente añade la oposición inicial como favorita,
    # preservando exactamente su experiencia actual (nada cambia para ellos).
    if "usuario" in existing_tables:
        usuario_table = sa.table("usuario", sa.column("id", sa.Integer()))
        usuariooposicion_table = sa.table(
            "usuariooposicion",
            sa.column("usuario_id", sa.Integer()),
            sa.column("oposicion_id", sa.Integer()),
            sa.column("favorita", sa.Boolean()),
            sa.column("created_at", sa.DateTime()),
        )
        usuarios_ids = [row[0] for row in bind.execute(sa.select(usuario_table.c.id))]
        ya_vinculados = {
            row[0]
            for row in bind.execute(
                sa.select(usuariooposicion_table.c.usuario_id).where(
                    usuariooposicion_table.c.oposicion_id == OPOSICION_INICIAL_ID
                )
            )
        }
        pendientes = [uid for uid in usuarios_ids if uid not in ya_vinculados]
        if pendientes:
            bind.execute(
                usuariooposicion_table.insert(),
                [
                    {
                        "usuario_id": uid,
                        "oposicion_id": OPOSICION_INICIAL_ID,
                        "favorita": True,
                        "created_at": datetime.datetime.utcnow(),
                    }
                    for uid in pendientes
                ],
            )


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = set(inspector.get_table_names())

    if "tema" in existing_tables:
        existing_cols = {c["name"] for c in inspector.get_columns("tema")}
        if "oposicion_id" in existing_cols:
            with op.batch_alter_table("tema", schema=None) as batch_op:
                batch_op.drop_constraint("fk_tema_oposicion_id_oposicion", type_="foreignkey")
                batch_op.drop_index(batch_op.f("ix_tema_oposicion_id"))
                batch_op.drop_column("oposicion_id")

    if "usuariooposicion" in existing_tables:
        with op.batch_alter_table("usuariooposicion", schema=None) as batch_op:
            batch_op.drop_index(batch_op.f("ix_usuariooposicion_usuario_id"))
            batch_op.drop_index(batch_op.f("ix_usuariooposicion_oposicion_id"))
        op.drop_table("usuariooposicion")

    if "oposicion" in existing_tables:
        with op.batch_alter_table("oposicion", schema=None) as batch_op:
            batch_op.drop_index(batch_op.f("ix_oposicion_slug"))
        op.drop_table("oposicion")
