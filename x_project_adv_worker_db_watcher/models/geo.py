from sqlalchemy import (Column, Integer, BigInteger, ForeignKey, select, Index, cast)

from .__libs__.sql_view import create_view
from .meta import Base


class Geo(Base):
    __tablename__ = 'geo'
    id_cam = Column(BigInteger, ForeignKey('campaign.id', ondelete='CASCADE'), primary_key=True, nullable=False)
    id_geo = Column(Integer, ForeignKey('geo_lite_city.id', ondelete='CASCADE'), primary_key=True, nullable=False)

    __table_args__ = (
        {'prefixes': ['UNLOGGED']}
    )


class MVGeo(Base):
    __table__ = create_view(
        Base.metadata,
        'mv_geo',
        select([
            Geo.id_cam,
            Geo.id_geo
        ]).select_from(Geo),
        is_mat=True)


Index('ix_mv_domains_id_cam_pk_id_geo_pk', MVGeo.id_cam, MVGeo.id_geo, unique=True)
