"""add_product_table

Revision ID: 36bbfdb07296
Revises: ded88ee04958
Create Date: 2024-08-30 15:08:41.801414

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "36bbfdb07296"
down_revision: Union[str, None] = "ded88ee04958"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "seasonal_event",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "product",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "pid",
            sa.UUID(),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("slug", sa.String(length=220), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_digital", sa.Boolean(), server_default="false", nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.Column("is_active", sa.Boolean(), server_default="false", nullable=False),
        sa.Column(
            "stock_status",
            sa.Enum("oos", "is", "obo", name="status_enum"),
            server_default="oos",
            nullable=False,
        ),
        sa.Column("category_id", sa.Integer(), nullable=False),
        sa.Column("seasonal_id", sa.Integer(), nullable=True),
        sa.CheckConstraint("LENGTH(name) > 0", name="product_name_length_check"),
        sa.CheckConstraint("LENGTH(slug) > 0", name="product_slug_length_check"),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["category.id"],
        ),
        sa.ForeignKeyConstraint(
            ["seasonal_id"],
            ["seasonal_event.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="uq_product_name"),
        sa.UniqueConstraint("pid"),
        sa.UniqueConstraint("slug", name="uq_product_slug"),
    )
    op.create_foreign_key(None, "category", "category", ["parent_id"], ["id"])
    op.execute(
        "ALTER TABLE category RENAME CONSTRAINT name_length_check TO category_name_length_check"
    )
    op.execute(
        "ALTER TABLE category RENAME CONSTRAINT slug_length_check TO category_slug_length_check"
    )

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "category", type_="foreignkey")
    op.drop_table("product")
    op.drop_table("seasonal_event")
    op.execute(
        "ALTER TABLE category RENAME CONSTRAINT category_name_length_check TO name_length_check"
    )
    op.execute(
        "ALTER TABLE category RENAME CONSTRAINT category_slug_length_check TO slug_length_check"
    )

    # ### end Alembic commands ###
