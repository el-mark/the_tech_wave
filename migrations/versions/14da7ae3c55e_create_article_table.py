"""Create article table

Revision ID: 14da7ae3c55e
Revises: 
Create Date: 2024-10-04 15:21:26.600652

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '14da7ae3c55e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('image_url', sa.String(length=255), nullable=True),
    sa.Column('source', sa.String(length=510), nullable=True),
    sa.Column('source_name', sa.String(length=64), nullable=True),
    sa.Column('views', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('article')
    # ### end Alembic commands ###
