import sqlalchemy
from sqlalchemy import Boolean, CheckConstraint, Column, DECIMAL, DateTime, Enum, Float, ForeignKey, Integer, String, \
    Text, \
    UUID, UniqueConstraint, text

from app.db_connection import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(120), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False, server_default="false")
    level = Column(Integer, nullable=False, default=100, server_default="100")
    parent_id = Column(Integer, ForeignKey("category.id"), nullable=True, )

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="category_name_length_check"),
        CheckConstraint("LENGTH(slug) > 0", name="category_slug_length_check"),
        UniqueConstraint("name", "level", name="uq_category_name_level"),
        UniqueConstraint("slug", name="uq_category_slug"),
    )


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    pid = Column(UUID(as_uuid=True), nullable=False, server_default=text("uuid_generate_v4()"))
    name = Column(String(200), nullable=False)
    slug = Column(String(220), nullable=False)
    description = Column(Text, nullable=True)
    is_digital = Column(Boolean, nullable=False, default=False, server_default="false")
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), )
    updated_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"),
                        onupdate=sqlalchemy.func.now())
    is_active = Column(Boolean, nullable=False, default=False, server_default="false")
    stock_status = Column(Enum("oos", "is", "obo", name="status_enum"), nullable=False, server_default="oos")
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False, )
    seasonal_id = Column(Integer, ForeignKey("seasonal_event.id"), nullable=True, )

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="product_name_length_check"),
        CheckConstraint("LENGTH(slug) > 0", name="product_slug_length_check"),
        UniqueConstraint("pid", name="uq_product_pid"),
        UniqueConstraint("name", name="uq_product_name"),
        UniqueConstraint("slug", name="uq_product_slug"),
    )


class SeasonalEvent(Base):
    __tablename__ = "seasonal_event"

    id = Column(Integer, primary_key=True)


class ProductLine(Base):
    __tablename__ = "product_line"

    id = Column(Integer, primary_key=True)
    price = Column(DECIMAL(5, 2), nullable=False)
    sku = Column(UUID(as_uuid=True), nullable=False, server_default=text("uuid_generate_v4()"))
    stock_qty = Column(Integer, nullable=False, default=0, server_default="0")
    is_active = Column(Boolean, nullable=False, default=False, server_default="false")
    order = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), )
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False, )

    __table_args__ = (
        CheckConstraint("price >= 0 AND price <= 999.99", name="product_line_check_price"),
        CheckConstraint('"order" >= 1 AND "order" <= 20', name="product_line_order_range"),
        UniqueConstraint("sku", name="uq_product_line_sku"),
        UniqueConstraint("order", "product_id", name="uq_product_line_order_product_id"),
    )


class ProductImage(Base):
    __tablename__ = "product_image"

    id = Column(Integer, primary_key=True)
    alternative_text = Column(String(100), nullable=False)
    url = Column(String(100), nullable=False)
    order = Column(Integer, nullable=False)
    product_line_id = Column(Integer, ForeignKey("product_line.id"), nullable=False, )

    __table_args__ = (
        CheckConstraint('"order" >= 1 AND "order" <= 20', name="product_image_order_range"),
        CheckConstraint("LENGTH(alternative_text) > 0", name="product_image_alternative_length_check"),
        CheckConstraint("LENGTH(url) > 0", name="product_image_url_length_check"),
        UniqueConstraint("order", "product_line_id", name="uq_product_image_order_product_line_id"),
    )