##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2025, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################

"""empty message

Revision ID: e6732a60c498
Revises: 255e2842e4d7
Create Date: 2025-02-28 14:14:25.542247

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6732a60c498'
down_revision = '255e2842e4d7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'query_tool_data',
        sa.Column('trans_id', sa.Integer(), nullable=False),
        sa.Column('uid', sa.Integer(), nullable=False),
        sa.Column('connection_info', sa.JSON()),
        sa.Column('query_data', sa.String()),
        sa.ForeignKeyConstraint(['uid'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('trans_id', 'uid'))

def downgrade():
    # pgAdmin only upgrades, downgrade not implemented.
    pass
