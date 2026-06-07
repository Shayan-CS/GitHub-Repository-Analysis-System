"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2026-06-07 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'repositories',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('github_url', sa.Text(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('stars', sa.Integer(), nullable=True),
        sa.Column('language', sa.String(length=100), nullable=True),
        sa.Column('last_analyzed', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        'analyses',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('repository_id', sa.String(length=36), sa.ForeignKey('repositories.id', ondelete='CASCADE'), nullable=False),
        sa.Column('summary', sa.Text(), nullable=False),
        sa.Column('complexity_score', sa.Float(), nullable=False),
        sa.Column('topics', sa.JSON(), nullable=True),
        sa.Column('embedding_id', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('analyses')
    op.drop_table('repositories')
