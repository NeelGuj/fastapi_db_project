"""create users table

Revision ID: e00acb7f5d98
Revises: c8b63e677a51
Create Date: 2025-03-28 13:22:54.460927

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e00acb7f5d98'
down_revision: Union[str, None] = 'c8b63e677a51'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users', 
    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),  # Primary key directly in the column
    sa.Column('email', sa.String(), nullable=False, unique=True),  # Unique constraint directly in the column
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False)
    # sa. PrimaryKeyConstraint('id'), # to declare primary key outside of column
    # sa. UniqueConstraint('email')   # to declare unique constraint outside of column
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")

    pass
