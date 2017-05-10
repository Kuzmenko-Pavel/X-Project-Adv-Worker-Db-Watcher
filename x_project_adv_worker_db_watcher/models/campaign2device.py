from sqlalchemy import (Column, Integer, BigInteger, ForeignKey)
from .meta import Base


class Campaign2Device(Base):
    __tablename__ = 'campaign2device'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cam = Column(BigInteger, ForeignKey('campaign.id'))
    id_dev = Column(Integer, ForeignKey('device.id'))
