from sqlalchemy import (Column, Integer, BigInteger, SmallInteger, ForeignKey)
from .meta import Base


class Campaign2Informer(Base):
    __tablename__ = 'campaign2informer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cam = Column(BigInteger, ForeignKey('campaign.id'))
    id_inf = Column(Integer, ForeignKey('informer.id'))
    allowed = Column(SmallInteger)
