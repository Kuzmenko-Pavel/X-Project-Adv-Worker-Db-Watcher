from sqlalchemy import (Column, Integer, String)
from .meta import Base


class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    guid = Column(String(length=64), unique=True, index=True)
    title = Column(String(length=1024))
