from sqlalchemy import (Column, Integer, ForeignKey)
from .meta import Base


class Categories2Domain(Base):
    __tablename__ = 'categories2domain'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cat = Column(Integer, ForeignKey('categories.id'))
    id_dom = Column(Integer, ForeignKey('domains.id'))
