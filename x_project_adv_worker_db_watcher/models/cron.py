from sqlalchemy import (Column, BigInteger, Integer, SmallInteger, Boolean, ForeignKey, select,
                        Index, cast)
from sqlalchemy.orm import relationship

from .__libs__.sql_view import create_view
from .meta import Base


class Cron(Base):
    __tablename__ = 'cron'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False)
    day = Column(SmallInteger)
    hour = Column(SmallInteger)
    min = Column(SmallInteger)
    start_stop = Column(Boolean)
    campaign = relationship('Campaign', back_populates="cron")

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVCron(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_cron',
        select([
            Cron.id,
            cast(Cron.id_cam, BigInteger).label('id_cam'),
            Cron.day,
            Cron.hour,
            Cron.min,
            Cron.start_stop
        ]).select_from(Cron),
        is_mat=True)


Index('ix_mv_cron_id', MVCron.id, unique=True)
Index('ix_mv_cron_id_cam_day_start_stop', MVCron.id_cam, MVCron.day, MVCron.start_stop)
Index('ix_mv_cron_day_hour_min', MVCron.day, MVCron.hour, MVCron.min)
