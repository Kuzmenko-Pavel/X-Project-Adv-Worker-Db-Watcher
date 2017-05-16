from sqlalchemy import (Column, Integer, BigInteger, ForeignKey)
from .meta import Base


class Campaign2Categories(Base):
    __tablename__ = 'campaign2categories'
    id_cam = Column(BigInteger, ForeignKey('campaign.id'), primary_key=True, nullable=False)
    id_cat = Column(Integer, ForeignKey('categories.id'), primary_key=True, nullable=False)
