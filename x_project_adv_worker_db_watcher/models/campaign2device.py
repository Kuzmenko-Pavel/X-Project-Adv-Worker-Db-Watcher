from sqlalchemy import (Column, Integer, ForeignKey)
from .meta import Base


class Campaign2Device(Base):
    __tablename__ = 'campaign2device'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cam = Column(Integer, ForeignKey('campaign.id'))
    id_dev = Column(Integer, ForeignKey('device.id'))
