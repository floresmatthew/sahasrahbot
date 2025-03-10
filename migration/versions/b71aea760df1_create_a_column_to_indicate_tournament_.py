"""create a column to indicate tournament uses a tracker

Revision ID: b71aea760df1
Revises: 2d29235b9738
Create Date: 2021-04-25 13:36:21.408551

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b71aea760df1'
down_revision = '2d29235b9738'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tournaments', sa.Column('scheduling_needs_tracker', mysql.TINYINT(display_width=1), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tournaments', 'scheduling_needs_tracker')
    # ### end Alembic commands ###
