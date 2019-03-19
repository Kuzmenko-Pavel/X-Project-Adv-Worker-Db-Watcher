from sqlalchemy import (Column, BigInteger, SmallInteger, Boolean, ForeignKey, select,
                        Index, cast)

from .__libs__.sql_view import create_view
from .meta import Base


class Cron(Base):
    __tablename__ = 'cron'
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    range = Column(SmallInteger, primary_key=True)
    day = Column(SmallInteger, primary_key=True)
    hour = Column(SmallInteger)
    min = Column(SmallInteger)
    start_stop = Column(Boolean, primary_key=True)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVCron(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_cron',
        select([
            cast(Cron.id_cam, BigInteger).label('id_cam'),
            Cron.range,
            Cron.day,
            Cron.hour,
            Cron.min,
            Cron.start_stop
        ]).select_from(Cron),
        is_mat=True)


Index('ix_mv_cron_id_cam_day_start_stop', MVCron.id_cam, MVCron.day, MVCron.start_stop, MVCron.range, unique=True)
Index('ix_mv_cron_day_hour_min', MVCron.day, MVCron.hour, MVCron.min)
