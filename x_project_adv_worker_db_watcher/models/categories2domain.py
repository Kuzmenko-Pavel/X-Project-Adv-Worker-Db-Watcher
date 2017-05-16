from sqlalchemy import (Column, Integer, ForeignKey)
from .meta import Base


class Categories2Domain(Base):
    __tablename__ = 'categories2domain'
    id_cat = Column(Integer, ForeignKey('categories.id'), primary_key=True, nullable=False)
    id_dom = Column(Integer, ForeignKey('domains.id'), primary_key=True, nullable=False)
