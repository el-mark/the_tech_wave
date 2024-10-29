"""fix name'


Revision ID: 127ac3b9d6fe
Revises: 2927bdc06395
Create Date: 2024-10-10 15:49:46.365193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '127ac3b9d6fe'
down_revision = '2927bdc06395'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=150),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=150),
               nullable=True)

    # ### end Alembic commands ###