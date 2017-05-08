from sqlalchemy import (Column, Integer, SmallInteger, Boolean, ForeignKey)
from .meta import Base


class Cron(Base):
    __tablename__ = 'cron'
    id_cam = Column(Integer, ForeignKey('campaign.id'), primary_key=True)
    day = Column(SmallInteger)
    hour = Column(SmallInteger)
    min = Column(SmallInteger)
    startStop = Column(Boolean, primary_key=True)
