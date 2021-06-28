"""Add transfer ticket to user

Revision ID: 3f54ae5d8f7f
Revises: 292882794509
Create Date: 2021-06-15 08:55:56.096141

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f54ae5d8f7f'
down_revision = '292882794509'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('user', sa.Column('transfer_ticket', sa.String(), nullable=True))


def downgrade():
    op.drop_column('user', 'transfer_ticket')
