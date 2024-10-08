"""add_attribute

Revision ID: d452c5deceba
Revises: 6bb36af74625
Create Date: 2024-08-30 17:41:59.785730

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d452c5deceba"
down_revision: Union[str, None] = "6bb36af74625"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "attribute",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=100), nullable=True),
        sa.CheckConstraint("LENGTH(name) > 0", name="attribute_name_length_check"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="uq_attribute_name"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("attribute")
    # ### end Alembic commands ###
