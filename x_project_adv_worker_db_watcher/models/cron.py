from sqlalchemy import (Column, BigInteger, Integer, SmallInteger, Boolean, UniqueConstraint, Index, ForeignKey)
from sqlalchemy.orm import relationship
from .meta import Base


class Cron(Base):
    __tablename__ = 'cron'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cam = Column(BigInteger, ForeignKey('campaign.id'), nullable=False)
    day = Column(SmallInteger)
    hour = Column(SmallInteger)
    min = Column(SmallInteger)
    start_stop = Column(Boolean)
    campaign = relationship('Campaign', back_populates="cron")

    __table_args__ = (UniqueConstraint('id_cam', 'day', 'start_stop', name='id_cam_day_start_stop_uc'),
                      Index('day_hour_min', 'day', 'hour', 'min'))
