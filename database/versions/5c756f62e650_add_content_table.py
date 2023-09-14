"""add content table

Revision ID: 5c756f62e650
Revises: 1afeaec79c48
Create Date: 2023-09-14 13:42:26.969225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c756f62e650'
down_revision: Union[str, None] = '1afeaec79c48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
