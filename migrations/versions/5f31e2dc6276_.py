"""empty message

Revision ID: 5f31e2dc6276
Revises: 
Create Date: 2025-01-10 15:31:16.547280

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f31e2dc6276'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('notes',
                    sa.Column('address', sa.String(), nullable=False),
                    sa.Column('floor', sa.Integer(), nullable=False),
                    sa.Column('full_name', sa.String(), nullable=False),
                    sa.Column('position_at_work', sa.String(), nullable=False),
                    sa.Column('computer_name', sa.String(), nullable=False),
                    sa.Column('work_group', sa.String(), nullable=False),
                    sa.Column('comment', sa.String(), nullable=True),
                    )
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
