from sqlalchemy import Boolean, Column, Integer, String

from app.db_connection import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    slug = Column(String(120))
    is_active = Column(Boolean)
    level = Column(Integer)
    parent_id = Column(Integer)
