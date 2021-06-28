"""Add Indexes

Revision ID: 0cdb4351a66d
Revises: 8ae9b5ddadf6
Create Date: 2021-04-29 17:47:42.670772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0cdb4351a66d'
down_revision = '8ae9b5ddadf6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(op.f('ix_audit_log_created_at'), 'audit_log', ['created_at'], unique=False)
    op.create_index(op.f('ix_user_last_modified'), 'user', ['last_modified'], unique=False)


def downgrade():
    op.drop_index(op.f('ix_user_last_modified'), table_name='user')
    op.drop_index(op.f('ix_audit_log_created_at'), table_name='audit_log')
