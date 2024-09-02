"""add_product_type_table

Revision ID: ea6e6e8d01a1
Revises: d452c5deceba
Create Date: 2024-09-02 15:52:23.742345

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea6e6e8d01a1'
down_revision: Union[str, None] = 'd452c5deceba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('level', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.CheckConstraint('LENGTH(name) > 0', name='product_type_name_length_check'),
    sa.ForeignKeyConstraint(['parent_id'], ['product_type.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name', 'level', name='uq_product_type_name_level')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_type')
    # ### end Alembic commands ###
