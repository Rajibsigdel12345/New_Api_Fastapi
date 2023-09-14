"""Add user table

Revision ID: 2751dae7d22e
Revises: 5c756f62e650
Create Date: 2023-09-14 13:46:47.550679

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2751dae7d22e'
down_revision: Union[str, None] = '5c756f62e650'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.UniqueConstraint("email"),
                    # sa.PrimaryKeyConstraint('id') or use primary_key = true
                    )

    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
