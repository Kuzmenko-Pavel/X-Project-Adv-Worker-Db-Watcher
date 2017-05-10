from sqlalchemy import (Column, Integer, BigInteger, ForeignKey)
from .meta import Base


class Categories2Informer(Base):
    __tablename__ = 'categories2informer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cat = Column(Integer, ForeignKey('categories.id'))
    id_inf = Column(BigInteger, ForeignKey('informer.id'))
