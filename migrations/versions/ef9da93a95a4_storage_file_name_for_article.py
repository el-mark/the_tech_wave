"""storage_file_name for article

Revision ID: ef9da93a95a4
Revises: 127ac3b9d6fe
Create Date: 2024-11-12 19:31:21.776222

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef9da93a95a4'
down_revision = '127ac3b9d6fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.add_column(sa.Column('storage_file_name', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('article', schema=None) as batch_op:
        batch_op.drop_column('storage_file_name')

    # ### end Alembic commands ###
