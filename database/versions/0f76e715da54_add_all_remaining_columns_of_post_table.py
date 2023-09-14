"""add all remaining columns of post table

Revision ID: 0f76e715da54
Revises: ca5179f7fcd2
Create Date: 2023-09-14 14:01:42.713793

"""
from tkinter.tix import Tree
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f76e715da54'
down_revision: Union[str, None] = 'ca5179f7fcd2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('published', sa.Boolean(),
                  nullable=False, server_default="TRUE"))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')

    pass
