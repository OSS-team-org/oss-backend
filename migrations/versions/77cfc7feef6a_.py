"""empty message

Revision ID: 77cfc7feef6a
Revises: a1fe3a879620
Create Date: 2022-04-30 21:54:16.369715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77cfc7feef6a'
down_revision = 'a1fe3a879620'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('account', sa.Column('code', sa.String(length=100), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('account', 'code')
    # ### end Alembic commands ###
