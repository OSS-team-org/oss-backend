"""empty message

Revision ID: cb75b53f3995
Revises: 7ad511e3b8c8
Create Date: 2022-04-30 22:24:04.552747

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb75b53f3995'
down_revision = '7ad511e3b8c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('account', 'role_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('account', 'role_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
