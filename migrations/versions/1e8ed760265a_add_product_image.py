"""add_product_image

Revision ID: 1e8ed760265a
Revises: a8bcaacbed52
Create Date: 2024-08-30 17:13:00.637070

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1e8ed760265a"
down_revision: Union[str, None] = "a8bcaacbed52"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "product_image",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("alternative_text", sa.String(length=100), nullable=False),
        sa.Column("url", sa.String(length=100), nullable=False),
        sa.Column("order", sa.Integer(), nullable=False),
        sa.Column("product_line_id", sa.Integer(), nullable=False),
        sa.CheckConstraint(
            '"order" >= 1 AND "order" <= 20', name="product_image_order_range"
        ),
        sa.CheckConstraint(
            "LENGTH(alternative_text) > 0",
            name="product_image_alternative_length_check",
        ),
        sa.CheckConstraint("LENGTH(url) > 0", name="product_image_url_length_check"),
        sa.ForeignKeyConstraint(
            ["product_line_id"],
            ["product_line.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "order", "product_line_id", name="uq_product_image_order_product_line_id"
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("product_image")
    # ### end Alembic commands ###
