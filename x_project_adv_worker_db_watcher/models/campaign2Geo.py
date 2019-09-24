from sqlalchemy import (Column, Integer, BigInteger, ForeignKey, select, Index, Boolean)

from .__libs__.sql_view import create_view
from .meta import Base


class Campaign2Geo(Base):
    __tablename__ = 'geo'
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_geo = Column(Integer, ForeignKey('geo_lite_city.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    change = Column(Boolean, default=False)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVCampaign2Geo(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_geo',
        select([
            Campaign2Geo.id_cam,
            Campaign2Geo.id_geo
        ]).select_from(Campaign2Geo),
        is_mat=True)


Index('ix_mv_geo_id_cam_pk_id_geo', MVCampaign2Geo.id_cam, MVCampaign2Geo.id_geo, unique=True)
