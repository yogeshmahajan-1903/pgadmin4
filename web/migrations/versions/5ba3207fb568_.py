##########################################################################
#
# pgAdmin 4 - PostgreSQL Tools
#
# Copyright (C) 2013 - 2025, The pgAdmin Development Team
# This software is released under the PostgreSQL Licence
#
##########################################################################
"""Added new table to store pgadmin state to restore after crash

Revision ID: 5ba3207fb568
Revises: e982c040d9b5
Create Date: 2025-03-20 16:41:06.825924

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '5ba3207fb568'
down_revision = 'e982c040d9b5'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'pgadmin_state_data',
        sa.Column('uid', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer()),
        sa.Column('connection_info', sa.JSON()),
        sa.Column('tool_name', sa.String()),
        sa.Column('tool_data', sa.String()),
        sa.ForeignKeyConstraint(['uid'], ['user.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', 'uid'))


def downgrade():
    # pgAdmin only upgrades, downgrade not implemented.
    pass
