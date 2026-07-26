"""add security question to usuario

Revision ID: a1c8f3d2e9b4
Revises: 839629e4d06a
Create Date: 2026-07-26 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1c8f3d2e9b4'
down_revision: Union[str, Sequence[str], None] = '839629e4d06a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema.

    Guarded because the initial migration never actually created any table
    (its upgrade() is a no-op) — tables are created by SQLModel's
    create_all(), which runs *after* this migration in render.yaml's start
    command. On a brand-new empty DB, `usuario` won't exist yet at this
    point, and create_all() will create it with these columns already
    included, so there is nothing to do here. On an existing deployment,
    `usuario` already exists and needs the new nullable columns added.
    """
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if 'usuario' not in inspector.get_table_names():
        return

    existing_cols = {c['name'] for c in inspector.get_columns('usuario')}
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        if 'pregunta_seguridad' not in existing_cols:
            batch_op.add_column(sa.Column('pregunta_seguridad', sa.String(), nullable=True))
        if 'respuesta_seguridad_hash' not in existing_cols:
            batch_op.add_column(sa.Column('respuesta_seguridad_hash', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if 'usuario' not in inspector.get_table_names():
        return

    existing_cols = {c['name'] for c in inspector.get_columns('usuario')}
    with op.batch_alter_table('usuario', schema=None) as batch_op:
        if 'respuesta_seguridad_hash' in existing_cols:
            batch_op.drop_column('respuesta_seguridad_hash')
        if 'pregunta_seguridad' in existing_cols:
            batch_op.drop_column('pregunta_seguridad')
