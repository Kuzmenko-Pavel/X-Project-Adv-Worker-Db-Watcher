from sqlalchemy import (Column, Integer, BigInteger, ForeignKey, select, Index, cast)

from .__libs__.sql_view import create_view
from .meta import Base


class Campaign2Device(Base):
    __tablename__ = 'campaign2device'
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_dev = Column(Integer, ForeignKey('device.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVCampaign2Device(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_campaign2device',
        select([
            Campaign2Device.id_cam,
            Campaign2Device.id_dev
        ]).select_from(Campaign2Device),
        is_mat=True)


Index('ix_mv_campaign2device__id_cam__id_dev',
      MVCampaign2Device.id_cam, MVCampaign2Device.id_dev, unique=True)
