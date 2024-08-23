"""created user model

Revision ID: dcfc85a36fb9
Revises: 41e2800fe40e
Create Date: 2024-08-23 17:13:02.683341

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dcfc85a36fb9'
down_revision = '41e2800fe40e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('email', sa.String(), nullable=False, unique=True, index=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('address', sa.String(), nullable=True),
        sa.Column('date_of_birth', sa.String(), nullable=True),
        sa.Column('dt_created', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('dt_updated', sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('users')
