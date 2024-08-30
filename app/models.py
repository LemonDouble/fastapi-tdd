from sqlalchemy import Boolean, CheckConstraint, Column, Integer, String, UniqueConstraint

from app.db_connection import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    slug = Column(String(120), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False, server_default="false")
    level = Column(Integer, nullable=False, default=100, server_default="100")
    parent_id = Column(Integer, nullable=True)

    __table_args__ = (
        CheckConstraint("LENGTH(name) > 0", name="name_length_check"),
        CheckConstraint("LENGTH(slug) > 0", name="slug_length_check"),
        UniqueConstraint("name", "level", name="uq_category_name_level"),
        UniqueConstraint("slug", name="uq_category_slug"),
    )
