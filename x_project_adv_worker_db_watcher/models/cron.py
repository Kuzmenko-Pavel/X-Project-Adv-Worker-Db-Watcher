from sqlalchemy import (Column, BigInteger, SmallInteger, Boolean, ForeignKey)
from .meta import Base


class Cron(Base):
    __tablename__ = 'cron'
    id_cam = Column(BigInteger, ForeignKey('campaign.id'), primary_key=True)
    day = Column(SmallInteger)
    hour = Column(SmallInteger)
    min = Column(SmallInteger)
    startStop = Column(Boolean, primary_key=True)
