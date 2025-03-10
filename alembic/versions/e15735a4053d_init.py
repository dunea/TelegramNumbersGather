"""init

Revision ID: e15735a4053d
Revises: 
Create Date: 2025-03-02 07:23:36.250629

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e15735a4053d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('three_eights_numbers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.String(length=18), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_three_eights_numbers_number'), 'three_eights_numbers', ['number'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_three_eights_numbers_number'), table_name='three_eights_numbers')
    op.drop_table('three_eights_numbers')
    # ### end Alembic commands ###
