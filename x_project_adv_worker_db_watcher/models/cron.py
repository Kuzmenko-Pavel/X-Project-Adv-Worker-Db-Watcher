from sqlalchemy import (Column, BigInteger, Integer, SmallInteger, Boolean, ForeignKey)
from sqlalchemy.orm import relationship
from .meta import Base


class Cron(Base):
    __tablename__ = 'cron'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cam = Column(BigInteger, ForeignKey('campaign.id'))
    day = Column(SmallInteger)
    hour = Column(SmallInteger)
    min = Column(SmallInteger)
    startStop = Column(Boolean, primary_key=True)
    campaign = relationship('Campaign', back_populates="cron")
