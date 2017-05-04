from sqlalchemy import (Column, Integer)
from .meta import Base


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)