"""add_attribute_value_table

Revision ID: b55a1fb29079
Revises: ea6e6e8d01a1
Create Date: 2024-09-02 16:06:13.276659

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b55a1fb29079"
down_revision: Union[str, None] = "ea6e6e8d01a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "attribute_value",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("attribute_value", sa.String(length=100), nullable=False),
        sa.Column("attribute_id", sa.Integer(), nullable=False),
        sa.CheckConstraint(
            "LENGTH(attribute_value) > 0", name="attribute_value_value_length_check"
        ),
        sa.ForeignKeyConstraint(
            ["attribute_id"],
            ["attribute.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("attribute_id", name="uq_attribute_value_attribute_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("attribute_value")
    # ### end Alembic commands ###
