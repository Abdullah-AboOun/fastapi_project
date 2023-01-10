"""add content column to posts table

Revision ID: fccf5b62e3a4
Revises: 160f84443b04
Create Date: 2023-01-10 13:30:01.693746

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fccf5b62e3a4'
down_revision = '160f84443b04'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
