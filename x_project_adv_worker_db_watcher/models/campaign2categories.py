from sqlalchemy import (Column, Integer, BigInteger, ForeignKey)
from .meta import Base


class Campaign2Categories(Base):
    __tablename__ = 'campaign2categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cam = Column(BigInteger, ForeignKey('campaign.id'))
    id_cat = Column(Integer, ForeignKey('categories.id'))
