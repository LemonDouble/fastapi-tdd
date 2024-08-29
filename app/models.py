from sqlalchemy import Column, Integer

from app.db_connection import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)