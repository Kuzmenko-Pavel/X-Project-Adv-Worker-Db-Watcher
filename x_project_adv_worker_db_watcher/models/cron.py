from sqlalchemy import (Column, BigInteger, SmallInteger, Boolean, ForeignKey, select,
                        Index, cast)
from sqlalchemy_utils import IntRangeType

from .__libs__.sql_view import create_view
from .meta import Base


class Cron(Base):
    __tablename__ = 'cron'
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    range = Column(SmallInteger, primary_key=True)
    day = Column(SmallInteger, primary_key=True)
    time = Column(IntRangeType)

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
            Cron.time,
        ]).select_from(Cron),
        is_mat=True)


Index('ix_mv_cron_id_cam_day_range', MVCron.id_cam, MVCron.day, MVCron.range, unique=True)
Index('ix_mv_cron_day_time', MVCron.day, MVCron.time)
Index('ix_mv_cron_time', MVCron.time, postgresql_using="gist")
