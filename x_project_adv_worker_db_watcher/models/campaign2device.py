from sqlalchemy import (Column, Integer, BigInteger, ForeignKey)
from .meta import Base


class Campaign2Device(Base):
    __tablename__ = 'campaign2device'
    id_cam = Column(BigInteger, ForeignKey('campaign.id'), primary_key=True, nullable=False)
    id_dev = Column(Integer, ForeignKey('device.id'), primary_key=True, nullable=False)
